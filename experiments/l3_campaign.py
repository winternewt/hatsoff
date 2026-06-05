"""Overnight zero-mode percolation campaign (L3 + spatial spanning).

Resumable, self-calibrating, checkpointed driver. See the approved plan and
``docs/PERCOLATION.md``.

Stage A — scalar + Gallai--Edmonds scaling on the full L2/L3 graphs:
    nullity, deficiency, gap, GE structure (|D|,|A|,|C|, c(D), factor-critical
    component sizes), trapped modes.
Stage B — support spatial spanning (percolation) on crop windows of growing
    side L cut from the L3 patch: does the kernel support cross the window?

Robustness:
  * append-only JSONL checkpoint, fsynced per unit; restart skips done keys
  * deterministic seeds; p=0 computed once (no randomness)
  * each stage runs to a wall-clock budget then stops cleanly, recording all
    completed units; interleaved so every (level/window, p) gets balanced R
  * heartbeat file with progress/ETA; Stage A is aggregated before Stage B

Tunable via environment:
  HATSOFF_STAGE_A_HOURS (default 16), HATSOFF_STAGE_B_HOURS (default 24),
  HATSOFF_SMOKE=1 caps to a tiny run for the pre-flight check.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from types import SimpleNamespace

import networkx as nx
import numpy as np
import scipy.sparse

from hat_amp.graph import crop_square
from hat_amp.tiling import generate_tiling
from hatsoff.dilution import dilute_sites
from hatsoff.graph import build_tb_graph
from hatsoff.matching import (
    adjacency_to_graph,
    gallai_edmonds,
    matching_number,
)
from hatsoff.support import kernel_support, support_spanning

EXP_DIR = Path(__file__).parent
JSONL = EXP_DIR / "l3_campaign.jsonl"
HEARTBEAT = EXP_DIR / "l3_campaign.heartbeat"

P_GRID = [0.0, 0.02, 0.05, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30]
STAGE_A_LEVELS = [2, 3]
STAGE_B_LEVEL = 3
STAGE_B_FRACTIONS = [0.40, 0.55, 0.70, 0.85]

STAGE_A_HOURS = float(os.environ.get("HATSOFF_STAGE_A_HOURS", "16"))
STAGE_B_HOURS = float(os.environ.get("HATSOFF_STAGE_B_HOURS", "24"))
STAGE_A_MAX_R = 60
STAGE_B_MAX_R = 300
SMOKE = os.environ.get("HATSOFF_SMOKE") == "1"

THETA = 0.01
# Proximity linking distances (absolute; clean edges are 0.5 / 1.0 long).
# d0=1.0 connects almost nothing, d0=1.6 connects almost everything — the
# transition lives in between, so we record the whole range per unit and let
# the window finite-size family decide what (if anything) is a real crossing.
D0_LIST = [1.0, 1.2, 1.4, 1.6]
BOUNDARY_THICKNESS = 1.6
SEED_BASE = 20240605


def neighbors_from_adj(adjacency: scipy.sparse.spmatrix) -> list[np.ndarray]:
    csr = scipy.sparse.csr_matrix(adjacency)
    return [csr.indices[csr.indptr[i]:csr.indptr[i + 1]].astype(np.int32)
            for i in range(csr.shape[0])]


def adj_from_edges(n: int, edges: np.ndarray) -> scipy.sparse.csr_matrix:
    if edges.size == 0:
        return scipy.sparse.csr_matrix((n, n), dtype=np.float64)
    r = np.concatenate([edges[:, 0], edges[:, 1]])
    c = np.concatenate([edges[:, 1], edges[:, 0]])
    data = np.ones(r.shape[0], dtype=np.float64)
    return scipy.sparse.coo_matrix((data, (r, c)), shape=(n, n)).tocsr()


def factor_critical_sizes(graph: nx.Graph, d_nodes: np.ndarray) -> list[int]:
    if d_nodes.size == 0:
        return []
    sub = graph.subgraph(d_nodes.tolist())
    return [len(c) for c in nx.connected_components(sub)]


def rng_for(level: int, p: float, seed: int, tag: str = "") -> np.random.Generator:
    h = (SEED_BASE * 1_000_003
         + level * 100_003
         + int(round(p * 1000)) * 1009
         + seed * 31
         + (hash(tag) & 0xFFFF))
    return np.random.default_rng(abs(h) % (2**63))


def load_done(path: Path) -> set[str]:
    done: set[str] = set()
    if not path.exists():
        return done
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            done.add(json.loads(line)["key"])
    return done


def append_record(path: Path, record: dict) -> None:
    with path.open("a") as fh:
        fh.write(json.dumps(record) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def write_heartbeat(stage: str, done: int, started: float, budget_s: float) -> None:
    elapsed = time.time() - started
    frac = elapsed / budget_s if budget_s else 0.0
    HEARTBEAT.write_text(
        f"stage={stage} units_this_stage={done} "
        f"elapsed={elapsed / 3600:.2f}h / budget={budget_s / 3600:.1f}h "
        f"({frac * 100:.0f}%)\n"
    )


def stage_a_unit(level: int, graphs: dict, p: float, seed: int) -> dict:
    verts, adj = graphs[level]
    sv, sa, _ = dilute_sites(verts, adj, p, rng_for(level, p, seed, "A"))
    n = sa.shape[0]
    g = adjacency_to_graph(sa)
    ge = gallai_edmonds(g, method="fast")
    sizes = factor_critical_sizes(g, ge.D)
    n0, support = kernel_support(sa, expected=ge.deficiency)
    trapped = int(np.sum(support > 0.99))
    return {
        "stage": "A", "level": level, "window": "full", "L": None,
        "p": p, "seed": seed, "N": n,
        "nullity": n0, "deficiency": ge.deficiency, "gap": n0 - ge.deficiency,
        "nD": int(ge.D.size), "nA": int(ge.A.size), "nC": int(ge.C.size),
        "c_D": ge.n_critical_components,
        "max_critical": max(sizes) if sizes else 0,
        "n_critical_gt1": int(sum(1 for s in sizes if s > 1)),
        "trapped": trapped,
        "trapped_frac": float(support[support > 0.99].sum() / n0) if n0 else 0.0,
    }


def stage_b_unit(window, frac: float, p: float, seed: int) -> dict:
    n_w = window.node_count
    w_adj = adj_from_edges(n_w, window.edges)
    sv, sa, kept = dilute_sites(window.nodes, w_adj, p,
                                rng_for(STAGE_B_LEVEL, p, seed, f"B{frac}"))
    new_index = {int(old): new for new, old in enumerate(kept)}

    def remap(arr: np.ndarray) -> np.ndarray:
        return np.array([new_index[int(x)] for x in arr if int(x) in new_index],
                        dtype=int)

    top = remap(window.top_boundary_nodes)
    bottom = remap(window.bottom_boundary_nodes)
    left = remap(window.left_boundary_nodes)
    right = remap(window.right_boundary_nodes)

    nu = matching_number(adjacency_to_graph(sa))
    defv = sa.shape[0] - 2 * nu
    n0, support = kernel_support(sa, expected=defv)
    spanning: dict = {}
    n_active = 0
    for d0 in D0_LIST:
        s = support_spanning(sv, support, top, bottom, left, right, d0, THETA)
        n_active = s["n_active"]
        spanning[str(d0)] = {
            "either": s["either"], "top_bottom": s["top_bottom"],
            "left_right": s["left_right"],
            "max_cluster_frac": s["largest_cluster_frac"],
        }
    return {
        "stage": "B", "level": STAGE_B_LEVEL, "window": frac,
        "L": float(window.L_value), "p": p, "seed": seed,
        "N": int(n_w), "n_kept": int(sa.shape[0]),
        "nullity": n0, "deficiency": defv, "n_active": n_active,
        "spanning": spanning,
    }


def make_key(stage: str, level: int, window, p: float, seed: int) -> str:
    return f"{stage}|L{level}|w{window}|p{p}|s{seed}"


def safe_record(compute, key: str, stage: str, done: set[str]) -> None:
    """Run one unit, checkpoint it; on failure log an error record and go on.

    A stochastic numerical failure (e.g. a LAPACK non-convergence on one of
    thousands of realizations) must not abort the whole campaign.  The key is
    marked done either way so a resume does not re-hit a deterministic failure.
    """
    try:
        rec = compute()
    except Exception as exc:  # noqa: BLE001 - isolate any per-unit failure
        rec = {"stage": stage, "error": repr(exc)}
        print(f"UNIT FAILED {key}: {exc!r}", flush=True)
    rec["key"] = key
    append_record(JSONL, rec)
    done.add(key)


def run_stage_a(graphs: dict, done: set[str]) -> None:
    started = time.time()
    budget = STAGE_A_HOURS * 3600
    max_r = 1 if SMOKE else STAGE_A_MAX_R
    levels = [3] if SMOKE else STAGE_A_LEVELS
    pgrid = [0.0, 0.10] if SMOKE else P_GRID
    count = 0
    for r in range(max_r):
        seed = r
        for level in levels:
            for p in pgrid:
                if p == 0.0 and r > 0:
                    continue
                key = make_key("A", level, "full", p, seed)
                if key in done:
                    continue
                safe_record(lambda lv=level, pp=p, sd=seed:
                            stage_a_unit(lv, graphs, pp, sd), key, "A", done)
                count += 1
                write_heartbeat("A", count, started, budget)
                if not SMOKE and time.time() - started > budget:
                    return
        if SMOKE:
            return


def run_stage_b(graphs: dict, done: set[str]) -> None:
    started = time.time()
    budget = STAGE_B_HOURS * 3600
    verts, adj = graphs[STAGE_B_LEVEL]
    graphlike = SimpleNamespace(nodes=verts, neighbors=neighbors_from_adj(adj))
    extent = float(min(np.ptp(verts[:, 0]), np.ptp(verts[:, 1])))
    fractions = [0.55] if SMOKE else STAGE_B_FRACTIONS
    windows = {f: crop_square(graphlike, L=f * extent,
                              boundary_thickness=BOUNDARY_THICKNESS)
               for f in fractions}
    max_r = 1 if SMOKE else STAGE_B_MAX_R
    pgrid = [0.0, 0.10] if SMOKE else P_GRID
    count = 0
    for r in range(max_r):
        seed = r
        for frac in fractions:
            for p in pgrid:
                if p == 0.0 and r > 0:
                    continue
                key = make_key("B", STAGE_B_LEVEL, frac, p, seed)
                if key in done:
                    continue
                safe_record(lambda fr=frac, pp=p, sd=seed:
                            stage_b_unit(windows[fr], fr, pp, sd), key, "B", done)
                count += 1
                write_heartbeat("B", count, started, budget)
                if not SMOKE and time.time() - started > budget:
                    return
        if SMOKE:
            return


def main() -> None:
    t0 = time.time()
    print("building L2, L3 graphs...", flush=True)
    graphs = {lvl: build_tb_graph(generate_tiling(lvl)) for lvl in (2, 3)}
    print(f"graphs built in {time.time() - t0:.1f}s; d0_list={D0_LIST}", flush=True)

    done = load_done(JSONL)
    print(f"resume: {len(done)} units already done", flush=True)

    print("=== Stage A ===", flush=True)
    run_stage_a(graphs, done)
    print("=== Stage B ===", flush=True)
    run_stage_b(graphs, done)
    HEARTBEAT.write_text("done\n")
    print(f"campaign finished in {(time.time() - t0) / 3600:.2f}h", flush=True)


if __name__ == "__main__":
    main()

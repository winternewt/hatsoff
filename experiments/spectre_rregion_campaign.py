"""Spectre zero-flux R-region (Gallai--Edmonds) dilution campaign — the
comparative-figure counterpart of the hat `rregion_campaign.py`.

The thesis figure is hat vs Spectre vs periodic under site dilution, at **zero
flux**, with the parameter-free matching-theoretic order parameter (does a single
factor-critical / R-region component span the window?).  The hat data is
`l3_rregion.jsonl` (extensive clean R-region; de-percolates at finite p_c≈0.055);
the periodic control is `periodic_control.py`.  The Spectre piece was missing.

The strictly-chiral Spectre has **no clean R-region** (zero-flux nullity 0,
deficiency 0/1 parity); site dilution *creates* zero modes (onset).  This run
measures, across window sizes and vacancy density p: the matching **deficiency**
(cheap proxy for nullity, nullity≈deficiency) and whether the GE R-region spans —
i.e. does the dilution-created sector percolate, and from what p?

Identical harness to `rregion_campaign.py` (resumable JSONL, heartbeat,
`multiprocessing` across realizations — the GE blossom matching is pure-Python
single-threaded).  The only change is the substrate:
``build_tb_graph(strip_gold_vertex(generate_spectre_tiling(LEVEL)))`` — the
Schirmann-consistent natural Spectre fixed in `spectre_reconcile.py`.

    HATSOFF_NPROC=$(nproc) uv run python experiments/spectre_rregion_campaign.py
Writes ``experiments/spectre_rregion.jsonl`` + ``spectre_rregion.heartbeat``.

Tunable: ``HATSOFF_NPROC`` (default cores-1), ``HATSOFF_SPECTRE_RREGION_HOURS``
(default 3), ``HATSOFF_SPECTRE_RREGION_MAX_R`` (default 300),
``HATSOFF_SPECTRE_LEVEL`` (default 3), ``HATSOFF_SMOKE=1`` (tiny serial pre-flight).
"""

from __future__ import annotations

import multiprocessing as mp
import os
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from hat_amp.graph import crop_square
from hat_amp.spectre import generate_spectre_tiling, strip_gold_vertex
from hatsoff.dilution import dilute_sites
from hatsoff.graph import build_tb_graph
from hatsoff.matching import adjacency_to_graph, gallai_edmonds
from hatsoff.support import rregion_spanning
from l3_campaign import (
    BOUNDARY_THICKNESS,
    P_GRID,
    adj_from_edges,
    append_record,
    load_done,
    make_key,
    neighbors_from_adj,
    rng_for,
)

EXP_DIR = Path(__file__).parent
JSONL = EXP_DIR / "spectre_rregion.jsonl"
HEARTBEAT = EXP_DIR / "spectre_rregion.heartbeat"

LEVEL = int(os.environ.get("HATSOFF_SPECTRE_LEVEL", "3"))
FRACTIONS = [0.35, 0.45, 0.55, 0.65, 0.75, 0.85]

RREGION_HOURS = float(os.environ.get("HATSOFF_SPECTRE_RREGION_HOURS", "3"))
MAX_R = int(os.environ.get("HATSOFF_SPECTRE_RREGION_MAX_R", "300"))
SMOKE = os.environ.get("HATSOFF_SMOKE") == "1"
NPROC = int(os.environ.get("HATSOFF_NPROC", str(max(1, mp.cpu_count() - 1))))

_WINDOWS: dict[float, object] | None = None


def write_heartbeat(done: int, started: float, budget_s: float) -> None:
    elapsed = time.time() - started
    frac = elapsed / budget_s if budget_s else 0.0
    HEARTBEAT.write_text(
        f"stage=SR units={done} "
        f"elapsed={elapsed / 3600:.2f}h / budget={budget_s / 3600:.1f}h "
        f"({frac * 100:.0f}%)\n"
    )


def stage_r_unit(window, frac: float, p: float, seed: int) -> dict:
    n_w = window.node_count
    w_adj = adj_from_edges(n_w, window.edges)
    sv, sa, kept = dilute_sites(window.nodes, w_adj, p,
                               rng_for(LEVEL, p, seed, f"SR{frac}"))
    new_index = {int(old): new for new, old in enumerate(kept)}

    def remap(arr: np.ndarray) -> np.ndarray:
        return np.array([new_index[int(x)] for x in arr if int(x) in new_index],
                        dtype=int)

    top = remap(window.top_boundary_nodes)
    bottom = remap(window.bottom_boundary_nodes)
    left = remap(window.left_boundary_nodes)
    right = remap(window.right_boundary_nodes)

    g = adjacency_to_graph(sa)
    ge = gallai_edmonds(g, method="fast")
    span = rregion_spanning(g, ge.D, top, bottom, left, right)
    return {
        "stage": "SR", "level": LEVEL, "window": frac,
        "L": float(window.L_value), "p": p, "seed": seed,
        "N": int(n_w), "n_kept": int(sa.shape[0]),
        "deficiency": int(ge.deficiency), "n_dnodes": span["n_dnodes"],
        "n_components": span["n_components"],
        "spanning": {
            "either": span["either"], "top_bottom": span["top_bottom"],
            "left_right": span["left_right"],
            "largest_comp_frac": span["largest_comp_frac"],
        },
    }


def _init_worker(fractions: list[float]) -> None:
    """Build the Spectre graph + crop windows once per worker process."""
    global _WINDOWS
    verts, adj = build_tb_graph(strip_gold_vertex(generate_spectre_tiling(LEVEL)))
    graphlike = SimpleNamespace(nodes=verts, neighbors=neighbors_from_adj(adj))
    extent = float(min(np.ptp(verts[:, 0]), np.ptp(verts[:, 1])))
    _WINDOWS = {f: crop_square(graphlike, L=f * extent,
                               boundary_thickness=BOUNDARY_THICKNESS)
                for f in fractions}


def _compute(task: tuple[float, float, int, str]) -> dict:
    frac, p, seed, key = task
    try:
        rec = stage_r_unit(_WINDOWS[frac], frac, p, seed)
    except Exception as exc:  # noqa: BLE001 - isolate any per-unit failure
        rec = {"stage": "SR", "error": repr(exc)}
        print(f"UNIT FAILED {key}: {exc!r}", flush=True)
    rec["key"] = key
    return rec


def pending_units(done: set[str], fractions: list[float], pgrid: list[float],
                  max_r: int):
    """Seed-major so an early stop leaves every (window, p) cell balanced."""
    for r in range(max_r):
        for frac in fractions:
            for p in pgrid:
                if p == 0.0 and r > 0:
                    continue
                key = make_key("SR", LEVEL, frac, p, r)
                if key not in done:
                    yield (frac, p, r, key)


def main() -> None:
    t0 = time.time()
    fractions = [0.55] if SMOKE else FRACTIONS
    pgrid = [0.0, 0.05, 0.10] if SMOKE else P_GRID
    max_r = 1 if SMOKE else MAX_R
    nproc = 1 if SMOKE else NPROC

    done = load_done(JSONL)
    print(f"resume: {len(done)} units already done; nproc={nproc}; level={LEVEL}",
          flush=True)

    started = time.time()
    budget = RREGION_HOURS * 3600
    units = pending_units(done, fractions, pgrid, max_r)
    count = 0

    def over_budget() -> bool:
        return not SMOKE and time.time() - started > budget

    if nproc == 1:
        _init_worker(fractions)
        for task in units:
            append_record(JSONL, _compute(task))
            count += 1
            write_heartbeat(count, started, budget)
            if over_budget():
                break
    else:
        with mp.Pool(nproc, initializer=_init_worker,
                     initargs=(fractions,)) as pool:
            for rec in pool.imap_unordered(_compute, units, chunksize=1):
                append_record(JSONL, rec)
                count += 1
                write_heartbeat(count, started, budget)
                if over_budget():
                    pool.terminate()
                    break

    HEARTBEAT.write_text("done\n")
    print(f"spectre rregion campaign finished {count} new units in "
          f"{(time.time() - t0) / 3600:.2f}h", flush=True)


if __name__ == "__main__":
    main()

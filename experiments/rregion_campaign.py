"""Rigorous R-region (Gallai--Edmonds) spanning campaign — the non-proxy
cross-check of finding #4, with a denser window-size family for a genuine nu.

For each crop window and site-removal probability we ask the **parameter-free**
question (no d0, no theta, no eigendecomposition): does a single factor-critical
("blossom") component of the Gallai--Edmonds inessential set ``D`` span the
window?  This is the matching-theoretic R-region order parameter of
Bhola--Damle, here on the aperiodic hat substrate.

It reuses the *exact* deterministic disorder realizations of the Stage-B proxy
run (same ``rng_for(..., f"B{frac}")`` seeds) for the four shared window
fractions, so the rigorous ``p_c(L)`` overlays the proxy directly; four extra
fractions extend the size lever-arm.  Per unit it needs only
``gallai_edmonds`` (blossom forest, ~N^1.9) — far cheaper than the proxy's
O(N^3) dense ``eigh``.

Resumable / checkpointed exactly like ``l3_campaign.py``:
    uv run python experiments/rregion_campaign.py
Writes ``experiments/l3_rregion.jsonl`` + ``l3_rregion.heartbeat``.

**Parallel:** unlike the proxy campaign (whose dense ``eigh`` was already
BLAS-multithreaded), the per-unit work here is pure-Python (blossom matching +
union-find) and single-threaded, so it is fanned across cores by realization
with a ``multiprocessing.Pool`` (``NPROC = cpu_count()-1`` workers; each builds
the windows once via the Pool initializer; the parent is the sole JSONL writer).
Deterministic ``rng_for`` seeds make the parallel result identical to serial.

Tunable: ``HATSOFF_NPROC`` (default cores-1), ``HATSOFF_RREGION_HOURS``
(default 16), ``HATSOFF_RREGION_MAX_R`` (default 300), ``HATSOFF_SMOKE=1`` (tiny,
serial pre-flight).
"""

from __future__ import annotations

import multiprocessing as mp
import os
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from hat_amp.graph import crop_square
from hat_amp.tiling import generate_tiling
from hatsoff.dilution import dilute_sites
from hatsoff.graph import build_tb_graph
from hatsoff.matching import adjacency_to_graph, gallai_edmonds
from hatsoff.support import rregion_spanning
from l3_campaign import (
    BOUNDARY_THICKNESS,
    P_GRID,
    STAGE_B_LEVEL,
    adj_from_edges,
    append_record,
    load_done,
    make_key,
    neighbors_from_adj,
    rng_for,
)

EXP_DIR = Path(__file__).parent
JSONL = EXP_DIR / "l3_rregion.jsonl"
HEARTBEAT = EXP_DIR / "l3_rregion.heartbeat"

# Existing Stage-B fractions reuse identical seeds (direct overlay); the four
# interleaved fractions extend the finite-size family for the nu fit.
FRACTIONS = [0.30, 0.40, 0.475, 0.55, 0.625, 0.70, 0.775, 0.85]
SHARED_FRACTIONS = {0.40, 0.55, 0.70, 0.85}

RREGION_HOURS = float(os.environ.get("HATSOFF_RREGION_HOURS", "16"))
RREGION_MAX_R = 300
SMOKE = os.environ.get("HATSOFF_SMOKE") == "1"
# Per-unit work is pure-Python (blossom matching + union-find), single-threaded
# and BLAS-free — so it parallelizes cleanly across cores by realization, unlike
# the proxy campaign whose dense eigh was already BLAS-multithreaded.
NPROC = int(os.environ.get("HATSOFF_NPROC", str(max(1, mp.cpu_count() - 1))))

# Per-worker window cache (built once per process via the Pool initializer).
_WINDOWS: dict[float, object] | None = None


def write_heartbeat(done: int, started: float, budget_s: float) -> None:
    elapsed = time.time() - started
    frac = elapsed / budget_s if budget_s else 0.0
    HEARTBEAT.write_text(
        f"stage=R units={done} "
        f"elapsed={elapsed / 3600:.2f}h / budget={budget_s / 3600:.1f}h "
        f"({frac * 100:.0f}%)\n"
    )


def stage_r_unit(window, frac: float, p: float, seed: int) -> dict:
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

    g = adjacency_to_graph(sa)
    ge = gallai_edmonds(g, method="fast")
    span = rregion_spanning(g, ge.D, top, bottom, left, right)
    return {
        "stage": "R", "level": STAGE_B_LEVEL, "window": frac,
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
    """Build the L3 graph + crop windows once per worker process."""
    global _WINDOWS
    verts, adj = build_tb_graph(generate_tiling(STAGE_B_LEVEL))
    graphlike = SimpleNamespace(nodes=verts, neighbors=neighbors_from_adj(adj))
    extent = float(min(np.ptp(verts[:, 0]), np.ptp(verts[:, 1])))
    _WINDOWS = {f: crop_square(graphlike, L=f * extent,
                               boundary_thickness=BOUNDARY_THICKNESS)
                for f in fractions}


def _compute(task: tuple[float, float, int, str]) -> dict:
    """Run one (window, p, seed) unit; isolate any per-unit failure."""
    frac, p, seed, key = task
    try:
        rec = stage_r_unit(_WINDOWS[frac], frac, p, seed)
    except Exception as exc:  # noqa: BLE001 - isolate any per-unit failure
        rec = {"stage": "R", "error": repr(exc)}
        print(f"UNIT FAILED {key}: {exc!r}", flush=True)
    rec["key"] = key
    return rec


def pending_units(done: set[str], fractions: list[float], pgrid: list[float],
                  max_r: int):
    """Yield (frac, p, seed, key) for every not-yet-done unit, seed-major so an
    early stop still leaves every (window, p) cell with a balanced seed count."""
    for r in range(max_r):
        for frac in fractions:
            for p in pgrid:
                if p == 0.0 and r > 0:
                    continue
                key = make_key("R", STAGE_B_LEVEL, frac, p, r)
                if key not in done:
                    yield (frac, p, r, key)


def main() -> None:
    t0 = time.time()
    fractions = [0.55] if SMOKE else FRACTIONS
    pgrid = [0.0, 0.05, 0.10] if SMOKE else P_GRID
    max_r = 1 if SMOKE else RREGION_MAX_R
    nproc = 1 if SMOKE else NPROC

    done = load_done(JSONL)
    print(f"resume: {len(done)} units already done; nproc={nproc}", flush=True)

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
    print(f"rregion campaign finished {count} new units in "
          f"{(time.time() - t0) / 3600:.2f}h", flush=True)


if __name__ == "__main__":
    main()

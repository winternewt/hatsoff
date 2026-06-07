"""π-flux Spectre support-SPANNING probe — transition-vs-crossover (CAVEATED).

Companion to `spectre_flux_campaign.py`. That run measured Mystic localization and
nullity; this one asks whether the π-flux zero-mode **support spatially spans** a
window under dilution, to look at the enrichment→1 crossover as a possible
de-percolation.

⚠ **Epistemic caveat (read before trusting any p_c here).** At π flux the matrix
is complex Hermitian, so the rigorous, parameter-free Gallai--Edmonds R-region
probe **does not apply** — the *only* spanning tool is the geometric proximity
proxy `support_spanning(d0)`, which is exactly the probe that **faked p_c→0** on
the zero-flux hat (see CLAUDE.md / CAMPAIGN_REPORT). There is no matching-theoretic
cross-check available at π flux. So this campaign records several `d0` and the full
window finite-size family (per the "never read a single-d0 p_c as physical" rule),
and its output is **suggestive, not a verdict**. The safe statement remains the
size-independent enrichment crossover (p*≈0.15, `spectre_flux_consolidate.py`).

Per (window, p, seed): dilute the Schirmann-consistent Spectre window, build the
π-flux Hamiltonian, get the kernel support diag(P) via the RRR value-subset, and
run `support_spanning` over `D0_LIST`. Resumable JSONL + heartbeat; BLAS pinned
to 1, parallel across realizations.

    OPENBLAS_NUM_THREADS=1 HATSOFF_NPROC=$(nproc) \
        uv run python experiments/spectre_flux_spanning_campaign.py
Writes `experiments/spectre_flux_spanning.jsonl` + `.heartbeat`.

Tunable: HATSOFF_NPROC, HATSOFF_SPECTRE_SPAN_HOURS (default 3),
HATSOFF_SPECTRE_SPAN_MAX_R (default 150), HATSOFF_SMOKE=1.
"""

from __future__ import annotations

import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import multiprocessing as mp  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402
from types import SimpleNamespace  # noqa: E402

import numpy as np  # noqa: E402
import scipy.linalg  # noqa: E402

from hat_amp.graph import crop_square  # noqa: E402
from hat_amp.spectre import generate_spectre_tiling, strip_gold_vertex  # noqa: E402
from hatsoff.dilution import dilute_sites  # noqa: E402
from hatsoff.flux import build_flux_hamiltonian, tile_area  # noqa: E402
from hatsoff.graph import build_tb_graph  # noqa: E402
from hatsoff.support import support_spanning  # noqa: E402
from l3_campaign import (  # noqa: E402
    BOUNDARY_THICKNESS,
    adj_from_edges,
    append_record,
    load_done,
    make_key,
    neighbors_from_adj,
    rng_for,
)

EXP_DIR = Path(__file__).parent
JSONL = EXP_DIR / "spectre_flux_spanning.jsonl"
HEARTBEAT = EXP_DIR / "spectre_flux_spanning.heartbeat"

LEVEL = int(os.environ.get("HATSOFF_SPECTRE_LEVEL", "3"))
FRACTIONS = [0.50, 0.65, 0.80, 0.95]
P_GRID = [0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30, 0.40]
D0_LIST = [1.2, 1.6, 2.0]  # Spectre edges are ~unit length; transition in between
THETA = 0.01
KERNEL_WINDOW = 1e-6

SPAN_HOURS = float(os.environ.get("HATSOFF_SPECTRE_SPAN_HOURS", "3"))
MAX_R = int(os.environ.get("HATSOFF_SPECTRE_SPAN_MAX_R", "150"))
SMOKE = os.environ.get("HATSOFF_SMOKE") == "1"
NPROC = int(os.environ.get("HATSOFF_NPROC", str(max(1, mp.cpu_count() - 1))))

_STATE: dict | None = None


def write_heartbeat(done: int, started: float, budget_s: float) -> None:
    elapsed = time.time() - started
    HEARTBEAT.write_text(
        f"stage=SPAN units={done} elapsed={elapsed / 3600:.2f}h "
        f"/ budget={budget_s / 3600:.1f}h "
        f"({100 * elapsed / budget_s if budget_s else 0:.0f}%)\n"
    )


def _build_state() -> dict:
    verts, adj = build_tb_graph(strip_gold_vertex(generate_spectre_tiling(LEVEL)))
    area = tile_area(strip_gold_vertex(generate_spectre_tiling(LEVEL))[0])
    graphlike = SimpleNamespace(nodes=verts, neighbors=neighbors_from_adj(adj))
    extent = float(min(np.ptp(verts[:, 0]), np.ptp(verts[:, 1])))
    windows = {f: crop_square(graphlike, L=f * extent,
                              boundary_thickness=BOUNDARY_THICKNESS)
               for f in FRACTIONS}
    return {"area": area, "windows": windows}


def flux_unit(frac: float, p: float, seed: int) -> dict:
    st = _STATE
    win = st["windows"][frac]
    n_w = win.node_count
    w_adj = adj_from_edges(n_w, win.edges)
    sv, sa, kept = dilute_sites(win.nodes, w_adj, p, rng_for(LEVEL, p, seed, f"SP{frac}"))
    new_index = {int(old): new for new, old in enumerate(kept)}

    def remap(arr: np.ndarray) -> np.ndarray:
        return np.array([new_index[int(x)] for x in arr if int(x) in new_index],
                        dtype=int)

    top = remap(win.top_boundary_nodes)
    bottom = remap(win.bottom_boundary_nodes)
    left = remap(win.left_boundary_nodes)
    right = remap(win.right_boundary_nodes)

    h = build_flux_hamiltonian(sv, sa, st["area"], flux=np.pi).toarray()
    _, evecs = scipy.linalg.eigh(
        h, driver="evr", subset_by_value=(-KERNEL_WINDOW, KERNEL_WINDOW))
    nullity = int(evecs.shape[1])
    support = (np.einsum("ij,ij->i", evecs.conj(), evecs).real
               if nullity else np.zeros(sa.shape[0]))

    span = {}
    for d0 in D0_LIST:
        r = support_spanning(sv, support, top, bottom, left, right, d0=d0, theta=THETA)
        span[str(d0)] = {"either": bool(r["either"]),
                         "largest_cluster_frac": float(r["largest_cluster_frac"]),
                         "n_active": int(r["n_active"])}

    return {
        "stage": "SPAN", "level": LEVEL, "window": frac,
        "L": float(win.L_value), "p": p, "seed": seed,
        "N": int(n_w), "n_kept": int(sa.shape[0]), "nullity": nullity,
        "span": span,
    }


def _init_worker() -> None:
    global _STATE
    _STATE = _build_state()


def _compute(task: tuple) -> dict:
    frac, p, seed, key = task
    try:
        rec = flux_unit(frac, p, seed)
    except Exception as exc:  # noqa: BLE001
        rec = {"stage": "SPAN", "error": repr(exc)}
        print(f"UNIT FAILED {key}: {exc!r}", flush=True)
    rec["key"] = key
    return rec


def pending_units(done: set[str], fractions: list[float], pgrid: list[float],
                  max_r: int):
    for r in range(max_r):
        for frac in fractions:
            for p in pgrid:
                if p == 0.0 and r > 0:
                    continue
                key = make_key("SPAN", LEVEL, frac, p, r)
                if key not in done:
                    yield (frac, p, r, key)


def main() -> None:
    t0 = time.time()
    fractions = [0.50] if SMOKE else FRACTIONS
    pgrid = [0.0, 0.1, 0.2] if SMOKE else P_GRID
    max_r = 1 if SMOKE else MAX_R
    nproc = 1 if SMOKE else NPROC

    done = load_done(JSONL)
    print(f"resume: {len(done)} done; nproc={nproc}; level={LEVEL}; d0={D0_LIST}",
          flush=True)
    started = time.time()
    budget = SPAN_HOURS * 3600
    units = pending_units(done, fractions, pgrid, max_r)
    count = 0

    def over_budget() -> bool:
        return not SMOKE and time.time() - started > budget

    if nproc == 1:
        _init_worker()
        for task in units:
            append_record(JSONL, _compute(task))
            count += 1
            write_heartbeat(count, started, budget)
            if over_budget():
                break
    else:
        with mp.Pool(nproc, initializer=_init_worker) as pool:
            for rec in pool.imap_unordered(_compute, units, chunksize=1):
                append_record(JSONL, rec)
                count += 1
                write_heartbeat(count, started, budget)
                if over_budget():
                    pool.terminate()
                    break

    HEARTBEAT.write_text("done\n")
    print(f"spanning probe finished {count} new units in "
          f"{(time.time() - t0) / 3600:.2f}h", flush=True)


if __name__ == "__main__":
    main()

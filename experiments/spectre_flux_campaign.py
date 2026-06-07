"""π-flux Spectre site-dilution campaign — the rich (Mystic) sector.

The zero-flux pipeline found the strictly-chiral Spectre has *no* clean zero
modes (``docs/SPECTRE_TODO.md``); the rich physics Schirmann/Singh--Flicker
describe lives at **π flux** (Mystic-localized modes).  ``spectre_reconcile.py``
fixed the construction (natural, gold stripped, hat-style long-edge treatment =
``build_tb_graph``; the count gate ``tests/test_flux.py`` proves it equals
Schirmann's convention) and showed clean π-flux nullity tracks the Mystic count.

This campaign asks what site dilution does to that π-flux Mystic sector:

  * **nullity vs p** — does dilution create / destroy π-flux zero modes?
  * **Mystic localization** — fraction of kernel support ``diag(P)`` sitting on
    Mystic ('M') sites; tests the Mystic-nucleation conjecture (Singh--Flicker:
    matching freedom lives on Upper Mystics).
  * **support participation** — gauge-invariant localization of the kernel
    (PR of the ``diag(P)`` field; per-mode IPR is *not* gauge-invariant inside a
    degenerate subspace, ``diag(P)`` is — see CLAUDE.md).

Run on the L3 Spectre full graph plus cropped windows of growing side L for
finite-size scaling, over a p-grid × seeds.

Per-unit cost is a **dense complex Hermitian ``eigh``**, but only the *kernel*
eigenpairs are needed, so it uses the RRR driver with a value subset
(``scipy.linalg.eigh(driver='evr', subset_by_value=(-w, w))``) — ~10-50× cheaper
than a full spectrum and, unlike sparse ``eigsh``, it resolves the deeply
degenerate null space reliably.  Like ``rregion_campaign.py`` it parallelizes
across realizations with ``multiprocessing`` and pins BLAS to one thread per
worker (set ``OPENBLAS_NUM_THREADS=1`` — done at import below for forked workers).

Resumable / checkpointed exactly like ``l3_campaign.py``:
    OPENBLAS_NUM_THREADS=1 HATSOFF_NPROC=$(nproc) \
        uv run python experiments/spectre_flux_campaign.py
Writes ``experiments/spectre_flux_campaign.jsonl`` + ``.heartbeat``.

Tunable: ``HATSOFF_NPROC`` (default cores-1), ``HATSOFF_SPECTRE_FLUX_HOURS``
(default 12), ``HATSOFF_SPECTRE_MAX_R`` (default 200), ``HATSOFF_SPECTRE_LEVEL``
(default 3), ``HATSOFF_SMOKE=1`` (tiny serial pre-flight).
"""

from __future__ import annotations

import os

# Pin BLAS to one thread BEFORE numpy/scipy import so forked workers inherit it;
# throughput comes from many single-threaded eigh processes, not threaded BLAS.
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import multiprocessing as mp  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402
from types import SimpleNamespace  # noqa: E402

import numpy as np  # noqa: E402
import scipy.linalg  # noqa: E402
import scipy.sparse  # noqa: E402

from hat_amp.graph import crop_square  # noqa: E402
from hat_amp.spectre import (  # noqa: E402
    generate_spectre_tiling_labeled,
    strip_gold_vertex,
)
from hatsoff.dilution import dilute_sites  # noqa: E402
from hatsoff.flux import build_flux_hamiltonian, label_vertex_mask, tile_area  # noqa: E402
from hatsoff.graph import build_tb_graph  # noqa: E402
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
JSONL = EXP_DIR / "spectre_flux_campaign.jsonl"
HEARTBEAT = EXP_DIR / "spectre_flux_campaign.heartbeat"

LEVEL = int(os.environ.get("HATSOFF_SPECTRE_LEVEL", "3"))
# Window side as a fraction of the patch extent; "full" = whole graph.  A dense
# size family (7 windows) gives a genuine finite-size lever-arm for the nullity
# density / Mystic-enrichment scaling.
FRACTIONS: list[float | str] = [0.40, 0.50, 0.60, 0.70, 0.80, 0.90, "full"]
# Fine p-grid to resolve the onset / any de-percolation of the Mystic sector.
P_GRID = [0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.15, 0.18,
          0.20, 0.25, 0.30, 0.35, 0.40]

FLUX_HOURS = float(os.environ.get("HATSOFF_SPECTRE_FLUX_HOURS", "12"))
# Seed ceiling; the wall-clock budget normally stops the run first.  Seed-major
# iteration keeps every (window, p) cell balanced under an early stop.
MAX_R = int(os.environ.get("HATSOFF_SPECTRE_MAX_R", "1000"))
SMOKE = os.environ.get("HATSOFF_SMOKE") == "1"
NPROC = int(os.environ.get("HATSOFF_NPROC", str(max(1, mp.cpu_count() - 1))))
KERNEL_WINDOW = 1e-6  # |E| < KERNEL_WINDOW counts as a zero mode

# Per-worker cache, built once per process via the Pool initializer.
_STATE: dict | None = None


def write_heartbeat(done: int, started: float, budget_s: float) -> None:
    elapsed = time.time() - started
    frac = elapsed / budget_s if budget_s else 0.0
    HEARTBEAT.write_text(
        f"stage=FLUX units={done} "
        f"elapsed={elapsed / 3600:.2f}h / budget={budget_s / 3600:.1f}h "
        f"({frac * 100:.0f}%)\n"
    )


def edges_from_adj(adjacency: scipy.sparse.spmatrix) -> np.ndarray:
    """Upper-triangle (i, j) edge list from a symmetric adjacency."""
    upper = scipy.sparse.triu(scipy.sparse.csr_matrix(adjacency), k=1).tocoo()
    return np.column_stack([upper.row, upper.col]).astype(np.int64)


def _build_state() -> dict:
    """Full Spectre graph + Mystic mask + cropped windows (nodes/edges only)."""
    polys14, labels = generate_spectre_tiling_labeled(LEVEL)
    polys13 = strip_gold_vertex(polys14)
    verts, adj = build_tb_graph(polys13)
    area = tile_area(polys13[0])

    graphlike = SimpleNamespace(nodes=verts, neighbors=neighbors_from_adj(adj))
    extent = float(min(np.ptp(verts[:, 0]), np.ptp(verts[:, 1])))

    windows: dict = {}
    for frac in FRACTIONS:
        if frac == "full":
            nodes, edges, lval = verts, edges_from_adj(adj), extent
        else:
            w = crop_square(graphlike, L=frac * extent,
                            boundary_thickness=BOUNDARY_THICKNESS)
            nodes, edges, lval = w.nodes, w.edges, float(w.L_value)
        windows[frac] = SimpleNamespace(nodes=nodes, edges=edges, L_value=lval,
                                        node_count=len(nodes))
    return {"polys13": polys13, "labels": labels, "area": area, "windows": windows}


def flux_unit(frac: float | str, p: float, seed: int) -> dict:
    st = _STATE
    win = st["windows"][frac]
    n_w = win.node_count
    w_adj = adj_from_edges(n_w, win.edges)
    sv, sa, _ = dilute_sites(win.nodes, w_adj, p, rng_for(LEVEL, p, seed, f"F{frac}"))

    h = build_flux_hamiltonian(sv, sa, st["area"], flux=np.pi).toarray()
    evals, evecs = scipy.linalg.eigh(
        h, driver="evr", subset_by_value=(-KERNEL_WINDOW, KERNEL_WINDOW)
    )
    nullity = int(evals.size)

    mystic = label_vertex_mask(sv, st["polys13"], st["labels"], "M")
    n_mystic = int(mystic.sum())
    if nullity > 0:
        support = np.einsum("ij,ij->i", evecs.conj(), evecs).real  # diag(P), gauge-inv.
        total = float(support.sum())
        mystic_support_frac = float(support[mystic].sum() / total) if total else 0.0
        # PR of the support field (gauge-invariant localization of the kernel).
        support_pr = float(total**2 / np.sum(support**2)) if np.any(support) else 0.0
    else:
        mystic_support_frac = 0.0
        support_pr = 0.0

    return {
        "stage": "FLUX", "level": LEVEL, "window": frac,
        "L": float(win.L_value), "p": p, "seed": seed,
        "N": int(n_w), "n_kept": int(sa.shape[0]),
        "nullity": nullity, "n_mystic": n_mystic,
        "mystic_support_frac": mystic_support_frac, "support_pr": support_pr,
    }


def _init_worker() -> None:
    global _STATE
    _STATE = _build_state()


def _compute(task: tuple) -> dict:
    frac, p, seed, key = task
    try:
        rec = flux_unit(frac, p, seed)
    except Exception as exc:  # noqa: BLE001 - isolate any per-unit failure
        rec = {"stage": "FLUX", "error": repr(exc)}
        print(f"UNIT FAILED {key}: {exc!r}", flush=True)
    rec["key"] = key
    return rec


def pending_units(done: set[str], fractions: list, pgrid: list[float], max_r: int):
    """Seed-major so an early stop leaves every (window, p) cell balanced."""
    for r in range(max_r):
        for frac in fractions:
            for p in pgrid:
                if p == 0.0 and r > 0:
                    continue
                key = make_key("FLUX", LEVEL, frac, p, r)
                if key not in done:
                    yield (frac, p, r, key)


def main() -> None:
    t0 = time.time()
    fractions = [0.55] if SMOKE else FRACTIONS
    pgrid = [0.0, 0.1, 0.3] if SMOKE else P_GRID
    max_r = 1 if SMOKE else MAX_R
    nproc = 1 if SMOKE else NPROC

    done = load_done(JSONL)
    print(f"resume: {len(done)} units already done; nproc={nproc}; level={LEVEL}",
          flush=True)

    started = time.time()
    budget = FLUX_HOURS * 3600
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
    print(f"spectre flux campaign finished {count} new units in "
          f"{(time.time() - t0) / 3600:.2f}h", flush=True)


if __name__ == "__main__":
    main()

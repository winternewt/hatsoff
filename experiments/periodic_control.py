"""Periodic-lattice control: the SAME spanning pipeline on a triangular lattice.

The "not a pipeline artifact" check for finding #4 — and a clarifying regime
comparison.  We run our own ``rregion_spanning`` on triangular crop windows
under site dilution and compare to the hat.  What the data shows:

* **Triangular (perfectly matchable, periodic, non-bipartite):** at the clean
  point deficiency = 0 → **no R-region, no spanning** (the code correctly finds
  nothing where there is nothing).  Under dilution an R-region appears; the
  binary D-spanning probe is then dominated by (i) a *parity* plateau at low p
  (odd # sites → def=1 → the whole connected graph is factor-critical →
  trivially spans ~half the realizations) and (ii) loss of spanning near
  p≈0.55, which is just the triangular *site-percolation* threshold (the lattice
  itself fragments).  So the binary probe does **not** cleanly isolate the
  Bhola--Damle intermediate R-region p_c at accessible sizes — that needs their
  larger-scale, parity-controlled finite-size scaling.
* **Hat (the real result):** an **extensive** clean-limit null space (51 zero
  modes at L3) → the R-region **spans at p=0** and dilution *destroys* it
  (p_c → 0).

The decisive, parity-free contrast is therefore at the **clean point** and in
the **deficiency density**: the hat carries an extensive spanning R-region at
p=0; the periodic lattice carries none.  The regimes are opposite — periodic
lattices *create* an R-region with dilution (finite-p onset), the hat *loses*
one (p_c → 0).  Same code on both ⇒ the hat's behaviour is a property of the
substrate, not a bug.

    uv run python experiments/periodic_control.py
Writes ``docs/figures/periodic_control.png``, prints P_span / deficiency density /
largest-R-region fraction vs (p, L), and emits per-unit records to
``experiments/periodic_rregion.jsonl`` in the same schema as ``l3_rregion.jsonl``
and ``spectre_rregion.jsonl`` (``stage``/``window``/``L``/``p``/``seed``/``N``/
``n_kept``/``deficiency``/``spanning{either,largest_comp_frac}``) so the periodic
control overlays directly in ``spectre_vs_hat_rregion.py``.
Tunable: ``HATSOFF_CTRL_SEEDS`` (default 40), ``HATSOFF_CTRL_M`` (lattice rows,
default 64).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from types import SimpleNamespace

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import scipy.sparse

from hat_amp.graph import crop_square
from hatsoff.dilution import dilute_sites
from hatsoff.matching import adjacency_to_graph, gallai_edmonds
from hatsoff.support import rregion_spanning

EXP_DIR = Path(__file__).parent
FIG = EXP_DIR.parent / "docs" / "figures" / "periodic_control.png"
JSONL = EXP_DIR / "periodic_rregion.jsonl"
P_GRID = [0.0, 0.02, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.55, 0.60]
FRACTIONS = [0.45, 0.60, 0.75, 0.90]
SEEDS = int(os.environ.get("HATSOFF_CTRL_SEEDS", "40"))
LATTICE_ROWS = int(os.environ.get("HATSOFF_CTRL_M", "64"))
BOUNDARY_THICKNESS = 1.2


def triangular_graphlike(rows: int, cols: int) -> SimpleNamespace:
    """Integer-indexed triangular lattice with a positions array + adjacency."""
    g = nx.triangular_lattice_graph(rows, cols)
    labels = list(g.nodes())
    index = {lab: i for i, lab in enumerate(labels)}
    positions = np.array([g.nodes[lab]["pos"] for lab in labels], dtype=float)
    neighbors = [np.array([index[w] for w in g.neighbors(lab)], dtype=np.int32)
                 for lab in labels]
    return SimpleNamespace(nodes=positions, neighbors=neighbors)


def adj_from_edges(n: int, edges: np.ndarray) -> scipy.sparse.csr_matrix:
    if edges.size == 0:
        return scipy.sparse.csr_matrix((n, n), dtype=np.float64)
    r = np.concatenate([edges[:, 0], edges[:, 1]])
    c = np.concatenate([edges[:, 1], edges[:, 0]])
    data = np.ones(r.shape[0], dtype=np.float64)
    return scipy.sparse.coo_matrix((data, (r, c)), shape=(n, n)).tocsr()


def unit_record(window, frac: float, p: float, seed: int,
                w_adj: scipy.sparse.csr_matrix) -> dict:
    """One (window, p, seed) record in the shared rregion-campaign schema."""
    rng = np.random.default_rng(10_000 + seed * 7 + int(round(p * 1000)))
    sv, sa, kept = dilute_sites(window.nodes, w_adj, p, rng)
    new_index = {int(old): new for new, old in enumerate(kept)}

    def remap(arr: np.ndarray) -> np.ndarray:
        return np.array([new_index[int(x)] for x in arr
                         if int(x) in new_index], dtype=int)

    g = adjacency_to_graph(sa)
    ge = gallai_edmonds(g, method="fast")
    r = rregion_spanning(g, ge.D,
                         remap(window.top_boundary_nodes),
                         remap(window.bottom_boundary_nodes),
                         remap(window.left_boundary_nodes),
                         remap(window.right_boundary_nodes))
    return {
        "stage": "P", "window": frac, "L": float(window.L_value),
        "p": p, "seed": seed, "N": int(window.node_count),
        "n_kept": int(sa.shape[0]), "deficiency": int(ge.deficiency),
        "spanning": {"either": bool(r["either"]),
                     "largest_comp_frac": float(r["largest_comp_frac"])},
        "key": f"P|tri|w{frac}|p{p}|s{seed}",
    }


def window_stats(window, frac: float, p: float, seeds: int,
                 records: list[dict]) -> dict:
    """Mean spanning prob, deficiency density, largest-R-region fraction.

    Appends each per-seed record (shared schema) to ``records``.
    """
    w_adj = adj_from_edges(window.node_count, window.edges)
    rows = [unit_record(window, frac, p, s, w_adj) for s in range(seeds)]
    records.extend(rows)
    return {
        "P_span": float(np.mean([r["spanning"]["either"] for r in rows])),
        "def_density": float(np.mean([r["deficiency"] / max(r["n_kept"], 1)
                                      for r in rows])),
        "largest_frac": float(np.mean([r["spanning"]["largest_comp_frac"]
                                       for r in rows])),
    }


def main() -> None:
    graphlike = triangular_graphlike(LATTICE_ROWS, LATTICE_ROWS)
    extent = float(min(np.ptp(graphlike.nodes[:, 0]),
                       np.ptp(graphlike.nodes[:, 1])))
    windows = {f: crop_square(graphlike, L=f * extent,
                              boundary_thickness=BOUNDARY_THICKNESS)
               for f in FRACTIONS}
    print(f"triangular lattice N={graphlike.nodes.shape[0]}, extent={extent:.1f}")
    for f in FRACTIONS:
        print(f"  frac {f}: window N={windows[f].node_count}, "
              f"L={windows[f].L_value:.1f}")

    stats: dict[float, list[dict]] = {}
    records: list[dict] = []
    print(f"\ntriangular R-region vs p ({SEEDS} seeds) — P_span / def-density / "
          f"largest-frac:")
    print("  L\\p   " + " ".join(f"{p:>5.2f}" for p in P_GRID))
    for f in FRACTIONS:
        row = [window_stats(windows[f], f, p, SEEDS, records) for p in P_GRID]
        stats[f] = row
        lval = windows[f].L_value
        print(f"  P L≈{lval:4.0f} " + " ".join(f"{r['P_span']:5.2f}" for r in row))
        print(f"  d L≈{lval:4.0f} "
              + " ".join(f"{r['def_density']:5.3f}" for r in row))

    fig, ax = plt.subplots(1, 2, figsize=(13, 5.2))
    for f in FRACTIONS:
        lval = windows[f].L_value
        ax[0].plot(P_GRID, [r["P_span"] for r in stats[f]], marker="o",
                   label=f"L≈{lval:.0f}")
        ax[1].plot(P_GRID, [r["largest_frac"] for r in stats[f]], marker="o",
                   label=f"L≈{lval:.0f}")
    ax[0].axhline(0.5, color="grey", ls=":", lw=1)
    ax[0].axvline(0.5, color="orange", ls="--", lw=1,
                  label="lattice site-perc. ~0.5")
    ax[0].set(xlabel="site removal probability p",
              ylabel="P(R-region spans)",
              title="Triangular: P_span — 0 at clean (def=0, no R-region),\n"
                    "parity plateau ~0.5, then lattice fragments near p≈0.55",
              ylim=(-0.05, 1.05))
    ax[0].legend(fontsize=8)
    ax[1].set(xlabel="site removal probability p",
              ylabel="largest R-region fraction",
              title="Largest R-region — created by dilution, not present at "
                    "clean\n(opposite of the hat, which starts extensive at p=0)")
    ax[1].legend(fontsize=8)
    fig.suptitle("Periodic control (triangular) — clean limit has NO R-region "
                 "(def=0); contrast the hat's extensive clean-limit R-region")
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=140)
    plt.close(fig)
    print(f"\nwrote {FIG}")

    with JSONL.open("w") as fh:
        for rec in records:
            fh.write(json.dumps(rec) + "\n")
    print(f"wrote {JSONL} ({len(records)} records)")


if __name__ == "__main__":
    main()

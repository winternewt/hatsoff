"""Spectre clean-point reconciliation with Schirmann et al.'s TB convention.

Open question (``docs/SPECTRE_TODO.md`` §Caveats): the natural-graph long-edge
(the length-2 doubled edge V9-V11 once the gold vertex is stripped) — kept
**direct** or **split** at its midpoint? — was never reconciled with Schirmann
et al.'s exact Spectre tight-binding model (arXiv:2307.11054), so the coarse
nullity-0 result is not yet load-bearing.

This script settles it by tabulating, at the clean point (no dilution) across
inflation levels, three constructions and both flux sectors:

  * ``natural-direct``  — strip gold; every polygon edge kept whole (length-2
    edge direct).  Non-bipartite.
  * ``natural-split``   — strip gold, then ``build_tb_graph``'s hat-style
    treatment: split a long edge through its midpoint **only** when a
    neighbouring tile already supplies a vertex there (boundary edges stay
    direct).  This is exactly how the hat type-c edge is handled, hence the
    Schirmann-consistent choice.
  * ``with-gold``       — Singh-Flicker bipartite 14-gon (gold = inserted
    degree-2 midpoint).

For each it reports zero-flux and π-flux nullity (dense complex ``eigh``), and
— the missing companion to Schirmann's hat-only table — the π-flux count vs the
Mystic fraction N_Mystic/N (Mystics play the anti-hat role; ~1 per 26.6 tiles).

The hat count gate (``tests/test_flux.py``: π-flux 1/3/22/147 reproduced with
``build_tb_graph``) already proves our edge convention equals Schirmann's *on
the hat*; this carries it to the Spectre and records the decision.

    uv run python experiments/spectre_reconcile.py
Writes ``experiments/spectre_reconcile.json`` and prints a markdown block for
``docs/SPECTRE_TODO.md``.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import scipy.linalg
import scipy.sparse

from hat_amp.graph import build_vertex_graph
from hat_amp.spectre import (
    generate_spectre_tiling,
    generate_spectre_tiling_labeled,
    strip_gold_vertex,
)
from hatsoff.flux import build_flux_hamiltonian, label_vertex_mask, tile_area
from hatsoff.graph import build_tb_graph

EXP_DIR = Path(__file__).parent
OUT_JSON = EXP_DIR / "spectre_reconcile.json"

LEVELS = [int(x) for x in os.environ.get("HATSOFF_RECONCILE_LEVELS", "1,2,3").split(",")]


def build_direct(
    polygons: list[np.ndarray], tol: float = 1e-5
) -> tuple[np.ndarray, scipy.sparse.csr_matrix]:
    """Vertex graph with every polygon edge kept whole (no long-edge splitting)."""
    graph = build_vertex_graph(polygons, tol=tol)
    verts = graph.nodes
    n = len(verts)
    edges = graph.edges
    if edges.size == 0:
        return verts, scipy.sparse.csr_matrix((n, n), dtype=np.float64)
    rows = np.concatenate([edges[:, 0], edges[:, 1]])
    cols = np.concatenate([edges[:, 1], edges[:, 0]])
    data = np.ones(rows.shape[0], dtype=np.float64)
    adj = scipy.sparse.coo_matrix((data, (rows, cols)), shape=(n, n))
    return verts, (adj.tocsr() > 0).astype(np.float64).tocsr()


def _nullity(verts: np.ndarray, adj: scipy.sparse.spmatrix, area: float,
             flux: float, window: float = 1e-6) -> int:
    """Kernel dimension via the fast RRR value-subset (validated == full eigh)."""
    h = build_flux_hamiltonian(verts, adj, area, flux=flux).toarray()
    evals = scipy.linalg.eigh(h, driver="evr", eigvals_only=True,
                              subset_by_value=(-window, window))
    return int(evals.size)


def nullities(verts: np.ndarray, adj: scipy.sparse.spmatrix, area: float) -> tuple[int, int]:
    """(zero-flux nullity, π-flux nullity) via dense complex eigh (subset)."""
    return _nullity(verts, adj, area, 0.0), _nullity(verts, adj, area, np.pi)


def analyse_level(level: int) -> dict:
    polys14, labels = generate_spectre_tiling_labeled(level)
    polys13 = strip_gold_vertex(polys14)
    n_tiles = len(polys14)
    n_mystic_tiles = sum(1 for lab in labels if lab == "M")
    area = tile_area(polys13[0])

    constructions = {
        "natural-direct": build_direct(polys13),
        "natural-split": build_tb_graph(polys13),
        "with-gold": build_tb_graph(polys14),
    }

    rec: dict = {"level": level, "n_tiles": n_tiles, "n_mystic_tiles": n_mystic_tiles}
    for name, (verts, adj) in constructions.items():
        n0, npi = nullities(verts, adj, area)
        mystic_verts = int(
            label_vertex_mask(verts, polys13, labels, "M").sum()
        )
        rec[name] = {
            "N": int(len(verts)),
            "n_edges": int(adj.nnz // 2),
            "nullity_zero_flux": n0,
            "nullity_pi_flux": npi,
            "n_mystic_vertices": mystic_verts,
            "pi_per_mystic_tile": (npi / n_mystic_tiles) if n_mystic_tiles else None,
        }
        print(
            f"  L{level} {name:14s} N={len(verts):6d} E={adj.nnz//2:6d} "
            f"null(0)={n0:4d} null(π)={npi:4d} "
            f"N_M={n_mystic_tiles} π/N_M={rec[name]['pi_per_mystic_tile']}",
            flush=True,
        )
    return rec


def main() -> None:
    print(f"Spectre reconciliation — levels {LEVELS}", flush=True)
    records = [analyse_level(lvl) for lvl in LEVELS]
    OUT_JSON.write_text(json.dumps(records, indent=2))
    print(f"\nwrote {OUT_JSON}", flush=True)

    # Markdown block for docs/SPECTRE_TODO.md
    print("\n=== markdown for docs/SPECTRE_TODO.md ===\n")
    print("| level | construction | N | nullity(0) | nullity(π) | N_Mystic | π/N_Mystic |")
    print("|---|---|---|---|---|---|---|")
    for r in records:
        for name in ("natural-direct", "natural-split", "with-gold"):
            c = r[name]
            ratio = c["pi_per_mystic_tile"]
            ratio_s = f"{ratio:.2f}" if ratio is not None else "—"
            print(
                f"| {r['level']} | {name} | {c['N']} | {c['nullity_zero_flux']} "
                f"| {c['nullity_pi_flux']} | {r['n_mystic_tiles']} | {ratio_s} |"
            )


if __name__ == "__main__":
    main()

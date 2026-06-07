"""π-flux count-gate: the reconciliation cross-check.

``build_tb_graph`` already reproduces the hat's *zero-flux* nullity 0/1/8/51
(see ``docs/NULLITY.md``).  If the ported complex Peierls Hamiltonian on the
*same* graph reproduces the hat's *π-flux* counts **1/3/22/147** — the anti-hat
counts of Franca/Schirmann et al. (arXiv:2307.11054) — then our edge convention
provably equals theirs, and the same convention carries to the Spectre.

L0-L2 run fast; the L3 headline (147, N≈7047 complex ``eigh``) is gated behind
``HATSOFF_SLOW=1`` because the dense complex diagonalization is minutes long.
"""

from __future__ import annotations

import os

import numpy as np
import pytest

from hat_amp.tiling import generate_tiling
from hatsoff.flux import (
    build_flux_hamiltonian,
    flux_kernel,
    signed_tile_area,
    tile_area,
)
from hatsoff.graph import build_tb_graph

# (level, zero-flux nullity, π-flux nullity).  Zero-flux L1 is 0 not 1 — the
# isolated H-L1 boundary effect documented in CLAUDE.md / docs/NULLITY.md.
HAT_GATE = [(0, 0, 1), (1, 0, 3), (2, 8, 22)]
HAT_GATE_L3 = (3, 51, 147)


def _nullities(level: int) -> tuple[int, int, int, int]:
    """Return (zero-flux nullity, π-flux nullity, minority tiles, N)."""
    polys = generate_tiling(level=level)
    verts, adj = build_tb_graph(polys)
    area = tile_area(polys[0])
    h0 = build_flux_hamiltonian(verts, adj, area, flux=0.0)
    hpi = build_flux_hamiltonian(verts, adj, area, flux=np.pi)
    n0, _, _, _ = flux_kernel(h0)
    npi, _, _, _ = flux_kernel(hpi)
    signs = np.sign([signed_tile_area(p) for p in polys])
    minority = int(min((signs > 0).sum(), (signs < 0).sum()))
    return n0, npi, minority, len(verts)


@pytest.mark.parametrize(("level", "n_zero_flux", "n_pi_flux"), HAT_GATE)
def test_hat_count_gate(level: int, n_zero_flux: int, n_pi_flux: int) -> None:
    """Zero-flux 0/0/8 and π-flux 1/3/22 on the hat (the reconciliation gate)."""
    n0, npi, minority, _ = _nullities(level)
    assert n0 == n_zero_flux
    assert npi == n_pi_flux
    # Franca identity: π-flux zero-mode count == number of reflected (anti-)hats.
    assert npi == minority


@pytest.mark.skipif(
    os.environ.get("HATSOFF_SLOW") != "1",
    reason="L3 complex eigh (N~7047) is minutes; set HATSOFF_SLOW=1 to run",
)
def test_hat_count_gate_l3() -> None:
    """The headline: hat L3 π-flux nullity is 147 (= anti-hat count)."""
    level, n_zero_flux, n_pi_flux = HAT_GATE_L3
    n0, npi, minority, _ = _nullities(level)
    assert n0 == n_zero_flux
    assert npi == n_pi_flux
    assert npi == minority


def test_zero_flux_hamiltonian_is_real_negative_adjacency() -> None:
    """``flux=0`` reproduces the real -adjacency (matching-pipeline matrix)."""
    polys = generate_tiling(level=1)
    verts, adj = build_tb_graph(polys)
    h0 = build_flux_hamiltonian(verts, adj, tile_area(polys[0]), flux=0.0)
    assert np.max(np.abs(h0.imag.toarray())) < 1e-12
    # Off-diagonal magnitude 1 on every bond, zero on-site.
    dense = h0.toarray().real
    assert np.allclose(dense, -adj.toarray())


def test_pi_flux_nullity_is_gauge_invariant() -> None:
    """A rigid coordinate shift changes the Peierls gauge but not the spectrum."""
    polys = generate_tiling(level=1)
    verts, adj = build_tb_graph(polys)
    area = tile_area(polys[0])
    base, _, _, _ = flux_kernel(build_flux_hamiltonian(verts, adj, area, np.pi))
    shifted_verts = verts + np.array([3.7, -2.1])
    shifted, _, _, _ = flux_kernel(
        build_flux_hamiltonian(shifted_verts, adj, area, np.pi)
    )
    assert base == shifted == 3


def test_flux_kernel_support_sums_to_nullity() -> None:
    """diag(P) is a probability-like field summing to the kernel dimension."""
    polys = generate_tiling(level=2)
    verts, adj = build_tb_graph(polys)
    hpi = build_flux_hamiltonian(verts, adj, tile_area(polys[0]), np.pi)
    n_zero, support, _, _ = flux_kernel(hpi)
    assert support.shape == (len(verts),)
    assert np.all(support > -1e-9)
    assert abs(support.sum() - n_zero) < 1e-6

"""Tests for hatsoff.dilution — site and bond removal on a small graph."""

import numpy as np
import scipy.sparse

from hatsoff.dilution import dilute_bonds, dilute_sites


def _grid_adj() -> scipy.sparse.csr_matrix:
    """4-cycle 0-1-2-3-0 with both diagonals; N=4, E=6 (K4)."""
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)]
    rows: list[int] = []
    cols: list[int] = []
    for u, v in edges:
        rows += [u, v]
        cols += [v, u]
    data = np.ones(len(rows), dtype=np.float64)
    return scipy.sparse.csr_matrix((data, (rows, cols)), shape=(4, 4))


class TestSiteDilution:
    def test_p_zero_keeps_everything(self):
        adj = _grid_adj()
        verts = np.arange(8, dtype=float).reshape(4, 2)
        rng = np.random.default_rng(0)
        sv, sa, kept = dilute_sites(verts, adj, 0.0, rng)
        assert kept.tolist() == [0, 1, 2, 3]
        assert sa.nnz == adj.nnz
        assert np.array_equal(sv, verts)

    def test_p_one_removes_everything(self):
        adj = _grid_adj()
        verts = np.zeros((4, 2))
        rng = np.random.default_rng(0)
        sv, sa, kept = dilute_sites(verts, adj, 1.0, rng)
        assert kept.size == 0
        assert sa.shape == (0, 0)

    def test_induced_subgraph_is_symmetric(self):
        adj = _grid_adj()
        verts = np.zeros((4, 2))
        rng = np.random.default_rng(3)
        _, sa, kept = dilute_sites(verts, adj, 0.5, rng)
        dense = sa.toarray()
        assert np.array_equal(dense, dense.T)
        # induced edges are a subset of the original among survivors
        orig = adj.toarray()[np.ix_(kept, kept)]
        assert np.all(dense <= orig + 1e-12)


class TestBondDilution:
    def test_p_zero_keeps_all_bonds(self):
        adj = _grid_adj()
        rng = np.random.default_rng(0)
        out = dilute_bonds(adj, 0.0, rng)
        assert out.nnz == adj.nnz

    def test_p_one_removes_all_bonds(self):
        adj = _grid_adj()
        rng = np.random.default_rng(0)
        out = dilute_bonds(adj, 1.0, rng)
        assert out.nnz == 0
        assert out.shape == adj.shape

    def test_symmetric_and_binary(self):
        adj = _grid_adj()
        rng = np.random.default_rng(7)
        out = dilute_bonds(adj, 0.5, rng).toarray()
        assert np.array_equal(out, out.T)
        assert set(np.unique(out)).issubset({0.0, 1.0})

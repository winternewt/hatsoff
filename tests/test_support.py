"""Tests for hatsoff.support — kernel support field and spatial spanning."""

import numpy as np
import scipy.sparse

from hatsoff.support import kernel_support, support_spanning


def _adj(n: int, edges: list[tuple[int, int]]) -> scipy.sparse.csr_matrix:
    rows: list[int] = []
    cols: list[int] = []
    for u, v in edges:
        rows += [u, v]
        cols += [v, u]
    data = np.ones(len(rows), dtype=np.float64)
    return scipy.sparse.csr_matrix((data, (rows, cols)), shape=(n, n))


class TestKernelSupport:
    def test_isolated_vertices_are_the_kernel(self):
        """3 disjoint edges + 4 isolated sites: nullity 4, support on isolated."""
        # edges among 0..5; isolated 6,7,8,9
        adj = _adj(10, [(0, 1), (2, 3), (4, 5)])
        n0, support = kernel_support(adj, expected=4)
        assert n0 == 4
        assert np.isclose(support.sum(), 4.0)
        # each isolated vertex carries a full unit of zero-mode weight
        assert np.allclose(support[6:], 1.0)
        # matched (edge) vertices carry none
        assert np.allclose(support[:6], 0.0, atol=1e-8)

    def test_star_support_avoids_center(self):
        """K_{1,4}: kernel dim 3; weight on leaves, none on the hub."""
        adj = _adj(5, [(0, 1), (0, 2), (0, 3), (0, 4)])
        n0, support = kernel_support(adj, expected=3)
        assert n0 == 3
        assert np.isclose(support.sum(), 3.0)
        assert support[0] < 1e-8
        assert np.all(support[1:] > 0.0)

    def test_eigsh_fallback_grows_k(self):
        """Force the eigsh path (max_dense=0); under-estimate must still
        recover the full count by growing k."""
        adj = _adj(8, [(0, 1), (2, 3)])  # 4 isolated -> nullity 4
        n0, support = kernel_support(adj, expected=0, buffer=1, max_dense=0)
        assert n0 == 4
        assert np.isclose(support.sum(), 4.0)


class TestSupportSpanning:
    def _grid(self, nx: int, ny: int) -> np.ndarray:
        xs, ys = np.meshgrid(np.arange(nx), np.arange(ny))
        return np.column_stack([xs.ravel().astype(float), ys.ravel().astype(float)])

    def test_full_grid_spans_both(self):
        """A fully-active unit grid (d0=1.5) crosses in both directions."""
        pos = self._grid(5, 5)
        support = np.ones(pos.shape[0])
        top = np.flatnonzero(pos[:, 1] >= 4)
        bottom = np.flatnonzero(pos[:, 1] <= 0)
        left = np.flatnonzero(pos[:, 0] <= 0)
        right = np.flatnonzero(pos[:, 0] >= 4)
        r = support_spanning(pos, support, top, bottom, left, right, d0=1.5)
        assert r["top_bottom"] and r["left_right"] and r["either"]
        assert r["n_active"] == 25

    def test_single_column_spans_only_vertical(self):
        """One active vertical column spans top-bottom, not left-right."""
        pos = self._grid(5, 5)
        support = np.zeros(pos.shape[0])
        support[pos[:, 0] == 2] = 1.0  # middle column active
        top = np.flatnonzero(pos[:, 1] >= 4)
        bottom = np.flatnonzero(pos[:, 1] <= 0)
        left = np.flatnonzero(pos[:, 0] <= 0)
        right = np.flatnonzero(pos[:, 0] >= 4)
        r = support_spanning(pos, support, top, bottom, left, right, d0=1.5)
        assert r["top_bottom"] is True
        assert r["left_right"] is False
        assert r["either"] is True

    def test_too_sparse_does_not_span(self):
        """Active sites farther apart than d0 form no spanning cluster."""
        pos = self._grid(5, 5)
        support = np.zeros(pos.shape[0])
        # two corners only
        support[(pos[:, 0] == 0) & (pos[:, 1] == 0)] = 1.0
        support[(pos[:, 0] == 4) & (pos[:, 1] == 4)] = 1.0
        top = np.flatnonzero(pos[:, 1] >= 4)
        bottom = np.flatnonzero(pos[:, 1] <= 0)
        left = np.flatnonzero(pos[:, 0] <= 0)
        right = np.flatnonzero(pos[:, 0] >= 4)
        r = support_spanning(pos, support, top, bottom, left, right, d0=1.5)
        assert r["either"] is False
        assert r["n_active"] == 2

    def test_no_active_sites(self):
        pos = self._grid(3, 3)
        support = np.zeros(pos.shape[0])
        empty = np.array([], dtype=int)
        r = support_spanning(pos, support, empty, empty, empty, empty, d0=1.5)
        assert r["n_active"] == 0
        assert r["either"] is False

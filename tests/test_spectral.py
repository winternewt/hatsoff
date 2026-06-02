"""Tests for hatsoff.spectral — bipartiteness, zero modes, Lieb bound."""

import numpy as np
import scipy.sparse

from hatsoff.spectral import check_bipartite, count_zero_modes, lieb_bound


class TestCheckBipartite:
    """BFS 2-coloring on known graphs."""

    def test_path_graph_p4_is_bipartite(self):
        """P4: 0-1-2-3 is bipartite (even/odd coloring)."""
        # Adjacency: 0-1, 1-2, 2-3
        row = [0, 1, 1, 2, 2, 3]
        col = [1, 0, 2, 1, 3, 2]
        data = [1, 1, 1, 1, 1, 1]
        A = scipy.sparse.csr_matrix((data, (row, col)), shape=(4, 4))

        is_bip, coloring = check_bipartite(A)
        assert is_bip is True
        assert coloring is not None
        assert len(coloring) == 4
        # Adjacent nodes must have different colors
        for u, v in [(0, 1), (1, 2), (2, 3)]:
            assert coloring[u] != coloring[v]

    def test_triangle_k3_is_not_bipartite(self):
        """K3 (triangle) is not bipartite."""
        row = [0, 0, 1, 1, 2, 2]
        col = [1, 2, 0, 2, 0, 1]
        data = [1, 1, 1, 1, 1, 1]
        A = scipy.sparse.csr_matrix((data, (row, col)), shape=(3, 3))

        is_bip, coloring = check_bipartite(A)
        assert is_bip is False
        assert coloring is None

    def test_disconnected_bipartite(self):
        """Two disconnected edges: both components are bipartite."""
        row = [0, 1, 2, 3]
        col = [1, 0, 3, 2]
        data = [1, 1, 1, 1]
        A = scipy.sparse.csr_matrix((data, (row, col)), shape=(4, 4))

        is_bip, coloring = check_bipartite(A)
        assert is_bip is True
        assert coloring is not None


class TestCountZeroModes:
    """Zero-mode counting via eigsh shift-invert."""

    def test_star_graph_k13(self):
        """Star graph K_{1,3}: center (0) connected to 1, 2, 3.

        Eigenvalues are {-sqrt(3), 0, 0, sqrt(3)}, so 2 zero modes.
        """
        row = [0, 1, 0, 2, 0, 3]
        col = [1, 0, 2, 0, 3, 0]
        data = [1.0] * 6
        A = scipy.sparse.csr_matrix((data, (row, col)), shape=(4, 4))

        count, eigenvalues, eigenvectors = count_zero_modes(A, k=2, tol=1e-8)
        assert count == 2
        assert eigenvectors.shape == (4, 2)
        # The two eigenvalues closest to zero should both be ~0
        assert np.all(np.abs(eigenvalues) < 1e-8)

    def test_complete_graph_k4_no_zero_modes(self):
        """K4 has eigenvalues {-1, -1, -1, 3} — no zero modes."""
        A = scipy.sparse.csr_matrix(
            np.ones((4, 4)) - np.eye(4)
        )
        count, eigenvalues, eigenvectors = count_zero_modes(A, k=2, tol=1e-8)
        assert count == 0


class TestLiebBound:
    """Lieb bound |N_A - N_B| on bipartite graphs."""

    def test_balanced_bipartite(self):
        """P4 has 2 nodes in each partition → bound = 0."""
        row = [0, 1, 1, 2, 2, 3]
        col = [1, 0, 2, 1, 3, 2]
        data = [1, 1, 1, 1, 1, 1]
        A = scipy.sparse.csr_matrix((data, (row, col)), shape=(4, 4))

        _, coloring = check_bipartite(A)
        bound = lieb_bound(A, coloring)
        assert bound == 0

    def test_star_graph_unbalanced(self):
        """K_{1,3}: partition sizes 1 and 3 → bound = 2."""
        row = [0, 1, 0, 2, 0, 3]
        col = [1, 0, 2, 0, 3, 0]
        data = [1, 1, 1, 1, 1, 1]
        A = scipy.sparse.csr_matrix((data, (row, col)), shape=(4, 4))

        is_bip, coloring = check_bipartite(A)
        assert is_bip is True
        bound = lieb_bound(A, coloring)
        assert bound == 2

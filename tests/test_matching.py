"""Tests for hatsoff.matching — matching number, deficiency, Gallai-Edmonds.

Ground truth is derived from small graphs whose matching structure and
adjacency spectra are known by hand.
"""

import networkx as nx
import numpy as np
import scipy.sparse

from hatsoff.matching import (
    adjacency_to_graph,
    deficiency,
    gallai_edmonds,
    matching_number,
    nullspace_support,
)


def _adj(n: int, edges: list[tuple[int, int]]) -> scipy.sparse.csr_matrix:
    rows: list[int] = []
    cols: list[int] = []
    for u, v in edges:
        rows += [u, v]
        cols += [v, u]
    data = np.ones(len(rows), dtype=np.float64)
    return scipy.sparse.csr_matrix((data, (rows, cols)), shape=(n, n))


class TestMatchingNumber:
    def test_path_p4(self):
        """P4 has a perfect matching: nu=2, deficiency 0."""
        g = adjacency_to_graph(_adj(4, [(0, 1), (1, 2), (2, 3)]))
        assert matching_number(g) == 2
        assert deficiency(g) == 0

    def test_triangle_k3(self):
        """K3: nu=1, one vertex always unmatched -> deficiency 1."""
        g = adjacency_to_graph(_adj(3, [(0, 1), (1, 2), (0, 2)]))
        assert matching_number(g) == 1
        assert deficiency(g) == 1

    def test_star_k13(self):
        """Star K_{1,3}: nu=1, deficiency 2 (= adjacency nullity, bipartite)."""
        g = adjacency_to_graph(_adj(4, [(0, 1), (0, 2), (0, 3)]))
        assert matching_number(g) == 1
        assert deficiency(g) == 2


class TestGallaiEdmonds:
    def test_triangle_is_factor_critical(self):
        """K3 is one factor-critical component: D=all, A=C=empty, def=1."""
        ge = gallai_edmonds(adjacency_to_graph(_adj(3, [(0, 1), (1, 2), (0, 2)])))
        assert sorted(ge.D.tolist()) == [0, 1, 2]
        assert ge.A.size == 0
        assert ge.C.size == 0
        assert ge.n_critical_components == 1
        assert ge.deficiency == 1

    def test_perfect_matching_all_in_C(self):
        """A graph with a perfect matching has D empty, all vertices in C."""
        ge = gallai_edmonds(adjacency_to_graph(_adj(4, [(0, 1), (1, 2), (2, 3)])))
        assert ge.D.size == 0
        assert sorted(ge.C.tolist()) == [0, 1, 2, 3]
        assert ge.deficiency == 0

    def test_star_partition(self):
        """K_{1,3}: leaves are inessential (D), center is A, def = 3-1 = 2."""
        ge = gallai_edmonds(adjacency_to_graph(_adj(4, [(0, 1), (0, 2), (0, 3)])))
        assert sorted(ge.D.tolist()) == [1, 2, 3]
        assert ge.A.tolist() == [0]
        assert ge.n_critical_components == 3
        assert ge.deficiency == 2


class TestFastVsSlow:
    """The single-matching fast GE must match the per-vertex reference."""

    def _agree(self, edges: list[tuple[int, int]], n: int) -> None:
        g = adjacency_to_graph(_adj(n, edges))
        fast = gallai_edmonds(g, method="fast")
        slow = gallai_edmonds(g, method="slow")
        assert set(fast.D.tolist()) == set(slow.D.tolist())
        assert set(fast.A.tolist()) == set(slow.A.tolist())
        assert set(fast.C.tolist()) == set(slow.C.tolist())
        assert fast.deficiency == slow.deficiency
        assert fast.deficiency == deficiency(g)

    def test_triangle(self):
        self._agree([(0, 1), (1, 2), (0, 2)], 3)

    def test_c5_blossom(self):
        self._agree([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)], 5)

    def test_bridged_triangles(self):
        self._agree([(0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (4, 5), (3, 5)], 6)

    def test_random_nonbipartite(self):
        rng = np.random.default_rng(7)
        for _ in range(40):
            n = int(rng.integers(3, 16))
            g = nx.gnp_random_graph(n, float(rng.uniform(0.15, 0.55)),
                                    seed=int(rng.integers(0, 1_000_000)))
            fast = gallai_edmonds(g, method="fast")
            slow = gallai_edmonds(g, method="slow")
            assert set(fast.D.tolist()) == set(slow.D.tolist())
            assert fast.deficiency == g.number_of_nodes() - 2 * matching_number(g)


class TestNullspaceSupport:
    def test_triangle_no_kernel(self):
        """K3 adjacency is full rank: nullity 0, support all zero."""
        nz, supp = nullspace_support(_adj(3, [(0, 1), (1, 2), (0, 2)]))
        assert nz == 0
        assert np.allclose(supp, 0.0)

    def test_star_support_sums_to_nullity(self):
        """K_{1,3}: kernel dim 2; support sums to 2 and avoids the center."""
        adj = _adj(4, [(0, 1), (0, 2), (0, 3)])
        nz, supp = nullspace_support(adj)
        assert nz == 2
        assert np.isclose(supp.sum(), 2.0)
        # center (node 0) carries no zero-mode weight; leaves do
        assert supp[0] < 1e-9
        assert np.all(supp[1:] > 0.0)

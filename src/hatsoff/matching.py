"""Generalized matching structure of the (non-bipartite) hat graph.

Bhola et al. (PRX 12, 021058, 2022) organize topologically protected zero
modes of *bipartite* dilute lattices via the Dulmage--Mendelsohn
decomposition.  The hat graph is non-bipartite, so the right tool is the
Gallai--Edmonds structure theorem for general graphs.

Key facts this module encodes:

* Maximum-matching number ν(G) and deficiency def(G) = N − 2ν(G).
* Gallai--Edmonds partition (D, A, C):
    - D(G) = inessential vertices (missed by *some* maximum matching);
      every component of G[D] is factor-critical.
    - A(G) = vertices outside D adjacent to D.
    - C(G) = the rest; G[C] has a perfect matching.
    - def(G) = c(D) − |A|, where c(D) = number of components of G[D].

For a *bipartite* graph the adjacency nullity equals def(G) generically
(structural zero modes = unmatched vertices).  For a *non-bipartite* graph
the odd factor-critical components (e.g. a triangle) make adjacency nullity
and def(G) diverge — quantifying that gap under dilution is the project.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

import networkx as nx
import numpy as np
import scipy.sparse


def adjacency_to_graph(adjacency: scipy.sparse.spmatrix) -> nx.Graph:
    """Build an unweighted ``networkx`` graph from a symmetric adjacency.

    All N vertices are added as nodes (including isolated ones) so node
    indices line up with matrix rows.
    """
    n = adjacency.shape[0]
    coo = scipy.sparse.triu(adjacency, k=1).tocoo()
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from(zip(coo.row.tolist(), coo.col.tolist()))
    return graph


def matching_number(graph: nx.Graph) -> int:
    """Maximum-cardinality matching number ν(G) (blossom algorithm)."""
    return len(nx.max_weight_matching(graph, maxcardinality=True))


def deficiency(graph: nx.Graph) -> int:
    """Matching deficiency N − 2ν(G): vertices unmatched by a max matching."""
    return graph.number_of_nodes() - 2 * matching_number(graph)


@dataclass(frozen=True)
class GallaiEdmonds:
    """Gallai--Edmonds partition of a graph's vertex set."""

    D: np.ndarray
    A: np.ndarray
    C: np.ndarray
    n_critical_components: int
    deficiency: int


def _from_d_set(graph: nx.Graph, d_set: set[int]) -> GallaiEdmonds:
    """Assemble the (D, A, C) partition from the inessential set D.

    A(G) = neighbours of D outside D; C(G) = the rest. def(G) = c(D) − |A|.
    """
    nodes = set(graph.nodes())
    a_set: set[int] = set()
    for v in d_set:
        for w in graph.neighbors(v):
            if w not in d_set:
                a_set.add(w)
    c_set = nodes - d_set - a_set
    d_subgraph = graph.subgraph(d_set)
    n_components = nx.number_connected_components(d_subgraph) if d_set else 0
    return GallaiEdmonds(
        D=np.array(sorted(d_set), dtype=np.int64),
        A=np.array(sorted(a_set), dtype=np.int64),
        C=np.array(sorted(c_set), dtype=np.int64),
        n_critical_components=n_components,
        deficiency=n_components - len(a_set),
    )


def _inessential_set_fast(graph: nx.Graph) -> set[int]:
    """The Gallai--Edmonds set D from a single maximum matching (O(V·E)).

    Grows alternating forests rooted at all M-exposed vertices simultaneously,
    contracting blossoms (Edmonds). Since M is maximum no augmenting path is
    found, and the *even/outer* vertices of the final forest are exactly the
    inessential vertices D(G).
    """
    index = {node: i for i, node in enumerate(graph.nodes())}
    rindex = list(graph.nodes())
    n = len(rindex)
    nbrs: list[list[int]] = [[] for _ in range(n)]
    for u, v in graph.edges():
        iu, iv = index[u], index[v]
        nbrs[iu].append(iv)
        nbrs[iv].append(iu)

    match = [-1] * n
    for u, v in nx.max_weight_matching(graph, maxcardinality=True):
        match[index[u]] = index[v]
        match[index[v]] = index[u]

    base = list(range(n))
    parent = [-1] * n
    used = [False] * n  # even / outer label
    queue: deque[int] = deque()
    for v in range(n):
        if match[v] == -1:
            used[v] = True
            queue.append(v)

    def lca(a: int, b: int) -> int:
        seen = [False] * n
        x = a
        while True:
            x = base[x]
            seen[x] = True
            if match[x] == -1:
                break
            x = parent[match[x]]
        y = b
        while True:
            y = base[y]
            if seen[y]:
                return y
            y = parent[match[y]]

    def mark(v: int, b: int, child: int, blossom: list[bool]) -> None:
        while base[v] != b:
            blossom[base[v]] = True
            blossom[base[match[v]]] = True
            parent[v] = child
            child = match[v]
            v = parent[match[v]]

    while queue:
        v = queue.popleft()
        for to in nbrs[v]:
            if base[v] == base[to] or match[v] == to:
                continue
            if used[to]:
                curbase = lca(v, to)
                blossom = [False] * n
                mark(v, curbase, to, blossom)
                mark(to, curbase, v, blossom)
                for i in range(n):
                    if blossom[base[i]]:
                        base[i] = curbase
                        if not used[i]:
                            used[i] = True
                            queue.append(i)
            elif parent[to] == -1:
                parent[to] = v
                if match[to] == -1:
                    msg = "matching was not maximum (augmenting path found)"
                    raise RuntimeError(msg)
                used[match[to]] = True
                queue.append(match[to])

    return {rindex[i] for i in range(n) if used[i]}


def gallai_edmonds(graph: nx.Graph, method: str = "fast") -> GallaiEdmonds:
    """Compute the Gallai--Edmonds (D, A, C) partition.

    ``method="fast"`` (default) extracts the inessential set D from a single
    maximum matching via one blossom-aware forest pass — O(V·E), scales to
    L3+. ``method="slow"`` uses the inessential-vertex test (v ∈ D iff
    ν(G−v)=ν(G)) — O(N) matchings, a simple reference for validation.

    Returns:
        GallaiEdmonds with vertex-index arrays D, A, C, the number of
        factor-critical components of G[D], and def(G) = c(D) − |A|.
    """
    if method == "fast":
        d_set = _inessential_set_fast(graph)
    elif method == "slow":
        nu = matching_number(graph)
        d_set = {
            v for v in graph.nodes()
            if matching_number(nx.restricted_view(graph, [v], [])) == nu
        }
    else:
        msg = f"unknown method {method!r}"
        raise ValueError(msg)
    return _from_d_set(graph, d_set)


def nullspace_support(
    adjacency: scipy.sparse.spmatrix,
    tol: float = 1e-8,
) -> tuple[int, np.ndarray]:
    """Per-site weight of the adjacency null space (gauge-invariant).

    Returns the kernel dimension and ``diag(P)`` where ``P = V Vᵀ`` is the
    orthogonal projector onto the kernel (V an orthonormal kernel basis).
    ``diag(P)_i`` is how much site *i* participates in the zero-mode subspace
    and is independent of the arbitrary basis choice within the degenerate
    subspace — the right field to test for *support percolation*.

    Args:
        adjacency: (N, N) symmetric binary adjacency.
        tol: Eigenvalues with ``|e| < tol`` count as zero.

    Returns:
        n_zero: Kernel dimension.
        support: (N,) array, ``diag(P)`` in [0, 1], summing to ``n_zero``.
    """
    a = adjacency.toarray().astype(np.float64)
    evals, evecs = np.linalg.eigh(a)
    mask = np.abs(evals) < tol
    basis = evecs[:, mask]
    support = np.einsum("ij,ij->i", basis, basis)
    return int(mask.sum()), support

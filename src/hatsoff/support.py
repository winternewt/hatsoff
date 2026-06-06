"""Zero-mode support field and spatial spanning (percolation) probe.

The adjacency kernel projector ``P = V Vᵀ`` (V an orthonormal kernel basis)
has a gauge-invariant diagonal ``diag(P)_i`` = how much site *i* participates
in the zero-mode subspace.  ``kernel_support`` computes it with a single
shift-invert ``eigsh`` (cheaper than a dense ``eigh``/``eigvalsh`` on the large
L3 graph, and it returns the count and the vectors together).

``support_spanning`` asks the percolation question: do the support-active
sites span a window?  Zero modes live on even-distance (Sutherland) sites, so
two active sites are linked by spatial proximity (KDTree within ``d0``), not by
direct graph adjacency — then a union-find with virtual edge electrodes tests
top-bottom / left-right crossing, reusing the ``hat_amp.percolation`` pattern.

``rregion_spanning`` is the rigorous, parameter-free counterpart: it tests
whether a single Gallai--Edmonds factor-critical component (the matching-theory
R-region) spans the window, using only graph connectivity — no ``d0``, no
``theta``, no eigendecomposition.
"""

from __future__ import annotations

import networkx as nx
import numpy as np
import scipy.linalg
import scipy.sparse
import scipy.sparse.linalg
import scipy.spatial

from hat_amp.percolation import WeightedQuickUnionUF


def _cpu_dense_eigh(dense: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Symmetric eigdecomposition, robust to LAPACK non-convergence.

    ``numpy.linalg.eigh`` (LAPACK ``syevd``) occasionally raises
    "Eigenvalues did not converge" on a particular matrix; the RRR driver
    (``scipy.linalg.eigh(driver="evr")``) reliably succeeds where it does.
    """
    try:
        return np.linalg.eigh(dense)
    except np.linalg.LinAlgError:
        return scipy.linalg.eigh(dense, driver="evr")


# Pluggable dense symmetric-eigh backend (set to a GPU implementation on a
# cluster via set_dense_eigh; defaults to the robust CPU path).
_DENSE_EIGH = _cpu_dense_eigh


def set_dense_eigh(fn) -> None:
    """Override the dense symmetric eigh backend used by ``kernel_support``.

    A cluster driver may inject a GPU implementation (e.g. ``torch.linalg.eigh``
    on CUDA) returning ``(eigenvalues, eigenvectors)`` as NumPy arrays.
    """
    global _DENSE_EIGH
    _DENSE_EIGH = fn


def _dense_eigh(dense: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Dispatch to the active dense-eigh backend."""
    return _DENSE_EIGH(dense)


def kernel_support(
    adjacency: scipy.sparse.spmatrix,
    tol: float = 1e-8,
    expected: int | None = None,
    buffer: int = 24,
    max_dense: int = 9000,
) -> tuple[int, np.ndarray]:
    """Kernel dimension and per-site support ``diag(P)``.

    For ``N <= max_dense`` (covers up to L3, N≈7047) a **dense** ``eigh`` is
    used: it is exact and robust against the high-multiplicity null space that
    site dilution produces (hundreds of exact zeros — where shift-invert
    ``eigsh`` silently under-counts because ARPACK cannot resolve a deeply
    degenerate eigenvalue).  For larger ``N`` it falls back to shift-invert
    ``eigsh`` sized from ``expected`` (the matching deficiency, since
    nullity ≈ deficiency), growing ``k`` until the count is confirmed
    unsaturated — acceptable only while the degeneracy stays modest.

    Args:
        adjacency: (N, N) symmetric binary adjacency.
        tol: Eigenvalues with ``|e| < tol`` count as zero.
        expected: Cheap nullity estimate; sets the initial eigsh ``k`` in the
            large-N fallback.  Ignored in the dense path.
        buffer: Extra eigenpairs beyond ``expected`` (fallback only).
        max_dense: Use dense ``eigh`` at or below this size.

    Returns:
        n_zero: Kernel dimension.
        support: (N,) ``diag(P)`` in [0, 1], summing to ``n_zero``.
    """
    n = adjacency.shape[0]
    if n <= max_dense:
        evals, evecs = _dense_eigh(adjacency.toarray().astype(np.float64))
        mask = np.abs(evals) < tol
        basis = evecs[:, mask]
        return int(mask.sum()), np.einsum("ij,ij->i", basis, basis)

    a = adjacency.tocsc().astype(np.float64)
    hard_cap = n - 2
    k = max(1, min(hard_cap, (expected if expected is not None else 8) + buffer))
    while True:
        vals, vecs = scipy.sparse.linalg.eigsh(a, k=k, sigma=1e-8, which="LM")
        mask = np.abs(vals) < tol
        n_zero = int(mask.sum())
        if n_zero < k or k >= hard_cap:
            break
        k = min(hard_cap, 2 * k)

    basis = vecs[:, mask]
    support = np.einsum("ij,ij->i", basis, basis)
    return n_zero, support


def support_spanning(
    positions: np.ndarray,
    support: np.ndarray,
    top: np.ndarray,
    bottom: np.ndarray,
    left: np.ndarray,
    right: np.ndarray,
    d0: float,
    theta: float = 0.01,
) -> dict:
    """Does the support-active site set span the window at proximity ``d0``?

    Active sites (``support > theta``) are linked when within Euclidean
    distance ``d0`` (proximity percolation, bridging the even-distance
    Sutherland sublattice that direct graph adjacency misses).  Spanning is
    tested by whether any boundary-band active site shares a proximity cluster
    with one on the opposite band (root-set intersection — no virtual-node
    merging that would corrupt cluster sizes).

    NB this measures spanning of the *union* of all kernel modes, so it tracks
    spatial coverage of the support, not single-mode extent — a proxy.
    ``largest_cluster_frac`` (biggest proximity cluster / window size) is the
    finer order parameter; record several ``d0`` to expose the sensitivity.

    Args:
        positions: (M, 2) window vertex positions.
        support: (M,) ``diag(P)`` over the same vertices.
        top, bottom, left, right: index arrays into ``positions`` for each
            boundary band.
        d0: Proximity linking distance.
        theta: Support-active threshold.

    Returns:
        dict: ``top_bottom``, ``left_right``, ``either`` (bools),
        ``n_active`` (int), ``largest_cluster_frac`` (float, / M).
    """
    m = positions.shape[0]
    active_idx = np.flatnonzero(support > theta)
    n_active = int(active_idx.size)
    result = {
        "top_bottom": False, "left_right": False, "either": False,
        "n_active": n_active, "largest_cluster_frac": 0.0,
    }
    if n_active == 0:
        return result

    uf = WeightedQuickUnionUF(n_active)  # index space = active sites only
    local = {int(g): i for i, g in enumerate(active_idx)}
    tree = scipy.spatial.KDTree(positions[active_idx])
    for i, j in tree.query_pairs(r=d0):
        uf.union(i, j)

    roots = np.array([uf.find(i) for i in range(n_active)])
    _, counts = np.unique(roots, return_counts=True)
    result["largest_cluster_frac"] = float(counts.max()) / float(m)

    def band_roots(band: np.ndarray) -> set[int]:
        return {uf.find(local[int(x)]) for x in band if int(x) in local}

    tb = bool(band_roots(top) & band_roots(bottom))
    lr = bool(band_roots(left) & band_roots(right))
    result["top_bottom"] = tb
    result["left_right"] = lr
    result["either"] = tb or lr
    return result


def rregion_spanning(
    graph: nx.Graph,
    d_nodes: np.ndarray,
    top: np.ndarray,
    bottom: np.ndarray,
    left: np.ndarray,
    right: np.ndarray,
) -> dict:
    """Does the matching-theoretic R-region span the window? (parameter-free)

    The **rigorous, parameter-free** counterpart of ``support_spanning``.  The
    Gallai--Edmonds inessential set ``D`` (``d_nodes``) is the R-region: the
    sites forced to carry a monomer in some maximum matching, where the
    topologically-protected zero-mode weight lives.

    Connectivity is the **projected (shared-neighbour) graph** on ``D``: two
    R-region sites are linked when they are adjacent *or* share a common
    neighbour.  This is the genuine even-sublattice structure of the zero-mode
    support — on the (near-bipartite, non-bipartite) hat ``D`` is essentially an
    independent set, so direct ``G[D]`` adjacency would see only isolated
    monomers; sites couple through the odd (A) sites between them.  The
    ``support_spanning`` proxy approximates exactly this coupling with a tunable
    Euclidean distance ``d0``; here it is fixed by the graph, with **no ``d0``,
    no support threshold ``theta``, and no kernel eigendecomposition / gauge
    choice**.  A region **spans** when one projected-connected component meets
    both opposite boundary bands.

    Args:
        graph: The (diluted) adjacency graph; node labels index the
            boundary-band arrays the caller supplies.
        d_nodes: Gallai--Edmonds inessential set ``D`` (node labels), e.g.
            ``gallai_edmonds(graph, "fast").D``.
        top, bottom, left, right: node-label arrays for each boundary band.

    Returns:
        dict: ``top_bottom``, ``left_right``, ``either`` (bools), ``n_dnodes``
        (|D|), ``n_components`` (projected-connected R-region count),
        ``largest_comp_frac`` (largest R-region size / N).
    """
    m = graph.number_of_nodes()
    result = {
        "top_bottom": False, "left_right": False, "either": False,
        "n_dnodes": int(d_nodes.size), "n_components": 0,
        "largest_comp_frac": 0.0,
    }
    if d_nodes.size == 0 or m == 0:
        return result

    d_set = {int(x) for x in d_nodes}
    local = {int(v): i for i, v in enumerate(d_nodes.tolist())}
    uf = WeightedQuickUnionUF(len(local))

    # Project onto D: each vertex w links all of its D-neighbours together
    # (shared-neighbour coupling); direct D-D edges link their endpoints.
    for w in graph.nodes():
        dn = [local[x] for x in graph.neighbors(w) if x in d_set]
        for k in range(1, len(dn)):
            uf.union(dn[0], dn[k])
    for u, v in graph.edges():
        if u in d_set and v in d_set:
            uf.union(local[u], local[v])

    roots = np.array([uf.find(i) for i in range(len(local))])
    _, counts = np.unique(roots, return_counts=True)
    result["n_components"] = int(counts.size)
    result["largest_comp_frac"] = float(counts.max()) / float(m)

    def band_roots(band: np.ndarray) -> set[int]:
        return {uf.find(local[int(x)]) for x in band if int(x) in local}

    tb = bool(band_roots(top) & band_roots(bottom))
    lr = bool(band_roots(left) & band_roots(right))
    result["top_bottom"] = tb
    result["left_right"] = lr
    result["either"] = tb or lr
    return result

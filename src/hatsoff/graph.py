"""Franca-style tight-binding graph construction from hat polygons."""

from __future__ import annotations

import numpy as np
import scipy.sparse
import scipy.spatial

from hat_amp.graph import build_vertex_graph


_TYPE_C_THRESHOLD_RATIO = 1.8


def build_tb_graph(
    polygons: list[np.ndarray],
    tol: float = 1e-5,
) -> tuple[np.ndarray, scipy.sparse.csr_matrix]:
    """Build the tight-binding vertex graph from hat polygons.

    Starts from the polygon boundary graph and splits type-c edges
    (the single edge per hat spanning two lattice spacings) through
    their midpoint vertex when that vertex already exists in the
    vertex set from a neighbouring hat.  Boundary type-c edges whose
    midpoint has no matching vertex are kept unsplit.

    Args:
        polygons: List of (13, 2) arrays from ``generate_tiling``.
        tol: Distance tolerance for merging coincident vertices.

    Returns:
        vertices: (M, 2) unique vertex positions.
        adjacency: (M, M) sparse CSR binary adjacency matrix.
    """
    graph = build_vertex_graph(polygons, tol=tol)
    verts = graph.nodes
    if len(verts) == 0:
        return verts, scipy.sparse.csr_matrix((0, 0), dtype=np.float64)

    tree = scipy.spatial.KDTree(verts)
    boundary_edges = graph.edges

    edge_vecs = verts[boundary_edges[:, 1]] - verts[boundary_edges[:, 0]]
    edge_lengths = np.linalg.norm(edge_vecs, axis=1)
    type_c_cutoff = edge_lengths.min() * _TYPE_C_THRESHOLD_RATIO

    edges: set[tuple[int, int]] = set()
    for idx in range(len(boundary_edges)):
        u, v = int(boundary_edges[idx, 0]), int(boundary_edges[idx, 1])
        if edge_lengths[idx] < type_c_cutoff:
            edges.add((min(u, v), max(u, v)))
        else:
            midpoint = (verts[u] + verts[v]) / 2.0
            dist, mid_idx = tree.query(midpoint)
            mid = int(mid_idx)
            if dist < tol * 100 and mid != u and mid != v:
                edges.add((min(u, mid), max(u, mid)))
                edges.add((min(v, mid), max(v, mid)))
            else:
                edges.add((min(u, v), max(u, v)))

    n = len(verts)
    rows: list[int] = []
    cols: list[int] = []
    for u, v in edges:
        rows.extend([u, v])
        cols.extend([v, u])

    if rows:
        data = np.ones(len(rows), dtype=np.float64)
        adj = scipy.sparse.coo_matrix(
            (data, (rows, cols)), shape=(n, n),
        )
        adj = (adj.tocsr() > 0).astype(np.float64).tocsr()
    else:
        adj = scipy.sparse.csr_matrix((n, n), dtype=np.float64)

    return verts, adj

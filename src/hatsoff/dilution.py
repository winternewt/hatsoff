"""Site and bond dilution of the hat tight-binding graph.

Dilution is the perturbation the zero modes are genuinely fragile to (see
``docs/DISORDER.md``): removing sites or bonds makes the adjacency null space
grow.  These helpers produce the diluted adjacency (and surviving vertex
positions) that the matching / null-space analysis consumes.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse


def dilute_sites(
    vertices: np.ndarray,
    adjacency: scipy.sparse.spmatrix,
    p: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, scipy.sparse.csr_matrix, np.ndarray]:
    """Remove each site independently with probability ``p``.

    Returns the induced subgraph on the surviving sites.  Edges to removed
    sites are dropped; isolated survivors are kept (they are zero modes).

    Args:
        vertices: (N, 2) vertex positions.
        adjacency: (N, N) symmetric binary adjacency.
        p: Per-site removal probability.
        rng: Seeded NumPy generator.

    Returns:
        sub_vertices: (M, 2) surviving positions.
        sub_adjacency: (M, M) induced CSR adjacency.
        kept: (M,) original indices of the survivors.
    """
    n = adjacency.shape[0]
    keep_mask = rng.random(n) >= p
    kept = np.flatnonzero(keep_mask)
    csr = scipy.sparse.csr_matrix(adjacency)
    sub = csr[kept][:, kept]
    sub = ((sub + sub.T) > 0).astype(np.float64).tocsr()
    return vertices[kept], sub, kept


def dilute_bonds(
    adjacency: scipy.sparse.spmatrix,
    p: float,
    rng: np.random.Generator,
) -> scipy.sparse.csr_matrix:
    """Remove each undirected bond independently with probability ``p``.

    Vertex set is unchanged; only edges are deleted.

    Args:
        adjacency: (N, N) symmetric binary adjacency.
        p: Per-bond removal probability.
        rng: Seeded NumPy generator.

    Returns:
        (N, N) diluted CSR adjacency (symmetric, binary).
    """
    n = adjacency.shape[0]
    upper = scipy.sparse.triu(adjacency, k=1).tocoo()
    keep = rng.random(upper.row.shape[0]) >= p
    rows = upper.row[keep]
    cols = upper.col[keep]
    data = np.ones(rows.shape[0], dtype=np.float64)
    sym = scipy.sparse.coo_matrix(
        (np.concatenate([data, data]),
         (np.concatenate([rows, cols]), np.concatenate([cols, rows]))),
        shape=(n, n),
    )
    return sym.tocsr()

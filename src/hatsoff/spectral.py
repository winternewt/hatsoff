"""Spectral analysis for hat tiling adjacency matrices.

Bipartiteness checking, zero-mode counting via ARPACK, and Lieb bound.
"""

from __future__ import annotations

from collections import deque

import numpy as np
import scipy.sparse
import scipy.sparse.linalg


def check_bipartite(
    A: scipy.sparse.spmatrix,
) -> tuple[bool, np.ndarray | None]:
    """BFS 2-coloring on a sparse adjacency matrix.

    Parameters
    ----------
    A : scipy sparse matrix
        Symmetric adjacency matrix (N x N).

    Returns
    -------
    is_bipartite : bool
    coloring : np.ndarray or None
        Array of 0/1 labels if bipartite, else None.
    """
    n = A.shape[0]
    coloring = np.full(n, -1, dtype=np.intp)

    # Convert to CSR for efficient row slicing
    A_csr = scipy.sparse.csr_matrix(A)

    for start in range(n):
        if coloring[start] != -1:
            continue
        # BFS from this unvisited node
        coloring[start] = 0
        queue: deque[int] = deque([start])
        while queue:
            node = queue.popleft()
            color = coloring[node]
            # Iterate over neighbors
            row_start = A_csr.indptr[node]
            row_end = A_csr.indptr[node + 1]
            for neighbor in A_csr.indices[row_start:row_end]:
                if coloring[neighbor] == -1:
                    coloring[neighbor] = 1 - color
                    queue.append(neighbor)
                elif coloring[neighbor] == color:
                    return False, None

    return True, coloring


def count_zero_modes(
    A: scipy.sparse.spmatrix,
    k: int = 200,
    tol: float = 1e-10,
) -> tuple[int, np.ndarray, np.ndarray]:
    """Count eigenvalues near zero energy using ARPACK shift-invert.

    Uses ``sigma=1e-8`` instead of ``sigma=0.0`` to avoid singular
    factorization when A has true zero eigenvalues.

    Parameters
    ----------
    A : scipy sparse matrix
        Symmetric adjacency / Hamiltonian matrix.
    k : int
        Number of eigenvalues to request from ARPACK (default 200).
        Must be less than the matrix dimension.
    tol : float
        Threshold for considering an eigenvalue to be zero.

    Returns
    -------
    count : int
        Number of eigenvalues with ``|e| < tol``.
    eigenvalues : np.ndarray
        The *k* eigenvalues closest to zero.
    eigenvectors : np.ndarray
        Corresponding eigenvectors as columns (N x k).
    """
    A_csc = scipy.sparse.csc_matrix(A, dtype=float)
    n = A_csc.shape[0]

    # Clamp k to valid range for ARPACK: 1 <= k <= n - 2
    k = min(k, n - 2) if n > 2 else 1

    eigenvalues, eigenvectors = scipy.sparse.linalg.eigsh(
        A_csc,
        k=k,
        sigma=1e-8,
        which="LM",
    )

    count = int(np.sum(np.abs(eigenvalues) < tol))
    return count, eigenvalues, eigenvectors


def lieb_bound(
    A: scipy.sparse.spmatrix,
    coloring: np.ndarray,
) -> int:
    """Lieb lower bound on zero modes for a bipartite graph.

    Parameters
    ----------
    A : scipy sparse matrix
        Adjacency matrix (unused in the calculation itself, accepted
        for API consistency).
    coloring : np.ndarray
        Array of 0/1 sublattice labels (length N).

    Returns
    -------
    bound : int
        ``|N_A - N_B|`` — the minimum number of zero modes guaranteed
        by Lieb's theorem.
    """
    n_a = int(np.sum(coloring == 0))
    n_b = int(np.sum(coloring == 1))
    return abs(n_a - n_b)

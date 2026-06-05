"""Hopping disorder and zero-mode fragility on the hat tight-binding graph.

The equal-hopping adjacency has a macroscopic E=0 degeneracy that the
literature calls *fragile* — it depends on all hoppings being equal.  This
module perturbs each bond by a random factor and measures how the formerly
degenerate modes split, so we can ask which zero modes are structurally
robust and which are accidents of equal hopping.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse


def disordered_adjacency(
    adjacency: scipy.sparse.spmatrix,
    delta: float,
    rng: np.random.Generator,
    distribution: str = "uniform",
    onsite: float = 0.0,
) -> np.ndarray:
    """Return a dense symmetric matrix with disordered hoppings (and on-site).

    The bond support (which pairs are connected) is left unchanged; only the
    hopping *values* are perturbed by ``1 + delta*eta``.  ``eta`` is drawn per
    undirected edge and applied symmetrically so the result stays Hermitian.
    A nonzero ``onsite`` adds an independent random diagonal potential of
    strength ``onsite`` — this breaks the zero-diagonal structure that
    protects the structural zero modes, unlike pure hopping disorder.

    Args:
        adjacency: Symmetric binary adjacency (N x N), sparse.
        delta: Hopping disorder strength.  ``delta=0`` keeps clean hoppings.
        rng: NumPy random generator (caller seeds for reproducibility).
        distribution: ``"uniform"`` for eta in [-1, 1], ``"gaussian"`` for
            unit-variance normal eta.
        onsite: On-site (diagonal) disorder strength.  ``0.0`` keeps the
            chiral zero diagonal.

    Returns:
        Dense (N, N) symmetric float matrix of perturbed hoppings.
    """
    coo = scipy.sparse.triu(adjacency, k=1).tocoo()
    rows, cols = coo.row, coo.col
    n_edges = rows.shape[0]
    n = adjacency.shape[0]

    if distribution == "uniform":
        eta = rng.uniform(-1.0, 1.0, size=n_edges)
        diag = rng.uniform(-1.0, 1.0, size=n)
    elif distribution == "gaussian":
        eta = rng.standard_normal(size=n_edges)
        diag = rng.standard_normal(size=n)
    else:
        msg = f"unknown distribution {distribution!r}"
        raise ValueError(msg)

    weights = 1.0 + delta * eta
    h = np.zeros((n, n), dtype=np.float64)
    h[rows, cols] = weights
    h[cols, rows] = weights
    if onsite != 0.0:
        h[np.arange(n), np.arange(n)] = onsite * diag
    return h


def zero_mode_splitting(
    adjacency: scipy.sparse.spmatrix,
    n_zero: int,
    delta: float,
    rng: np.random.Generator,
    n_realizations: int = 1,
    distribution: str = "uniform",
) -> np.ndarray:
    """Eigenvalues nearest E=0 of the disordered Hamiltonian.

    Diagonalizes the dense perturbed matrix for each realization and returns
    the ``n_zero`` eigenvalues closest to zero — the images of the clean
    zero-mode subspace.  Stacked over realizations.

    Args:
        adjacency: Clean symmetric binary adjacency (N x N).
        n_zero: Size of the clean E=0 degenerate subspace.
        delta: Disorder strength.
        rng: NumPy random generator.
        n_realizations: Number of disorder realizations.
        distribution: Passed to :func:`disordered_adjacency`.

    Returns:
        (n_realizations, n_zero) array of near-zero eigenvalues, sorted by
        absolute value within each realization.
    """
    out = np.empty((n_realizations, n_zero), dtype=np.float64)
    for r in range(n_realizations):
        h = disordered_adjacency(adjacency, delta, rng, distribution)
        evals = np.linalg.eigvalsh(h)
        order = np.argsort(np.abs(evals))
        out[r] = np.sort(evals[order[:n_zero]])
    return out


def clean_zero_modes(
    adjacency: scipy.sparse.spmatrix,
    tol: float = 1e-8,
) -> tuple[int, np.ndarray]:
    """Dimension and an orthonormal basis of the clean E=0 kernel.

    Args:
        adjacency: Symmetric binary adjacency (N x N).
        tol: Eigenvalues with ``|e| < tol`` count as zero.

    Returns:
        n_zero: Kernel dimension.
        basis: (N, n_zero) orthonormal columns spanning the kernel.
    """
    a = adjacency.toarray().astype(np.float64)
    evals, evecs = np.linalg.eigh(a)
    mask = np.abs(evals) < tol
    return int(np.sum(mask)), evecs[:, mask]

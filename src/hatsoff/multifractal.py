"""Multifractal analysis of eigenstates.

Participation ratios, inverse participation ratios, and D2 scaling
exponent for distinguishing extended, localized, and multifractal states.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import linregress


def participation_ratio(psi: np.ndarray) -> float:
    """Participation ratio of a (normalized) wavefunction.

    .. math::
        P = \\frac{(\\sum |\\psi_i|^2)^2}{\\sum |\\psi_i|^4}

    For an extended state P ~ N; for a localized state P ~ O(1).

    Parameters
    ----------
    psi : np.ndarray
        Wavefunction amplitudes (1-D, real or complex).

    Returns
    -------
    float
        Participation ratio.
    """
    prob = np.abs(psi) ** 2
    return float(np.sum(prob) ** 2 / np.sum(prob**2))


def inverse_participation_ratio(psi: np.ndarray) -> float:
    """Inverse participation ratio: IPR = 1 / P.

    Parameters
    ----------
    psi : np.ndarray
        Wavefunction amplitudes.

    Returns
    -------
    float
    """
    return 1.0 / participation_ratio(psi)


def multifractal_exponent(
    sizes: list[int],
    participation_ratios: list[float],
) -> tuple[float, float]:
    """Fit the D2 multifractal exponent from finite-size scaling.

    Performs linear regression of ``log(P)`` vs ``log(N)``.
    ``D2 = 1`` indicates fully extended states; ``0 < D2 < 1``
    indicates multifractal scaling.

    Parameters
    ----------
    sizes : list[int]
        System sizes N.
    participation_ratios : list[float]
        Corresponding mean participation ratios.

    Returns
    -------
    D2 : float
        Slope of the log-log fit (multifractal exponent).
    r_squared : float
        Coefficient of determination of the fit.
    """
    log_n = np.log(np.asarray(sizes, dtype=float))
    log_p = np.log(np.asarray(participation_ratios, dtype=float))

    result = linregress(log_n, log_p)
    d2 = float(result.slope)
    r_squared = float(result.rvalue**2)
    return d2, r_squared


def analyze_modes(
    eigenvalues: np.ndarray,
    eigenvectors: np.ndarray,
    tol: float = 1e-10,
) -> dict:
    """Convenience analysis of zero modes from an eigsh result.

    Parameters
    ----------
    eigenvalues : np.ndarray
        Eigenvalue array (length k).
    eigenvectors : np.ndarray
        Eigenvector matrix (N x k), columns are eigenvectors.
    tol : float
        Threshold for zero eigenvalues.

    Returns
    -------
    dict
        ``count``  — number of zero modes,
        ``participation_ratios`` — list of PR for each zero mode,
        ``mean_pr`` — mean participation ratio,
        ``iprs`` — list of IPR for each zero mode.
    """
    zero_mask = np.abs(eigenvalues) < tol
    count = int(np.sum(zero_mask))

    if count == 0:
        return {
            "count": 0,
            "participation_ratios": [],
            "mean_pr": 0.0,
            "iprs": [],
        }

    zero_vecs = eigenvectors[:, zero_mask]
    prs = [participation_ratio(zero_vecs[:, i]) for i in range(count)]
    iprs = [inverse_participation_ratio(zero_vecs[:, i]) for i in range(count)]

    return {
        "count": count,
        "participation_ratios": prs,
        "mean_pr": float(np.mean(prs)),
        "iprs": iprs,
    }

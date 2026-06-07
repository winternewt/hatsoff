"""π-flux (magnetic) tight-binding Hamiltonian for monotile vertex graphs.

The zero-flux pipeline (``graph.py`` + ``matching``/``support``) builds a real
±1 adjacency and uses combinatorial matching theory.  At **π flux per tile
plaquette** the hoppings become complex (Peierls phase), matching theory no
longer applies (the matrix is complex Hermitian, not a 0/1 adjacency), and the
zero-mode count tracks the *minority* tiles — anti-hats on the hat (1/3/22/147),
Mystics on the Spectre.  This module builds that complex Hermitian Hamiltonian
and counts its kernel by **dense** ``eigh``.

The Peierls phase is the gauge of Schirmann et al. (PRL 132, 086402 (2024);
arXiv:2307.11054), matching the kwant reference ``hat/hat.py:Cst_Hopping``::

    H_ij = -exp(-0.5j * B * (x_i - x_j) * (y_i + y_j)),   B = flux / A_tile

The line integral of the vector potential ``A = (0, B x)`` around any closed
loop equals ``B`` times the enclosed signed area; since every tile face is
congruent with area ``A_tile``, choosing ``B = π / A_tile`` threads exactly π
through every plaquette (uniform π flux).  Splitting a long edge through a
collinear midpoint vertex (as ``build_tb_graph`` does for the hat type-c edge)
does not change any enclosed area, so the per-face flux is unaffected.

Reproducing the hat π-flux counts **1/3/22/147** with ``build_tb_graph``'s graph
is the parameter-free cross-check that our edge convention equals Schirmann's
(the zero-flux 0/1/8/51 is already reproduced); the same convention then carries
to the Spectre.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse
import scipy.spatial

from hatsoff.support import _dense_eigh

PI_FLUX: float = np.pi


def tile_area(polygon: np.ndarray) -> float:
    """Unsigned shoelace area of one tile polygon (the plaquette area).

    All monotile faces are congruent, so a single tile fixes the flux scale
    ``B = flux / A_tile``.

    Args:
        polygon: (V, 2) ordered vertex coordinates of one tile.

    Returns:
        The unsigned polygon area.
    """
    x = polygon[:, 0]
    y = polygon[:, 1]
    return 0.5 * float(abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))))


def signed_tile_area(polygon: np.ndarray) -> float:
    """Signed shoelace area — its sign is the tile orientation (chirality).

    Used to count minority/reflected tiles (anti-hats): the majority handedness
    gives one sign, the reflected minority the other.
    """
    x = polygon[:, 0]
    y = polygon[:, 1]
    return 0.5 * float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def build_flux_hamiltonian(
    vertices: np.ndarray,
    adjacency: scipy.sparse.spmatrix,
    plaquette_area: float,
    flux: float = PI_FLUX,
) -> scipy.sparse.csr_matrix:
    """Complex Hermitian TB Hamiltonian with ``flux`` threaded per tile face.

    Hopping amplitude magnitude is 1; the Peierls phase is the Landau-like
    gauge ``-exp(-0.5j * B * (x_i - x_j)(y_i + y_j))`` with ``B = flux/area``.
    ``flux=0`` returns the real ±1 adjacency (sign ``-1`` per bond), so the
    zero-flux spectrum is recovered up to an overall sign.

    Args:
        vertices: (N, 2) vertex positions.
        adjacency: (N, N) symmetric binary adjacency (the bond structure).
        plaquette_area: Area of one tile (``tile_area``); sets ``B = flux/area``.
        flux: Flux per plaquette in radians (default π).

    Returns:
        (N, N) complex128 Hermitian CSR Hamiltonian.
    """
    n = adjacency.shape[0]
    upper = scipy.sparse.triu(scipy.sparse.csr_matrix(adjacency), k=1).tocoo()
    i, j = upper.row, upper.col
    b = flux / plaquette_area
    xi, yi = vertices[i, 0], vertices[i, 1]
    xj, yj = vertices[j, 0], vertices[j, 1]
    phase = -np.exp(-0.5j * b * (xi - xj) * (yi + yj))
    h_upper = scipy.sparse.coo_matrix((phase, (i, j)), shape=(n, n))
    h = (h_upper + h_upper.conj().transpose()).tocsr()
    return h


def flux_kernel(
    hamiltonian: scipy.sparse.spmatrix,
    tol: float = 1e-8,
) -> tuple[int, np.ndarray, np.ndarray, np.ndarray]:
    """Kernel dimension, per-site support ``diag(P)`` and near-zero modes.

    Uses **dense** complex-Hermitian ``eigh`` (LAPACK ``zheevd``/``zheevr`` via
    the pluggable ``support._dense_eigh`` backend — a GPU backend set through
    ``support.set_dense_eigh`` must accept complex input).  Sparse shift-invert
    ``eigsh`` is unusable here: it silently under-counts a deeply degenerate
    null space (see ``docs``/CLAUDE.md) and is fragile on complex matrices.

    Args:
        hamiltonian: (N, N) Hermitian matrix (real or complex).
        tol: Eigenvalues with ``|E| < tol`` count as zero.

    Returns:
        n_zero: Kernel dimension.
        support: (N,) ``diag(P)`` in [0, 1] summing to ``n_zero``.
        evals: All eigenvalues, ascending.
        kernel_vecs: (N, n_zero) orthonormal kernel basis (columns), for IPR.
    """
    dense = np.asarray(hamiltonian.toarray())
    if not np.iscomplexobj(dense):
        dense = dense.astype(np.float64)
    evals, evecs = _dense_eigh(dense)
    mask = np.abs(evals) < tol
    n_zero = int(mask.sum())
    basis = evecs[:, mask]
    support = np.einsum("ij,ij->i", basis.conj(), basis).real
    return n_zero, support, evals, basis


def label_vertex_mask(
    vertices: np.ndarray,
    polygons: list[np.ndarray],
    labels: list[str],
    target_label: str,
    tol: float = 1e-3,
) -> np.ndarray:
    """Boolean mask of graph vertices touched by a tile carrying ``target_label``.

    Maps each labelled polygon's corners onto the merged vertex set (nearest
    neighbour within ``tol``).  On the Spectre, ``label_vertex_mask(..., "M")``
    marks the Mystic sites where Singh--Flicker matching freedom concentrates.

    Args:
        vertices: (N, 2) merged graph vertex positions (from ``build_tb_graph``).
        polygons: Tile polygons (same coordinates the graph was built from).
        labels: Per-polygon labels, parallel to ``polygons``.
        target_label: Label whose vertices to mark (e.g. ``"M"``).
        tol: Match radius for corner→merged-vertex assignment.

    Returns:
        (N,) boolean mask.
    """
    tree = scipy.spatial.KDTree(vertices)
    mask = np.zeros(vertices.shape[0], dtype=bool)
    for poly, lab in zip(polygons, labels):
        if lab != target_label:
            continue
        dist, idx = tree.query(poly)
        hit = np.asarray(idx)[np.asarray(dist) < tol]
        mask[hit] = True
    return mask

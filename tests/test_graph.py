"""Tests for Franca-style tight-binding graph construction."""

from __future__ import annotations

import numpy as np

from hat_amp.tiling import generate_tiling
from hatsoff.graph import build_tb_graph


def test_build_tb_graph_empty_input() -> None:
    """Empty polygon input should produce an empty sparse graph."""
    vertices, adjacency = build_tb_graph([])

    assert vertices.shape == (0, 2)
    assert adjacency.shape == (0, 0)


def test_build_tb_graph_level_2_degree_distribution() -> None:
    """The level-2 H metatile TB graph matches Franca et al. (2024)."""
    polygons = generate_tiling(level=2)
    vertices, adjacency = build_tb_graph(polygons)

    degrees = np.asarray(adjacency.sum(axis=1)).ravel().astype(np.int64)
    unique_degrees, counts = np.unique(degrees, return_counts=True)

    assert vertices.shape == (1084, 2)
    assert adjacency.shape == (1084, 1084)
    assert adjacency.nnz // 2 == 1252
    assert dict(zip(unique_degrees.tolist(), counts.tolist(), strict=True)) == {
        2: 792,
        3: 248,
        4: 44,
    }

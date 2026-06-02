"""Tests for hatsoff.multifractal — participation ratios and D2 scaling."""

import numpy as np
import pytest

from hatsoff.multifractal import (
    participation_ratio,
    inverse_participation_ratio,
    multifractal_exponent,
    analyze_modes,
)


class TestParticipationRatio:
    """PR on analytically tractable vectors."""

    def test_uniform_vector(self):
        """Uniform |psi> = 1/sqrt(N) on every site → P = N."""
        N = 100
        psi = np.ones(N) / np.sqrt(N)
        pr = participation_ratio(psi)
        assert pr == pytest.approx(N, rel=1e-10)

    def test_delta_function(self):
        """Localized on one site → P = 1."""
        N = 200
        psi = np.zeros(N)
        psi[42] = 1.0
        pr = participation_ratio(psi)
        assert pr == pytest.approx(1.0, rel=1e-10)

    def test_two_site_equal(self):
        """Equal weight on two sites → P = 2."""
        psi = np.zeros(50)
        psi[0] = 1.0 / np.sqrt(2)
        psi[1] = 1.0 / np.sqrt(2)
        pr = participation_ratio(psi)
        assert pr == pytest.approx(2.0, rel=1e-10)


class TestInverseParticipationRatio:
    def test_ipr_uniform(self):
        N = 100
        psi = np.ones(N) / np.sqrt(N)
        ipr = inverse_participation_ratio(psi)
        assert ipr == pytest.approx(1.0 / N, rel=1e-10)

    def test_ipr_delta(self):
        psi = np.zeros(50)
        psi[7] = 1.0
        ipr = inverse_participation_ratio(psi)
        assert ipr == pytest.approx(1.0, rel=1e-10)


class TestMultifractalExponent:
    """D2 fitting with synthetic scaling data."""

    def test_extended_states_d2_one(self):
        """PR proportional to N → D2 = 1."""
        sizes = [100, 400, 1600]
        prs = [float(n) for n in sizes]  # P = N
        d2, r2 = multifractal_exponent(sizes, prs)
        assert d2 == pytest.approx(1.0, abs=0.01)
        assert r2 > 0.999

    def test_multifractal_d2_half(self):
        """PR proportional to N^0.5 → D2 ≈ 0.5."""
        sizes = [100, 400, 1600]
        prs = [float(n**0.5) for n in sizes]
        d2, r2 = multifractal_exponent(sizes, prs)
        assert d2 == pytest.approx(0.5, abs=0.01)
        assert r2 > 0.999

    def test_localized_d2_zero(self):
        """PR = const (localized) → D2 ≈ 0."""
        sizes = [100, 400, 1600]
        prs = [3.0, 3.0, 3.0]
        d2, r2 = multifractal_exponent(sizes, prs)
        assert d2 == pytest.approx(0.0, abs=0.01)


class TestAnalyzeModes:
    """Integration test for analyze_modes."""

    def test_with_zero_modes(self):
        """Fabricate eigenvalues/vectors with one zero mode."""
        eigenvalues = np.array([0.0, 1.5, -2.0])
        # 5 sites, 3 eigenvectors as columns
        eigenvectors = np.zeros((5, 3))
        # Zero mode: uniform
        eigenvectors[:, 0] = 1.0 / np.sqrt(5)
        # Non-zero modes: arbitrary
        eigenvectors[:, 1] = [1, 0, 0, 0, 0]
        eigenvectors[:, 2] = [0, 1, 0, 0, 0]

        result = analyze_modes(eigenvalues, eigenvectors, tol=1e-8)
        assert result["count"] == 1
        assert len(result["participation_ratios"]) == 1
        assert result["participation_ratios"][0] == pytest.approx(5.0, rel=1e-8)
        assert result["mean_pr"] == pytest.approx(5.0, rel=1e-8)
        assert len(result["iprs"]) == 1

    def test_no_zero_modes(self):
        eigenvalues = np.array([1.0, -1.0])
        eigenvectors = np.eye(3, 2)
        result = analyze_modes(eigenvalues, eigenvectors, tol=1e-10)
        assert result["count"] == 0
        assert result["participation_ratios"] == []
        assert result["mean_pr"] == 0.0

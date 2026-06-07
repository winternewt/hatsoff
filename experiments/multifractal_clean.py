"""Multifractal tier B: clean band-center IPR / D2 scaling, hat vs Spectre.

A cheap first look at whether the monotile vertex-graph eigenstates are critical
(multifractal) — the standard probe, on the **zero-flux** real adjacency spectrum.
For each substrate and size we take the full dense ``eigh`` (all eigenvectors,
clean = no dilution), compute the per-state participation ratio
``PR = (Σ|ψ|²)² / Σ|ψ|⁴`` (extended ~ N, localized ~ O(1)), and:

  * the **IPR(E) spectrum** (mean 1/PR in energy bins) — where states localize;
  * the **band-center D2**: mean PR of states in a small |E| window vs N, fitted
    as ``PR ~ N^{D2}`` (D2=1 extended, 0<D2<1 multifractal, 0 localized).

We exclude the exact zero modes (|E|<tol) from the per-state PR — within that
degenerate subspace single eigenvectors are gauge-arbitrary (only diag(P) is
meaningful, handled separately in the π-flux support analysis); the band-center
window uses the small-but-nonzero states, which are non-degenerate.

Sizes: hat levels 1–3 (N≈180/1084/7047), Spectre levels 1–3 (N≈73/491/3563).
Cost is the full real ``eigh`` (hat L3 N=7047 ≈ a few minutes); the rest is free.

    uv run python experiments/multifractal_clean.py
Writes `docs/figures/multifractal_clean.png` and prints D2(band center).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from hat_amp.spectre import generate_spectre_tiling, strip_gold_vertex  # noqa: E402
from hat_amp.tiling import generate_tiling  # noqa: E402
from hatsoff.graph import build_tb_graph  # noqa: E402
from hatsoff.multifractal import participation_ratio  # noqa: E402
from hatsoff.support import _dense_eigh  # noqa: E402

EXP_DIR = Path(__file__).parent
FIG = EXP_DIR.parent / "docs" / "figures" / "multifractal_clean.png"

ZERO_TOL = 1e-8
BAND_HALF = 0.25  # |E| < BAND_HALF (and > ZERO_TOL) = "band centre" window


def hat_graph(level: int):
    return build_tb_graph(generate_tiling(level=level))


def spectre_graph(level: int):
    return build_tb_graph(strip_gold_vertex(generate_spectre_tiling(level)))


def analyse(adjacency) -> dict:
    """Full clean spectrum → IPR(E) and band-centre mean PR."""
    dense = adjacency.toarray().astype(np.float64)
    evals, evecs = _dense_eigh(dense)
    n = dense.shape[0]
    iprs = np.array([1.0 / participation_ratio(evecs[:, i]) for i in range(n)])
    band = (np.abs(evals) > ZERO_TOL) & (np.abs(evals) < BAND_HALF)
    prs_band = [participation_ratio(evecs[:, i]) for i in np.flatnonzero(band)]
    return {
        "N": n, "evals": evals, "iprs": iprs,
        "n_zero": int((np.abs(evals) < ZERO_TOL).sum()),
        "pr_band": float(np.mean(prs_band)) if prs_band else float("nan"),
        "n_band": len(prs_band),
    }


def ipr_spectrum(evals: np.ndarray, iprs: np.ndarray, bins: int = 40):
    edges = np.linspace(evals.min(), evals.max(), bins + 1)
    centres = 0.5 * (edges[:-1] + edges[1:])
    idx = np.clip(np.digitize(evals, edges) - 1, 0, bins - 1)
    mean = np.array([iprs[idx == b].mean() if np.any(idx == b) else np.nan
                     for b in range(bins)])
    return centres, mean


def fit_d2(Ns: list[int], prs: list[float]) -> tuple[float, float]:
    x, y = np.log(np.array(Ns, float)), np.log(np.array(prs, float))
    slope, intercept = np.polyfit(x, y, 1)
    resid = y - (slope * x + intercept)
    r2 = 1.0 - np.sum(resid**2) / np.sum((y - y.mean()) ** 2)
    return float(slope), float(r2)


def main() -> None:
    substrates = {
        "hat": (hat_graph, [1, 2, 3], "C0"),
        "Spectre": (spectre_graph, [1, 2, 3], "C3"),
    }
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 4.8))
    print("clean zero-flux band-centre PR (|E|<%.2f), D2 = slope of PR~N^D2:"
          % BAND_HALF)

    for name, (builder, levels, color) in substrates.items():
        Ns, prs, largest = [], [], None
        for lvl in levels:
            verts, adj = builder(lvl)
            res = analyse(adj)
            Ns.append(res["N"])
            prs.append(res["pr_band"])
            largest = res
            print(f"  {name} L{lvl}: N={res['N']:5d} n_zero={res['n_zero']:3d} "
                  f"PR_band={res['pr_band']:8.1f} (n_band={res['n_band']})")
        d2, r2 = fit_d2(Ns, prs)
        print(f"    → {name}: D2(band centre) = {d2:.3f}  (R²={r2:.3f})")
        ax1.loglog(Ns, prs, "o-", color=color, label=f"{name}: D2={d2:.2f}")
        c, m = ipr_spectrum(largest["evals"], largest["iprs"])
        ax0.plot(c, m, "-", color=color, label=f"{name} (N={largest['N']})")

    ax0.axvline(0.0, color="k", ls=":", lw=0.8)
    ax0.set(xlabel="energy E", ylabel="mean IPR = ⟨1/PR⟩",
            title="(a) IPR spectrum (clean, largest size)")
    ax0.legend(fontsize=8)
    ax0.grid(alpha=0.3)
    ax1.set(xlabel="N", ylabel="band-centre mean PR",
            title="(b) band-centre PR ~ N^{D2}  (1=extended, <1=multifractal)")
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.3, which="both")
    fig.suptitle("Clean zero-flux eigenstates: band-centre multifractal scaling")
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=140)
    print(f"\nwrote {FIG}")


if __name__ == "__main__":
    main()

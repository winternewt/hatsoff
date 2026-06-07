"""Multifractal tier A: D2-like scaling of the π-flux zero-mode SUPPORT.

No new compute — reuses `spectre_flux_campaign.jsonl`. The campaign recorded, per
unit, the gauge-invariant support participation ratio
``support_pr = (Σ_i s_i)² / Σ_i s_i²`` of the kernel projector diagonal
``s_i = diag(P)_i`` (summing to the nullity). This is a legitimate participation
measure of the *whole π-flux zero-mode sector* (gauge-safe, unlike a single
degenerate eigenvector). Its finite-size scaling ``support_pr ~ N^τ`` gives a
D2-like exponent: τ→1 = the zero-mode support is extended/critical (occupies a
finite fraction of sites); τ→0 = localized on O(1) sites.

We fit τ(p) across the window-size family (6 windows + full), at the clean point
and under dilution. (Spectre only — the flux campaign was Spectre; the hat π-flux
sector would need its own run.)

    uv run python experiments/spectre_flux_multifractal.py
Writes `docs/figures/spectre_flux_multifractal.png` and prints τ(p).
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

EXP_DIR = Path(__file__).parent
JSONL = EXP_DIR / "spectre_flux_campaign.jsonl"
FIG = EXP_DIR.parent / "docs" / "figures" / "spectre_flux_multifractal.png"


def load() -> list[dict]:
    return [
        r for r in (json.loads(line) for line in JSONL.open() if line.strip())
        if "error" not in r
    ]


def by_p(recs: list[dict]) -> dict:
    """{p: {N: mean support_pr}} averaged over seeds (N = window node count)."""
    acc: dict = defaultdict(lambda: defaultdict(list))
    for r in recs:
        acc[r["p"]][r["N"]].append(r["support_pr"])
    return {p: {n: float(np.mean(v)) for n, v in nm.items()}
            for p, nm in acc.items()}


def fit_tau(nmap: dict) -> tuple[float, float]:
    """log–log slope of support_pr vs N (D2-like exponent) and its R²."""
    ns = np.array(sorted(nmap))
    ys = np.array([nmap[n] for n in ns])
    good = ys > 0
    if good.sum() < 2:
        return float("nan"), float("nan")
    x, y = np.log(ns[good]), np.log(ys[good])
    slope, intercept = np.polyfit(x, y, 1)
    resid = y - (slope * x + intercept)
    ss = 1.0 - np.sum(resid**2) / np.sum((y - y.mean()) ** 2)
    return float(slope), float(ss)


def main() -> None:
    recs = load()
    print(f"{len(recs)} records")
    pmap = by_p(recs)
    ps = sorted(pmap)

    print("\nπ-flux zero-mode SUPPORT scaling  support_pr ~ N^τ:")
    print("   p   |  τ (D2-like) |  R²  | support_pr(N range)")
    taus, r2s = [], []
    for p in ps:
        tau, r2 = fit_tau(pmap[p])
        taus.append(tau)
        r2s.append(r2)
        ns = sorted(pmap[p])
        rng = f"{pmap[p][ns[0]]:.0f}→{pmap[p][ns[-1]]:.0f} (N {ns[0]}→{ns[-1]})"
        print(f"  {p:.2f} |   {tau:.3f}     | {r2:.3f}| {rng}")

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 4.6))
    # left: log-log support_pr vs N at a few p
    for p in [0.0, 0.05, 0.10, 0.20, 0.30, 0.40]:
        if p not in pmap:
            continue
        ns = np.array(sorted(pmap[p]))
        ys = np.array([pmap[p][n] for n in ns])
        ax0.loglog(ns, ys, "o-", ms=4, label=f"p={p:.2f}")
    ax0.set(xlabel="window N", ylabel="support_pr",
            title="(a) π-flux zero-mode support_pr vs N (log–log)")
    ax0.legend(fontsize=7)
    ax0.grid(alpha=0.3, which="both")
    # right: tau(p)
    ax1.plot(ps, taus, "o-", color="C3")
    ax1.axhline(1.0, color="k", ls=":", lw=0.8, label="τ=1 (extended)")
    ax1.set(xlabel="vacancy density p", ylabel="τ  (support_pr ~ N^τ)",
            ylim=(0, 1.1),
            title="(b) D2-like exponent of the zero-mode support vs p")
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3)
    fig.suptitle("Spectre π-flux zero-mode support: finite-size scaling "
                 "(gauge-invariant diag(P) participation)")
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=140)
    print(f"\nwrote {FIG}")


if __name__ == "__main__":
    main()

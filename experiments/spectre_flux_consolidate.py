"""Consolidate the π-flux Spectre dilution result (no new compute).

Two questions on the finished `spectre_flux_campaign.jsonl`:

  1. **Clean-point finite-size scaling.**  Does the Mystic-support fraction of the
     clean π-flux kernel extrapolate to 1 (all protected modes on Mystics), and
     does the nullity density extrapolate to the Mystic-compound-per-vertex value
     (N_Mystic/2 / N)?  Cropped windows leak at the boundary; the full graph is
     the clean number.  Fit vs 1/L.
  2. **Is the p≈0.3 enrichment→1 a transition or a smooth crossover?**  For each
     window size, locate the vacancy density where the Mystic enrichment
     (support_frac / Mystic-vertex-fraction) drops through 1.1.  If that p* is
     size-independent and the curves do not steepen with L, it is a crossover,
     not a sharp de-percolation — and a genuine spanning claim would need a
     π-flux support-spanning probe (not recorded here).

Writes `docs/figures/spectre_flux_consolidate.png` and prints findings.

    uv run python experiments/spectre_flux_consolidate.py
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
FIG = EXP_DIR.parent / "docs" / "figures" / "spectre_flux_consolidate.png"


def load() -> list[dict]:
    return [
        r for r in (json.loads(line) for line in JSONL.open() if line.strip())
        if "error" not in r
    ]


def enrichment(r: dict) -> float:
    nk = r["n_kept"] or 1
    frac = r["n_mystic"] / nk
    return r["mystic_support_frac"] / frac if frac else 0.0


def clean_scaling(recs: list[dict]) -> list[dict]:
    """One row per window at p=0 (deterministic), sorted by N."""
    rows = [
        {"window": r["window"], "L": r["L"], "N": r["n_kept"],
         "nullity_density": r["nullity"] / r["n_kept"],
         "mystic_frac": r["mystic_support_frac"], "enrichment": enrichment(r)}
        for r in recs if r["p"] == 0.0
    ]
    return sorted(rows, key=lambda d: d["N"])


def crossover(recs: list[dict], level: float = 1.1) -> dict:
    """Per window: mean enrichment(p), and the p* where it crosses `level`."""
    by_win: dict = defaultdict(lambda: defaultdict(list))
    for r in recs:
        by_win[r["window"]][r["p"]].append(enrichment(r))
    out: dict = {}
    for win, pmap in by_win.items():
        ps = sorted(pmap)
        ys = [float(np.mean(pmap[p])) for p in ps]
        pstar = None
        for i in range(1, len(ps)):
            if ys[i - 1] >= level > ys[i]:
                # linear interpolation between the bracketing points
                t = (ys[i - 1] - level) / (ys[i - 1] - ys[i])
                pstar = ps[i - 1] + t * (ps[i] - ps[i - 1])
                break
        out[win] = {"ps": ps, "enrichment": ys, "p_star": pstar}
    return out


def extrapolate(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Linear fit y = a + b·x; return (intercept a = x→0 limit, slope b)."""
    b, a = np.polyfit(x, y, 1)
    return float(a), float(b)


def main() -> None:
    recs = load()
    print(f"{len(recs)} records\n")

    rows = clean_scaling(recs)
    win_rows = [r for r in rows if r["window"] != "full"]
    full = next((r for r in rows if r["window"] == "full"), None)
    invL = np.array([1.0 / r["L"] for r in win_rows])

    print("=== clean point (p=0): finite-size scaling ===")
    print("window |   N   |  L   | nullity/N | mystic_frac | enrichment")
    for r in rows:
        print(f"{str(r['window']):>6} | {r['N']:5d} | {r['L']:4.1f} | "
              f"{r['nullity_density']:.4f}    | {r['mystic_frac']:.3f}       | "
              f"{r['enrichment']:.3f}")

    mf_inf, _ = extrapolate(invL, np.array([r["mystic_frac"] for r in win_rows]))
    nd_inf, _ = extrapolate(invL, np.array([r["nullity_density"] for r in win_rows]))
    print(f"\nwindow 1/L→0 extrapolation:  mystic_frac → {mf_inf:.3f}   "
          f"nullity/N → {nd_inf:.4f}")
    if full:
        print(f"full graph (no boundary):    mystic_frac = {full['mystic_frac']:.3f}   "
              f"nullity/N = {full['nullity_density']:.4f}")
    # Expected clean nullity density = (Mystic compounds)/N = (N_Mystic/2)/N
    nm = next(r["n_mystic"] for r in recs if r["window"] == "full" and r["p"] == 0.0)
    nfull = next(r["n_kept"] for r in recs if r["window"] == "full" and r["p"] == 0.0)
    print(f"  (Mystic vertices/N on full graph = {nm/nfull:.3f}; "
          f"clean enrichment ≈ 1/that = {nfull/nm:.2f})")

    cross = crossover(recs)
    print("\n=== dilution: enrichment→1 crossover (p* where enrichment=1.1) ===")
    print("window |  p*(enrich=1.1)")
    for win in sorted(cross, key=lambda w: (w == "full", str(w))):
        ps = cross[win]["p_star"]
        print(f"{str(win):>6} |  {ps:.3f}" if ps else f"{str(win):>6} |  (no crossing)")
    pstars = [c["p_star"] for c in cross.values() if c["p_star"]]
    if pstars:
        print(f"\np* spread: {min(pstars):.3f}–{max(pstars):.3f} "
              f"(σ={np.std(pstars):.3f}) → "
              f"{'size-independent ⇒ smooth crossover' if np.std(pstars) < 0.03 else 'size-dependent ⇒ inspect'}")

    # --- figure ---
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 4.6))
    xs = np.linspace(0, invL.max() * 1.05, 50)
    for key, lab, color in [("mystic_frac", "Mystic-support frac", "C0"),
                            ("nullity_density", "nullity / N", "C1")]:
        y = np.array([r[key] for r in win_rows])
        a, b = extrapolate(invL, y)
        ax0.plot(invL, y, "o", color=color, label=f"{lab} (→{a:.3f})")
        ax0.plot(xs, a + b * xs, "--", color=color, lw=1)
        if full:
            ax0.plot(0, full[key], "*", color=color, ms=14)
    ax0.axhline(1.0, color="k", ls=":", lw=0.8)
    ax0.set_xlabel("1 / L (window side)")
    ax0.set_title("clean point: finite-size scaling (★ = full graph)")
    ax0.legend(fontsize=8)
    ax0.grid(alpha=0.3)

    for win in sorted(cross, key=lambda w: (w == "full", str(w))):
        c = cross[win]
        ax1.plot(c["ps"], c["enrichment"], "o-", ms=3, label=f"L={win}")
    ax1.axhline(1.0, color="k", ls="--", lw=0.8)
    ax1.set_xlabel("vacancy density p")
    ax1.set_ylabel("Mystic enrichment")
    ax1.set_title("dilution: enrichment → 1 (smooth crossover?)")
    ax1.legend(fontsize=7)
    ax1.grid(alpha=0.3)

    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=140)
    print(f"\nwrote {FIG}")


if __name__ == "__main__":
    main()

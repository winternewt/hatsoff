"""Comparative R-region figure: hat vs Spectre under site dilution (zero flux).

The paper's R3/R5 centerpiece. Both campaigns share a schema
(`deficiency`, `n_components`, `spanning.{either,largest_comp_frac}`):
  * hat     — `l3_rregion.jsonl`     (rregion_campaign.py)
  * Spectre — `spectre_rregion.jsonl` (spectre_rregion_campaign.py)

The contrast is **extensive vs intensive**, not raw spanning booleans: cropping
any window injects boundary monomers, so even the Spectre (bulk clean nullity 0)
shows a windowed clean R-region. The discriminator is the **size-scaling** of the
largest R-region component fraction:
  * hat — extensive clean R-region ⇒ `largest_comp_frac` at p=0 stays finite /
    grows with N, then de-percolates at finite p_c≈0.055;
  * Spectre — no clean R-region ⇒ `largest_comp_frac` at p=0 **decays with N**
    (boundary only); dilution *creates* the R-region (onset).

Panels:
  (a) deficiency density (deficiency/N) vs p, both substrates, size family
  (b) largest_comp_frac vs p, both substrates, size family
  (c) clean-point (p=0) largest_comp_frac vs N — the extensive-vs-intensive test

    uv run python experiments/spectre_vs_hat_rregion.py
Writes `docs/figures/hat_vs_spectre_rregion.png`.
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
HAT = EXP_DIR / "l3_rregion.jsonl"
SPECTRE = EXP_DIR / "spectre_rregion.jsonl"
FIG = EXP_DIR.parent / "docs" / "figures" / "hat_vs_spectre_rregion.png"


def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [
        r for r in (json.loads(line) for line in path.open() if line.strip())
        if "error" not in r
    ]


def aggregate(recs: list[dict]) -> dict:
    """{window: {p: {metric: mean}}} for deficiency density, comp frac, spanning."""
    buckets: dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for r in recs:
        nk = r["n_kept"] or 1
        buckets[r["window"]][r["p"]]["def_density"].append(r["deficiency"] / nk)
        buckets[r["window"]][r["p"]]["comp_frac"].append(
            r["spanning"]["largest_comp_frac"])
        buckets[r["window"]][r["p"]]["span"].append(
            1.0 if r["spanning"]["either"] else 0.0)
    out: dict = {}
    for win, pmap in buckets.items():
        out[win] = {p: {m: float(np.mean(v)) for m, v in mm.items()}
                    for p, mm in pmap.items()}
    return out


def clean_NL(recs: list[dict]) -> list[tuple[float, float]]:
    """(N, largest_comp_frac) at p=0, sorted by N."""
    pts = [(r["N"], r["spanning"]["largest_comp_frac"])
           for r in recs if r["p"] == 0.0]
    return sorted(set(pts))


def _plot_family(ax, agg: dict, metric: str, color, label: str) -> None:
    wins = sorted(agg.keys())
    for i, win in enumerate(wins):
        ps = sorted(agg[win])
        ys = [agg[win][p][metric] for p in ps]
        ax.plot(ps, ys, "-o", ms=3, color=color,
                alpha=0.35 + 0.6 * i / max(1, len(wins) - 1),
                label=label if i == len(wins) - 1 else None)


def main() -> None:
    hat, spec = load(HAT), load(SPECTRE)
    print(f"hat: {len(hat)} records; spectre: {len(spec)} records")
    if not spec:
        print("no spectre data yet — run spectre_rregion_campaign.py first")
        return
    ah, asp = aggregate(hat), aggregate(spec)

    fig, axes = plt.subplots(1, 3, figsize=(17, 4.8))

    _plot_family(axes[0], ah, "def_density", "C0", "hat")
    _plot_family(axes[0], asp, "def_density", "C3", "Spectre")
    axes[0].set(xlabel="vacancy density p", ylabel="deficiency / N",
                title="(a) deficiency density (≈ nullity/N)")

    _plot_family(axes[1], ah, "comp_frac", "C0", "hat")
    _plot_family(axes[1], asp, "comp_frac", "C3", "Spectre")
    axes[1].axvline(0.055, color="k", ls=":", lw=0.8)
    axes[1].set(xlabel="vacancy density p", ylabel="largest R-region / N",
                title="(b) R-region order parameter (dotted: hat p_c≈0.055)")

    for recs, color, lab in [(hat, "C0", "hat"), (spec, "C3", "Spectre")]:
        pts = clean_NL(recs)
        if pts:
            Ns, fr = zip(*pts)
            axes[2].plot(Ns, fr, "o-", color=color, ms=5, label=lab)
    axes[2].set(xlabel="window N", ylabel="largest R-region / N  (p=0)",
                title="(c) clean point: extensive (hat) vs intensive (Spectre)")

    for ax in axes:
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    fig.suptitle("Hat vs Spectre — Gallai–Edmonds R-region under site dilution "
                 "(zero flux)")
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=140)
    print(f"wrote {FIG}")

    # quick numeric contrast for the caption
    print("\nclean-point largest_comp_frac vs N:")
    for lab, recs in [("hat", hat), ("Spectre", spec)]:
        pts = clean_NL(recs)
        if pts:
            print(f"  {lab}: " + ", ".join(f"N={n}:{f:.3f}" for n, f in pts))


if __name__ == "__main__":
    main()

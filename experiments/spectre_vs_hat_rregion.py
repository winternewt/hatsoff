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
PERIODIC = EXP_DIR / "periodic_rregion.jsonl"
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


def _plot_family(ax, agg: dict, metric: str, color, label: str) -> None:
    wins = sorted(agg.keys())
    for i, win in enumerate(wins):
        ps = sorted(agg[win])
        ys = [agg[win][p][metric] for p in ps]
        ax.plot(ps, ys, "-o", ms=3, color=color,
                alpha=0.35 + 0.6 * i / max(1, len(wins) - 1),
                label=label if i == len(wins) - 1 else None)


def main() -> None:
    hat, spec, peri = load(HAT), load(SPECTRE), load(PERIODIC)
    print(f"hat: {len(hat)} records; spectre: {len(spec)} records; "
          f"periodic: {len(peri)} records")
    if not spec:
        print("no spectre data yet — run spectre_rregion_campaign.py first")
        return
    ah, asp = aggregate(hat), aggregate(spec)
    ape = aggregate(peri) if peri else None
    # (substrate, agg, colour, label)
    families = [(ah, "C0", "hat"), (asp, "C3", "Spectre")]
    if ape:
        families.append((ape, "C2", "periodic (tri.)"))

    fig, axes = plt.subplots(1, 3, figsize=(17, 4.8))

    for agg_, color, lab in families:
        _plot_family(axes[0], agg_, "def_density", color, lab)
    axes[0].set(xlabel="vacancy density p", ylabel="deficiency / N",
                title="(a) deficiency density (≈ nullity/N)")

    # Spanning probability vs p (seed-averaged for p>0).  NB the clean p=0 point
    # is a single realization per window and is boundary-parity contaminated for
    # Spectre/periodic — read the def-density panel (a) + full-graph nullity for
    # the clean contrast, not this p=0 value.  Dotted: hat p_c≈0.055 (from the
    # dedicated parity-controlled rregion_campaign, not this windowed overlay).
    for agg_, color, lab in families:
        _plot_family(axes[1], agg_, "span", color, lab)
    axes[1].axvline(0.055, color="k", ls=":", lw=0.8)
    axes[1].set(xlabel="vacancy density p", ylabel="P(R-region spans)",
                ylim=(-0.03, 1.03),
                title="(b) spanning prob vs p (p=0 boundary-noisy; dotted hat p_c≈0.055)")

    for agg_, color, lab in families:
        _plot_family(axes[2], agg_, "comp_frac", color, lab)
    axes[2].set(xlabel="vacancy density p", ylabel="largest R-region / N",
                title="(c) R-region order parameter")

    for ax in axes:
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    fig.suptitle("Hat vs Spectre vs periodic — Gallai–Edmonds R-region under "
                 "site dilution (zero flux): hat de-percolates, the others onset")
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=140)
    print(f"wrote {FIG}")

    # quick numeric contrast for the caption: P(span) at clean and small p
    print("\nP(span) at p=0 / p=0.02 / p=0.05 (mid window):")
    for lab, agg_ in [("hat", ah), ("Spectre", asp)] + (
            [("periodic", ape)] if ape else []):
        wins = sorted(agg_)
        w = wins[len(wins) // 2]
        row = agg_[w]
        def g(p: float) -> str:
            return f"{row[p]['span']:.2f}" if p in row else "  - "
        print(f"  {lab:9s} (L={w}): {g(0.0)} / {g(0.02)} / {g(0.05)}")


if __name__ == "__main__":
    main()

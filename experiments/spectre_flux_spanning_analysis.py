"""Analyse the π-flux support-spanning probe — crossover vs transition.

Reads `spectre_flux_spanning.jsonl`. For each proximity `d0`, plots the spanning
probability P(span) vs p across the window-size family. The question: does the
P(span) curve **sharpen / develop a size-independent crossing** as the window
grows (→ a genuine de-percolation transition) or stay a **smooth, drifting**
sigmoid (→ crossover / proxy threshold effect)?

⚠ This is the geometric `d0`-proxy (the one that faked p_c→0 on the hat); read
across `d0` and sizes, never a single curve. The robust statement remains the
size-independent enrichment crossover (`spectre_flux_consolidate.py`).

    uv run python experiments/spectre_flux_spanning_analysis.py
Writes `docs/figures/spectre_flux_spanning.png`.
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
JSONL = EXP_DIR / "spectre_flux_spanning.jsonl"
FIG = EXP_DIR.parent / "docs" / "figures" / "spectre_flux_spanning.png"


def load() -> list[dict]:
    return [
        r for r in (json.loads(line) for line in JSONL.open() if line.strip())
        if "error" not in r
    ]


def aggregate(recs: list[dict]) -> tuple[dict, list[str]]:
    """{d0: {window: {p: P(span)}}} and the sorted d0 list (as strings)."""
    d0s = sorted({k for r in recs for k in r["span"]}, key=float)
    acc: dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for r in recs:
        for d0, s in r["span"].items():
            acc[d0][r["window"]][r["p"]].append(1.0 if s["either"] else 0.0)
    out = {d0: {w: {p: float(np.mean(v)) for p, v in pm.items()}
                for w, pm in wm.items()}
           for d0, wm in acc.items()}
    return out, d0s


def p_cross(pmap: dict, level: float = 0.5) -> float | None:
    ps = sorted(pmap)
    ys = [pmap[p] for p in ps]
    for i in range(1, len(ps)):
        if (ys[i - 1] - level) * (ys[i] - level) <= 0 and ys[i - 1] != ys[i]:
            t = (ys[i - 1] - level) / (ys[i - 1] - ys[i])
            return ps[i - 1] + t * (ps[i] - ps[i - 1])
    return None


def main() -> None:
    recs = load()
    print(f"{len(recs)} records")
    if not recs:
        print("no data — run spectre_flux_spanning_campaign.py first")
        return
    agg, d0s = aggregate(recs)

    fig, axes = plt.subplots(1, len(d0s), figsize=(5.2 * len(d0s), 4.6),
                             squeeze=False)
    for ax, d0 in zip(axes[0], d0s):
        wins = sorted(agg[d0])
        print(f"\nd0={d0}: P(span)=0.5 crossing per window")
        for i, w in enumerate(wins):
            ps = sorted(agg[d0][w])
            ys = [agg[d0][w][p] for p in ps]
            ax.plot(ps, ys, "-o", ms=3,
                    alpha=0.4 + 0.6 * i / max(1, len(wins) - 1),
                    label=f"L={w}")
            pc = p_cross(agg[d0][w])
            print(f"  L={w}: p*={'%.3f' % pc if pc else 'none'}")
        ax.axhline(0.5, color="grey", ls=":", lw=0.8)
        ax.set(xlabel="vacancy density p", ylabel="P(support spans)",
               ylim=(-0.03, 1.03), title=f"d0={d0}")
        ax.legend(fontsize=7)
        ax.grid(alpha=0.3)
    fig.suptitle("π-flux support spanning (d0-PROXY — suggestive, not a verdict): "
                 "sharpening crossing = transition, drifting sigmoid = crossover")
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=140)
    print(f"\nwrote {FIG}")


if __name__ == "__main__":
    main()

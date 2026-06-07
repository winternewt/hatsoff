"""Aggregate + plot the π-flux Spectre dilution campaign.

Reads ``spectre_flux_campaign.jsonl`` and produces, with a window finite-size
family overlaid:

  1. π-flux nullity density (nullity / N_kept) vs vacancy density p
  2. Mystic support fraction vs p, with the Mystic *enrichment*
     (support_frac / mystic_vertex_frac) — > 1 means the kernel concentrates on
     Mystics (Singh--Flicker / nucleation picture)
  3. support participation ratio (gauge-invariant kernel localization) vs p

Writes ``docs/figures/spectre_flux.png`` and prints a summary table.

    uv run python experiments/spectre_flux_analysis.py
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
FIG = EXP_DIR.parent / "docs" / "figures" / "spectre_flux.png"


def load_records() -> list[dict]:
    recs = []
    with JSONL.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if "error" not in r:
                recs.append(r)
    return recs


def aggregate(recs: list[dict]) -> dict:
    """{window: {p: {metric: (mean, sem, n)}}} for the plotted metrics."""
    buckets: dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for r in recs:
        n_kept = r["n_kept"] or 1
        metrics = {
            "nullity_density": r["nullity"] / n_kept,
            "mystic_support_frac": r["mystic_support_frac"],
            "mystic_enrichment": (
                r["mystic_support_frac"] / (r["n_mystic"] / n_kept)
                if r["n_mystic"] else 0.0
            ),
            "support_pr": r["support_pr"],
        }
        for name, val in metrics.items():
            buckets[r["window"]][r["p"]][name].append(val)

    out: dict = {}
    for win, pmap in buckets.items():
        out[win] = {}
        for p, mmap in pmap.items():
            out[win][p] = {
                name: (float(np.mean(v)), float(np.std(v) / np.sqrt(len(v))), len(v))
                for name, v in mmap.items()
            }
    return out


def plot(agg: dict) -> None:
    metrics = [
        ("nullity_density", "π-flux nullity / N", "nullity density"),
        ("mystic_enrichment", "Mystic support enrichment", "enrichment (=1: uniform)"),
        ("support_pr", "support participation ratio", "PR of diag(P)"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    windows = sorted(agg.keys(), key=lambda w: (w == "full", w))
    for ax, (key, title, ylab) in zip(axes, metrics):
        for win in windows:
            ps = sorted(agg[win].keys())
            ys = [agg[win][p][key][0] for p in ps]
            es = [agg[win][p][key][1] for p in ps]
            ax.errorbar(ps, ys, yerr=es, marker="o", ms=4, capsize=2,
                        label=f"L={win}")
        ax.set_xlabel("vacancy density p")
        ax.set_ylabel(ylab)
        ax.set_title(title)
        ax.grid(alpha=0.3)
        if key == "mystic_enrichment":
            ax.axhline(1.0, color="k", ls="--", lw=0.8)
    axes[0].legend(fontsize=8)
    fig.suptitle("π-flux Spectre under site dilution (Mystic sector)")
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=140)
    print(f"wrote {FIG}", flush=True)


def main() -> None:
    recs = load_records()
    print(f"{len(recs)} records", flush=True)
    if not recs:
        return
    agg = aggregate(recs)
    print("\nwindow |   p  | n | nullity/N | mystic_frac | enrichment | support_PR")
    for win in sorted(agg.keys(), key=lambda w: (w == "full", str(w))):
        for p in sorted(agg[win].keys()):
            c = agg[win][p]
            n = c["nullity_density"][2]
            print(f"{str(win):>6} | {p:.2f} | {n:3d} | "
                  f"{c['nullity_density'][0]:.4f}    | "
                  f"{c['mystic_support_frac'][0]:.3f}       | "
                  f"{c['mystic_enrichment'][0]:.3f}      | "
                  f"{c['support_pr'][0]:.1f}")
    plot(agg)


if __name__ == "__main__":
    main()

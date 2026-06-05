"""Aggregate the L3 campaign JSONL into a summary + figures.

Idempotent and safe to run on partial data mid-run:

    uv run python experiments/aggregate_campaign.py

Reads ``experiments/l3_campaign.jsonl``; writes
``experiments/l3_campaign_summary.json`` and two figures under
``docs/figures/``.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

EXP_DIR = Path(__file__).parent
SUMMARY = EXP_DIR / "l3_campaign_summary.json"
FIG_DIR = EXP_DIR.parent / "docs" / "figures"


def load_all() -> list[dict]:
    """Load every record from the single-node file and all rank shards.

    Matches ``l3_campaign.jsonl`` and ``l3_campaign.rank###.jsonl``; the
    deterministic seeds make shard work disjoint, so a plain concatenation has
    no duplicate units.
    """
    records: list[dict] = []
    seen: set[str] = set()
    for path in sorted(EXP_DIR.glob("l3_campaign*.jsonl")):
        with path.open() as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                key = rec.get("key")
                if key in seen:
                    continue
                seen.add(key)
                records.append(rec)
    return records


def _stats(values: list[float]) -> dict:
    arr = np.asarray(values, dtype=float)
    return {
        "mean": float(arr.mean()),
        "std": float(arr.std()),
        "sem": float(arr.std() / np.sqrt(len(arr))) if len(arr) else 0.0,
        "n": int(arr.size),
    }


def aggregate_stage_a(records: list[dict]) -> dict:
    by: dict[tuple, list[dict]] = defaultdict(list)
    for r in records:
        if r["stage"] == "A" and "error" not in r:
            by[(r["level"], r["p"])].append(r)
    fields = ["N", "nullity", "deficiency", "gap", "trapped", "trapped_frac",
              "c_D", "max_critical", "n_critical_gt1"]
    out: dict = defaultdict(dict)
    for (level, p), rs in sorted(by.items()):
        out[str(level)][str(p)] = {f: _stats([r[f] for r in rs]) for f in fields}
    return dict(out)


def aggregate_stage_b(records: list[dict]) -> dict:
    by: dict[tuple, list[dict]] = defaultdict(list)
    for r in records:
        if r["stage"] == "B" and "spanning" in r:
            by[(r["window"], r["p"])].append(r)
    out: dict = defaultdict(dict)
    for (frac, p), rs in sorted(by.items()):
        d0s = sorted(rs[0]["spanning"].keys(), key=float)
        per_d0 = {
            d0: {
                "P_span": _stats([1.0 if r["spanning"][d0]["either"] else 0.0
                                  for r in rs]),
                "max_cluster_frac": _stats(
                    [r["spanning"][d0]["max_cluster_frac"] for r in rs]),
            }
            for d0 in d0s
        }
        out[str(frac)][str(p)] = {
            "L": float(np.mean([r["L"] for r in rs])),
            "active_frac": _stats([r["n_active"] / max(r["n_kept"], 1)
                                   for r in rs]),
            "per_d0": per_d0,
        }
    return dict(out)


def plot_stage_a(agg: dict, out: Path) -> None:
    if not agg:
        return
    fig, ax = plt.subplots(2, 2, figsize=(11, 8))
    for level, pmap in sorted(agg.items()):
        ps = sorted(float(p) for p in pmap)
        keys = [str(p) for p in ps]
        nul = [pmap[k]["nullity"]["mean"] for k in keys]
        nul_e = [pmap[k]["nullity"]["std"] for k in keys]
        defv = [pmap[k]["deficiency"]["mean"] for k in keys]
        gap = [pmap[k]["gap"]["mean"] for k in keys]
        gap_e = [pmap[k]["gap"]["sem"] for k in keys]
        tf = [pmap[k]["trapped_frac"]["mean"] for k in keys]
        mc = [pmap[k]["max_critical"]["mean"] for k in keys]
        ax[0, 0].errorbar(ps, nul, yerr=nul_e, marker="o", label=f"L{level} null")
        ax[0, 0].plot(ps, defv, marker="s", ls="--", alpha=0.6,
                      label=f"L{level} def")
        ax[0, 1].errorbar(ps, gap, yerr=gap_e, marker="o", label=f"L{level}")
        ax[1, 0].plot(ps, tf, marker="o", label=f"L{level}")
        ax[1, 1].plot(ps, mc, marker="o", label=f"L{level}")
    ax[0, 0].set(xlabel="site removal p", ylabel="count",
                 title="Zero modes vs dilution")
    ax[0, 0].legend(fontsize=8)
    ax[0, 1].axhline(0, color="grey", lw=0.8)
    ax[0, 1].set(xlabel="site removal p", ylabel="nullity - deficiency",
                 title="Non-bipartite gap (size scaling)")
    ax[0, 1].legend(fontsize=8)
    ax[1, 0].set(xlabel="site removal p", ylabel="trapped weight fraction",
                 title="Locally trapped zero modes")
    ax[1, 0].legend(fontsize=8)
    ax[1, 1].set(xlabel="site removal p",
                 ylabel="max factor-critical component size",
                 title="Largest odd (factor-critical) component")
    ax[1, 1].legend(fontsize=8)
    fig.suptitle("Stage A — zero-mode counting & Gallai-Edmonds scaling")
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    plt.close(fig)


def plot_stage_b(agg: dict, out: Path) -> None:
    if not agg:
        return
    fracs = sorted(agg.keys(), key=float)
    all_d0 = sorted(next(iter(agg[fracs[0]].values()))["per_d0"].keys(),
                    key=float)
    # primary d0 = the middle one (where the transition lives)
    primary = all_d0[len(all_d0) // 2]
    largest = fracs[-1]

    fig, ax = plt.subplots(1, 3, figsize=(16, 5))
    # (0) window finite-size family at primary d0 -> crossing ≈ p_c
    for frac in fracs:
        pmap = agg[frac]
        ps = sorted(float(p) for p in pmap)
        keys = [str(p) for p in ps]
        lval = pmap[keys[0]]["L"]
        y = [pmap[k]["per_d0"][primary]["P_span"]["mean"] for k in keys]
        e = [pmap[k]["per_d0"][primary]["P_span"]["sem"] for k in keys]
        ax[0].errorbar(ps, y, yerr=e, marker="o", label=f"L≈{lval:.1f}")
    ax[0].set(xlabel="site removal p", ylabel="P(support spans)",
              title=f"Window crossing at d0={primary} (cross ≈ p_c)",
              ylim=(-0.05, 1.05))
    ax[0].legend(fontsize=8)
    # (1) d0 sensitivity at the largest window
    pmap = agg[largest]
    ps = sorted(float(p) for p in pmap)
    keys = [str(p) for p in ps]
    for d0 in all_d0:
        y = [pmap[k]["per_d0"][d0]["P_span"]["mean"] for k in keys]
        ax[1].plot(ps, y, marker="o", label=f"d0={d0}")
    ax[1].set(xlabel="site removal p", ylabel="P(support spans)",
              title=f"d0 sensitivity (largest window, frac {largest})",
              ylim=(-0.05, 1.05))
    ax[1].legend(fontsize=8)
    # (2) active fraction + largest-cluster fraction at primary d0
    for frac in fracs:
        pmap = agg[frac]
        ps = sorted(float(p) for p in pmap)
        keys = [str(p) for p in ps]
        mc = [pmap[k]["per_d0"][primary]["max_cluster_frac"]["mean"]
              for k in keys]
        ax[2].plot(ps, mc, marker="o", label=f"frac {frac}")
    ax[2].set(xlabel="site removal p",
              ylabel="largest support cluster / N",
              title=f"Largest support cluster at d0={primary}")
    ax[2].legend(fontsize=8)
    fig.suptitle("Stage B — zero-mode support spatial spanning (proximity proxy)")
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    plt.close(fig)


def main() -> None:
    records = load_all()
    stage_a = aggregate_stage_a(records)
    stage_b = aggregate_stage_b(records)
    n_a = sum(1 for r in records if r["stage"] == "A")
    n_b = sum(1 for r in records if r["stage"] == "B")
    summary = {
        "n_records": len(records), "n_stage_a": n_a, "n_stage_b": n_b,
        "stage_a": stage_a, "stage_b": stage_b,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2))
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plot_stage_a(stage_a, FIG_DIR / "campaign_stage_a.png")
    plot_stage_b(stage_b, FIG_DIR / "campaign_stage_b.png")
    print(f"records={len(records)} (A={n_a}, B={n_b}) -> {SUMMARY.name}, "
          f"figures in {FIG_DIR}", flush=True)


if __name__ == "__main__":
    main()

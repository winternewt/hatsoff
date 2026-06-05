"""Site-dilution sweep on the hat tight-binding graph (Phase 3, step a).

For a grid of removal probabilities p and several disorder realizations,
measures how the adjacency null space grows and localizes:

    nullity(p)        true zero-mode count      = dim ker A
    deficiency(p)     structural matching count = N - 2*nu
    gap(p)            nullity - deficiency      (0 in the bipartite regime;
                                                 non-zero from odd
                                                 factor-critical components)
    trapped(p)        # fully localized modes   (sites with diag(P) ~ 1)
    trapped_frac(p)   fraction of zero-mode weight on fully-trapped sites
    gyration(p)       support radius of gyration / sample radius -- an
                      extent-based localization proxy (1 = spread over the
                      whole sample, ->0 = pinned).

NB: a true support-*percolation* order parameter (does the support set span
the sample) needs a spatial crossing test, deferred to campaign step 2: the
zero modes live on even-distance sites, so support-active sites are rarely
directly bonded and a naive graph-cluster metric is degenerate.

Writes JSON + a summary table to ``experiments/`` and a figure to
``docs/figures/``.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from hat_amp.tiling import generate_tiling
from hatsoff.dilution import dilute_sites
from hatsoff.graph import build_tb_graph
from hatsoff.matching import adjacency_to_graph, deficiency, nullspace_support

LEVEL = 2
P_GRID = [0.0, 0.02, 0.05, 0.08, 0.10, 0.15, 0.20, 0.25, 0.30]
N_REALIZATIONS = 20
TRAPPED_THRESHOLD = 0.99
SEED = 12345


def _support_gyration(vertices: np.ndarray, support: np.ndarray) -> float:
    """Support radius of gyration / sample radius of gyration.

    1 ~ support spread over the whole sample; ->0 ~ pinned to a small region.
    """
    total = support.sum()
    if total <= 0 or vertices.shape[0] == 0:
        return 0.0
    cm = (support[:, None] * vertices).sum(axis=0) / total
    rg2_supp = (support * np.sum((vertices - cm) ** 2, axis=1)).sum() / total
    sample_cm = vertices.mean(axis=0)
    rg2_sample = np.mean(np.sum((vertices - sample_cm) ** 2, axis=1))
    if rg2_sample <= 0:
        return 0.0
    return float(np.sqrt(rg2_supp / rg2_sample))


def run() -> dict:
    polys = generate_tiling(LEVEL)
    verts, adj = build_tb_graph(polys)
    n_full = adj.shape[0]
    rng = np.random.default_rng(SEED)

    summary: list[dict] = []
    for p in P_GRID:
        nul, defi, gap, trapped, tfrac, gyr, n_kept = [], [], [], [], [], [], []
        for _ in range(N_REALIZATIONS):
            sv, sa, kept = dilute_sites(verts, adj, p, rng)
            n = sa.shape[0]
            nz, support = nullspace_support(sa)
            graph = adjacency_to_graph(sa)
            d = deficiency(graph)
            n_trap = int(np.sum(support > TRAPPED_THRESHOLD))
            nul.append(nz)
            defi.append(d)
            gap.append(nz - d)
            trapped.append(n_trap)
            tfrac.append(
                support[support > TRAPPED_THRESHOLD].sum() / nz if nz else 0.0
            )
            gyr.append(_support_gyration(sv, support))
            n_kept.append(n)
        row = {
            "p": p,
            "n_kept": float(np.mean(n_kept)),
            "nullity": float(np.mean(nul)),
            "nullity_std": float(np.std(nul)),
            "deficiency": float(np.mean(defi)),
            "gap": float(np.mean(gap)),
            "gap_std": float(np.std(gap)),
            "trapped": float(np.mean(trapped)),
            "trapped_frac": float(np.mean(tfrac)),
            "gyration": float(np.mean(gyr)),
            "gyration_std": float(np.std(gyr)),
        }
        summary.append(row)
        print(
            f"p={p:<5} N={row['n_kept']:6.1f} "
            f"null={row['nullity']:6.2f}±{row['nullity_std']:4.2f} "
            f"def={row['deficiency']:6.2f} gap={row['gap']:+5.2f} "
            f"trapped={row['trapped']:5.2f} "
            f"tfrac={row['trapped_frac']:.2f} gyr={row['gyration']:.3f}",
            flush=True,
        )
    return {
        "level": LEVEL,
        "n_full": n_full,
        "n_realizations": N_REALIZATIONS,
        "trapped_threshold": TRAPPED_THRESHOLD,
        "rows": summary,
    }


def plot(result: dict, out: Path) -> None:
    rows = result["rows"]
    p = [r["p"] for r in rows]
    fig, ax = plt.subplots(2, 2, figsize=(11, 8))

    ax[0, 0].errorbar(p, [r["nullity"] for r in rows],
                      yerr=[r["nullity_std"] for r in rows], marker="o",
                      label="nullity n0")
    ax[0, 0].plot(p, [r["deficiency"] for r in rows], marker="s",
                  label="deficiency N-2nu")
    ax[0, 0].set(xlabel="site removal p", ylabel="count",
                 title="Zero modes vs dilution")
    ax[0, 0].legend()

    ax[0, 1].axhline(0, color="grey", lw=0.8)
    ax[0, 1].errorbar(p, [r["gap"] for r in rows],
                      yerr=[r["gap_std"] for r in rows], marker="o",
                      color="C3")
    ax[0, 1].set(xlabel="site removal p", ylabel="n0 - deficiency",
                 title="Non-bipartite gap (odd factor-critical comps)")

    ax[1, 0].plot(p, [r["trapped"] for r in rows], marker="o", color="C2",
                  label="# trapped modes")
    ax[1, 0].plot(p, [r["trapped_frac"] * r["nullity"] for r in rows],
                  marker="x", ls="--", color="C2", alpha=0.5)
    ax2 = ax[1, 0].twinx()
    ax2.plot(p, [r["trapped_frac"] for r in rows], marker="s", color="C5")
    ax2.set_ylabel("trapped weight fraction", color="C5")
    ax[1, 0].set(xlabel="site removal p", ylabel="# fully-trapped modes",
                 title="Locally trapped zero modes")

    ax[1, 1].errorbar(p, [r["gyration"] for r in rows],
                      yerr=[r["gyration_std"] for r in rows],
                      marker="o", color="C4")
    ax[1, 1].set(xlabel="site removal p",
                 ylabel="support Rg / sample Rg", ylim=(0, 1.05),
                 title="Zero-mode support extent")

    fig.suptitle(f"Zero-mode dilution sweep, H level {result['level']} "
                 f"(N={result['n_full']}, R={result['n_realizations']})")
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"figure -> {out}", flush=True)


def main() -> None:
    result = run()
    exp_dir = Path(__file__).parent
    fig_dir = exp_dir.parent / "docs" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    (exp_dir / "dilution_sweep_L2.json").write_text(json.dumps(result, indent=2))
    plot(result, fig_dir / "dilution_sweep_L2.png")


if __name__ == "__main__":
    main()

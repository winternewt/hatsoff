"""Finite-size analysis of zero-mode support spanning: does p_c(L) -> 0?

Reads ``experiments/l3_campaign_summary.json`` (produced by
``aggregate_campaign.py``) and, for each proximity distance ``d0`` and each
crop-window size ``L``, extracts the spanning threshold ``p_c(L)`` as the
linearly-interpolated site-removal probability where the spanning probability
``P_span`` crosses ``0.5``.  It then fits ``p_c(L)`` against ``1/L`` and reports
the ``L -> infinity`` intercept: an intercept consistent with zero is the
quantitative statement of finding #4 (``p_c -> 0`` on the aperiodic monotile,
unlike the finite ``p_c`` of every periodic lattice in the Damle program).

    uv run python experiments/pc_collapse.py

Writes ``docs/figures/pc_collapse.png`` and prints the crossing / fit table.
This is the **proximity-proxy** order parameter (``d0``-dependent); the result
is reported as the whole ``d0`` family, never a single ``d0`` (see
``docs/PERCOLATION.md``).
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

EXP_DIR = Path(__file__).parent
SUMMARY = EXP_DIR / "l3_campaign_summary.json"
FIG = EXP_DIR.parent / "docs" / "figures" / "pc_collapse.png"
CROSS = 0.5


def crossing(ps: np.ndarray, span: np.ndarray, level: float = CROSS) -> float | None:
    """Linearly-interpolated p where ``span`` first drops through ``level``.

    ``span`` is monotone-ish decreasing in ``ps``.  Returns ``None`` if the
    curve never crosses (stays above or starts below the level over the grid).
    """
    for i in range(len(ps) - 1):
        a, b = span[i], span[i + 1]
        if (a - level) >= 0.0 > (b - level):
            t = (a - level) / (a - b) if a != b else 0.0
            return float(ps[i] + t * (ps[i + 1] - ps[i]))
    return None


def collect(summary: dict) -> tuple[list[str], dict[str, list[tuple[float, float]]]]:
    """Return (d0 list, {d0: [(L, p_c(L)), ...] sorted by L})."""
    sb = summary["stage_b"]
    windows = sorted(sb.keys(), key=float)
    d0_list = sorted(next(iter(sb[windows[0]].values()))["per_d0"].keys(),
                     key=float)
    out: dict[str, list[tuple[float, float]]] = {d0: [] for d0 in d0_list}
    for w in windows:
        pmap = sb[w]
        ps = np.array(sorted(float(p) for p in pmap))
        keys = [str(p) if str(p) in pmap else f"{p}" for p in ps]
        # robust key lookup (p values stored as their float repr)
        kl = {float(k): k for k in pmap}
        keys = [kl[p] for p in ps]
        lval = pmap[keys[0]]["L"]
        for d0 in d0_list:
            span = np.array([pmap[k]["per_d0"][d0]["P_span"]["mean"] for k in keys])
            pc = crossing(ps, span)
            if pc is not None:
                out[d0].append((lval, pc))
    for d0 in out:
        out[d0].sort()
    return d0_list, out


def fit_intercept(ls: np.ndarray, pcs: np.ndarray) -> tuple[float, float, float]:
    """Least-squares ``p_c = a + b * (1/L)``; return (a, b, a_stderr)."""
    x = 1.0 / ls
    A = np.vstack([np.ones_like(x), x]).T
    coef, res, *_ = np.linalg.lstsq(A, pcs, rcond=None)
    a, b = float(coef[0]), float(coef[1])
    n = len(x)
    if n > 2:
        resid = pcs - (a + b * x)
        s2 = float(resid @ resid) / (n - 2)
        cov = s2 * np.linalg.inv(A.T @ A)
        a_se = float(np.sqrt(cov[0, 0]))
    else:
        a_se = float("nan")
    return a, b, a_se


def main() -> None:
    summary = json.loads(SUMMARY.read_text())
    d0_list, by_d0 = collect(summary)

    print(f"{'d0':>5} {'L':>8} {'p_c(L)':>8}")
    fits: dict[str, tuple[float, float, float]] = {}
    for d0 in d0_list:
        pts = by_d0[d0]
        for lval, pc in pts:
            print(f"{d0:>5} {lval:8.1f} {pc:8.4f}")
        if len(pts) >= 2:
            ls = np.array([p[0] for p in pts])
            pcs = np.array([p[1] for p in pts])
            a, b, a_se = fit_intercept(ls, pcs)
            fits[d0] = (a, b, a_se)
            print(f"      -> fit p_c = {a:+.4f} + {b:.3f}/L   "
                  f"(L->inf intercept = {a:.4f} +/- {a_se:.4f})")
    print()

    # ---- figure -----------------------------------------------------------
    sb = summary["stage_b"]
    windows = sorted(sb.keys(), key=float)
    primary = d0_list[len(d0_list) // 2]  # middle d0 = where transition lives
    fig, ax = plt.subplots(1, 2, figsize=(13, 5.2))

    # (a) P_span vs p for each window size at the primary d0
    for w in windows:
        pmap = sb[w]
        kl = {float(k): k for k in pmap}
        ps = np.array(sorted(kl))
        keys = [kl[p] for p in ps]
        lval = pmap[keys[0]]["L"]
        y = [pmap[k]["per_d0"][primary]["P_span"]["mean"] for k in keys]
        e = [pmap[k]["per_d0"][primary]["P_span"]["sem"] for k in keys]
        ax[0].errorbar(ps, y, yerr=e, marker="o", capsize=2, label=f"L≈{lval:.0f}")
    ax[0].axhline(CROSS, color="grey", ls=":", lw=1)
    ax[0].set(xlabel="site removal probability p",
              ylabel="P(zero-mode support spans)",
              title=f"Spanning collapses with size (d0={primary})",
              ylim=(-0.05, 1.05))
    ax[0].legend(title="window", fontsize=9)
    ax[0].annotate("larger L\n→ lower crossing", xy=(0.045, 0.5),
                   xytext=(0.12, 0.7), fontsize=9,
                   arrowprops=dict(arrowstyle="->", color="black"))

    # (b) p_c(L) vs 1/L for all d0, with linear extrapolation to 1/L -> 0
    colors = plt.cm.viridis(np.linspace(0.1, 0.85, len(d0_list)))
    for d0, c in zip(d0_list, colors):
        pts = by_d0[d0]
        if len(pts) < 2:
            continue
        ls = np.array([p[0] for p in pts])
        pcs = np.array([p[1] for p in pts])
        inv = 1.0 / ls
        a, b, a_se = fits[d0]
        ax[1].plot(inv, pcs, "o", color=c, label=f"d0={d0}: a={a:+.3f}")
        xx = np.linspace(0.0, inv.max() * 1.05, 50)
        ax[1].plot(xx, a + b * xx, "-", color=c, lw=1.4, alpha=0.8)
        ax[1].errorbar([0.0], [a], yerr=[a_se if np.isfinite(a_se) else 0.0],
                       fmt="*", color=c, ms=12, capsize=3)
    ax[1].axhline(0.0, color="grey", ls="--", lw=1)
    ax[1].set(xlabel="1 / L", ylabel="spanning threshold  p_c(L)",
              title="Extrapolation: p_c(L) → 0 as L → ∞", xlim=(-0.002, None))
    ax[1].legend(fontsize=9)

    fig.suptitle("Finding #4 — zero-mode support spanning threshold vanishes "
                 "in the thermodynamic limit (proximity proxy)")
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=140)
    plt.close(fig)
    print(f"wrote {FIG}")


if __name__ == "__main__":
    main()

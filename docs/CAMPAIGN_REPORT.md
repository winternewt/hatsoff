# L3 campaign — conclusive report

Final analysis of the long single-node campaign
(`experiments/l3_campaign.py`). The run completed on **2026-06-06**
(`heartbeat = done`) after resuming once from a checkpoint; it reached its 24 h
Stage-B wall-clock budget with the full planned grid populated.

- **Records:** 5390 total — Stage A = 1082, Stage B = 4308.
- **Statistics:** 60 disorder realizations per Stage-A point; **~120 per
  Stage-B point** (p = 0 is the single deterministic clean realization).
- **Reproduce:** `uv run python experiments/aggregate_campaign.py` (summary +
  `docs/figures/campaign_stage_{a,b}.png`) then
  `uv run python experiments/pc_collapse.py` (the finding-#4 figure +
  crossing/fit table → `docs/figures/pc_collapse.png`).
- **Source data:** `experiments/l3_campaign_summary.json`
  (from `l3_campaign.jsonl`).

System sizes: full L2 graph N = 1084, full L3 graph N = 7047; Stage-B crop
windows of side L ≈ 35, 49, 62, 75 (fractions 0.40/0.55/0.70/0.85 of the L3
patch extent). Site-removal grid p ∈ {0, .02, .05, .08, .10, .12, .15, .20,
.25, .30}.

---

## Headline (finding #4): the spanning threshold vanishes as L → ∞

The spatial spanning probability of the zero-mode support, `P_span(p, L)`,
**decreases monotonically with system size at every finite p** and is pinned to
1 only at the clean point p = 0. Extracting the threshold `p_c(L)` as the
interpolated crossing `P_span = ½` and fitting `p_c(L) = a + b/L`, the
`L → ∞` intercept `a` is **statistically consistent with zero** for both
proximity distances where a transition exists in-window:

| d0 | p_c(L=35) | p_c(L=49) | p_c(L=62) | p_c(L=75) | intercept a (L→∞) |
|----|-----------|-----------|-----------|-----------|-------------------|
| 1.2 | 0.0481 | 0.0424 | 0.0377 | 0.0186 | **+0.0037 ± 0.0145** |
| 1.4 | 0.0609 | 0.0466 | 0.0427 | 0.0195 | **−0.0048 ± 0.0152** |
| 1.0 | — (support too sparse to span; no crossing on the grid) | | | | — |
| 1.6 | — (support spans up to large p; only L≈75 crosses in-grid) | | | | — |

Figure: `docs/figures/pc_collapse.png` — left, the `P_span(p)` family
collapsing to lower crossings with size; right, `p_c(L)` vs `1/L` with the
linear extrapolation hitting ~0 at `1/L → 0`.

**Interpretation.** On the aperiodic hat substrate the zero-mode support spans
*only* in the clean limit; any finite site dilution destroys the spanning
R-region in the thermodynamic limit. This contrasts every periodic lattice in
the Damle program — square/honeycomb (PRX 2022), triangular/Shastry–Sutherland
(arXiv:2311.05634), kagome (arXiv:2512.23639) — all of which have a **finite**
threshold. Per the 2026-06-05 deep-research scan (`docs/NOVELTY.md`), this is a
genuine, aperiodicity-driven departure, *not* Gade–Wegner chiral-class folklore
(that concerns Anderson-localization scaling of generic E=0 states, a different
object from the combinatorial support of the protected subspace).

### Caveats on the headline (read before quoting it as physics)

- **Proximity proxy.** `P_span` is built from a proximity graph on
  support-carrying sites with linking distance `d0` (zero modes live on
  even-distance sites). It is *not* a first-principles spanning order parameter.
  d0 = 1.0 links almost nothing (no spanning at all); d0 = 1.6 links almost
  everything (spans up to large p). Only the intermediate d0 = 1.2 / 1.4 carry
  the transition — and *both* extrapolate to ~0, which is the robustness we can
  claim. Do **not** quote a single-d0 p_c as physical.
- **Few sizes, mild curvature.** Four window sizes, and the largest window's
  p_c drops faster than a clean 1/L line (visible curvature). The intercept is
  consistent with zero but the error bar (~0.015) is comparable to the smaller
  p_c values; this demonstrates a *strong downward trend to ≈0*, not a
  high-precision exponent. A rigorous per-mode / R-region order parameter and
  more sizes are the upgrade path before this is the paper's load-bearing claim.

---

## Stage A — zero-mode counting & Gallai–Edmonds scaling (full L2/L3)

60 realizations per p. Figure: `docs/figures/campaign_stage_a.png`.

L3 (N = 7047 clean):

| p | N | nullity | deficiency | gap (null−def) | trapped frac | max blossom | c(D) |
|---|---|---------|-----------|----------------|--------------|-------------|------|
| 0.00 | 7047 | 51.0 | 51.0 | 0.00 | 0.000 | 1 | 2313 |
| 0.02 | 6907 | 96.0 | 97.1 | −1.13 | 0.020 | 47.9 | 2196 |
| 0.05 | 6691 | 173.7 | 175.2 | −1.48 | 0.068 | 41.7 | 2002 |
| 0.08 | 6484 | 255.3 | 256.9 | −1.50 | 0.120 | 32.0 | 1910 |
| 0.10 | 6345 | 310.5 | 312.2 | **−1.72** | 0.151 | 24.1 | 1885 |
| 0.12 | 6201 | 366.6 | 367.9 | −1.35 | 0.183 | 17.1 | 1847 |
| 0.15 | 5992 | 444.7 | 445.8 | −1.08 | 0.226 | 13.9 | 1824 |
| 0.20 | 5635 | 582.0 | 582.5 | −0.58 | 0.303 | 9.2 | 1798 |
| 0.25 | 5283 | 705.7 | 706.1 | −0.42 | 0.367 | 4.9 | 1781 |
| 0.30 | 4932 | 812.5 | 812.8 | −0.25 | 0.435 | 3.8 | 1754 |

Three structural results, now with full statistics:

1. **nullity ≈ deficiency, with a small *negative* non-bipartite gap.** The
   nullity tracks the matching deficiency closely (the matching/zero-mode
   correspondence holds), but sits *below* it — gap = nullity − def < 0 — and
   the gap is **extensive**: it deepens from ≈ −0.2 (L2) to a peak ≈ **−1.7 at
   L3, p ≈ 0.10**, i.e. it grows with system size. (L2 row for comparison: gap
   stays in [−0.4, 0].) This is the genuinely non-bipartite content; on a
   bipartite graph the gap would vanish.
2. **Trapped-weight fraction is intensive.** The fraction of kernel weight on
   fully-localized (diag P > 0.99) sites rises 0 → ~0.44 with p and the **L2
   and L3 curves coincide** (0.440 vs 0.435 at p = 0.30) — a size-independent
   collapse, the expected monomer/R-type picture.
3. **Largest factor-critical ("blossom") component grows with size and peaks at
   small p.** Max blossom size ≈ 16 at L2 (peak p ≈ 0.05) vs ≈ **48 at L3 (peak
   p ≈ 0.02)**, decaying as p increases. The incipient-percolation R-region
   geometry; its growth with size is what underlies finding #4.

Per the novelty scan these (#1/#3) are *supporting structural diagnostics* —
the GE machinery is the Damle group's; the aperiodic-specific quantification
(the small-p blossom peak, the extensive negative gap tied to the inflation
structure) is what is ours. #2 alone is low-novelty.

---

## What this run does and does not settle

**Settles (with statistics):**
- The clean-limit count gate (nullity 8 / 51 at L2 / L3) and nullity ≈ def under
  dilution.
- The qualitative finding-#4 trend is real and well-sampled (~120 seeds/point,
  4 sizes): `P_span` collapses with size; both transitional d0 extrapolate to
  p_c(L→∞) ≈ 0.
- Stage-A structural scalings (#1 extensive negative gap, #2 intensive trapped
  fraction, #3 growing small-p blossom).

**Does not settle (next steps, in priority order):**
1. A **non-proxy** spanning order parameter (per-mode / R-region spanning rather
   than a d0-proximity graph) — the single highest-leverage upgrade before #4 is
   load-bearing.
2. **More sizes** (and/or larger L via the SLURM/GPU cluster path) to pin the
   curvature and quote a real exponent ν, not just "intercept ≈ 0".
3. Optional **vertex-TB multifractal / IPR** sketch separating E = 0 from E ≠ 0
   (would be the first such data on the hat; preempts a TB version of
   Daníelsson–Sigurðsson — see `docs/REFLIST.md` [D1]).

Per CLAUDE.md: do **not** bump R / go to cluster until (1) is in hand.

---

## Numerical note

One unit in the *pre-fix* run hit a LAPACK `syevd` non-convergence
(`np.linalg.eigh` "Eigenvalues did not converge"); the current
`support.kernel_support` routes dense eigh through `_cpu_dense_eigh`, which falls
back to `scipy.linalg.eigh(driver="evr")`, and the resumed run completed clean.
The campaign's `safe_record` also isolates any single-unit failure (logs an
error record, marks the key done) so one bad realization never aborts the run.
No data loss; the failed key carried no usable record and is a negligible
fraction of 4308 Stage-B units.

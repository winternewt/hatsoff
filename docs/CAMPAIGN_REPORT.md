# L3 campaign — conclusive report

> **⚠ MAJOR UPDATE (2026-06-06, rigorous cross-check) — finding #4 does NOT
> survive.** The parameter-free Gallai–Edmonds **R-region** spanning order
> parameter (`rregion_campaign.py`, 8 sizes L≈27–75, **300 seeds/cell**) gives a
> **FINITE** spanning threshold **p_c ≈ 0.055** (linear extrapolation
> 0.0546 ± 0.0066), *not* p_c → 0. The "p_c → 0" below was an artifact of the
> `d0`-proximity proxy. Under the matching-theoretic order parameter the hat's
> zero-mode R-region percolates at a finite vacancy density — qualitatively
> **like** the periodic Damle lattices, not unlike them. See the new section
> **"Rigorous cross-check (the decisive result)"** below; the proxy section that
> follows is retained for the record but is **superseded**.

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

## Rigorous cross-check (the decisive result) — p_c is FINITE

`experiments/rregion_campaign.py` (multiprocess, 15 cores) +
`rregion_analysis.py`; figure `docs/figures/rregion_collapse.png`. Same L3
substrate, **8 window sizes** L ≈ 27/35/42/49/55/62/68/75, **300 seeds/cell**
(p=0 is the single clean realization). For the four shared sizes the disorder
realizations are *identical* to the proxy run (same `rng_for` seeds).

Order parameter: the **parameter-free Gallai–Edmonds R-region**. The inessential
set `D` (forced-monomer sites = where the protected zero modes live) is connected
via the **projected / shared-neighbour** graph (two R-region sites couple when
they share a common neighbour — the real even-sublattice structure; on the
near-bipartite hat `D` is essentially independent so direct `G[D]` adjacency sees
only isolated monomers). A region **spans** when one projected-connected
component meets both opposite boundary bands. **No `d0`, no `θ`, no
eigendecomposition, no gauge choice.**

Result — `P_span(p, L)` crosses ½ at a threshold that **converges to a finite
value** as L grows, and the curves **sharpen** with L (classic finite-p_c
percolation, opposite to the proxy whose crossing drifted to 0):

| L | 27 | 35 | 42 | 49 | 55 | 62 | 68 | 75 |
|---|----|----|----|----|----|----|----|----|
| p_c(L) | 0.062 | 0.068 | 0.066 | 0.066 | 0.066 | 0.062 | 0.059 | 0.048 |

- **Linear fit** p_c = 0.0546 + 0.349/L → **L→∞ intercept = 0.0546 ± 0.0066**
  (a *finite* threshold, ~8σ above 0).
- A pure power-law fit p_c ∼ L^(−1/ν) gives ν ≈ 5.6 (i.e. p_c ∝ L^(−0.18), an
  extremely slow decay) — so a strict asymptotic →0 cannot be excluded from
  these sizes, but the data **favour a finite p_c ≈ 0.05–0.06**.

**Interpretation.** The dramatic finding #4 ("p_c → 0, qualitatively unlike every
periodic lattice in the Damle program") was a **proximity-proxy artifact**. Under
the rigorous matching-theoretic order parameter the hat's R-region percolates at
a **finite** vacancy density, like the periodic lattices. The qualitative
headline contrast is **removed**.

**What does survive (still real, parity-/proxy-free):**
- The hat has an **extensive clean-limit null space** (51 zero modes at L3;
  in-window def ≈ 64) → its R-region **spans at p = 0** and is *destroyed* at the
  finite p_c ≈ 0.055. Periodic lattices have **no** clean R-region (def = 0) and
  must *create* one with dilution (onset). So the hat and periodic lattices still
  differ in *direction* (de-percolation from an extensive clean null space vs
  onset), but both have a **finite** p_c — a much subtler statement than #4.
- Stage-A structural findings #1 (extensive negative non-bipartite gap) and #3
  (small-p blossom peak) are unaffected.
- A methodological result worth stating: a geometric proximity proxy for
  zero-mode-support percolation can **fake a vanishing threshold**; the
  matching-theoretic R-region is the trustworthy probe.

**Caveat / open:** the two largest windows show a downturn (p_c 0.066→0.048 for
L=62→75). Larger L (L4 via GPU/cluster) would settle finite-p_c vs very-slow-→0.
Until then, the honest statement is **finite p_c ≈ 0.055 on accessible sizes**.

**Periodic control** (`periodic_control.py`, triangular, `periodic_control.png`):
confirms the code finds **no** R-region at the clean point of a perfectly-matched
lattice (def=0 → no spanning), and that the binary D-spanning probe is parity-
and lattice-connectivity-dominated there — so it does not isolate the
Bhola–Damle intermediate p_c at small sizes, but it does validate the clean-limit
behaviour and the regime contrast (hat: extensive clean R-region; periodic: none).

---

## (SUPERSEDED) Proxy headline (finding #4): spanning threshold vanishes as L → ∞

> Retained for the record. The d0-proximity proxy below indicated p_c → 0; the
> rigorous cross-check above shows this was an artifact and the true (matching-
> theoretic) threshold is finite.

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

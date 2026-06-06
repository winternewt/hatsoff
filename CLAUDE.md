# Hatsoff — Hat Tiling Zero-Mode Analysis

Weekend project: compute zero-mode counting and multifractal analysis on the hat monotile family.

## Current state (hot-load anchor — read first after /clear)

The project grew from zero-mode counting into **zero-mode behavior under
disorder and site dilution**, analyzed via **maximum-matching / Gallai–Edmonds**
structure theory. Full handoff is in `README.md`; per-topic detail in `docs/`.

**Done & trusted:**
- *Count gate* (`docs/NULLITY.md`): π-flux/anti-hat counts **1/3/22/147 exact**;
  zero-flux **0/1/8/51** match except an isolated H-L1 boundary effect. Rank/
  matching code trusted.
- *Disorder* (`docs/DISORDER.md`, `src/hatsoff/disorder.py`): zero modes are
  **robust to hopping disorder** (structural/matching protection), **fragile to
  on-site (chiral-breaking)** disorder and to **bond/site removal**.
- *Dilution + Gallai–Edmonds* (`docs/PERCOLATION.md`, final write-up
  `docs/CAMPAIGN_REPORT.md`; `src/hatsoff/{dilution,matching,support}.py`):
  nullity ≈ deficiency; non-bipartite **gap (nullity−def) small at L2, extensive
  & growing at L3** (peak ≈ −1.7 at p≈0.10); trapped-weight fraction
  **intensive 0→0.44**; largest factor-critical component grows with size
  (16→48, peaks p≈0.02). **L3 campaign COMPLETE (2026-06-06, 5390 records).**
  Finding #4 now **demonstrated**: support spanning threshold `p_c(L)`
  extrapolates to an `L→∞` intercept consistent with **0** (d0=1.2: +0.004±0.015;
  d0=1.4: −0.005±0.015) — still the **proximity proxy** (`pc_collapse.py`,
  `docs/figures/pc_collapse.png`).
- *Novelty* (`docs/NOVELTY.md`, refs in `docs/REFLIST.md`): **GREEN** (web
  deep-research scan, 2026-06-05, archived as `docs/compass_artifact_*.md`).
  Both gate questions cleared: **Q1** — p_c→0 is **not** Gade–Wegner folklore
  (it's a Gallai–Edmonds *combinatorial-support* statement, distinct from
  Anderson-localization scaling); **Q2** — the aperiodic-monotile + matching +
  dilution niche is **open**. Framework still the **Damle group's** (bipartite
  PRX 2022 = arXiv:2007.04974; non-bipartite periodic arXiv:2311.05634; kagome
  arXiv:2512.23639 — all periodic, all finite p_c). New competitors to
  cite-and-distinguish: **Roche Carrasco et al. PRL 135,236603 (2025) /
  arXiv:2505.13304** (Anderson on a Chern hat model) and **Daníelsson–Sigurðsson
  arXiv:2605.29023** (continuum-polariton hat multifractality). Headline =
  finding **#4 (p_c→0)**.

**Pending decision (do NOT scale blindly):**
- Novelty gate PASSED (deep research done — do **not** re-run the web scan or
  the in-harness deep-research workflow; the latter failed/over-spent).
- Campaign DONE and the finite-size collapse is in hand (intercept ≈ 0). The
  remaining condition for #4 is **the non-proxy order parameter**: replace the
  d0-proximity spanning with a rigorous per-mode/R-region spanning order
  parameter (and add more sizes for a real ν) **before** bumping R / going to
  cluster. This is now the single highest-leverage next step.

**Bibliography upkeep:** `docs/REFLIST.md` is the curated, annotated reference
list (per-ref "how to use when writing" hints + ✓/⚠id/⚠pub verification flags).
**Keep it fresh** — whenever a new relevant paper surfaces or the narrative
sharpens, add/update the entry there (and reconcile the short list in README).

**Long campaign (`experiments/`):** `l3_campaign.py` (single-node, resumable,
checkpoints to `l3_campaign.jsonl`; **COMPLETE 2026-06-06**, Stage A R=60,
Stage B ~120 seeds/point). `l3_campaign_cluster.py` + `submit_l3.sbatch` =
SLURM/multi-node + optional GPU `eigh` (for the *next, larger* run).
`aggregate_campaign.py` (idempotent, globs all shards) →
`l3_campaign_summary.json` + `docs/figures/campaign_stage_{a,b}.png`;
`pc_collapse.py` → the finding-#4 `pc_collapse.png` + p_c(L) fit. Conclusive
write-up: `docs/CAMPAIGN_REPORT.md`. Resume/extend = re-launch (skip-done keys).
Check `experiments/l3_campaign.heartbeat` (currently `done`).

## Key physics facts (from literature)

- The hat vertex graph is **non-bipartite** (Franca, Schirmann, Flicker, Grushin, PRL 2024, arXiv:2307.11054)
- Lieb's theorem doesn't directly apply, but macroscopic zero modes still exist ("fragile" — depend on equal hoppings)
- Expected zero modes: 8 (level 2), 51 (level 3) per Franca et al.
- Average coordination number: ~2.31
- Zero modes form Sutherland loops (alternating 0, +1, 0, -1 patterns)
- At pi-flux: zero-mode count = number of anti-hats (22 at L2, 147 at L3)

## Tile counts per inflation level (from single H metatile)

| Level | Total hats | Est. vertices |
|-------|------------|---------------|
| 0     | 4          | ~20           |
| 1     | 25         | ~140          |
| 2     | 169        | ~950          |
| 3     | 1,156      | ~6,500        |
| 4     | ~7,921     | ~44,000       |

Note: counts are perfect squares of 2, 5, 13, 34, 89... (recurrence a(n) = 3a(n-1) - a(n-2)). Verified against Kaplan's reference JS.

Levels 3-4 are the sweet spot. Level 5 can run overnight.

## Reference implementations

- **Kaplan's hatviz**: `github.com/isohedral/hatviz` (JS, BSD-3-Clause) — the authoritative implementation
  - `geometry.js`: affine transforms as 6-element arrays `[a,b,tx,c,d,ty]`
  - `hat.js`: metatile definitions, 28 substitution rules, recursive inflation
- **Bharadwaj percolation**: `github.com/aaryashBharadwaj/Aperiodic-Monotile-Percolation` — Python port with KDTree vertex merging; local vendored copy and reuse guide: `Aperiodic-Monotile-Percolation/README.md`

## Hat polygon

13 vertices in hex coords: `hexPt(x,y) = (x + 0.5*y, (sqrt(3)/2)*y)`
```
(0,0), (-1,-1), (0,-2), (2,-2), (2,-1), (4,-2), (5,-1), (4,0), (3,0), (2,2), (0,3), (0,2), (-1,2)
```

## Substitution system

4 metatiles (H, T, P, F) with 28 placement rules. `constructPatch()` builds a patch; `constructMetatiles()` extracts new metatiles for the next level.

## Numerical pitfalls

- `eigsh(sigma=0)` fails on singular matrices — use `sigma=1e-8` instead
- **`eigsh` shift-invert SILENTLY UNDER-COUNTS a deeply degenerate null space**
  (hundreds of exact zeros under dilution): at L3 p=0.3 it gave nullity 547 vs
  true 790. Use **dense `eigh`** for N≤9000 (what `support.kernel_support` does).
- `np.linalg.eigh` (`syevd`) occasionally raises "did not converge" — fall back
  to `scipy.linalg.eigh(driver="evr")` (done in `support._cpu_dense_eigh`).
- Support-spanning is sensitive to the proximity distance `d0` (zero modes live
  on even-distance sites) — record several `d0` + window finite-size family;
  never read a single-`d0` p_c as physical.
- Vertex merging tolerance ~1e-5 is fine for hex coords with O(1) edge lengths
- Boundary vertices have lower coordination — compare across system sizes
- Zero-mode eigenvectors within degenerate subspace are arbitrary rotations —
  only gauge-invariant stats (mean IPR, `diag(P)`) are meaningful

## Dependencies

scipy, numpy, matplotlib, networkx

## Coding standards (from user's other projects)

- Type hints mandatory on all functions
- Pathlib for file paths
- Absolute imports only (no relative imports)
- All imports at module top level (no inline imports)
- Avoid try-catch unless the error is truly unavoidable
- No placeholders in code
- `uv sync` / `uv add` only, never `uv pip install`
- Tests: derived ground truth, meaningful assertions, parametrize over duplication

## Project structure

```
src/hatsoff/
  graph.py        # build_tb_graph: Franca-style tight-binding graph from polygons
  spectral.py     # bipartiteness (BFS), count_zero_modes (eigsh), Lieb bound
  disorder.py     # hopping & on-site disorder; zero-mode splitting stats
  dilution.py     # dilute_sites (induced subgraph), dilute_bonds
  matching.py     # matching_number, deficiency, gallai_edmonds (fast blossom + slow ref), nullspace_support
  support.py      # kernel_support (nullity+diag(P)), support_spanning; pluggable dense-eigh backend (set_dense_eigh for GPU)
  multifractal.py # participation ratios, D2 scaling (Phase 2 scaffolding, not yet pursued)
experiments/      # dilution_sweep.py, l3_campaign.py, l3_campaign_cluster.py, aggregate_campaign.py, pc_collapse.py, submit_l3.sbatch
docs/             # NULLITY, DISORDER, PERCOLATION, CAMPAIGN_REPORT, NOVELTY, REFLIST, PLAN, deepresearch_prompt, THEHAT
                  #   CAMPAIGN_REPORT = conclusive L3-run report (Stage A + finding #4)
                  #   REFLIST = curated annotated bibliography (keep fresh)
                  #   compass_artifact_*.md = archived web deep-research scan (2026-06-05)
```

Reusable geometry, tiling generation, and generic vertex/dual graph + percolation
utilities live in `hat_amp`; import from `hat_amp.{tiling,graph,percolation}`.
(`viz.py` was never created — viz is via experiment figures.)

## Visualization approach

pyvista + console output for now (research-focused). JS webapp is viable later (Kaplan's hatviz is JS-based). Keep viz separate from computation.

## Acknowledgments

Tiling generation ported from Craig Kaplan's `hatviz` (BSD-3-Clause). Must credit in README.

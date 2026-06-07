# Hatsoff — Hat Tiling Zero-Mode Analysis

Weekend project, now a **comparative matching/percolation study of monotile zero
modes** (hat vs Spectre vs periodic control). Multifractal/IPR is scaffolded but
not pursued. Current one-line thesis: *local order, not aperiodicity, governs the
protected zero modes* (see "Current working thesis" below).

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
  ⚠ **Finding #4 (p_c→0) does NOT survive the rigorous cross-check.** The
  proximity proxy (`pc_collapse.py`) gave `p_c(L)→0`, but the **parameter-free
  Gallai–Edmonds R-region** order parameter (`rregion_campaign.py` 8 sizes ×300
  seeds, `rregion_analysis.py`, `docs/figures/rregion_collapse.png`) gives a
  **FINITE p_c ≈ 0.055** (0.0546±0.0066) with crossings that *sharpen* at fixed
  p — i.e. the hat percolates at a finite vacancy density **like** the periodic
  Damle lattices. The p_c→0 was a **proxy artifact**. Full write-up + caveats
  (large-L downturn; need L4 to fully settle finite-vs-slow-→0):
  `docs/CAMPAIGN_REPORT.md` §"Rigorous cross-check". Still real: hat's
  **extensive clean-limit R-region** (spans at p=0, unlike periodic def=0;
  destroyed at finite p_c) + findings #1/#3.
- *Novelty* (`docs/NOVELTY.md`, refs in `docs/REFLIST.md`): **DOWNGRADED from
  GREEN (2026-06-06)** — the #4 headline was retracted by its own cross-check
  (above). The **literature gate still holds**: a 2026-06-05 web scan (archived
  `docs/compass_artifact_*3b599644*.md`) confirmed **Q1** p_c→0 is not Gade–Wegner
  folklore and **Q2** the aperiodic-monotile + matching + dilution niche is
  **open/unstudied** — but the *result* that was going to fill it (p_c→0) is gone.
  Framework is the **Damle group's** (bipartite PRX 2022 = arXiv:2007.04974;
  non-bipartite periodic arXiv:2311.05634; kagome arXiv:2512.23639 — all periodic,
  finite p_c — and the hat now joins them at finite p_c). Cite-and-distinguish:
  **Roche Carrasco et al. PRL 135,236603 (2025)/arXiv:2505.13304** (Anderson on a
  Chern hat model), **Daníelsson–Sigurðsson arXiv:2605.29023** (continuum-polariton
  hat multifractality).
  **Current working thesis (reframe):** *local order, not aperiodicity, governs
  protected zero modes on monotiles* — the achiral, mta-hexagonal-derived **hat**
  has an extensive clean null space + finite-p_c de-percolation; the strictly-
  chiral **Spectre** (same aperiodicity, no hexagonal order) has **no zero-flux
  clean modes** and onset-type creation under dilution; periodic triangular is the
  control. Honest negative #4 + this hat/Spectre/periodic contrast = the paper.

**Pending decision (headline overturned — reassess framing):**
- The non-proxy cross-check is DONE and it **killed the p_c→0 headline** (finite
  p_c≈0.055; see above). The literature niche is still open and findings #1/#3
  stand, but the flagship "qualitatively unlike periodic lattices" claim is gone.
  **`docs/NOVELTY.md` needs a verdict downgrade from GREEN.** Open strategic
  forks (PI call): (a) **larger L (L4, GPU/cluster)** to settle whether the
  large-L downturn means finite p_c vs very-slow →0 (ν≈5.6); (b) **reframe** the
  paper around the *finite p_c on an aperiodic monotile* + extensive clean-limit
  R-region + #1/#3 + the methodological "proxy fakes p_c→0" caution; (c) pivot to
  the **Spectre** comparison (`docs/SPECTRE_TODO.md`) or the IPR/multifractal
  angle. Do **not** re-run the web deep-research or scale blindly.

**Bibliography upkeep:** `docs/REFLIST.md` is the curated, annotated reference
list (per-ref "how to use when writing" hints + ✓/⚠id/⚠pub verification flags).
**Keep it fresh** — whenever a new relevant paper surfaces or the narrative
sharpens, add/update the entry there (and reconcile the short list in README).

**Sideways / future — Spectre monotile (`docs/SPECTRE_TODO.md`):** `hat_amp` 0.2
now has `hat_amp.spectre` (tiling + 'S'/'M' Mystic labels + gold toggle); our
pipeline runs on it unchanged. **Coarse result (2026-06-06):** the strictly-
chiral Spectre has **nullity 0 (zero-flux) at the clean point** for N up to 26825
— *opposite* of the hat's extensive clean null space (8/51). Dilution *creates*
zero modes (onset, like the periodic lattices / triangular control), not
de-percolation. ⇒ the hat's protected zero modes come from its achiral,
mta-hexagonal-derived local order, not from aperiodicity.
**π-flux now in-pipeline + reconciled (2026-06-07, `src/hatsoff/flux.py`):** the
Peierls complex Hamiltonian (`B=π/A_tile`, uniform π per equal-area tile face) is
ported; the count gate (`tests/test_flux.py`) reproduces the hat π-flux
**1/3/22/147** with `build_tb_graph`, which **proves our edge convention =
Schirmann's** and settles the long-edge caveat. The Schirmann-consistent natural
Spectre (gold stripped, long edge through its real shared midpoint =
`build_tb_graph`, *not* the redundant-chord "direct" nor the with-gold
bipartization) has zero-flux nullity 0 but **clean π-flux nullity = N_Mystic/2 =
one protected mode per Mystic compound** (L1/2/3 = 1/8/63; the strict-chiral
analogue of "one per anti-hat") — first quantitative check of Schirmann's
data-free anti-spectre conjecture. `experiments/spectre_reconcile.py` tabulates
direct-vs-split-vs-gold. **Dilution campaign DONE (2026-06-07,
`spectre_flux_campaign.py` → `spectre_flux_campaign.jsonl`, 33047 units, 364 seeds,
L3 full + 6 windows N≈793→3563, p∈[0,0.40]; `spectre_flux_analysis.py` →
`docs/figures/spectre_flux.png`):** clean-point Mystic-support fraction **rises
with size → 1.000 on the full graph** (enrichment 2.57 = 1/0.389) — i.e. **all
clean π-flux zero modes live entirely on Mystics** in the TD limit (strongest form
of the conjecture; matches Singh–Flicker). Under dilution nullity/N grows but the
Mystic **enrichment decays monotonically to ~1.0** by p≈0.3 — disorder-created
modes are delocalized, *not* Mystic-anchored: the clean (Mystic-nucleated) and
diluted sectors are physically distinct. Use **dense complex `eigh` with the RRR
value-subset** for π-flux nullity (not `eigsh`; see perf note in Numerical
pitfalls). Scope = follow-up to the (now negative-result) hat paper.

**Campaigns (`experiments/`) — all COMPLETE, nothing running:**
- `l3_campaign.py` — the **proxy** campaign (dense-`eigh`, BLAS-threaded).
  Resumable, `l3_campaign.jsonl`, **done 2026-06-06** (Stage A R=60, Stage B
  ~120 seeds). → `aggregate_campaign.py` (`l3_campaign_summary.json`,
  `campaign_stage_{a,b}.png`); `pc_collapse.py` → `pc_collapse.png` (the proxy
  p_c→0, now known to be an artifact).
- `rregion_campaign.py` — the **rigorous** R-region campaign (pure-Python,
  **`multiprocessing` across cores**, `HATSOFF_NPROC`). `l3_rregion.jsonl`,
  **done 2026-06-06**, 8 sizes × **300 seeds** (21608 units). →
  `rregion_analysis.py` → `rregion_collapse.png` (the decisive **finite p_c**).
- `periodic_control.py` — triangular-lattice control → `periodic_control.png`
  (parity/connectivity caveat; clean-limit regime contrast).
- `l3_campaign_cluster.py` + `submit_l3.sbatch` = SLURM/multi-node + GPU `eigh`,
  for the *optional next* larger (L4) run only.
- Conclusive write-up: `docs/CAMPAIGN_REPORT.md` (§"Rigorous cross-check" is the
  load-bearing one). Resume/extend any campaign = re-launch (skip-done keys).
  Heartbeats `experiments/*.heartbeat` (both currently `done`).

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
- **Methodological (cost us the headline):** a geometric *proximity* proxy for
  zero-mode-support percolation (`support_spanning`, tunable `d0`) **faked
  `p_c→0`**; the parameter-free Gallai–Edmonds R-region (`rregion_spanning`) gave
  the true **finite** p_c≈0.055. Trust the matching-theoretic probe, not the proxy.
- **R-region connectivity gotcha:** on the (near-bipartite) hat the GE `D` set is
  ~independent, so *direct* `G[D]` adjacency sees only isolated monomers and never
  spans. `rregion_spanning` instead connects D-sites that **share a neighbour**
  (projected/even-sublattice graph) — that is the physical connectivity.
- **Parallelism:** dense `eigh` is BLAS-multithreaded (proxy campaign saturates
  cores for free); the GE matching is **pure-Python single-threaded**, so the
  rigorous campaign parallelizes across realizations with `multiprocessing`
  (`HATSOFF_NPROC`), not BLAS.
- **Dense `eigh` real cost — budget campaigns from THESE numbers, not "seconds"**
  (this box: 16 cores, `scipy-openblas` 0.3.31; measured 2026-06-07):
  - Full **complex** Hermitian `eigh`, **1 BLAS thread**: N=1200 → 3.4s (zheevd) /
    4.9s (evr); N=2400 → 31s / 9.4s; N=3563 → **117s / 56s**. 16-thread `zheevd`:
    N=3563 → ~104s, N=7047 → **~555s**. Cost is ~O(N³); real `syevd` ≈ ⅓–½ of
    complex at the same N.
  - **Two big constant-factor wins** (both used in `flux.py` / the Spectre campaign):
    (1) the **RRR driver beats divide-and-conquer** for large complex Hermitian
    here — `scipy.linalg.eigh(driver="evr")` is ~2× faster than `np.linalg.eigh`
    (zheevd); (2) when only the kernel is needed, the **value-subset**
    `subset_by_value=(-1e-6,1e-6)` is a further ~3–5× (it still pays the O(N³)
    tridiagonalization but skips most eigenvector back-transforms), and is exact
    on degeneracy (verified to 305-fold) where `eigsh` under-counts.
  - **Throughput rule:** for many small-N solves, run `HATSOFF_NPROC`
    single-thread (`OPENBLAS_NUM_THREADS=1`) processes — the Spectre π-flux
    campaign did **33k units (L3, N≤3563, 364 seeds) in its 10h budget** this way.
    L4 (N≈27k) dense complex is infeasible (~hours/solve, ~TB RAM) → GPU/sparse only.
- Spectre natural (non-bipartite) graph: nullity at clean is **construction-
  dependent** (long-edge split vs direct; gold vs no-gold). **RECONCILED 2026-06-07:**
  the count gate (hat π-flux 1/3/22/147 reproduced by `build_tb_graph`) proves the
  Schirmann-consistent graph = `build_tb_graph` on gold-stripped 13-gons (long edge
  = two unit bonds through its *real* shared midpoint; **not** the redundant-chord
  "direct" graph, **not** the with-gold bipartization). Use this for all Spectre TB.
  Zero-flux nullity 0; π-flux nullity = N_Mystic/2. See `docs/SPECTRE_TODO.md`.
- **π-flux nullity must use dense complex `eigh`** (real-valued matching/GE does
  not apply); only the kernel is needed, so prefer
  `scipy.linalg.eigh(driver="evr", subset_by_value=(-1e-6, 1e-6))` — ~5× cheaper
  than a full spectrum and exact on the degenerate null space (verified to 305-fold),
  where `eigsh` would silently under-count.

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
  support.py      # kernel_support (nullity+diag(P)); support_spanning (d0-PROXY, retracted); rregion_spanning (rigorous, parameter-free — THE trusted probe); set_dense_eigh for GPU
  multifractal.py # participation ratios, D2 scaling (Phase 2 scaffolding, not yet pursued)
  flux.py         # π-flux Peierls complex Hamiltonian (build_flux_hamiltonian), flux_kernel (dense complex eigh / RRR subset), tile_area + signed_tile_area, label_vertex_mask (Mystic sites)
experiments/      # proxy: l3_campaign.py, aggregate_campaign.py, pc_collapse.py
                  # rigorous: rregion_campaign.py (parallel), rregion_analysis.py
                  # control: periodic_control.py ; cluster: l3_campaign_cluster.py, submit_l3.sbatch
                  # spectre π-flux: spectre_reconcile.py (long-edge convention), spectre_flux_campaign.py (dilution, parallel), spectre_flux_analysis.py
                  # also dilution_sweep.py (L2); outputs *.jsonl / *.heartbeat / *.log
docs/             # NULLITY, DISORDER, PERCOLATION, CAMPAIGN_REPORT, NOVELTY, REFLIST, SPECTRE_TODO, PLAN, deepresearch_prompt, THEHAT
                  #   CAMPAIGN_REPORT = conclusive L3 report; §"Rigorous cross-check" = the live result
                  #   NOVELTY = DOWNGRADED from GREEN (#4 retracted); REFLIST = annotated bib (keep fresh)
                  #   SPECTRE_TODO = Spectre program + coarse results (the reframe direction)
                  #   compass_artifact_*9cb25304*.md = Spectre scan; *95d25a67*.md = novelty scan (2026-06-05)
```

Reusable geometry, tiling generation, and generic vertex/dual graph + percolation
utilities live in `hat_amp`; import from `hat_amp.{tiling,graph,percolation}`.
(`viz.py` was never created — viz is via experiment figures.)

## Visualization approach

pyvista + console output for now (research-focused). JS webapp is viable later (Kaplan's hatviz is JS-based). Keep viz separate from computation.

## Acknowledgments

Tiling generation ported from Craig Kaplan's `hatviz` (BSD-3-Clause). Must credit in README.

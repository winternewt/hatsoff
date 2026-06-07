# Spectre monotile — future program (sideways extension)

Side-quest scan (web deep-research, archived
`docs/compass_artifact_wf-9cb25304-…_text_markdown.md`) on porting the hat
program to the **Spectre** strictly-chiral monotile. Verdict: a **wide-open,
high-payoff frontier** that our pipeline can reach with one new ingredient.

## Coarse computation results (2026-06-06) — pipeline runs; striking contrast

`hat_amp` 0.2 now ships `hat_amp.spectre` (`generate_spectre_tiling`,
`generate_spectre_tiling_labeled` → 'S'/'M' Mystic labels, `add/strip_gold_vertex`
for the Singh–Flicker bipartite↔natural toggle). Our pipeline consumes it
**unchanged** — `build_tb_graph` handles the polygons (with-gold = 14 unit edges;
strip-gold = 13 verts with one length-2 edge kept direct), `dilute_sites` /
`gallai_edmonds` / `rregion_spanning` all run. Coarse results (**zero flux**):

| | clean nullity (L2/L3/L4) | ⟨z⟩ | bipartite | under dilution |
|---|---|---|---|---|
| **Hat** | **8 / 51 / extensive** | 2.31 | no | de-percolation (finite p_c≈0.055) |
| **Spectre (natural, no gold)** | **0 / 0 / 0** (def=1 parity only) | 2.31 | no | nullity *created*: 0→32→76→152→420 at p=0/.02/.05/.10/.30 (L3, N=3563) |
| **Spectre (with gold)** | 0 (balanced bipartite) | 2.27 | yes | — |

**The decisive finding:** the strictly-chiral Spectre has **no zero-flux zero
modes at the clean point** (nullity 0 at N up to 26,825), the *opposite* of the
hat's extensive clean null space. Dilution **creates** zero modes on the Spectre
(onset), grouping it with the periodic lattices / triangular control — not with
the hat. So the hat's extensive protected zero-mode sector is a consequence of
its **achiral, mta-hexagonal-derived local order** (it sits on a deletion of the
hexagonal lattice → graphene-like Dirac features), which the Spectre lacks
entirely. This *sharpens* the project's question: **what drives protected zero
modes on aperiodic monotiles is local order, not aperiodicity per se.**

**Caveats:** (i) nullity=0 holds for both gold/no-gold constructions here, but the
natural-graph long-edge convention (split vs direct) must be reconciled with
Schirmann et al.'s exact Spectre TB model before it is load-bearing. **[RESOLVED
2026-06-07 — see "π-flux reconciliation" below.]** (ii) The *rich* Spectre
zero-mode physics Schirmann/Singh–Flicker describe is at **π-flux** (Mystic-
localized modes), which our zero-flux pipeline does not yet probe. **[NOW PROBED
2026-06-07 — π-flux Hamiltonian ported to `src/hatsoff/flux.py`; see below.]**

## Zero-flux R-region: hat vs Spectre under dilution (comparative, 2026-06-07)

`experiments/spectre_rregion_campaign.py` (16206 units, 6 windows N≈623→2756,
p∈[0,0.30], 300 seeds; the hat-`rregion_campaign` harness on the Schirmann-
consistent Spectre) → `spectre_rregion.jsonl`;
`spectre_vs_hat_rregion.py` → `docs/figures/hat_vs_spectre_rregion.png`. The
parameter-free GE R-region **spanning probability vs p** is the clean
discriminator (window L≈0.55):

| p | hat P(span) | Spectre P(span) |
|---|---|---|
| 0.00 | **1.00** | **0.00** |
| 0.02 | 0.99 | **0.61** |
| 0.05 | 0.76 | 0.47 |
| 0.10 | 0.09 | 0.09 |
| ≥0.15 | 0 | 0 |

**The hat de-percolates monotonically** from a spanning *extensive clean*
R-region (P=1 at p=0 → 0 by p≈0.12; finite p_c≈0.055). **The Spectre is
onset-type / non-monotonic:** no clean R-region (P=0 at p=0), dilution *creates*
a spanning one (peak at p≈0.02), which then de-percolates. Deficiency density
(≈nullity/N) grows similarly for both (~0.017→0.17), so the *creation* of modes
is shared — but only the hat has the protected clean sector. (Caveat: clean-point
*windowed* `largest_comp_frac`/deficiency are boundary-dominated for both and do
**not** discriminate — use P(span) vs p, not the p=0 window number.) This is the
paper's R3/R5 contrast (periodic triangular = the third leg, `periodic_control`).

## π-flux reconciliation + Mystic sector (2026-06-07)

`src/hatsoff/flux.py` ports the Peierls complex-Hermitian π-flux Hamiltonian
(`H_ij = -exp(-0.5j·B·(x_i−x_j)(y_i+y_j))`, `B = π/A_tile`; uniform π per equal-
area tile face) into the pipeline.  **Count gate (`tests/test_flux.py`):** on the
hat, `build_tb_graph`'s graph reproduces the π-flux counts **1/3/22/147** (= the
anti-hat counts of Franca/Schirmann), exactly as it already reproduces the zero-
flux 0/1/8/51.  This is the parameter-free proof that **our edge convention
equals Schirmann's**, settling caveat (i).  Matching/Gallai–Edmonds does *not*
apply at π flux (complex H); nullity is by dense complex `eigh` — and only the
kernel eigenpairs are needed, so the RRR value-subset
(`scipy.linalg.eigh(driver='evr', subset_by_value=(-1e-6,1e-6))`) gives the count
~5× faster than a full spectrum and, unlike `eigsh`, resolves the deeply
degenerate null space exactly (verified to 305-fold degeneracy).

**Clean-point reconciliation (`experiments/spectre_reconcile.py`,
`spectre_reconcile.json`).**  Three constructions × {0, π} flux × L1–L3:

| level | construction | N | nullity(0) | nullity(π) | N_Mystic | π/N_Mystic |
|---|---|---|---|---|---|---|
| 1 | natural-direct | 73   | 0 | 0   | 2   | 0.00 |
| 1 | natural-split  | 73   | 0 | 1   | 2   | 0.50 |
| 1 | with-gold      | 78   | 0 | 4   | 2   | 2.00 |
| 2 | natural-direct | 491  | 0 | 0   | 16  | 0.00 |
| 2 | natural-split  | 491  | 0 | 8   | 16  | 0.50 |
| 2 | with-gold      | 518  | 0 | 18  | 16  | 1.12 |
| 3 | natural-direct | 3563 | 0 | 0   | 126 | 0.00 |
| 3 | natural-split  | 3563 | 0 | **63**  | 126 | **0.50** |
| 3 | with-gold      | 3734 | 0 | 126 | 126 | 1.00 |

- **natural-split** (= `build_tb_graph` on gold-stripped 13-gons; the long edge
  passes through a *real* shared neighbour vertex, so it is two unit bonds, never
  a chord — exactly how the hat type-c edge is treated) is the **Schirmann-
  consistent** construction, and is **locked** for all π-flux work.
- **natural-direct** wrongly adds the length-2 edge as a redundant *chord* on top
  of the two unit bonds (E=4427 vs 4121 at L3) → kills the π-flux modes (π=0). Not
  the natural graph.
- **with-gold** is Singh–Flicker's bipartization (an extra degree-2 vertex per
  tile), a *different* model — doubles the count.

**Headline:** zero-flux nullity = 0 at every level (robustly confirms the coarse
result), while the natural Spectre's **clean π-flux nullity = N_Mystic/2 = the
number of Mystic *compounds*** — i.e. **exactly one protected π-flux zero mode
per Mystic**, the strict-chiral analogue of "one per anti-hat" on the hat.  This
is the first *quantitative* check of Schirmann et al.'s data-free assertion that
anti-spectres exhaust the π-flux zero modes.

(NB measured Mystic-tile fraction is a level-independent **22.5%** — 'M' counts
both Gamma halves, so 11.25% Mystic compounds; the deep-research artifact's "~1
per 26.6 vertices" is not what the generator yields — flag for the write-up.)

**Dilution campaign DONE (`experiments/spectre_flux_campaign.py` →
`spectre_flux_campaign.jsonl`, 2026-06-07, full 10h budget, 15-way
`multiprocessing` BLAS-pinned).** **33047 units, 364 seeds, 0 errors**; L3
natural-split full graph + 6 cropped windows (N≈793→3563), p∈[0,0.40] (14 points).
Per unit: π-flux nullity, Mystic-support fraction (gauge-invariant `diag(P)` on
'M' sites — the Mystic-nucleation probe), support-field PR.  Analysis:
`spectre_flux_analysis.py` → `docs/figures/spectre_flux.png`;
`spectre_flux_consolidate.py` → `docs/figures/spectre_flux_consolidate.png`.

**Findings (consolidated):**
- *Clean point.* Full-graph π-flux kernel is **100% Mystic-localized**
  (mystic_support_frac = 1.000; cropped windows leak at the boundary and
  extrapolate to ≈1.07 in 1/L). Nullity density → **0.0177 = (Mystic
  compounds)/N** = (N_Mystic/2)/N (63/3563), i.e. exactly one protected π-flux
  zero mode per Mystic, *all* of its weight on Mystic sites. Clean enrichment
  2.57 = 1/(Mystic-vertex fraction 0.389).
- *Dilution.* Nullity density climbs (full 0.018→0.234 over p∈[0,0.40]); the
  Mystic **enrichment decays monotonically to ~1.0** (uniform) — disorder-created
  modes are **delocalized, not Mystic-anchored**. The enrichment→1.1 crossover is
  at a **size-independent p\*≈0.15** (σ=0.024 across windows) ⇒ a **smooth
  crossover, not a sharp de-percolation transition** in this observable. The clean
  (Mystic-nucleated) and diluted (delocalized) sectors are physically distinct.
- *Caveat / open.* A genuine *de-percolation* claim for the Mystic-localized
  sector needs a **π-flux support-spanning order parameter** (kernel `diag(P)`
  spanning a window) — `support_spanning` machinery exists but this run did not
  record positions/boundary bands. A targeted smaller re-run recording them would
  settle transition-vs-crossover; current honest statement is **smooth crossover**.

## Why it's attractive

- **Strongest robustness argument for finding #4.** If the support-spanning
  `p_c(L) → 0` we see on the hat *also* holds on the Spectre, the result is
  **aperiodicity-general**, not a hat accident — a major strengthening (a second
  substrate is the single most convincing control a referee could ask for). If
  it *doesn't*, chirality is the knob and that is itself a new result.
- **Empty niche, even emptier than the hat's.** Per the scan, **no** paper does
  site-dilution / Gallai–Edmonds / Dulmage–Mendelsohn / zero-mode percolation /
  IPR / Anderson on the Spectre vertex graph. Only two papers do *any*
  quantitative spectral/many-body Spectre physics: Singh–Flicker (dimers) and
  one paragraph of Schirmann et al.
- **A sharp, testable conjecture.** The Spectre has no reflected tiles; the
  "anti-hat" role is played by the **Mystic** (a π/6-rotated minority tile,
  ~1 per 26.6 vertices). Singh–Flicker proved that on the bipartite Spectre
  (add a "gold" vertex per tile) *all* maximum-matching freedom sits on **Upper
  Mystics** (Z = 2^(N_Mystic+1)). **Conjecture (now testable with our code):**
  under site dilution the Gallai–Edmonds factor-critical / R-type regions
  **nucleate on Mystics and percolate via the substitution hierarchy** — a
  Mystic-anchored analogue of the hat's anti-hat sublattice-imbalance picture.

## Feasibility — pipeline transfers; only the tiling is new

Our analysis stack is **substrate-agnostic**: everything downstream of
`(verts, adj)` already works on any vertex graph —
`hatsoff.{dilution,matching,support}`, `crop_square`, `rregion_spanning`,
`support_spanning`, the `l3_campaign` / `rregion_campaign` harness, the
`pc_collapse` / `rregion_analysis` fits, the periodic-control machinery.

**The one blocker:** `hat_amp` ships only the Hat tiling (H/T/P/F substitution);
there is **no Spectre/Mystic generator**. Building it is the main new work:
the two-prototile Spectre + Mystic substitution (σ takes right→left handed, so
the local inflation is σ²; area inflation λ = 4+√15 ≈ 7.873; recursion
S_{n+1}=M_n+7 S_n, M_{n+1}=M_n+6 S_n). References with the rules: Smith–Myers–
Kaplan–Goodman-Strauss "A chiral aperiodic monotile" (arXiv:2305.17743) and
Tatham's 9-tile finite-state transducer refinement (arXiv:2512.16595). Then
build the vertex graph the same way `hatsoff.graph.build_tb_graph` does for the
hat (merge coincident polygon vertices; the Spectre 14-gon has 90°/120°/180°
vertex angles). Natural Spectre vertex graph is **non-bipartite** (like the
hat) — so Gallai–Edmonds is again the right tool and our code is ready.

## Staged plan (condensed from the scan's recommendations)

0. **Clean baseline.** Spectre/Mystic tiling generator + vertex graph; reproduce
   Singh–Flicker matching; sublattice imbalance |A|−|B| vs patch size for the
   bipartite (with-gold) and natural (non-bipartite) graphs. Fixes the zero-mode
   count and whether Mystics contribute systematically.
1. **Zero-mode density at 0 and π flux** vs N_Mystic (the missing companion to
   Schirmann et al.'s hat tables; they give *no* Spectre count). Does π-flux
   count track N_Mystic/N ≈ 1/26.6 (Mystic-anchoring) or exceed it (chirality
   generating extra modes)?
2. **Gallai–Edmonds under site dilution** — D/A/C and factor-critical-component
   scaling vs vacancy density; **test the Mystic-nucleation conjecture**; and the
   headline question: **does support spanning `p_c(L) → 0` as on the hat, or
   finite?** This is the direct reuse of `rregion_campaign` + `rregion_analysis`.
3. **IPR / multifractality** of Spectre eigenstates (reuse `multifractal.py`
   scaffold). Intuition: no minority "anti" population to concentrate localized
   states → states may be *more* uniformly critical than the hat's.
4. **Anderson disorder / TAI** (standalone — Spectre is *not* in the Roche
   Carrasco et al. Chevron–Hat–Turtle–Comet tunable family, arXiv:2505.13304).

## Key references (see also `docs/REFLIST.md`)

- **Singh & Flicker**, PRB 109, L220303 (2024); arXiv:2309.14447 ✓ — exact
  classical+quantum dimer solution on Spectre; Z = 2^(N_Mystic+1); matching
  freedom only on Upper Mystics. *The* structural anchor. (= REFLIST [F3].)
- **Smith, Myers, Kaplan, Goodman-Strauss**, *A chiral aperiodic monotile*,
  arXiv:2305.17743 (Combinatorial Theory, 2024) ✓ — defines Spectre/Tile(1,1),
  the Spectre+Mystic substitution. The generator spec.
- **Baake, Gähler, Mazáč, Sadun**, *On the long-range order of the Spectre
  tilings*, Discrete Comput. Geom. (2025); arXiv:2411.15503 ✓ — σ² inflation,
  λ=4+√15, pure-point spectrum, chirality-sector structure.
- **Tatham**, *Finite-state transducers for substitution tilings*,
  arXiv:2512.16595 — practical 9-tile refinement, useful for generation/enumeration.
- **Schirmann, Franca, Flicker, Grushin**, PRL 132, 086402 (2024);
  arXiv:2307.11054 ✓ — one paragraph + 4-row SM table on Spectre; asserts
  (no data) anti-spectres exhaust π-flux zero modes — treat as conjecture.

## Caveats / decision points

- **Do not start until the hat paper's load-bearing claims are locked** (the
  rigorous R-region cross-check + ν). Spectre is a *second-paper / extension*
  scope, not a prerequisite for finding #4.
- Bipartize-with-gold (Singh–Flicker) vs natural non-bipartite are *different*
  graphs; decide which is "the" Spectre TB model (the natural non-bipartite one
  matches the hat treatment and Schirmann et al.).
- Spectre has **no** Bloch/Dirac structure (vertices don't sit on a periodic
  hexagonal lattice, unlike the hat) — momentum-space methods won't transfer,
  but our real-space matching/percolation pipeline doesn't need them.

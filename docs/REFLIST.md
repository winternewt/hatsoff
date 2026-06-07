# REFLIST — curated bibliography + writing hints

Working reference list for the eventual hatsoff paper. Each entry: the citation,
**what it says**, and **how to use it when writing** (the framing / sentence it
supports). Keep this fresh — add a row whenever a new relevant ref surfaces, and
update "how to use" as the narrative sharpens. Verification status is flagged;
re-confirm anything tagged ⚠ before it goes into a submitted manuscript.

Last updated: 2026-06-05 (folded in the web deep-research scan
`compass_artifact_wf-95d25a67-…` + the user's cross-check of which IDs were
directly fetched vs synthesized).

**Verification legend:**
- ✓ = arXiv/DOI ID **directly fetched** during the deep-research run; ID solid.
- ⚠id = ID came through the report's *synthesis*, not a fetched page — verify
  volume/page/arXiv number before it enters a submitted bibliography.
- ⚠pub = ID solid but it is a recent **preprint**; confirm journal publication
  status before final submission.

IDs confirmed ✓ (directly fetched): 2307.11054, 2007.04974, 2311.05634,
2512.23639, 2604.21165, 2505.13304, 2605.29023, 1201.6288, cond-mat/0201580,
1304.5968, 1902.02799, 2309.14447.

---

## Tier 1 — load-bearing (cite in intro + positioning)

### [S1] The hat monotile
**D. Smith, J. S. Myers, C. S. Kaplan, C. Goodman-Strauss**, *An aperiodic
monotile*, arXiv:2303.10798 (2023); Combinatorial Theory 4(1) (2024).
- **What:** discovery of the single aperiodic tile ("the hat").
- **How to use:** first sentence of the intro — the substrate. Cite alongside
  Kaplan's `hatviz` for the tiling-generation lineage.

### [S2] Hat tight-binding zero modes — *the model we extend*
**J. Schirmann, S. Franca, F. Flicker, A. G. Grushin**, *Physical properties of
an aperiodic monotile with graphene-like features, chirality, and zero modes*,
PRL **132**, 086402 (2024); arXiv:2307.11054.
- **What:** vertex tight-binding model on the hat; non-bipartite (Lieb fails);
  clean-limit zero-mode counts 0/1/8/51; anti-hat count = π-flux count
  (1/3/22/147); modes "fragile" (depend on equal hoppings).
- **How to use:** "We reproduce the clean-limit counts of Ref. [S2] (our count
  gate, `docs/NULLITY.md`), then extend to dilution + matching structure, which
  [S2] does not treat." This is our baseline and our reproduction target.
- **π-flux count gate reproduced in-pipeline (2026-06-07, `tests/test_flux.py`,
  `src/hatsoff/flux.py`):** both the zero-flux 0/1/8/51 *and* the π-flux
  **1/3/22/147** (= anti-hat counts) now come out of *our* `build_tb_graph` graph
  — parameter-free proof our edge convention equals [S2]'s. Lets us quantify
  [S2]'s data-free Spectre claim: the natural Spectre's clean π-flux nullity =
  N_Mystic/2 (one mode per Mystic compound). See `docs/SPECTRE_TODO.md`.
- **Note:** Flicker also co-authors the Penrose-dimer PRX [F1] → he bridges the
  monotile and matching/dimer worlds. Competitive-overlap flag.

### [S3] Bipartite matching ↔ zero-mode percolation — *the framework, bipartite*
**R. Bhola, S. Biswas, M. M. Islam, K. Damle**, *Dulmage–Mendelsohn percolation:
geometry of maximally-packed dimer models and topologically-protected zero modes
on site-diluted bipartite lattices*, PRX **12**, 021058 (2022);
arXiv:2007.04974.
- **What:** site-diluted **bipartite** (square, honeycomb) lattices; maximum
  matching → R-regions of forced monomers control E=0 localization; a distinct
  **finite-p_c** percolation universality of zero-mode support.
- **How to use:** the framework we generalize. Key contrast sentence for our
  headline: "On bipartite lattices the support percolates at *finite* vacancy
  density [S3]; on the hat it collapses to the clean point."

### [S4] Non-bipartite periodic Gallai–Edmonds — *closest method precedent*
**R. Bhola, K. Damle**, *Chaotic percolation in the random geometry of
maximum-density dimer packings*, arXiv:2311.05634 (2023, rev. 2025).
- **What:** **non-bipartite** site-diluted periodic lattices (triangular,
  Shastry–Sutherland, 3D stacked-triangular, octahedral) via Gallai–Edmonds;
  R-type (factor-critical, blossom) vs P-type regions; **finite** critical
  densities; chaotic self-averaging violations in the percolated phase.
- **How to use:** direct precedent for findings #1/#3 (the GE machinery), and
  the finite-p_c contrast object for #4. "Periodic non-bipartite lattices also
  percolate at finite density [S4]; the aperiodic hat does not."
- **Status:** ✓ ID fetched; finite-threshold claim WebFetch-confirmed. ⚠pub
  (rev-2025 preprint — check for journal version).

### [S5] Site-diluted kagome — *Damle group still active, still periodic*
**R. Bhola, K. Damle**, *Random geometry of maximum-density dimer packings of
the site-diluted kagome lattice*, arXiv:2512.23639 (Dec 2025).
- **What:** GE on site-diluted kagome; every odd connected cluster → a single
  spanning R-region with exactly one monomer; proof extends to all **claw-free**
  graphs (kagome, star, pyrochlore, hyperkagome).
- **How to use:** cite as the most-current proof that "the Damle program has not
  moved to aperiodic substrates." The claw-free phenomenology is *orthogonal* to
  ours (their blossom trivially = whole odd cluster; our blossom peaks at p≈0.03
  — an aperiodic-specific feature). Confirms niche open as of Dec 2025.
- **Status:** ✓ HTML-fetch-confirmed real & attributed. ⚠pub (Dec-2025 preprint).

---

## Tier 2 — competitors to cite-and-distinguish (newly surfaced)

### [G1] Anderson disorder on a Chern hat-family model — *only Hat-TB+disorder in PRL*
**Roche Carrasco, J. Schirmann, A. Mordret, A. G. Grushin**, *Family of
Aperiodic Tilings with Tunable Quantum Geometric Tensor*, PRL **135**, 236603
(4 Dec 2025); arXiv:2505.13304.
- **What:** tunable aperiodic-tiling family (Chevron/Hat/Turtle/Comet) +
  two-orbital QWZ **Chern** tight-binding; includes uniform diagonal **on-site
  Anderson** disorder → topological-Anderson-insulator transition via spectral
  localizer.
- **How to use:** cite up front as closest prior art; **distinguish on three
  points** — (i) their disorder is on-site Anderson, ours is vacancy/site
  dilution; (ii) their model is a Chern insulator, ours the vertex adjacency
  graph; (iii) they are not zero-mode / matching focused. Reviewers from the
  Grushin lineage will expect this citation.
- **Status:** ✓ ID fetched (arXiv:2505.13304 ↔ PRL 135, 236603).

### [D1] Continuum-polariton hat multifractality
**V. K. Daníelsson (U. Iceland), H. Sigurðsson (U. Warsaw)**, *Critical states
and anomalous wave transport in an aperiodic polariton monotile*,
arXiv:2605.29023 (27 May 2026).
- **What:** 2D **continuum** Schrödinger model, Gaussian polariton scatterers on
  hat vertices; extracts D_q, reports super-/sub-diffusion. NOT the
  vertex-adjacency TB model; no zero-mode / dilution / matching.
- **How to use:** cite if/when we add an IPR/multifractal section — "prior hat
  multifractality is for the continuum polariton model [D1]; we give the first
  vertex tight-binding multifractal data." Leaves our angle open.
- **Status:** ✓ ID fetched. ⚠pub (May-2026 preprint — confirm journal status).

### [B1] Classical hat percolation
**H. Gao (UNSW), A. Bharadwaj (U. Sydney)**, *Percolation Critical Probability of
Aperiodic Smith Hat tile (1, √3)*, arXiv:2604.21165 (23 Apr 2026).
- **What:** classical Bernoulli site/bond percolation on the Smith hat;
  p_c^site ≈ 0.8227, p_c^bond ≈ 0.7982, dual-site ≈ 0.5442.
- **How to use:** background only — "geometric monotile percolation exists [B1]
  but is classical Bernoulli, not quantum zero-mode." Do NOT cite as a
  zero-mode reference. (We also vendor a Bharadwaj port for vertex merging.)
- **Status:** ✓ ID fetched. ⚠pub (Apr-2026 preprint).

---

## Tier 3 — the Gade–Wegner / chiral-class objection (Q1 defense)

Use these to **preempt** the "p_c → 0 is just chiral-class folklore" referee
objection. The argument: Gade–Wegner is about Anderson-localization scaling of
generic E=0 states on a full lattice; our p_c is about geometric spanning of
GE R-regions under dilution — different objects (see NOVELTY.md Q1).

### [C1] **R. König, P. M. Ostrovsky, I. V. Protopopov, A. D. Mirlin**,
*Metal-insulator transition in 2D random fermion systems of chiral symmetry
classes*, PRB **85**, 195130 (2012); arXiv:1201.6288 ✓.
- **How to use:** the authoritative statement that 2D chiral E=0 states are
  anomalous (divergent DOS, perturbatively vanishing weak-localization), not
  generically localized at finite disorder.

### [C2] **P. W. Brouwer, A. Furusaki, Y. Hatsugai, Y. Morita, C. Mudry,
A. Racine**, *Zero-modes in the random hopping model*, PRB **66**, 014204
(2002); cond-mat/0201580 ✓.
- **How to use:** cleanest non-specialist reference — chiral zero-mode
  localization length is boundary-dependent, "anywhere between mean free path
  and infinity." Cite + one sentence on the matching-vs-Anderson distinction.

### [C3] **I. Kleftogiannis, S. Evangelou**, *Multifractal zero mode for
disordered graphene*, arXiv:1304.5968 (2013) ✓.
- **How to use:** supporting — D_2 of the chiral zero mode evolves continuously
  with disorder (critical/multifractal, not abruptly localized).

---

## Tier 4 — clean-limit dimer/matching on aperiodic tilings (context for #2/#3)

These show intensive monomer density + extensive combinatorial structure are
*expected* on aperiodic substrates (so #2 alone is low-novelty); our angle is
the **random geometry of GE under dilution**, which none of them treat.

- **[F1] F. Flicker, S. H. Simon, S. A. Parameswaran**, *Classical Dimers on
  Penrose Tilings*, PRX **10**, 011005 (2020); arXiv:1902.02799 ✓. — rhombic
  Penrose min monomer density 81−50φ ≈ 0.098; introduces impermeable monomer
  membranes. (Flicker overlap with [S2].)
- **[F2] G. Lloyd, S. Biswas, S. H. Simon, S. A. Parameswaran, F. Flicker**,
  *Statistical mechanics of dimers on quasiperiodic Ammann–Beenker tilings*,
  PRB **106**, 094202 (2022). — Ammann–Beenker admits perfect matchings.
  **⚠id** — came via report synthesis; verify volume/page + arXiv number.
- **[F3] A. Singh, F. Flicker**, *Exact Solution to the Quantum and Classical
  Dimer Models on the Spectre Aperiodic Monotiling*, PRB **109**, L220303
  (2024); arXiv:2309.14447 ✓. — Spectre Z = 2^(N_Mystic+1).
- **[F4] Shah, Nambiar, Gorshkov, Galitski**, *A quantum monomer-dimer model on
  Penrose tilings*, arXiv:2503.15588 (2025). — RK model, uniform superposition
  of maximal coverings despite finite monomer density.
- **How to use:** one paragraph — "clean-limit aperiodic matching is mature
  [F1–F4]; the random geometry of Gallai–Edmonds under dilution is the gap."

## Tier 5 — quasicrystal multifractality (context if we add IPR section)

- **[M1] N. Macé, A. Jagannathan, P. Kalugin, R. Mosseri, F. Piéchon**,
  *Critical eigenstates and their properties in 1D and 2D quasicrystals*,
  PRB **96**, 045138 (2017). — exact multifractal states, Penrose/AB.
- **[M2] A. Jagannathan, M. Duneau**, *Properties of the Ammann–Beenker Tiling
  and its Square Periodic Approximants*, Isr. J. Chem. 64(10–11), e202300119
  (2024); DOI 10.1002/ijch.202300119. — modern review.
- **[M3] L. Rieth, U. Grimm, M. Schreiber**, multifractal analysis of
  Ammann–Beenker eigenstates, cond-mat/9809117 (1998). **⚠id** — came via
  report synthesis; verify exact arXiv number + bibliographic details.
- **How to use:** connect a future hat IPR section to the Penrose/AB tradition.

## Tier 5b — Spectre extension (future; see `docs/SPECTRE_TODO.md`)

For the strictly-chiral Spectre monotile as a *second substrate* testing whether
finding #4 is aperiodicity-general. [F3] above is the structural anchor.

- **[SP1] D. Smith, J. S. Myers, C. S. Kaplan, C. Goodman-Strauss**, *A chiral
  aperiodic monotile*, arXiv:2305.17743 (Combinatorial Theory, 2024) ✓. —
  defines Spectre/Tile(1,1) + the Spectre+Mystic two-prototile substitution.
  The generator spec for a Spectre tiling builder.
- **[SP2] M. Baake, F. Gähler, T. Mazáč, L. Sadun**, *On the long-range order of
  the Spectre tilings*, Discrete Comput. Geom. (2025); arXiv:2411.15503 ✓. —
  σ² inflation, area factor λ=4+√15, pure-point spectrum, chirality sectors.
- **[SP3] J. Tatham**, *Finite-state transducers for substitution tilings*,
  arXiv:2512.16595. — practical 9-tile refinement of Spectre/Mystic; useful for
  generation + matching enumeration. **⚠id/⚠pub** — preprint; verify ID.
- **How to use:** [F3]+[SP1] anchor the Spectre matching structure (freedom on
  Upper Mystics, Z=2^(N_Mystic+1)); [SP2] fixes the inflation; cite [S2]'s
  one-paragraph Spectre remark as the only prior TB touchpoint.

## Tier 6 — method / tooling

- **[E1] J. Edmonds**, *Paths, trees, and flowers*, Canad. J. Math. **17**, 449
  (1965); **T. Gallai** (1964); **L. Lovász, M. D. Plummer**, *Matching Theory*
  (1986). — Gallai–Edmonds structure theorem + blossom algorithm. Cite in the
  methods section for the decomposition (D, A, C) and ν / deficiency.
- **[K1] C. S. Kaplan**, *hatviz* (github.com/isohedral/hatviz, BSD-3-Clause). —
  tiling-inflation reference; our generation is ported from it (acknowledge +
  license).

---

## Open citation TODOs

- [ ] **⚠id refs — verify before bibliography:** [F2] Lloyd et al. (PRB 106,
      094202 — vol/page + arXiv), [M3] Rieth–Grimm–Schreiber (cond-mat/9809117 —
      exact ID + details), and [SP3] Tatham (arXiv:2512.16595 — confirm ID/status).
      These came via report synthesis, not a directly fetched page.
- [ ] **⚠pub refs — confirm journal status before submission:** [S4] 2311.05634,
      [S5] 2512.23639, [D1] 2605.29023, [B1] 2604.21165 (all preprints; IDs ✓).
- [ ] If we add the IPR/multifractal section, promote [M1]/[M2]/[D1] to Tier 1.
- [ ] Once finite-size collapse for #4 is in hand, add our own forthcoming
      preprint as the anchor and finalize the contrast sentences vs [S3]/[S4].

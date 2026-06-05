# Hatsoff — Research Plan

Analysis of the four proposed directions (percolation bridge, disorder
fragility, multifractal analysis, closed-form counting) and the concrete
program we will follow.

## Asset inventory (what we actually have)

- `hatsoff.graph.build_tb_graph` — Franca-style vertex tight-binding graph
  from hat polygons (type-c edge splitting). Verified isomorphic to Franca's
  SVGs.
- `hatsoff.spectral` — bipartiteness BFS, `count_zero_modes` (eigsh
  shift-invert), Lieb bound.
- `hatsoff.multifractal` — PR / IPR / D2 log-log slope only. **No** τ(q) or
  f(α) yet.
- `hat_amp.tiling` — full Kaplan substitution (H/T/P/F), `generate_tiling`,
  `expand_hats(metatile)` for per-type expansion, `generate_patch_tiling`.
- `hat_amp.graph` — `build_vertex_graph`, `build_dual_graph`, `crop_square`
  (square window + boundary node sets).
- `hat_amp.percolation` — **working site & bond percolation engine**
  (union-find, crossing criteria, finite-size p_c extrapolation). This is the
  rare asset the percolation project leans on.

Gap vs the advisor's framing: the percolation engine does *geometric*
percolation (does an open cluster span the box). The "zero-mode percolation"
project needs *null-space* percolation — track the support of the adjacency
kernel under dilution — which is new code on top of the dilution machinery
we already have.

## Phase 0 — Trust the integers (GATE, do first)

The advisor is explicit: before scaling any dilution run, reproduce both
tables exactly.

- Zero-flux nullity (Table 2): H = 0/1/8/51. We match L0/L2/L3; **L1 is
  0 vs 1**.
- π-flux zero modes = anti-hat count (Table 3): H = 1/3/22/147. **Not yet
  implemented.**

Tasks:
1. Cross-validate T/P/F at L0–L2 against Table 2 (P/F have nonzero entries:
   P=1/0/1, F=1/0/1, T=0/0/0). If our P(0)/F(0) come out 0 instead of 1, the
   L1 mismatch is a *systematic boundary convention*, not an H-specific bug.
   [running]
2. Implement the π-flux Hamiltonian. π-flux = assign hopping signs so every
   plaquette carries flux π; zero-mode count should equal the anti-hat count.
   Reproduce 1/3/22/147. This is an independent check of the rank/matching
   code that does *not* depend on the boundary convention that trips L1.
3. Characterize (not necessarily "fix") L1: the advisor's prior is boundary
   anti-hat frustration (SM Appendix B.2). If π-flux counts land on the nose
   and the bulk zero-flux counts match, we declare the matching/rank code
   trustworthy and treat L1 as a documented boundary effect.

Exit criterion: π-flux 1/3/22/147 reproduced; zero-flux 0/1/8/51 reproduced
or L1 explained as boundary. Then dilution is trustworthy.

## Phase 1 — Fragility under disorder (warm-up, cheap)

Add random hopping disorder δt·U(-1,1) (or Gaussian) to the equal-hopping
adjacency, diagonalize, watch the E=0 degeneracy split.

- Measure the distribution of |E| for the formerly-zero modes vs disorder
  strength δ and system size (L2, L3).
- Classify modes by spatial support *before* disorder: compact Sutherland
  loops (local, even-distance connectivity) vs extended Hermite-normal-form
  modes. Hypothesis: loop modes are parametrically more robust.
- Deliverable: splitting-distribution figure + short note answering "which
  zero modes are robust, which are accidental."

New module: `src/hatsoff/disorder.py`. Also a sanity check on our E=0
eigenvalue resolution.

## Phase 2 — Multifractal flag-plant (clean single paper)

The paper does DOS + spectral function but **no** multifractal analysis of
eigenstates. Extend `multifractal.py`:

- Generalized IPR R_q = Σ|ψ_i|^{2q}; box-counting on the 2-D vertex
  positions; τ(q) from finite-size scaling; f(α) by Legendre transform.
  Reference: Evers–Mirlin RMP 80, 1355 §II.
- Apply across inflation generations to *all* eigenstates, energy-resolved.
- Open question with teeth: zero modes compact-support (NOT multifractal)
  while non-zero critical states ARE multifractal — coexistence at different
  energies. C6 hat symmetry vs 5-fold Penrose / 8-fold Ammann–Beenker may
  give a distinct f(α).

## Phase 3 — Zero-mode percolation (the real project)

"Zero-mode percolation on a non-bipartite aperiodic monotile via generalized
matching." Bhola et al. (PRX 12, 021058, 2022) use Dulmage–Mendelsohn (a
bipartite construction); the hat is non-bipartite, so we need the
Edmonds–Gallai decomposition (general-graph matching structure theorem).

- Site-dilute the tiling (reuse the dilution path from the percolation
  engine). Track (a) null-space dimension of the diluted adjacency and (b)
  its spatial support.
- Edmonds–Gallai decomposition (D, A, C) of the diluted graph: factor-critical
  components in D carry the topologically protected modes; compare the
  matching deficiency def(G)=|D|-|A| against the actual adjacency nullity to
  separate structural from accidental modes.
- Question: is there a dilution threshold p_c at which *extended* (rather than
  locally trapped) zero modes appear? On bipartite lattices the threshold is
  sharp; on non-bipartite factor-critical components it need not be.

New code: `src/hatsoff/dilution.py` (remove sites, induced subgraph),
`src/hatsoff/matching.py` (Edmonds–Gallai via `networkx.max_weight_matching`
/ blossom + component classification), null-space support tracking, then
fan-out over disorder/dilution realizations × system sizes.

## Execution order

0. Phase 0 gate — π-flux counting + T/P/F cross-val + L1 characterization.
1. Phase 1 warm-up — disorder fragility (cheap, this weekend).
2. Phase 3 scaffolding — dilution + matching, the rare-asset project.
3. Phase 2 — multifractal, parallelizable single paper.

Phases 2 and 3 are each a paper; 0 and 1 are this weekend's concrete work.

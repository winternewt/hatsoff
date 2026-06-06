# hatsoff — zero modes, disorder, and dilution percolation on the hat monotile

Computational study of the **E = 0 zero modes** of the tight-binding
(adjacency) graph of the **hat aperiodic monotile**, and how they behave under
**disorder** and **site dilution** — analyzed through the lens of
**maximum-matching / Gallai–Edmonds** structure theory for general
(non-bipartite) graphs.

The hat vertex graph is non-bipartite, so Lieb's theorem does not apply and the
zero modes are "fragile." We reproduce the clean-limit zero-mode counts of
Schirmann–Franca–Flicker–Grushin, then push into territory their paper does not
cover: random-hopping vs on-site disorder, and the growth/localization of the
null space under dilution — the non-bipartite analogue of the
Dulmage–Mendelsohn percolation of Bhola–Biswas–Islam–Damle.

> **Status: research in progress — novelty GREEN (2026-06-05).** A focused web
> deep-research scan cleared both make-or-break questions: (Q1) **p_c → 0 is not
> Gade–Wegner chiral-class folklore** — it is a Gallai–Edmonds *combinatorial
> support* statement, distinct from Anderson-localization scaling; (Q2) the
> *aperiodic-monotile + matching/Gallai–Edmonds + dilution* niche is **open**.
> Closest live work to cite-and-distinguish: Roche Carrasco et al. PRL 135,
> 236603 (Dec 2025, Anderson on a Chern hat model) and Daníelsson–Sigurðsson
> arXiv:2605.29023 (continuum-polariton hat multifractality). Headline =
> finding #4, now **numerically demonstrated**: the L3 campaign (complete,
> 2026-06-06) gives a spanning threshold `p_c(L)` whose `L → ∞` intercept is
> consistent with **zero** for both transitional proximity distances
> ([`docs/CAMPAIGN_REPORT.md`](docs/CAMPAIGN_REPORT.md),
> `docs/figures/pc_collapse.png`). Remaining upgrade is a non-proxy spanning
> order parameter, not a literature question. See
> [`docs/NOVELTY.md`](docs/NOVELTY.md) and [`docs/REFLIST.md`](docs/REFLIST.md).

## Results so far (where to read)

| Topic | Document | One-line takeaway |
|---|---|---|
| Zero-mode count gate | [`docs/NULLITY.md`](docs/NULLITY.md) | π-flux/anti-hat counts (1/3/22/147) reproduced exactly; zero-flux 0/1/8/51 match except an isolated H-L1 boundary effect → matching/rank code trusted. |
| Disorder fragility | [`docs/DISORDER.md`](docs/DISORDER.md) | Modes are **robust to hopping disorder** (structural/matching protection), **fragile to on-site (chiral-breaking)** disorder and to **bond/site removal**. |
| Dilution + Gallai–Edmonds | [`docs/PERCOLATION.md`](docs/PERCOLATION.md) | nullity ≈ deficiency; non-bipartite gap is small at L2 but **extensive and growing at L3**; trapped-weight fraction intensive (0→0.44); support spanning **p_c(L) → 0** (demonstrated). |
| L3 campaign — final report | [`docs/CAMPAIGN_REPORT.md`](docs/CAMPAIGN_REPORT.md) | Conclusive write-up of the completed run (5390 records): Stage A scalings + the finding-#4 finite-size collapse, with caveats. |
| Novelty / prior art | [`docs/NOVELTY.md`](docs/NOVELTY.md) | **GREEN** — per-finding (a/b/c) verdict + deep-research gate (Q1/Q2) + competitors. |
| Curated bibliography | [`docs/REFLIST.md`](docs/REFLIST.md) | References + per-ref "how to use when writing" hints — kept fresh as work proceeds. |
| Deep-research scan | [`docs/compass_artifact_…_text_markdown.md`](docs) | Full web deep-research report (verbatim) backing the GREEN verdict. |
| Re-run literature scan | [`docs/deepresearch_prompt.md`](docs/deepresearch_prompt.md) | Focused follow-up prompt (open questions only) for a web deep-research tool. |

## Repository map

```
src/hatsoff/
  graph.py         # build_tb_graph: Franca-style vertex tight-binding graph from hat polygons
  spectral.py      # bipartiteness (BFS), zero-mode counting (eigsh), Lieb bound
  disorder.py      # hopping & on-site disorder; zero-mode splitting statistics
  dilution.py      # dilute_sites (induced subgraph), dilute_bonds
  matching.py      # matching_number, deficiency, gallai_edmonds (fast blossom + slow reference), nullspace_support
  support.py       # kernel_support (nullity + diag(P)), support_spanning (proximity percolation); pluggable dense-eigh backend
  multifractal.py  # participation ratios, D2 scaling (Phase 2 scaffolding)

experiments/
  dilution_sweep.py        # L2 site-dilution sweep + figure
  l3_campaign.py           # single-node resumable campaign (Stage A: scalar/GE scaling; Stage B: support spanning)
  l3_campaign_cluster.py   # SLURM multi-node edition (sharded, per-rank JSONL shards, optional GPU eigh)
  submit_l3.sbatch         # SLURM submission script (3x A100 example)
  aggregate_campaign.py    # idempotent: JSONL shards -> summary JSON + figures
  pc_collapse.py           # finding-#4 finite-size analysis: p_c(L) crossing + 1/L fit + figure
  *.jsonl / *.heartbeat / *.log   # checkpoints & progress (generated)

docs/        NULLITY, DISORDER, PERCOLATION, CAMPAIGN_REPORT, NOVELTY, REFLIST, PLAN, THEHAT, deepresearch_prompt
tests/       test_{graph,spectral,multifractal,matching,dilution,support}.py
hat/         Franca et al. Zenodo reference code (BSD 2-Clause) + tiling SVGs
```

Tiling generation, geometry, and generic vertex/dual-graph + percolation
utilities live in the separate **`hat_amp`** package (a dependency);
`hatsoff` imports `hat_amp.{tiling,graph,percolation}`.

## Method in brief

- **Graph.** Each hat polygon contributes 13 boundary vertices; coincident
  vertices are merged (KDTree), and the single double-length "type-c" edge per
  hat is split through its midpoint *only when that midpoint already exists*
  from a neighbour (matches Franca's construction). Result: a non-bipartite
  adjacency matrix `A`.
- **Zero modes.** Count = nullity of `A` (rank deficiency). At π-flux the count
  equals the number of anti-hats (reflected tiles).
- **Matching mapping.** For a general graph, the maximum matching number ν and
  **deficiency** def(G) = N − 2ν bound the structural (topologically protected)
  zero modes; the **Gallai–Edmonds** decomposition (D, A, C) exposes the
  factor-critical ("blossom") components where non-bipartite corrections live.
  For bipartite graphs nullity = def generically; the **gap** = nullity − def
  measures the genuinely non-bipartite content.
- **Support field.** `diag(P)` of the kernel projector `P = VVᵀ` is the
  gauge-invariant per-site zero-mode weight; its spatial spanning is the
  percolation order parameter (see caveats in `docs/PERCOLATION.md`).

## Quickstart

```bash
uv sync
uv run pytest -q                      # tests
uv run python experiments/dilution_sweep.py        # L2 sweep + figure
```

**Single-node campaign** (resumable; writes `experiments/l3_campaign.jsonl`):
```bash
uv run python experiments/l3_campaign.py
uv run python experiments/aggregate_campaign.py     # refresh summary + figures (any time)
uv run python experiments/pc_collapse.py            # finding-#4: p_c(L) fit + pc_collapse.png
cat experiments/l3_campaign.heartbeat               # progress
```

**Multi-node SLURM** (work sharded by task rank; per-rank JSONL shards; optional
GPU `eigh`, one A100 per task; CPU fallback):
```bash
sbatch experiments/submit_l3.sbatch
# or directly:
srun --ntasks=3 --gpus-per-task=1 uv run python experiments/l3_campaign_cluster.py
# raise statistics / runtime:
HATSOFF_STAGE_A_MAX_R=300 HATSOFF_STAGE_B_MAX_R=600 HATSOFF_GPU=1 ...
```
Resume = just re-launch; completed `(stage,level,window,p,seed)` keys are
skipped across all shards. `aggregate_campaign.py` merges every shard.

## Numerical pitfalls (learned the hard way)

- `eigsh(sigma=0)` fails on singular matrices — use `sigma=1e-8`. **And**
  shift-invert `eigsh` *silently under-counts* a deeply degenerate null space
  (hundreds of exact zeros under dilution); `kernel_support` uses **dense
  `eigh`** for N ≤ 9000 (covers L3). See `docs/PERCOLATION.md`.
- `np.linalg.eigh` (LAPACK `syevd`) occasionally raises "Eigenvalues did not
  converge"; we fall back to `scipy.linalg.eigh(driver="evr")`.
- Aggregate-support spanning is sensitive to the proximity distance `d0`
  (zero modes live on even-distance sites); record several `d0` and use the
  window finite-size family — do not read a single-`d0` p_c as physical.
- Boundary vertices have low coordination; small-size counts (e.g. H-L1) can
  show isolated boundary anti-hat frustration effects.

## References

The **authoritative, annotated bibliography** (with per-ref "how to use when
writing" hints and verification status) is [`docs/REFLIST.md`](docs/REFLIST.md).
The short list below is the core; REFLIST adds the chiral-class (Q1 defense),
clean-limit aperiodic dimer, quasicrystal-multifractality, and competitor refs.

Framework and prior art we build on / replicate:

1. **D. Smith, J. S. Myers, C. S. Kaplan, C. Goodman-Strauss**, *An aperiodic
   monotile*, arXiv:2303.10798 (2023); Combinatorial Theory (2024). — The hat.
2. **J. Schirmann, S. Franca, F. Flicker, A. G. Grushin**, *Physical properties
   of an aperiodic monotile with graphene-like features, chirality, and zero
   modes*, Phys. Rev. Lett. **132**, 086402 (2024); arXiv:2307.11054. — Hat
   tight-binding zero modes; clean-limit counts (0/1/8/51), anti-hat = π-flux
   count, non-bipartite/fragile. **The model we replicate and extend.**
3. **R. Bhola, S. Biswas, M. M. Islam, K. Damle**, *Dulmage–Mendelsohn
   percolation: geometry of maximally-packed dimer models and
   topologically-protected zero modes on site-diluted bipartite lattices*,
   Phys. Rev. X **12**, 021058 (2022); arXiv:2007.04974. — Bipartite
   matching↔zero-mode percolation (finite p_c). The framework we generalize.
4. **R. Bhola, K. Damle**, *Chaotic percolation in the random geometry of
   maximum-density dimer packings*, arXiv:2311.05634 (2023, rev. 2025). —
   Gallai–Edmonds on *periodic* non-bipartite lattices (triangular,
   Shastry–Sutherland, …); finite critical densities. Closest method precedent.
5. **R. Bhola, K. Damle** (and co.), *Random geometry of maximum-density dimer
   packings of the site-diluted kagome lattice*, arXiv:2512.23639 (2025).
   *(recent preprint — verify before citing in print.)*
6. **J. Edmonds**, *Paths, trees, and flowers*, Canad. J. Math. **17**, 449
   (1965); **T. Gallai** (1964); **L. Lovász, M. D. Plummer**, *Matching
   Theory* (1986). — The Gallai–Edmonds structure theorem and blossom algorithm.
7. **C. S. Kaplan**, *hatviz* (github.com/isohedral/hatviz, BSD-3-Clause). —
   Authoritative tiling-inflation reference; our generation is ported from it.

Closest live competitors (cite up front, distinguish — see REFLIST [G1]/[D1]):

8. **Roche Carrasco, J. Schirmann, A. Mordret, A. G. Grushin**, *Family of
   Aperiodic Tilings with Tunable Quantum Geometric Tensor*, PRL **135**, 236603
   (2025); arXiv:2505.13304. — on-site Anderson on a Chern hat-family model;
   *not* vacancy/matching/zero-mode. Only Hat-TB+disorder paper in PRL.
9. **V. K. Daníelsson, H. Sigurðsson**, *Critical states and anomalous wave
   transport in an aperiodic polariton monotile*, arXiv:2605.29023 (2026). —
   continuum-polariton hat multifractality; *not* the vertex-TB model.

(arXiv IDs marked ✓ in REFLIST were directly fetched and are solid; the recent
preprints — refs 4, 5, 8, 9 — need a journal-status check before print, and a
few synthesis-only IDs in REFLIST are flagged ⚠id for verification.)

## Acknowledgments & license

Tiling generation is ported from Craig Kaplan's `hatviz` (BSD-3-Clause). The
`hat/` directory vendors the Schirmann–Franca–Flicker–Grushin Zenodo code
(BSD 2-Clause, DOI 10.5281/zenodo.8215399). Percolation utilities follow the
Bharadwaj *Aperiodic-Monotile-Percolation* port. Please cite references 1–4
above if you reuse this work.

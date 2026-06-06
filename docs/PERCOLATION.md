# Zero-Mode Percolation via Generalized Matching (Phase 3) — Status

Goal: as the hat tiling is site-diluted, how does the adjacency null space
grow, and is there a threshold p_c where *extended* (rather than locally
trapped) zero modes appear? Bhola et al. (PRX 12, 021058, 2022) answer this
for *bipartite* lattices via Dulmage--Mendelsohn matching; the hat is
non-bipartite, so we use the **Gallai--Edmonds** structure theorem instead.

## Scaffolding (done)

| Module | Provides |
|---|---|
| `hatsoff.dilution` | `dilute_sites` (induced subgraph), `dilute_bonds` |
| `hatsoff.matching` | `matching_number` ν, `deficiency` N−2ν, `gallai_edmonds` (D,A,C + factor-critical component count; fast/slow), `nullspace_support` (gauge-invariant per-site kernel weight diag(P)) |
| `hatsoff.disorder` | hopping / on-site disorder (Phase 1) |

Tests: `tests/test_matching.py`, `tests/test_dilution.py` (14, all pass),
ground-truthed on K3 / P4 / star.

## Observables

1. **Adjacency nullity** n₀ = dim ker A — the true zero-mode count.
2. **Matching deficiency** def(G) = N − 2ν(G) — the structural/topological
   count.
3. **The gap** n₀ − def(G). For bipartite graphs this is ≡ 0 (Bhola regime).
   For non-bipartite graphs the **odd factor-critical components** of G[D]
   make it nonzero — this is the new physics. (K3: n₀=0, def=1, gap=−1.)
4. **Support field** diag(P)_i ∈ [0,1], P the kernel projector. max≈1 ⇒ a
   site carries a fully *trapped* (localised) mode; broad small values ⇒
   *extended* support. Order parameter for the percolation question: does the
   set {i : diag(P)_i > θ} span the sample (reuse `hat_amp` crossing tests)?

## First findings (L2, N=1084, single realizations)

| State | nullity | ν | def | gap | max diag(P) | support sites |
|---|---|---|---|---|---|---|
| clean | 8 | 538 | 8 | 0 | 0.11 | 325 |
| site-dilute p=0.05 | 23 | 505 | 24 | −1 | 1.00 | 242 |
| site-dilute p=0.10 | 68 | 439 | 68 | 0 | 1.00 | 331 |

- **At the clean point the 8 zero modes are exactly the matching-deficiency
  modes** (gap 0) and are *delocalized* (no trapped site). This matches the
  Phase 1 result that hopping disorder cannot split them.
- **Dilution immediately creates trapped modes** (max diag(P) → 1) and opens
  a fluctuating gap that can go negative (odd factor-critical components) —
  the genuinely non-bipartite behavior absent from Bhola et al.

## Step (a) — L2 dilution sweep (done)

`experiments/dilution_sweep.py` → `experiments/dilution_sweep_L2.json`,
`docs/figures/dilution_sweep_L2.png`. H level 2, N=1084, R=20 realizations,
p ∈ [0, 0.30].

| p | N_kept | nullity | def | gap | trapped | trapped-wt frac |
|---|---|---|---|---|---|---|
| 0.00 | 1084 | 8.0  | 8.0  | +0.00 | 0.0  | 0.00 |
| 0.05 | 1032 | 28.9 | 28.8 | +0.05 | 1.4  | 0.05 |
| 0.10 | 972  | 50.0 | 50.2 | −0.20 | 7.5  | 0.16 |
| 0.20 | 864  | 92.5 | 92.6 | −0.05 | 28.2 | 0.31 |
| 0.30 | 758  | 125.8| 125.8| +0.00 | 55.3 | 0.44 |

Findings:
- **nullity ≈ deficiency throughout** (top-left panel): zero-mode growth is
  governed by the matching number, ≈ +4 modes per 1% of sites removed.
- **The non-bipartite gap is small and always ≤ 0 on average** (mean ≈ −0.1,
  within realization scatter). Odd factor-critical components do appear but
  are a subleading correction at these dilutions — the hat is "almost
  bipartite" for *counting*. Whether the gap grows at larger p / larger L is
  open and needs the fast GE (step b) for the size dependence.
- **Locally trapped modes proliferate**: trapped-weight fraction rises
  monotonically 0 → 0.44 by p=0.30. A growing share of the null space is
  pinned on isolated/dangling sites.
- The global support radius of gyration saturates near 1 — this is *global*
  spread (point modes scattered across the sample), **not** per-mode
  localization, so it does not answer the percolation question. That needs a
  spatial spanning / per-mode crossing probe (below).

## Step (b) — fast Gallai--Edmonds (done)

`gallai_edmonds(graph, method="fast")` extracts the inessential set D from a
single maximum matching via one blossom-aware alternating-forest pass
(O(V·E)); `method="slow"` keeps the O(N)-matchings reference. Validated to
agree with the reference on K3 / C5 / K5 / Petersen / bridged triangles and
400/400 random non-bipartite graphs (`tests/test_matching.py`). Timing:

| Level | N | fast GE | def_GE = N−2ν = nullity |
|---|---|---|---|
| 2 | 1084 | 0.18 s | 8 |
| 3 | 7047 | 11.4 s | 51 |

At both clean sizes every G[D] component is a single vertex
(c(D)=|D|), and def_GE reproduces the exact zero-mode counts (8, 51) — the
clean zero modes are exactly the matching-deficiency modes at L3 too.

## Next steps (the campaign)

1. **Support percolation order parameter.** Threshold diag(P) and run a
   spatial square-crossing test on the support set (reuse `hat_amp`
   `crop_square` + crossing); finite-size scaling for p_c. NB the support
   lives on even-distance sites, so the crossing must use spatial spanning,
   not direct graph adjacency.
2. **Gallai--Edmonds scaling vs p.** With fast GE, track c(D), |A|, and the
   size distribution of factor-critical components across p and L2/L3 —
   locate where large (extended) factor-critical components first appear.
3. **L3 sweep.** `def`/GE are now cheap; the remaining L3 bottleneck for the
   *gap* is exact nullity + support (dense eigh ~ minutes/realization). Use a
   sparse/iterative null-space (e.g. shift-invert `eigsh` near 0, or exact
   GF(p) rank on the integer adjacency) so the gap and support fields scale
   alongside GE.

## L3 campaign — COMPLETE (2026-06-06)

> **Conclusive report: [`CAMPAIGN_REPORT.md`](CAMPAIGN_REPORT.md).** The run
> finished (5390 records: Stage A 1082 @ R=60, Stage B 4308 @ ~120 seeds/point).
> Stage B proxy gave `p_c(L) → 0` — **but ⚠ this did NOT survive the rigorous
> cross-check.** The parameter-free Gallai–Edmonds R-region order parameter
> (`rregion_campaign.py`, 8 sizes × 300 seeds; `rregion_collapse.png`) gives a
> **finite** p_c ≈ 0.055; the p_c→0 was a proximity-proxy artifact. See
> `CAMPAIGN_REPORT.md` §"Rigorous cross-check". Figures
> `campaign_stage_{a,b}.png` + `pc_collapse.png` (proxy) + `rregion_collapse.png`
> (rigorous, decisive).

Driver `experiments/l3_campaign.py` (resumable, self-calibrating,
checkpointed); aggregator `experiments/aggregate_campaign.py` (idempotent,
runs on partial data). New module `hatsoff.support`
(`kernel_support`, `support_spanning`).

- **Stage A** — scalar + GE scaling on full L2/L3 graphs: nullity, def, gap,
  GE structure (|D|,|A|,|C|, c(D), factor-critical component sizes), trapped.
- **Stage B** — support spatial spanning on crop windows (fractions
  0.40/0.55/0.70/0.85 of the L3 extent), recorded at d0 ∈ {1.0,1.2,1.4,1.6}.

**Cluster (SLURM/multi-node)**: `experiments/l3_campaign_cluster.py` +
`experiments/submit_l3.sbatch`. Same per-unit physics, sharded by global task
rank (deterministic seeds → rank-independent, identical results); each task
writes its own `l3_campaign.rank###.jsonl` shard (no append contention),
resume globs all shards. `HATSOFF_GPU=1` routes the dominant dense `eigh`
through CUDA (PyTorch fp64, one A100 per task; Gallai–Edmonds matching stays
CPU). R caps raised via `HATSOFF_STAGE_A_MAX_R`/`HATSOFF_STAGE_B_MAX_R`.
`aggregate_campaign.py` reads every shard + the single-node file (dedup by key).

Checkpoints: append-only `experiments/l3_campaign.jsonl` (one fsynced record
per unit, skip-done resume), `l3_campaign.heartbeat`, `l3_campaign.log`.
Self-calibrating to wall-clock budgets (Stage A 16h cap / R≤60, Stage B 24h
cap / R≤300); deterministic seeds; portable to a cluster (copy script + JSONL,
rerun → continues). Monitor: `cat experiments/l3_campaign.heartbeat`; refresh
figures anytime: `uv run python experiments/aggregate_campaign.py`.

### Numerical lesson (important)

`eigsh` shift-invert **silently under-counts** the null space once dilution
creates a deeply degenerate kernel (hundreds of exact zeros): at L3 p=0.30 it
returned nullity 547 vs deficiency 791 (gap −244) and trapped_frac 0 — wrong.
ARPACK cannot resolve a several-hundred-fold degenerate eigenvalue. `eigsh`
returned ~3 s but lied. **Dense `eigh` (~35–74 s, exact, robust)** gives
nullity 790 / gap −1 / trapped_frac 0.41 — consistent with L2. `kernel_support`
therefore uses dense `eigh` for N ≤ 9000 (covers L3); `eigsh` is only a
large-N (L4+) fallback and should be validated against `eigvalsh` before trust.

### Stage A results — COMPLETE (L2 & L3, R=60), `docs/figures/campaign_stage_a.png`

Three findings, the first two genuinely new:

1. **The non-bipartite gap is extensive and grows with system size.** At L2
   the mean gap (n₀−def) hugs 0 — the "almost bipartite" reading from the
   earlier single-size sweep. At **L3 the gap dips to ≈ −1.7 around p≈0.08**
   and recovers toward 0 by p=0.30. Gap *density* is comparable across sizes
   (≈ −3×10⁻⁴/site at the dip), i.e. the odd factor-critical correction to the
   zero-mode count is **extensive**, peaking at intermediate dilution. So the
   non-bipartite physics is NOT subleading — it was just invisible at L2 size.
   This is the qualitative departure from the bipartite Bhola picture.
2. **Trapped-weight fraction is intensive — L2 and L3 collapse** onto one
   curve, rising 0 → 0.44 by p=0.30. Localization onto isolated/dangling sites
   is size-independent.
3. **The largest factor-critical (odd) component grows with size**: max size
   ≈16 at L2 vs ≈48 at L3, both **peaking at small p≈0.03** then shrinking as
   the graph fragments. Extended odd matching structure (the Edmonds–Gallai
   "blossoms") is most prominent just past the clean point and is larger in
   larger systems — the structural signature absent from bipartite lattices.

### Stage B results — COMPLETE (finding #4), `docs/figures/pc_collapse.png`

Support spatial spanning on crop windows L ≈ 35/49/62/75, ~120 seeds/point,
d0 ∈ {1.0,1.2,1.4,1.6}. The spanning probability `P_span(p,L)` **decreases
monotonically with size at every finite p** and is pinned to 1 only at p = 0.
Extracting `p_c(L)` as the `P_span = ½` crossing and fitting `p_c = a + b/L`:

| d0 | p_c(35) | p_c(49) | p_c(62) | p_c(75) | intercept a (L→∞) |
|----|---------|---------|---------|---------|-------------------|
| 1.2 | 0.048 | 0.042 | 0.038 | 0.019 | **+0.004 ± 0.015** |
| 1.4 | 0.061 | 0.047 | 0.043 | 0.020 | **−0.005 ± 0.015** |

d0 = 1.0 never spans (support too sparse — no crossing); d0 = 1.6 spans up to
large p (only L≈75 crosses in-grid). The transition lives at d0 = 1.2 / 1.4 and
**both extrapolate to ~0** — the robustness we claim. This is finding #4:
`p_c → 0` on the aperiodic hat, vs **finite** p_c on every periodic Damle
lattice. See `CAMPAIGN_REPORT.md` for the full discussion + caveats (proximity
proxy; few sizes / mild curvature; non-proxy order parameter is the next
upgrade before this is load-bearing).

(Supersedes the earlier preliminary read "clean spans, p=0.10 does not span at
any d0" — qualitatively the same, now quantified with the size family.)

## References

- Bhola, Biswas, Islam, Damle — PRX 12, 021058 (2022) — DM percolation,
  bipartite.
- Gallai--Edmonds structure theorem (general-graph maximum matching).
- Franca, Schirmann, Flicker, Grushin — PRL 132, 086402 (2024) /
  arXiv:2307.11054.

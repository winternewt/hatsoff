# Zero-Mode Fragility Under Disorder (Phase 1 warm-up)

Module: `src/hatsoff/disorder.py`. System: H metatile, level 2
(N = 1084 vertices, 8 clean zero modes). Disorder strengths swept with 10–20
realizations each; seeded RNG.

## Headline result — "fragile" needs qualifying

The literature calls the hat zero modes *fragile — they depend on equal
hoppings*. Our numerics show the fragility is **selective**, not generic:

| Perturbation | Preserves bond support? | Preserves zero diagonal? | Effect on the 8 modes |
|---|---|---|---|
| Hopping disorder `t→t(1+δη)` | yes | yes | **none** — stay at \|E\|~1e-15 up to δ=0.3 |
| On-site disorder `ε_i=Wη_i` | yes | **no** | split, rms\|E\| ∝ W (modestly: ~0.014 at W=0.3) |
| Bond dilution (remove fraction p) | **no** | yes | **proliferate**: 8→16→28→51→112 for p=0→0.2 |

### 1. Robust to hopping disorder (structural protection)

rms\|E\| of the former zero modes is flat at ~4e-15 across δ ∈ [0.001, 0.3]
(fitted exponent ≈ 0). All 8 modes survive every realization. This is the
generic-rank property: a real symmetric matrix with **fixed off-diagonal
support and zero diagonal** has a fixed maximal rank, so the kernel dimension
N − rank is the same for (almost) any hopping values, not just equal ones.
The equal-hopping point is not special. The zero-mode *count* is therefore a
graph (matching) invariant, which is exactly why the Edmonds–Gallai framing
of Phase 3 is the right language.

### 2. Fragile to chiral-symmetry breaking (on-site disorder)

Adding a random diagonal potential breaks the zero-diagonal (sublattice-like)
structure and does split the modes, with rms\|E\| growing roughly linearly in
W but staying small (≈1.4e-2 at W=0.3). The modes broaden into a narrow
E≈0 band rather than scattering — consistent with a Lifshitz-tail-like
feature; worth a finite-size DOS-near-zero study.

### 3. Fragile to bond dilution (→ Phase 3)

Removing bonds is the perturbation the modes are genuinely fragile to: the
nullity climbs steeply with dilution (≈ +5 modes per 1% of bonds removed near
p=0). This zero-mode proliferation under dilution is precisely the
phenomenon the percolation project quantifies via generalized matching.

## Takeaways

- Reframe "fragile to equal hoppings" → **fragile to chiral breaking and to
  topology change, robust to hopping randomness.** This is a publishable
  short-note correction/clarification on its own.
- The robustness under hopping disorder confirms the zero-mode count is a
  matching invariant of the graph → validates the Phase 3 approach.
- Next: classify the clean kernel basis into compact (Sutherland-loop) vs
  extended (HNF) supports and check whether on-site disorder hits them
  differently; run L3 (51 modes) to confirm size-independence.

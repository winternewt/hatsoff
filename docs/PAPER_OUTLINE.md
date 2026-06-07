# Paper outline (reframe after the #4 retraction) — 2026-06-07

**One-line thesis:** *Local order, not aperiodicity per se, governs the protected
zero modes of aperiodic-monotile tight-binding graphs.*

The original flagship ("p_c → 0 on the hat, qualitatively unlike periodic
lattices") was **retracted** by its own rigorous cross-check (finite p_c ≈ 0.055).
This reframe keeps the honest negative and builds the paper around a **substrate
contrast** — hat vs Spectre vs periodic triangular — plus a genuinely novel
positive result (the Spectre π-flux Mystic sector) and a methodological caution.

## Working title
*Local order versus aperiodicity in monotile zero modes: a matching-theoretic and
π-flux study of the hat and the Spectre.*

## Candidate venue framing
First combined (aperiodic monotile) × (site dilution) × (maximum-matching /
Gallai–Edmonds) study; first spectral data on the Spectre vertex graph beyond
Schirmann et al.'s one paragraph. Niche confirmed open (NOVELTY.md Q1/Q2).

## Sections

1. **Introduction.** Hat & Spectre monotiles; vertex tight-binding graphs; protected
   zero modes (Franca/Schirmann); the question — does aperiodicity or local order
   protect them? Position vs the Damle program (periodic, finite p_c) and vs
   Singh–Flicker (Spectre dimers).

2. **Methods.** Vertex TB graph (`build_tb_graph`, type-c / long-edge convention);
   maximum matching + Gallai–Edmonds R-region; site dilution; the **parameter-free
   R-region spanning** order parameter (vs the retracted geometric proxy); π-flux
   Peierls Hamiltonian (`flux.py`, `B=π/A_tile`) and dense complex `eigh`/RRR-subset.

3. **R1 — Count gate (trust).** Reproduce Franca/Schirmann clean counts: zero-flux
   0/1/8/51 and π-flux 1/3/22/147 (= anti-hats) from our graph. Establishes the
   pipeline and that our edge convention = theirs. [`docs/NULLITY.md`,
   `tests/test_flux.py`.]

4. **R2 — Hat under dilution (the honest result + methodology).** nullity ≈
   deficiency; non-bipartite gap; trapped weight; largest factor-critical
   component. **Finite p_c ≈ 0.055** from the rigorous GE R-region (sharpening
   crossings), *unlike* the geometric proxy which faked p_c → 0. The hat has an
   **extensive clean-limit R-region** (spans at p=0) that de-percolates at finite
   p_c — like the periodic Damle lattices. [`CAMPAIGN_REPORT.md`,
   `rregion_*`, fig `rregion_collapse.png`.]
   *Methodological caution:* report the proxy-vs-rigorous discrepancy as a warning
   to the field.

5. **R3 — Hat vs Spectre, clean limit (the contrast).** Same aperiodicity, opposite
   local order. Hat: extensive zero-flux clean null space. Strictly-chiral Spectre:
   **zero-flux clean nullity 0** at all sizes. [`SPECTRE_TODO.md`; comparative
   dilution fig from `spectre_rregion_campaign.py` (running) + hat `l3_rregion`
   + `periodic_control`.]

6. **R4 — Spectre π-flux Mystic sector (the novel positive).** Reconciled
   construction (count gate). **Clean π-flux nullity = N_Mystic/2 = one protected
   mode per Mystic**, and the kernel is **100% Mystic-localized in the TD limit**
   (fig `spectre_flux.png`, `spectre_flux_consolidate.png`) — first quantitative
   check of Schirmann's data-free anti-spectre conjecture. Under dilution: nullity
   grows but Mystic enrichment decays to ~1 (size-independent crossover p\*≈0.15)
   — disorder-created modes are delocalized, not Mystic-anchored; **smooth
   crossover, no sharp transition** (a spanning probe would be needed to claim one).

7. **R5 — Periodic triangular control.** Finite p_c, no extensive clean R-region —
   anchors "the hat behaves like periodic under dilution, but has the extra clean
   sector." [`periodic_control.py`.]

8. **Discussion.** The thesis: achiral, mta-hexagonal-derived **hat** → extensive
   clean (graphene-like) modes + finite-p_c de-percolation; strictly-chiral
   **Spectre** → no zero-flux clean modes, only π-flux Mystic-anchored ones;
   periodic = control. ⇒ **local order (hexagonal descent / chirality), not
   aperiodicity, is the knob.** Methodological note (proxy artifact).

9. **Conclusion + outlook.** L4 hat (finite vs slow→0), Spectre π-flux
   de-percolation spanning probe, IPR/multifractal, Anderson/TAI.

## Status of evidence (what exists vs to-do)

| Section | Data / figure | Status |
|---|---|---|
| R1 count gate | `tests/test_flux.py`, NULLITY | ✅ done |
| R2 hat dilution + p_c | `l3_rregion.jsonl`, `rregion_collapse.png`, CAMPAIGN_REPORT | ✅ done |
| R3 clean contrast + R5 control | hat `l3_rregion` + `spectre_rregion.jsonl` (running) + `periodic_control` | ⏳ Spectre campaign running; needs a 3-substrate comparative figure |
| R4 π-flux Mystic | `spectre_flux*.png`, SPECTRE_TODO | ✅ done |
| Outlook | — | optional (L4 GPU; π-flux spanning re-run) |

**Immediate next after the Spectre rregion campaign lands:** a single
hat-vs-Spectre-vs-periodic comparative figure (R-region spanning fraction &
deficiency density vs p, finite-size family) — the visual centerpiece of R3/R5.

# Novelty assessment — zero-mode dilution on the hat monotile

Salvaged from the (crashed) deep-research run: the verification phase had
completed with 9 adversarially-verified claims (3-vote) before the final
synthesis step failed. The load-bearing "finite vs zero threshold" fact was
re-confirmed by direct WebFetch. Confidence levels marked per item.

## Bottom line (go / no-go)

**Yellow light.** The matching-theory ↔ zero-mode-percolation *framework* is
NOT ours to claim — the Damle group (TIFR) owns it and is actively extending
it. But it has only ever been applied to **periodic** lattices; **nobody has
done it on an aperiodic monotile**, and Franca et al.'s monotile paper does no
dilution/matching/percolation at all. So the *substrate is open*, and one of
our results — finding #4 (p_c → 0) — would be a genuine qualitative departure
from the **finite** thresholds they find on periodic non-bipartite lattices,
**if** it survives a non-proxy treatment. Verdict: worth pursuing only if we
(a) reframe around what is aperiodic-specific and (b) nail #4 rigorously;
otherwise it risks reading as "Bhola–Damle on yet another lattice."

## Reference map (verified)

| Ref | What | Bearing |
|---|---|---|
| **arXiv:2307.11054 = PRL 132, 086402 (2024)**, Schirmann–Franca–Flicker–Grushin | Hat monotile tight-binding; non-bipartite; Lieb fails; zero modes 0/1/8/51; "fragile" (equal hoppings). Does **no** dilution/percolation/matching/chiral-class/multifractal analysis. | Our clean-limit baseline; leaves all our directions open. (3-0) |
| **arXiv:2007.04974 = PRX 12, 021058 (2022)**, Bhola–Biswas–Islam–Damle | "Dulmage–Mendelsohn percolation": site-diluted **bipartite** lattices; maximum matching → monomer regions of sublattice imbalance control E=0 localization; a distinct **finite-p_c** percolation universality class of zero-mode support. | Bipartite precedent for finding #4 (finite p_c). (3-0) |
| **arXiv:2311.05634 (2023, rev 2025)**, Bhola–Damle, "Chaotic percolation in the random geometry of maximum-density dimer packings" | **Non-bipartite** site-diluted lattices (triangular, Shastry–Sutherland; 3D stacked-triangular, octahedral) via **Gallai–Edmonds**; R-type (factor-critical, monomer) vs P-type regions; **finite** critical vacancy densities (phases "separated by critical points," "well within the geometrically percolated phase"). **No aperiodic/monotile.** | Direct method precedent for findings #1/#3; its finite p_c is the contrast for #4. (3-0 + WebFetch-confirmed) |
| **arXiv:2512.23639 (Dec 2025)**, Bhola/Damle, "…maximum-density dimer packings of the site-diluted **kagome** lattice" | Gallai–Edmonds on site-diluted kagome: odd connected clusters → exactly one factor-critical R-region hosting one monomer; even clusters perfectly matched. | Shows the group is still actively mining this vein (non-bipartite, periodic). (2-0) |
| **arXiv:2604.21165 (2026)** (Bharadwaj-style) | **Classical** Bernoulli percolation on the hat (p_c^site≈0.823, bond≈0.798, dual≈0.544). "The only existing monotile percolation paper" — but geometric, **not** quantum/zero-mode. | Confirms monotile-percolation interest exists; orthogonal to our quantum question. (unverified, 0-0) |
| cond-mat/0201580; arXiv:1304.5968 | Random-hopping / chiral-class (BDI/AIII, Gade–Wegner) E=0 localization in graphene-like models; anomalous, boundary-dependent localization length. | #4's "p_c→0 / delocalized only at clean point" may be chiral-class folklore — must rule this out. (unverified) |
| arXiv:2209.01443 / 2308.07701 / 2403.04598 (Jagannathan–Macé); 2004.12291 | Ammann–Beenker / Penrose tight-binding, confined/strictly-localized states, multifractality; "Nature of protected zero modes in Penrose" (bipartite-protected). | Context for a future multifractal angle and the bipartite-protected contrast. |

## Per-finding verdict

**#1 — Extensive negative non-bipartite gap (nullity − def), growing with size.**
Verdict **(b), method known / monotile-specific quantification possibly (c).**
The nullity↔matching-deficiency mapping via Gallai–Edmonds, with factor-critical
("blossom") components carrying the correction, is exactly the Bhola–Damle
framework (2311.05634, 2512.23639) — on periodic lattices. Closest prior: those
two. Publishable only if the *extensivity and its p-dependence are tied to the
aperiodic (inflation) structure*, not just reproduced.

**#2 — Trapped-weight fraction intensive (L2/L3 collapse), 0→0.44.**
Verdict **(a)/(b), low standalone novelty.** Monomers on small/odd clusters and
isolated sites are the standard R-type/monomer picture; an intensive trapped
fraction is expected. Useful as supporting data, not a headline.

**#3 — Largest factor-critical component grows with size, peaks at small p.**
Verdict **(b), concept known.** This *is* the Gallai–Edmonds R-region geometry
and its incipient-percolation growth — the core object of "chaotic percolation"
(2311.05634). Novelty is only in the aperiodic substrate.

**#4 — Zero-mode support spanning with p_c → 0 (vs finite p_c on bipartite/
periodic non-bipartite lattices).**
Verdict **potentially (c) — the one flag-worthy result, conditional.**
The bipartite case (2007.04974) and periodic non-bipartite case (2311.05634)
both have **finite** thresholds (WebFetch-confirmed for the latter). A genuine
p_c → 0 on the *aperiodic* monotile would be a qualitative, aperiodicity-driven
difference with no found precedent. **Conditions to trust it:** (i) replace the
proximity-proxy spanning with a rigorous per-mode / R-region spanning order
parameter; (ii) confirm finite-size trend across all d0 and larger L; (iii)
rule out that it is generic chiral-class random-hopping localization
(cond-mat/0201580, 1304.5968) rather than monotile-specific.

## Direct competitors

- **Damle group (TIFR): Bhola, Biswas, Islam, Damle.** Own the entire
  machinery — bipartite (2022) → non-bipartite periodic (2023) → kagome
  (Dec 2025). They are the people most likely to do the monotile next; the
  niche is open but not safe indefinitely.
- **Grushin / Flicker / Schirmann / Franca** (monotile zero modes) could bolt
  dilution onto their own model.
- Classical monotile percolation (2604.21165) shows the substrate is on radar.

## Caveats

- Reconstructed from a failed run: claims tagged 3-0/2-0 passed adversarial
  verification; the finite-threshold fact for 2311.05634 was re-confirmed live.
  The chiral-class "p_c→0 is known" possibility (cond-mat/0201580, 1304.5968)
  was NOT fully verified — it is the main risk to #4's novelty and should be
  checked before committing.
- Recency: 2512.23639 (Dec 2025) and 2604.21165 (2026) are very new; verify
  they are real and final before citing in a paper.
- Re-run the full prompt in `docs/deepresearch_prompt.md` on web to close the
  loop (especially: any 2024–2026 paper already pairing a monotile/quasicrystal
  with matching-theory zero modes, and the chiral-class question for #4).

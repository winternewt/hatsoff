# Novelty assessment — zero-mode dilution on the hat monotile

> **⚠ STATUS DOWNGRADE (2026-06-06): the #4 headline did NOT survive its own
> cross-check.** The rigorous, parameter-free Gallai–Edmonds R-region order
> parameter (`docs/CAMPAIGN_REPORT.md` §"Rigorous cross-check") gives a **FINITE**
> spanning threshold p_c ≈ 0.055, not p_c → 0; the proximity-proxy p_c→0 was an
> artifact. So the flagship claim "p_c→0, qualitatively unlike every periodic
> Damle lattice" is **retracted**. The literature gate below (Q1/Q2) is still
> valid — the *niche* (aperiodic monotile + matching + dilution) remains open and
> unstudied — but the headline RESULT that filled it is gone. **Net: from GREEN
> (novel headline) to a weaker "first study of an open niche, finite p_c like
> periodic lattices" + residual angles (extensive clean-limit R-region; findings
> #1/#3; a methodological proxy-artifact caution).** Reassess paper framing
> before proceeding — see CLAUDE.md "Pending decision". The pre-cross-check
> assessment is retained below for the record.
>
> **UPDATE 2026-06-07 — the reframe has a genuinely novel positive result.** The
> hat-vs-Spectre contrast under the *same* aperiodicity is now quantitative and
> the **first** spectral data on the Spectre vertex graph beyond Schirmann's one
> paragraph: zero-flux clean nullity 0 (vs hat's extensive), and **π-flux clean
> nullity = N_Mystic/2 = one protected mode per Mystic, 100%-Mystic-localized in
> the TD limit** (`src/hatsoff/flux.py`, `docs/SPECTRE_TODO.md`) — the first
> *quantitative* check of Schirmann et al.'s data-free anti-spectre conjecture.
> This **supports the thesis** (*local order, not aperiodicity, governs protected
> zero modes*: hat's achiral hexagonal order → extensive clean modes; chiral
> Spectre → modes only at π flux, on its Mystic minority). Net verdict now:
> **YELLOW-GREEN** — open niche + a novel positive Spectre result + the honest
> negative #4 + the proxy-artifact methodology, not a single retracted headline.

> **⟦ARCHIVED — pre-cross-check assessment, retained for the record. The
> "GREEN" verdict below is SUPERSEDED by the 2026-06-06 downgrade above; read it
> only for the still-valid Q1/Q2 literature gate, not for the headline verdict.⟧**
>
> **STATUS: GREEN (updated 2026-06-05).** A focused web deep-research run
> (`docs/compass_artifact_wf-95d25a67-…_text_markdown.md`) resolved both
> make-or-break questions **in our favor**. The earlier "yellow" assessment
> below (salvaged from a crashed in-harness run) is superseded on the two gate
> questions; the per-finding verdicts and reference map remain valid and are
> now augmented. See "Deep-research verdict" immediately below.

## Deep-research verdict (2026-06-05) — GREEN

Both gate questions answered:

- **Q1 — Is p_c → 0 just chiral-class (Gade–Wegner) folklore? → NO.** Two
  genuinely different objects were being conflated. *Gade–Wegner* (classes
  AIII/BDI/CII) concerns the Anderson localization length / multifractal scaling
  of **generic random-hopping eigenstates at E=0 on a full lattice** (König–
  Ostrovsky–Protopopov–Mirlin PRB 85, 195130 (2012); Brouwer et al. PRB 66,
  014204 (2002)). *Our p_c* concerns the **geometric spanning of the
  Gallai–Edmonds R-regions** (forced-monomer sites) under **site dilution** — a
  Hamiltonian-disorder-independent combinatorial property. Both can be true at
  once; they answer different questions. Every periodic lattice in the Damle
  program has **finite** p_c, so our p_c → 0 is a real departure, not folklore.
- **Q2 — Is the aperiodic-monotile + matching/Gallai–Edmonds + dilution niche
  occupied? → NO, OPEN.** No preprint/journal/thesis/APS abstract 2023–2026
  combines (i) aperiodic tiling + (ii) site dilution + (iii) maximum-matching /
  Gallai–Edmonds zero-mode analysis.

**Two new adjacent competitors surfaced — cite up front, neither preempts:**
- **Roche Carrasco, Schirmann, Mordret, Grushin, PRL 135, 236603 (4 Dec 2025);
  arXiv:2505.13304** — tunable aperiodic-tiling family + two-orbital QWZ **Chern**
  model, with a uniform **on-site Anderson** disorder / topological-Anderson
  section. NOT vacancy dilution, NOT the vertex graph, NOT zero-mode/matching.
  Currently the *only* Hat-TB + disorder paper in PRL → reviewers will know it;
  distinguish on those three points.
- **Daníelsson & Sigurðsson, arXiv:2605.29023 (27 May 2026)** — multifractal /
  D_q of a **continuum polariton** Hat (Gaussian scatterers on hat vertices),
  not the vertex-adjacency TB model, no zero-mode/dilution/matching. Leaves our
  vertex-TB multifractal angle open too.

**Headline framing recommended by the scan:** lead with finding #4 —
*"On aperiodic monotiles, Gallai–Edmonds support percolation collapses to the
clean point — qualitatively unlike every periodic lattice in the Damle program."*
Findings #1/#3 are supporting structural diagnostics. The single highest-leverage
upgrade: a **finite-size collapse** of the spanning probability / support
fraction at 2–3 small p across the largest tractable sizes, fit to
p_c(L) ∼ L^(−1/ν), to convert "trend suggests p_c → 0" into "scaling collapse
demonstrates p_c → 0." (Optional second upgrade: a modest vertex-TB IPR /
multifractal sketch separating E=0 from E≠0 — would be the first such data on
the hat and preempt a TB version of Daníelsson–Sigurðsson.)

**Stop signals:** a 2026 preprint doing our exact dilution+matching analysis on
Hat/Spectre (none at time of writing) → pivot framing; any new Bhola–Damle
output adding aperiodic content → revisit positioning immediately. Window is
open but the Flicker bridge (co-author on both the hat-PRL and the Penrose-dimer
PRX) means it will not stay open indefinitely — move quickly.

---

## (Superseded) earlier bottom line — yellow

Salvaged from the (crashed) deep-research run: the verification phase had
completed with 9 adversarially-verified claims (3-vote) before the final
synthesis step failed. The load-bearing "finite vs zero threshold" fact was
re-confirmed by direct WebFetch. Confidence levels marked per item.

**Yellow light.** The matching-theory ↔ zero-mode-percolation *framework* is
NOT ours to claim — the Damle group (TIFR) owns it and is actively extending
it. But it has only ever been applied to **periodic** lattices; **nobody has
done it on an aperiodic monotile**, and Franca et al.'s monotile paper does no
dilution/matching/percolation at all. So the *substrate is open*, and one of
our results — finding #4 (p_c → 0) — would be a genuine qualitative departure
from the **finite** thresholds they find on periodic non-bipartite lattices,
**if** it survives a non-proxy treatment. (Now upgraded to GREEN per the
2026-06-05 scan above: #4 is confirmed not-folklore and the niche confirmed
open; the remaining condition is the rigorous finite-size collapse, not a
literature risk.)

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
Verdict **(c) — the headline result. Novelty confirmed (2026-06-05).**
The bipartite case (2007.04974) and periodic non-bipartite case (2311.05634)
both have **finite** thresholds (WebFetch-confirmed for the latter). A genuine
p_c → 0 on the *aperiodic* monotile is a qualitative, aperiodicity-driven
difference with no found precedent. **Condition (iii) — rule out chiral-class
folklore — is now RESOLVED:** the deep-research scan establishes that p_c → 0
is a matching/Gallai–Edmonds (combinatorial support) statement, distinct from
Gade–Wegner Anderson-localization scaling (see Q1 above). **Remaining
conditions (numerics, not literature):** (i) replace the proximity-proxy
spanning with a rigorous per-mode / R-region spanning order parameter;
(ii) finite-size collapse p_c(L) ∼ L^(−1/ν) across d0 and larger L. **(ii) is
now DONE** — the completed L3 campaign (`docs/CAMPAIGN_REPORT.md`) gives an
`L→∞` intercept consistent with 0 for both transitional d0 (1.2: +0.004±0.015;
1.4: −0.005±0.015). **(i) remains** the next step before #4 is load-bearing.

## Direct competitors

- **Damle group (TIFR): Bhola, Biswas, Islam, Damle.** Own the entire
  machinery — bipartite (2022) → non-bipartite periodic (2023) → kagome
  (Dec 2025). As of Dec 2025 (2512.23639) they show **no sign** of moving to
  aperiodic substrates, but are the people most likely to do the monotile next;
  the niche is open, not safe indefinitely.
- **Grushin / Flicker / Schirmann / Franca** (monotile zero modes) could bolt
  dilution onto their own model. Their PRL 135, 236603 (Dec 2025) /
  arXiv:2505.13304 already does **on-site Anderson** disorder on a Chern
  hat-family model — the closest live work, but a different model and not
  matching/vacancy/zero-mode. Flicker bridges the hat-PRL and the
  Penrose-dimer PRX → cross-group overlap is the real competitive risk.
- **Daníelsson & Sigurðsson (Iceland/Warsaw), arXiv:2605.29023 (May 2026)** —
  multifractality of a continuum-polariton Hat; not the vertex-TB model, no
  zero-mode/matching. Owns the "hat multifractality" label for the continuum
  case; our vertex-TB IPR angle remains open.
- Classical monotile percolation (2604.21165, Gao–Bharadwaj, Apr 2026) shows
  the substrate is on radar; geometric Bernoulli, orthogonal to our quantum
  question.

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

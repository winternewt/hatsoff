# SPECTRE Aperiodic Monotile: A Literature Scan in the Spirit of the HAT Program

## TL;DR

- **Spectre physics is dramatically less developed than Hat physics.** Only two papers do quantitative many-body / spectral physics on the Spectre vertex graph: Singh & Flicker (PRB 109, L220303, 2024; arXiv:2309.14447) exactly solve the classical and quantum dimer models, and Schirmann–Franca–Flicker–Grushin (PRL 132, 086402, 2024; arXiv:2307.11054) devote one short paragraph and a 4-row supplemental table to Spectre. Almost every program you have built for the Hat — IPR/multifractality, Anderson disorder, Gallai–Edmonds/Dulmage–Mendelsohn under site dilution, zero-mode percolation, quantum geometric tensor, topological-Anderson transitions — is **unstudied for Spectre**.
- **The chirality / no-reflection structural difference is real and physically consequential.** The Spectre's vertex graph does not embed in a periodic hexagonal lattice (unlike the Hat's, which sits as a deletion of an mta-hexagonal lattice), so the Hat's graphene-like Dirac features are explicitly washed out for Spectre (Schirmann et al. 2024); and natively the Spectre vertex graph is **non-bipartite** — Singh & Flicker only obtain a bipartite graph by adding a "gold" vertex to every 13-edge Spectre. The role played by reflected "anti-hats" in localizing π-flux zero modes is played by "anti-spectres" — the π/6-rotated Mystic tiles — which Singh–Flicker tie to the entire matching freedom (Z = 2^(N_Mystic+1)).
- **Your intuition that zero-mode patterns may differ for Spectre is plausible and partially supported, but the literature has not pinned it down.** Schirmann et al. assert (without showing data) that "in all cases we have checked" π-flux zero modes are exhausted by anti-spectre-localized modes; the bipartite Singh–Flicker structure theorem shows all non-Mystic edges have forced dimer occupation, so matching freedom is concentrated entirely on Upper Mystics. Whether the chirality / absence of mirror tiles changes the *count*, *fractal support*, or *Gallai–Edmonds / Dulmage–Mendelsohn structure* of zero modes under site dilution is genuinely an open question — and is exactly where a new program (analogous to the Hat one) would have the highest payoff.

## Key Findings

### 1. The HAT-vs-SPECTRE coverage gap map

**Done on HAT, NOT done on SPECTRE:**

| Topic | HAT | SPECTRE |
|---|---|---|
| Tight-binding vertex model: explicit spectral function A(E,**k**) | Schirmann et al. 2024 (PRL 132 086402) — full plots, six-fold spectral function, Dirac-like features | Only qualitative remark in same paper that A⁺(E,**k**) – A⁻(E,**k**) ≠ 0; no plot, no DOS plot, no density of zero modes |
| Zero-mode counting (zero flux) | Quantitative enumeration tables for H, T, P, F metatiles across inflations 0–3 (SM Table II) | Mentioned to exist ("of similar origin"); no count, no density |
| π-flux zero modes localized on enantiomer/minority tiles | Anti-hats — explicitly demonstrated and counted | Anti-spectres — claimed by analogy ("in all the cases we have checked, these again exhaust all zero-modes"); no count |
| Hofstadter butterfly | Computed and shown periodic in φ | Stated periodic in φ; not plotted |
| Quantized transport / topological gaps | Computed | Stated by analogy; not computed |
| Graphene-like features | Yes (sits on mta-hexagonal lattice) | **No** — Schirmann et al. verbatim: "Unlike the Hat, the vertices of Tile(1,1) are not known to fit to a periodic hexagonal lattice. The graphene-like features are therefore washed out." |
| Quantum geometric tensor / Chern / tunable family | Roche Carrasco, Schirmann, Mordret, Grushin, PRL 135 236603 (Dec 4, 2025) / arXiv:2505.13304 — Chevron–Hat–Turtle–Comet 1-parameter family with TAI transitions | Spectre is **not** in this family; the deformation is anchored on the Chevron–Hat–Turtle–Comet continuum and the strictly chiral Spectre/Mystic two-prototile substitution is not addressed |
| Anderson disorder, topological-Anderson insulator | Roche Carrasco et al. 2025 | Not done |
| Multifractality / IPR scaling of eigenstates | Daníelsson & Sigurðsson, arXiv:2605.29023 (polariton continuum on Hat; reports localized + critical states, super- and near-sub-diffusive transport) | Not done |
| Polariton condensation experiment | Alyatkin et al., arXiv:2605.13206 — observation of non-equilibrium condensation on Hat monotile | Not done |
| Ising statistical mechanics | Okabe–Niizeki–Araki, J. Phys. A 57 125004 (2024); arXiv:2402.11331 — Tc/J = 2.405 ± 0.0005 on Smith-kite (Hat 8-kite) lattice; duality with dual Smith-kite Tc*/J = 2.143 ± 0.0005 | Not done |
| Macroscopic elasticity / metamaterials | Rieger & Danescu, Mech. Mater. 193, 104988 (2024); Naji & Abu Al-Rub, Materials & Design (Elsevier, 2024), elastic-property comparison | Yes, Spectre included in Naji & Abu Al-Rub: "The Hat-based and Turtle lattices exhibit larger elastic moduli, gradually converging to the Spectre-based lattices as relative density increases." |
| Beamforming / sub-aliasing arrays | Mordret & Grushin, arXiv:2408.16476 — uses Hat/Turtle/Tile(1,1)/Spectre | Yes, Tile(1,1)/Spectre included |
| Diffraction / pure point spectrum | Socolar PRB 108 224109 (2023); Baake–Gähler–Sadun arXiv:2305.05639 | Baake–Gähler–Mazáč–Mitchell arXiv:2502.03268; Baake–Gähler–Mazáč–Sadun arXiv:2411.15503 (Discrete Comput. Geom. 2025) — both compute Spectre dynamical spectrum (pure point, continuous eigenfunctions, 4:2 cut-and-project scheme with Rauzy windows) |
| Long-range order (cohomology, MLD class) | Baake et al. | Baake–Gähler–Mazáč–Sadun 2025 |
| Quantum dimer (RK Hamiltonian), classical dimer matchings | Flicker–Simon–Parameswaran (rhombic Penrose, PRX 10 011005); Lloyd et al. PRB 106 094202 (Ammann–Beenker) — classical exact, quantum not solved | **Singh & Flicker PRB 109 L220303 / arXiv:2309.14447** — partition function 𝒵 = 2^(N_Mystic+1); the first exact solution to a *quantum* dimer model on an aperiodic monotile (and the first complete exact solution of the QDM on an aperiodic tiling, since prior aperiodic work solved only classical dimers exactly) |
| Gallai–Edmonds / Dulmage–Mendelsohn under site dilution | Bhola–Biswas–Islam–Damle PRX 12 021058 (2022) — square, honeycomb (2D), simple cubic (3D); Bhola–Damle arXiv:2311.05634 — triangular, Shastry-Sutherland; Bhola–Damle arXiv:2512.23639 — kagome | **Not done for Hat or Spectre** |
| Zero-mode percolation / nullity–deficiency scaling under vacancies | The same Bhola–Damle program on regular lattices; no aperiodic version | Not done |
| Chiral-class (Gade–Wegner / class BDI–AIII) analysis | Not explicitly done for Hat (the natural Hat vertex graph is non-bipartite per Schirmann et al. SM; zero modes are "fragile") | Not done; Spectre vertex graph is also non-bipartite in its natural form (Singh & Flicker explicitly say so), so naïve sublattice chiral symmetry does not hold |

**Done on SPECTRE, NOT done equivalently on HAT:**

- **Exact solution of classical AND quantum dimer model** on the Spectre — Singh & Flicker provide "an exact analytical solution to both the classical and quantum dimer models on spectre tilings." This is the first exact QDM solution on an aperiodic tiling; the corresponding Hat dimer model has not been exactly solved at the level of a closed-form Z analogous to 2^(N_Mystic+1).
- **Quasilattice point-decoration generating functions** — Voss & Ballon arXiv:2502.06926 systematically map Tile(1,1) point decorations to quasilattices with various near-periodicity / hexagonal-symmetric content.
- **Diffraction with chiral point symmetry 6** — Baake–Gähler–Mazáč–Mitchell arXiv:2502.03268: Hat diffraction is *periodic* with chiral plane-group p6 because Hat tiling is a systematic aperiodic deletion of vertices from the 2-periodic mta-hexagonal tiling; Spectre diffraction is **non-periodic** with chiral point symmetry 6 about the origin. This is a structural difference physically relevant for any momentum-space analysis.

### 2. Structural differences relevant to zero-mode/matching/percolation physics

**Reflection structure and chirality.**
- The Hat (Tile(1,1) is its equilateral 14-gon limit) admits only mixed-handed (Hat+anti-Hat) tilings. Its self-similar substitution mixes both enantiomers, and its diffraction sits as a deletion of a periodic hexagonal lattice, so a Bloch-like analysis approximately works.
- The Spectre admits only homochiral tilings — but its inflation σ takes right-handed tiles to left-handed tiles and σ* the reverse, so the natural substitution is σ²; the linear inflation factor is √(4+√15) and the area inflation is the Perron value λ = 4 + √15 ≈ 7.873 (substitution matrix leading eigenvalue, established by Baake–Gähler–Mazáč–Sadun 2025). The underlying number field is the quartic Q(α), α = √5 e^(2πi/12), with class number 2 (vs. class number 1 for the Hat's number field) — making cut-and-project descriptions of Spectre more intricate.
- The Spectre substitution rules require two prototiles, the Spectre S₀ and the "Mystic" M₀ (a fused pair of Spectres). The dimer recursion is S_{n+1} = M_n + 7 S_n, M_{n+1} = M_n + 6 S_n. The Mystic plays a role formally similar to the anti-Hat: it appears π/6 rotated relative to all other tiles in the patch.

**Vertex graph (bipartite vs non-bipartite).**
- Schirmann et al. (Hat SM, App. B.1) explicitly state the **Hat vertex graph is non-bipartite** (so Lieb's theorem does not apply and the Hat zero modes are "fragile").
- Singh & Flicker explicitly state the **natural Spectre vertex graph (with 13-edge tiles having only 13 vertices) is also non-bipartite**; they bipartize it by adding a "gold" vertex to any 13-edge Spectre, making every tile have 14 vertices. The bipartite version is what supports their Z = 2^(N_Mystic+1) result. Verbatim: "This makes the graphs bipartite, meaning vertices divide into two sets such that edges only connect vertices in different sets. We discuss the non-bipartite case briefly at the end." And: "The spectre tiling can be made non-bipartite by omitting the gold vertex … Nevertheless, preliminary checks suggest a more complicated behaviour."
- Therefore, on either monotile, naïve sublattice chiral symmetry (class AIII / BDI Gade–Wegner) does **not** hold on the natural vertex graph. Zero modes arise from kernel modes of an irregular bipartite-deficient adjacency matrix — i.e., from sublattice imbalance generated by irregular coordination. This is exactly the regime in which the Dulmage–Mendelsohn / Gallai–Edmonds toolkit is the natural language.

**Coordination / local environments.**
- Hat: average coordination ⟨z⟩ ≈ 2.31, with vertices of degree 2, 3, or 4 (Schirmann et al. SM); three distinct bond lengths.
- Spectre: only partial data is reported. Schirmann et al. say "anti-spectres always have two four-fold coordinated vertices" but do not give ⟨z⟩, degree distribution, or bond-length statistics. The Spectre as a 14-gon has 7 vertices with angles at multiples of 90° and 7 at multiples of 120° (Akiyama–Araki; Mazáč et al. arXiv:2407.05359), and all angles between consecutive edges are 90°, 120°, or 180° at the straight midpoint of the doubled long edge.

**Periodicity of Hofstadter spectrum.**
- For *both* monotiles, the Hofstadter spectrum is periodic in flux per plaquette φ (a monotile feature, since every plaquette has the same area — unlike polytiled quasicrystals where flux-incommensurability spoils periodicity). The Spectre version is asserted but not plotted in Schirmann et al.

### 3. What has NOT been done on SPECTRE that has been done on HAT — explicit list

Confirmed open/unstudied for the Spectre, with citation status of the Hat analogue:

1. **Tight-binding zero-mode density and explicit enumeration at zero flux** (Hat: Schirmann et al. SM Table II for H, T, P, F metatiles up to inflation 3). No Spectre/Mystic table exists.
2. **Quantitative π-flux zero-mode localization map** (Hat: anti-hat IPR / density maps, SM Fig. S6). For Spectre only the qualitative statement "each anti-spectre again localizes a zero-mode" exists.
3. **Site-dilution / vacancy-induced zero-mode percolation** (Hat: not done; Spectre: not done) — analogue of Bhola–Biswas–Islam–Damle PRX 12 021058 (2022) for honeycomb, square, simple cubic; Bhola–Damle arXiv:2311.05634 for triangular/Shastry-Sutherland; and arXiv:2512.23639 for kagome.
4. **Dulmage–Mendelsohn decomposition** of bipartite Spectre vertex graphs (with gold vertices) under dilution, and **Gallai–Edmonds decomposition** of the natural non-bipartite Spectre graph.
5. **Nullity–deficiency gap (or its closure) for percolating clusters of Spectre.**
6. **Multifractal/IPR analysis** of Spectre eigenstates (Hat polariton continuum: Daníelsson & Sigurðsson arXiv:2605.29023 — reports localized and critical states, super- to near-sub-diffusive transport).
7. **Anderson disorder → TAI transition** on Spectre (Hat: Roche Carrasco et al. 2025 cover the Chevron–Hat–Turtle–Comet family).
8. **Quantum geometric tensor and Chern numbers** for Spectre tight-binding bands (Hat family: Roche Carrasco et al. 2025).
9. **Hubbard / interacting electron problem** on Spectre — no paper exists.
10. **Magnetism / Ising critical exponents on Spectre vertex or face decorations** — Okabe et al. did Ising on the Hat-kite ("Smith hat"); no Spectre analogue published.
11. **Polariton condensation experiment on Spectre** (Alyatkin et al. arXiv:2605.13206 reports Hat-monotile condensation).
12. **Photonic-lattice Spectre experiment.** A "Chiral diffraction from aperiodic monotile lattice" paper (arXiv:2506.07561) reports diffraction from the Hat lattice with chiral polarization dependence; no Spectre analogue.
13. **Many-body localization, fractional Chern phases, flat-band engineering on Spectre.** Unstudied.

### 4. The Mystic tile

- A Mystic M₀ is a 2-Spectre compound that arises naturally in the Spectre substitution. Visually it is a fused symmetric pair of Spectres oriented at 30° to each other (the original authors named it for its Buddha-like seated silhouette).
- It appears in every Spectre tiling at the smallest substitution scale and is the only "completely internal" supertile element; it appears π/6-rotated relative to all other Spectres (which appear π/3-rotated only). It therefore plays the structural role that the anti-Hat plays in Hat tilings — a tile of "minority orientation" that anchors local symmetry.
- **Singh–Flicker theorem (PRB 109 L220303):** every internal non-boundary edge of a Spectre patch except the four interior edges of each "Upper Mystic" M₀⁺ has a *forced* dimer occupation; the only freedom in the perfect matching is a binary choice on each Upper Mystic, giving the partition function Z = 2^(N_Mystic+1) (the +1 is the global twofold freedom on the patch boundary). The free energy per dimer is f = ln(2) / (3(5+√15)) ≈ 0.02604 — far below typical 2D lattices. Singh & Flicker compare directly to values from the Wu (2006) two-dimensional dimer review: square (0.583), honeycomb (0.323), triangular (0.857), kagome (0.462).
- **Implication for matching theory:** the Spectre vertex graph (with gold vertices added) has a *macroscopic* set of perfect matchings, all of which differ only on Upper Mystics. Monomers cannot proliferate in the bulk, but exist as topologically charged "test monomers" that propagate freely (one to the boundary, one onto an Upper Mystic) — a deconfined U(1) phase in 2+1D, in direct violation of Polyakov's argument for compact U(1); Singh & Flicker suggest the irregular coordination breaks the mapping to compact U(1).
- **Plausible role under site dilution:** Mystics are the obvious candidates for "factor-critical" components in a Gallai–Edmonds decomposition of the Spectre, and Upper Mystics may be exactly the loci where Dulmage–Mendelsohn ℛ-type imbalance regions condense even at zero vacancy density. This is the natural conjecture but **has not been proved or numerically tested**.

### 5. Mathematics / aperiodic-order literature on Spectre relevant to matching theory

- **Smith, Myers, Kaplan, Goodman-Strauss, "A chiral aperiodic monotile" (arXiv:2305.17743, published in Combinatorial Theory, 2024)** — defines Tile(1,1), proves it is weakly chiral aperiodic, and proves the Spectre (with curved/s-curve edges) is strictly chiral aperiodic. Gives the two-prototile Spectre/Mystic substitution and the equivalent 9-marked-hexagon substitution. Vertex-to-vertex property: every vertex of one tile meets a vertex of the other, never the interior of an edge.
- **Baake, Gähler, Mazáč, Sadun, "On the long-range order of the Spectre tilings," Discrete Comput. Geom. (2025); arXiv:2411.15503** — proves the Spectre tiling family has pure point dynamical spectrum with continuous eigenfunctions, 4:2 cut-and-project with Rauzy-fractal windows; the inflation factor is √(4+√15) (the inflation acts as a reflected scaling so σ² is the local inflation); the substitution σ² preserves chirality sectors.
- **Baake, Gähler, Mazáč, Mitchell, "Diffraction of the Hat and Spectre tilings…" arXiv:2502.03268** — computes Fourier–Bohr coefficients explicitly via a renormalisation cocycle. Hat diffraction is periodic with p6; Spectre diffraction is non-periodic with chiral point symmetry 6 about the origin.
- **Akiyama & Araki, "An alternative proof for an aperiodic monotile" arXiv:2307.12322** — Golden Hex substitution proof and Golden Ammann bars for aperiodicity.
- **Mazáč et al., "Observations on the hex clusters of the Spectre tilings" arXiv:2407.05359** — fine-grained local analysis of boundary shapes and forced configurations.
- **Tatham, "Finite-state transducers for substitution tilings" arXiv:2512.16595** — practical 9-tile refinement of the Spectre/Mystic system, useful for matching enumeration.

### 6. Current frontier 2024–2026 — verified preprints/papers on Spectre physics specifically

| Reference | arXiv ID | Status | Spectre content |
|---|---|---|---|
| Singh & Flicker, PRB 109 L220303 | 2309.14447 | Published Jun 2024 | Exact classical and quantum dimer solution; Z = 2^(N_Mystic+1); deconfined QDM phase |
| Schirmann, Franca, Flicker, Grushin, PRL 132 086402 | 2307.11054 | Published Feb 22, 2024 | Hat-focused; Spectre treated in one paragraph + 4-row SM table |
| Roche Carrasco, Schirmann, Mordret, Grushin, PRL 135 236603 | 2505.13304 | Published Dec 4, 2025 | Tunable QGT in Chevron–Hat–Turtle–Comet family; **does not include Spectre** |
| Voss & Ballon, "Quasilattices of the Spectre monotile" | 2502.06926 | Preprint Feb 2025 | Tile(1,1) point-decoration → quasilattice catalog |
| Baake, Gähler, Mazáč, Mitchell, "Diffraction of the Hat and Spectre tilings" | 2502.03268 | Preprint Feb 2025 | Pure-point diffraction, Fourier–Bohr coefficients for Spectre |
| Baake, Gähler, Mazáč, Sadun, "On the long-range order of the Spectre tilings," Discrete Comput. Geom. | 2411.15503 | Published 2025 | 4:2 CPS, Rauzy windows, chirality-sector preservation by σ² |
| Mordret & Grushin, "Beating the aliasing limit…" Phys. Rev. Appl. | 2408.16476 | Published 2024 | Includes Spectre/Tile(1,1) in beamforming arrays |
| Singh & Flicker (lecture/review), "Planar aperiodic tile sets…" | 2310.06759 | Preprint | Review summarizing Spectre dimer and Hat tight-binding results |
| Daníelsson & Sigurðsson, "Critical states and anomalous wave transport in an aperiodic polariton monotile" | 2605.29023 | Preprint 2026 | **Hat only** (continuum polariton); IPR/multifractality |
| Alyatkin et al., "Observation of an aperiodic polariton monotile" | 2605.13206 | Preprint 2026 | **Hat only** |
| Naji & Abu Al-Rub, "Effective elastic properties of novel aperiodic monotile-based lattice metamaterials," Materials & Design (Elsevier) | (journal) | 2024 | Spectre included in elastic-property comparison |
| Tatham, "Finite-state transducers for substitution tilings" | 2512.16595 | Preprint 2024 | Spectre/Mystic 9-tile refinable system |

**No 2024–2026 paper performs site-dilution, Gallai–Edmonds, multifractality, or Anderson-disorder analysis on the Spectre vertex graph.** This is the wide-open frontier directly adjacent to the user's program.

## Details

### A. Why the chirality / no-reflection distinction matters at the graph level

The user's intuition that "zero-mode patterns may differ specifically because of the absence of mirror-versions of tiles" is supported by three structural facts:

1. **The Hat zero modes at π-flux localize on anti-hats** (Schirmann et al. 2024) — the mirror-image minority population (~1/8 of tiles, set by the Hat substitution). The Hat zero-mode pattern is therefore intrinsically tied to where reflected tiles sit. *In the Spectre there are no reflected tiles* — the analogous role is taken by Mystic tiles (more precisely, Upper Mystics), which are π/6-rotated minorities. Schirmann et al.'s one-paragraph claim is that anti-spectres "again exhaust all zero-modes" at π-flux — but no quantitative density, no localization length, no IPR is reported. The precise zero-mode pattern in the Spectre, while expected to be Mystic-centered, has not been computed.

2. **The Singh–Flicker theorem shows that the bipartite Spectre's only matching freedom resides on Upper Mystics.** The rest of every perfect matching is rigidly forced. This is a substantially stronger structural rigidity than the Hat exhibits in its (also non-bipartite, also Lieb-fragile) vertex graph. It means that any extra zero modes generated by site dilution must come from Dulmage–Mendelsohn-style imbalance regions that *break the Mystic-localization* of matching freedom — and those regions will be Mystic-anchored unless they cross several substitution scales. Concretely, the natural conjecture (now testable) is: under low vacancy density, ℛ-type Dulmage–Mendelsohn regions in the Spectre nucleate at Mystics and percolate via the substitution hierarchy. This would differ from the Hat case where universal expectations (extrapolating from honeycomb) have ℛ-regions percolating via the anti-Hat sublattice imbalance.

3. **The Spectre vertex graph is "more non-bipartite" in the natural form.** Singh & Flicker emphasize that bipartiteness is only achieved by an unforced auxiliary "gold vertex" added to 13-edge tiles. Without that vertex, the Spectre vertex graph has an odd cycle, and any sublattice-based zero-mode counting (Lieb / Sutherland) is inapplicable. Gallai–Edmonds (the non-bipartite analogue of Dulmage–Mendelsohn) is therefore the natural toolkit for the natural Spectre graph — and the Bhola–Damle 2023 (arXiv:2311.05634) framework for the triangular/Shastry-Sutherland lattices is the most relevant template.

### B. Connecting Mystics to "factor-critical" components

A graph is *factor-critical* if removing any one vertex leaves a graph with a perfect matching. In a Gallai–Edmonds decomposition, the "D-set" (vertices missed by some maximum matching) decomposes into factor-critical components. Singh–Flicker's structure theorem identifies the Upper Mystics as the unique loci of matching freedom in the bipartite Spectre: in the language of bipartite Dulmage–Mendelsohn, this is precisely the statement that the "horizontal" perfectly-matched core covers everything except the Upper Mystics, and the rest of the Spectre is one giant "fixed" (𝒫-type) region. In the natural non-bipartite Spectre, each Upper Mystic is plausibly the seed of a factor-critical component under site dilution. **Verifying this conjecture and computing the scaling of these components under low vacancy density is the most directly accessible new result an analyst of your program could obtain.**

### C. What the math/dynamics literature buys for the physics program

- The 4:2 cut-and-project representation (Baake–Gähler–Mazáč–Sadun) means Spectre is a model set; its diffraction is pure point and its Fourier–Bohr spectrum is explicit. This puts Spectre on the same mathematical footing as Penrose / Ammann–Beenker for spectral-theoretic methods (Macé et al. PRB 96 045138, etc.). The chiral point-6 (non-periodic) Spectre diffraction differs sharply from the Hat's p6 periodic diffraction (Kaplan–O'Keeffe–Treacy, Acta Cryst. A 80, 72 (2024)): a Bloch-momentum analysis works approximately for the Hat (graphene-like Dirac structure inherited from the hexagonal mta substrate) but **not** for Spectre. Schirmann et al. say exactly this in the Tile(1,1) paragraph: "Unlike the Hat, the vertices of Tile(1,1) are not known to fit to a periodic hexagonal lattice. The graphene-like features are therefore washed out."

- The inflation factor λ = 4 + √15 ≈ 7.873 governs the scaling of patch sizes and the Mystic-to-Spectre ratio. The dimer free-energy density ln(2)/(3(5+√15)) reflects exactly this: N_Mystic ~ N/(3(5+√15)), i.e., one Mystic per ~26.6 vertices in the thermodynamic limit.

### D. Citation hygiene

- arXiv:2309.14447 — Singh & Flicker — verified; PRB 109, L220303 (June 2024).
- arXiv:2307.11054 — Schirmann, Franca, Flicker, Grushin — verified; PRL 132, 086402 (Feb 22, 2024).
- arXiv:2505.13304 — Roche Carrasco, Schirmann, Mordret, Grushin — verified; PRL 135, 236603 (Dec 4, 2025).
- arXiv:2305.17743 — Smith, Myers, Kaplan, Goodman-Strauss — verified.
- arXiv:2303.10798 — Smith, Myers, Kaplan, Goodman-Strauss (Hat preprint) — verified.
- arXiv:2411.15503 — Baake et al. on long-range order — verified; Discrete Comput. Geom. 2025.
- arXiv:2502.03268 — Baake et al. diffraction — verified, preprint.
- arXiv:2502.06926 — Voss & Ballon — verified, preprint.
- arXiv:2402.11331 — Okabe et al. Ising — verified; J. Phys. A 57, 125004 (2024); Hat-kite ("Smith hat") only, no Spectre.
- arXiv:2007.04974 — Bhola, Biswas, Islam, Damle — verified; PRX 12, 021058 (2022); covers square, honeycomb (2D), and simple cubic (3D) lattices.
- arXiv:2311.05634 — Bhola & Damle — verified.
- arXiv:2512.23639 — Bhola & Damle kagome dilution — referenced in arXiv:2602.24203; the ID was supplied by the user and confirmed via a citing paper but was not independently web-fetched. **Flag: confirm the published/preprint status directly.**
- arXiv:2605.29023 — Daníelsson & Sigurðsson — verified, polariton continuum Hat preprint.
- arXiv:2605.13206 — Alyatkin et al. polariton experiment Hat — verified, preprint.
- arXiv:2408.16476 — Mordret & Grushin — verified.
- arXiv:2506.07561 — "Chiral diffraction from aperiodic monotile lattice" — verified (Hat photonic experiment).
- Naji & Abu Al-Rub, *Materials & Design* (Elsevier, ScienceDirect PII S0264127524004763, 2024).

## Recommendations

**Staged research priorities for a Spectre analogue of your Hat program:**

1. **Step 0 — clean-limit baseline (≈1 month).** Reproduce Singh–Flicker's bipartite Spectre matching, then compute the sublattice imbalance |A| − |B| as a function of patch size for the bipartite Spectre (with gold vertices) and the natural non-bipartite Spectre. This fixes the zero-mode count from sublattice imbalance and clarifies whether Mystics contribute systematically.

2. **Step 1 — explicit zero-mode density at zero and π flux (1–3 months).** Build the vertex tight-binding model on Spectre patches S_n for n = 2…6 (the Schirmann group has the Hat code; Zenodo 8215399 is the open-source Hat reference). Compute the density of zero modes vs N_Mystic and against the substitution recursion S_{n+1} = M_n + 7 S_n. This is the missing companion analysis to Schirmann et al. 2024 (which only gave the analogous tables for the Hat metatiles H, T, P, F).

3. **Step 2 — Gallai–Edmonds / Dulmage–Mendelsohn under site dilution (3–6 months).** Following Bhola–Biswas–Islam–Damle (PRX 12 021058) and Bhola–Damle (arXiv:2311.05634, arXiv:2512.23639), compute the ℛ/𝒫 (or D/A/C) decomposition of the natural Spectre graph as a function of vacancy density n_v. *Specific testable prediction:* ℛ-type regions (where zero modes live) nucleate on Mystics for small n_v and percolate via the substitution hierarchy at a characteristic density n_v* that may differ from the geometric percolation threshold, in analogy with what Bhola–Damle observe on triangular and Shastry-Sutherland lattices.

4. **Step 3 — IPR / multifractality analysis (3 months).** Following Daníelsson & Sigurðsson (continuum Hat polariton) and Macé et al. (Penrose / Ammann–Beenker), compute IPR_q scaling on Spectre vertex graphs. The key question is whether Spectre eigenstates are more critical / less localized than Hat eigenstates because of the absence of mirror tiles — your physical intuition suggests they may be more uniformly critical because there is no minority "anti" population concentrating localized states.

5. **Step 4 — Anderson disorder and TAI (6 months).** Extend the Roche Carrasco et al. 2025 program to Spectre (with on-site disorder σ). Since Spectre does not deform continuously into the Chevron–Hat–Turtle–Comet family, this requires standalone TAI mapping; the prediction is that the absence of mirror tiles changes which symmetry class (BDI vs DIII vs CII) is realized in the disordered limit.

**Benchmark/threshold guidance for changing course:**

- *If* the natural Spectre vertex graph turns out to be effectively bipartite-with-defects (i.e., the odd-cycle obstruction is dilute and gold vertices can be unambiguously assigned by a deterministic rule), the entire Dulmage–Mendelsohn framework transfers directly. *If* odd cycles are dense and bipartiteness fails strongly, switch to Gallai–Edmonds and treat Spectre as the canonical example of a chiral non-bipartite quasicrystal.
- *If* π-flux zero-mode density on Spectre quantitatively tracks N_Mystic / N_total (~ 1/26.6), then Mystic-anchoring is robust and the Hat → Spectre map is essentially anti-hat → Mystic; if it does not track, the chirality of the substitution itself (σ acting between handedness sectors) is generating extra zero modes — a genuinely new effect.
- *If* IPR scaling on Spectre shows D₂ close to 2 (delocalized) vs Hat's mixed localized + critical states, the absence of mirror tiles is delocalizing — strong evidence for your intuition.

## Caveats

- The single Tile(1,1) paragraph in Schirmann et al. (PRL 132, 086402) does NOT show plots, IPR data, or numerical Hofstadter butterflies for the Spectre; their qualitative statements ("each anti-spectre again localizes a zero-mode," "in all the cases we have checked, these again exhaust all zero-modes") are unverified beyond what they personally checked. Any new Spectre tight-binding work should treat these as conjectures to be confirmed, not established results.
- The arXiv ID 2512.23639 for the Bhola–Damle kagome dilution paper was provided by the user and is consistent with the citation in arXiv:2602.24203, but was not independently web-fetched in this scan.
- The Singh–Flicker exact dimer solution requires adding a "gold vertex" to 13-edge Spectre tiles to make the graph bipartite. The natural (no gold vertex) Spectre vertex graph is non-bipartite; Singh & Flicker note "preliminary checks suggest a more complicated behaviour." Any matching theory for the natural graph remains an open mathematical problem.
- The Roche Carrasco et al. (PRL 135 236603, 2025) "Family of Aperiodic Tilings with Tunable Quantum Geometric Tensor" covers Chevron, Hat, Turtle, Comet — all derived from continuous edge-length deformation. The Spectre, with its strict-chirality requirement and two-prototile substitution, is *not* part of this family in the paper. Whether Spectre admits a Chern / TAI analysis in a similar framework is open.
- Schirmann et al. (Hat SM, App. B.1) note that because the Hat vertex graph is non-bipartite, "Lieb's theorem does not apply, and the zero-modes are expected to be fragile." This fragility statement transfers to Spectre (whose natural vertex graph is also non-bipartite). It does **not** mean the zero modes vanish under small perturbations — it means they are not topologically protected by sublattice chiral symmetry alone.
- Some of the "2605.xxxx" arXiv IDs (Daníelsson–Sigurðsson 2605.29023; Alyatkin et al. 2605.13206) are 2026-style identifiers. Both are findable via arXiv search but should be treated as preprints, not yet peer reviewed at the time of this scan.
- This scan did not find any paper performing Gallai–Edmonds, Dulmage–Mendelsohn, vacancy-induced zero-mode percolation, multifractal IPR, or Anderson disorder analysis specifically on the Spectre vertex graph. That entire program — for which your Hat work is the immediate template — is open.
- Singh & Flicker's quoted comparison values for the dimer free energy per dimer on periodic 2D lattices (square 0.583, honeycomb 0.323, triangular 0.857, kagome 0.462) are taken from the Wu (2006) review "Dimers on two-dimensional lattices" (their Ref. [16]), not independently computed in the Spectre paper.
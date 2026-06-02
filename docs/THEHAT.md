# The Hat Lattice — A Research Program

*From mathematical curio to physical material, with a weekend project at the bottom.*

---

## The big picture

The hat (Smith, Myers, Kaplan, Goodman-Strauss, 2023) is the first true aperiodic monotile — a single shape that tiles the plane only non-periodically. It sits in a continuous family with the turtle and the chiral spectre. The mathematical novelty is settled. What's open is whether a *physical realization* of the hat lattice — most plausibly a 2D covalent heteroaromatic framework — can be made, and whether such a material would have genuinely new physics or just be aesthetic.

Three predicted properties make it more than a curio:

1. **Periodic Hofstadter spectrum in magnetic flux** — unique among quasicrystals
2. **Macroscopically degenerate flat band of zero modes** — a candidate platform for aperiodic correlated phases
3. **Hexagonal quasiperiodicity locked to the golden mean** — diffraction signature on a ℤ[φ]-module of rank 4

The realistic outcome distribution is bimodal: most likely a beautiful aperiodic 2D covalent framework with modest applications; non-trivial chance of a quantum anomalous Hall material or flat-band superconductor.

---

## The pipeline

```
[1] Math layer          [2] Theory layer        [3] Design layer
substitution rules  →   tight-binding /     →   molecular target
inflation matrices      DFT / phonons           heteroatom partition
diffraction theory      magnetotransport        edge-matching graph
                                                       │
                                                       ▼
[6] Characterization  ←  [5] On-surface       ←  [4] Synthesis
XRD, STM, transport      polymerization           PAH chemistry
phason analysis          Au(111)/Cu(111)          B-N, C-N, C-P
                         registration sub.        orthogonal coupling
```

Each stage prunes the candidate space. Stages 1–2 are pure desk work; stages 3–4 need synthetic chemistry; stages 5–6 need a surface-science lab.

---

## Names and groups worth contacting

**Mathematics / tiling theory**

- *Craig Kaplan* (Waterloo) — co-discoverer, maintains reference code and SVG tooling
- *Joseph Myers* (Trinity, Cambridge) — proof author, deepest structural understanding
- *Chaim Goodman-Strauss* (MoMath / Arkansas) — public-facing author, broad tilings expertise
- *Joshua Socolar* (Duke) — quasicrystal structure of hat tilings, ℤ[φ] connection
- *Michael Baake / Uwe Grimm* — *Aperiodic Order* (CUP, 2 vols), the standard reference for diffraction theory of aperiodic systems

**Physics / topological matter**

- *Selma Franca / Adolfo Grushin* (Grenoble) — hat tight-binding, Hofstadter prediction, zero modes
- *Jean Bellissard* — gap labelling theorem, K-theory of tilings
- *Johannes Kellendonk* — substitution C*-algebras
- *Roderich Moessner* (MPI-PKS Dresden) — flat-band physics, frustrated magnetism on quasicrystals

**Synthetic chemistry**

- *Holger Bettinger* (Tübingen) — BN-doped PAH synthesis
- *Takuji Hatakeyama* (Kwansei Gakuin) — selective BN substitution in nanographenes
- *Kazunori Itami* (now CRO Nagoya) — warped nanographenes, non-planar PAH
- *Klaus Müllen* / *Akimitsu Narita* (OIST) — large PAH synthesis, nanographene polymerization
- *Xinliang Feng* (Dresden) — 2D-COFs, on-surface polymerization

**Surface science / STM**

- *Roman Fasel* (Empa Zürich) — on-surface synthesis, atomically precise nanostructures
- *Leonhard Grill* (Graz) — molecular self-assembly on metal surfaces
- *Stefan Förster* (Halle) — quasicrystal growth on periodic substrates

**Quantum optimization (for the QUBO sub-problem)**

- *Catherine McGeoch* (D-Wave) — annealer benchmarking
- *Andrew King / Murray Thom* (D-Wave) — materials partnerships

---

## Implications to explore

**Settled (publishable from theory alone)**

- Exact zero-mode count by Lieb's theorem on hat tight-binding graphs
- Multifractal analysis of zero-mode wavefunctions in the hat family
- Phonon density of states and localized vibrational modes at golden-ratio frequencies
- ℤ[φ]-module diffraction theory: explicit Fourier intensities for the H/P/T/F substitution
- Mean-field Hubbard at half-filling: aperiodic magnetic ground state

**Speculative (high-risk, high-reward)**

- Quantum anomalous Hall at zero field via spin-orbit coupling from heavy heteroatoms
- Flat-band superconductivity — first quasicrystal candidate with macroscopic degeneracy
- Quasiperiodic thermoelectrics with matched electron-phonon length scales
- Galois action (φ ↔ 1−φ) as a constraint on physical observables — modest, not "new quantum number"
- Self-tuning catalysis on aperiodic active-site distributions (Sabatier-principle smoothing)

**Engineering-adjacent (mechanical metamaterials, already partly demonstrated)**

- Isotropic elastic moduli with anisotropic Poisson's ratio (Mizzi et al. 2024)
- Zero Poisson's ratio over a wide density range (Tan et al. 2023)
- Impact mitigation via aperiodic ordering (semi re-entrant einstein lattice)

---

## Papers to dig into

**The discovery papers**

- Smith, Myers, Kaplan, Goodman-Strauss. *An aperiodic monotile.* Combinatorial Theory 4 (2024). arXiv:2303.10798
- Same authors. *A chiral aperiodic monotile.* arXiv:2305.17743

**Structure**

- Socolar. *Quasicrystalline structure of the Hat monotile tilings.* arXiv:2305.01174
- Smith (J.). *Turtles, Hats and Spectres: Aperiodic structures on a Rhombic tiling.* arXiv:2403.01911

**Physics**

- Franca, Grushin, et al. *Physical properties of an Aperiodic monotile: Graphene-like features, chirality and zero-modes.* arXiv:2307.11054 — the must-read for anyone doing tight-binding on the hat

**Mechanical metamaterials**

- Tan et al. *An isotropic zero Poisson's ratio metamaterial based on the aperiodic 'hat' monotile.* Results in Materials (2023)
- Mizzi et al. *Effective elastic properties of novel aperiodic monotile-based lattice metamaterials.* Materials & Design (2024)

**Diffraction / aperiodic order**

- Baake, Grimm. *Aperiodic Order, Vol. 1: A Mathematical Invitation.* CUP (2013) — Ch. 9 covers diffraction on ℤ[φ]-modules
- Bellissard, Herrmann, Zarrouati. *Hulls of aperiodic solids and gap labeling theorems.* (2000) — for the K-theory crowd

**Adjacent: synthesis and on-surface**

- Bieri et al. *Porous graphenes: two-dimensional polymer synthesis with atomic precision.* Chem Commun (2009) — the foundational on-surface 2D polymer paper
- Hatakeyama et al. on selective multiple BN doping — search his recent JACS/ACIE output

---

## The weekend project — roll a hard 6

**Title:** *Zero-mode counting and multifractal analysis on the hat family*

**Question:** How many exact zero-energy eigenstates does the vertex tight-binding model on a hat tiling have per unit area, and how do those wavefunctions distribute spatially?

**Why it's tractable in a weekend:**

The zero-mode count is given by Lieb's theorem — it's a property of the graph, not the Hamiltonian. You count vertices on each sublattice of a bipartite hat graph and the difference is a lower bound on the zero-mode count. No quantum mechanics required for step 1; just graph theory and sparse linear algebra.

**The roll-a-hard-6 part:**

Whether the bipartite structure gives a *tight* bound (i.e., exactly the right count) or just a lower bound. If tight, you have a clean closed-form answer. If not, the gap between Lieb's bound and the actual zero-mode count is itself an interesting quantity that nobody has computed for the hat. Either outcome is publishable.

**What you'd actually do, in order:**

1. Generate a level-3 or level-4 inflation of the hat using Kaplan's open-source code (Python or JS — both exist on GitHub, search "hat tiling generator"). Output: a list of vertex coordinates and an edge list. Aim for 5,000–20,000 vertices.

2. Build the adjacency matrix as a `scipy.sparse.csr_matrix`. Sanity-check it's symmetric and has the expected average coordination number (~2.31, per Franca et al.).

3. Check bipartiteness with a 2-coloring algorithm (BFS-based). If bipartite, count |N_A − N_B|. This is your Lieb lower bound.

4. Diagonalize near zero: `scipy.sparse.linalg.eigsh(A, k=200, sigma=0)`. Count eigenvalues with |E| < 1e-10. Compare to Lieb bound.

5. For each zero mode ψ_i, compute the participation ratio P = (Σ|ψ|²)² / Σ|ψ|⁴. Plot P versus system size on a log-log scale across multiple inflation levels — the slope gives the multifractal exponent.

6. Spatially plot |ψ|² for the lowest few zero modes. Compare to Franca et al.'s prediction that they localize on anti-hat tiles.

**Stretch goal (if you have a second weekend):**

Repeat across the hat family — pick three values of (a, b) on the deformation continuum, including the equilateral spectre point. Track how the zero-mode count and localization pattern evolve. The chirality structure must reorganize as you cross the spectre point because reflections become unnecessary; whether that's smooth or has a phase-transition-like signature is open.

**What you'd need:**

Python 3, `numpy`, `scipy`, `matplotlib`, `networkx`. A laptop. Eight hours of attention.

**What you'd produce:**

A short note (5-8 pages) with: exact zero-mode count for several inflation levels, multifractal scaling exponent, spatial maps of zero modes, and either (a) confirmation of Lieb saturation or (b) measurement of the gap. Phys. Rev. B short paper or arXiv preprint level. The kind of thing where you're the second or third group on the leaderboard, not the first, but the analysis is clean and reproducible.

**Why this specifically:**

It's the cheapest way to put your hands on hat physics. The graph-theoretic part is bulletproof — Lieb's theorem is a theorem. The numerical part uses standard tools. The output is concrete numbers that feed directly into every more ambitious project downstream (Hubbard mean-field, transport, optical response). And the multifractal angle is *exactly* the kind of question that hasn't been pushed hard yet because the field is six months old.

If you do this and the multifractal scaling turns out anomalous compared to Penrose or Ammann-Beenker, that's a real result. If it's the same, that's still informative — you've shown the hat's flat band is generic for quasicrystals rather than special. Either way, you'd have walked the path from substitution rule to physical observable on a single weekend.

The result feeds back: clean zero-mode statistics → motivates the Hubbard project → motivates synthesis target choice → motivates D-Wave QUBO formulation. It's the trunk of the tree.

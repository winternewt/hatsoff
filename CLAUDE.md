# Hatsoff — Hat Tiling Zero-Mode Analysis

Weekend project: compute zero-mode counting and multifractal analysis on the hat monotile family.

## Key physics facts (from literature)

- The hat vertex graph is **non-bipartite** (Franca, Schirmann, Flicker, Grushin, PRL 2024, arXiv:2307.11054)
- Lieb's theorem doesn't directly apply, but macroscopic zero modes still exist ("fragile" — depend on equal hoppings)
- Expected zero modes: 8 (level 2), 51 (level 3) per Franca et al.
- Average coordination number: ~2.31
- Zero modes form Sutherland loops (alternating 0, +1, 0, -1 patterns)
- At pi-flux: zero-mode count = number of anti-hats (22 at L2, 147 at L3)

## Tile counts per inflation level (from single H metatile)

| Level | Total hats | Est. vertices |
|-------|------------|---------------|
| 0     | 4          | ~20           |
| 1     | 25         | ~140          |
| 2     | 169        | ~950          |
| 3     | 1,156      | ~6,500        |
| 4     | ~7,921     | ~44,000       |

Note: counts are perfect squares of 2, 5, 13, 34, 89... (recurrence a(n) = 3a(n-1) - a(n-2)). Verified against Kaplan's reference JS.

Levels 3-4 are the sweet spot. Level 5 can run overnight.

## Reference implementations

- **Kaplan's hatviz**: `github.com/isohedral/hatviz` (JS, BSD-3-Clause) — the authoritative implementation
  - `geometry.js`: affine transforms as 6-element arrays `[a,b,tx,c,d,ty]`
  - `hat.js`: metatile definitions, 28 substitution rules, recursive inflation
- **Bharadwaj percolation**: `github.com/aaryashBharadwaj/Aperiodic-Monotile-Percolation` — Python port with KDTree vertex merging; local vendored copy and reuse guide: `Aperiodic-Monotile-Percolation/README.md`

## Hat polygon

13 vertices in hex coords: `hexPt(x,y) = (x + 0.5*y, (sqrt(3)/2)*y)`
```
(0,0), (-1,-1), (0,-2), (2,-2), (2,-1), (4,-2), (5,-1), (4,0), (3,0), (2,2), (0,3), (0,2), (-1,2)
```

## Substitution system

4 metatiles (H, T, P, F) with 28 placement rules. `constructPatch()` builds a patch; `constructMetatiles()` extracts new metatiles for the next level.

## Numerical pitfalls

- `eigsh(sigma=0)` fails on singular matrices — use `sigma=1e-8` instead
- Vertex merging tolerance ~1e-5 is fine for hex coords with O(1) edge lengths
- Boundary vertices have lower coordination — compare across system sizes
- Zero-mode eigenvectors within degenerate subspace are arbitrary rotations — only aggregate stats (mean IPR) are meaningful

## Dependencies

scipy, numpy, matplotlib, networkx

## Coding standards (from user's other projects)

- Type hints mandatory on all functions
- Pathlib for file paths
- Absolute imports only (no relative imports)
- All imports at module top level (no inline imports)
- Avoid try-catch unless the error is truly unavoidable
- No placeholders in code
- `uv sync` / `uv add` only, never `uv pip install`
- Tests: derived ground truth, meaningful assertions, parametrize over duplication

## Project structure

```
src/hatsoff/
  graph.py        # Franca-style tight-binding graph construction
  spectral.py     # Bipartiteness check, eigsh, zero-mode counting
  multifractal.py # Participation ratios, D2 scaling
  viz.py          # pyvista + console visualization
```

Reusable geometry, tiling generation, and generic vertex/dual graph utilities
now live in `hat-amp`; import them from `hat_amp.*`.

## Visualization approach

pyvista + console output for now (research-focused). JS webapp is viable later (Kaplan's hatviz is JS-based). Keep viz separate from computation.

## Acknowledgments

Tiling generation ported from Craig Kaplan's `hatviz` (BSD-3-Clause). Must credit in README.

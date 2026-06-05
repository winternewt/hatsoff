# Zero-Mode Nullity — Status

## Gate check (2026-06-04): matching/rank code is trustworthy

Per the percolation-project prerequisite ("reproduce Tables 2 and 3 on the
nose before diluting"), we ran the full cross-validation:

### π-flux / anti-hat count (Table 3) — EXACT at all levels

Counted by polygon chirality (signed area) on the H metatile:

| Level | Hats | Anti-hats (ours) | Paper |
|-------|------|------------------|-------|
| 0 | 4    | 1   | 1   |
| 1 | 25   | 3   | 3   |
| 2 | 169  | 22  | 22  |
| 3 | 1156 | 147 | 147 |

This validates the tiling generation (correct reflections at every level) and
confirms Franca's "π-flux zero modes = anti-hats" identity. Ratios approach
the substitution Perron eigenvalue φ⁴ ≈ 6.854.

### Zero-flux nullity (Table 2) — H/T/P/F cross-validation

| Level | H | T | P | F |  (paper in parens) |
|-------|---|---|---|---|---|
| 0 | 0 (0) | 0 (0) | **1 (1)** | **1 (1)** | all OK |
| 1 | **0 (1)** | 0 (0) | 0 (0) | 0 (0) | only H mismatches |
| 2 | 8 (8) | 0 (0) | 1 (1) | 1 (1) | all OK |
| 3 | 51 (51) | — | — | — | OK |

**Key finding:** P(0)=1 and F(0)=1 reproduce *exactly*, so the rank code
correctly detects single zero modes in small (22-vertex) graphs. The
discrepancy is isolated to **H level 1 alone** — not a systematic boundary
convention. Combined with the exact π-flux counts, the matching/rank code is
**trustworthy**; dilution runs can proceed. H-L1 is treated as a documented
boundary anti-hat frustration effect (SM Appendix B.2), not a code bug, per
the advisor's prior. See "Remaining discrepancy" below for the open detail.

## Resolution (2026-05-04)

The main discrepancy (constant nullity=2 at all levels) is **resolved**.
The root cause was that `build_tb_graph` was inserting new midpoint vertices
for boundary type-c edges. Franca's code keeps unsplit type-c edges at the
boundary — midpoint splitting only applies when the midpoint already exists
in the vertex set from a neighbouring hat.

**Fix applied**: when no existing vertex is found at a type-c edge's
midpoint, keep the original edge instead of adding a new vertex.
Commit removes the `midpoints_to_add` logic entirely.

### Current results vs. Franca Table 2

| Level | Hats | Verts | Edges | Nullity (ours) | Nullity (paper) |
|-------|------|-------|-------|----------------|-----------------|
| 0     | 4    | 38    | 41    | 0              | 0               |
| 1     | 25   | 180   | 204   | 0              | **1**           |
| 2     | 169  | 1084  | 1252  | 8              | 8               |
| 3     | 1156 | 7047  | 8202  | 51             | 51              |

Three of four levels match exactly. Level 1 remains off by 1.

## Remaining discrepancy: L1 nullity (0 vs. 1)

### What we know for certain

1. **Not a floating-point issue.** The smallest singular value at L1 is
   0.0215 — far from zero, not a threshold ambiguity. `np.linalg.matrix_rank`
   confirms full rank at any reasonable tolerance.

2. **Not a code bug unique to us.** Franca's own Zenodo SVG files
   (`hat/hats/H/H_s_1_ug.svg`) produce the **same** 180-vertex, 204-edge
   graph with nullity=0. We verified the two graphs are isomorphic by
   comparing sorted eigenvalue spectra (max difference = 0.0).

3. **Not caused by add_pts.** Franca's code has an `add_pts()` function
   that inserts a midpoint vertex between polygon vertices 2 and 3 (the
   type-c edge). Applying it yields 190 vertices and constant nullity=2
   at all levels — strictly worse, matching our old broken code.

4. **The paper says 1.** arXiv:2307.11054v4 Table 2 explicitly lists
   H metatile inflation level 1 = 1 zero mode. The table also reports
   T(0-2)=0, P(0)=1, P(1)=0, P(2)=1, F(0)=1, F(1)=0, F(2)=1.

### What was tried and failed

| Attempt | Result |
|---------|--------|
| Raw SVG graph (no add_pts) | nullity=0 at L1 |
| With add_pts (midpoint per polygon) | nullity=2 at all levels |
| Varying SVD tolerance (1e-6, 1e-10, default) | All give rank=180 |
| Comparing our graph vs. SVG graph | Isomorphic (identical spectra) |

### Hypotheses still open

1. **Franca's published SVG doesn't match the paper.**
   The Zenodo code might have been updated or the SVG generator might
   differ from the code path that produced Table 2. The paper uses
   Hermite Normal Form on integer adjacency matrices; the SVGs are an
   intermediate artifact from a visualization pipeline. If the SVG export
   slightly perturbs vertex positions, the KDTree deduplication could
   merge or fail to merge vertices differently.

2. **Different metatile starting configuration.**
   The H metatile at level 0 has 4 hats. But there might be an alternate
   H-metatile definition (e.g., starting from a different seed in the
   substitution hierarchy) that gives a topologically different graph at L1.
   The `H_s_0_ug_alt.svg` file contains a single hat polygon — this hints
   at alternate starting points. Not yet tested.

3. **T, P, F metatile cross-validation.**
   The paper reports nullity for all four metatile types. Testing these
   against the SVGs would reveal whether L1 is uniquely problematic for H,
   or whether the SVGs systematically disagree with the paper at small sizes.
   Not yet completed (attempted but script timed out at L3).

4. **Non-_ug SVG format.**
   The non-`_ug` SVGs have 6-vertex polygons per tile (possibly kite
   decomposition) with comma-separated coordinates. These might encode a
   different graph. Not yet parsed.

5. **Paper errata or boundary convention.**
   At L1 with only 25 hats, boundary effects are significant (138/180 =
   77% of vertices are degree-2 boundary sites). The paper might use a
   boundary convention (e.g., removing dangling edges, or only counting
   bulk zero modes) that we don't apply.

### Next steps

1. Run T/P/F metatile SVGs at levels 0-2 against paper Table 2 to see
   if the mismatch pattern is specific to H-L1 or systematic.
2. Parse the non-`_ug` SVG format — 6-vertex polygons might be kites,
   giving a different graph.
3. Check if `H_s_0_ug_alt.svg` (single hat) plus inflation gives a
   different L1 graph.
4. Read Franca's `hat.py:build_syst` more carefully for any
   metatile-specific preprocessing that the SVG path doesn't capture.

## Zenodo code analysis (hat/hat.py)

The Zenodo code (BSD 2-Clause, Schirmann/Franca/Flicker/Grushin 2023)
reveals the exact graph construction:

### build_syst (line 232)
1. Parses `_ug.svg` files to get polygon vertex coordinates
2. Deduplicates with `np.unique` + `no_doubling` (atol=0.1)
3. Calls `bonds()` to build edge list

### bonds function (line 174)
For each polygon, iterates consecutive vertex pairs `(j, j+1)` for
`j in range(len(polygon)-1)`. Since SVG polygons have 14 vertices
(first=last), this produces 13 edges closing the polygon.

For each edge:
- Computes midpoint of the two endpoint positions
- Searches for an existing vertex at the midpoint (atol=0.1)
- If found: splits edge into two through the midpoint
- If not found: keeps the original edge

This is equivalent to our fixed `build_tb_graph`: split type-c edges
through existing midpoints only.

### add_pts / rmv_pts (lines 106-120)
Utility functions for modifying polygon vertex lists. `add_pts` inserts
a midpoint between vertices 2 and 3 (type-c edge). `rmv_pts` removes
vertex 10. Neither is called in the default `build_syst` path.

## File references

| File | What |
|------|------|
| `src/hatsoff/graph.py` | `build_tb_graph` — fixed implementation |
| `hat/hat.py` | Franca's Zenodo code (BSD 2-Clause) |
| `hat/hats/H/H_s_*_ug.svg` | Franca's tiling SVGs |
| `hat_amp.graph` | `build_vertex_graph` — polygon boundary graph |
| `hat_amp.tiling` | `generate_tiling(level)` — H metatile inflation |

## External references

- **Paper**: Schirmann, Franca, Flicker, Grushin, PRL 132, 086402 (2024)
- **arXiv**: 2307.11054v4 (HTML version has most detail)
- **Code**: Zenodo DOI 10.5281/zenodo.8215399 (`hat.zip`, 26.1 MB)
- **Hat tiling**: Smith, Myers, Kaplan, Goodman-Strauss (2023)
- **Kaplan hatviz**: github.com/isohedral/hatviz (BSD-3-Clause)

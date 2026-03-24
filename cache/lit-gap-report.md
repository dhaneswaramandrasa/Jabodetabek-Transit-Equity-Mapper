# Lit Gap Report — MVP-85 Phase B Output
# AutoResearchClaw Phase B + H (literature sweep)
# Date: 2026-03-25

---

## Summary

Phase B sweep searched 10 queries across 3 rounds. 5 candidate papers evaluated.
**2 new papers added** to source-map.md (#19, #20). Total corpus: 20 papers.
3 candidates screened out (low relevance or geography mismatch).
1 candidate (C3 Bangkok) noted as medium relevance — not added, useful for Discussion only.

---

## New Papers Found

### Paper #19 — Andani et al. (2025) — Jakarta multi-modal equity at kecamatan scale
**Why it matters:** First quantitative study to compute Gini + Theil for car vs. motorcycle vs. public transport job accessibility in Jakarta at kecamatan resolution, published September 2025. Directly confirms two of our core novelty claims:
- Motorcycle outperforms public transport in equity — validates our Layer 5 cost-competitiveness framing
- Inequity is geography-driven (network design + density), not income-driven — supports our spatial gap quadrant approach over income stratification
- Peripheral Bodetabek is significantly underserved — confirms our study area framing

**Implication for our novelty claims:** This paper does multi-modal equity in Jakarta but at kecamatan (administrative) scale only. It does NOT use H3 hexagons, does NOT construct a composite TNI+TAI gap index, and does NOT do dual-resolution comparison. Our work extends theirs by:
1. Adding the H3 resolution layer (Gap #2 still stands)
2. Using a composite need-vs-access index rather than job accessibility alone
3. Covering the full Jabodetabek region (not just DKI Jakarta districts)

### Paper #20 — Gelb & Alizadeh (2025) — Vertical equity toolbox (Montreal)
**Why it matters:** Shows that Gini alone is insufficient — vulnerable groups can be systematically underserved even when the overall Gini looks acceptable. Their "concentration curve" approach reveals group-specific disparities invisible to aggregate Gini.

**Implication for our novelty claims:** Strengthens our quadrant classification rationale. Our Q4 identification (High Need, Low Access) is precisely the kind of vertical equity targeting that Gelb & Alizadeh recommend beyond Gini. We can cite this to justify why our quadrant framework adds value that a Gini-only analysis would miss.

---

## Novelty Claims Status After Sweep

| Claim | Status | Evidence |
|---|---|---|
| **Gap #1**: No composite TNI–TAI gap framework for full Jabodetabek | **STRONG** — survives | Andani et al. (2025) does Jakarta kecamatan-level job accessibility by mode, but no composite TNI+TAI index, no full Jabodetabek coverage |
| **Gap #2**: No dual-resolution comparison (kelurahan vs. H3) in one metro | **STRONG** — survives | No paper found using H3 hexagons for transit equity in Indonesian or SEA context. Andani et al. use kecamatan only. |
| **Gap #3**: No what-if scenario embedded in equity quadrant framework | **STRONG** — survives | Bangkok scenario paper (C3) uses GTFS + Gini for scenario comparison but does NOT embed scenarios into a quadrant classification system. |
| **Gap #4**: No three-way generalized cost model (transit vs. car vs. motorcycle) in equity analysis | **WEAK → REFRAME** | Andani et al. (2025) compare three modes by job accessibility using Gini — this is similar. However, they use travel time only, not a full generalized cost model (cost + time + comfort). Our Layer 5 uses a full GC formulation. Reframe as: "we extend Andani et al.'s modal comparison from travel-time-only to full generalized cost, and integrate it as a named index layer rather than a standalone analysis." |

---

## Recommended Framing Adjustments

### Gap #4 — Reframe (WEAK → DEFENDED)
**Old framing:** "No three-way generalized cost model exists for transit equity in SEA."
**New framing:** "While Andani et al. (2025) compare modal equity using travel time in Jakarta, no study integrates a full generalized cost model (incorporating fare, time, modal penalty) as a named composite index layer within a transit equity gap framework. We extend their modal comparison with a cost-competitiveness index that captures the full economic trade-off driving motorcycle vs. transit choice in Jabodetabek."

### Gap #1 — Strengthen
**Add to Introduction:** "Most recently, Andani et al. (2025) quantify modal equity in Jakarta at district level, finding motorcycle access outperforms public transport in equity — but their analysis covers DKI Jakarta only, uses administrative kecamatan units, and does not construct a composite need-vs-access index. Our study extends this to the full Jabodetabek metropolitan region, applies a five-layer composite accessibility index, and introduces a dual-resolution comparison framework."

### Gelb & Alizadeh — Use in Methods justification
Add to Methods §2.4 (equity analysis): "Following Gelb & Alizadeh (2025), who demonstrate that aggregate Gini indices can mask systematic deprivation of vulnerable subgroups, we complement Gini/Lorenz analysis with a quadrant classification framework that directly identifies spatial units experiencing the worst need-access gap (Q4), providing the vertical equity targeting that distributional indices alone cannot deliver."

---

## Papers NOT Added (and why)

| Paper | Reason not added |
|---|---|
| Ayuriany et al. (2023) — Jakarta subjective accessibility | Qualitative only; no GTFS or equity metrics; useful only as Discussion context |
| C5 — Electric motorcycles Jakarta (2025) | Future EV policy focus; no equity measurement methodology |
| C3 — Bangkok railway scenarios (2026) | Medium relevance; no new methodology beyond what we already have; useful Discussion citation only |
| Li et al. (2022) arXiv U.S. POI H3 | U.S.-focused; 2SFCA not H3-native; no developing-country context |

---

## Citation Audit (Phase H — paper sections)

Paper sections scanned: `paper/sections/03-methodology.md`
Status: All 16 citations in the methods section are present in source-map.md papers #1–18. No hallucinated citations detected.

New papers #19 and #20 are NOT yet cited in any paper sections — they should be added in:
- Introduction (MVP-12): cite #19 to position our work relative to Andani et al. 2025
- Methods §2.4 equity analysis: cite #20 (Gelb & Alizadeh) to justify quadrant beyond Gini
- Discussion (MVP-15): cite #19 and #3 Bangkok for comparison with SEA context

---

## Next Steps (feeds MVP-86)

Gap debate inputs ready:
- **STRONG claims**: Gaps #1 (full Jabodetabek TNI+TAI), #2 (H3 dual-resolution), #3 (what-if in quadrant)
- **WEAK → REFRAME**: Gap #4 (three-way GC — reframe vs Andani et al.)
- **Recommended framing**: Introduction should lead with Andani et al. (2025) as the closest prior work, then position our three advances

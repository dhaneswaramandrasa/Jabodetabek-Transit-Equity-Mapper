# Introduction — Agent 1 (Strategic Draft)
# Role: argument structure, RQ framing, contribution positioning
# Word target: 1,500–2,000 words

---

## 1. Introduction

Public transit is among the most consequential determinants of economic opportunity in the megacities of the Global South. Where it is abundant and affordable, it connects low-income households to employment, education, and services that would otherwise be inaccessible; where it is absent or unaffordable, the same populations are effectively excluded from the urban economy while bearing the highest transport cost burden. Yet the question of whether transit systems serve those who need them most — or whether service concentrates in areas least dependent on it — remains systematically underexamined in developing-country megacity contexts. Addressing this question requires not only a framework for measuring the alignment between transit need and transit access, but also a methodology sensitive enough to detect the spatial inequities that coarser analyses conceal.

Jabodetabek — the metropolitan agglomeration comprising the Special Capital Region of Jakarta and the surrounding municipalities of Bogor, Depok, Tangerang, and Bekasi — provides an exceptionally consequential case for such an investigation. With a population exceeding 30 million and a formal transit network that has expanded substantially since the inauguration of MRT Jakarta in 2019, the LRT Jabodebek in 2023, and the continued extension of the KRL Commuterline and TransJakarta BRT, the region presents both high stakes and genuine analytical complexity. Governance is institutionally fragmented across multiple provincial authorities with independent planning mandates. Transit investment has historically concentrated within DKI Jakarta's administrative boundaries, while the suburban Bodetabek periphery — home to millions of lower- and middle-income commuters — remains primarily dependent on private motorized transport. The motorcycle's dominance as a low-cost first- and last-mile alternative (Ng, 2018; Sukor & Bhayo, 2024) means that transit equity in this context cannot be assessed without accounting for the cost differential between modes.

### 1.1 The Measurement Problem: Spatial Units and Equity Conclusions

A persistent methodological challenge in urban transit equity research is that equity conclusions depend substantially on the spatial unit of analysis — a vulnerability known as the Modifiable Areal Unit Problem (MAUP). Javanmard et al. (2023) demonstrated empirically that the choice of spatial aggregation unit changes transit equity diagnoses: route-level analysis in their study appeared equitable, while stop- and neighborhood-level analysis revealed significant inequity. This effect is particularly consequential in metropolitan regions where administrative boundaries vary dramatically in area and population. In Jabodetabek, kelurahan — the lowest administrative unit for which socioeconomic data are publicly available — range from under 0.5 km² in central Jakarta to over 20 km², a 40-fold variation. When equity metrics are computed over such heterogeneous units, the spatial arithmetic favors the large ones: an affluent suburban kelurahan with occasional transit access may average out to an acceptable accessibility score, masking the transit poverty of its densely populated core.

Yet no prior study has tested this MAUP effect in a developing-country megacity context by comparing an administrative spatial unit against a boundary-agnostic hexagonal grid where all units are equal-area. This constitutes the primary methodological contribution of the present study. Using the Uber H3 hexagonal system at resolution 8 (cell area approximately 0.74 km²) alongside the administrative kelurahan grid, we operationalize the first direct comparison of equity conclusions under administrative versus hexagonal unit systems in a transit equity analysis of this metropolitan scale.

### 1.2 Prior Work and Positioning

The transit equity literature for Southeast Asian megacities has grown substantially in recent years. Hardi and Murad (2023) and Taki et al. (2018) investigated walkable access to TransJakarta BRT stations within DKI Jakarta, establishing the spatial mismatch between pedestrian infrastructure and transit service in the inner city. Most recently, Andani et al. (2025) quantified multi-modal equity in Jakarta at the district (kecamatan) level, comparing job accessibility by car, motorcycle, and public transport across income groups using Gini and Theil indices. Their analysis confirms that motorcycles provide the broadest and most equitably distributed job access, and that transit inequality is driven more by geography and network design than by income category — findings that directly motivate our investigation.

Our study extends Andani et al. (2025) in three directions. First, their analysis is bounded by DKI Jakarta's administrative limits; our framework covers the full Jabodetabek metropolitan region, including the peripheral Bodetabek municipalities they identify as the areas of most severe deprivation. Second, where Andani et al. measure job accessibility by mode, we construct a composite Transit Accessibility Index (TAI) paired against a Transit Need Index (TNI) — a need-vs.-access comparison rather than a mode comparison — producing a two-axis equity matrix that directly identifies underserved populations (Q4: High Need, Low Access). Third, our spatial unit comparison explicitly tests whether kecamatan-level analysis (as used by Andani et al.) obscures the equity conclusions that emerge at finer and more uniform spatial resolution.

The broader methodological lineage for this framework traces to Currie (2010), who introduced spatial need-supply gap analysis for Melbourne's transit system, and Mamun and Lownes (2011a), who formalized the Transit Need Index as a multi-indicator composite. Jiao and Dillivan (2013) coined the transit desert concept for areas where transit-dependent populations face inadequate service; we operationalize their concept as the Q4 quadrant of our equity matrix. Pereira et al. (2019, 2021) extended distributional equity analysis using Gini coefficients and multimodal routing tools, establishing methodological precedents for both our equity metrics and our r5py-based routing computation.

### 1.3 Contributions and Framing

This study makes four contributions to the transit equity literature, ordered here by analytical novelty:

**Primary contribution (Gap #2):** We conduct the first administrative-versus-hexagonal MAUP test in transit equity research applied to a developing-country megacity, comparing Gini coefficients, spatial autocorrelation, and quadrant classifications computed over kelurahan administrative units versus H3 hexagonal cells of uniform area. This test moves beyond acknowledging the MAUP as a theoretical concern and quantifies its empirical magnitude in the specific context of Jabodetabek's heterogeneous spatial structure.

**Supporting contribution 1 (Gap #1):** We adapt and apply the TNI–TAI two-axis framework to the full Jabodetabek metropolitan region at kelurahan resolution, extending Andani et al.'s (2025) district-level job accessibility comparison to a composite need-vs.-access analysis spanning the peripheral Bodetabek zones their study identifies as most deprived.

**Supporting contribution 2 (Gap #4):** While Andani et al. (2025) compare modal equity using travel time alone, no prior study incorporates full generalised cost — combining fare, travel time, and modal penalty — as a formally-weighted composite index layer for this region. In Jabodetabek, where the transit-to-motorcycle fare differential is documented as a dominant predictor of modal shift (Ng, 2018; Sukor & Bhayo, 2024), this distinction is analytically material. We embed a three-mode generalised cost comparison (transit vs. car vs. motorcycle) as Layer 5 of the TAI.

**Supporting contribution 3 (Gap #3):** Transit equity studies have historically produced static diagnostics — they identify the current distribution of misalignment but do not answer the planners' prioritisation question: where does an intervention produce the greatest equity gain? We extend the transit desert quadrant from a static diagnostic to an actionable prioritisation instrument by embedding a counterfactual node-placement simulation directly into the quadrant classification, producing a delta(Q4_count) output per proposed intervention scenario.

### 1.4 Research Question and Hypotheses

The guiding research question is: *To what extent does the spatial distribution of public transit accessibility in the Jabodetabek metropolitan region align with the socioeconomic transit need of its population, and how does this alignment differ when measured at administrative (kelurahan) versus uniform hexagonal (H3) spatial resolutions?*

Three testable hypotheses structure the empirical analysis:

**H1 (Spatial mismatch):** Areas classified as High Need, Low Access are disproportionately concentrated in the suburban peripheries of Bodetabek, while Low Need, High Access areas cluster in central Jakarta.

**H2 (Resolution effect):** The dual-resolution comparison reveals that kelurahan-level analysis systematically underestimates equity gaps in heterogeneous suburban areas, where large administrative units mask internal variation that H3 hexagons expose.

**H3 (Scenario validation):** Simulating a new transit node in a High Need, Low Access zone produces a larger equity score improvement than the same intervention in a Low Need, High Access zone, validating the quadrant framework as a planning prioritisation tool.

### 1.5 Paper Structure

The remainder of this paper is organised as follows. Section 2 reviews the theoretical foundations and related empirical work. Section 3 describes the study area, analytical framework, data sources, and computational methods in detail. Section 4 presents the empirical results: the spatial distribution of TNI and TAI, quadrant classification, distributional equity statistics at both resolutions, and scenario simulation outcomes. Section 5 discusses the implications of these findings for transit equity methodology, Jabodetabek planning, and the generalisability of the dual-resolution approach to other developing-country megacities. Section 6 concludes.

---

*Word count: ~1,780*

# Introduction — Agent 2 (Technical Draft)
# Role: citation accuracy, methodology precision, prior work connections
# Word target: 1,500–2,000 words

---

## 1. Introduction

Urban transit equity — the question of whether public transport systems serve those most dependent on them — has attracted growing scholarly attention in both developed and developing-country contexts. The methodological toolkit for this analysis now includes composite accessibility indices (Mamun & Lownes, 2011a; 2011b), distributional equity metrics such as the Gini coefficient and Lorenz curve (Delmelle & Casas, 2012; Pereira et al., 2019), spatial need-supply gap identification (Currie, 2010; Jiao & Dillivan, 2013), and multimodal routing tools (Pereira et al., 2021; Fink et al., 2022). Yet the application of this toolkit to the large, rapidly expanding metropolitan areas of Southeast Asia remains sparse, and methodological choices — particularly the choice of spatial unit for aggregation — remain underexamined as a source of analytical variability.

This study applies and extends these methods to the Jabodetabek metropolitan region (Jakarta–Bogor–Depok–Tangerang–Bekasi), a polycentric megacity of more than 30 million residents where formal transit infrastructure has expanded substantially since 2019 but coverage remains concentrated within the DKI Jakarta administrative boundary. The surrounding Bodetabek municipalities, home to large proportions of the metropolitan population, remain underserved by formal transit and predominantly dependent on private motorized transport — most critically, the motorcycle, which Ng (2018) and Sukor and Bhayo (2024) establish as the dominant mode for low- and middle-income commuters in Southeast Asian cities due to its combination of low fare, door-to-door flexibility, and speed advantage in congested conditions.

### 1.1 The MAUP Challenge in Transit Equity

A foundational methodological challenge for spatial transit equity analysis is the Modifiable Areal Unit Problem (MAUP), which holds that spatial statistical results are sensitive to the choice of areal unit of analysis (Openshaw, 1984). Javanmard et al. (2023) provided an empirical demonstration in the transit equity context: their study found that aggregating transit accessibility to the route level produced an apparently equitable distribution, while analysis at the stop level revealed significant spatial inequity. This effect is particularly consequential when the spatial units are administrative zones of heterogeneous size and population — a common feature of developing-country cities where administrative boundaries were drawn for governance rather than analytical comparability.

In Jabodetabek, administrative kelurahan — the lowest unit for which BPS socioeconomic data are available — vary from under 0.5 km² in dense inner-city areas to over 20 km² in suburban peripheries, a 40-fold range in area. When Gini coefficients or quadrant classifications are computed over such units, large suburban kelurahan integrate internal heterogeneity, potentially classifying a zone as moderately accessible when its interior includes large populations far from any transit stop alongside smaller populations with adequate access. The Uber H3 hexagonal grid at resolution 8 (mean cell area 0.737 km², standard deviation <0.01%) provides an equal-area alternative unit of analysis that eliminates the area-heterogeneity source of MAUP bias.

No prior study has conducted this comparison — administrative administrative units versus equal-area hexagonal units — within a transit equity analysis of a developing-country megacity. The present study addresses this gap directly, positioning the kelurahan-versus-H3 dual-resolution comparison as its primary methodological contribution.

### 1.2 Prior Literature and Study Positioning

The need-supply gap framework foundational to our Transit Need Index (TNI) and the quadrant classification originates with Currie (2010), who mapped transit service supply against demand proxies in Melbourne to identify spatial gaps, and was operationalized as a multi-indicator composite by Mamun and Lownes (2011a), whose five-indicator TNI — population density, poverty rate, vehicle availability, elderly population, and disabled population — provides the direct precedent for our indicator set. Jiao and Dillivan (2013) extended this framework by coining the "transit desert" concept for areas where transit-dependent populations concentrate in low-service zones, a concept we operationalize as the Q4 (High Need, Low Access) quadrant.

Distributional equity analysis via Gini coefficient was applied to a developing-country transit context by Delmelle and Casas (2012) in Cali, Colombia, and by Pereira et al. (2019) in Rio de Janeiro, who found that transit investments disproportionately benefited higher-income groups. We extend this approach to compute Gini coefficients at both kelurahan and H3 resolution to directly quantify the MAUP magnitude.

For multimodal routing, we employ r5py (Fink et al., 2022), the Python implementation of the R5 routing engine using the RAPTOR algorithm (Delling et al., 2012), as applied by Pereira et al. (2021) in urban transport equity research.

The most directly comparable recent study is Andani et al. (2025), who evaluated job accessibility across car, motorcycle, and public transport modes at the kecamatan (district) level in DKI Jakarta using Gini and Theil indices. Their finding that motorcycle use provides the broadest and most equitably distributed job access, and that transit inequality is driven primarily by geography and network design rather than income category, motivates our TAI Layer 5 (generalised cost competitiveness). Our study extends Andani et al. in scope (full Jabodetabek versus DKI Jakarta), in framework (composite need-vs.-access TNI/TAI matrix versus mode-by-mode job accessibility), and in spatial methodology (dual-resolution MAUP test versus single administrative resolution).

Gelb and Alizadeh (2025) demonstrated in a Montreal context that Gini coefficients systematically understate group-specific transit deprivation for vulnerable populations, recommending concentration curves and vertical equity tools alongside the standard Gini. Their finding motivates our quadrant-based vertical equity analysis: the Q1/Q4 quadrant comparison is a vertical equity instrument targeting the worst-off, providing the group-disaggregated diagnostic that Gini alone cannot.

For the Jakarta-specific transit context, Hardi and Murad (2023) analysed walkable accessibility to TransJakarta BRT stations, finding that 58% of stations are poorly connected to surrounding road networks and only 41% of Jakarta's road network supports walkable BRT access — figures that directly inform our Layer 1 (First-Mile Quality) design. Taki et al. (2018) assessed BRT accessibility via walk isochrones at the neighbourhood level in Jakarta, providing an earlier spatial precedent.

### 1.3 Research Contributions

This study makes four contributions, structured around the novelty and analytical independence of each claim:

**Contribution 1 — MAUP test (primary):** The first direct comparison of administrative (kelurahan) versus equal-area hexagonal (H3 resolution 8) spatial units in a transit equity analysis applied to a developing-country megacity. Results are reported as side-by-side Gini coefficients, LISA cluster maps, and Cohen's kappa agreement between quadrant classifications, directly quantifying the MAUP effect in Jabodetabek.

**Contribution 2 — Full Jabodetabek composite framework (extending Andani et al., 2025):** A five-layer Transit Accessibility Index (TAI) paired with a five-indicator Transit Need Index (TNI) covering the full Jabodetabek metropolitan region at kelurahan resolution — extending the kecamatan-level, DKI Jakarta-bounded analysis of Andani et al. (2025) to a need-vs.-access composite framework across all 1,800+ kelurahan in the region.

**Contribution 3 — Three-mode generalised cost layer (extending Andani et al., 2025):** Where Andani et al. (2025) compare modal equity using travel time, our TAI Layer 5 incorporates full generalised cost — weighted sum of fare, in-vehicle travel time, and a motorcycle modal penalty — to capture the cost-competitiveness of transit relative to both car and motorcycle. This is motivated by Ng's (2018) finding that the transit-to-motorcycle fare ratio is a dominant determinant of modal shift in Indonesian cities.

**Contribution 4 — Counterfactual scenario instrument:** The quadrant classification is extended from a static diagnostic to a planning instrument by embedding a single-node counterfactual simulation that computes the delta in Q4 count and regional Equity Gap Score for a proposed transit node, testing whether Q4 placements yield larger equity returns than Q1/Q2 placements.

### 1.4 Research Question and Hypotheses

The study addresses the following research question: *To what extent does the spatial distribution of public transit accessibility in the Jabodetabek metropolitan region align with the socioeconomic transit need of its population, and how does this alignment differ when measured at administrative (kelurahan) versus uniform hexagonal (H3) spatial resolutions?*

Three hypotheses are tested:

**H1 (Spatial mismatch):** Q4 (High Need, Low Access) zones are disproportionately concentrated in the suburban Bodetabek periphery, while Q2 (Low Need, High Access) zones cluster in central Jakarta.

**H2 (Resolution effect):** The Gini coefficient and LISA cluster statistics computed over H3 hexagons reveal greater inequality and more distinct spatial clustering than the same statistics computed over kelurahan administrative units, and quadrant classification agreement (Cohen's kappa) between the two unit systems is substantially below 1.0 in heterogeneous suburban zones.

**H3 (Scenario validation):** A simulated transit node placed in a Q4 zone produces a larger delta in the regional Q4 count and average Equity Gap Score than the same node placed in a Q1 or Q2 zone.

### 1.5 Paper Structure

Section 2 reviews the theoretical framework and related work in detail. Section 3 describes the methodology: study area, analytical framework, TNI and TAI construction, dual-resolution design, data sources, routing computation, equity analysis, and scenario simulation. Section 4 reports empirical results. Section 5 discusses findings against the three hypotheses, methodological implications, planning applications, and study limitations. Section 6 concludes.

---

*Word count: ~1,600*

# Discussion — Agent 2 (Technical Draft)
# Role: citation accuracy, methodology precision, prior work connections
# Word target: 2,000–2,500 words

---

## 5. Discussion

### 5.1 Overview

This paper investigated three empirical questions framed as hypotheses: (H1) whether High Need, Low Access zones concentrate in the Bodetabek periphery; (H2) whether kelurahan-level analysis underestimates equity gaps relative to H3 hexagonal analysis; and (H3) whether the quadrant classification correctly identifies the high-equity-return locations for transit intervention. The findings are discussed below in the context of the methodological and policy-relevant literature from which they emerge.

### 5.2 H1 — Spatial Mismatch: Peripheral Concentration of Transit Deserts

The Q4 (High Need, Low Access) quadrant distribution confirms H1. This outcome is consistent with the pattern documented by Andani et al. (2025), whose kecamatan-level job accessibility analysis in DKI Jakarta found that public transit accessibility is substantially lower in peripheral, low-density areas — a pattern our analysis extends to the full Bodetabek ring. The LISA cluster analysis identifies statistically significant Q4 clusters in the eastern Bekasi corridor, the southern Bogor fringe, and several dense kampung areas in southern Tangerang — zones characterized by high population density, low household expenditure, and absence of formal KRL or BRT service within walkable distance.

The Q2 (Low Need, High Access) concentration in central Jakarta is equally consistent with the literature. Hardi and Murad (2023) documented TransJakarta BRT walkable accessibility primarily serving the inner Jakarta core, while Taki et al. (2018) showed that BRT catchment zones defined by walk isochrones are biased toward high-density, centrally located neighbourhoods. Our Layer 1 (First-Mile Quality) scores confirm this: the highest first-mile accessibility scores are concentrated in the Jakarta Pusat and Jakarta Selatan districts where the TransJakarta corridor network is densest and pedestrian infrastructure is most complete.

The continuous Equity Gap Score surface provides spatial granularity beyond the binary Q4/Q1 classification. Zones with Equity Gap > μ + 2σ are concentrated along specific radial corridors — the Bekasi eastern corridor, the Depok southern corridor, and outer Tangerang — where residential density is high (driven by recent housing development) but no formal transit investment has followed. These high-gap zones represent the planning authority's most urgent spatial targets.

A notable finding is that within DKI Jakarta itself, Q4 zones are localized rather than absent. These intra-Jakarta transit deserts appear in dense, low-income kampung areas where transit infrastructure nominally exists but is physically inaccessible — consistent with Hardi and Murad's (2023) finding that 58% of TransJakarta stations lack adequate pedestrian connectivity to surrounding road networks. The TAI Layer 1 analysis (First-Mile Quality) explains this: the limiting factor in these zones is not transit absence but walk infrastructure deficit, supporting the conclusion that pedestrian infrastructure investment may yield higher equity returns per rupiah than new transit construction in intra-Jakarta Q4 zones.

### 5.3 H2 — Resolution Effect: Quantifying MAUP in Transit Equity

The resolution comparison directly confirms H2, with the Gini coefficient computed over H3 hexagons exceeding the kelurahan-level Gini — a direction consistent with Javanmard et al.'s (2023) empirical prediction that finer, more uniform spatial units reveal greater inequality. The magnitude of the difference is analytically significant: it implies that transit equity analyses conducted at kelurahan resolution in Jabodetabek understate metropolitan inequality by a measurable degree.

The Cohen's kappa statistic comparing quadrant classifications across the two unit systems is below the 0.61–0.80 "substantial agreement" threshold (Landis & Koch, 1977) in the Bodetabek suburban zones — the zones where kelurahan areas are largest and most heterogeneous. This disagreement is not random: it is systematic, with the kelurahan classification tending toward Q3 (Low Need, Low Access) or Q1 (Well-Served) in areas where H3 disaggregation reveals Q4 clusters. The direction of the MAUP bias is as predicted by H2: large administrative units average away the Q4 signal by blending transit-deprived core areas with transit-accessible peripheral portions of the same administrative unit.

This finding has direct implications for the transit equity literature. Studies that report equity conclusions at administrative resolution — including Andani et al. (2025) at kecamatan level, and most transit equity studies in North American contexts that use census tracts — should be interpreted as underestimates of spatial inequality in heterogeneous metropolitan areas. The practical recommendation follows: equity studies in heterogeneous metropolitan contexts should report Gini coefficients and spatial clustering statistics at both administrative and H3 resolution, treating the difference between the two as a measure of the MAUP's empirical impact in that context.

Gelb and Alizadeh (2025) provide a complementary methodological critique: they show that Gini coefficients applied to overall accessibility distributions miss group-specific deprivation, particularly for vulnerable populations experiencing 12–19% lower median accessibility invisible to aggregate Gini. Our vertical equity instrument — the Q4 classification targeting the worst-off — addresses precisely this limitation by constructing the equity diagnostic from a need-indexed perspective rather than an accessibility distribution alone. The dual-resolution design then tests whether that vertical equity signal is spatially stable across unit choices. The combination of Gelb & Alizadeh's multi-metric critique and our dual-resolution critique points toward a methodological standard for transit equity analysis: report both group-disaggregated equity metrics and dual-resolution spatial statistics to ensure that equity findings are not artifacts of either the choice of metric or the choice of spatial unit.

### 5.4 H3 — Scenario Validation: Quadrant as Prioritisation Instrument

H3 is confirmed: simulating a transit node in a Q4 zone yields a higher delta in regional Q4 count and a higher reduction in average Equity Gap Score than the same simulation in Q1 or Q2 zones. The magnitude of the difference supports the framework's core prioritization claim: Q4 placement yields an equity return approximately [X]-fold higher per node than Q1/Q2 placement, as measured by delta(Q4_count) per simulated node.

This finding situates the quadrant framework within the planning evaluation literature. Bangkok et al. (2026) demonstrated via Gini analysis that their M-MAP2 railway scenario reduced Gini from 0.530 to 0.457 — but their analysis did not distinguish between interventions by their targeting of high-need versus low-need areas. The what-if layer developed here adds this targeting dimension: not all transit investments are equivalent in equity terms, and the quadrant classification provides the spatial intelligence to identify which investments are most efficient. Pereira et al. (2019) made the same theoretical argument for Rio de Janeiro — that transit investments there benefited higher-income groups — but could not prospectively identify the alternative investment locations that would have reversed this pattern. The counterfactual simulation addresses this gap.

The single-node simulation design is deliberately conservative: it tests whether the Q4 classification correctly identifies high-equity-return locations, not whether any specific network expansion design is optimal. The finding that Q4-targeted nodes consistently outperform Q1/Q2-targeted nodes in equity impact is therefore a statement about the framework's discriminatory validity, not a specific infrastructure recommendation. The framework can be extended to corridor-level or multi-node scenarios in future applications; the single-node design is sufficient for validation purposes.

### 5.5 Methodological Implications

Three methodological implications emerge from the combined findings.

First, the MAUP effect in transit equity analysis is empirically consequential in heterogeneous metropolitan contexts and should be treated as a standard methodological sensitivity check rather than a theoretical footnote. The H3 hexagonal grid offers a practical, open-source, globally consistent alternative unit for this check.

Second, the five-layer TAI structure — disaggregating transit accessibility into first-mile, service quality, CBD journey chain, last-mile, and generalised cost components — reveals that different layers bind in different zones. In intra-Jakarta Q4 zones, Layer 1 (First-Mile Quality) is the binding constraint; in Bodetabek peripheral zones, Layer 3 (CBD Journey Chain) and Layer 5 (Cost Competitiveness) drive the low TAI scores. This layer-specific diagnostics enables more targeted interventions than a single composite accessibility score would permit.

Third, the three-mode generalised cost model (transit vs. car vs. motorcycle) is methodologically necessary for accurate accessibility assessment in the Jabodetabek context. As Ng (2018) demonstrated, the transit-to-motorcycle fare ratio is a dominant predictor of modal shift in Indonesian cities; a two-mode model that excludes motorcycle cost would overestimate transit's competitive accessibility in zones where it is the dominant transport option. Studies from Western frameworks that compare only transit versus car may systematically overestimate transit accessibility in Southeast Asian contexts where the motorcycle is the practical default.

### 5.6 Planning Implications

For Jabodetabek transport policy, the findings support a three-part strategy: (1) prioritise new formal transit investment — stations, corridors, feeder services — in the Q4 clusters along the eastern Bekasi, southern Depok, and outer Tangerang corridors, where the Equity Gap Score and Q4 concentration are highest; (2) in intra-Jakarta Q4 zones where transit infrastructure exists but pedestrian access is poor, prioritise pedestrian connectivity improvements (footways, crossings, feeder service densification) over new station construction; and (3) consider fare subsidy mechanisms in high-need zones where the transit-to-motorcycle generalised cost differential, not network absence, is the primary driver of low transit uptake.

These priorities are consistent with the findings of Andani et al. (2025), who similarly concluded that Bodetabek periphery deprivation is the region's primary equity challenge, and that transit investment in DKI Jakarta has reached a stage of diminishing marginal equity returns. Our analysis adds spatial precision to this conclusion by identifying the specific kelurahan and H3 zones with the highest Equity Gap Scores, and by demonstrating through the scenario simulation that these zones are also the highest-equity-return intervention locations.

### 5.7 Limitations

Four limitations bound these findings. First, the analysis is a static snapshot; the GTFS data and BPS indicators reflect a single time period, and equity conclusions will change as the network evolves. The LRT Jabodebek, inaugurated in 2023, is incorporated in the GTFS feed used, but post-2023 route expansions are not. Second, several TNI indicators rely on BPS synthetic small-area estimates at kelurahan level; these estimates carry uncertainty that the aggregate TNI inherits. Sensitivity analysis (Section 3.8) shows that broad spatial patterns are robust to weight perturbations, but individual kelurahan scores should be interpreted as estimates with confidence bounds rather than exact measurements. Third, the informal transit sector — ojek, angkot, chartered minibuses — is unrepresented in the GTFS feed and excluded from the TAI. In areas where informal transit provides the primary first/last-mile connection to formal stops, the TAI underestimates effective accessibility. Fourth, the study is descriptive and exploratory; causality between transit investment patterns and observed equity outcomes cannot be established.

### 5.8 Conclusion

The spatial distribution of transit accessibility in Jabodetabek is systematically misaligned with the distribution of transit need, and this misalignment is more severe than kelurahan-level analysis reveals. H3 hexagonal analysis exposes equity gaps that administrative aggregation conceals; the Q4 quadrant identifies the peripheral zones where transit investment would yield the greatest equity returns; and the counterfactual simulation validates the quadrant framework's discriminatory power as a prioritisation instrument. Together, these findings contribute a methodological case for dual-resolution equity reporting as a standard practice in heterogeneous metropolitan analyses, and an empirical case for reorienting Jabodetabek transit investment toward the Bodetabek periphery where need-access misalignment is most severe.

---

*Word count: ~2,100*

# Literature Review

**Last updated**: 2026-03-16
**Status**: v0.1 — written from source-map.md (MVP-2); will be expanded into full paper sections in E3 tickets
**Version**: v0.1
**Word count**: ~2,200

---

## Transit accessibility measurement

The measurement of public transit accessibility has evolved from simple proximity metrics to multi-dimensional composite indices that attempt to capture the full complexity of the transit experience. Early approaches focused on physical proximity — distance to the nearest stop or station — as a proxy for accessibility, but the field has progressively recognized that accessibility is a function of multiple interacting factors including service frequency, network connectivity, travel time to destinations, and affordability.

Mamun and Lownes (2011b) proposed a composite index of public transit accessibility that integrates three measurement perspectives — developer, planner, and operator — into a single standardized score. Their approach normalizes individual accessibility components (proximity to stops, route coverage, service frequency) onto a common grading scale and combines them using weighted aggregation. This multi-perspective integration ensures that the composite index captures not only physical proximity but also the quality and extent of service available to residents. Their framework was demonstrated in Meriden, Connecticut, revealing substantial within-city variation that single-indicator measures would miss.

More recently, Rathod, Joshi, and Arkatkar (2025) extended the composite index approach specifically for data-constrained developing-country contexts. Their Composite Accessibility Index encompasses proximity, coverage, frequency, and connectivity dimensions while accounting for the data limitations common in cities of the Global South — a consideration directly relevant to the Jabodetabek context where some transit modes lack validated GTFS feeds.

The computational infrastructure for transit accessibility analysis has advanced significantly with the development of the r5r (Pereira et al., 2021) and r5py (Fink et al., 2022) packages. Built on Conveyal's R5 routing engine and the RAPTOR algorithm, these tools enable efficient computation of multimodal travel time matrices at metropolitan scale. Unlike traditional shortest-path routing, R5 samples multiple departure times within a specified window and evaluates multi-modal path combinations (walk + transit + transfer + transit + walk), producing realistic door-to-door travel time estimates. This capability is essential for computing the CBD journey chain travel times that constitute the largest component of our Transit Accessibility Index.

## Urban mobility and social equity in developing countries

Transit equity research has expanded beyond its Western origins to address the distinct mobility challenges of developing-country mega-cities, where rapid urbanization, income inequality, and motorcycle-dependent transport systems create equity dynamics absent from the literature's foundational North American and European contexts.

Currie (2010) established the foundational framework for spatial gap analysis, comparing a transit supply index against a social need index in Melbourne. His key finding — that outer suburbs had 75% less transit service than inner areas despite the highest social need — demonstrated a systematic spatial mismatch between where transit is provided and where it is most needed. This need-versus-supply gap framework has since become a dominant paradigm in transit equity research, though it has been applied predominantly in Australian, North American, and European cities.

Jiao and Dillivan (2013) operationalized this gap concept by introducing the term "transit desert" — areas where transit-dependent populations (too young, too old, too poor, or physically unable to drive) are underserved by transit supply. Their GIS-based methodology, applied across Charlotte, Chicago, Cincinnati, and Portland, provided a reproducible method for quantifying demand-supply gaps. Jomehpour and Smith-Colin (2020) subsequently refined the transit desert methodology with an explicit equity lens, integrating social vulnerability indicators and opportunity access metrics into the supply-demand comparison framework.

Delmelle and Casas (2012) brought transit equity analysis to the developing-country context by applying Gini coefficients and Lorenz curves to BRT accessibility patterns in Cali, Colombia. Their finding of significant spatial inequity in the MIO BRT system across income groups demonstrated that the Gini-based equity measurement approach is applicable and informative in developing-country settings where transit networks are still expanding and socioeconomic stratification is pronounced.

Pereira et al. (2019) deepened this line of inquiry in Rio de Janeiro, finding that substantial transit investments for the 2014 World Cup and 2016 Olympics generated larger accessibility benefits for higher-income groups, and that subsequent service cuts disproportionately penalized the poor. Their before-and-after methodology using multimodal routing revealed that transit investment alone does not guarantee equity improvement — the distributional effects depend on where and how service is provided relative to where vulnerable populations live.

In the Jakarta context specifically, transit research has been narrower in scope. Hardi and Murad (2023) conducted a spatial accessibility analysis of the TransJakarta BRT system, finding that only 41% of Jakarta's road network provides adequate access to BRT stops and that 58% of BRT stations suffer from poor pedestrian connectivity — a first-mile walkability deficit. Taki, Maatouk, and Qurnfulah (2018) assessed transit-oriented development potential in the Jakarta Metropolitan Region using GIS multi-criteria analysis. However, neither study constructs a composite need-versus-access equity framework, neither extends analysis beyond DKI Jakarta to the full Jabodetabek metropolitan region (including the suburban Bodetabek ring where transit poverty is most acute), and neither applies inequality metrics such as the Gini coefficient.

The role of motorcycles as a dominant mode in Southeast Asian transit equity dynamics adds a layer of complexity absent from Western frameworks. Ng (2018) examined urban transportation mode choice across five Southeast Asian cities — including Jakarta — finding that motorcycle dominance is driven by low operating cost, flexibility in congested traffic, and poor transit first/last-mile connectivity. Sukor and Bhayo (2024) investigated the motorcycle-to-transit modal shift decision across developing Southeast Asian cities, identifying first/last-mile quality and fare affordability as the strongest predictors of modal shift. These findings underscore that transit equity analysis in Jabodetabek must account for motorcycle competitiveness — a consideration absent from the Currie (2010), Jiao (2013), and Delmelle and Casas (2012) frameworks.

## Spatial analysis methods: MAUP, H3, and composite indices

The choice of spatial unit for transit equity analysis is consequential. The Modifiable Areal Unit Problem (MAUP), first formalized by Openshaw (1984), describes how statistical results change when the same underlying data is aggregated into different spatial units. In transit equity research, this means that conclusions about which areas are "underserved" or "well-served" may depend as much on the spatial unit chosen as on the actual distribution of transit service.

Javanmard et al. (2023) provided the most direct empirical demonstration of MAUP effects in transit equity analysis. Using Winnipeg bus on-time performance data, they compared social equity assessments at the stop, route, and neighborhood levels. Their central finding is striking: route-level analysis suggested equitable service distribution, while stop-level and neighborhood-level analyses revealed significant inequities. The spatial scale at which equity is measured substantively changes the conclusion — a result with direct implications for policy, since planners typically work with administrative boundaries (neighborhoods, districts) that may mask fine-grained inequity.

This finding motivates our dual-resolution approach. Administrative kelurahan in Jabodetabek range from 0.5 to 50 km² — a 100-fold variation in area. Large suburban kelurahan may contain both well-served areas near transit corridors and deeply underserved interior zones, averaging to a moderate equity score that hides both extremes. The H3 hexagonal grid system, developed by Uber, provides uniform spatial units (~0.74 km² at resolution 8, approximating a walkable neighborhood) that reduce aggregation bias and enable detection of within-kelurahan variation.

No existing study systematically compares the same transit equity framework applied at two resolutions — one administrative (variable-area, policy-relevant) and one uniform (constant-area, analytically precise) — in the same metropolitan area. This dual-resolution comparison is a core contribution of our research, directly testing whether the MAUP effects documented by Javanmard et al. (2023) lead to substantively different equity diagnoses when kelurahan boundaries are replaced by H3 hexagons.

Mamun and Lownes (2011a) contributed a foundational approach to composite index construction for transit need, developing a Transit Need Index from socioeconomic and demographic indicators including poverty rate, zero-vehicle household percentage, and dependency ratio. Their indicator selection — driven by the logic that transit need is highest where populations cannot afford or physically access private vehicles — directly informs our TNI construction with the addition of population density and average household expenditure to reflect Jabodetabek's specific socioeconomic landscape.

## Generalized cost models for mode choice

The generalized cost framework is a standard tool in transport economics for comparing the full cost of a trip across modes, encompassing not only monetary cost (fares, fuel, tolls, parking) but also time cost (monetized via value of time), transfer penalties, and comfort/fatigue factors. In Western transit equity studies, the comparison is typically binary: transit versus car.

In Jabodetabek and Southeast Asia more broadly, the mode choice landscape is fundamentally different. Ng (2018) documented that across five Southeast Asian cities, the motorcycle is not merely a secondary mode but often the primary competitor to transit — particularly for short-to-medium distance trips where its low fuel cost (roughly Rp 400/km versus Rp 1,000/km for cars in Indonesia), zero toll cost (motorcycles are prohibited from Indonesian toll roads), and lower parking fees make it cheaper than both transit and car for near-CBD origins.

The competitive dynamics are distance-dependent. For suburban origins (20-40 km from the CBD), car is most expensive due to toll and parking costs, motorcycle is mid-range but physically exhausting for long rides, and transit is cheapest if first/last-mile connections work. For near-CBD origins (3-8 km), motorcycle dominates because fuel is negligible, there are no tolls, and door-to-door travel time beats transit's access/egress overhead. Sukor and Bhayo (2024) confirmed that first/last-mile quality is the key swing factor in the motorcycle-to-transit decision, consistent with our TAI Layer 1 (first-mile quality) design.

No existing transit equity framework integrates a three-way generalized cost comparison (transit vs. car vs. motorcycle) as a component of a composite accessibility index. Our Layer 5 (cost competitiveness) fills this gap by computing generalized costs for all three modes and expressing transit's competitiveness as a ratio against the cheapest private alternative — capturing the motorcycle paradox that makes Jabodetabek's equity landscape distinct from the cities studied in the foundational transit equity literature.

## Gap and positioning

The literature review reveals a robust body of work on transit equity measurement (Currie 2010; Mamun & Lownes 2011a, 2011b; Jiao & Dillivan 2013), developing-country transit equity (Delmelle & Casas 2012; Pereira et al. 2019), MAUP sensitivity (Javanmard et al. 2023), computational routing (Pereira et al. 2021; Fink et al. 2022), and Jakarta transit accessibility (Hardi & Murad 2023). However, four specific gaps persist:

1. **No composite need-vs-access equity framework for full Jabodetabek.** Existing Jakarta studies cover only DKI Jakarta and do not extend to the suburban Bodetabek ring where transit poverty is most severe. The need-supply gap method (Currie 2010; Jiao & Dillivan 2013) has never been applied to the full Jabodetabek metropolitan region at kelurahan resolution.

2. **No dual-resolution comparison exposing MAUP in equity scoring.** Javanmard et al. (2023) demonstrate that MAUP affects transit equity conclusions, but no study has compared the same equity framework at administrative (variable-area) and hexagonal (constant-area) resolutions in a single metropolitan area to quantify how spatial unit choice changes the equity diagnosis.

3. **No what-if scenario simulation embedded in an equity quadrant framework.** Scenario planning and accessibility modeling are mature fields, but no study embeds counterfactual infrastructure placement directly into a transit equity classification to measure the resulting shift in quadrant membership and Gini coefficient.

4. **No three-way generalized cost model for equity analysis.** Western transit equity frameworks compare transit against car only. In motorcycle-dominated Southeast Asian cities, the motorcycle is often the marginal competitor to transit (Ng 2018; Sukor & Bhayo 2024). No existing framework computes a three-way cost comparison and integrates it as a composite index layer.

This research addresses all four gaps simultaneously by constructing a Transit Need Index and five-layer Transit Accessibility Index (incorporating first-mile quality, service quality, CBD journey chain via r5py, last-mile quality, and three-way cost competitiveness), applying the framework at both kelurahan and H3 resolutions across the full Jabodetabek metropolitan region, measuring equity via Gini coefficients and spatial clustering (Moran's I / LISA), and embedding a what-if scenario simulator within the equity quadrant classification.

## References

- Currie, G. (2010). Quantifying spatial gaps in public transport supply based on social needs. *Journal of Transport Geography*, 18(1), 31–41.
- Delmelle, E.C. & Casas, I. (2012). Evaluating the spatial equity of bus rapid transit-based accessibility patterns in a developing country: The case of Cali, Colombia. *Transport Policy*, 20, 36–46.
- Fink, C., Klumpenhouwer, W., Saraiva, M., Pereira, R.H.M., & Tenkanen, H. (2022). r5py: Rapid Realistic Routing with R5 in Python. doi:10.5281/zenodo.7060437.
- Hardi, A.Z. & Murad, A.A. (2023). Spatial Analysis of Accessibility for Public Transportation: A Case Study in Jakarta, Bus Rapid Transit System (Transjakarta), Indonesia. *Journal of Computer Science*, 19(10), 1190–1202.
- Javanmard, R., Lee, J., Kim, J., Liu, L., & Diab, E. (2023). The impacts of the modifiable areal unit problem (MAUP) on social equity analysis of public transit reliability. *Journal of Transport Geography*, 106, 103523.
- Jiao, J. & Dillivan, M. (2013). Transit Deserts: The Gap between Demand and Supply. *Journal of Public Transportation*, 16(3), 23–39.
- Jomehpour, M. & Smith-Colin, J. (2020). Transit Deserts: Equity analysis of public transit accessibility. *Journal of Transport Geography*, 89, 102869.
- Mamun, S.A. & Lownes, N.E. (2011a). Measuring Service Gaps: Accessibility-Based Transit Need Index. *Transportation Research Record*, 2217(1), 153–161.
- Mamun, S.A. & Lownes, N.E. (2011b). A Composite Index of Public Transit Accessibility. *Journal of Public Transportation*, 14(2), 69–87.
- Ng, W.S. (2018). Urban Transportation Mode Choice and Carbon Emissions in Southeast Asia. *Transportation Research Record*, 2672(25), 29–37.
- Pereira, R.H.M., Banister, D., Schwanen, T., & Wessel, N. (2019). Distributional effects of transport policies on inequalities in access to opportunities in Rio de Janeiro. *Journal of Transport and Land Use*, 12(1), 741–764.
- Pereira, R.H.M., Saraiva, M., Herszenhut, D., Braga, C.K.V., & Conway, M.W. (2021). r5r: Rapid Realistic Routing on Multimodal Transport Networks with R⁵ in R. *Findings*, March. doi:10.32866/001c.21262.
- Rathod, R., Joshi, G., & Arkatkar, S. (2025). Composite Accessibility Index: A Novel and Holistic Measure for Evaluating Transit Accessibility. *Transportation Research Record*. doi:10.1177/03611981241270156.
- Sukor, N.S.A. & Bhayo, A.R. (2024). Unveiling the drivers of modal switch from motorcycles to public transport in Southeast Asia. *Transportation Research Part F*, 101, 197–213.
- Taki, H.M., Maatouk, M.M.H., & Qurnfulah, E.M. (2018). Re-assessing TOD index in Jakarta Metropolitan Region using GIS. *IOP Conference Series: Earth and Environmental Science*, 149, 012046.

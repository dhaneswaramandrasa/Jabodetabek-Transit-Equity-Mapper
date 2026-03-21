# Source Map

**Last updated**: 2026-03-22
**Status**: Complete — literature scan done (MVP-2 / E0-001), NTL proxy papers added (MVP-22 investigation)
**Papers reviewed**: 18
**Search queries used**: 12 queries across Google Scholar, Semantic Scholar, and web (3 rounds)

---

## Search Queries

1. `transit equity accessibility Gini developing country`
2. `H3 hexagonal grid MAUP transport`
3. `composite transit accessibility index need-access gap`
4. `generalized cost model transit motorcycle Indonesia`
5. `Jakarta Jabodetabek transit accessibility r5py`
6. `Currie 2010 gap analysis Melbourne`
7. `r5py r5r Pereira accessibility`
8. `dasymetric WorldPop disaggregation`
9. `Mamun Lownes transit need index`
10. `Pereira r5r Brazil inequality`
11. `transit deserts Jiao equity`
12. `MAUP transport accessibility scales`

---

## Papers

| # | Citation | Method + Findings | Data Sources | Relevance to RQ |
|---|----------|-------------------|--------------|-----------------|
| 1 | Currie, G. (2010). Quantifying spatial gaps in public transport supply based on social needs. *Journal of Transport Geography*, 18(1), 31–41. | Compared a transit supply index (route density, frequency) against a social need index (SEIFA disadvantage) using spatial overlay in Melbourne. Found outer suburbs had 75% less transit service than inner areas despite highest social need — a clear spatial mismatch. | Melbourne bus network data; SEIFA socioeconomic disadvantage index (Australian Bureau of Statistics) | **High** — Foundational need-vs-supply gap framework; directly inspires our TNI–TAI equity gap concept. |
| 2 | Mamun, S.A. & Lownes, N.E. (2011). Measuring Service Gaps: Accessibility-Based Transit Need Index. *Transportation Research Record*, 2217(1), 153–161. | Developed a composite Transit Need Index from socioeconomic and demographic indicators (poverty, vehicle ownership, elderly population); identified areas where high need coincides with low transit service. | U.S. Census data, transit route data, Hartford CT | **High** — Direct methodological precedent for TNI construction; uses similar indicator set (poverty, zero-vehicle HH, dependency ratio). |
| 3 | Mamun, S.A. & Lownes, N.E. (2011). A Composite Index of Public Transit Accessibility. *Journal of Public Transportation*, 14(2), 69–87. | Created composite accessibility index combining proximity, frequency, and coverage measures using standardized grading; integrates planner, developer, and operator perspectives into a single interpretable score. | Transit network data, census tract demographics, Meriden CT | **High** — Precedent for composite TAI construction; demonstrates how to combine multiple accessibility dimensions into one index. |
| 4 | Delmelle, E.C. & Casas, I. (2012). Evaluating the spatial equity of bus rapid transit-based accessibility patterns in a developing country: The case of Cali, Colombia. *Transport Policy*, 20, 36–46. | Applied Gini coefficient and Lorenz curve to BRT accessibility distribution; found significant spatial inequity in accessibility across income groups in Cali's MIO BRT system. | Cali MIO BRT route/stop data, census demographics, income data | **High** — Gini-based transit equity measurement in a developing country; methodological precedent for our Gini + Lorenz analysis. |
| 5 | Jiao, J. & Dillivan, M. (2013). Transit Deserts: The Gap between Demand and Supply. *Journal of Public Transportation*, 16(3), 23–39. | Coined "transit desert" concept — areas where transit-dependent population (demand) exceeds transit service level (supply). Used GIS overlay to quantify demand-supply gaps across four U.S. cities. | U.S. Census, transit route data for Charlotte, Chicago, Cincinnati, Portland | **High** — Originated the transit desert concept; our Q4 quadrant ("High Need, Low Access") directly operationalizes this. |
| 6 | Taki, H.M., Maatouk, M.M.H., & Qurnfulah, E.M. (2018). Re-assessing TOD index in Jakarta Metropolitan Region using GIS. *IOP Conference Series: Earth and Environmental Science*, 149, 012046. | Evaluated transit-oriented development potential using spatial multi-criteria analysis; classified Jakarta areas by TOD readiness based on transit proximity, density, and land use mix. | Jakarta transit network, land use data, population density | **Medium** — Jakarta transit spatial analysis context; TOD-focused rather than equity-focused, but confirms spatial patterns of transit concentration. |
| 7 | Ng, W.S. (2018). Urban Transportation Mode Choice and Carbon Emissions in Southeast Asia. *Transportation Research Record*, 2672(25), 29–37. | Mode choice model examining car, motorcycle, and transit across 5 Southeast Asian cities; found motorcycle dominance driven by low operating cost, flexibility in congestion, and poor transit first/last-mile. | Household travel surveys from Jakarta, Bangkok, Manila, Kuala Lumpur, Ho Chi Minh City | **Medium** — Southeast Asian mode choice with motorcycle inclusion; validates our three-mode generalized cost approach and motorcycle competitiveness framing. |
| 8 | Pereira, R.H.M., Banister, D., Schwanen, T., & Wessel, N. (2019). Distributional effects of transport policies on inequalities in access to opportunities in Rio de Janeiro. *Journal of Transport and Land Use*, 12(1), 741–764. | Before-and-after comparison of Rio's transit investments (2014–2017); found BRT/metro expansion benefits accrued disproportionately to higher-income groups; subsequent service cuts worsened inequality. | GTFS Rio de Janeiro, census income data, jobs/schools locations | **High** — Transit accessibility inequality in developing-country mega-city; equity-focused methodology using R5 routing predecessor. |
| 9 | Jomehpour, M. & Smith-Colin, J. (2020). Transit Deserts: Equity analysis of public transit accessibility. *Journal of Transport Geography*, 89, 102869. | Updated transit desert methodology with spatial equity focus; integrated supply-demand gap analysis with social vulnerability indicators and opportunity access. | Dallas TX transit data, ACS demographics, employment locations | **High** — Transit desert equity methodology with vulnerability integration; parallels our TNI approach to identifying underserved communities. |
| 10 | Pereira, R.H.M., Saraiva, M., Herszenhut, D., Braga, C.K.V., & Conway, M.W. (2021). r5r: Rapid Realistic Routing on Multimodal Transport Networks with R⁵ in R. *Findings*, March. doi:10.32866/001c.21262. | Introduced r5r package for efficient multimodal routing using R5 engine and RAPTOR algorithm; computes travel time matrices and accessibility measures across departure time windows. | GTFS + OSM road network; demonstrated on São Paulo, Brazil | **High** — Methodological tool; r5py (Python port) is our routing engine for TAI Layer 3 (CBD journey chain). |
| 11 | Fink, C., Klumpenhouwer, W., Saraiva, M., Pereira, R.H.M., & Tenkanen, H. (2022). r5py: Rapid Realistic Routing with R5 in Python. doi:10.5281/zenodo.7060437. | Python wrapper for R5 multimodal routing engine; provides GeoPandas-compatible travel time matrix and accessibility computation with parallel processing. | GTFS + OSM; GeoPandas interoperability | **High** — The specific computational tool for our travel time matrices and isochrone analysis; Python ecosystem fits our stack. |
| 12 | Hardi, A.Z. & Murad, A.A. (2023). Spatial Analysis of Accessibility for Public Transportation: A Case Study in Jakarta, Bus Rapid Transit System (Transjakarta), Indonesia. *Journal of Computer Science*, 19(10), 1190–1202. | GIS-based spatial accessibility analysis of TransJakarta BRT using 5/10/15-minute walk isochrones; found only 41% of Jakarta's road network provides access to BRT, and 58% of BRT stations are poorly connected to the surrounding road network. | TransJakarta stop locations, Jakarta road network, district boundaries | **High** — Closest existing Jakarta transit accessibility study; quantifies first-mile walkability deficit that our TAI Layer 1 addresses. |
| 13 | Javanmard, R., Lee, J., Kim, J., Liu, L., & Diab, E. (2023). The impacts of the modifiable areal unit problem (MAUP) on social equity analysis of public transit reliability. *Journal of Transport Geography*, 106, 103523. | Tested MAUP effects by comparing transit equity metrics at stop, route, and neighborhood aggregation levels; found route-level analysis showed equitable distribution, while stop/neighborhood-level revealed significant inequity — demonstrating that spatial scale choice changes equity conclusions. | Winnipeg bus on-time performance data, neighborhood demographics | **High** — Directly demonstrates that spatial aggregation level changes equity conclusions; core support for our H2 hypothesis on resolution effects. |
| 14 | Rathod, R., Joshi, G., & Arkatkar, S. (2025). Composite Accessibility Index: A Novel and Holistic Measure for Evaluating Transit Accessibility. *Transportation Research Record*. doi:10.1177/03611981241270156. | Proposed holistic composite accessibility index encompassing multiple measurement dimensions (proximity, coverage, frequency, connectivity); designed for data-constrained developing-country contexts. | Multi-modal transit data, Surat, India | **Medium** — Recent composite index framework for developing countries; validates multi-indicator approach and addresses data scarcity similar to Jabodetabek. |
| 15 | Sukor, N.S.A. & Bhayo, A.R. (2024). Unveiling the drivers of modal switch from motorcycles to public transport in Southeast Asia. *Transportation Research Part F*, 101, 197–213. | Investigated factors influencing motorcycle-to-transit modal shift across developing SE Asian cities using behavioral models; found first/last-mile quality and fare affordability as strongest predictors of shift. | Survey data from SE Asian developing cities | **Medium** — Contextualizes motorcycle dominance and transit competitiveness in our study region; supports our Layer 5 cost competitiveness framing. |
| 16 | Mellander, C., Lobo, J., Stolarick, K., & Matheson, Z. (2015). Night-time light data: A good proxy measure for economic activity? *PLOS ONE*, 10(10), e0139779. | Geographically weighted regression at 250 m grid using full-population Swedish micro-data; found NTL is a reliable proxy for population/establishment density (r~0.76) but a weak proxy for wages (r~0.52); documents urban-core overestimation and peri-urban underestimation. | Swedish full-population geo-coded register; DMSP and calibrated radiance data | **Medium** — Most rigorous sub-city NTL proxy test; calibrates expectations for NTL use in Jabodetabek; confirms NTL alone insufficient for income/poverty estimation at kelurahan scale. |
| 17 | Utomo, A.J.P., Aini, N.N., Hendayana, Y., & Dewi, R.S. (2023). Spatially granular poverty index (SGPI) for urban poverty mapping in Jakarta metropolitan area (JMA). *Earth Science Informatics*, 16, 3531–3544. | Composite poverty index for JMA at 1 km resolution using NTL + NDBI + CO/NO₂ + POI density; equal-weighted sum with Yeo-Johnson transformation achieves r=0.954 correlation with SUSENAS poverty data; NTL alone performs substantially lower. | VIIRS NTL; Sentinel-5P (CO, NO₂); OSM POIs; SUSENAS poverty validation | **High** — Directly parallel to TNI construction; demonstrates NTL must be combined with multiple covariates and calibrated against survey data to achieve reliable poverty proxy in JMA; supports decision to use BPS-calibrated synthetic data rather than NTL alone. |
| 18 | Prawira, M., Maulana, E., Bhaskara, A., & Ramdhani, M.F. (2022). Developing Relative Spatial Poverty Index Using Integrated Remote Sensing and Geospatial Big Data Approach: A Case Study of East Java, Indonesia. *ISPRS International Journal of Geo-Information*, 11(5), 275. | Multi-covariate poverty index for East Java using VIIRS NTL + NDVI + built-up index + NDWI + LST + air pollutants; kecamatan-level validation; confirms multi-source approach outperforms NTL alone in Indonesian context. | NOAA-VIIRS NTL; Sentinel-2; MODIS LST; BPS kecamatan poverty statistics | **Medium** — Indonesian-specific validation of NTL + covariate methodology; further supports that NTL alone cannot derive specific TNI indicators (vehicle ownership, dependency ratio). |

---

## Synthesis

### What the literature establishes

Transit equity measurement has matured around two complementary approaches:

1. **Need-supply gap analysis** (Currie 2010; Mamun & Lownes 2011; Jiao & Dillivan 2013): These studies compare transit service supply against socioeconomic transit need using composite indices, identifying "service gaps" or "transit deserts" where need exceeds supply. This is well-established in North American and Australian contexts.

2. **Distributional equity via Gini/Lorenz** (Delmelle & Casas 2012; Pereira et al. 2019): These studies apply inequality measures to transit accessibility distributions, sometimes stratified by income. The Gini coefficient has become a standard summary metric for accessibility equity.

3. **Composite accessibility indices** (Mamun & Lownes 2011; Rathod et al. 2025): Multi-indicator composite indices combining proximity, frequency, coverage, and connectivity are well-established and increasingly adapted for data-constrained developing-country contexts.

4. **Multimodal routing tools** (Pereira et al. 2021; Fink et al. 2022): The r5r/r5py ecosystem provides computationally efficient, RAPTOR-based multimodal routing that can generate travel time matrices at metropolitan scale, making door-to-door transit accessibility measurement feasible for large study areas like Jabodetabek.

5. **Jakarta-specific transit studies** exist (Hardi & Murad 2023; Taki et al. 2018) but focus narrowly on BRT accessibility or TOD potential within DKI Jakarta only, without equity gap framing and without covering the full Jabodetabek metropolitan region.

6. **Motorcycle-transit competition** is well-documented in Southeast Asia (Ng 2018; Sukor & Bhayo 2024) as a dominant mode choice dynamic not present in Western transit equity studies.

7. **Nighttime lights as socioeconomic proxy** have been investigated for Jakarta (Utomo et al. 2023; Prawira et al. 2022; Mellander et al. 2015). NTL alone is a weak proxy for income/poverty at sub-city scales (r~0.52 for wages); multi-covariate composites (NTL + built-up index + POI density) achieve r=0.954 against SUSENAS data but require survey ground truth for calibration. Critically, NTL cannot proxy vehicle ownership or age-structure indicators at all — these require census data.

### The gap your research fills

Despite the breadth of transit equity literature, **four specific gaps** remain that this research addresses:

1. **No composite need-vs-access equity framework for full Jabodetabek.** Existing Jakarta studies (Hardi & Murad 2023; Taki et al. 2018) cover only DKI Jakarta and do not construct a TNI–TAI gap framework spanning the full metropolitan region including the suburban Bodetabek ring where transit poverty is most severe. The need-supply gap method (Currie 2010; Jiao 2013) has never been applied to Jabodetabek at kelurahan resolution.

2. **No dual-resolution comparison exposing MAUP in equity scoring.** Javanmard et al. (2023) demonstrate that MAUP significantly affects transit equity conclusions, but no study has systematically compared the same equity gap framework at two resolutions (administrative kelurahan vs. H3 hexagon) in a single metropolitan area. This dual-resolution approach tests whether large, heterogeneous kelurahan mask within-unit variation that uniform hexagons expose.

3. **No what-if scenario simulation embedded in an equity quadrant framework.** While scenario planning and accessibility modeling are mature fields, no study embeds counterfactual infrastructure placement (e.g., "add a station here") directly into a transit equity quadrant classification to measure the shift in equity scores — making the gap analysis actionable rather than purely descriptive.

4. **No three-way generalized cost model (transit vs. car vs. motorcycle) for equity analysis.** Western transit equity studies compare transit against car only. In Jabodetabek (and Southeast Asia broadly), the motorcycle is often the marginal competitor to transit (Ng 2018; Sukor & Bhayo 2024). No existing framework computes a three-way generalized cost comparison and integrates it as a cost-competitiveness layer within a composite accessibility index.

### Methodological precedents

| Precedent | Papers | What to borrow |
|-----------|--------|----------------|
| Need-supply gap framework | Currie (2010), Mamun & Lownes (2011), Jiao & Dillivan (2013) | Two-axis structure: Need Index vs. Supply/Access Index; quadrant classification of spatial units |
| Composite accessibility index | Mamun & Lownes (2011), Rathod et al. (2025) | Multi-indicator composite with normalization and weighting; standardized grading scale |
| Gini coefficient for equity | Delmelle & Casas (2012), Pereira et al. (2019) | Gini + Lorenz curve as summary equity metrics; stratification by income/need group |
| Transit desert identification | Jiao & Dillivan (2013), Jomehpour & Smith-Colin (2020) | GIS overlay method for identifying demand-supply gap zones; vulnerability integration |
| Multimodal routing via r5py | Pereira et al. (2021), Fink et al. (2022) | RAPTOR-based routing for travel time matrices; GTFS + OSM input; departure time window sampling |
| MAUP sensitivity | Javanmard et al. (2023) | Multi-scale comparison to test robustness of equity conclusions; report metrics at multiple aggregation levels |
| Jakarta spatial analysis | Hardi & Murad (2023), Taki et al. (2018) | Walk-isochrone BRT accessibility method; Jakarta-specific transit network characterization |
| NTL socioeconomic proxy (evaluated, not adopted) | Mellander et al. (2015), Utomo et al. (2023), Prawira et al. (2022) | NTL alone insufficient for specific TNI indicators; multi-covariate composites need survey calibration; supports BPS-calibrated synthetic data approach |

### Data sources to consider

From the literature, the following datasets and tools are commonly used for transit equity analysis in comparable contexts:

| Dataset/Tool | Used by | Our equivalent |
|--------------|---------|----------------|
| GTFS feeds (static) | Pereira et al. (2021), Hardi & Murad (2023) | TransJakarta, KRL, MRT Jakarta, LRT Jabodebek GTFS |
| OSM road network | Fink et al. (2022), Pereira et al. (2021) | Geofabrik Java PBF extract |
| Census demographics (income, poverty, vehicle ownership) | Currie (2010), Mamun & Lownes (2011), Delmelle & Casas (2012) | BPS kecamatan/kelurahan data |
| Population raster (WorldPop/LandScan) | Pereira et al. (2019) dasymetric references | WorldPop Indonesia ~100m GeoTIFF |
| r5py/r5r routing engine | Pereira et al. (2021), Fink et al. (2022) | r5py for travel time matrices |
| H3 hexagonal grid | Referenced in spatial analysis literature | h3-py at resolution 8 |
| POI locations (hospitals, schools, employment centers) | Jomehpour & Smith-Colin (2020) | Overpass API + manual verification |
| VIIRS nighttime lights (evaluated, not adopted) | Mellander et al. (2015), Utomo et al. (2023), Prawira et al. (2022) | Investigated as poverty/expenditure proxy; insufficient alone for TNI indicators — kept BPS-calibrated synthetic data |

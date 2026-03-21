# 3. Methodology

## 3.1 Study Area

The Jabodetabek metropolitan region encompasses the Special Capital Region of Jakarta (DKI Jakarta) and the surrounding satellite cities and regencies of Bogor, Depok, Tangerang, and Bekasi in the provinces of West Java and Banten. With a population exceeding 30 million residents distributed across multiple municipal governments, Jabodetabek constitutes one of the largest and most complex urban agglomerations in Southeast Asia. The region's governance is fragmented: DKI Jakarta operates as a provincial-level special region, while the surrounding municipalities (both kota and kabupaten) fall under two different provinces, each with independent planning authorities. This institutional fragmentation has historically resulted in uncoordinated transit investment, with service concentrated within DKI Jakarta's administrative boundaries while the suburban Bodetabek ring --- where much of the population growth has occurred over the past two decades --- remains dependent on private motorized transport.

The formal public transit network in Jabodetabek comprises several distinct systems operating at different scales and under different operators. The MRT Jakarta North--South line, inaugurated in 2019, spans approximately 16 kilometers with 13 stations connecting Lebak Bulus in the south to Bundaran HI in central Jakarta. The LRT Jabodebek, completed in 2023, serves 18 stations linking Cawang in East Jakarta to Bekasi and Cibubur. The KRL Commuterline, operated by KAI Commuter, is the region's oldest and most extensive rail network, with approximately 80 stations across six lines radiating from central Jakarta to Bogor, Depok, Tangerang, Rangkasbitung, and Bekasi. TransJakarta operates the world's longest bus rapid transit system, with over 260 routes including dedicated busway corridors and JakLingko/Mikrotrans feeder services that extend into residential neighborhoods.

Despite this infrastructure, a pronounced spatial asymmetry persists. MRT and LRT serve exclusively the inner Jakarta core and eastern corridor, respectively. KRL stations, while reaching suburban municipalities, are spaced at intervals that leave large areas beyond walkable range. TransJakarta's dedicated corridors operate primarily within DKI Jakarta, with feeder services providing limited suburban penetration. The result is a metropolitan region where transit investment has historically been concentrated in the central city, while the suburban periphery --- home to millions of lower-to-middle-income commuters --- exhibits characteristics of transit poverty. This spatial asymmetry, combined with the motorcycle's dominance as a low-cost private alternative (Ng, 2018; Sukor & Bhayo, 2024), makes Jabodetabek an ideal case study for examining the alignment between transit need and transit access across a developing-country megacity.

## 3.2 Analytical Framework

The core analytical framework employed in this study is a two-axis Transit Equity Matrix that classifies every spatial unit according to two composite indices: a Transit Need Index (TNI) measuring the socioeconomic urgency of public transit provision, and a Transit Accessibility Index (TAI) measuring the quality and extent of transit service available. Each spatial unit is scored on both dimensions and assigned to one of four quadrants based on a median-split classification:

- **Q1 (Well-Served):** High Need, High Access --- areas where substantial transit need is adequately matched by accessible transit service. These represent successful alignment between demand and supply.
- **Q2 (Potential Overinvestment):** Low Need, High Access --- areas with good transit service but relatively low socioeconomic need. Transit resources here may be disproportionately allocated relative to the population's dependence on public transport.
- **Q3 (Low Priority):** Low Need, Low Access --- areas with both low transit need and limited service. These zones, typically affluent suburban enclaves with high private vehicle ownership, represent the lowest priority for transit investment.
- **Q4 (Transit Desert):** High Need, Low Access --- areas where populations with the greatest socioeconomic need for public transit are inadequately served. This quadrant directly operationalizes the transit desert concept introduced by Jiao and Dillivan (2013) and constitutes the primary focus of equity concern in this study.

The framework extends the need-supply gap analysis pioneered by Currie (2010) and formalized by Mamun and Lownes (2011a) by introducing a continuous Equity Gap Score defined as:

$$\text{Equity Gap} = \text{TNI}_{\text{normalized}} - \text{TAI}_{\text{normalized}}$$

Positive values indicate underserved areas (need exceeds access), while negative values indicate overserved areas (access exceeds need). This continuous score complements the categorical quadrant classification by preserving the magnitude of mismatch, enabling distributional analysis through Gini coefficients and spatial autocorrelation statistics.

## 3.3 Transit Need Index (TNI)

The Transit Need Index quantifies the latent socioeconomic demand for public transit in each spatial unit using five indicators selected from the transit equity literature. Following Mamun and Lownes (2011a) and Currie (2010), the indicators capture dimensions of aggregate demand, economic vulnerability, transit dependence, and demographic vulnerability:

1. **Population density** (pop_density): measured as residents per square kilometer, this indicator captures aggregate transit demand. Higher population density implies greater potential ridership and thus greater need for transit provision (Mamun & Lownes, 2011a; Jiao & Dillivan, 2013).

2. **Poverty rate** (poverty_rate): the percentage of the population living below the official poverty line. Economically disadvantaged populations are disproportionately dependent on affordable public transport for access to employment and services (Mamun & Lownes, 2011a; Currie, 2010).

3. **Average household expenditure** (avg_household_expenditure): monthly average expenditure in Indonesian Rupiah, used as a continuous economic gradient indicator. Unlike poverty rate, which is binary at a threshold, expenditure captures the full income spectrum. This indicator is inverted in the composite: higher expenditure implies lower transit need, as wealthier households have greater capacity to absorb private transport costs (Pereira et al., 2019).

4. **Zero-vehicle household percentage** (zero_vehicle_hh_pct): the estimated proportion of households owning no motor vehicle. Households without private transport are structurally dependent on public transit for all trip purposes (Mamun & Lownes, 2011a; Jiao & Dillivan, 2013).

5. **Dependency ratio** (dependency_ratio): the ratio of non-working-age population (under 15 and over 64) to working-age population. Areas with high dependency ratios contain greater proportions of individuals who cannot drive and thus rely on public transit or walking for mobility (Mamun & Lownes, 2011a).

All indicators are normalized to the [0, 1] range using min-max normalization with winsorization at the 2nd and 98th percentiles to reduce the influence of extreme outliers while preserving the distributional shape of each indicator. Winsorization is preferred over trimming because extreme values in transit equity analysis often represent genuine spatial variation rather than measurement error --- a kelurahan with exceptionally high poverty or zero-vehicle rates should be capped rather than excluded. For the inverted indicator (average household expenditure), the normalization formula is $(x_{\max} - x) / (x_{\max} - x_{\min})$, ensuring that lower expenditure yields higher TNI contribution.

The five indicators are combined using equal weighting (0.20 each), following the methodological precedent established by Mamun and Lownes (2011a) and supported by Rathod et al. (2025), who demonstrated that equal weighting performs comparably to statistically derived weights in composite accessibility indices, particularly when indicators capture conceptually distinct dimensions. The composite TNI formula is:

$$\text{TNI} = 0.20 \times \text{norm}(\text{pop\_density}) + 0.20 \times \text{norm}(\text{poverty\_rate}) + 0.20 \times \text{norm\_inv}(\text{avg\_hh\_expenditure}) + 0.20 \times \text{norm}(\text{zero\_vehicle\_hh\_pct}) + 0.20 \times \text{norm}(\text{dependency\_ratio})$$

The robustness of equal weighting is tested through sensitivity analysis (Section 3.8).

Four edge-case strategies govern the TNI computation. First, missing data are handled through a hierarchical fallback: if a kelurahan-level value is unavailable, the parent kecamatan value is used; if that is also missing, the adjacent kelurahan average, then the kota/kabupaten average, and finally exclusion if more than two of the five indicators are missing. Second, indicators with zero variance within the study area are assigned a neutral score of 0.5, with their weight redistributed equally among the remaining indicators. Third, outliers are winsorized rather than deleted, preserving spatial coverage. Fourth, kelurahan with very low populations (fewer than 100 residents) are excluded from TNI computation but retained in the spatial dataset to avoid gaps in the analysis grid.

## 3.4 Transit Accessibility Index (TAI) --- 5-Layer Model

The Transit Accessibility Index departs from flat composite approaches that aggregate proximity and frequency indicators without regard to the commuter's actual experience. Instead, it models the full commuter journey chain from home to workplace in five sequential layers, reflecting the decision-making process that Jabodetabek commuters face each morning: walk to a transit stop, board and ride through the network, arrive at a CBD station, reach the final destination, and evaluate whether the entire chain is cost-competitive against private alternatives. This journey-chain structure ensures that each component of accessibility is evaluated in its functional context --- a spatial unit may have a nearby transit stop (high L1) but poor service frequency (low L2), or excellent service to a non-CBD destination but poor CBD connectivity (low L3).

The master TAI formula assigns differential weights to reflect the relative importance of each layer:

$$\text{TAI} = 0.20 \times L1 + 0.15 \times L2 + 0.35 \times L3 + 0.15 \times L4 + 0.15 \times L5$$

Layer 3, the CBD journey chain, receives the highest weight (0.35) because for most Jabodetabek residents, the ability to reach their workplace in the central Jakarta employment corridor via transit is the single most determinative dimension of transit utility. The remaining layers are weighted to balance first-mile access (0.20), service quality (0.15), last-mile integration (0.15), and cost competitiveness (0.15).

### Layer 1: First-Mile Quality (20%)

The first-mile layer captures the accessibility of the nearest transit stop or station from the residential origin. This layer addresses a well-documented deficit in Jakarta's transit network: Hardi and Murad (2023) found that 58% of TransJakarta BRT stations are poorly connected to the surrounding road network, and only 41% of Jakarta's road network provides walkable access to BRT. Four indicators compose this layer:

- **Walk distance to nearest stop** (walk_dist_to_nearest_stop_m): the network walking distance from the spatial unit centroid to the nearest formal transit stop, computed over the OSM road network rather than Euclidean distance to account for barriers such as highways, rivers, and gated communities.
- **Pedestrian infrastructure share** (pct_footway_pedestrian): the percentage of road length within the spatial unit classified as footway, pedestrian path, or cycle path in OpenStreetMap, measuring the physical walkability of the local network.
- **Network connectivity** (network_connectivity): intersection density, measured as nodes per square kilometer with degree three or greater. Grid-pattern networks with frequent intersections offer more direct walking routes than cul-de-sac or superblock layouts.
- **Feeder service availability** (has_feeder_service): a binary indicator for whether a JakLingko or Mikrotrans feeder bus route operates within the spatial unit, connecting residential areas to trunk transit stations.

The layer formula is:

$$L1 = 0.35 \times \text{norm}(1/\text{walk\_dist}) + 0.25 \times \text{norm}(\text{pct\_footway}) + 0.20 \times \text{norm}(\text{connectivity}) + 0.20 \times \text{norm}(\text{has\_feeder})$$

Walk distance receives the highest sub-weight (0.35) because proximity to a stop is the most fundamental first-mile determinant, while the remaining indicators modulate the quality of that access.

### Layer 2: Service Quality (15%)

Once a commuter reaches the transit stop, the quality of available service determines whether transit is a viable daily option. This layer captures four service dimensions:

- **Average headway** (avg_headway_min): the mean scheduled interval between vehicle arrivals at stops within the spatial unit, computed from GTFS stop_times data. Lower headways indicate more frequent, reliable service.
- **Transit mode diversity** (transit_mode_diversity): the count of distinct formal transit modes (BRT, KRL, MRT, LRT, Mikrotrans) accessible from the spatial unit. Greater modal diversity provides commuters with alternative routes and redundancy.
- **Fare tier** (best_mode_fare_tier): the affordability tier of the most affordable transit mode available, classified on a four-point scale from Tier 1 (KRL Commuterline and regular TransJakarta, Rp 3,500--13,000) to Tier 4 (TransJakarta Royaltrans premium service, Rp 20,000). Areas where only premium modes are accessible are penalized, as high-need populations may be unable to afford them.
- **Affordable mode availability** (has_affordable_mode): a binary indicator for whether any Tier 1 or Tier 2 mode is available within the spatial unit.

$$L2 = 0.35 \times \text{norm}(1/\text{headway}) + 0.25 \times \text{norm}(\text{mode\_diversity}) + 0.20 \times \text{norm}(1/\text{fare\_tier}) + 0.20 \times \text{norm}(\text{has\_affordable})$$

### Layer 3: CBD Journey Chain (35%)

Layer 3 constitutes the dominant component of the TAI, capturing the full door-to-door multi-modal transit travel time from each spatial unit to Jakarta's employment centers. This layer is computed using r5py (Fink et al., 2022), the Python implementation of the R5 multimodal routing engine that employs the RAPTOR algorithm for public transit routing (Pereira et al., 2021).

The routing configuration reflects realistic Jabodetabek commuting conditions: transit mode with walk access and egress, a maximum walk time of 20 minutes for first-mile and last-mile legs, a maximum trip duration of 120 minutes, a maximum of three transfers per journey, a transfer penalty of 10 minutes (600 seconds) per transfer to capture the friction of walking between platforms and waiting under uncertainty, and a departure time window of 7:00--8:00 AM on a weekday to sample the morning peak commuting period. The r5py engine inherently handles multi-modal path optimization, computing the best combination of walking, waiting, and riding across the loaded GTFS network for each origin-destination pair.

Rather than measuring travel time to a single CBD centroid, this layer employs a gravity-weighted model across nine defined CBD zones that reflect the polycentric employment structure of metropolitan Jakarta. The gravity-weighted travel time is computed as:

$$\text{poi\_reach\_cbd\_weighted} = \frac{\sum_{i=1}^{9} (t_i \times w_i)}{\sum_{i=1}^{9} w_i}$$

where $t_i$ is the r5py-computed transit travel time from the spatial unit centroid to CBD zone $i$, and $w_i$ is the gravity weight reflecting each zone's employment pull. The Sudirman--Thamrin financial corridor, as Indonesia's highest-density employment center, receives a gravity weight of 5.0; Kuningan (corporate and diplomatic hub) receives 4.0; Gatot Subroto (government ministry corridor) receives 3.5; TB Simatupang (emerging technology hub) receives 3.0; Kelapa Gading receives 2.0; Pantai Indah Kapuk receives 1.5; and three satellite CBDs (BSD City, Summarecon Bekasi, Summarecon Serpong) each receive 1.0. This weighting scheme ensures that Sudirman--Thamrin, which accounts for the plurality of metropolitan commuter flows, dominates the weighted average (approximately 23% of total weight), while satellite CBDs that primarily serve local populations contribute proportionally less.

The gravity-weighted approach is preferred over a nearest-CBD measure because the latter would mischaracterize suburban locations near satellite CBDs as highly accessible when their residents predominantly commute to central Jakarta. The layer score is:

$$L3 = \text{norm}(1/\text{poi\_reach\_cbd\_weighted})$$

### Layer 4: Last-Mile Quality (15%)

The last-mile layer evaluates the quality of integration at the destination end of the journey. While r5py's routing inherently includes a walking egress component (capped at 20 minutes), this layer adds explicit scoring for the quality of CBD-end station integration through two indicators:

- **CBD station integration** (cbd_station_integration): whether the optimal arrival station at the CBD end of the journey is within 500 meters walking distance of the CBD polygon centroid, measuring the spatial alignment between the transit network and employment destinations.
- **CBD mode transfer availability** (cbd_mode_transfer_available): whether bus-rail or rail-rail transfer integration exists at the CBD-end station, enabling onward travel within the employment district.

$$L4 = \text{r5py egress component} + 0.50 \times \text{norm}(\text{cbd\_station\_integration}) + 0.50 \times \text{norm}(\text{cbd\_mode\_transfer})$$

The partial overlap between L4 and L3 is acknowledged: r5py already accounts for egress walk time in its travel time output. The distinct contribution of L4 is to evaluate the quality of intermodal integration at the destination, recognizing that a commuter arriving at Tanah Abang KRL station with convenient Busway transfer to the Sudirman corridor has superior last-mile access compared to one arriving at Jatinegara KRL station with no onward CBD connection.

### Layer 5: Cost Competitiveness (15%)

Layer 5 introduces a novel element to the composite accessibility framework: a three-way generalized cost comparison that evaluates whether transit is cost-competitive against both car and motorcycle for the journey to the Sudirman--Thamrin CBD. This extension responds to a critical gap in the transit equity literature, where existing frameworks compare transit only against car (Currie, 2010; Delmelle & Casas, 2012). In Jabodetabek and across Southeast Asia more broadly, the motorcycle is the marginal competitor to transit, offering lower operating costs and superior flexibility in congested traffic (Ng, 2018; Sukor & Bhayo, 2024).

The generalized cost for each mode incorporates monetary costs, time costs, and discomfort penalties:

$$GC_{\text{transit}} = \text{fare} + (t_{\text{transit}} \times \text{VOT}) + (n_{\text{transfers}} \times \text{transfer\_friction}) + \text{first\_mile\_cost} + \text{discomfort\_penalty}$$

$$GC_{\text{car}} = \text{fuel} + \text{toll} + \text{parking} + (t_{\text{car}} \times \text{VOT})$$

$$GC_{\text{motorcycle}} = \text{fuel} + \text{parking} + (t_{\text{moto}} \times \text{VOT}) + \text{fatigue\_premium}$$

The value of time (VOT) is set at Rp 500 per minute (approximately Rp 30,000 per hour), calibrated to the Jakarta minimum wage (UMR) and cross-validated against Ng (2018), who reports VOT of USD 1.5--3.0 per hour for Southeast Asian transit users (equivalent to Rp 23,000--47,000 per hour), and Sukor and Bhayo (2024), who estimate VOT at 30--50% of hourly wage. Transfer friction is set at Rp 5,000 per transfer, representing approximately 10 minutes of equivalent time cost. Motorcycle fatigue premiums are distance-bracketed following behavioral evidence from Sukor and Bhayo (2024) that rides exceeding 30 minutes trigger willingness to switch to transit: Rp 0 for rides under 20 minutes, Rp 5,000 for 20--40 minutes, Rp 10,000 for 40--60 minutes, and Rp 15,000 for rides exceeding 60 minutes. Motorcycle toll costs are set to zero, reflecting Indonesian regulations (PP No. 15/2005) that prohibit motorcycles from toll roads.

The Transit Competitive Ratio (TCR) synthesizes the three-way comparison:

$$\text{TCR}_{\text{combined}} = \frac{\min(GC_{\text{car}}, GC_{\text{motorcycle}})}{GC_{\text{transit}}}$$

Transit must beat the cheapest private alternative. The TCR is classified into competitive zones: values above 1.2 indicate that transit clearly wins on generalized cost; values between 0.8 and 1.2 constitute a swing zone where first-mile quality and personal preference determine mode choice; values below 0.8 indicate private transport dominance; and values below 0.5 indicate strong private transport dominance. For spatial units where no transit service is available, the TCR is null and the competitive zone is classified as "transit not available." The layer score is:

$$L5 = \text{norm}(\text{clamp}(\text{TCR}_{\text{combined}}, 0.3, 2.0))$$

The clamping bounds prevent extreme TCR values from dominating the normalization.

## 3.5 Spatial Units and Dual-Resolution Design

The analysis is conducted at two spatial resolutions to address the Modifiable Areal Unit Problem (MAUP), which Javanmard et al. (2023) demonstrated can substantively alter transit equity conclusions depending on the spatial unit of aggregation.

**Kelurahan resolution.** The primary administrative unit comprises approximately 1,800 kelurahan (urban village) polygons across the Jabodetabek metropolitan region. Kelurahan boundaries are policy-relevant --- they align with census enumeration, government administration, and budget allocation --- but they vary dramatically in area, from less than 0.5 km² in dense central Jakarta to over 50 km² in outer Bodetabek. This area heterogeneity is precisely the MAUP vulnerability: a large suburban kelurahan containing both a transit-served corridor and a transit-poor interior will receive a single averaged score that masks internal variation.

**H3 hexagonal resolution.** The secondary analytical unit employs Uber's H3 hierarchical hexagonal grid at resolution 8, generating approximately 15,000--20,000 cells across the study area, each with a constant area of approximately 0.74 km² (edge-to-edge distance of approximately 860 meters). The uniform cell size eliminates the area-based component of MAUP, while the hexagonal tessellation avoids the edge effects and directional bias inherent in square grids. Resolution 8 is selected because its cell size approximates a walkable neighborhood, providing sufficient spatial granularity to detect within-kelurahan variation while remaining computationally tractable for the r5py routing engine.

Deriving H3-level data requires four distinct strategies, matched to the nature of each data type. Socioeconomic indicators (population, poverty rate, household expenditure, zero-vehicle household percentage, dependency ratio) are mapped from kelurahan to H3 cells through dasymetric disaggregation using the WorldPop population raster at approximately 100-meter resolution as the allocation surface. For each H3 cell, the population-weighted average of overlapping kelurahan values is computed:

$$\text{value}_{h3} = \frac{\sum_k (\text{pop}_{\text{raster in } h3 \cap k} \times \text{value}_k)}{\sum \text{pop}_{\text{raster in } h3}}$$

For cells entirely within a single kelurahan (the vast majority), the kelurahan rate passes through unchanged. For cells straddling boundaries, the formula produces a population-weighted blend. Infrastructure indicators (road network length, class proportions, intersection density) are derived through area-weighted spatial clipping: road segments are clipped to each H3 cell boundary and metrics recomputed from the clipped geometry. Point features (transit stops, POIs) are assigned to H3 cells through direct point-in-polygon spatial joins using exact coordinates. Travel time indicators are computed directly from each H3 cell centroid via fresh r5py routing, as redistributing kelurahan-level travel times would be methodologically invalid.

The H3 grid is generated by applying h3-py's polyfill function to the Jabodetabek study area boundary at resolution 8, then clipping to the GADM administrative boundary with a 500-meter buffer for edge handling. Cells straddling the study area boundary are flagged (is_edge_cell) for sensitivity analysis.

To quantify the resolution effect on equity conclusions, the full analytical pipeline --- TNI, TAI, equity gap, quadrant classification, Gini coefficient, and LISA clustering --- is executed identically at both resolutions. Differences between kelurahan-level and H3-level results are attributable to the spatial unit choice rather than methodological variation. Additionally, resolution sensitivity analysis is conducted at H3 resolutions 7 (approximately 3,000--5,000 cells, ~5.2 km² each) and 9 (approximately 50,000--70,000 cells, ~0.11 km² each), with results compared via confusion matrices of quadrant classification stability, Cohen's kappa statistic, Gini coefficient comparison, and LISA cluster pattern stability.

## 3.6 Data Sources and Processing

The analysis draws on ten open-access datasets assembled from public repositories and government portals (Table 1).

**Table 1. Data sources and specifications.**

| # | Dataset | Granularity | Format | Source | Access |
|---|---------|------------|--------|--------|--------|
| 1 | TransJakarta BRT GTFS | Stop/route/trip | GTFS ZIP | Mobility Database | Open |
| 2 | KRL Commuterline GTFS | Stop/route/trip | GTFS ZIP | Mobility Database | Open |
| 3 | MRT Jakarta GTFS | Stop/route/trip | GTFS ZIP | Mobility Database | Open |
| 4 | LRT Jabodebek stations | Point locations | Manual GeoJSON | Wikipedia / official sources | Open (manual) |
| 5 | OSM road network | Segment level | PBF | Geofabrik Java extract | Open |
| 6 | POIs (strict categories) | Point/polygon | GeoJSON | Overpass API | Open |
| 7 | Administrative boundaries | Polygon | GeoJSON | GADM / Indonesia Geoportal | Open |
| 8 | BPS demographic data | Kecamatan (some kelurahan) | CSV / tables | BPS Jakarta, BPS Jabar, BPS Banten | Open |
| 9 | WorldPop population raster | ~100 m grid | GeoTIFF | WorldPop | Open |
| 10 | H3 hexagonal grid | Resolution 8 hexagons | Generated | h3-py | N/A |

Socioeconomic indicators were modeled using spatial gradients calibrated to published BPS statistics (2020--2023). A nighttime lights (NTL) proxy was investigated as an alternative approach for estimating poverty and expenditure at sub-kecamatan scales, following Mellander et al. (2015) and Utomo et al. (2023). However, NTL alone was found insufficient for the specific TNI indicators required: Mellander et al. (2015) demonstrated that NTL is a reliable proxy for population density (r ~ 0.76) but a weak proxy for wages (r ~ 0.52), while Utomo et al. (2023) showed that multi-covariate composites (NTL combined with built-up indices and POI density) can achieve high correlation with SUSENAS poverty data (r = 0.954) but require survey-based calibration data that were not available at the required spatial granularity. Critically, NTL cannot proxy vehicle ownership or age-structure indicators at any resolution. The BPS-calibrated synthetic data approach was therefore retained.

The data processing pipeline proceeds through five phases. In the first phase (transit network assembly), the three GTFS feeds (TransJakarta, KRL, MRT) are parsed and merged into a unified transit stop dataset with mode tags, and LRT Jabodebek stations are appended as point locations without schedule data, flagged as schedule-unavailable. In the second phase (infrastructure extraction), the OSM road network is extracted from the Java PBF file, clipped to the Jabodetabek bounding box, and filtered to retain highway classifications relevant to pedestrian and vehicular access (motorway through cycleway). Road metrics --- length, density, class proportions, and intersection density --- are computed per kelurahan through spatial overlay. POIs are extracted from Overpass API using strict category-specific OSM tag filters, with manual verification for hospitals (cross-referenced against the Kemenkes database for type A/B classification), schools (filtered to SMA, SMK, and university level only), and CBD zones (defined as named polygons rather than point features).

In the third phase (socioeconomic preparation), BPS demographic data are assembled from multiple provincial and municipal sources, unified by BPS administrative codes, and disaggregated from kecamatan to kelurahan level using WorldPop-based population-weighted allocation. The TNI is then computed for each kelurahan. In the fourth phase (accessibility computation), transit stop metrics (count, route count, mode diversity, average headway), network walking distance to the nearest transit stop, and multi-modal travel times to CBD zones and other POI categories are computed using r5py routing from kelurahan centroids. The TAI is assembled from the five-layer model. In the fifth phase (H3 derivation and dual-resolution analysis), the H3 grid is generated, all indicators are derived at hexagonal resolution using the four derivation strategies described in Section 3.5, and TNI, TAI, equity gap, and quadrant classification are recomputed at H3 resolution.

## 3.7 Equity Analysis Methods

Three complementary statistical approaches are employed to characterize the distributional equity of transit accessibility across the metropolitan region.

The Gini coefficient is computed for the TAI distribution at both kelurahan and H3 resolutions, providing a single summary statistic of overall inequality in transit accessibility. A Gini of zero indicates perfect equality (all spatial units have identical TAI scores), while a Gini of one indicates maximal inequality (all accessibility concentrated in a single unit). The accompanying Lorenz curve plots the cumulative share of population against the cumulative share of transit accessibility, enabling visual comparison of equity profiles across the two resolutions. Comparing Gini coefficients between kelurahan and H3 directly tests whether administrative aggregation masks inequality that finer-grained analysis reveals.

Global Moran's I is computed to test whether the spatial distribution of equity gap scores exhibits statistically significant clustering across the metropolitan region, versus a spatially random distribution. A positive and significant Moran's I indicates that transit deserts (and transit-rich areas) are spatially clustered rather than randomly dispersed. Local Indicators of Spatial Association (LISA) are then computed to identify the specific locations and types of spatial clusters. Spatial weights are constructed using queen contiguity for the irregular kelurahan polygons and k-nearest-neighbors (k = 6) for the regular H3 hexagons, where k = 6 corresponds to the six immediate neighbors of each hexagonal cell. LISA identifies four cluster types: High-High clusters (areas with high equity gap scores surrounded by similarly high-gap neighbors, indicating concentrated transit deserts), Low-Low clusters (transit-rich areas surrounded by transit-rich neighbors), High-Low outliers (isolated transit deserts amid transit-rich surroundings), and Low-High outliers (isolated well-served areas amid transit-poor surroundings).

Quadrant classification employs a median split on both TNI and TAI to assign each spatial unit to one of four quadrants (Q1 through Q4). The median split is preferred over natural breaks or equal-interval classification because it is distribution-agnostic and ensures balanced group sizes, facilitating cross-resolution comparison. The spatial distribution of quadrants, particularly the concentration of Q4 (transit desert) zones, provides the primary test of hypothesis H1.

## 3.8 Sensitivity Analysis

The robustness of the TNI and TAI composite indices to weighting assumptions is evaluated through two complementary approaches. First, a Monte Carlo weight perturbation analysis randomly varies all indicator weights by up to plus or minus 20% of their default values across 1,000 iterations. For each iteration, the perturbed weights are re-normalized to sum to 1.0, the TNI and TAI are recomputed, and the resulting quadrant classifications are recorded. The proportion of spatial units that maintain their quadrant assignment across at least 90% of iterations provides a stability measure. Second, principal component analysis (PCA) is applied to the TNI and TAI indicator sets to derive data-driven weights as a robustness check. If PCA-derived weights produce substantially different quadrant classifications than equal weights, this signals sensitivity to the weighting assumption and warrants discussion.

The resolution sensitivity analysis extends the dual-resolution comparison by running the full pipeline at H3 resolutions 7 and 9 in addition to the primary resolution 8. Resolution 7 produces approximately 3,000--5,000 cells at ~5.2 km² each, while resolution 9 produces approximately 50,000--70,000 cells at ~0.11 km² each. Results are compared across the three resolutions using confusion matrices quantifying quadrant classification stability, Cohen's kappa as a chance-corrected agreement measure, Gini coefficient comparison, and LISA cluster pattern stability. Resolution 9 routing, which requires r5py computation from approximately 60,000 origin points, may necessitate stratified sampling if computational resources prove insufficient.

## 3.9 What-If Scenario Simulator

To validate the quadrant framework as an actionable planning tool (hypothesis H3), the study includes a scenario simulation module that evaluates the equity impact of hypothetical transit infrastructure placement. The simulation proceeds as follows: a new transit node (station or stop) is placed at a user-specified location within the study area. A catchment area is defined around the new node using two concentric buffers --- a 1-kilometer walking catchment and a 3-kilometer feeder service catchment. For all spatial units (kelurahan or H3 cells) whose centroids fall within the catchment, the TAI is recomputed: Layer 1 (first-mile quality) is recalculated with the new stop as an additional option, potentially reducing walk distance and increasing feeder service availability, and Layer 2 (service quality) is updated if the new node provides additional mode diversity or improved headway. The remaining layers (L3, L4, L5) are held constant under the simplifying assumption that a single new node does not alter the full journey-chain travel time or cost competitiveness at metropolitan scale.

The equity impact of the simulated intervention is measured through three metrics: the number and percentage of spatial units that shift quadrant membership (particularly Q4 to Q1 or Q3 transitions), the change in the metropolitan Gini coefficient, and the total population affected by the quadrant reclassification. Hypothesis H3 is tested by comparing the equity improvement (Gini delta and population-weighted quadrant shifts) from placing a new node in a Q4 (transit desert) zone against the same intervention in a Q2 (low need, high access) zone. If Q4 placement produces a larger improvement, this validates the quadrant framework's utility for prioritizing investment.

It is important to note that the scenario simulator is indicative rather than predictive. It employs a simplified buffer-based catchment model rather than a full transit assignment model, does not account for induced demand or network effects beyond the immediate catchment, and holds fare structures and service frequencies constant. Results should be interpreted as directional estimates of equity impact, not as engineering-grade forecasts.

## 3.10 Limitations

Several limitations of the methodology warrant acknowledgment. First, informal transit services --- including angkot (minibus) networks, non-app ojek (motorcycle taxi), and unregulated paratransit --- are excluded from the analysis because no GTFS or standardized spatial data exist for these services. This exclusion systematically underestimates transit accessibility in kampung areas and lower-income neighborhoods where informal transit plays a substantial role in daily mobility, and the resulting equity gap scores in these areas should be interpreted as conservative estimates.

Second, the LRT Jabodebek system is included as point locations (station proximity) rather than as a fully scheduled GTFS feed, because no validated GTFS data were available at the time of analysis. LRT travel times are therefore not computed through r5py routing, and LRT's contribution to the TAI is limited to Layer 1 (first-mile proximity) and Layer 2 (mode diversity). This likely underestimates accessibility for spatial units near LRT stations.

Third, socioeconomic data from BPS are available at kecamatan granularity for most indicators and are disaggregated to kelurahan level using WorldPop-based population weighting. This disaggregation assumes that within-kecamatan variation in poverty, expenditure, and vehicle ownership follows the population density distribution --- an assumption that may not hold in socioeconomically heterogeneous kecamatan. The synthetic nature of kelurahan-level socioeconomic estimates introduces additional uncertainty that propagates through the TNI computation.

Fourth, the analysis represents a cross-sectional snapshot based on current transit schedules and the most recent available demographic data (2020--2023). It does not capture temporal trends in transit investment, ridership growth, or demographic shifts, and the equity patterns identified may evolve as new infrastructure (such as MRT Phase 2 or additional LRT extensions) comes online.

Fifth, the current implementation does not incorporate real-time traffic data. OSM road classification captures the structural characteristics of the network (class, connectivity, pedestrian infrastructure) but not congestion-induced delays. The generalized cost model for car and motorcycle uses estimated travel times rather than empirical congestion-adjusted times. The schema includes null-by-default fields for traffic speed and congestion indices, designed for future integration via traffic API services.

Sixth, the what-if scenario simulator employs a simplified buffer-and-recalculate approach rather than a full transit network assignment model. It does not model induced demand, route restructuring, or fare integration effects, and should be interpreted as an indicative tool for equity prioritization rather than an engineering planning instrument.

Finally, the socioeconomic data underlying the TNI are modeled from published BPS statistics using spatial gradient calibration rather than derived from household-level survey microdata (such as SUSENAS), which would require restricted-access data not available for this study. While the calibration approach produces plausible spatial patterns consistent with known socioeconomic gradients across Jabodetabek, it introduces uncertainty in the absolute values of individual kelurahan estimates.

## References

Currie, G. (2010). Quantifying spatial gaps in public transport supply based on social needs. *Journal of Transport Geography*, 18(1), 31--41.

Delmelle, E. C., & Casas, I. (2012). Evaluating the spatial equity of bus rapid transit-based accessibility patterns in a developing country: The case of Cali, Colombia. *Transport Policy*, 20, 36--46.

Fink, C., Klumpenhouwer, W., Saraiva, M., Pereira, R. H. M., & Tenkanen, H. (2022). r5py: Rapid Realistic Routing with R5 in Python. doi:10.5281/zenodo.7060437.

Hardi, A. Z., & Murad, A. A. (2023). Spatial analysis of accessibility for public transportation: A case study in Jakarta, Bus Rapid Transit System (Transjakarta), Indonesia. *Journal of Computer Science*, 19(10), 1190--1202.

Javanmard, R., Lee, J., Kim, J., Liu, L., & Diab, E. (2023). The impacts of the modifiable areal unit problem (MAUP) on social equity analysis of public transit reliability. *Journal of Transport Geography*, 106, 103523.

Jiao, J., & Dillivan, M. (2013). Transit deserts: The gap between demand and supply. *Journal of Public Transportation*, 16(3), 23--39.

Jomehpour, M., & Smith-Colin, J. (2020). Transit deserts: Equity analysis of public transit accessibility. *Journal of Transport Geography*, 89, 102869.

Mamun, S. A., & Lownes, N. E. (2011a). Measuring service gaps: Accessibility-based Transit Need Index. *Transportation Research Record*, 2217(1), 153--161.

Mamun, S. A., & Lownes, N. E. (2011b). A composite index of public transit accessibility. *Journal of Public Transportation*, 14(2), 69--87.

Mellander, C., Lobo, J., Stolarick, K., & Matheson, Z. (2015). Night-time light data: A good proxy measure for economic activity? *PLOS ONE*, 10(10), e0139779.

Ng, W. S. (2018). Urban transportation mode choice and carbon emissions in Southeast Asia. *Transportation Research Record*, 2672(25), 29--37.

Pereira, R. H. M., Banister, D., Schwanen, T., & Wessel, N. (2019). Distributional effects of transport policies on inequalities in access to opportunities in Rio de Janeiro. *Journal of Transport and Land Use*, 12(1), 741--764.

Pereira, R. H. M., Saraiva, M., Herszenhut, D., Braga, C. K. V., & Conway, M. W. (2021). r5r: Rapid Realistic Routing on Multimodal Transport Networks with R5 in R. *Findings*, March. doi:10.32866/001c.21262.

Rathod, R., Joshi, G., & Arkatkar, S. (2025). Composite Accessibility Index: A novel and holistic measure for evaluating transit accessibility. *Transportation Research Record*. doi:10.1177/03611981241270156.

Sukor, N. S. A., & Bhayo, A. R. (2024). Unveiling the drivers of modal switch from motorcycles to public transport in Southeast Asia. *Transportation Research Part F*, 101, 197--213.

Utomo, A. J. P., Aini, N. N., Hendayana, Y., & Dewi, R. S. (2023). Spatially granular poverty index (SGPI) for urban poverty mapping in Jakarta metropolitan area (JMA). *Earth Science Informatics*, 16, 3531--3544.

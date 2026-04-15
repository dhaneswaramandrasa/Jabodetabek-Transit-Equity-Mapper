# Scientific Methodology
## Jabodetabek Transit Equity Mapper

**Status**: **Signed off** — 2026-03-21 (MVP-81). Journey estimation section added 2026-04-15.
**Last updated**: 2026-04-15
**Feeds**: Paper Methods section, product data layer, `docs/DATA_MODEL.md`, `docs/ARCHITECTURE.md`

---

## 2.1 Research Question & Hypothesis

### Research Question (refined from Phase 1.2)

> To what extent does the spatial distribution of public transit accessibility in the Jabodetabek metropolitan region align with the socioeconomic transit need of its population, and how does this alignment differ when measured at administrative (kelurahan) versus uniform hexagonal (H3) spatial resolutions?

### Hypotheses

**H1** (Spatial mismatch): Areas classified as "High Need, Low Access" are disproportionately concentrated in the suburban peripheries of Bodetabek, while "Low Need, High Access" areas cluster in central Jakarta.

**H2** (Resolution effect): The dual-resolution comparison reveals that kelurahan-level analysis systematically underestimates equity gaps in heterogeneous suburban areas — large kelurahan mask internal variation that H3 hexagons expose.

**H3** (Scenario validation): Simulating a new transit node in a "High Need, Low Access" zone produces a larger equity score improvement than the same intervention in a "Low Need, High Access" zone, validating the quadrant framework as a prioritization tool.

### Analysis Type

Descriptive + Exploratory spatial analysis with scenario simulation. Not causal inference.

---

## 2.1b Theoretical Framework

*Added from literature scan (MVP-2). See `docs/source-map.md` for full paper table and `docs/literature_review.md` for expanded prose.*

This research builds on three established theoretical foundations from the transit equity literature:

**1. Need-Supply Gap Framework (Currie 2010; Mamun & Lownes 2011; Jiao & Dillivan 2013)**

The core analytical structure — comparing transit need against transit supply to identify spatial gaps — originates from Currie's (2010) spatial gap analysis in Melbourne and was formalized by Mamun and Lownes (2011) through their Transit Need Index. Jiao and Dillivan (2013) coined the term "transit desert" for areas where transit-dependent populations exceed transit service. Our two-axis Transit Equity Matrix (TNI vs. TAI) directly extends this tradition, with the Q4 quadrant ("High Need, Low Access") operationalizing the transit desert concept.

**2. Distributional Equity Measurement (Delmelle & Casas 2012; Pereira et al. 2019)**

Beyond binary gap identification, distributional equity analysis uses Gini coefficients and Lorenz curves to quantify the overall inequality of transit accessibility across a metropolitan area. Delmelle and Casas (2012) demonstrated this approach in Cali, Colombia — a developing-country BRT context similar to Jakarta. Pereira et al. (2019) extended it to show that Rio de Janeiro's transit investments disproportionately benefited higher-income groups. We adopt the Gini/Lorenz approach and additionally compute it at two spatial resolutions to test MAUP sensitivity.

**3. MAUP Sensitivity in Transit Equity (Javanmard et al. 2023)**

Javanmard et al. (2023) empirically demonstrated that the spatial unit of analysis substantively changes transit equity conclusions — route-level analysis appeared equitable while stop/neighborhood-level analysis revealed significant inequity. This motivates our dual-resolution design: comparing kelurahan (variable-area administrative units) against H3 hexagons (constant-area analytical units) to expose how aggregation choices affect equity diagnoses in Jabodetabek.

**Extension beyond existing frameworks:**

Our research extends the theoretical foundations in two directions not previously combined:
- **Three-way cost competitiveness**: Western frameworks compare transit vs. car only. Following Ng (2018) and Sukor & Bhayo (2024) on motorcycle dominance in Southeast Asia, we add motorcycle as a third mode in the generalized cost comparison — a novel layer within the composite TAI.
- **Scenario simulation within equity classification**: No existing study embeds what-if infrastructure placement directly into a transit equity quadrant framework to measure shifts in equity scores, making the analysis actionable for planners.

## 2.1c Methodological Precedents

| Precedent | Key papers | What we borrow | What we extend |
|-----------|------------|----------------|----------------|
| Need-supply gap analysis | Currie (2010), Mamun & Lownes (2011a), Jiao & Dillivan (2013) | Two-axis need vs. access structure; quadrant classification | Apply to full Jabodetabek (not just DKI Jakarta); add motorcycle cost layer |
| Composite accessibility index | Mamun & Lownes (2011b), Rathod et al. (2025) | Multi-indicator composite with normalization | Restructure as 5-layer journey chain model reflecting Jabodetabek commuter experience |
| Gini/Lorenz equity measurement | Delmelle & Casas (2012), Pereira et al. (2019) | Gini coefficient + Lorenz curve for accessibility distribution | Compute at two resolutions; compare Gini between kelurahan and H3 |
| Transit desert identification | Jiao & Dillivan (2013), Jomehpour & Smith-Colin (2020) | GIS overlay for demand-supply gap zones | Embed what-if scenario to test interventions in transit desert zones |
| Multimodal routing (r5py) | Pereira et al. (2021), Fink et al. (2022) | RAPTOR-based travel time matrices; GTFS + OSM input | Apply to Jabodetabek GTFS feeds; gravity-weighted CBD model |
| MAUP multi-scale comparison | Javanmard et al. (2023) | Compare equity metrics across spatial scales | Use H3 hexagons (not just administrative tiers) for constant-area comparison |
| Jakarta transit analysis | Hardi & Murad (2023), Taki et al. (2018) | Walk-isochrone BRT accessibility; Jakarta network context | Extend beyond BRT/DKI Jakarta to full multi-modal Jabodetabek with equity framing |

---

## 2.2 Methodology Definition

### Analytical Framework: Two-Axis Transit Equity Matrix

The core framework scores every spatial unit on two composite indices, then classifies each unit into a quadrant:

```
                    HIGH TRANSIT ACCESS
                          │
         Q2: Low Need,    │    Q1: Well-Served
         High Access      │    (adequate match)
         (potential        │
          overinvestment)  │
    ──────────────────────┼──────────────────────
         Q3: Low Need,    │    Q4: High Need,
         Low Access       │    Low Access
         (low priority)   │    (**TRANSIT DESERT**)
                          │
                    LOW TRANSIT ACCESS
    LOW TRANSIT NEED ◄────┼────► HIGH TRANSIT NEED
```

**Axis 1 — Transit Need Index (TNI)**: Composite of socioeconomic and demographic indicators measuring latent demand for public transit.

**Axis 2 — Transit Accessibility Index (TAI)**: Composite of physical proximity, network connectivity, and service quality indicators measuring how well transit serves an area.

**Equity Gap Score** = TNI_normalized − TAI_normalized (positive = underserved, negative = overserved)

### TNI Indicator Set (finalized — MVP-5)

Five indicators confirmed against literature (Mamun & Lownes 2011a, Jiao & Dillivan 2013, Currie 2010):

| # | Indicator | Dimension | Direction | Literature precedent |
|---|-----------|-----------|-----------|---------------------|
| 1 | `pop_density` | Aggregate demand | Higher = higher need | Mamun & Lownes (2011a), Jiao & Dillivan (2013) |
| 2 | `poverty_rate` | Economic vulnerability | Higher = higher need | Mamun & Lownes (2011a), Currie (2010) |
| 3 | `avg_household_expenditure` | Economic gradient | **Higher = LOWER need** (invert) | Pereira et al. (2019) income proxy |
| 4 | `zero_vehicle_hh_pct` | Transit dependence | Higher = higher need | Mamun & Lownes (2011a), Jiao & Dillivan (2013) |
| 5 | `dependency_ratio` | Demographic vulnerability | Higher = higher need | Mamun & Lownes (2011a) |

**Normalization**: Min-max to [0, 1] with winsorization at 2nd/98th percentiles before scaling. `avg_household_expenditure` uses inverted formula: `(x_max - x) / (x_max - x_min)`.

**Weighting**: Equal (0.20 each) as default — literature consensus (Mamun & Lownes 2011a, Rathod et al. 2025). Sensitivity analysis: Monte Carlo ±20% perturbation (1,000 iterations) + PCA-derived weights as robustness check.

```
TNI = 0.20 × norm(pop_density) + 0.20 × norm(poverty_rate)
    + 0.20 × norm_inv(avg_household_expenditure)
    + 0.20 × norm(zero_vehicle_hh_pct) + 0.20 × norm(dependency_ratio)
```

**Edge cases**: (1) Missing data: hierarchical fallback (parent kecamatan → adjacent kelurahan → kota/kab average → exclude if >2 indicators missing). (2) Zero variance: assign 0.5, redistribute weight. (3) Outliers: winsorize, don't delete. (4) Zero-population kelurahan (<100 pop): exclude from TNI, retain in spatial dataset.

*Full detail: `docs/drafts/mvp5-tni-methodology.md`*

### Spatial Units (Dual Resolution)

| Unit | Type | Count (approx.) | Avg area | Purpose |
|------|------|-----------------|----------|---------|
| Kelurahan | Administrative polygon | ~1,800 across Jabodetabek | Variable (0.5–50 km²) | Policy-relevant reporting; aligns with census data |
| H3 hexagon (res 8) | Uniform hexagonal grid | ~15,000–20,000 across Jabodetabek | ~0.74 km² | Analytical precision; reduces MAUP; enables fine-grained comparison |

**Resolution 8 rationale**: At ~0.74 km² per cell, resolution 8 approximates a walkable neighborhood (~860m edge-to-edge). This is large enough to contain meaningful population and infrastructure, but small enough to detect within-kelurahan variation. Sensitivity analysis at resolutions 7 and 9 will be conducted to test robustness.

### Statistical & Spatial Methods

| Method | Purpose | Application |
|--------|---------|-------------|
| Min-max normalization | Scale indicators to [0, 1] | All sub-indicators before composite index construction |
| Weighted linear combination | Construct composite TNI and TAI | Layer-weighted TAI (see below); sensitivity analysis on weights |
| Gini coefficient + Lorenz curve | Measure overall equity of transit access distribution | Compare Gini across kelurahan vs. H3 to quantify resolution effect |
| Moran's I (global + local LISA) | Detect spatial autocorrelation and clustering | Identify statistically significant clusters of Q4 (transit desert) zones |
| Quadrant classification | Categorize spatial units | Median-split or natural breaks on TNI and TAI to define quadrants |
| Generalized cost comparison | Compare transit vs. motorcycle competitiveness | Per spatial unit: flag where motorcycle generalized cost < transit generalized cost |
| Scenario delta analysis | Measure equity impact of hypothetical infrastructure | Recalculate TAI with simulated transit node → measure shift in quadrant membership and Gini |

### TAI Restructured: 5-Layer Effective Access Model

The TAI is no longer a flat composite of proximity indicators. It models the **full commuter journey** from home to workplace in five layers, reflecting the actual decision Jabodetabek commuters make each morning: "Is transit worth it, or do I just ride my motorcycle?"

```
TAI = 0.20 × L1_first_mile
    + 0.15 × L2_service_quality
    + 0.35 × L3_cbd_journey_chain
    + 0.15 × L4_last_mile
    + 0.15 × L5_cost_competitiveness
```

**Layer 1: First-mile quality (20%)** — Home → nearest transit stop/station

This layer captures the Jakarta Selatan paradox: an area surrounded by MRT/KRL/Busway stations scores poorly if residents can't physically reach them. Indicators:

| Indicator | Source | What it measures |
|-----------|--------|-----------------|
| `walk_dist_to_nearest_stop_m` | OSM network + GTFS stops | Network walking distance (not Euclidean) from centroid to nearest transit stop |
| `pct_footway_pedestrian` | OSM road network | % of roads classified as footway/pedestrian — measures walkability |
| `network_connectivity` | OSM road network | Intersection density — grid networks score higher than cul-de-sacs |
| `has_feeder_service` | GTFS (Mikrotrans routes) | Whether a feeder bus/mikrotrans connects to a trunk station within the spatial unit |

```
L1_first_mile = 0.35 × norm(1/walk_dist) + 0.25 × norm(pct_footway)
              + 0.20 × norm(connectivity) + 0.20 × norm(has_feeder)
```

A kampung in Jakarta Selatan 1.5km from MRT Haji Nawi with no sidewalk and no feeder bus: L1 ≈ 0.15 (terrible). A perumahan in Depok 400m from KRL Depok Baru with proper sidewalks and a Mikrotrans route: L1 ≈ 0.75 (good).

**Layer 2: Transit service quality (15%)** — At the station/stop

Once you reach the station, how good is the service? Indicators:

| Indicator | Source | What it measures |
|-----------|--------|-----------------|
| `avg_headway_min` | GTFS stop_times | Average scheduled headway — MRT every 5 min vs KRL Green Line every 10-15 min |
| `transit_mode_diversity` | GTFS | Count of distinct modes available (BRT, KRL, MRT, LRT, Mikrotrans) |
| `best_mode_fare_tier` | Fare tier table | Tier of the most affordable mode available (1=KRL/Busway, 4=Royaltrans) |
| `has_affordable_mode` | Fare tier table | Boolean: is a tier 1 or 2 mode available? |

```
L2_service_quality = 0.35 × norm(1/headway) + 0.25 × norm(mode_diversity)
                   + 0.20 × norm(1/fare_tier) + 0.20 × norm(has_affordable)
```

**Layer 3: CBD journey chain (35%)** — Full door-to-door multi-modal travel time

The dominant layer. Computed via r5py multi-modal routing with transfer penalties. See §2.6a for the gravity-weighted CBD model. This is `poi_reach_cbd_weighted` — the gravity-weighted average travel time across all 9 CBD zones, with Sudirman–Thamrin weighted 5× vs satellite CBDs at 1×.

```
L3_cbd_journey = norm(1/poi_reach_cbd_weighted)
```

r5py inherently handles:
- Multi-modal path optimization (KRL → transfer → Busway → walk)
- Transfer waiting time + 10 min penalty per transfer
- Walking access/egress legs (capped at 20 min)
- Service frequency (samples multiple departures in the 7:00–8:00 AM window)

**Layer 4: Last-mile quality (15%)** — CBD station → office

This is partially captured within the r5py routing (egress_mode: WALK), but we add explicit last-mile indicators for the destination end:

| Indicator | Source | What it measures |
|-----------|--------|-----------------|
| `cbd_station_integration` | GTFS + CBD polygons | Whether the optimal CBD arrival station is within 500m walk of the CBD polygon centroid |
| `cbd_mode_transfer_available` | GTFS | Whether Busway/feeder integration exists at the CBD-end station (e.g., Tanah Abang → Busway Corridor 1) |

```
L4_last_mile = r5py egress component (already in L3 travel time)
             + 0.50 × norm(cbd_station_integration)
             + 0.50 × norm(cbd_mode_transfer)
```

Note: L4 partially overlaps with L3 (r5py includes walk egress). L4's distinct contribution is scoring the quality of integration at the destination end — a commuter arriving at Tanah Abang KRL with easy Busway transfer to Sudirman scores higher than one arriving at Jatinegara KRL with no CBD connection.

**Layer 5: Cost competitiveness vs. private transport (15%)** — The three-way choice

This is the novel indicator. For each spatial unit, we estimate whether transit to Sudirman–Thamrin CBD is cost-competitive against **both car and motorcycle** — the two private alternatives. The competitive dynamic is distance-dependent:

- **Suburban origins (20-40 km)**: Car is most expensive (fuel + toll ~Rp 35k + parking ~Rp 25k + heavy traffic), motorcycle is mid-range (fuel + toll cheaper + parking cheaper, but exhausting in heat/rain for 1hr+), transit is cheapest and most time-reliable **if** first/last mile works.
- **Mid-ring origins (10-20 km)**: All three modes converge in generalized cost — first-mile quality becomes the swing factor.
- **Near-CBD origins (3-8 km)**: Private transport wins on convenience — no toll, cheap fuel, 15-20 min door-to-door. Transit can't overcome the first/last mile overhead for such short distances.

```
Generalized Cost (transit):
  GC_transit = fare_total_idr
             + (travel_time_min × VOT)
             + (n_transfers × transfer_friction_idr)
             + first_mile_cost_idr        (ojol/walk time monetized)

Generalized Cost (car):
  GC_car = fuel_cost_idr                  (distance × Rp 1,000/km, assuming 12 km/L at Rp 12k/L)
         + toll_cost_idr                  (Rp 0 near-CBD; Rp 25-40k suburban via toll)
         + parking_cost_idr               (CBD parking: Rp 15-30k for cars)
         + (travel_time_min × VOT)        (car travel time with congestion)
         + fatigue_premium_idr            (Rp 0 — car is comfortable)

Generalized Cost (motorcycle):
  GC_motorcycle = fuel_cost_idr           (distance × Rp 200/km, 50 km/L at Rp 10k/L)
                + toll_cost_idr           (Rp 0 — motorcycles cannot use toll roads in Indonesia)
                + parking_cost_idr        (CBD parking: Rp 5-10k for motorcycles)
                + (travel_time_min × VOT) (motorcycle faster in traffic but variable)
                + fatigue_premium_idr     (Rp 10,000 — heat, rain, exhaust exposure for >30 min rides)

Where:
  VOT (value of time) = Rp 500/min (~Rp 30k/hr, Jakarta UMR proxy)
    Cross-validated: Ng (2018) USD 1.5–3.0/hr → Rp 23–47k/hr; Sukor & Bhayo (2024) 30–50% of hourly wage
  transfer_friction = Rp 5,000 per transfer (~10 min equivalent; Wardman 2004)
  first_mile_cost = ojol_fare OR (walk_time_min × VOT), whichever is lower
  discomfort_penalty = Rp 3,000 (peak-hour crowding default; Rp 0 off-peak, Rp 5,000 severe)
  fatigue_premium (motorcycle) = Rp 0 (<20 min), Rp 5,000 (20–40 min), Rp 10,000 (40–60 min), Rp 15,000 (>60 min)
    Based on Sukor & Bhayo (2024): >30 min triggers willingness to switch to transit
  fatigue_premium (car) = Rp 0 (climate-controlled, seated)

  NOTE: Motorcycles CANNOT use toll roads in Indonesia (PP No. 15/2005) — zero toll fees but
  forced onto surface roads. Net effect: cost advantage at all suburban distances because
  toll savings (Rp 8k–35k) consistently exceed time penalty cost (Rp 2.5k–20k).

Cost parameters (finalized — MVP-8):
  Car fuel: Rp 1,000/km (12 km/L × Rp 10k/L Pertalite, rounded for mixed Pertalite/Pertamax)
  Motorcycle fuel: Rp 200/km (50 km/L × Rp 10k/L — 5:1 car:motorcycle ratio)
  Car parking (CBD): Rp 25,000 | Motorcycle parking: Rp 8,000
  Toll: Rp 8,000–35,000 per corridor (Jasa Marga 2024 tariffs, car only)
  Transit fares: KRL Rp 3k–13k | MRT Rp 3k–14k | BRT Rp 3,500 flat | LRT Rp 5k–20k

Transit competitive ratio (3-way):
  TCR_vs_car = GC_car / GC_transit
  TCR_vs_motor = GC_motorcycle / GC_transit
  TCR_combined = min(GC_car, GC_motorcycle) / GC_transit
    (transit must beat the CHEAPEST private alternative)

  If TCR_combined > 1.2: transit clearly wins
  If TCR_combined 0.8–1.2: swing zone (first-mile decides)
  If TCR_combined < 0.8: private transport wins
  If TCR_combined < 0.5: private transport strongly dominates

L5_cost_competitive = norm(clamp(TCR_combined, 0.3, 2.0))
```

**Worked example — BSD resident (suburban, 30 km to Sudirman):**

| Component | Transit | Car | Motorcycle |
|-----------|---------|-----|------------|
| First-mile/access | Ojol: Rp 12k, 15 min | Door-to-door | Door-to-door |
| Fare / fuel | KRL Rp 5k + Busway Rp 3.5k = Rp 8.5k | Rp 30k (30km × Rp1k) | Rp 6k (30km × Rp200) |
| Toll | — | Rp 35k (BSD–Jakarta toll) | Rp 0 (motorcycles can't use toll) |
| Parking | — | Rp 25k (car CBD) | Rp 8k (motorcycle CBD) |
| Travel time | 90 min (incl. transfers) | 75 min (toll + congestion) | 80 min (surface roads, no toll) |
| Time cost (@Rp 500) | Rp 45k | Rp 37.5k | Rp 40k |
| Transfer friction | 1 × Rp 5k | — | — |
| Discomfort penalty | Rp 3k (peak crowding) | — | — |
| Fatigue premium | — | — | Rp 15k (>60 min ride) |
| **Generalized cost** | **Rp 73.5k** | **Rp 127.5k** | **Rp 69k** |
| | | | |

TCR_vs_car = 127.5/73.5 = **1.73** (transit strongly beats car)
TCR_vs_motor = 69/73.5 = **0.94** (motorcycle slightly beats transit)
TCR_combined = min(127.5, 69)/73.5 = **0.94** → **Swing zone**

Interpretation: For BSD, motorcycle slightly beats transit in generalized cost (Rp 69k vs Rp 73.5k). Car is far more expensive. The swing factor is first-mile quality — if BSD improves feeder service to the KRL station (removing the Rp 12k ojol), transit GC drops to ~Rp 61.5k, pushing TCR above 1.0. This matches reality: BSD commuters with good first-mile access use KRL, others ride motorcycles.

**Worked example — Tebet resident (near-CBD, 5 km to Sudirman):**

| Component | Transit | Car | Motorcycle |
|-----------|---------|-----|------------|
| First-mile/access | Walk 10 min to Busway | Door-to-door | Door-to-door |
| Fare / fuel | Busway Rp 3.5k | Rp 5k (5km × Rp1k) | Rp 1k (5km × Rp200) |
| Toll | — | Rp 0 | Rp 0 |
| Parking | — | Rp 25k (car CBD) | Rp 8k |
| Travel time | 35 min (walk + wait + ride) | 20 min | 15 min |
| Time cost (@Rp 500) | Rp 17.5k | Rp 10k | Rp 7.5k |
| Transfer friction | — | — | — |
| Discomfort penalty | Rp 3k (peak crowding) | — | — |
| Fatigue premium | — | — | Rp 0 (<20 min) |
| **Generalized cost** | **Rp 24k** | **Rp 40k** | **Rp 16.5k** |

TCR_vs_car = 40/24 = **1.67** (transit beats car)
TCR_vs_motor = 16.5/24 = **0.69** (motorcycle beats transit)
TCR_combined = **0.69** → **Private transport wins**

Interpretation: For near-CBD Tebet, motorcycle is cheaper and faster than transit despite having Busway access. The short distance means fuel is negligible and there's no toll. Transit's fare advantage disappears because Busway's Rp 3.5k barely undercuts Rp 1k fuel, but the 20-min time difference costs Rp 10k in VOT. This explains why near-CBD residents with motorcycles rarely use transit for commuting.

**Worked example — Ciputat resident (peri-urban, 18 km to Sudirman):**

| Component | Transit | Car | Motorcycle |
|-----------|---------|-----|------------|
| First-mile/access | Walk 12 min to feeder | Door-to-door | Door-to-door |
| Fare / fuel | Feeder Rp 3.5k + MRT Rp 10k = Rp 13.5k | Rp 18k (18km × Rp1k) | Rp 3.6k (18km × Rp200) |
| Toll | — | Rp 18k (JORR) | Rp 0 |
| Parking | — | Rp 25k | Rp 8k |
| Travel time | 85 min (feeder + MRT + walk) | 55 min (JORR + congestion) | 50 min (surface arterial) |
| Time cost (@Rp 500) | Rp 42.5k | Rp 27.5k | Rp 25k |
| Transfer/discomfort | 1 × Rp 5k + Rp 2k | — | — |
| Fatigue premium | — | — | Rp 10k (40–60 min tier) |
| **Generalized cost** | **Rp 63k** | **Rp 88.5k** | **Rp 46.6k** |

TCR_vs_car = 88.5/63 = **1.40** (transit beats car)
TCR_vs_motor = 46.6/63 = **0.74** (motorcycle clearly beats transit)
TCR_combined = **0.74** → **Private transport wins**

Interpretation: Ciputat demonstrates the "missing middle" — close enough that motorcycle is fast (50 min), but far enough that transit requires a multi-leg chain (feeder → MRT). The 52 min of non-in-vehicle time (walk + wait + transfer + wait + egress) is the problem, not fare. Without a direct high-frequency connection, motorcycle dominance is entrenched.

**Key finding across all three examples**: Motorcycle beats transit at every distance tested (BSD TCR 0.94, Ciputat TCR 0.74, Tebet TCR 0.69). Car is always most expensive. The marginal competitor to transit is always motorcycle, not car — validating the three-mode approach. First-mile cost (ojol Rp 12k for BSD) is the decisive swing factor (Sukor & Bhayo 2024).

**Spatial units without transit**: Where no transit service exists, `gc_transit_idr = null`, `tcr_combined = null`, `transit_competitive_zone = "transit_not_available"`, and `L5 = 0.0`.

*Full detail with toll exclusion analysis, sensitivity parameters, and corridor-specific dynamics: `docs/drafts/mvp8-gc-methodology.md`*

**Schema fields for three-way comparison:**

| Field | Type | Description |
|-------|------|-------------|
| `gc_transit_idr` | float | Generalized cost of optimal transit journey to Sudirman–Thamrin |
| `gc_car_idr` | float | Generalized cost of car journey to Sudirman–Thamrin |
| `gc_motorcycle_idr` | float | Generalized cost of motorcycle journey to Sudirman–Thamrin |
| `cheapest_private_mode` | enum (car/motorcycle) | Which private mode has lower GC |
| `tcr_vs_car` | float | GC_car / GC_transit |
| `tcr_vs_motorcycle` | float | GC_motorcycle / GC_transit |
| `tcr_combined` | float | min(GC_car, GC_motorcycle) / GC_transit |
| `transit_competitive_zone` | enum | "transit_wins" (>1.2), "swing" (0.8–1.2), "private_wins" (<0.8), "transit_not_available" |
| `distance_to_sudirman_km` | float | Straight-line distance to Sudirman–Thamrin centroid |

### Validation Approach

- **Internal**: Sensitivity analysis on (a) H3 resolution, (b) indicator weights, (c) classification thresholds
- **External**: Cross-validate Q4 "transit desert" zones against known commuter pain points (e.g., Jabodetabek commuter survey data, news reports on underserved areas, BPTJ reports)
- **Expert review**: If possible, present quadrant maps to 2–3 urban planning practitioners for face-validity assessment

### Key Assumptions

1. GTFS scheduled service approximates actual service (acknowledged overestimate due to bunching/delays)
2. Population is distributed within kelurahan according to WorldPop density raster (dasymetric assumption)
3. Road network from OSM is reasonably complete for Jabodetabek (well-mapped region)
4. POIs extracted from OSM represent the actual major facilities (manual verification for hospital/school tier)
5. Equal weighting of sub-indicators is the default; sensitivity analysis tests this assumption

### Limitations

1. **Informal transit excluded**: Angkot networks have no GTFS data; access is systematically underestimated in kampung areas where informal transit dominates
2. **LRT Jabodebek approximated**: No validated GTFS feed; stations included as point proximity only, not schedule-based routing
3. **Socioeconomic data granularity**: BPS data at kecamatan level disaggregated to kelurahan via proxies; within-kelurahan variation further modeled via dasymetric mapping to H3
4. **Cross-sectional snapshot**: Single time period, no longitudinal trend analysis
5. **No real-time traffic data in v1**: OSM road classification captures network structure but not congestion; traffic API is a future enhancement
6. **What-if simulator is indicative**: Simplified buffer/isochrone model for scenario simulation, not a full transit assignment model

---

## 2.3 Data Requirements & Schema Design

### Raw Datasets

| # | Dataset | Description | Granularity | Format | Source | Access |
|---|---------|-------------|-------------|--------|--------|--------|
| 1 | TransJakarta BRT GTFS | Full BRT + Mikrotrans network | Stop/route/trip level | GTFS ZIP | [Mobility Database](https://database.mobilitydata.org) | Open |
| 2 | KRL Commuterline GTFS | Jabodetabek rail network | Stop/route/trip level | GTFS ZIP | [Mobility Database](https://database.mobilitydata.org) | Open |
| 3 | MRT Jakarta GTFS | North–South MRT line | Stop/route/trip level | GTFS ZIP | [Mobility Database](https://database.mobilitydata.org) | Open |
| 4 | LRT Jabodebek stations | Station locations only (no schedule) | Point | Manual GeoJSON | Wikipedia / official sources | Open (manual) |
| 5 | OSM road network | Road segments with classification (highway tag) | Segment level | PBF → GeoDataFrame | [Geofabrik Java extract](https://download.geofabrik.de/asia/indonesia/java-latest.osm.pbf) | Open |
| 6 | POIs — strict categories | Hospitals, schools, CBD, transit, markets, industrial, gov offices | Point/polygon | GeoJSON | [Overpass API](https://overpass-api.de) | Open |
| 7 | Administrative boundaries | Kelurahan + kecamatan + kota/kab polygons | Polygon | GeoJSON | GADM / Indonesia Geoportal | Open |
| 8 | BPS demographic data | Population, poverty rate, household expenditure | Kecamatan (some kelurahan) | CSV / published tables | [BPS](https://jakarta.bps.go.id) + BPS Jabar, Banten | Open |
| 9 | WorldPop population raster | Gridded population estimates (~100m) | Raster cell | GeoTIFF | [WorldPop](https://www.worldpop.org) | Open |
| 10 | H3 hexagonal grid | Generated grid at resolution 8 covering Jabodetabek | Hexagon | Generated (h3-py) | Computed | N/A |

### Future enhancement datasets (v2, budget-dependent)

| # | Dataset | Description | Source | Cost |
|---|---------|-------------|--------|------|
| 11 | Google Maps Distance Matrix API | Real travel times by driving/transit between points | Google Maps Platform | ~$5–10/1000 requests |
| 12 | TomTom Traffic Stats | Historical traffic speed profiles by road segment | TomTom API | Free tier available |
| 13 | SUSENAS microdata | Household-level socioeconomic data | BPS (restricted access) | Application required |

---

### Target Schema — Kelurahan Level (primary analysis unit)

| Field | Type | Description | Source Dataset(s) | In Paper | In Product |
|-------|------|-------------|-------------------|----------|------------|
| `kelurahan_id` | string | Unique admin code (BPS code) | #7 | ✓ | ✓ |
| `kelurahan_name` | string | Name | #7 | ✓ | ✓ |
| `kecamatan_name` | string | Parent kecamatan | #7 | ✓ | ✓ |
| `kota_kab_name` | string | Parent kota/kabupaten | #7 | ✓ | ✓ |
| `geometry` | polygon | Kelurahan boundary | #7 | ✓ | ✓ |
| `area_km2` | float | Area in square kilometers | Computed from #7 | ✓ | ✓ |
| **— NEED INDICATORS —** | | | | | |
| `population` | int | Total population | #8 + #9 | ✓ | ✓ |
| `pop_density` | float | Population per km² | Computed | ✓ | ✓ |
| `poverty_rate` | float | % population below poverty line | #8 (kecamatan disaggregated) | ✓ | ✓ |
| `avg_household_expenditure` | float | Monthly avg (IDR) | #8 (kecamatan disaggregated) | ✓ | ✓ |
| `zero_vehicle_hh_pct` | float | Estimated % households with no motor vehicle | #8 modeled from kecamatan + density proxy | ✓ | ✓ |
| `dependency_ratio` | float | (Age <15 + >64) / working-age population | #8 | ✓ | ✓ |
| `tni_score` | float [0,1] | Composite Transit Need Index | Computed | ✓ | ✓ |
| **— ROAD NETWORK INDICATORS —** | | | | | |
| `road_length_km` | float | Total road length within kelurahan | #5 | ✓ | ✓ |
| `road_density_km_per_km2` | float | Road length / area | Computed | ✓ | ✓ |
| `pct_primary_secondary` | float | % of road length that is primary or secondary road | #5 (OSM highway tag) | ✓ | ✓ |
| `pct_residential_tertiary` | float | % of road length that is residential/tertiary | #5 | ✓ | ✓ |
| `pct_footway_pedestrian` | float | % of road length classified as footway/pedestrian/path | #5 | ✓ | ✓ |
| `avg_road_class_score` | float | Weighted average road hierarchy score (primary=5, secondary=4, tertiary=3, residential=2, footway=1) | #5 Computed | ✓ | ✓ |
| `network_connectivity` | float | Intersection density (nodes/km²) or alpha index | #5 Computed | ✓ | ✓ |
| **— ACCESS INDICATORS —** | | | | | |
| `n_transit_stops` | int | Count of unique transit stops within boundary | #1–4 | ✓ | ✓ |
| `n_transit_routes` | int | Count of unique routes serving stops within boundary | #1–4 | ✓ | ✓ |
| `avg_headway_min` | float | Average scheduled headway (minutes) across all stops in boundary | #1–3 (stop_times.txt) | ✓ | ✓ |
| `min_dist_to_transit_m` | float | Distance from kelurahan centroid to nearest transit stop (network distance if possible, else Euclidean) | #1–4, #5 | ✓ | ✓ |
| `transit_mode_diversity` | int | Count of distinct transit modes available (BRT, KRL, MRT, LRT, Mikrotrans) | #1–4 | ✓ | ✓ |
| `road_adjusted_access` | float | Access score weighted by road network quality (penalize areas with poor pedestrian/road connectivity to nearest stop) | #1–5 Computed | ✓ | ✓ |
| `poi_reach_cbd_min` | float | Travel time (transit) to nearest CBD zone — **priority POI** (see §2.6a) | #1–3, #6 (r5py isochrone) | ✓ | ✓ |
| `poi_reach_hospital_min` | float | Travel time (transit) to nearest major hospital (RS tipe A/B / RSUD) | #1–3, #6 | ✓ | ✓ |
| `poi_reach_school_min` | float | Travel time (transit) to nearest SMA/SMK/University | #1–3, #6 | ✓ | ✓ |
| `poi_reach_market_min` | float | Travel time (transit) to nearest major market/pasar | #1–3, #6 | ✓ | ✓ |
| `poi_reach_industrial_min` | float | Travel time (transit) to nearest industrial/job zone | #1–3, #6 | ✓ | ✓ |
| `poi_reach_govoffice_min` | float | Travel time (transit) to nearest government service office | #1–3, #6 | ✓ | ✓ |
| **— FARE TIER INDICATORS —** | | | | | |
| `best_mode_fare_tier` | int [1–4] | Fare tier of the best available transit mode in the area (see §2.6b) | #1–4 Computed | ✓ | ✓ |
| `has_affordable_mode` | bool | Whether any fare tier 1–2 mode (KRL, regular TransJakarta) is available | #1–4 Computed | ✓ | ✓ |
| **— TRAFFIC EXTENSION (v2) —** | | | | | |
| `avg_traffic_speed_kmh` | float \| null | Average road traffic speed in spatial unit (null until traffic API integrated) | #11/#12 (future) | ✓ | ✓ |
| `peak_congestion_index` | float \| null | Peak-hour speed / free-flow speed ratio (null until traffic API integrated) | #11/#12 (future) | ✓ | ✓ |
| `traffic_adjusted_access` | float \| null | Access score re-weighted by actual traffic conditions (null until v2) | Future computed | ✓ | ✓ |
| `tai_score` | float [0,1] | Composite Transit Accessibility Index | Computed | ✓ | ✓ |
| **— DERIVED —** | | | | | |
| `equity_gap` | float [-1,1] | tni_score − tai_score | Computed | ✓ | ✓ |
| `quadrant` | enum | Q1–Q4 classification | Computed | ✓ | ✓ |

### Target Schema — H3 Level (derived from kelurahan)

Same fields as kelurahan, plus:

| Field | Type | Description | Derivation Method |
|-------|------|-------------|-------------------|
| `h3_index` | string | H3 cell ID at resolution 8 | h3-py |
| `h3_geometry` | polygon | Hexagon boundary | h3-py |
| `h3_area_km2` | float | ~0.74 km² (constant) | h3-py |
| `is_edge_cell` | boolean | True if cell straddles study area boundary | Spatial check |
| `kelurahan_ids` | list[string] | Kelurahan(s) overlapping this cell | Spatial overlay |
| `population` | float | Dasymetric-estimated population (not census count) | **Dasymetric**: WorldPop raster (#9) aggregated to H3 cell |
| `pop_density` | float | population / h3_area_km2 | Computed |
| `poverty_rate` | float | Redistributed from kelurahan | **Dasymetric**: population-weighted from overlapping kelurahan(s) |
| `avg_household_expenditure` | float | Redistributed | **Dasymetric**: population-weighted |
| `zero_vehicle_hh_pct` | float | Redistributed | **Dasymetric**: population-weighted |
| `dependency_ratio` | float | Redistributed | **Dasymetric**: population-weighted |
| `road_length_km` | float | Road segments clipped to hex | **Area-weighted**: clip road network to H3 cell, sum lengths |
| `road_density_km_per_km2` | float | road_length / h3_area | Computed from clipped network |
| `pct_primary_secondary` | float | From clipped road segments | **Area-weighted**: computed from clipped segments |
| `network_connectivity` | float | Intersection density in hex | **Area-weighted**: count nodes within H3 cell |
| `n_transit_stops` | int | Stops within hex | **Point-in-polygon**: direct spatial join |
| `n_transit_routes` | int | Routes serving stops in hex | **Point-in-polygon**: from GTFS spatial join |
| `avg_headway_min` | float | From stops within hex | **Point-in-polygon**: from GTFS |
| `min_dist_to_transit_m` | float | From hex centroid | **Direct computation**: hex centroid to nearest stop |
| `poi_reach_*` | float | Travel time from hex centroid | **Direct computation**: r5py from hex centroid |
| All other derived fields | | Same as kelurahan | Computed from H3-level inputs |

### H3 Derivation Strategy (finalized — MVP-7)

| Data type | Derivation method | Source unit | Rationale |
|-----------|-------------------|------------|-----------|
| Socioeconomic (population, poverty, expenditure, vehicle ownership) | **Dasymetric mapping** via WorldPop raster | Kelurahan (from BPS kecamatan via step 9) | Population not uniform within kelurahan; WorldPop ~100m resolution as allocation surface |
| Infrastructure (road network, class proportions) | **Area-weighted spatial clip** | OSM segments | Physical features with known geometries; clip to H3 boundary, recompute per cell |
| Point features (transit stops, POIs) | **Point-in-polygon** spatial join | GTFS/Overpass points | Exact coordinates; assign to containing H3 cell via `h3.geo_to_h3()` |
| Travel times (poi_reach_*, min_dist_to_transit) | **Direct computation** from H3 centroid | r5py routing | Fresh routing from each centroid; redistributing kelurahan values would be methodologically incorrect |

**Dasymetric formula (rate-based indicators)**:
```
value_h3 = sum(pop_raster_in_h3_and_kelurahan_k * value_kelurahan_k) / sum(pop_raster_in_h3)
```
For cells entirely within one kelurahan (vast majority): rate passes through unchanged.
For cells straddling boundaries: population-weighted average of overlapping kelurahan values.

**Grid generation**: `h3.polyfill_geojson(study_area, res=8)` → clip to GADM boundary → ~15,000–20,000 cells. Buffer 500m for edge handling; flag `is_edge_cell` for sensitivity.

**MAUP mitigation** (Javanmard et al. 2023): Dual-resolution comparison (kelurahan vs H3) quantifies scale and zoning effects. Identical pipeline at both resolutions; differences attributable to spatial unit choice.

**Resolution sensitivity**: Full pipeline at res-7 (~3–5k cells), res-8 (primary), res-9 (~50–70k cells). Compare via confusion matrix (quadrant stability), Cohen's kappa, Gini comparison, and LISA pattern stability. Res-9 r5py computation (~60k origins) may require stratified sampling fallback.

*Full detail with derivation formulas, edge case handling, and implementation sequence: `docs/drafts/mvp7-h3-methodology.md`*

---

## 2.4 Data Acquisition Plan

| Dataset | Source URL | Method | Access | Rate Limits / Notes |
|---------|-----------|--------|--------|---------------------|
| TransJakarta GTFS | mobilitydata.org | Direct download | Open | Check feed freshness date |
| KRL GTFS | mobilitydata.org | Direct download | Open | Check feed freshness date |
| MRT GTFS | mobilitydata.org | Direct download | Open | Check feed freshness date |
| LRT stations | Manual compilation | Manual GeoJSON | Open | ~18 stations; verify against official list |
| OSM road network | download.geofabrik.de | Download java-latest.osm.pbf → clip to Jabodetabek bbox with osmium | Open | ~600 MB; update periodically |
| POIs (strict) | overpass-api.de | Overpass QL query per category with Jabodetabek bbox | Open | Rate-limited; batch queries, cache results |
| Admin boundaries | gadm.org + geoportal.ina.go.id | Download | Open | Verify kelurahan count matches BPS |
| BPS demographic | jakarta.bps.go.id + bps.go.id (Jabar, Banten) | Manual download / scrape published tables | Open | Multi-source assembly required for Bodetabek |
| WorldPop raster | worldpop.org | Download Indonesia 2020 constrained population | Open | ~100m resolution GeoTIFF |
| H3 grid | Generated in code | h3-py `polyfill` on Jabodetabek boundary at res 8 | N/A | ~15,000–20,000 cells |

**Restricted / future datasets** (flagged per skill):
- SUSENAS microdata → requires BPS application; synthetic fallback = kecamatan-level proxies (already planned)
- Google Maps API / TomTom → paid; v2 enhancement

---

## 2.5 Data Processing & Wrangling Plan

| Step | Operation | Input | Output | Tool | Notes |
|------|-----------|-------|--------|------|-------|
| 1 | **Parse GTFS feeds** | 3 GTFS ZIPs (#1–3) | Unified stops, routes, trips, stop_times DataFrames | `gtfs_kit` or `partridge` (Python) | Merge all modes into single transit stop dataset with mode tag |
| 2 | **Add LRT stations** | Manual GeoJSON (#4) | Append to unified stops (no schedule data) | `geopandas` | Flag as `schedule_available=False` |
| 3 | **Extract + clip road network** | Java PBF (#5) | Jabodetabek road GeoDataFrame with highway class | `osmium` → `osmnx` or `pyrosm` | Filter to Jabodetabek bbox; keep highway tags: motorway, trunk, primary, secondary, tertiary, residential, living_street, footway, pedestrian, path, cycleway |
| 4 | **Compute road metrics per kelurahan** | Road GDF + kelurahan polygons (#7) | Road length, density, class proportions, intersection density per kelurahan | `geopandas` spatial join + overlay | Clip roads to kelurahan; count intersections (degree ≥ 3 nodes) |
| 5 | **Extract strict POIs** | Overpass API (#6) | Filtered POI GeoDataFrame | `requests` + Overpass QL | Separate queries per category with strict OSM tag filters (see POI Filtering Rules below) |
| 6 | **Manually verify POIs** | POI GeoDataFrame | Verified POI set | Manual review + web check | Spot-check hospitals (verify tipe A/B), schools (verify SMA/SMK/univ), CBD zones (define as polygons) |
| 7 | **Load admin boundaries** | GeoJSON (#7) | Kelurahan GeoDataFrame with BPS codes | `geopandas` | Join with BPS codes; verify polygon count |
| 8 | **Assemble BPS demographic data** | Multiple CSV/tables (#8) | Unified demographic table keyed by kecamatan/kelurahan BPS code | `pandas` | Multi-source: DKI Jakarta, Kab/Kota Bogor, Depok, Tangerang, Bekasi |
| 9 | **Disaggregate kecamatan data to kelurahan** | Demographic table + kelurahan boundaries + WorldPop (#9) | Kelurahan-level estimates | `pandas` + `rasterstats` | Population-weighted disaggregation using WorldPop zonal stats |
| 10 | **Compute Transit Need Index (TNI)** | Kelurahan demographics | `tni_score` per kelurahan | `pandas` + `sklearn.preprocessing` | Min-max normalize each indicator → weighted sum (default: equal weights) |
| 11 | **Compute transit stop metrics per kelurahan** | Unified stops + kelurahan polygons | Stop count, route count, mode diversity, avg headway | `geopandas` spatial join + `pandas` groupby | Headway = median of (stop_times departure diffs) per stop, then average across kelurahan |
| 12 | **Compute network distance to nearest transit** | Kelurahan centroids + transit stops + road network | `min_dist_to_transit_m` (network distance) | `osmnx` shortest path or `networkx` | Network distance preferred; fall back to Euclidean if network routing too slow |
| 13 | **Compute road-adjusted access score** | Road network metrics + transit proximity | `road_adjusted_access` | Custom formula | Penalize: high distance + low pedestrian road % + low intersection density |
| 14 | **Compute POI travel times (transit)** | Kelurahan centroids + POIs + GTFS + road network | `poi_reach_*_min` (6 POI categories) | `r5py` (R5 routing engine, Python wrapper) | Transit travel time from centroid to nearest POI per category; weekday AM peak |
| 15 | **Compute Transit Accessibility Index (TAI)** | All access indicators | `tai_score` per kelurahan | `pandas` + `sklearn.preprocessing` | Min-max normalize → weighted sum |
| 16 | **Compute equity gap + quadrant** | TNI + TAI | `equity_gap`, `quadrant` per kelurahan | `pandas` | Gap = TNI − TAI; quadrant from median split |
| 17 | **Generate H3 grid** | Jabodetabek boundary polygon | H3 hexagon GeoDataFrame (res 8) | `h3-py` + `geopandas` | `h3.polyfill_geojson` on boundary → to GeoDataFrame |
| 18 | **Dasymetric mapping: socioeconomic → H3** | Kelurahan-level demographics (from step 9) + WorldPop raster + H3 grid | Socioeconomic estimates per H3 cell | `rasterstats` + `geopandas` overlay | For each H3 cell: (a) extract WorldPop pop sum, (b) find overlapping kelurahan(s), (c) allocate kelurahan-level rates proportionally to WorldPop pop within hex. Formula: `value_h3 = Σ(pop_in_intersection_k × value_kelurahan_k) / pop_h3` |
| 19 | **Area-weighted: road network → H3** | Road GDF + H3 grid | Road metrics per H3 cell | `geopandas` overlay + clip | Clip road segments to each H3 cell; recompute metrics |
| 20 | **Point-in-polygon: stops/POIs → H3** | Unified stops + POIs + H3 grid | Stop/POI counts per H3 cell | `geopandas` spatial join | Direct assignment |
| 21 | **Direct computation: travel times from H3 centroids** | H3 centroids + GTFS + road network + POIs | `poi_reach_*`, `min_dist_to_transit_m` per H3 cell | `r5py` | Same methodology as step 14 but from hex centroids |
| 22 | **Compute TNI, TAI, equity gap, quadrant for H3** | All H3-level indicators | Full H3 analysis table | Same as steps 10, 15, 16 | Identical methodology, different spatial unit |
| 23 | **Gini + Lorenz curve computation** | TAI distribution (kelurahan) + TAI distribution (H3) | Gini coefficients, Lorenz data | `numpy` | Compare equity measure across resolutions |
| 24 | **Spatial autocorrelation (LISA)** | Quadrant classification + geometry (both resolutions) | Moran's I, LISA cluster maps | `pysal` / `esda` | Identify statistically significant transit desert clusters |
| 25 | **What-if scenario engine** | Full analysis table + user-specified new stop location | Recalculated TAI, equity gap, quadrant for affected cells | Custom Python | Buffer around new stop → recalculate access indicators for cells within catchment → re-score |

### Missing Data Strategy

| Issue | Strategy |
|-------|----------|
| Null values in BPS demographic fields | Impute from kecamatan-level parent value (already disaggregated) |
| Kelurahan with zero transit stops | Valid data point (transit desert by definition); `avg_headway_min` = NaN → set to max value (worst case) |
| POIs with ambiguous classification | Manual verification; exclude if uncertain |
| WorldPop raster cells with 0 population in built-up areas | Cross-check against BPS total; flag anomalies |

### Outlier Strategy

- Keep outliers for spatial analysis (extreme values are the signal, not noise)
- Cap POI travel times at 120 minutes (transit routing ceiling)
- Flag but retain kelurahan with area > 20 km² (common in outer Bodetabek; note in limitations)

### Join Keys

| Join | Left key | Right key | Type |
|------|----------|-----------|------|
| Demographics → Kelurahan | BPS kelurahan code | kelurahan_id | 1:1 |
| Transit stops → Kelurahan | stop geometry | kelurahan polygon | spatial (point-in-polygon) |
| Road network → Kelurahan | road geometry | kelurahan polygon | spatial (overlay/clip) |
| WorldPop → H3 | raster cell | H3 polygon | zonal stats |
| Kelurahan rates → H3 | kelurahan polygon | H3 polygon | spatial overlay + population weighting |
| Transit stops → H3 | stop geometry | H3 polygon | spatial (point-in-polygon) |

---

## 2.6 POI Filtering Rules

Each POI category has strict inclusion criteria to avoid noise from irrelevant entries.

### 2.6a CBD Zones — Priority POI with Employment Gravity Weighting

CBD zones are the **highest-priority POI** in this framework. The rationale: millions of commuters travel to Jakarta's CBDs every working day, and the core equity question is whether populations with high transit need can actually reach these job centers by public transit.

**Critical modeling principle — multi-modal journey chains, not station proximity:**

A BSD resident's accessibility to Sudirman is NOT "distance to the nearest KRL station." It is the **full door-to-door multi-modal travel time**: walk/ojek to KRL Serpong → ride to Tanah Abang → transfer to TransJakarta Corridor 1 → ride to Sudirman → walk to office. This is what r5py computes: optimal multi-modal routing across the loaded GTFS network including walking legs, waiting times, and transfers.

This means:
- A spatial unit near a KRL station on the Serpong line that connects to Tanah Abang (→ Sudirman) scores higher than one near a KRL station on a branch line with no direct CBD connection.
- A spatial unit near MRT Lebak Bulus (direct to Bendungan Hilir / Sudirman) scores differently than one near KRL Bekasi (longer ride but tier 1 fare).
- Transfer friction is real — two transfers adds 15–20 min of walking + waiting, even if the clock time seems comparable.

**r5py configuration for multi-modal routing:**
```
transport_mode: TRANSIT
access_mode: WALK
egress_mode: WALK
max_walk_time: 20          # minutes (first/last mile walking cap)
max_trip_duration: 120     # minutes (ceiling)
max_transfers: 3           # typical Jabodetabek commute
transfer_penalty: 600      # seconds (10 min penalty per transfer — captures walking between platforms, waiting, uncertainty)
departure_time: 07:00      # weekday AM peak
departure_window: 60       # minutes (7:00–8:00 AM, r5py samples multiple departures)
```

**CBD gravity weighting:**

Not all CBDs are equal employment destinations. Most white-collar and blue-collar commuters in Jabodetabek travel to the central Jakarta employment corridor (Sudirman–Thamrin, Kuningan, Gatot Subroto, TB Simatupang). Satellite CBDs like BSD and Summarecon serve primarily local populations.

The `poi_reach_cbd_min` field is therefore **not** the travel time to the nearest CBD. It is a **gravity-weighted average travel time** to all CBDs:

```
poi_reach_cbd_weighted = Σ (travel_time_to_CBD_i × gravity_weight_i) / Σ gravity_weight_i

where gravity_weight captures employment pull:
```

| CBD Zone | Approximate Center | Key Anchors | Gravity Weight | Rationale |
|----------|-------------------|-------------|----------------|-----------|
| **Sudirman–Thamrin** | -6.200, 106.823 | SCBD, Wisma 46, Bundaran HI, Thamrin | **5.0** | Financial/corporate HQ corridor — highest employment density in Indonesia |
| **Kuningan** | -6.228, 106.833 | Mega Kuningan, Rasuna Said, embassies | **4.0** | Corporate/diplomatic — second-highest office concentration |
| **Gatot Subroto** | -6.222, 106.810 | Semanggi, Slipi, gov ministries corridor | **3.5** | Government ministry corridor + corporate |
| **TB Simatupang** | -6.292, 106.812 | Arkadia, Cilandak Town Square, tech offices | **3.0** | Growing secondary CBD — tech/startup concentration |
| **Kelapa Gading** | -6.157, 106.907 | Mall Kelapa Gading, office towers | **2.0** | North Jakarta commercial hub |
| **Pantai Indah Kapuk** | -6.112, 106.743 | PIK 2, commercial strip | **1.5** | Emerging commercial |
| **BSD City** | -6.301, 106.652 | BSD Green Office Park, The Breeze | **1.0** | Satellite — primarily local employment |
| **Summarecon Bekasi** | -6.225, 107.000 | Summarecon Mall, office complex | **1.0** | Satellite — primarily local employment |
| **Summarecon Serpong** | -6.242, 106.631 | Summarecon Mall Serpong | **1.0** | Satellite — primarily local employment |

**Why gravity-weighted average, not nearest-CBD:**
- A resident of BSD is 10 min from BSD Green Office Park, but most BSD workers commute to Sudirman (60+ min). Taking `min(travel_time)` would score BSD as highly accessible, which misrepresents the commuting reality.
- The gravity weights ensure Sudirman–Thamrin dominates the weighted average (5.0 out of ~22.0 total weight = ~23% of the score), reflecting its outsized employment pull.
- This is a simplification — ideally we'd use actual commuter flow data (OD matrix) — but gravity weights are a defensible proxy. Sensitivity analysis will test alternative weight schemes.

**How CBD travel time enters TAI:**
`poi_reach_cbd_weighted` is weighted **3× in the TAI composite** relative to other POI categories (upgraded from 2× given the multi-modal chain importance). This reflects the reality that for most Jabodetabek residents, the ability to reach their workplace via transit is the single most important accessibility dimension.

**CBD-station corridor awareness:**
The r5py routing inherently captures which stations connect to which CBDs. For example:
- KRL Serpong line → Tanah Abang transfer → Sudirman area (via Busway or walk)
- MRT from Lebak Bulus → direct to Bundaran HI / Bendungan Hilir
- KRL Bekasi line → Sudirman/Manggarai → walk or Busway transfer
- LRT Jabodebek → Dukuh Atas (MRT/KRL hub) → Sudirman area

No manual corridor mapping is needed — the GTFS network encodes all of this. But the **transfer penalty** (10 min per transfer) ensures that a 2-transfer journey is appropriately scored lower than a direct connection of similar clock time.

**Cumulative journey fare estimate (new schema field):**

| Field | Type | Description |
|-------|------|-------------|
| `est_cbd_journey_fare_idr` | int \| null | Estimated cumulative fare for the optimal multi-modal journey to Sudirman–Thamrin CBD |

Fare estimation logic (simplified):
```
For the r5py optimal path to Sudirman–Thamrin:
- Count legs by mode
- Sum: KRL leg (Rp 3,000 base + Rp 1,000/station, cap Rp 13,000)
       + MRT leg (Rp 3,000 base + distance-based, cap Rp 14,000)
       + TransJakarta leg (Rp 3,500 flat, Rp 20,000 if Royaltrans)
       + LRT leg (Rp 5,000 base + distance-based)
- JakLingko integration: if using JakLingko card, Busway→KRL transfer may be discounted
```

This is a rough estimate — actual fares depend on payment method and integration schemes. The field is nullable and computed post-hoc from the r5py path output, not during routing.

### 2.6b Transit Fare Tier Classification

Not all transit modes are equally affordable. While fare data is not modeled at a granular per-trip level, modes are classified into tiers to capture affordability as a dimension of access:

| Tier | Modes | Approximate Fare Range | Affordability |
|------|-------|----------------------|---------------|
| 1 (Most affordable) | KRL Commuterline, TransJakarta regular BRT + Mikrotrans | Rp 3,500–13,000 (flat/distance-based) | High — accessible to low-income commuters |
| 2 | LRT Jabodebek | Rp 5,000–20,000 (distance-based) | Medium — comparable to KRL but newer |
| 3 | MRT Jakarta | Rp 3,000–14,000 (distance-based) | Medium — similar range but perceived as premium |
| 4 (Most premium) | TransJakarta Royaltrans (premium express bus) | Rp 20,000 (flat) | Low — premium service, price exceeds MRT/LRT |

**How fare tier enters TAI**: `has_affordable_mode` is a binary indicator (tier 1 or 2 available = True). Areas where the *only* available transit is tier 3–4 are penalized in the composite TAI because high-need populations may not afford premium services. This is a coarse proxy — full fare modeling is out of scope but the schema supports future refinement.

### 2.6c Road-Adjusted Access Formula

The `road_adjusted_access` score modifies raw transit proximity by penalizing areas where the road/pedestrian network makes the nearest station effectively unreachable:

```
road_adjusted_access = raw_proximity_score × road_quality_modifier

where:
  raw_proximity_score = 1 - normalize(min_dist_to_transit_m)
    (closer = higher score, 0–1 range)

  road_quality_modifier = w1 × norm(pct_footway_pedestrian)
                        + w2 × norm(network_connectivity)
                        + w3 × norm(road_density_km_per_km2)

  default weights: w1 = 0.4, w2 = 0.35, w3 = 0.25
    (pedestrian infrastructure matters most, then connectivity, then overall density)

  road_quality_modifier is clamped to [0.3, 1.0]
    (floor of 0.3 prevents complete zeroing — even poor road areas have some access)
```

**Interpretation**: A kelurahan 300m from a KRL station but with zero footways and dead-end roads (road_quality_modifier ≈ 0.3) gets an adjusted score of 0.85 × 0.3 = 0.255. A kelurahan 600m away but with good pedestrian paths and a grid network (modifier ≈ 0.9) gets 0.70 × 0.9 = 0.630 — correctly ranked higher despite being farther.

**Sensitivity analysis**: Test w1/w2/w3 variations to ensure results are robust to weight choices.

### 2.6d Traffic API Extension Architecture (v2)

The schema includes three null-by-default traffic fields (`avg_traffic_speed_kmh`, `peak_congestion_index`, `traffic_adjusted_access`) designed for plug-in integration:

**Data source options** (v2, budget-dependent):
1. **TomTom Traffic Stats API** (preferred for v2): Historical speed profiles per road segment, free tier available. Aggregate 6 months of weekday AM-peak speeds per spatial unit.
2. **Google Maps Distance Matrix API**: Real travel times between origin-destination pairs. More expensive but captures actual routing + congestion.
3. **Uber Movement** (if available for Jakarta): Historical travel time aggregates.

**Integration pattern**:
```
# v1: traffic fields are null, TAI computed without traffic
# v2: traffic pipeline fills these fields, TAI recomputed with traffic modifier

traffic_adjusted_access = road_adjusted_access × traffic_modifier

where:
  traffic_modifier = peak_congestion_index  (speed_peak / speed_freeflow)
  Range: 0.2 (severe congestion) to 1.0 (free flow)
```

This means the v1 product can ship without traffic data, and v2 simply adds a pipeline step that populates the null fields and re-runs the TAI computation. No schema changes needed.

### 2.6e Other POI Categories (strict filters)

| Category | OSM Tags | Additional Filter | Verification |
|----------|----------|-------------------|--------------|
| **Hospital** | `amenity=hospital` | Name contains "RSUD" or "RS" + tipe A or B (check against Kemenkes list) | Manual: verify against Kemenkes RS Online database |
| **School** | `amenity=school` OR `amenity=university` | Only SMA, SMK, Madrasah Aliyah, University/Politeknik (exclude SD, SMP, TK) | Filter by `name` patterns; manual spot-check |
| **Transit station** | From GTFS data (not OSM) | Already in datasets #1–4 | N/A — authoritative source |
| **Market** | `amenity=marketplace` OR `shop=supermarket` | Only major pasar tradisional (> 100 vendors, named) + large supermarkets/hypermarkets | Filter by name recognition; exclude mini/convenience |
| **Industrial zone** | `landuse=industrial` | Only major industrial estates (Jababeka, MM2100, KIIC, Pulogadung, Cakung, etc.) | Filter by area > 10 hectares or named estates |
| **Government office** | `amenity=townhall` OR `office=government` | Kelurahan office, kecamatan office, kantor pemerintah kota/kab | Filter by `name` containing "Kantor Kelurahan/Kecamatan/Walikota/Bupati" |

---

## 2.7 EDA Plan

| Check | What to look for | Visualization | In Paper | In Product |
|-------|-----------------|---------------|----------|------------|
| TNI distribution | Skew, outliers, urban-suburban gradient | Histogram + choropleth | ✓ | Optional |
| TAI distribution | Skew, bimodality (transit-rich vs transit-poor) | Histogram + choropleth | ✓ | Optional |
| TNI vs TAI correlation | How tightly do need and access align? | Scatter plot (TNI vs TAI, colored by quadrant) | ✓ | ✓ |
| Quadrant spatial pattern | Where are Q4 transit deserts? Do they cluster? | Choropleth map (4-color quadrant) | ✓ | ✓ |
| Road network quality spatial pattern | Do transit deserts also have poor road networks? | Choropleth of road density, pedestrian road % | ✓ | ✓ |
| LISA clusters | Statistically significant transit desert clusters | LISA cluster map (HH, HL, LH, LL) | ✓ | Optional |
| Resolution comparison | How does quadrant classification change kelurahan → H3? | Side-by-side choropleths + confusion matrix | ✓ | ✓ |
| Gini comparison | Is transit access more or less equitable at H3 vs kelurahan? | Lorenz curves overlaid | ✓ | Optional |
| POI accessibility patterns | Which POI types are hardest to reach by transit? | Box plot of travel times by POI category | ✓ | ✓ |

---

## Methodology Summary (1-page condensed)

**Research Question**: Does transit accessibility in Jabodetabek align with socioeconomic need, and does the answer depend on the spatial resolution of analysis?

**Method**: Construct a two-axis Transit Equity Matrix (Transit Need Index × Transit Accessibility Index) for ~1,800 kelurahan and ~15,000–20,000 H3 hexagons across Jabodetabek. TNI combines 5 indicators (population density, poverty rate, household expenditure [inverted], zero-vehicle household rate, dependency ratio) with equal weighting, min-max normalization, and winsorization at 2nd/98th percentiles. TAI uses a 5-layer model (first-mile 20%, service quality 15%, CBD journey chain 35%, last-mile 15%, cost competitiveness 15%) with three-way generalized cost comparison (transit vs car vs motorcycle). CBD travel time is gravity-weighted across 9 employment zones.

**CBD as priority POI**: Nine defined CBD zones (Sudirman-Thamrin, Kuningan, Simatupang, Gatot Subroto, Kelapa Gading, PIK, BSD, Summarecon Bekasi, Summarecon Serpong) anchor the accessibility analysis, reflecting the reality that millions commute to these centers daily.

**Fare tier modeling**: Transit modes are classified into 4 affordability tiers (KRL + regular TransJakarta as most affordable → Royaltrans as most premium). Areas where only premium modes are available are penalized in TAI, since high-need populations may not afford them.

**Road network integration**: OSM-derived pedestrian path percentage (weight 0.4), intersection connectivity (0.35), and road density (0.25) form a road_quality_modifier that adjusts raw transit proximity. A station 300m away behind a highway with no sidewalk scores lower than one 600m away on a walkable grid.

**Traffic API extension (v2)**: Schema includes null-by-default fields for historical traffic speed and congestion index. When populated (via TomTom or Google Maps API), these automatically feed into a traffic_adjusted_access score. No schema change needed — plug-in architecture.

**Dual resolution**: Kelurahan is the primary analysis unit (census-aligned). H3 resolution 8 (~0.74 km²) is derived via dasymetric mapping from kelurahan-level values (socioeconomic), area-weighted spatial clipping (infrastructure), point-in-polygon (stops/POIs), and direct r5py routing (travel times). Sensitivity at res-7 and res-9. Comparing quadrant classifications across resolutions quantifies the MAUP effect (Javanmard et al. 2023).

**Equity measurement**: Gini coefficient and Lorenz curves measure overall distributional equity; Moran's I and LISA identify spatial clustering of transit deserts. Quadrant classification (Q1–Q4) enables actionable policy categorization.

**What-if simulator**: Hypothetical transit node placement recalculates TAI within a catchment radius, enabling scenario comparison of equity score improvement across quadrants.

**Data**: Open-source GTFS (TransJakarta, KRL, MRT), OSM road network, BPS demographics, WorldPop population raster, OSM-sourced strict POIs, GADM administrative boundaries. LRT and informal transit are acknowledged gaps.

**Compute**: Designed for local machine execution (Python/geopandas/r5py), with cloud compute as optional scale-up for heavy r5py routing.

---

---

## 2.7 Commuter Journey Estimation (Product Layer)

*Added 2026-04-15. Governs `web/src/lib/journey.ts`.*

This section documents the methodology for the commuter journey comparison feature. All estimates are derived from zone-level aggregate data — they are **indicative for comparison purposes**, not precise trip plans (which would require GTFS trip planning, not available in this product).

### 2.7.1 Network Distance (Circuity Factor)

Straight-line (Euclidean/haversine) distance systematically underestimates actual travel distance in urban road networks. A **circuity factor** converts Euclidean to network distance:

```
d_network = d_euclidean × C
```

For Jabodetabek, **C = 1.35** — the ratio of network distance to Euclidean distance typical for radial Asian megacity grids. This value is consistent with Boeing (2016) findings for similar urban forms and with OSM-based analysis of Jakarta's street network.

**References**: Barthelemy (2011) *Spatial networks*; Boeing (2016) *OSMnx*; Tsiotas & Polyzos (2015) on circuity in developing-country cities.

### 2.7.2 Generalized Cost Formula (Transit)

Transit comparison uses **Generalized Cost (GC)** rather than financial cost alone. GC captures the full perceived burden of a trip, including time spent walking and waiting which commuters weight more heavily than in-vehicle time:

```
GC_transit = fare + VOT × (IVT + λ_walk × t_walk + λ_wait × t_wait + t_transfer)
```

| Parameter | Value | Source |
|-----------|-------|--------|
| VOT (Value of Time) | Rp 500/min (Rp 30,000/hr) | BPS 2023 median urban household expenditure ~Rp 4.5M/month ÷ 160 working hours; conservative estimate |
| λ_walk (walk penalty) | 2.0 | Wardman (1998) meta-analysis; replicated in SE Asia by Sukor & Bhayo (2024) |
| λ_wait (wait penalty) | 2.5 | Wardman (1998); consistent with TCQSM (2013) recommended values |
| IVT | In-vehicle time (min) | Derived from `poi_reach_cbd_min` scaled by distance ratio |
| t_walk | Walk time (min) | First mile: `min_dist_to_transit_m` ÷ 80 m/min; Last mile: 5 min flat |
| t_wait | Wait time (min) | `avg_headway_min` ÷ 2 (random arrival assumption) |
| t_transfer | Transfer penalty (min) | See §2.7.4 |

GC determines the **"Recommended"** mode label. Displayed costs are financial costs (fare only) so users can realistically budget.

### 2.7.3 BPR Distance-Banded Speeds (Road Modes)

Fixed average speeds overestimate short-trip times in dense inner-city areas and underestimate long-trip times in outer Bodetabek. Speeds are banded by network distance, calibrated to BPTJ (2022) Jakarta peak-hour speed survey:

| Network distance | Motorcycle | Car |
|-----------------|------------|-----|
| < 5 km (inner city) | 22 km/h | 18 km/h |
| 5–15 km (middle ring) | 30 km/h | 25 km/h |
| > 15 km (outer Bodetabek) | 38 km/h | 32 km/h |

**References**: Bureau of Public Roads (1964) volume-delay function; Akçelik (1991) speed-flow relationships; BPTJ (2022) *Jakarta Metropolitan Transportation Survey*.

### 2.7.4 Transfer Penalty

Each transit transfer imposes a perceived time penalty beyond actual wait time (boarding friction, uncertainty). Transfer count is estimated from network distance bands, which proxy corridor crossing likelihood in Jabodetabek's radial transit network:

| Network distance | Expected transfers | Time equivalent |
|-----------------|-------------------|----------------|
| < 5 km | 0 | +0 min |
| 5–15 km | 1 | +10 min |
| > 15 km | 2 | +20 min |

**References**: Wardman et al. (2016) transfer penalty meta-analysis; TCQSM (2013) §4.2.

### 2.7.5 Two-Zone Composite (Destination Zone)

When the user-selected destination falls within a mapped zone, **both origin and destination zone data** are used to improve headway estimation. The corridor headway is the bottleneck (maximum) of home and destination zone headways:

```
headway_effective = max(headway_home, headway_dest)
```

This reflects the real-world constraint: a commuter travelling from a high-frequency home corridor to a low-frequency destination corridor is limited by the weaker link. When destination zone data is unavailable (user pins a point outside mapped zones), the home zone headway is used.

**References**: Páez et al. (2012) two-point accessibility; Boisjoly & El-Geneidy (2016) O-D accessibility measurement.

### 2.7.6 IVT Scaling for Non-CBD Destinations

Pipeline data provides transit metrics calibrated to **Sudirman–Thamrin CBD** as destination. For arbitrary office locations, in-vehicle time is scaled proportionally:

```
IVT_scaled = IVT_cbd × (d_network(home→office) / d_network(home→CBD))
```

Walk time and wait time are not scaled — they are properties of the home zone and do not change with destination. Fare is scaled by the same ratio as IVT, consistent with distance-based fare structures on KRL and MRT.

**Limitation**: This scaling assumes comparable transit corridor density along the home→office path as the home→CBD path. It may overestimate transit access for trips that do not follow major transit corridors.

### 2.7.7 Ride-Hailing Tariffs

GoRide and GoCar tariffs are estimated from 2024 market rates:

| Mode | Rate | Minimum | Wait time |
|------|------|---------|-----------|
| GoRide | Rp 2,500/km | Rp 10,000 | 3 min |
| GoCar | Rp 4,000/km | Rp 20,000 | 5 min |

Surge pricing is not modelled. Actual fares vary by time of day, demand, and promotional pricing.

### 2.7.8 Fuel Costs (Private Modes)

| Mode | Rate | Basis |
|------|------|-------|
| Motorcycle | Rp 1,200/km | Pertalite Rp 10,000/L at ~8 km/L |
| Car | Rp 2,000/km | Pertamax Rp 14,000/L at ~7 km/L |

Parking costs added for longer trips: Rp 5,000 motorcycle (>5 km), Rp 15,000 car (>3 km).

---

*Signed off: 2026-03-21 (MVP-81). All formulas verified, pipeline steps complete and ordered, limitations reviewed. Journey estimation §2.7 added 2026-04-15. Ready for paper Methods section (E4) and data pipeline implementation (E6).*

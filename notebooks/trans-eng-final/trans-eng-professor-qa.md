# Trans-Eng Final Project — Professor Q&A Responses

**Student**: Dhaneswara Mandrasa
**Course**: Transportation Engineering, Hiroshima University AY2026
**Project title**: *Mode Choice and Accessibility Equity in Jabodetabek Commuter Corridors: A Nested Logit and Mixed Logit Analysis with Policy Simulation*

---

## Q1. Research Question

How does the available transport mode set affect commuter welfare across income groups in Jabodetabek corridors, and what is the marginal welfare gain of adding a new rail link to transit-desert zones?

---

## Q2. Method

**Four-stage Travel Behavior model:**

1. **Multinomial Logit (MNL)** — baseline mode choice over 9 alternatives (Car, Motorcycle, 4-wheel ridehailing, 2-wheel ridehailing, KRL commuter rail, TransJakarta BRT, RoyalTrans express, LRT Jabodebek, MRT Jakarta) with a linear-in-parameters systematic utility:

   ```
   V_m = ASC_m + β_time,m · T_m + β_cost · C_m
   ```

   where T_m is door-to-door linked-trip travel time (minutes) and C_m is full trip cost (Rp '000). β_time is mode-specific (9 values); β_cost is generic across modes.

2. **Nested Logit (NL)** — 3-nest ownership-based structure to correct the IIA violation that is particularly acute when Car and Motorcycle compete in the same choice set:

   ```
   Nest 1: Own Vehicle   (Car, Moto)
   Nest 2: Ridehailing   (4WRH, 2WRH)
   Nest 3: Transit       (KRL, TJ, Royal, LRT, MRT)
   ```

   Within-nest inclusive value (Train 2009 dividing convention):

   ```
   IV_nest = ρ · ln Σ_{m ∈ nest} exp(V_m / ρ)
   ```

   Nest-specific ρ values: ρ_OwnVehicle = 0.55, ρ_Ridehailing = 0.70, ρ_Transit = 0.75
   (anchored to Bastarianto et al. 2019, Bekasi–Jakarta NL estimate λ_hwh = 0.55).

3. **Mixed Logit (MXL)** — random ASCs on 3 key alternatives (Car, Motorcycle, TransJakarta) to test for unobserved preference heterogeneity beyond nest correlation. Specification follows Ilahi et al. (2021) Model 3 (MXL with 8 alternatives, random ASC on MC as baseline):

   ```
   U_in = ASC_i + η_in + β_time,i · t_in + β_cost · c_in + ε_in
   ```

   where η_in ~ N(0, σ_i²) is the individual-specific random intercept for alternative i. Random ASCs capture that some commuters inherently prefer Car (or Moto, or TJ) more than the average, beyond what time and cost explain.

   Estimation: Simulated MLE with 200 Halton draws (Train 2009; 200 Halton ≈ 1,000 pseudo-random in coverage). LR test against NL: H₀ = no unobserved heterogeneity (all σ_i = 0). On synthetic data with fixed DGP parameters, we expect to fail to reject H₀ — this is the correct diagnostic outcome, demonstrating the L07 "be willing to reject the richer model" principle.

4. **Logsum welfare measure (McFadden 1978)** — consumer surplus change from policy scenarios, computed from the best-supported model (NL if LR test fails to reject; MXL if heterogeneity is detected):

   ```
   ΔCS_n = [LS_after − LS_before] / |β_cost|     (Rp per trip)
   ```

   where LS = ln Σ_nest exp(IV_nest) is the upper-level NL logsum (or the MXL simulated logsum). Aggregated by zone × income segment to produce an equity-comparable welfare change map.

**Policy simulation**: 8 scenarios (KRL extension to transit-desert zones, MRT Phase 2, toll pricing, RoyalTrans frequency, etc.), each reported as mode share before/after and ΔCS by zone × income group.

---

## Q3. Data

- **Unit of analysis**: 7 origin zones → 1 destination (Jakarta CBD). Each zone stratified by 3 income segments, giving 21 zone-income combinations.

- **Key variables**:
  - Mode choice (9 alternatives; availability varies by zone)
  - Travel time per mode per OD pair (minutes, peak hour)
  - Travel cost per mode per OD pair (Rp '000 — Ilahi's cost-unit convention)
  - Income segment (low / middle / high)
  - Vehicle access (car access, motorcycle access — controls Own Vehicle nest availability)

- **Data provenance — every value traceable to a PDF in `docs/literature/`**:

### 3.1 Zone definitions and aggregate attributes

| Variable | Source | PDF? |
|---|---|---|
| Zone boundaries (7 zones) | Kecamatan membership of 1,502 kelurahan from `kelurahan_scores.geojson` | Pipeline data |
| Zone population | Aggregated from kelurahan-level BPS population | Pipeline data |
| Zone mean expenditure → income | `avg_household_expenditure` ÷ 0.70 (standard SUSENAS expenditure-to-income ratio) | Pipeline data; ratio from BPS methodology |
| Distance to CBD (km) | `distance_to_sudirman_km` — road network distance from pipeline | Pipeline data |

### 3.2 Income segments and vehicle access

**All segment thresholds and ownership rates are anchored to Ilahi et al. (2021)** — the same peer-reviewed Greater Jakarta mode choice study from which the β parameters are transferred. This ensures internal consistency (parameters and sample characteristics from the same source).

| Segment parameter | Value | Source |
|---|---|---|
| Low income share (33.30%) | < IDR 5M/month — Ilahi Table 6, row "Row percentage" (p. 412) | Ilahi et al. (2021) §3.3, Table 6: income × trip chain cross-tabulation |
| Mid income share (50.30%) | IDR 5–15M/month — Ilahi Table 6 |
| High income share (16.40%) | > IDR 15M/month — Ilahi Table 6 |
| Low income mean (Rp 3,000k/mo) | Midpoint of 0–5M range, weighted upward for urban commuter sample | Ilahi (2021) §3.3: income categories defined on p. 410 |
| Middle income mean (Rp 9,000k/mo) | Midpoint of 5–15M range |
| High income mean (Rp 22,000k/mo) | Right-tail estimate for > 15M category |
| **Car access, overall** | **25.60%** of sample has access to car | **Ilahi Table 3 (p. 407)**: 23.80% HH access / 30.20% individual access |
| **MC access, overall** | **67.90%** of sample has access to motorcycle | **Ilahi Table 3 (p. 407)**: 60.00% HH access / 88.50% individual access |
| Car access by income | Low 5% / Mid 26% / High 65% (weighted avg → 25.40%) | Calibrated to match Ilahi Table 3 overall 25.60% |
| MC access by income | Low 60% / Mid 80% / High 48% (weighted avg → 68.09%) | Calibrated to match Ilahi Table 3 overall 67.90% |

**Defense**: Ilahi's Table 3 directly reports vehicle access rates for the Greater Jakarta sample. These are "has access to" (not "owns"), which is the correct measure for mode choice — a person who lives in a household with a car has the car alternative available even if they don't personally own it. The income gradient (low-income: 5% car, 60% MC; mid-income: 26% car, 80% MC; high-income: 65% car, 48% MC) is calibrated so the population-weighted average matches Ilahi Table 3 overall rates (25.60% car, 67.90% MC) and the declining MC-with-income pattern (MC is an inferior good beyond middle-income). Cross-validated with Belgiawan et al. (2019) who survey Bodetabek-specific commuters.

### 3.3 Level-of-Service (LOS) matrix

| Mode | Time source | Cost source | PDF? |
|---|---|---|---|
| KRL | Schedule-based estimates (r5py CBD routing failed — documented) | GTFS fare table (KCI published) | GTFS feed |
| TJ (BRT) | Schedule-based | GTFS fare (flat Rp 3,500) | GTFS feed |
| RoyalTrans | Published schedule + MRT transfer where applicable | Published route fares (Rp 20–40k) | GTFS feed |
| LRT | Published timetable | Flat Rp 5,000 (Jabodebek LRT schedule) | GTFS feed |
| MRT | Published timetable | Distance-based Rp 3–14k (MRT Jakarta fare table) | Published fare schedule |
| Car | BPR function on road distance (25 km/h peak) | Pipeline `gc_car_idr` — fuel + toll from kelurahan data | Pipeline data |
| Motorcycle | 1.1× car time (32 km/h peak) | Pipeline `gc_motorcycle_idr` | Pipeline data |
| 4WRH | Car time + 7 min peak wait | Rp 3,500/km + Rp 1,500 booking (Gojek/Grab published tariff) | Published tariff schedule |
| 2WRH | Moto time + 5 min peak wait | Rp 2,000/km + Rp 1,000 booking (Gojek/Grab published tariff) | Published tariff schedule |

### 3.4 DGP parameters (synthetic approach)

Because no individual-level RP dataset exists, this project uses the **synthetic DGP framework** (same as the V-City course exercise): parameters are set from published literature, synthetic choice data is generated, then parameters are recovered via MLE to validate the estimator.

| Parameter group | Count | Source | PDF? |
|---|---|---|---|
| β_time (mode-specific) | 9 values | Derived from **Ilahi et al. (2021) Table 11** VTTS via β_time = β_cost × VTTS / 60,000 | Ilahi (2021) PDF ✓ |
| β_cost (generic) | 1 value | **Ilahi Table 10**: −1.42 per Thousand IDR (t = −12.08, p < 0.01) | Ilahi (2021) PDF ✓ |
| ASC (mode constants) | 8 values (KRL=0) | DGP-specified; ordinal preference informed by Ilahi's preference ordering + Bodetabek modal share | Ilahi (2021) PDF + Belgiawan (2019) PDF |
| ρ_OwnVehicle | 0.55 | **Bastarianto et al. (2019) Table 3**: λ_hwh = 0.55 (t = 6.01, p < 0.01) | Bastarianto (2019) PDF ✓ |
| ρ_Ridehailing | 0.70 | Derived — midpoint between 0.55 (strong) and 0.85 (near-MNL) | Sensitivity range ±0.10 |
| ρ_Transit | 0.75 | Bastarianto CNL cross-nest α values; weakest within-nest correlation | Bastarianto (2019) PDF ✓ |

### 3.5 What the synthetic approach means (and doesn't mean)

- **Synthetic choices**: 5,000 persons drawn from the DGP with zone-specific availability + Gumbel(0,1) noise. Used ONLY to validate the MLE estimator (notebooks 02–03).
- **Synthetic persons**: income segment and vehicle access drawn from Ilahi's sample distribution. These are NOT real individuals — they are draws from a literature-calibrated distribution. The purpose is pedagogic (demonstrate correct MLE implementation), not predictive.
- **LOS — NOT synthetic**: zone-to-CBD time and cost per mode are computed from real GTFS data, real pipeline costs, and published fare schedules. The LOS matrix is the data-driven layer.
- **Policy analysis (notebook 04)**: does NOT use the 5,000 synthetic individuals. It computes logsum welfare directly from zone×segment×mode LOS and estimated parameters — 21 rows, not 5,000.

### 3.6 Literature PDFs available for Q&A

| Paper | In `docs/literature/` | Used for |
|---|---|---|
| Ilahi et al. (2021). *Understanding travel mode choice...* TRA Part A 150, 398–422 | ✓ `2021_ilahi_understanding_travel.pdf` | β_cost, β_time (VTTS), ASC ordering, sample characteristics, vehicle access rates |
| Bastarianto et al. (2019). *Tour-based mode choice...* JSCE D3 75(5) | ✓ `2019_bastrianto_tour_based_mode_choice.pdf` | NL ρ_OwnVehicle = 0.55, CNL cross-nest validation for ρ_Transit |
| Belgiawan et al. (2019). *Influence of pricing on mode choice...* | ✓ `2019_belgiawan_influence_pricing_mode_choice.pdf` | Bodetabek-specific RP: ASC validation, income-segmented VOT |
| Binsuwadan & Wardman (2023). *Income elasticity of VoT...* | ✓ `2023_binsuwadan_income_elasticity.pdf` | Income elasticity η ≈ 0.5–0.7 for welfare extrapolation |
| World Bank (2023). *Meta-analysis of VTTS...* | ✓ `2023_world_bank_meta-analysis.pdf` | VTTS transfer methodology validation |
| Train (2009). *Discrete Choice Methods with Simulation* | Course textbook | ρ bounds, NL specification, dividing convention |

---

## Q4. Anticipated Obstacle

The main obstacle is justifying parameter transfer from Ilahi et al. (2021) — estimated on intra-Jakarta trips — to Bodetabek long-distance commuter corridors (30–60 km), where private-mode preference is stronger, transit access is sparser, and the cost-sensitivity context differs from the Jakarta intra-city sample mean at which Ilahi's β_cost is evaluated.

---

## Q5. Questions or Comments

No questions at this stage. I plan to present the full NL estimation and logsum welfare results in the report. The policy simulation will focus on transit-desert zones (J1b Kab. Bogor outer, J3b Gading Serpong) where the restricted choice set produces structurally lower consumer surplus before any policy intervention — this is the central equity finding.

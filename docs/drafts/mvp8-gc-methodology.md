# Three-Way Generalized Cost Model: Transit vs. Car vs. Motorcycle

**Ticket**: MVP-8 (E0-005)
**Status**: Draft
**Last updated**: 2026-03-19
**Feeds**: `docs/methodology.md` Layer 5, `docs/DATA_MODEL.md` Three-Way Cost Comparison, Paper Methods section

---

## 1. Rationale

Western transit equity frameworks compare transit against car as the sole private alternative. In Jabodetabek -- and across Southeast Asia broadly -- this framing misses the dominant modal competitor: the motorcycle. Indonesia has the third-largest motorcycle fleet globally, with over 125 million registered units (BPS, 2023). In Jabodetabek, motorcycles account for approximately 73% of registered motor vehicles and serve as the primary commuting mode for low-to-middle income households (Ng, 2018).

A transit equity analysis that ignores motorcycle competition produces misleading competitiveness scores. Transit may appear cost-competitive against car in suburban areas, but if motorcycle generalized cost is lower than transit, the practical mode choice for most households favors motorcycle -- undermining transit ridership and perpetuating auto-dependent commuting patterns.

This section specifies a three-way generalized cost (GC) model that computes the full monetized cost of a representative commute to the Sudirman-Thamrin CBD for each of three modes: transit, car, and motorcycle. The Transit Cost Ratio (TCR) derived from these costs becomes Layer 5 of the TAI composite index.

---

## 2. Generalized Cost Formulas

Generalized cost monetizes all components of a journey -- not just the out-of-pocket fare or fuel cost, but also the opportunity cost of time, the discomfort of transfers, and the physical toll of exposure to weather and traffic. The GC framework follows the standard transport economics formulation (Ortuzar & Willumsen, 2011) adapted for Jabodetabek's three-mode context.

### 2.1 Transit

```
GC_transit = fare_total
           + VOT x (access_time + wait_time + in_vehicle_time + transfer_walk_time + egress_time)
           + n_transfers x transfer_penalty
           + first_mile_cost
           + discomfort_penalty
```

| Component | Definition | Unit |
|-----------|-----------|------|
| `fare_total` | Cumulative fare across all transit legs (KRL + MRT + BRT etc.) | IDR |
| `VOT` | Value of time (see Section 3.1) | IDR/min |
| `access_time` | Walking or feeder ride time from origin to first transit stop | min |
| `wait_time` | Time waiting for the first vehicle (half-headway assumption) + waiting at transfer points | min |
| `in_vehicle_time` | Time spent aboard transit vehicles across all legs | min |
| `transfer_walk_time` | Walking time between platforms/stops during transfers | min |
| `egress_time` | Walking time from final transit stop to destination | min |
| `n_transfers` | Number of vehicle-to-vehicle transfers | count |
| `transfer_penalty` | Monetized disutility per transfer (captures uncertainty, physical effort, missed-connection risk) | IDR |
| `first_mile_cost` | Out-of-pocket cost if using ojol/angkot for first-mile access (Rp 0 if walking) | IDR |
| `discomfort_penalty` | Monetized penalty for crowding, standing, weather exposure at stops | IDR |

**Transit fare structure** (2024/2025 tariffs):

| Mode | Fare Structure | Range |
|------|---------------|-------|
| KRL Commuterline | Distance-based: Rp 3,000 base + Rp 1,000/station | Rp 3,000 -- Rp 13,000 |
| MRT Jakarta | Distance-based: Rp 3,000 base + distance increments | Rp 3,000 -- Rp 14,000 |
| TransJakarta BRT (regular) | Flat fare | Rp 3,500 |
| TransJakarta Mikrotrans | Flat fare (integrated with BRT) | Rp 0 (free transfer) -- Rp 3,500 |
| TransJakarta Royaltrans | Flat fare (premium express) | Rp 20,000 |
| LRT Jabodebek | Distance-based | Rp 5,000 -- Rp 20,000 |

**JakLingko integration note**: With JakLingko card, inter-modal transfers within the integrated system (BRT to KRL, BRT to MRT) may receive fare discounts. The model uses full individual fares as the default (conservative estimate), with JakLingko-discounted fares as a sensitivity scenario.

**Discomfort penalty specification**:

| Condition | Penalty | Justification |
|-----------|---------|---------------|
| Peak-hour crowding (standing, load factor > 100%) | Rp 3,000 | Sukor & Bhayo (2024) identify crowding as a deterrent to transit use; monetized as ~6 min equivalent VOT |
| Weather exposure at open stops (no shelter) | Rp 2,000 | Relevant for TransJakarta halte without adequate shelter; monsoon season amplifies |
| No discomfort (off-peak, seated, sheltered) | Rp 0 | Baseline |

Default model uses Rp 3,000 for peak-hour commutes (the primary analysis scenario). Sensitivity analysis tests Rp 0 (optimistic) and Rp 5,000 (high-discomfort).

### 2.2 Car

```
GC_car = fuel_cost
       + toll_cost
       + parking_cost
       + VOT x travel_time
       + fatigue_factor
```

| Component | Definition | Derivation |
|-----------|-----------|------------|
| `fuel_cost` | Distance x fuel consumption rate x fuel price | `distance_km x (1/12) x 13,000` = Rp 1,083/km |
| `toll_cost` | Sum of toll segments used on optimal route | Route-specific (see Section 3.4) |
| `parking_cost` | Parking fee at destination | Zone-specific (see Section 3.5) |
| `VOT x travel_time` | Opportunity cost of time in car | `VOT x travel_time_min` |
| `fatigue_factor` | Physical/mental toll of driving | Rp 0 (car is climate-controlled, seated) |

**Fuel cost derivation for car**:
- Average fuel consumption for urban sedan/MPV in Jakarta traffic: **12 km/L** (consistent with ESDM data for Euro-4 compliant vehicles in urban stop-and-go conditions)
- Fuel price (Pertalite, subsidized): **Rp 10,000/L** (as of 2024; Pertamina official tariff)
- Effective cost: **Rp 833/km**
- Alternative: Pertamax (RON 92): **Rp 13,000/L** -> Rp 1,083/km
- **Model default: Rp 1,000/km** (rounded, between Pertalite and Pertamax, reflecting mixed usage)

**Fatigue factor for car**: Set to Rp 0. Car travel in Jabodetabek, while slow in congestion, is physically comfortable (air conditioning, seated, enclosed). The time cost already captures the congestion penalty through travel_time.

### 2.3 Motorcycle

```
GC_motorcycle = fuel_cost
              + parking_cost
              + VOT x travel_time
              + fatigue_factor
```

**Critical: NO toll component.** Motorcycles are legally prohibited from toll roads in Indonesia (Peraturan Pemerintah No. 15/2005 on Toll Roads, as amended). This has two consequences:
1. Motorcycles pay zero toll fees (direct cost advantage).
2. Motorcycles must use surface roads (arteri/collector/local), which are slower on suburban routes where toll roads provide a faster car alternative.

| Component | Definition | Derivation |
|-----------|-----------|------------|
| `fuel_cost` | Distance x fuel consumption rate x fuel price | `distance_km x (1/50) x 10,000` = Rp 200/km |
| `parking_cost` | Parking fee at destination | Zone-specific, lower than car (see Section 3.5) |
| `VOT x travel_time` | Opportunity cost of time on motorcycle | `VOT x travel_time_min` |
| `fatigue_factor` | Physical toll of riding in Jakarta traffic conditions | Distance/time-dependent (see below) |

**Fuel cost derivation for motorcycle**:
- Average fuel consumption for 110-125cc scooter (Honda Beat, Vario, Yamaha NMAX -- dominant fleet): **50 km/L** (manufacturer spec under mixed urban conditions; real-world Jakarta ~45-55 km/L)
- Fuel price (Pertalite): **Rp 10,000/L**
- Effective cost: **Rp 200/km**
- This is **5x cheaper per km than car** -- a fundamental structural advantage

**Fatigue factor specification**:

The fatigue factor captures the physical disutility of motorcycle riding that time-cost alone does not monetize: heat exposure (Jakarta average 32 deg C, humidity > 80%), rain during monsoon (November-March), air pollution from proximity to exhaust, and physical strain from maneuvering through traffic.

| Ride Duration | Fatigue Factor | Justification |
|---------------|---------------|---------------|
| < 20 min | Rp 0 | Short rides are tolerable; consistent with revealed preference data showing motorcycles dominant for short trips (Ng, 2018) |
| 20 -- 40 min | Rp 5,000 | Moderate exposure; discomfort noticeable but manageable |
| 40 -- 60 min | Rp 10,000 | Significant discomfort; heat/rain exposure becomes a deterrent. Sukor & Bhayo (2024) find that ride duration > 30 min significantly increases stated willingness to switch to transit |
| > 60 min | Rp 15,000 | Extreme discomfort; safety risk increases with fatigue. Few commuters willingly ride > 60 min daily |

The fatigue factor creates a distance-dependent inflection point: motorcycles are unambiguously superior for short trips (low fuel cost, zero toll, fast in traffic) but become increasingly uncompetitive for long suburban commutes where rider fatigue accumulates.

---

## 3. Cost Parameters

### 3.1 Value of Time (VOT)

VOT converts travel time into monetary terms, enabling direct comparison across modes. Jakarta-specific VOT estimates are scarce in the peer-reviewed literature; we derive our parameter from multiple sources.

**Primary source**: The Jakarta UMR (Upah Minimum Regional) for 2024 is Rp 5,067,381/month. Assuming 22 working days and 8 hours per day:

```
VOT_umr = 5,067,381 / (22 x 8 x 60) = Rp 479/min ~ Rp 500/min (rounded)
```

This yields **Rp 30,000/hour**, which we adopt as the base VOT.

**Cross-validation with literature**:
- Ng (2018) reports VOT estimates for Jakarta commuters in the range of USD 1.5-3.0/hour for middle-income groups. At 2024 exchange rates (~Rp 15,500/USD), this translates to Rp 23,250-46,500/hour. Our Rp 30,000/hr falls within this range.
- Sukor & Bhayo (2024) note that VOT in SE Asian developing cities is typically 30-50% of hourly wage for commuting trips, consistent with international transport economics norms (Wardman et al., 2016). At 50% of UMR hourly wage: Rp 29,000/hr, closely matching our estimate.
- JICA SITRAMP II (2019) survey data for Jabodetabek commuters implies VOT of approximately Rp 25,000-35,000/hr for transit users and Rp 35,000-50,000/hr for car users.

**Income differentiation** (sensitivity analysis, not base model):

| Income Group | Monthly Income Proxy | VOT | Justification |
|-------------|---------------------|-----|---------------|
| Low income | < Rp 3.5M | Rp 350/min (Rp 21,000/hr) | Below UMR; time less monetized but transit-dependent |
| Middle income (base) | Rp 3.5M -- 8M | Rp 500/min (Rp 30,000/hr) | UMR-derived; majority of commuters |
| Upper-middle income | > Rp 8M | Rp 800/min (Rp 48,000/hr) | Higher opportunity cost; car-oriented |

The base model uses a single VOT of Rp 500/min for all spatial units. Income-differentiated VOT is reserved for sensitivity analysis because the spatial unit (kelurahan/H3 cell) contains a mix of income groups, and assigning a single income-differentiated VOT per cell would conflate spatial and individual variation. The income-differentiated scenario tests whether equity conclusions change when VOT varies by local income level (using `avg_household_expenditure` as proxy).

### 3.2 Fuel Cost Per Kilometer

| Mode | Fuel Efficiency | Fuel Price | Cost/km | Source |
|------|----------------|-----------|---------|--------|
| Car (sedan/MPV) | 12 km/L | Rp 10,000/L (Pertalite) | **Rp 833/km** | ESDM fuel efficiency data; Pertamina 2024 tariff |
| Car (default model) | -- | Mixed Pertalite/Pertamax | **Rp 1,000/km** (rounded) | Conservative estimate |
| Motorcycle (110-125cc) | 50 km/L | Rp 10,000/L (Pertalite) | **Rp 200/km** | Manufacturer spec; dominant Honda Beat/Vario fleet |

The 5:1 fuel cost ratio (car:motorcycle) is a structural feature of Indonesia's transport economics and a primary driver of motorcycle dominance for middle-income households.

### 3.3 Transit Fares

Transit fares are route-specific and computed from the r5py optimal path to Sudirman-Thamrin CBD. The fare estimation is performed post-hoc from the routing output:

```
For the r5py optimal path to Sudirman-Thamrin:
1. Identify each leg by transit mode
2. Sum fares per leg:
   - KRL leg: Rp 3,000 + (n_stations x Rp 1,000), cap Rp 13,000
   - MRT leg: Rp 3,000 + distance-based increment, cap Rp 14,000
   - TransJakarta leg: Rp 3,500 (flat)
   - LRT leg: Rp 5,000 + distance-based increment, cap Rp 20,000
3. Cumulative fare = sum of all leg fares
```

**Typical fare ranges by origin distance**:

| Origin Distance | Typical Route | Estimated Fare |
|----------------|--------------|----------------|
| 5 km (inner Jakarta) | Single BRT leg | Rp 3,500 |
| 15 km (mid-ring) | KRL + BRT transfer | Rp 6,500 -- 10,000 |
| 30 km (suburban) | KRL + BRT or KRL + MRT | Rp 8,500 -- 17,000 |
| 40+ km (outer Bodetabek) | KRL long haul + transfer | Rp 13,000 -- 17,500 |

### 3.4 Toll Rates

Jakarta toll road tariffs (Golongan I -- sedan/MPV, 2024 rates):

| Toll Road | Section | Distance | Toll (Car) | Toll (Motorcycle) |
|-----------|---------|----------|-----------|-------------------|
| Jakarta-Tangerang (Sedyatmo) | Tangerang -- Tomang | ~28 km | Rp 16,500 | **N/A** |
| BSD -- Jakarta (Serpong-Pd Aren) | BSD -- Pd Aren | ~10 km | Rp 8,000 | **N/A** |
| JORR (Outer Ring) | Varies by section | Varies | Rp 12,000 -- 18,000 | **N/A** |
| Jakarta-Cikampek | Bekasi Timur -- Cawang | ~30 km | Rp 19,000 | **N/A** |
| Jakarta-Cikampek Elevated | Bekasi -- Cikunir | ~36 km | Rp 22,000 -- 35,000 | **N/A** |
| Jakarta-Bogor (Jagorawi) | Bogor -- Cawang | ~46 km | Rp 14,500 | **N/A** |
| Depok-Antasari (DESARI) | Depok -- Antasari | ~21 km | Rp 18,000 | **N/A** |
| Inner-city toll (Cawang-Priok etc.) | Various | Short | Rp 7,500 -- 12,000 | **N/A** |

**N/A for motorcycle** in all cases: Per PP No. 15/2005, motorcycles (Golongan V in the old classification, now simply excluded) are prohibited from all toll roads in Indonesia. This is not a cost difference -- it is a complete exclusion.

**Model implementation**: For each spatial unit, the toll cost is assigned based on the most likely toll route to Sudirman-Thamrin. Spatial units within inner Jakarta (no toll needed) receive toll_cost = Rp 0 for car. Spatial units in suburban corridors receive the applicable toll per the table above.

### 3.5 Parking Costs

| Zone | Car Parking | Motorcycle Parking | Source |
|------|------------|-------------------|--------|
| **CBD (Sudirman-Thamrin, Kuningan)** | Rp 25,000 -- 40,000/day | Rp 5,000 -- 10,000/day | Jakarta CBD office building rates (2024 survey) |
| **Secondary CBD (TB Simatupang, Gatot Subroto)** | Rp 15,000 -- 25,000/day | Rp 5,000 -- 8,000/day | Lower density, more surface parking |
| **Suburban commercial (BSD, Bekasi)** | Rp 5,000 -- 10,000/day | Rp 2,000 -- 5,000/day | Mall/office rates |

**Model defaults** (commute to Sudirman-Thamrin):
- Car: **Rp 25,000** (mid-range CBD building rate, assuming employer does not subsidize)
- Motorcycle: **Rp 8,000** (typical motorcycle bay or street parking near CBD)

Parking cost is a significant component of car GC that has no equivalent in transit. The 3:1 ratio between car and motorcycle parking further advantages motorcycle mode choice.

### 3.6 Transfer Penalty and First-Mile Cost

**Transfer penalty**: Rp 5,000 per transfer

This monetizes the disutility of each vehicle change: walking between platforms (3-8 min), uncertainty about the next vehicle's arrival, physical effort (stairs, overpasses, weather exposure between stops), and the psychological cost of a potential missed connection. At VOT = Rp 500/min, Rp 5,000 is equivalent to 10 minutes of travel time -- consistent with international transfer penalty estimates of 5-15 min equivalent (Currie, 2005; Wardman, 2004) and calibrated for Jabodetabek's relatively poor interchange infrastructure.

**First-mile cost**: Two modes, take the lesser generalized cost:

| First-Mile Mode | Out-of-Pocket | Time | Generalized Cost |
|-----------------|--------------|------|-----------------|
| Walking | Rp 0 | walk_time_min x VOT | walk_time_min x 500 |
| Ojol (Grab/Gojek) | Base Rp 10,000 -- 15,000 (distance-dependent) | 5-10 min | fare + (time x 500) |

For spatial units within 1 km walk of a transit stop (~12 min walk), walking is cheaper (GC = Rp 6,000) than ojol (GC = Rp 12,000+). For spatial units > 1.5 km from a transit stop, ojol becomes cost-effective despite the fare because walk time (> 18 min) generates VOT > Rp 9,000.

**This parameter is critical**: Sukor & Bhayo (2024) identify first-mile quality as the strongest predictor of motorcycle-to-transit modal shift. Areas with poor first-mile access effectively add Rp 10,000-15,000 to transit GC, pushing it above motorcycle GC and into the "private wins" zone.

---

## 4. Transit Cost Ratio (TCR)

### 4.1 Definition

The Transit Cost Ratio expresses transit's cost competitiveness as a ratio against each private mode and their combined minimum:

```
TCR_vs_car       = GC_car / GC_transit
TCR_vs_motorcycle = GC_motorcycle / GC_transit
TCR_combined     = min(GC_car, GC_motorcycle) / GC_transit
```

**Interpretation**: TCR_combined > 1.0 means the cheapest private alternative is more expensive than transit (transit is competitive). TCR_combined < 1.0 means at least one private mode is cheaper than transit (transit loses).

Note: TCR is defined as private/transit (not transit/private) so that higher values = transit more competitive. This orientation ensures that `L5 = norm(clamp(TCR_combined, 0.3, 2.0))` produces higher TAI scores for areas where transit wins.

### 4.2 Threshold Classification

| TCR_combined Range | Classification | Label | Interpretation |
|-------------------|---------------|-------|----------------|
| > 1.2 | Transit clearly wins | `transit_wins` | Both private modes are > 20% more expensive than transit |
| 0.8 -- 1.2 | Swing zone | `swing` | Marginal difference; first-mile quality, comfort, and habit determine mode choice |
| 0.5 -- 0.8 | Private transport wins | `private_wins` | At least one private mode is 20-50% cheaper than transit |
| < 0.5 | Private strongly dominates | `private_wins` | At least one private mode is < half the cost of transit |

**Threshold justification**:
- The 0.8/1.2 swing zone boundaries derive from the transport mode choice literature, where a 20% cost differential is commonly cited as the threshold below which non-cost factors (convenience, habit, comfort) dominate mode choice (Ortuzar & Willumsen, 2011).
- The swing zone is where policy interventions (improved first-mile, fare subsidies, frequency increases) have the highest marginal impact on mode shift -- making these areas the priority targets for transit investment from an equity perspective.
- Sukor & Bhayo (2024) find that respondents in their SE Asian sample exhibit modal inertia within approximately +/- 15-25% of cost parity, supporting the 0.8-1.2 band.

### 4.3 Distance-Dependent Competitive Dynamics

The three-way competition has a systematic spatial pattern driven by distance from CBD:

| Distance Band | Typical TCR_combined | Why | Dominant Private Competitor |
|---------------|---------------------|-----|-----------------------------|
| **0 -- 8 km** (inner Jakarta) | 0.6 -- 0.9 | Short distance = cheap private fuel, no toll, fast door-to-door. Transit overhead (walk + wait + ride) cannot compete on short trips | Motorcycle |
| **8 -- 15 km** (mid-ring) | 0.8 -- 1.2 | Convergence zone. Congestion equalizes car time; motorcycle still fast but fatigue starts. Transit competitive if good first-mile | Motorcycle (shifting) |
| **15 -- 25 km** (inner suburban) | 1.0 -- 1.5 | Toll costs push car GC up; motorcycle ride > 40 min triggers fatigue premium. Transit (KRL/MRT) becomes time- and cost-efficient | Car (toll corridor), Motorcycle (non-toll) |
| **25 -- 40+ km** (outer suburban) | 1.2 -- 2.0+ | High toll + fuel for car; extreme fatigue for motorcycle (60+ min). Transit strongly wins IF accessible | Car |

This distance-dependent pattern produces a characteristic spatial gradient on the map: inner Jakarta cells show `private_wins` (red), mid-ring shows `swing` (yellow), and outer suburban shows `transit_wins` (green) -- but only along corridors with actual transit service. Outer suburban cells with no transit access have no valid GC_transit and are excluded from TCR calculation (flagged as `transit_not_available`).

---

## 5. Worked Examples

### 5.1 BSD (Bumi Serpong Damai) -- Suburban, 30 km to Sudirman

**Profile**: Outer suburban new town in South Tangerang. Served by KRL Serpong line (Rawa Buntu/Serpong stations). Toll road available (BSD - Pondok Aren - JORR - Semanggi corridor). Moderate first-mile challenge: KRL stations are 2-4 km from many residential clusters.

#### Transit

| Component | Value | Calculation |
|-----------|-------|-------------|
| First-mile access | Ojol to KRL Rawa Buntu: Rp 12,000 fare, 15 min | First-mile mode: ojol (> 2 km to station) |
| Wait time | 7 min | KRL headway ~15 min; half-headway assumption |
| KRL fare | Rp 5,000 | Rawa Buntu to Tanah Abang (~12 stations) |
| KRL in-vehicle time | 45 min | Serpong line to Tanah Abang (schedule) |
| Transfer walk | 8 min | Tanah Abang KRL to TransJakarta halte |
| TransJakarta fare | Rp 3,500 | Flat fare |
| TransJakarta wait | 5 min | Corridor 1 headway ~10 min |
| TransJakarta ride | 10 min | Tanah Abang to Sudirman corridor |
| Discomfort penalty | Rp 3,000 | Peak-hour crowding on KRL |
| **Total fare** | **Rp 20,500** | 12,000 + 5,000 + 3,500 |
| **Total time** | **90 min** | 15 + 7 + 45 + 8 + 5 + 10 |
| **Time cost** | **Rp 45,000** | 90 x 500 |
| **Transfer penalty** | **Rp 5,000** | 1 transfer (KRL to BRT) |
| **GC_transit** | **Rp 73,500** | 20,500 + 45,000 + 5,000 + 3,000 |

#### Car

| Component | Value | Calculation |
|-----------|-------|-------------|
| Fuel | Rp 30,000 | 30 km x Rp 1,000/km |
| Toll | Rp 35,000 | BSD toll (Rp 8,000) + JORR (Rp 12,000) + inner toll (Rp 15,000) |
| Parking | Rp 25,000 | CBD building rate |
| Travel time | 75 min | Toll + congestion (AM peak) |
| Time cost | Rp 37,500 | 75 x 500 |
| Fatigue | Rp 0 | Car comfort |
| **GC_car** | **Rp 127,500** | 30,000 + 35,000 + 25,000 + 37,500 |

#### Motorcycle

| Component | Value | Calculation |
|-----------|-------|-------------|
| Fuel | Rp 6,000 | 30 km x Rp 200/km |
| Toll | Rp 0 | Motorcycles excluded from toll roads |
| Parking | Rp 8,000 | Motorcycle CBD rate |
| Travel time | 80 min | Surface roads only (no toll shortcut), moderate congestion |
| Time cost | Rp 40,000 | 80 x 500 |
| Fatigue | Rp 10,000 | 80 min > 40 min threshold |
| **GC_motorcycle** | **Rp 64,000** | 6,000 + 0 + 8,000 + 40,000 + 10,000 |

#### TCR Calculation

```
TCR_vs_car       = 127,500 / 73,500 = 1.73  (transit strongly beats car)
TCR_vs_motorcycle = 64,000 / 73,500  = 0.87  (motorcycle slightly beats transit)
TCR_combined     = min(127,500, 64,000) / 73,500 = 64,000 / 73,500 = 0.87

Classification: SWING ZONE (0.8 -- 1.2)
Cheapest private mode: motorcycle
```

**Interpretation**: Transit and motorcycle are close competitors for the BSD-Sudirman commute. Car is prohibitively expensive (Rp 127.5k vs Rp 73.5k transit). The motorcycle's structural advantage -- zero toll, cheap fuel -- is partially offset by the 80-minute surface road ride and Rp 10k fatigue premium.

**Key insight**: The first-mile ojol cost (Rp 12,000) is the swing factor. If BSD had feeder bus service or better pedestrian access to KRL Rawa Buntu, transit GC drops to ~Rp 61,500 (replacing Rp 12k ojol + 15 min with Rp 0 walk + 12 min), pushing TCR_combined to 64,000/61,500 = 1.04 -- firmly in the swing zone favoring transit. This validates Sukor & Bhayo's (2024) finding that first-mile quality is the strongest predictor of motorcycle-to-transit mode shift.

### 5.2 Ciputat -- Peri-Urban, 18 km to Sudirman

**Profile**: Established peri-urban area in South Tangerang. No direct rail service (KRL Serpong line is 5+ km west). TransJakarta feeder services available but infrequent. No toll road shortcut (must use arterial Jl. Raya Ciputat or JORR via detour). Mix of middle-income kampung and newer developments.

#### Transit

| Component | Value | Calculation |
|-----------|-------|-------------|
| First-mile access | Walk to TransJakarta feeder: Rp 0 fare, 12 min | Walk (station within 1 km) |
| Wait time | 10 min | Feeder headway ~20 min; half-headway |
| TransJakarta feeder ride | 25 min | Feeder to Lebak Bulus |
| Transfer walk | 5 min | Lebak Bulus feeder to MRT |
| MRT fare | Rp 10,000 | Lebak Bulus to Bundungan Hilir (distance-based) |
| MRT wait | 5 min | MRT headway ~10 min |
| MRT ride | 20 min | Lebak Bulus to Bundungan Hilir / Sudirman |
| Egress | 8 min | Walk from MRT station to destination |
| TransJakarta fare | Rp 3,500 | Feeder fare |
| Discomfort penalty | Rp 2,000 | Moderate crowding, feeder standing |
| **Total fare** | **Rp 13,500** | 3,500 + 10,000 |
| **Total time** | **85 min** | 12 + 10 + 25 + 5 + 5 + 20 + 8 |
| **Time cost** | **Rp 42,500** | 85 x 500 |
| **Transfer penalty** | **Rp 5,000** | 1 transfer (feeder to MRT) |
| **GC_transit** | **Rp 63,000** | 13,500 + 42,500 + 5,000 + 2,000 |

#### Car

| Component | Value | Calculation |
|-----------|-------|-------------|
| Fuel | Rp 18,000 | 18 km x Rp 1,000/km |
| Toll | Rp 18,000 | JORR section (Pd Aren -- Cilandak) + inner toll |
| Parking | Rp 25,000 | CBD rate |
| Travel time | 55 min | Mixed arterial + JORR, heavy peak congestion |
| Time cost | Rp 27,500 | 55 x 500 |
| Fatigue | Rp 0 | |
| **GC_car** | **Rp 88,500** | 18,000 + 18,000 + 25,000 + 27,500 |

#### Motorcycle

| Component | Value | Calculation |
|-----------|-------|-------------|
| Fuel | Rp 3,600 | 18 km x Rp 200/km |
| Toll | Rp 0 | Excluded |
| Parking | Rp 8,000 | Motorcycle CBD rate |
| Travel time | 50 min | Surface arterial (Jl. Ciputat Raya), motorcycle can filter through traffic |
| Time cost | Rp 25,000 | 50 x 500 |
| Fatigue | Rp 5,000 | 50 min ride; 20-40 min tier |
| **GC_motorcycle** | **Rp 41,600** | 3,600 + 0 + 8,000 + 25,000 + 5,000 |

#### TCR Calculation

```
TCR_vs_car       = 88,500 / 63,000 = 1.40  (transit beats car)
TCR_vs_motorcycle = 41,600 / 63,000 = 0.66  (motorcycle clearly beats transit)
TCR_combined     = 41,600 / 63,000 = 0.66

Classification: PRIVATE WINS (< 0.8)
Cheapest private mode: motorcycle
```

**Interpretation**: Ciputat demonstrates the worst case for transit competitiveness in the mid-ring. Despite having MRT access via feeder, the long feeder ride (25 min) plus transfer overhead inflates transit time to 85 min. Motorcycle riders cover the same 18 km in 50 min at a fraction of the cost (Rp 41.6k vs Rp 63k). The TCR of 0.66 means motorcycle is ~34% cheaper than transit in generalized cost terms.

**Key insight**: Ciputat's problem is not fare (transit fare Rp 13.5k is reasonable) but time. The feeder-to-MRT journey chain adds 52 min of non-in-vehicle time (walk + wait + transfer + wait + egress). This is the "missing middle" problem: areas close enough that motorcycle is fast, but far enough that transit requires multi-leg chains. Without a direct high-frequency connection (e.g., dedicated BRT corridor on Jl. Ciputat Raya), motorcycle dominance is entrenched.

### 5.3 Tebet -- Inner Jakarta, 5 km to Sudirman

**Profile**: Inner-city Jakarta neighborhood. Excellent transit access: TransJakarta Corridor 6 (Ragunan-Dukuh Atas) runs through the area, MRT Fatmawati line accessible via short ride, KRL Manggarai nearby. Dense road network with moderate pedestrian infrastructure.

#### Transit

| Component | Value | Calculation |
|-----------|-------|-------------|
| First-mile access | Walk to TransJakarta halte: Rp 0, 10 min | Walk (halte within 800m) |
| Wait time | 5 min | BRT headway ~10 min, half-headway |
| TransJakarta fare | Rp 3,500 | Flat fare |
| TransJakarta ride | 15 min | Corridor 6 to Sudirman area |
| Egress | 5 min | Walk from halte |
| Discomfort penalty | Rp 3,000 | Peak crowding on Corridor 6 |
| **Total fare** | **Rp 3,500** | |
| **Total time** | **35 min** | 10 + 5 + 15 + 5 |
| **Time cost** | **Rp 17,500** | 35 x 500 |
| **Transfer penalty** | **Rp 0** | No transfer |
| **GC_transit** | **Rp 24,000** | 3,500 + 17,500 + 0 + 3,000 |

#### Car

| Component | Value | Calculation |
|-----------|-------|-------------|
| Fuel | Rp 5,000 | 5 km x Rp 1,000/km |
| Toll | Rp 0 | No toll needed for inner-city trip |
| Parking | Rp 25,000 | CBD building rate |
| Travel time | 20 min | Urban congestion, short distance |
| Time cost | Rp 10,000 | 20 x 500 |
| Fatigue | Rp 0 | |
| **GC_car** | **Rp 40,000** | 5,000 + 0 + 25,000 + 10,000 |

#### Motorcycle

| Component | Value | Calculation |
|-----------|-------|-------------|
| Fuel | Rp 1,000 | 5 km x Rp 200/km |
| Toll | Rp 0 | Excluded (and irrelevant -- no toll needed) |
| Parking | Rp 8,000 | Motorcycle CBD rate |
| Travel time | 15 min | Short distance, motorcycle filters through congestion |
| Time cost | Rp 7,500 | 15 x 500 |
| Fatigue | Rp 0 | < 20 min ride |
| **GC_motorcycle** | **Rp 16,500** | 1,000 + 0 + 8,000 + 7,500 + 0 |

#### TCR Calculation

```
TCR_vs_car       = 40,000 / 24,000 = 1.67  (transit beats car)
TCR_vs_motorcycle = 16,500 / 24,000 = 0.69  (motorcycle clearly beats transit)
TCR_combined     = 16,500 / 24,000 = 0.69

Classification: PRIVATE WINS (< 0.8)
Cheapest private mode: motorcycle
```

**Interpretation**: Even with excellent transit service (direct BRT, no transfers, Rp 3,500 fare), Tebet shows motorcycle dominance for short-distance CBD commutes. The motorcycle's GC is 31% lower than transit. The culprit is pure time cost: the 20-minute time differential (35 min transit vs 15 min motorcycle) translates to Rp 10,000 in VOT -- more than erasing transit's Rp 2,500 fare advantage (Rp 3,500 vs Rp 1,000 fuel).

**Key insight**: For inner-Jakarta spatial units, transit cannot compete with motorcycle on generalized cost for CBD commutes unless (a) motorcycle parking is eliminated/priced higher, (b) dedicated bus lanes reduce BRT travel time below 20 min, or (c) motorcycle fatigue is not applicable (already zero for short trips). This is consistent with Ng (2018): motorcycle dominance is strongest for short urban trips where its speed and cost advantages are maximal.

---

## 6. Motorcycle Toll Exclusion: Structural Implications

### 6.1 The Regulatory Context

Indonesian Government Regulation (PP No. 15/2005 on Toll Roads, as subsequently amended by PP No. 30/2017) explicitly excludes motorcycles from toll road access. This regulation applies to all toll roads nationwide, including all Jabodetabek toll corridors: Jakarta-Tangerang, Jakarta-Cikampek, Jagorawi, JORR, DESARI, and the Jakarta-Cikampek Elevated toll road.

### 6.2 Dual Impact on Generalized Cost

The toll exclusion affects motorcycle GC through two opposing channels:

**Channel 1 -- Direct cost advantage**: Motorcycles save Rp 8,000-35,000 per trip in toll fees. For suburban commuters using long toll corridors (e.g., BSD-Jakarta: Rp 35,000 toll, Bekasi-Jakarta: Rp 19,000-35,000), this is a substantial absolute savings.

**Channel 2 -- Indirect time penalty**: Motorcycles are forced onto surface arterials and collector roads, which are slower due to traffic signals, intersections, market activity, and mixed traffic. On routes where toll roads save 20-30 min of car travel time, motorcycle surface-road travel can be 15-30 min longer than the toll alternative.

**Net effect by distance**:

| Distance | Toll Savings | Time Penalty (extra min on surface road) | Time Cost of Penalty | Net Benefit to Motorcycle |
|----------|-------------|------------------------------------------|---------------------|---------------------------|
| 5 km | Rp 0 (no toll relevant) | 0 min | Rp 0 | Neutral |
| 15 km | Rp 12,000-18,000 | 5-10 min | Rp 2,500-5,000 | **Rp 7,000-15,500 advantage** |
| 30 km | Rp 25,000-35,000 | 15-25 min | Rp 7,500-12,500 | **Rp 12,500-27,500 advantage** |
| 40+ km | Rp 30,000-40,000 | 25-40 min | Rp 12,500-20,000 | **Rp 10,000-27,500 advantage** |

**Conclusion**: The toll exclusion is a net advantage for motorcycles at all suburban distances, because toll savings consistently exceed the time cost of the surface road detour. However, the advantage peaks at 15-30 km and begins to narrow beyond 40 km as surface road travel time becomes extremely long (80-100+ min), triggering higher fatigue premiums.

### 6.3 Corridor-Specific Analysis

The toll exclusion creates heterogeneous competitive dynamics across Jabodetabek corridors:

| Corridor | Toll Road | Effect of Motorcycle Toll Exclusion |
|----------|----------|-------------------------------------|
| **Tangerang (west)** | Jakarta-Tangerang toll | Car saves 20+ min via toll, but pays Rp 16,500. Motorcycle uses Jl. Daan Mogot (very congested). Motorcycle still competitive due to lane filtering. |
| **BSD/Serpong (southwest)** | BSD-JORR-Semanggi | Heavy toll dependency for car (Rp 35,000). Motorcycle on Jl. Raya Serpong / Jl. Ciputat is slower but saves the entire toll. Strong motorcycle advantage at 15-25 km. |
| **Depok (south)** | Jagorawi / DESARI | Jagorawi toll saves significant time for car. Motorcycle uses Jl. Margonda / Jl. Raya Bogor -- highly congested but motorcycle filters through. |
| **Bekasi (east)** | Jakarta-Cikampek / Elevated | Longest toll corridor. Car saves 30+ min. Motorcycle on Jl. Raya Bekasi is extremely congested. This is the corridor where toll exclusion most penalizes motorcycles in time -- but cost savings still dominate for distances < 35 km. |
| **Bogor (far south)** | Jagorawi | 46 km toll corridor. Surface road alternative (Jl. Raya Bogor) is heavily congested. At 60+ km, motorcycle GC approaches or exceeds transit GC due to extreme fatigue premium (Rp 15,000 for > 60 min ride). |

### 6.4 Implication for Transit Equity

The toll exclusion creates a structural "motorcycle cost floor" that transit must beat to be competitive. Because motorcycles pay zero toll regardless of distance, they maintain a low GC baseline across all corridors. This means:

1. **Transit is never the cheapest mode for short trips** (< 10 km) -- motorcycle's zero toll + cheap fuel + speed advantage is insurmountable.
2. **Transit becomes competitive in the 15-30 km band** only when it offers high-quality first-mile access and direct/low-transfer routes.
3. **For very long commutes (40+ km), transit wins strongly** -- but only if the commuter has physical access to rail. Motorcycle fatigue for 90+ min rides is severe.

This spatial pattern implies that transit equity interventions should focus on the 15-30 km band (inner suburban ring) where TCR is in the swing zone and where first-mile improvements can tip mode choice from motorcycle to transit.

---

## 7. Integration with TAI Layer 5

### 7.1 Layer 5 Formula

```
L5_cost_competitiveness = norm(clamp(TCR_combined, 0.3, 2.0))
```

Where:
- `TCR_combined = min(GC_car, GC_motorcycle) / GC_transit`
- `clamp(x, 0.3, 2.0)` bounds the ratio to avoid extreme outliers distorting normalization
- `norm()` applies min-max normalization across all spatial units

**Interpretation**:
- L5 = 1.0 for spatial units where `TCR_combined >= 2.0` (transit is half the cost of the cheapest private mode)
- L5 = 0.0 for spatial units where `TCR_combined <= 0.3` (private mode is ~3x cheaper than transit)
- L5 = 0.5 approximately at `TCR_combined = 1.15` (transit marginally competitive)

### 7.2 Weight in TAI Composite

Layer 5 receives **15% weight** in the TAI composite:

```
TAI = 0.20 x L1 + 0.15 x L2 + 0.35 x L3 + 0.15 x L4 + 0.15 x L5
```

The 15% weight reflects that cost competitiveness is important but secondary to actual accessibility (can you physically reach the CBD by transit at all? -- captured in L1 + L3 + L4 at 70% combined). Cost competitiveness matters most at the margin: for spatial units in the swing zone, L5 determines whether the TAI score reflects a functionally useful transit option or a technically available but practically uncompetitive one.

### 7.3 Spatial Units Without Transit

For spatial units where no transit service exists (no stops within walking distance, no r5py path found), GC_transit is undefined. These units receive:
- `gc_transit_idr = null`
- `tcr_combined = null`
- `transit_competitive_zone = "transit_not_available"`
- `L5 = 0.0` (worst possible cost competitiveness -- transit cannot compete if it does not exist)

---

## 8. Sensitivity Analysis Parameters

The GC model contains several assumed parameters. Sensitivity analysis tests the robustness of TCR classifications to parameter variation:

| Parameter | Base Value | Low Scenario | High Scenario | Rationale |
|-----------|-----------|-------------|---------------|-----------|
| VOT | Rp 500/min | Rp 350/min | Rp 800/min | Income variation across Jabodetabek |
| Car fuel cost | Rp 1,000/km | Rp 833/km (Pertalite only) | Rp 1,083/km (Pertamax) | Fuel choice |
| Motorcycle fuel cost | Rp 200/km | Rp 180/km (efficient scooter) | Rp 250/km (older motorcycle) | Fleet age variation |
| Transfer penalty | Rp 5,000 | Rp 3,000 | Rp 8,000 | Interchange quality variation |
| Motorcycle fatigue (40-60 min) | Rp 10,000 | Rp 5,000 | Rp 15,000 | Subjective; literature-supported range |
| Discomfort penalty (transit) | Rp 3,000 | Rp 0 (off-peak) | Rp 5,000 (severe crowding) | Time-of-day and route variation |
| Car parking (CBD) | Rp 25,000 | Rp 15,000 (subsidized) | Rp 40,000 (premium building) | Employer subsidy variation |
| TCR swing zone bounds | 0.8 -- 1.2 | 0.7 -- 1.3 (wider) | 0.9 -- 1.1 (tighter) | Classification sensitivity |

**Key sensitivity test**: VOT has the largest leverage on TCR outcomes. Low-VOT commuters (below UMR) have lower time costs, which reduces the GC differential between fast private modes and slower transit. Paradoxically, this makes transit MORE competitive for low-income groups (their VOT-weighted time penalty is smaller), which aligns with revealed preference: low-income Jabodetabek residents are more likely to use transit despite longer travel times (Ng, 2018).

---

## 9. Literature Citations

| Citation | Contribution to This Section |
|----------|------------------------------|
| Ng, W.S. (2018). Urban Transportation Mode Choice and Carbon Emissions in Southeast Asia. *Transportation Research Record*, 2672(25), 29-37. | Southeast Asian mode choice with motorcycle inclusion; validates three-mode framing; provides VOT range for Jakarta; documents motorcycle dominance for short trips |
| Sukor, N.S.A. & Bhayo, A.R. (2024). Unveiling the drivers of modal switch from motorcycles to public transport in Southeast Asia. *Transportation Research Part F*, 101, 197-213. | First-mile quality as strongest predictor of motorcycle-to-transit shift; fare affordability as secondary factor; ride duration > 30 min as shift trigger; modal inertia within 15-25% cost parity |
| Currie, G. (2010). Quantifying spatial gaps in public transport supply based on social needs. *Journal of Transport Geography*, 18(1), 31-41. | Foundational need-supply gap framework; transit accessibility as equity concern |
| Delmelle, E.C. & Casas, I. (2012). Evaluating the spatial equity of bus rapid transit-based accessibility patterns. *Transport Policy*, 20, 36-46. | Gini-based equity measurement in developing country BRT context |
| Pereira, R.H.M. et al. (2019). Distributional effects of transport policies on inequalities in access to opportunities in Rio de Janeiro. *Journal of Transport and Land Use*, 12(1), 741-764. | Transit equity measurement framework in developing mega-city; VOT and accessibility distribution methodology |
| Hardi, A.Z. & Murad, A.A. (2023). Spatial Analysis of Accessibility for Public Transportation: Jakarta BRT. *Journal of Computer Science*, 19(10), 1190-1202. | Jakarta-specific BRT accessibility quantification; 41% road network access finding validates first-mile deficit |
| Ortuzar, J.D. & Willumsen, L.G. (2011). *Modelling Transport* (4th ed.). Wiley. | Standard transport economics textbook; generalized cost framework; mode choice theory; 20% cost differential threshold |

---

## 10. DATA_MODEL.md Field Review

The current `docs/DATA_MODEL.md` Three-Way Cost Comparison section contains all necessary fields for this model. No new fields are required. Review of existing fields:

| Field | Status | Notes |
|-------|--------|-------|
| `gc_transit_idr` | OK | Matches formula output |
| `gc_car_idr` | OK | Matches formula output |
| `gc_motorcycle_idr` | OK | Matches formula output |
| `cheapest_private_mode` | OK | Derived from min(GC_car, GC_motorcycle) |
| `tcr_vs_car` | OK | GC_car / GC_transit |
| `tcr_vs_motorcycle` | OK | GC_motorcycle / GC_transit |
| `tcr_combined` | OK | min(GC_car, GC_motorcycle) / GC_transit |
| `transit_competitive_zone` | **Suggest update** | Current enum has 3 values. Consider adding `"transit_not_available"` for spatial units with no transit service. |
| `distance_to_sudirman_km` | OK | Used for distance-band analysis |

**Recommended DATA_MODEL.md update**:
- `transit_competitive_zone` enum: change from `"transit_wins" / "swing" / "private_wins"` to `"transit_wins" / "swing" / "private_wins" / "transit_not_available"`

This addition handles the null-GC_transit case explicitly rather than leaving it implicit.

---

## 11. Open Questions

1. **Motorcycle travel time estimation**: The model assumes motorcycle surface-road travel times that account for lane filtering (motorcycles weaving between cars). This is difficult to model from OSM road network alone. Field validation or Google Maps motorcycle routing (if available for Jakarta) would improve accuracy. In v1, we use estimated times based on average motorcycle speeds of 20-25 km/h on urban arterials during peak hours.

2. **Ojol fare variability**: Ojol (Grab/Gojek) fares fluctuate with surge pricing, time of day, and route. The model uses base fares. Sensitivity analysis should test 1.5x surge scenario for peak hours.

3. **JakLingko fare integration**: The model uses full individual fares. As JakLingko integration expands, discounted multi-modal fares may reduce transit GC by Rp 2,000-5,000. This should be tracked as a scenario.

4. **Parking cost variation**: CBD parking varies significantly between employer-subsidized (common in large corporations) and market rate. The model uses market rate; subsidized parking would reduce car GC and widen the transit competitiveness gap.

5. **Motorcycle fatigue calibration**: Fatigue factor values (Rp 5,000/10,000/15,000) are derived from literature-supported ride-duration thresholds but have not been validated for Jakarta commuters specifically. A stated-preference survey would calibrate these values. For now, sensitivity analysis covers the uncertainty range.

6. **Electric motorcycle emergence**: The growing adoption of electric motorcycles (lower fuel cost, potentially different fatigue profile) could shift the competitive dynamics. Not modeled in v1 but noted as a future consideration.

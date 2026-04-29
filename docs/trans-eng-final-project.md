# Trans-Eng Final Project — Hiroshima University AY2026

**Course**: Transportation Engineering, Hiroshima University
**Deadline**: June 3, 2026 (Session L15 — Final Presentation & Q&A)
**Branch**: `trans-eng/final-project-jabodetabek`
**Notebook folder**: `notebooks/trans-eng-final/`
**Status**: Scoping complete — data prep in progress

---

## 1. Course Context & Grading

The final individual project is **50% of total course grade**, split:

| Component | Weight | What it tests |
|---|---|---|
| Written Report | 50% of project | Framing, method transparency, result interpretation, policy implication |
| Q&A (June 3) | 50% of project | Ability to defend assumptions, explain choices, respond to critiques — designed to verify the work is yours and not AI-generated |

**Q&A is the higher-stakes half.** Every modelling choice must be defensible from first principles.

### Report sub-criteria
| Criterion | Weight | Notes |
|---|---|---|
| Problem Framing & Motivation | 10% | Why this corridor? Why mode choice? |
| Method Appropriateness & Transparency | 15% | MNL → NL justification; parameter sources |
| Result Interpretation & Limitations | 15% | What the numbers mean; what they can't tell us |
| Engineering/Policy Implications | 10% | Real-world decision value of the findings |

### Required framework
Must use **at least one** of: Travel Behavior, Network Analysis, Traffic Flow.
This project uses **Travel Behavior (mode choice)** as the primary framework, with an optional
extension to a logsum-based accessibility measure (bridges to the main research project).

---

## 2. Project Framing

**Title**: *Mode Choice and Accessibility Equity in Jabodetabek Commuter Corridors: A Nested Logit Analysis with Policy Simulation*

**Research Question**: How does the available transport mode set affect commuter welfare across income groups in Jabodetabek corridors, and what is the marginal welfare gain of adding a new rail link?

**Why this matters (motivation)**:
- Jabodetabek is Southeast Asia's largest urban agglomeration (~35 M people), yet car-dependent sprawl creates severe equity gaps in transit access
- Mode choice in Indonesian context is dominated by motorcycle (≥ 60% modal share nationally) — the IIA violation of MNL is particularly acute here
- Adding modes (MRT extensions, new KRL branches) is a live policy question; quantifying welfare gain by zone and income group informs prioritization

**Connection to main research project**:
The logsum welfare measure computed here is the same analytical layer as the TAI (Transit Accessibility Index) in the equity mapper. This project provides the travel behavior grounding for the mapper's accessibility scores.

---

## 3. Analytical Framework

### 3.1 Model sequence

```
Zone attributes + LOS matrix
        ↓
MNL mode choice (baseline)          ← L05 framework
        ↓
Nested Logit (motorized nest)       ← L06 framework, corrects IIA
        ↓
Logsum / Consumer Surplus           ← L06 welfare measure
        ↓
Policy simulation (ΔCS by zone + income group)
```

### 3.2 Why Nested Logit?

In Indonesia, car and motorcycle share a strong unobserved "motorization" attribute (ownership cost sunk, door-to-door convenience, cultural preference). Ridehailing (GoRide/GoCar) shares the app-platform utility but lacks the ownership component. Transit modes share schedule-bound public infrastructure. A plain MNL would assume all cross-elasticities are equal — clearly wrong when a KRL improvement draws far more from GoRide than from Car.

**3-nest structure**:
```
           Mode Choice
      /         |           \
Own Vehicle  Ridehailing   Transit
(Car, Moto)  (GoCar,GoRide) (KRL, TJ)
```

### 3.3 Welfare measure

Consumer Surplus change from a policy shock:

```
ΔCS_n = [logsum_n(after) − logsum_n(before)] / |β_cost|
```

This is in Rupiah per trip. Aggregated by zone and income segment = equity-comparable welfare gain.

---

## 4. Study Area — J-City

Seven origin zones + one destination (JCBD). Zones were split where a single administrative
area contains meaningfully different transit access sub-populations. This creates natural
within-region comparisons (J1a vs J1b, J3a vs J3b) and an inner-city reference zone (J5).

| Zone ID | Area | Character | TAI proxy* |
|---|---|---|---|
| J1a | Kota Bogor | Dense city core; KRL terminus (Bogor station); Jagorawi toll access | Q2 |
| J1b | Kab. Bogor (Parung, Leuwiliyang, outer ring) | Sprawl corridor; no rail within practical distance; car + moto only | Q4 |
| J2 | Bekasi (Kota) | Multi-modal hub: KRL Bekasi line + LRT Jabodebek + TransJakarta; high car ownership | Q2–Q3 |
| J3a | BSD Serpong (near KRL corridor) | KRL-served (Serpong line via Tanah Abang); newer mixed-use | Q2 |
| J3b | Gading Serpong / Karawaci | Far from KRL; car-dominant; some TransJakarta/Busway reach | Q3–Q4 |
| J4 | Depok | KRL (Depok line via Manggarai); partial TJ access; university corridor | Q2 |
| J5 | South Jakarta (Kebayoran Baru / Cilandak / Lebak Bulus) | Inner city; MRT Phase 1 corridor; shorter distances → lower absolute costs for all modes | Q1–Q2 |
| JCBD | Jakarta CBD (SCBD / Sudirman / Thamrin) | Destination only | — |

*TAI proxy references the equity mapper's four-quadrant classification (Q1=low need/high access,
Q4=high need/low access — "transit desert"). This annotation connects J-City to the main
research project without changing the model. See Discussion §6.

**Analytical value of zone design:**
- J1a vs J1b: same region, KRL-served vs transit desert → starkest welfare gap
- J3a vs J3b: same sub-district cluster, KRL proximity determines choice set width
- J5 South Jakarta: inner-city "best case" — MRT access + short OD distances → lower absolute
  costs for all modes; serves as upper-bound welfare reference vs outer transit-desert zones

### Zone attributes

| Zone | Population | Avg. monthly income (Rp k) | Car ownership | Moto ownership |
|---|---|---|---|---|
| J1a Kota Bogor | 1,100,000 | 3,500 | 25% | 65% |
| J1b Kab. Bogor (outer) | 800,000 | 2,800 | 20% | 72% |
| J2 Bekasi | 2,400,000 | 4,200 | 35% | 70% |
| J3a BSD Serpong | 250,000 | 9,000 | 65% | 50% |
| J3b Gading Serpong/Karawaci | 400,000 | 7,500 | 55% | 58% |
| J4 Depok | 1,100,000 | 3,800 | 28% | 68% |
| J5 South Jakarta | 700,000 | 8,000 | 55% | 52% |

### Mode availability by zone

Not all modes are available in all zones. Availability is a first-order finding: J1b and J3b
have no rail, so their choice set is Own Vehicle + Ridehailing only — the logsum for these
zones is structurally lower before any policy change.

| Zone | Car | Moto | 4WRH | 2WRH | KRL | TJ | Royal | LRT | MRT |
|---|---|---|---|---|---|---|---|---|---|
| J1a Kota Bogor | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| J1b Kab. Bogor | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| J2 Bekasi | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ direct | ✅ | ❌ |
| J3a BSD Serpong | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ +MRT | ❌ | ❌ |
| J3b Gading Serpong | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ partial | ✅ +MRT | ❌ | ❌ |
| J4 Depok | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ partial | ✅ direct | ❌ | ❌ |
| J5 South Jakarta | ✅ | ✅ | ✅ | ✅ | ✅ partial | ✅ | ❌ | ❌ | ✅ |

4WRH = GoCar/GrabCar economy class aggregate.
2WRH = GoRide/GrabBike/Maxim aggregate.
Royal = RoyalTrans express. "direct" = terminates at JCBD (Kuningan/Senayan). "+MRT" = terminates at Lebak Bulus or Fatmawati, requires onward MRT leg to reach JCBD.

**J1a and J1b have no RoyalTrans** — no published routes serve Bogor corridor.
**J1b remains the only zone with zero transit of any kind.**
**J3a/J3b Royal is not cost-equivalent to J2/J4 Royal** — the +MRT transfer adds ~Rp 9k and 25 min, making the full linked-trip cost ~Rp 39k and ~110 min.

### Population segments

| Segment | Share | Income (Rp k/month, mean) | Car own. | Moto own. |
|---|---|---|---|---|
| Low income | 30% | 2,500 | 5% | 60% |
| Middle income | 55% | 4,500 | 30% | 72% |
| High income | 15% | 12,000 | 75% | 45% |

---

## 5. Modes

9 modes in 3 nests:

| Mode | Label | Nest | Availability | Approx. cost basis | Notes |
|---|---|---|---|---|---|
| Car | Car | Own Vehicle | Car owners only | Fuel + toll; varies by distance | Higher cost from outer zones due to toll + distance |
| Motorcycle | Moto | Own Vehicle | Moto owners | Fuel only; no toll | Dominant nationally; shorter inner-city trips cheaper |
| 4-wheel ridehailing | 4WRH | Ridehailing | Everyone | Rp 3,500–4,500/km + Rp 1,500 booking | Aggregate: GoCar/GrabCar economy class; 5–10 min wait |
| 2-wheel ridehailing | 2WRH | Ridehailing | Everyone | Rp 2,000–2,500/km + Rp 1,000 booking | Aggregate: GoRide/GrabBike/Maxim; 3–7 min wait |
| KRL | KRL | Transit | Zone-specific (see §4) | Flat 3,000–8,000 | From GTFS routing (r5py output) |
| TransJakarta regular | TJ | Transit | Zone-specific (see §4) | Flat 3,500 | Partial reach in J3b, J4, J5; may require MRT transfer to reach JCBD |
| RoyalTrans (TransJakarta express) | Royal | Transit | J1a, J2, J3a, J3b, J4 | Flat 20,000–40,000 | Express bus; drops at Sudirman/Kuningan → egress ≈ 0 at JCBD |
| LRT Jabodebek | LRT | Transit | J2 Bekasi only | Flat 5,000 | Opened 2023; Bekasi Timur–Dukuh Atas |
| MRT Jakarta | MRT | Transit | J5 South Jakarta | Distance-based 3,000–14,000 | Phase 1 open; Lebak Bulus–Bundaran HI |

**Bike is excluded** (distances 30–60 km — infeasible unlike V-City's ≤5 km constraint).

### RoyalTrans — actual routes and destination reachability

Based on the published TransJakarta RoyalTrans route list, destinations vary significantly
by origin zone. Not all routes reach JCBD (Sudirman/Kuningan/Senayan) directly.

| Zone | Route | Terminus | JCBD direct? | Extra leg to JCBD |
|---|---|---|---|---|
| J1a Kota Bogor | None | — | ❌ no service | — |
| J1b Kab. Bogor | None | — | ❌ no service | — |
| J2 Bekasi | B14 Summarecon Bekasi → Kuningan | Kuningan | ✅ | none |
| J3a BSD Serpong | S12 Terminal BSD → Fatmawati | Fatmawati | ❌ | MRT Fatmawati→Sudirman |
| J3b Gading Serpong | S14 Summarecon Serpong → Lebak Bulus | Lebak Bulus | ❌ | MRT Lebak Bulus→Sudirman |
| J4 Depok (Cinere) | D31/D32 Cinere → Kuningan / Bundaran Senayan | Kuningan / Senayan | ✅ | none |
| J5 South Jakarta | None relevant | — | — | MRT already available |

**Linked-trip cost for J3a/J3b using Royal** is a two-leg chain:
Royal fare (~Rp 30k) + MRT fare (~Rp 9k) + MRT time (~25 min)
= total ~Rp 39,000 and ~110 min — barely cheaper than 4WRH and slower.

```
V_Royal_J3x = ASC_Royal + β_time × (T_access + T_Royal + T_MRT_egress)
                        + β_cost × (C_Royal_fare + C_MRT_fare)
```

This is the same linked-trip structure as regular TJ for zones that don't reach JCBD
directly. R5py handles the full routing automatically. The equity implication: J3b has
Royal *available* but the full-chain cost (~Rp 39k, ~110 min) erodes the advantage over
direct private modes, particularly for low-income commuters.

### Ridehailing aggregation rationale

4WRH and 2WRH are each modelled as a single aggregate alternative:
- **4WRH** covers GoCar, GrabCar economy. Premium taxis (Bluebird, GreenSM) and premium
  ride tiers are excluded — their users are a small, price-insensitive high-income segment
  better captured by income-segment interaction on β_cost than by a separate alternative.
- **2WRH** covers GoRide, GrabBike, Maxim. Discount dynamics (Maxim and GrabBike run
  heavy promotions with time-varying effective prices) are not modellable as a fixed cost
  in the LOS matrix. A single "effective average price" per km is used; discount variability
  goes in the Limitations section.

**Further study**: Disaggregate 4WRH into economy vs. premium tiers (separate ASC for
Bluebird/GreenSM) once income-stratified RP data is available.

### LRT / MRT scope notes

- **LRT Jabodebek**: Harjamukti branch (Cibubur direction) not modelled — does not serve
  any origin zone directly in this study. Relevant if future scope includes Cibubur corridor.
- **MRT Jakarta**: Phase 1 only (Lebak Bulus–Bundaran HI). Phase 2 north extension
  (Bundaran HI–Kota/Ancol) not included as it does not affect origin zone access.

### Nest structure rationale

```
              Mode Choice
       /           |            \
Own Vehicle    Ridehailing          Transit
(Car, Moto)   (4WRH, 2WRH)  (KRL, TJ, Royal, LRT, MRT)
```

Each nest shares a distinct unobserved utility component:
- **Own Vehicle**: sunk ownership cost + full door-to-door flexibility; no schedule dependency
- **Ridehailing**: app-platform convenience; no ownership barrier; waiting time uncertainty
- **Transit**: schedule-bound; shared infrastructure; lowest cost per km over long distances

The IIA violation is strongest within Own Vehicle (car/moto are highly substitutable in
Jakarta), moderate within Ridehailing (4WRH and 2WRH share app-platform preference but
differ significantly in comfort), and weakest within Transit (KRL/TJ/LRT/MRT share a
"public transit commuter" identity but serve different corridors). ρ values reflect this
ordering: ρ_OwnVehicle < ρ_Ridehailing < ρ_Transit.

### Multi-modal journey modelling — linked trip framework

MNL/NL alternatives in this project are **journey alternatives** (linked trips), not
individual mode segments. The choice set is:

```
Alt 1: Car direct          (one door-to-door journey)
Alt 2: Motorcycle direct
Alt 3: 4WRH direct
Alt 4: 2WRH direct
Alt 5: KRL chain           (access + trunk + egress — one journey utility)
Alt 6: TJ chain
Alt 7: LRT chain           (J2 only)
Alt 8: MRT chain           (J5 only)
```

For any transit alternative, the utility function sums impedance across all legs:

```
V_transit = ASC_transit
          + β_time × (T_access + T_trunk + T_egress)
          + β_cost × (C_access + C_transit_fare + C_egress)
```

Under Option A, `T_access` and `T_egress` are walk times from r5py; `C_access = C_egress = 0`
(walking is free). `ASC_transit` implicitly absorbs transfer disutility.
This is the standard linked-trip skim approach used in four-step models including JUTPI.

### First-mile / Last-mile options — progressive extensions

**Option A — PRIMARY METHOD (in scope)**: r5py computes the full composite journey time
(walk access + trunk + walk egress). This goes directly into the LOS matrix. Transit
alternatives compete against Car/Moto/Ridehailing as complete journey alternatives.
Methodologically sound and standard practice. No changes needed to implement.

**Option B — EXTENSION (if core notebooks done before ~May 17)**: Add a lower nest under
each transit alternative for access mode choice (walk vs GoRide vs park & ride):

```
Upper nest: journey alternatives
├── Car / Moto / 4WRH / 2WRH  (direct, unchanged)
└── Transit chain
    └── Lower nest: access mode to station
        ├── Walk          (r5py time, free)
        ├── 2WRH to station  (GoRide cost explicit)
        └── Park & ride   (moto fuel to station)
```

Logsum of lower nest = effective transit utility entering upper nest comparison.
GoRide access cost and a β_transfer parameter become explicit.
Trigger: core notebooks 01–04 stable AND L08+ material covered.

**Option C — EXTENSION (only if B stable with >2 weeks to June 3)**: Model both access
AND egress as sequential sub-choices. True trip-chain model. Requires per-person
station proximity data. Do not attempt if <2 weeks to deadline.

---

## 6. Level-of-Service (LOS) Matrix

### 6.1 Data sources

| Mode | Travel time source | Cost source |
|---|---|---|
| KRL | r5py GTFS routing output (already computed) | GTFS fare |
| TransJakarta regular | r5py GTFS routing output | GTFS fare (flat Rp 3,500); may include MRT transfer cost in composite |
| RoyalTrans | Published schedule / r5py if in GTFS feed | Flat Rp 20,000–40,000 depending on route |
| LRT Jabodebek | r5py GTFS routing output if present, else published timetable | Flat Rp 5,000 |
| MRT Jakarta | r5py GTFS routing output | Distance-based Rp 3,000–14,000 |
| Car | BPR function on approximate road distance; tolled segments from real toll tariff table | Fuel (Rp 2,350/km × consumption) + toll |
| Motorcycle | 1.1× car free-flow time (slightly slower in congestion); no toll | Fuel only (better consumption) |
| 4WRH | Car time + 7 min wait (peak average) | Rp 3,500/km + Rp 1,500 booking fee (effective average, no discount) |
| 2WRH | Motorcycle time + 5 min wait (peak average) | Rp 2,000/km + Rp 1,000 booking fee (effective average, no discount) |

### 6.2 Approximate LOS values (to be refined in 01_data_prep.ipynb)

`—` = mode not available. All times peak-hour estimates. Costs in Rp (k = thousands).

| OD pair | Car | Moto | 4WRH | 2WRH | KRL | TJ | Royal | LRT | MRT |
|---|---|---|---|---|---|---|---|---|---|
| J1a→JCBD (Kota Bogor) | 110 min / 120k | 100 min / 20k | 117 min / 175k | 105 min / 72k | 75 min / 8k | — | — | — | — |
| J1b→JCBD (Kab. Bogor outer) | 130 min / 90k | 120 min / 22k | 137 min / 130k | 125 min / 80k | — | — | — | — | — |
| J2→JCBD (Bekasi) | 75 min / 80k | 70 min / 15k | 82 min / 112k | 75 min / 49k | 55 min / 6k | 70 min / 3.5k | 65 min / 28k ✅ | 65 min / 5k | — |
| J3a→JCBD (BSD Serpong) | 90 min / 100k | 80 min / 18k | 97 min / 143k | 85 min / 56k | 85 min / 7k | — | 110 min / 39k ⚠️ | — | — |
| J3b→JCBD (Gading Serpong) | 95 min / 105k | 85 min / 20k | 102 min / 150k | 90 min / 60k | — | 90 min / 3.5k | 115 min / 39k ⚠️ | — | — |
| J4→JCBD (Depok) | 70 min / 70k | 65 min / 13k | 77 min / 98k | 70 min / 43k | 50 min / 5k | 65 min / 3.5k | 60 min / 22k ✅ | — | — |
| J5→JCBD (S. Jakarta) | 35 min / 40k | 30 min / 8k | 42 min / 60k | 35 min / 22k | 35 min / 4k | 30 min / 3.5k | — | — | 25 min / 6k |

✅ = Royal terminates at JCBD directly (no egress leg).
⚠️ = Royal terminates at Lebak Bulus or Fatmawati; time and cost include onward MRT leg (~25 min, ~Rp 9k).

4WRH/2WRH times = own-vehicle time + wait. Ridehailing cost = per-km rate × network distance + booking fee.

**J1b and J3b have no transit** — choice set is Own Vehicle + Ridehailing only. Their logsum
is structurally lower before any policy intervention. This is the central equity finding.

**J5 South Jakarta** shows the inner-city dynamic: distances are 3–5× shorter than outer zones,
so absolute ridehailing costs (Rp 22k–60k) are far lower — not a different tariff structure,
just shorter OD distance. MRT gives J5 the best transit option in the study.

### 6.3 Value of Time (VoT) — Indonesian literature

| Segment | VoT (Rp/hour) | Source |
|---|---|---|
| Low income | 12,000 | Consistent with BAPPENAS road pricing studies |
| Middle income | 25,000 | Standard Indonesian transport appraisal (BAPPENAS 2005, updated) |
| High income | 55,000 | Similar to Singapore studies scaled by PPP |

β_time and β_cost are calibrated so that VoT = β_time / β_cost matches these values per segment.

---

## 7. True DGP Parameters (Synthetic Approach)

Because no revealed preference dataset at individual level is available, this project uses
the **same synthetic approach as V-City** — parameters are set from literature, data is
generated from the DGP, then recovered by estimation. This is transparent and defensible.

### MNL DGP

| Parameter | Value | Rationale |
|---|---|---|
| β_time | −0.030 /min | VoT ≈ Rp 30,000/hr at β_cost = −0.0015 (middle income anchor) |
| β_cost | −0.0015 /Rp | ~1 std dev below V-City Japanese value, scaled for Indonesian income |
| ASC_Car | +1.20 | Strong revealed car preference in Jakarta (JUTPI 2010) |
| ASC_Moto | +1.80 | Dominant mode — highest intrinsic preference |
| ASC_4WRH | +0.60 | Below own car (waiting time, surge uncertainty); above transit for comfort |
| ASC_2WRH | +1.20 | Close to own motorcycle; slight penalty for waiting time and weather exposure |
| ASC_KRL | 0.00 | Reference |
| ASC_TJ | −0.30 | Slightly less preferred than KRL (lower reliability perception) |
| ASC_Royal | +0.10 | Above regular TJ (reserved seating, express, less crowded); below KRL (still road-based, traffic-dependent) |
| ASC_LRT | −0.10 | Near KRL baseline; newer, less familiar, limited corridor reach |
| ASC_MRT | +0.20 | Slightly above KRL — premium comfort, AC, punctual; well-received since 2019 opening |

### NL DGP — 3-nest structure

| Parameter | Value | Notes |
|---|---|---|
| ρ_OwnVehicle (Car + Moto) | 0.55 | Strong substitution — both require ownership, both fully door-to-door |
| ρ_Ridehailing (4WRH + 2WRH) | 0.70 | Looser — 4WRH and 2WRH share app-platform utility but differ sharply in comfort/price |
| ρ_Transit (KRL, TJ, LRT, MRT) | 0.75 | Moderate — all schedule-bound public modes; different corridors but shared rider identity |
| β_time, β_cost, ASCs | Same as MNL table | Only nest structure differs |

ρ closer to 1.0 = weaker within-nest correlation (approaches MNL). ρ closer to 0 = strong
substitution within the nest. Ordering: ρ_OwnVehicle < ρ_Ridehailing < ρ_Transit reflects
decreasing within-nest similarity across the three groups.

---

## 8. Policy Scenarios

### Scenario A — KRL/rail extension to J3b (Gading Serpong / Karawaci)
- **Shock**: Add direct rail access to J3b — transit time J3b→J5 drops from — to 70 min; cost Rp 7,500
- **Rationale**: J3b currently has zero transit. This is the closest real-world analogue to a planned rail extension in the Tangerang corridor.
- **Expected**: ΔCS largest for middle-income J3b commuters currently car/GoRide-dependent; J3b logsum rises sharply; J3a serves as a counterfactual (already rail-served)

### Scenario B — Toll price increase (congestion charge)
- **Shock**: Inner-Jakarta toll doubles for car users (+Rp 40,000 for all zones→J5)
- **Expected**: ΔCS negative for car-owning high-income; KRL share ↑ in J1a/J2/J3a/J4; no transit shift in J1b/J3b (no alternatives) — welfare loss falls hardest on transit-desert zones

### Scenario C — KRL frequency improvement (wait time reduction)
- **Shock**: KRL in-vehicle + wait time −20% across all KRL-served zones (J1a, J2, J3a, J4)
- **Expected**: Largest welfare gain for low-income KRL-captive (J1a Bogor corridor); J1b and J3b receive zero benefit — equity gap between transit-served and transit-desert zones widens in relative terms

For each scenario, report:
- Mode share before/after (bar chart per zone)
- ΔCS by zone × income segment (heatmap)
- Aggregate welfare gain in Rp/trip and Rp/day (zone population × share using transit × ΔCS)

---

## 9. Notebook Structure

All notebooks in `notebooks/trans-eng-final/`. Each is self-contained and sequentially numbered.

| Notebook | Purpose | Key outputs |
|---|---|---|
| `01_data_prep.ipynb` | Build zone table, LOS matrix, synthetic population | `data/jabodetabek_zones.csv`, `data/od_skim_jkt.csv`, `data/persons_jkt.csv` |
| `02_mnl_estimation.ipynb` | MNL from scratch (scipy MLE); parameter recovery; IIA demo | MNL parameter table, LL surface, mode share bar charts |
| `03_nl_estimation.ipynb` | Nested Logit; IIA violation test; parameter recovery | NL parameter table, rho interpretation, NL vs MNL mode share diff |
| `04_policy_simulation.ipynb` | Logsum / CS; 3 policy scenarios; ΔCS by zone + income | Welfare heatmaps, mode share shift charts, equity summary |

**Data folder**: `notebooks/trans-eng-final/data/`
**Figures folder**: `notebooks/trans-eng-final/figures/`

---

## 10. Report Structure

Target: ~3,000–4,000 words + figures. Saved at `notebooks/trans-eng-final/report/`.

```
1. Introduction (300w)
   - Jabodetabek context; why mode choice matters; RQ

2. Study Area and Data (400w)
   - J-City description; LOS matrix construction; synthetic population rationale

3. Methodology (800w)
   3.1 MNL specification + IIA limitation
   3.2 Nested Logit: 3-nest structure (Own Vehicle / Ridehailing / Transit) + rho interpretation
   3.3 First/last mile: Option A — access time absorbed in r5py transit skims
   3.4 Logsum welfare measure (L06 formula; units: Rp/trip)

4. Results (800w)
   4.1 MNL estimation — parameter recovery, VoT by segment
   4.2 NL vs MNL — rho estimates; IIA violation evidence
   4.3 Baseline mode shares by zone

5. Policy Simulations (600w)
   5.1 Scenario A (MRT/KRL extension to BSD)
   5.2 Scenario B (toll price increase)
   5.3 Scenario C (KRL frequency)
   Equity comparison: ΔCS across income segments

6. Discussion & Limitations (400w)
   - Synthetic data caveat; model scope
   - TAI quadrant bridge: J1b (Q4) and J3b (Q3–Q4) map to equity mapper's transit deserts —
     the welfare gap quantified here is the demand-side evidence for what the supply-side TAI shows
   - First/last mile: Option A used; Options B (GoRide as feeder sub-model) + C (full trip chain)
     as future directions
   - Ridehailing disaggregation: 4WRH and 2WRH are aggregated; premium taxis (Bluebird,
     GreenSM) and discount dynamics (Maxim/GrabBike promotions) not modelled
   - No peak-hour congestion feedback in baseline model (Extension D addresses this)
   - LRT scope limited to J2 (Bekasi); MRT scope limited to J5 (South Jakarta)

7. Conclusion (200w)
   - If Extension D was completed: note the UE→SO framing and how it recontextualises Scenario B
```

---

## 11. Further Extensions — Network Analysis

These extensions are **not required** for the June 3 submission but are natural continuations
using methods from L08–L10. The core project (notebooks 01–04) is self-contained without them.
Add only after the core notebooks are stable and only if time permits.

### Extension D — Car User Equilibrium assignment (after L08)
**Trigger**: after L08 lecture covers Frank-Wolfe UE algorithm.
**What**: take car demand from `04_policy_simulation.ipynb` → assign to a simplified
Jabodetabek road network → find User Equilibrium → compare congested times vs free-flow
times used in mode choice LOS.
**Network**: ~6–8 key links: Jagorawi (J1a), Tol Bekasi (J2), JORR (J3a/J3b), TB Simatupang
(J5), inner-ring arterials. BPR: t_a(v) = t_0[1 + 0.15·(v/c)^4] (same formula as V-City).
**Finding**: UE times are 30–50% higher than free-flow on congested inner links → mode choice
underestimated car disutility → true transit welfare advantage is larger than §5 results show.
**Policy connection**: Scenario B (toll increase) reframed as SO-seeking policy — show the
UE/SO gap (Price of Anarchy) and argue the toll bridges it.
**Notebook**: `05_car_ue_assignment.ipynb`

### Extension E — PT crowding check (after L09)
**Trigger**: after L09 lecture covers Davidson delay function for transit.
**What**: take KRL/MRT/LRT demand from mode choice → assign to transit lines → Davidson
delay: t(v) = t_0[1 + 0.2·v/(s−v)] → check whether Scenario C (frequency improvement)
causes overcrowding on high-demand lines.
**Finding**: capacity sanity check on policy scenarios — "does KRL actually have capacity
for the modal shift we predict in §5?"
**Notebook**: add cells to `04_policy_simulation.ipynb` or new `05_pt_crowding.ipynb`

### Extension F — Combined mode choice + assignment feedback (after L10)
**Trigger**: after L10; only attempt if D and E are stable with >1 week remaining.
**What**: full four-step feedback loop — iterate (mode choice → assignment → updated LOS →
mode choice) until convergence. This is the academically complete model.
**Risk**: convergence logic + debugging. Do not attempt if < 1 week to June 3.

### Data needed for D and E

| Item | Source |
|---|---|
| Link free-flow travel times (6–8 arterials) | Google Maps or Waze historical data; approximate from road class |
| Link capacities (pcu/hr) | Indonesia MKJI standard values by road class |
| PT line capacities (pax/hr) | KRL KCI published data; MRT Jakarta published data |

---

## 12. Timeline

| Date | Milestone | Track |
|---|---|---|
| 2026-04-28 | Branch created; project scoped | Core |
| 2026-05-03 (target) | `01_data_prep.ipynb` + `02_mnl_estimation.ipynb` complete | Core |
| 2026-05-10 (target) | `03_nl_estimation.ipynb` complete | Core |
| 2026-05-10 (L08 lecture) | Frank-Wolfe UE algorithm covered | Extension D unlocks |
| 2026-05-17 (target) | `04_policy_simulation.ipynb` + figures complete | Core |
| 2026-05-17 (L09 lecture) | Davidson PT crowding covered | Extension E unlocks |
| 2026-05-20 (target, if time) | `05_car_ue_assignment.ipynb` complete | Extension D |
| 2026-05-24 (target) | Draft report complete; Q&A prep begins | Core |
| 2026-05-31 (target) | Final report submitted; slides ready | Core |
| **2026-06-03** | **Final Presentation & Q&A (Session L15)** | |

---

## 12. Q&A Preparation — Anticipated Questions

These are the questions most likely from Prof. Chikaraishi. Each must be answerable cold.

| Question | Prepared answer anchor |
|---|---|
| "Why nested logit and not MNL?" | IIA violation — Car/Moto substitution is much stronger than Car/KRL; the 3-nest structure captures three distinct unobserved components (ownership, app convenience, schedule-bound). ρ < 1 estimated from data confirms it. |
| "Why include ridehailing?" | GoRide/GoCar are the dominant discretionary modes in Jakarta — omitting them would misattribute their share to Car/Moto and bias welfare estimates. No ownership barrier makes them especially relevant for equity analysis. |
| "Where does your β_time come from?" | Literature VoT anchor (BAPPENAS + Indonesian transport appraisal); calibrated so VoT = β_time/β_cost matches Rp 25,000/hr for middle income. Sensitivity table shows results are robust to ±30% VoT. |
| "Your data is synthetic — is this valid?" | V-City approach: known DGP, demonstrate parameter recovery (estimated ≈ true within SE), then apply to realistic Indonesian LOS values. The methodology is the contribution, not the raw observations. |
| "How does the logsum welfare measure work?" | Expected maximum utility over all alternatives; ΔCS = Δlogsum/|β_cost| in Rp; equivalent to compensating variation. Derived in L06 lecture. |
| "What's the equity finding?" | ΔCS from rail extension is largest for low-income KRL-dependent zones (Bogor); ridehailing welfare gain is highest for middle income (can afford GoRide, can't afford car) → corridor prioritization argument. |
| "How do you handle multi-modal journeys like GoRide→KRL→GoRide?" | Alternatives are modelled as linked-trip journeys, not individual segments. The KRL alternative's utility sums impedance across all legs: V = β_t(T_access + T_trunk + T_egress) + β_c(C_access + C_fare + C_egress). Under Option A, access/egress times come from r5py's walk routing; transfer disutility is absorbed into ASC_KRL. Explicit access mode competition — GoRide vs walk to station — is Option B: a lower nest under the transit alternative with GoRide access cost and β_transfer explicit. |
| "Why aggregate GoRide/GrabBike/Maxim into one alternative?" | Discount dynamics (Maxim and GrabBike run heavy promotions with time-varying effective prices) cannot be represented as a fixed cost in the LOS matrix. A single effective average price is used. Within-tier heterogeneity goes in Limitations. Premium 4WRH (Bluebird/GreenSM) is excluded for the same reason — their users are better captured via income-segment β_cost interaction than a separate alternative. |
| "Why model RoyalTrans separately from regular TransJakarta?" | RoyalTrans and regular TJ have fundamentally different cost structures (Rp 3,500 vs Rp 20,000–40,000) and destination profiles. Regular TJ may require an onward MRT transfer to reach JCBD from some termini (Lebak Bulus, Fatmawati), making its true linked-trip cost higher than Rp 3,500. RoyalTrans routes terminate at Sudirman/Kuningan directly — zero egress cost at JCBD. Modelling them as one alternative would conflate a budget feeder mode with an express premium service. Separate ASCs and cost inputs capture this correctly. |
| "Why add South Jakarta? It's close to the CBD." | J5 is an origin zone (~10–20 km from SCBD), not the CBD itself. Its analytical value is as an inner-city reference: it has MRT access and shorter OD distances, so absolute ridehailing and car costs are 3–5× lower than outer zones — not because of a different tariff, but because of distance. This upper-bound welfare zone makes the equity contrast with J1b/J3b sharper. |
| "Why use geographic zones instead of TAI quadrant zones?" | Geographic zones are nameable and defensible — J1b is Parung/Leuwiliyang, Kabupaten Bogor, which any examiner can place on a map. TAI quadrant zones are abstract and require explaining the equity mapper framework first. Instead, zones are *annotated* with TAI proxy (Q2/Q4 etc.) in the Discussion to bridge the two projects without complicating the choice model. |
| "Could you extend this to network analysis?" | Yes — mode choice output is the input OD matrix for assignment. Extension D (car UE assignment via Frank-Wolfe) uses the car demand from §5 as the trip matrix, assigns it to 6–8 key Jabodetabek links with BPR, and computes UE travel times. These are higher than the free-flow times used in mode choice — meaning the current model underestimates car disutility. Scenario B (toll increase) then maps cleanly to a System Optimum policy. Extension E (Davidson PT crowding) checks whether the KRL capacity can absorb the modal shift predicted in §5. |
| "What's the difference between UE and SO?" | At User Equilibrium (UE), each traveller minimises their own travel time — no traveller can reduce their time by switching routes. At System Optimum (SO), the total system travel time is minimised. SO requires internalising externalities (congestion you impose on others) — a toll equal to the marginal external cost achieves this. The toll in Scenario B is the instrument; UE vs SO is the theoretical justification. |
| "What are the limitations?" | No RP data; ownership endogenous; surge/discount dynamics not modelled; premium ridehailing excluded; no congestion feedback in baseline (Extension D adds this); single trip purpose; LRT limited to J2; MRT limited to J5; first/last mile absorbed not explicit. |

---

## 13. Current Status

| Item | Status | Notes |
|---|---|---|
| Project scoping | ✅ Done | This document |
| Branch | ✅ `trans-eng/final-project-jabodetabek` | Off `ui/stitch-redesign` |
| Folder structure | ⬜ Not created | Next action |
| `01_data_prep.ipynb` | ⬜ Not started | |
| `02_mnl_estimation.ipynb` | ⬜ Not started | Can reuse logic from `notebooks/logit_eda_mle.ipynb` |
| `03_nl_estimation.ipynb` | ⬜ Not started | Can reuse NL cells 27-36 from `notebooks/logit_eda_mle.ipynb` |
| `04_policy_simulation.ipynb` | ⬜ Not started | Can reuse logsum cells 43-54 from `notebooks/logit_eda_mle.ipynb` |
| `05_car_ue_assignment.ipynb` | ⏸ On hold | Extension D — unlock after L08 lecture; requires core notebooks complete |
| Report draft | ⬜ Not started | |

---

## 14. Key Files to Reference

| File | Why |
|---|---|
| `notebooks/logit_eda_mle.ipynb` | Existing MNL + NL + logsum implementation — reuse cells, adapt to J-City data |
| `notebooks/trans-eng-lectures/vcity_spec.md` | V-City DGP reference — methodology template |
| `notebooks/trans-eng-lectures/L06_logsum_concept.md` | Logsum formula + welfare measure derivation |
| `notebooks/trans-eng-lectures/L05_pres_discrete_choice.pdf` | MNL specification reference |
| `notebooks/trans-eng-lectures/L06_pres_nested_logit.pdf` | NL specification reference |
| `data/processed/scores/kelurahan_scores.geojson` | r5py routing output — source for KRL/TJ travel times per zone |

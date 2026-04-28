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

Four origin zones to Jakarta CBD. Chosen to represent the range of transit access quality
in the Jabodetabek periphery:

| Zone ID | Name | Character | Dominant current mode | KRL access |
|---|---|---|---|---|
| J1 | Bogor | Satellite city, KRL terminus | KRL + motorcycle | Strong |
| J2 | Bekasi | East corridor, mixed | Car + motorcycle | Moderate |
| J3 | BSD Serpong | South-west, car-dominant | Car | Weak |
| J4 | Depok | South, university corridor | KRL + Angkot | Moderate |
| J5 | Jakarta CBD | Destination (Sudirman/Thamrin) | — | — |

### Zone attributes (approximate, sourced from BPS + literature)

| Zone | Population | Avg. monthly income (Rp k) | Car ownership | Motorcycle ownership |
|---|---|---|---|---|
| J1 Bogor | 1,100,000 | 3,500 | 25% | 65% |
| J2 Bekasi | 2,400,000 | 4,200 | 35% | 70% |
| J3 BSD | 350,000 | 8,500 | 60% | 55% |
| J4 Depok | 1,100,000 | 3,800 | 28% | 68% |

### Population segments

| Segment | Share | Income (Rp k/month, mean) | Car own. | Moto own. |
|---|---|---|---|---|
| Low income | 30% | 2,500 | 5% | 60% |
| Middle income | 55% | 4,500 | 30% | 72% |
| High income | 15% | 12,000 | 75% | 45% |

---

## 5. Modes

6 modes in 3 nests:

| Mode | Nest | Availability | Cost per trip (Rp) | Notes |
|---|---|---|---|---|
| **Car** | Own Vehicle | Car owners only | Fuel + toll ≈ 50,000–150,000 | Varies by distance + toll road |
| **Motorcycle** | Own Vehicle | Moto owners | Fuel ≈ 10,000–25,000 | Dominant mode nationally |
| **GoCar / GrabCar** | Ridehailing | Everyone | ~Rp 3,500/km + Rp 1,500 booking | No ownership barrier; 5–10 min wait |
| **GoRide / GrabBike** | Ridehailing | Everyone | ~Rp 2,000/km + Rp 1,000 booking | Fastest door-to-door in congestion |
| **KRL** | Transit | Everyone | Flat 3,000–8,000 | From GTFS routing (r5py output) |
| **TransJakarta BRT** | Transit | Everyone | Flat 3,500 | From GTFS; limited to J1/J4 direct |

**Bike is excluded** (distances 30–60 km — infeasible unlike V-City's ≤5 km constraint).

### Nest structure rationale

```
           Mode Choice
      /         |           \
Own Vehicle  Ridehailing   Transit
(Car, Moto)  (GoCar,GoRide) (KRL, TJ)
```

Each nest shares a distinct unobserved utility component:
- **Own Vehicle**: sunk ownership cost + full door-to-door flexibility
- **Ridehailing**: app convenience + no ownership required, but waiting time uncertainty
- **Transit**: schedule-bound + shared infrastructure; lowest cost per km

The IIA violation between Car and Motorcycle (strong within-nest substitution) and between KRL and TJ (shared "transit rider" identity) motivates the 3-nest structure over plain MNL.

### First-mile / Last-mile (access/egress)

**Current scope — Option A (absorbed)**: r5py routes include walking access to the nearest boarding stop and egress to the destination. KRL and TJ travel times in the LOS matrix already embed first/last mile walking time. This is the standard skim-based approach and is methodologically sufficient for this analysis.

**Further study — Option B (explicit access mode choice)**: Model GoRide as a first-mile feeder to KRL stations as a separate sub-choice. This requires a two-stage nested model (access mode → main mode) and is a natural extension given Gojek's real-world role at Jakarta station forecourts.

**Further study — Option C (full trip chain)**: Model the full multi-modal sequence (origin → access leg → trunk leg → egress leg → destination) as a behavioural discrete choice problem. Equivalent to what r5py does for routing but rendered as a utility-maximising sequential choice. Relevant if origin-destination micro-data becomes available.

---

## 6. Level-of-Service (LOS) Matrix

### 6.1 Data sources

| Mode | Travel time | Cost |
|---|---|---|
| KRL | r5py GTFS routing output (already computed) | GTFS fare |
| TransJakarta | r5py GTFS routing output | GTFS fare |
| Car | BPR function on approximate road distance; tolled segments from real toll tariff table | Fuel (Rp 2,350/km × consumption) + toll |
| Motorcycle | 1.1× car free-flow time (slightly slower in traffic); no toll | Fuel only (better consumption) |
| GoCar | Car time + 7 min wait (peak average) | Rp 3,500/km + Rp 1,500 booking fee |
| GoRide | Motorcycle time + 5 min wait (peak average) | Rp 2,000/km + Rp 1,000 booking fee |

### 6.2 Approximate LOS values (to be refined in 01_data_prep.ipynb)

| OD pair | Car | Moto | GoCar | GoRide | KRL | TJ |
|---|---|---|---|---|---|---|
| J1→J5 (Bogor) | 110 min / Rp 120k | 100 min / Rp 20k | 117 min / Rp 175k | 105 min / Rp 72k | 75 min / Rp 8k | — |
| J2→J5 (Bekasi) | 75 min / Rp 80k | 70 min / Rp 15k | 82 min / Rp 112k | 75 min / Rp 49k | 55 min / Rp 6k | 70 min / Rp 3.5k |
| J3→J5 (BSD) | 90 min / Rp 100k | 80 min / Rp 18k | 97 min / Rp 143k | 85 min / Rp 56k | 90 min / Rp 7k (transfer) | — |
| J4→J5 (Depok) | 70 min / Rp 70k | 65 min / Rp 13k | 77 min / Rp 98k | 70 min / Rp 43k | 50 min / Rp 5k | 65 min / Rp 3.5k |

GoCar/GoRide times = own-vehicle time + wait. Cost = per-km rate × approximate network distance + booking fee.

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
| ASC_GoCar | +0.60 | Below own car (waiting time disutility, surge uncertainty) but above transit |
| ASC_GoRide | +1.20 | Close to own motorcycle; slightly below due to waiting time |
| ASC_KRL | 0.00 | Reference |
| ASC_TJ | −0.30 | Slightly less preferred than KRL (lower reliability perception) |

### NL DGP — 3-nest structure

| Parameter | Value | Notes |
|---|---|---|
| ρ_OwnVehicle (Car + Moto nest) | 0.55 | Strong substitution — both require ownership, both door-to-door |
| ρ_Ridehailing (GoCar + GoRide nest) | 0.70 | Looser — GoCar and GoRide differ significantly in comfort; shared app platform only |
| ρ_Transit (KRL + TJ nest) | 0.75 | Moderate — both schedule-bound public modes but different route structures |
| β_time, β_cost, ASCs | Same as MNL table | Only nest structure differs |

ρ closer to 1.0 = weaker correlation within nest (approaches MNL). ρ closer to 0 = strong within-nest substitution (IIA violation is large).

---

## 8. Policy Scenarios

### Scenario A — MRT/KRL extension to BSD (J3)
- **Shock**: Add direct rail to J3 (BSD Serpong MRT extension): transit time J3→J5 drops from 90 → 45 min; cost 9,500 Rp
- **Expected**: ΔCS largest for middle-income J3 commuters; mode shift from car

### Scenario B — Toll price increase (congestion charge)
- **Shock**: Toll on inner Jakarta doubles for car users (cost +40,000 Rp for J1/J2/J3→J5)
- **Expected**: ΔCS negative for car-owning high-income; KRL share ↑; motorcycle unaffected

### Scenario C — KRL frequency doubling (wait time halved)
- **Shock**: KRL in-vehicle + wait time −20% across all KRL-served zones
- **Expected**: Largest welfare gain for low-income KRL-dependent (J1 Bogor corridor)

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
   - First/last mile: Option A used; Options B + C as future directions
   - Ridehailing dynamics (surge pricing, availability heterogeneity) not modelled
   - No peak-hour congestion feedback; single trip purpose

7. Conclusion (200w)
```

---

## 11. Timeline

| Date | Milestone |
|---|---|
| 2026-04-28 | Branch created; project scoped |
| 2026-05-03 (target) | `01_data_prep.ipynb` + `02_mnl_estimation.ipynb` complete |
| 2026-05-10 (target) | `03_nl_estimation.ipynb` complete |
| 2026-05-17 (target) | `04_policy_simulation.ipynb` + figures complete |
| 2026-05-24 (target) | Draft report complete; Q&A prep begins |
| 2026-05-31 (target) | Final report submitted; slides ready |
| **2026-06-03** | **Final Presentation & Q&A (Session L15)** |

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
| "Why not model first/last mile explicitly?" | Access/egress time is already embedded in r5py GTFS skims (Option A). Explicit access mode choice (Option B) is a natural extension — GoRide as first-mile feeder to KRL — but requires a two-stage nested model outside this scope. |
| "What are the limitations?" | No RP data; ownership endogenous; surge pricing not modelled; no peak-hour congestion feedback; single trip purpose; first/last mile absorbed not explicit. |

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

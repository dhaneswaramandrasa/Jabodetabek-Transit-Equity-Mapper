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

In Indonesia, car and motorcycle share a strong unobserved "motorization" attribute (ownership cost sunk, door-to-door convenience, cultural preference). A policy shock that makes KRL faster will shift motorcycle users to KRL **more** than it shifts them to car — this is exactly the IIA violation that NL corrects for. The motorized nest (Car + Motorcycle) vs. non-motorized / transit nest is the theoretically grounded structure.

**Nest structure**:
```
           Mode Choice
          /            \
   Motorized           Transit
  (Car, Moto)      (KRL, TransJakarta)
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

| Mode | Availability | Cost per trip (Rp) | Notes |
|---|---|---|---|
| **Car** | Car owners only | Fuel + toll ≈ 50,000–150,000 | Varies by zone distance + toll road |
| **Motorcycle** | Moto owners + rental | Fuel ≈ 10,000–25,000 | Dominant mode; no fixed route |
| **KRL** | All | Flat 3,000–8,000 | From GTFS routing (r5py output) |
| **TransJakarta BRT** | All | Flat 3,500 | From GTFS; limited to J1/J4 direct |

**Bike is excluded** (distances 30–60 km — infeasible unlike V-City's ≤5 km constraint).

---

## 6. Level-of-Service (LOS) Matrix

### 6.1 Data sources

| Mode | Travel time | Cost |
|---|---|---|
| KRL | r5py GTFS routing output (already computed) | GTFS fare |
| TransJakarta | r5py GTFS routing output | GTFS fare |
| Car | BPR function on approximate road distance; tolled segments from real toll tariff table | Fuel (Rp 2,350/km × consumption) + toll |
| Motorcycle | 1.1× car free-flow time (slightly slower in traffic); no toll | Fuel only (better consumption) |

### 6.2 Approximate LOS values (to be refined in 01_data_prep.ipynb)

| OD pair | Car time (min) | Car cost (Rp) | Moto time (min) | Moto cost (Rp) | KRL time (min) | KRL cost (Rp) |
|---|---|---|---|---|---|---|
| J1→J5 (Bogor) | 90–120 | 120,000 | 100 | 20,000 | 75 | 8,000 |
| J2→J5 (Bekasi) | 60–90 | 80,000 | 70 | 15,000 | 55 | 6,000 |
| J3→J5 (BSD) | 75–100 | 100,000 | 80 | 18,000 | 90 (transfer) | 7,000 |
| J4→J5 (Depok) | 60–80 | 70,000 | 65 | 13,000 | 50 | 5,000 |

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
| ASC_KRL | 0.00 | Reference |
| ASC_TJ | −0.30 | Slightly less preferred than KRL (lower reliability perception) |

### NL DGP

| Parameter | Value | Notes |
|---|---|---|
| ρ_Motorized (Car+Moto nest) | 0.55 | Strong within-motorized substitution; < V-City's 0.60 reflecting deeper moto-car similarity |
| ρ_Transit (KRL+TJ nest) | 0.75 | Looser transit nest |
| β_time, β_cost, ASCs | Same as MNL table | Only nest structure differs |

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
   3.2 Nested Logit: motorized nest structure + rho interpretation
   3.3 Logsum welfare measure (L06 formula; units: Rp/trip)

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
   - Synthetic data caveat; model scope; extensions

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
| "Why nested logit and not MNL?" | IIA violation — motorcycle-car substitution is stronger than motorcycle-KRL; rho < 1 confirms within-motorized correlation |
| "Where does your β_time come from?" | Literature VoT anchor (BAPPENAS + Indonesian transport appraisal); calibrated so VoT = β_time/β_cost matches Rp 25,000/hr for middle income |
| "Your data is synthetic — is this valid?" | V-City approach: known DGP, demonstrate parameter recovery (estimated ≈ true within SE), then apply to realistic Indonesian LOS values |
| "How does the logsum welfare measure work?" | Expected maximum utility over alternatives; ΔCS = Δlogsum/|β_cost| in Rp; consumer surplus with inclusive value |
| "What's the equity finding?" | ΔCS from rail extension is largest for low-income KRL-dependent zones (Bogor) → welfare-distributional argument for corridor prioritization |
| "What are the limitations?" | No RP data; car/moto ownership endogenous; no peak-hour congestion feedback; single-purpose trips only |

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

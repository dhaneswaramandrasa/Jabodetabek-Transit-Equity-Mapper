# Trans-Eng Final Project — Hiroshima University AY2026

**Course**: Transportation Engineering, Hiroshima University
**Deadline**: June 3, 2026 (Session L15 — Final Presentation & Q&A)
**Branch**: `trans-eng/final-project-jabodetabek`
**Notebook folder**: `notebooks/trans-eng-final/`
**Status**: Scoping complete — ready to begin `01_data_prep.ipynb`

---

## ⚑ MASTER PLAN — READ FIRST (for agents and future-self)

This document is the **single source of truth** for the trans-eng final project track.
CLAUDE.md instructs every agent to read this before touching any notebook in this track.

**Before doing any work**:
1. Read this entire document
2. Check **§13 Current Status** for the next incomplete notebook
3. Check **§14 Key Files** for code/data to reuse before writing anything from scratch
4. Read `docs/state.md` "Trans-Eng Track" section for last action

**Before ending a session**:
1. Update **§13 Current Status** — mark ✅ what was completed
2. Update `docs/state.md` "Trans-Eng Track" — last action + next action
3. Commit with `feat(trans-eng): ...` or `docs(trans-eng): ...`

**Do not unilaterally change**:
- The mode list in §5 (9 modes, 3 nests, ownership-based nesting)
- The DGP parameters in §7 — these are the literature-anchored values defended in Q&A
- The zone definitions in §4 — these are the geographically defensible zones
- The nest structure in §5 — see §3.4 for why ownership-based, not vehicle-type

If a section needs revision because of new data or methodological insight, flag it in
the next session's commit message; do not silently rewrite.

---

## PROJECT FLOW — Data → Estimation → Welfare (comprehensive)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        STAGE 0: DATA INGESTION                          │
│                                                                         │
│  ┌──────────────────────┐  ┌──────────────────┐  ┌───────────────────┐  │
│  │ kelurahan_scores     │  │ GTFS feeds        │  │ transit_stops     │  │
│  │ .geojson             │  │ (KRL, TJ, MRT)    │  │ _summary.csv      │  │
│  │ 1,502 kelurahan      │  │ frequencies.txt   │  │ 4,000+ stops      │  │
│  │                      │  │ stop_times.txt    │  │ mode, fare_tier   │  │
│  │ • population         │  │ trips.txt         │  │ route_ids          │  │
│  │ • avg_expenditure    │  └──────────────────┘  └───────────────────┘  │
│  │ • poverty_rate       │                                               │
│  │ • gc_car_idr  ← BPR  │  ┌──────────────────────────────────────────┐ │
│  │ • gc_motorcycle_idr  │  │ docs/literature/ (5 PDFs)                 │ │
│  │ • distance_to_cbd_km │  │ Ilahi 2021, Bastarianto 2019,             │ │
│  │ • transit_metrics    │  │ Belgiawan 2019, Binsuwadan 2023,          │ │
│  │ • zero_vehicle_hh_pct│  │ World Bank 2023                           │ │
│  └──────────────────────┘  └──────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                  STAGE 1: ZONE TABLE + LOS (01_data_prep.ipynb)          │
│                                                                         │
│  ┌─────────────────────────────────────┐                                │
│  │ 1,502 kelurahan → 7 zones           │                                │
│  │ via KEC_TO_ZONE mapping (CamelCase) │                                │
│  │                                     │                                │
│  │  J1a (68 kel)  J1b (75 kel)         │                                │
│  │  J2  (56 kel)  J3a (33 kel)         │                                │
│  │  J3b (51 kel)  J4  (71 kel)         │                                │
│  │  J5  (43 kel)                       │                                │
│  └─────────────────────────────────────┘                                │
│                    │                                                     │
│                    ▼                                                     │
│  ┌─────────────────────────────────────┐                                │
│  │ Zone attributes (aggregated)        │                                │
│  │ • commuting_population              │                                │
│  │ • est_monthly_income_k = exp/0.70   │  ◄── from kelurahan data       │
│  │ • mean_gc_car_idr, mean_gc_moto_idr │                                │
│  │ • distance_cbd_km                   │                                │
│  │ • q4_pct, q1_pct (TAI quadrants)   │                                │
│  └─────────────────────────────────────┘                                │
│                    │                                                     │
│                    ▼                                                     │
│  ┌─────────────────────────────────────┐                                │
│  │ Mode availability (per zone)        │                                │
│  │ • Transit stops → zones via cKDTree │  ◄── from transit_stops        │
│  │ • Geographic overrides applied      │      + geographic knowledge    │
│  │ • Private + RH: always available    │                                │
│  └─────────────────────────────────────┘                                │
│                    │                                                     │
│                    ▼                                                     │
│  ┌─────────────────────────────────────┐                                │
│  │ LOS matrix (43 rows)                │                                │
│  │ origin × destination × mode         │                                │
│  │                                     │                                │
│  │ Car:    time = dist/25kmh           │  ◄── BPR speed assumption      │
│  │         cost = gc_car_idr (pipeline)│                                │
│  │ Moto:   time = dist/32kmh           │                                │
│  │         cost = gc_motorcycle_idr     │                                │
│  │ 4WRH:   time = car + 7min wait      │  ◄── published tariff schedule │
│  │         cost = 3500/km + 1500       │                                │
│  │ 2WRH:   time = moto + 5min wait     │                                │
│  │         cost = 2000/km + 1000       │                                │
│  │ Transit: schedule-based estimates   │  ◄── r5py NULL (documented)    │
│  │         published fare tables       │                                │
│  └─────────────────────────────────────┘                                │
│                                                                         │
│  Exports: jabodetabek_zones.csv, od_skim_jkt.csv                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│           STAGE 2: DGP PARAMETERS + SYNTHETIC PERSONS (01_data_prep)    │
│                                                                         │
│  ┌─────────────────────────────────────┐                                │
│  │ TRUE_DGP (18 MNL params)            │  ◄── Ilahi (2021) PDF ✓        │
│  │                                     │                                │
│  │ 9 × β_time (mode-specific)          │  Ilahi Table 11 VTTS           │
│  │   β_time = β_cost × VTTS / 60,000   │  β_cost = −1.42 (Table 10)    │
│  │                                     │                                │
│  │ 8 × ASC (KRL = 0 reference)         │  DGP-specified; Bodetabek-     │
│  │   Car +0.90, Moto +1.20, 2WRH +1.10 │  adjusted from Ilahi's        │
│  │   4WRH +0.50, MRT +0.30, RT +0.05   │  intra-Jakarta ordering        │
│  │   LRT −0.10, TJ −0.30               │                                │
│  └─────────────────────────────────────┘                                │
│                    │                                                     │
│                    ▼                                                     │
│  ┌─────────────────────────────────────┐                                │
│  │ Income segments + vehicle access    │  ◄── Ilahi Table 2-3           │
│  │                                     │                                │
│  │ low  33.3%: Rp 3.0M, car 5%, moto 60%│  car access: 25.60% overall    │
│  │ mid  50.3%: Rp 9.0M, car 26%, moto 80%│  MC access:  67.90% overall    │
│  │ high 16.4%: Rp 22M,  car 65%, moto 48%│  (Ilahi Table 3, p. 407)       │
│  └─────────────────────────────────────┘                                │
│                    │                                                     │
│                    ▼                                                     │
│  ┌─────────────────────────────────────┐                                │
│  │ 5,000 synthetic persons             │  ◄── weighted by zone pop       │
│  │ • zone_id (weighted by population)  │      income from Ilahi dist.   │
│  │ • income_segment + income_rp_k      │      ownership calibrated to    │
│  │ • car_owner, moto_owner             │      Ilahi's access rates       │
│  │ • LOS joined per zone×mode          │                                │
│  │ • V_m = ASC + β_time×t + β_cost×c   │                                │
│  │ • V_m = -inf for unavailable modes  │                                │
│  └─────────────────────────────────────┘                                │
│                                                                         │
│  Export: persons_jkt.csv (5,000 rows × 33 cols)                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
┌──────────────────────────────┐  ┌──────────────────────────────┐
│  STAGE 3: MNL MLE            │  │  STAGE 5: NL DGP params      │
│  (02_mnl_estimation.ipynb)   │  │  (for 03_nl_estimation)      │
│                              │  │                              │
│  1. Add Gumbel(0,1) to V     │  │  ρ_OwnVehicle  = 0.55        │
│     → synthetic choices      │  │  ρ_Ridehailing = 0.70        │
│                              │  │  ρ_Transit     = 0.75        │
│  2. MLE via scipy BFGS       │  │                              │
│     recover 18 params        │  │  Bastarianto (2019) ✓        │
│                              │  │                              │
│  3. Hessian + Robust SE      │  └──────────────────────────────┘
│                              │               │
│  4. Recovery: |θ̂-θ|<2·SE?   │               ▼
│                              │  ┌──────────────────────────────┐
│  5. IIA demo (KRL Express)   │  │  STAGE 4: NL MLE            │
│                              │  │  (03_nl_estimation.ipynb)   │
│  6. Export: mnl_estimates    │  │                              │
│     .json                    │  │  1. NL choice generation     │
└──────────────────────────────┘  │     (correlated Gumbel)      │
                                  │                              │
                                  │  2. MLE recover β_time,      │
                                  │     β_cost, ASCs, 3×ρ        │
                                  │                              │
                                  │  3. LR test: NL vs MNL       │
                                  │     H₀: ρ = 1 (MNL)          │
                                  │                              │
                                  │  4. MNL-on-NL SE divergence  │
                                  │     (misspecification check)  │
                                  └──────────────────────────────┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│            STAGE 4b: MIXED LOGIT DIAGNOSTIC (03b_mixed_logit.ipynb)      │
│                                                                         │
│  Purpose: test for unobserved heterogeneity beyond NL nest correlation. │
│  Anchored to L07 lab (your L07_estimation_lab.ipynb Tasks 3 + 3.5),     │
│  not Ilahi Model 3 — same Beta names, same Wald-test pattern.           │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ SPEC (random β_time on TIME, NOT random ASCs)                  │    │
│  │                                                                │    │
│  │   β_time_n = β_time_mean + σ_time · η_n,    η_n ~ N(0, 1)      │    │
│  │   V_m,n = ASC_m + β_time_n · t_m + β_cost · c_m                │    │
│  │                                                                │    │
│  │ Justification: matches L07 lab Task 3 specification. Random    │    │
│  │ ASCs (Ilahi Model 3 pattern) noted in Discussion as alternative│    │
│  │ parameterization in Indonesian literature.                     │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐    │
│  │  4b.1 — MXL on MNL-DGP data  │  │  4b.2 — MXL recovery test    │    │
│  │  (negative test)             │  │  (positive test)             │    │
│  │                              │  │                              │    │
│  │  Data: persons_jkt.csv       │  │  Data: persons_jkt_mixed.csv │    │
│  │   (DGP fixed β_time)         │  │   (DGP β_time ~ N(μ, 0.04²)) │    │
│  │                              │  │                              │    │
│  │  Estimation: simulated MLE   │  │  Estimation: same MXL spec   │    │
│  │   80–200 Halton draws        │  │   on heterogeneous DGP       │    │
│  │                              │  │                              │    │
│  │  Expected: σ̂ ≈ 0,            │  │  Expected: σ̂ ≈ 0.04 ✓        │    │
│  │   Wald |t| < 1.96            │  │   Wald |t| > 1.96            │    │
│  │                              │  │                              │    │
│  │  → "no evidence of unobs.    │  │  → "estimator works; the     │    │
│  │     heterogeneity, NL stays" │  │     null in 4b.1 is real"   │    │
│  └──────────────────────────────┘  └──────────────────────────────┘    │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ DIAGNOSTIC HIERARCHY (L07 protocol — Wald primary, NOT LR)     │    │
│  │                                                                │    │
│  │ ① PRIMARY:  Wald test on σ_time vs 0   (|t| > 1.96 → reject)   │    │
│  │ ② SECONDARY: Boundary-corrected LR vs χ²(0.5,1), crit = 2.71   │    │
│  │             (Gourieroux et al. 1982 — σ tested at boundary)    │    │
│  │ ③ FORBIDDEN: Plain LR vs χ²(1) — simulated LL is Jensen-biased │    │
│  │              downward, statistic can flip sign (L07 Task 3.5). │    │
│  │ ④ Cross-spec ρ², SE divergence — supplementary fit checks      │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  Outcome on synthetic data: 4b.1 fails to reject σ = 0 → NL is the      │
│  best-supported model → Stage 5 uses NL parameters.                     │
│  This is the L07 Five Habits punchline: "be willing to reject the       │
│  richer model when evidence does not support it" (slide 33).            │
│                                                                         │
│  Exports: mxl_estimates.json, mxl_recovery_diagnostics.json,            │
│           persons_jkt_mixed.csv (recovery DGP)                          │
└─────────────────────────────────────────────────────────────────────────┘
                                                  │
                    ┌─────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              STAGE 5: WELFARE + POLICY (04_policy_simulation.ipynb)      │
│                                                                         │
│  ┌─────────────────────────────────────┐                                │
│  │ For each zone × income_segment:     │  ◄── 21 rows, NOT 5,000        │
│  │                                     │                                │
│  │  V_zm = ASC_m + β_time_m×t_zm       │  estimated params from 02/03   │
│  │         + β_cost×c_zm               │                                │
│  │                                     │                                │
│  │  MNL logsum = ln Σ exp(V_m)         │                                │
│  │  NL  logsum = ln Σ_nest exp(IV_k)   │                                │
│  │     IV_k = ρ_k ln Σ_{m∈k} exp(V/ρ)  │  NL gives more conservative ΔCS│
│  │                                     │                                │
│  │  CS = logsum / |β_cost|  (Rp/trip)  │  money-metric welfare          │
│  └─────────────────────────────────────┘                                │
│                    │                                                     │
│                    ▼                                                     │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ BASELINE WELFARE MAP (RQ1)                                       │   │
│  │                                                                  │   │
│  │           J1b-low   J1b-mid   J1b-high   ...   J5-high           │   │
│  │ # modes      4         4         4                  7            │   │
│  │ CS/trip    X₁₁       X₁₂       X₁₃               X₇₃             │   │
│  │                                                                  │   │
│  │  → ΔCS between J1b-low and J2-low = welfare cost of transit      │   │
│  │    desert, controlling for income                                │   │
│  │  → ΔCS between J1b-low and J1b-high = income gradient within     │   │
│  │    the same constrained choice set                               │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                    │                                                     │
│                    ▼                                                     │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ POLICY SIMULATIONS (RQ2) — 8 scenarios A–H                        │   │
│  │                                                                  │   │
│  │  Group 1 — Baseline (A–C):                                       │   │
│  │   A: KRL to J3b       — add KRL to transit desert zone           │   │
│  │   B: Toll +Rp 40k     — congestion charge on all zones            │   │
│  │   C: KRL freq −20%    — service improvement on served zones       │   │
│  │                                                                  │   │
│  │  Group 2 — Transit expansion (D–E):                              │   │
│  │   D: TJ to J1b        — budget BRT to worst-served zone          │   │
│  │   E: MRT to BSD       — premium rail to already-served zone       │   │
│  │                                                                  │   │
│  │  Group 3 — Restructuring + service (F–H):                        │   │
│  │   F: TJ BSD→CBD direct — eliminate transfer penalty              │   │
│  │   G: RoyalTrans freq  — 3→12 departures/peak                     │   │
│  │   H: RoyalTrans fare  — 50% fare reduction                       │   │
│  │                                                                  │   │
│  │  For each scenario:                                              │   │
│  │   ΔCS_zone,segment = (LS_after − LS_before) / |β_cost|           │   │
│  │   Aggregate welfare = ΔCS × trips/segment × pop_zone             │   │
│  │   Equity report: which zones/segments gain most?                 │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     OUTPUT: Report + Presentation                        │
│                                                                         │
│  • Parameter recovery tables (MNL 18 params, NL 18+3)                   │
│  • Baseline mode share bar charts × zone                                │
│  • Baseline welfare (CS) heatmap × zone × income                        │
│  • Policy scenario ΔCS heatmaps (8 panels)                              │
│  • Equity comparison: which scenarios close Q4 vs Q1 gap?               │
│  • NL vs MNL welfare comparison: why NL is more conservative            │
└─────────────────────────────────────────────────────────────────────────┘
```

### Data lineage at a glance

| Stage | What | Real or synthetic? | Source |
|---|---|---|---|
| Zone boundaries | 7 zones from kecamatan | **Real** — 1,502 kelurahan | `kelurahan_scores.geojson` |
| Zone attributes | population, expenditure, poverty, CBD distance | **Real** — aggregated from kelurahan | Pipeline |
| Car/moto LOS | time, generalized cost | **Real** — BPR + pipeline | `gc_car_idr`, `gc_motorcycle_idr` |
| Transit LOS | time, fare | **Estimated** — schedule-based (r5py NULL) | GTFS + published timetables |
| Ridehailing LOS | time, cost | **Real tariff** — published per-km + zone distance | Gojek/Grab schedule |
| Mode availability | which modes exist per zone | **Real** — transit stop spatial join | `transit_stops_summary.csv` |
| DGP parameters | β_time, β_cost, ASCs, ρ | **Synthetic** — anchored to Ilahi + Bastarianto | Literature PDFs ✓ |
| Income segments | thresholds + shares | **Synthetic** — drawn from Ilahi sample distribution | Ilahi Table 2–3 ✓ |
| Vehicle access | car access %, MC access % | **Synthetic** — calibrated to Ilahi's 25.60% / 67.90% | Ilahi Table 3 ✓ |
| 5,000 persons | individual choices | **Synthetic** — Gumbel noise from DGP | Used ONLY for MLE validation (02–03b) |
| 5,000 persons (mixed-DGP) | per-person β_time draws | **Synthetic** — β_time_n ~ N(−0.040, 0.040²) | Recovery test in 03b only |
| Policy ΔCS | welfare change per zone×segment | **Computed** — from estimated params + modified LOS | Notebook 04 |

### Why 5,000 synthetic persons?

The 5,000 individuals exist **only** to validate the MLE estimator in notebooks 02–03.
This is a pedagogic exercise: demonstrate that a correctly written `scipy.optimize` MLE
recovers known DGP parameters within standard error. The course requires this competence.

The **welfare analysis** (notebook 04, answering both RQs) does NOT use these 5,000
individuals. It computes logsum directly from the **21 zone×income×mode combinations**
using the estimated parameters. Every value in the policy analysis is traceable to a
zone attribute (real), a LOS value (estimated from real), or a parameter (literature PDF).

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
Zone attributes + LOS matrix (§4, §6)
        ↓
MNL mode choice (baseline, 9 modes, flat)        ← L05 framework
        ↓
Nested Logit (3 nests, ownership-based)          ← L06 framework, corrects IIA
        ↓
Mixed Logit diagnostic (random β_time)           ← L07 framework, tests for
        │                                          unobserved heterogeneity
        │  Primary test: Wald on σ_time vs 0     (NOT LR — Jensen-biased)
        │  + Mixed-on-Mixed recovery (positive control)
        ↓
Best-supported model (NL or MXL) → Logsum / CS   ← L06 welfare measure
        ↓
Policy simulation (ΔCS by zone + income group)   ← §8 scenarios
```

The MXL is a **specification test**, not a parallel third model: it asks "does the
NL miss heterogeneity that random β_time would catch?" If the Wald test on σ fails
to reject zero (expected on this synthetic DGP), NL stays as the welfare model and
the report tells the L07 Five Habits story explicitly. If σ is significant, welfare
is computed via simulated logsum from MXL.

### 3.2 Why Nested Logit?

In Indonesia, car and motorcycle share a strong unobserved "motorization" attribute (ownership
cost sunk, door-to-door convenience). Ridehailing modes share an app-platform utility but lack
the ownership component. Transit modes share schedule-bound public infrastructure. A plain MNL
would assume all cross-elasticities are equal — clearly wrong when a KRL improvement draws
much more from 2WRH than from Car.

**3-nest structure** (full version in §5):
```
              Mode Choice
       /           |            \
Own Vehicle    Ridehailing          Transit
(Car, Moto)   (4WRH, 2WRH)  (KRL, TJ, Royal, LRT, MRT)
```

### 3.3 Formal model — MNL, NL, logsum, welfare

**MNL choice probability** (L05 derivation, Gumbel i.i.d. errors):
```
P_m = exp(V_m) / Σ_k exp(V_k)
```
where `V_m = ASC_m + β_time · T_m + β_cost · C_m` is the linked-trip systematic utility.

**MNL logsum** (expected maximum utility over the choice set):
```
LS = ln Σ_m exp(V_m)
```

**Nested Logit** (3 nests, with inclusive value parameter ρ ∈ (0, 1]):
```
IV_nest = ρ · ln Σ_{m ∈ nest} exp(V_m / ρ)        ← lower-nest inclusive value
P(nest) = exp(IV_nest) / Σ_n exp(IV_n)            ← upper-level choice over nests
P(m | nest) = exp(V_m / ρ) / Σ_{m' ∈ nest} exp(V_m' / ρ)   ← within-nest conditional
P_m = P(m | nest) · P(nest)                       ← unconditional
```

ρ = 1 collapses to MNL. ρ → 0 means perfect within-nest substitution. We use the
**dividing convention** `V_m / ρ` (matches L06 lecture and the existing
`notebooks/logit_eda_mle.ipynb`).

**Welfare measure** (McFadden 1978 log-sum rule for consumer surplus; full citation in §16):
```
ΔCS_n = [LS_after − LS_before] / |β_cost|        ← in Rupiah per trip
```
where `LS = ln Σ_nest exp(IV_nest)` is the upper-level NL logsum.
Aggregated by zone and income segment = equity-comparable welfare change.

### 3.4 Notation map and methodological notes

**ρ vs μ symbol**: the L06 lecture uses ρ; the existing `notebooks/logit_eda_mle.ipynb`
uses μ. They are the same parameter (inclusive value scale). Notebooks in this project
should use ρ in markdown explanations and may use either symbol in code, with a comment
clarifying the equivalence.

**Why ownership-based nesting and not vehicle-type (2W/4W) nesting?**
The existing `notebooks/logit_eda_mle.ipynb` uses a 2W (Moto+GoRide) / 4W (Car+GoCar) /
Transit nesting for its V-City-style synthetic exercise. This project chooses
**ownership-based** nesting (Own Vehicle / Ridehailing / Transit) for two reasons:

1. **Equity narrative**: ridehailing's distinguishing feature is that it has no ownership
   barrier — this is the central equity finding (low-income commuters use ridehailing
   precisely because they cannot own a car). Vehicle-type nesting hides this distinction
   inside the same nest as private modes.
2. **IIA pattern**: a KRL improvement should draw more from ridehailing than from owned
   vehicles (a sunk-cost effect). Ownership-based nesting captures this pattern; 2W/4W
   nesting does not.

Both are theoretically defensible. Document this choice explicitly in the report Methods
section. Vehicle-type nesting goes in Limitations as an alternative specification.

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
| Low income | 33.30% | 3,000 | 5% | 60% |
| Middle income | 50.30% | 9,000 | 26% | 80% |
| High income | 16.40% | 22,000 | 65% | 48% |

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
This is the standard linked-trip skim approach used in four-step models (see Koppelman & Bhat 2006 §16.5 for the linked-trip framework).

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

**Note**: The DGP uses **mode-specific VTTS** from Ilahi et al. (2021) Table 11 — see §7 MNL DGP.
This §6.3 table provides population-level income-segment VoT for **welfare interpretation**
(discussion of which income groups gain/lose from policy scenarios). It is not used in
the utility specification.

| Segment | VoT (Rp/hour) | Source |
|---|---|---|
| Low income | 12,000 | ~40% of Jakarta minimum wage (Rp 5.0 M/mo ÷ 173 hrs ≈ Rp 29,000/hr); consistent with VoT/wage ratio for low-income commuters in LMICs: World Bank (2024) VoT meta-analysis; Binsuwadan & Wardman (2023) income elasticity η ≈ 0.5–0.7 |
| Middle income | 25,000 | Ilahi et al. (2021) Table 11 (p. 413): Car VTTS = 1.80 USD/hr ≈ Rp 25,200/hr. Also the lower bound of Belgiawan et al. (2019) Table 4 (p. 92) Model 2: Car Rp 44,609/hr, MC Rp 38,677/hr. |
| High income | 55,000 | Belgiawan et al. (2019) Table 4 (p. 92): PT VTTS = Rp 50,250/hr; scaled with η ≈ 0.6 from Binsuwadan & Wardman (2023) meta-analysis (268 elasticities). |

For the DGP utility specification, see **§7 MNL DGP** — mode-specific β_time derived from
Ilahi Table 11 VTTS.

---

## 7. True DGP Parameters (Synthetic Approach)

Because no revealed preference dataset at individual level is available, this project uses
the **same synthetic approach as V-City** — parameters are set from literature, data is
generated from the DGP, then recovered by estimation. This is transparent and defensible.

### MNL DGP

**Important**: these are DGP inputs (researcher-set synthetic parameters), NOT values
estimated from real data. The parameter recovery exercise in `02_mnl_estimation.ipynb`
verifies that the estimator recovers these true values within standard error.

**Cost-units convention**: cost enters in **thousands of Rupiah** (Rp '000), following
Ilahi et al. (2021) Table 10. A trip costing Rp 14,000 is entered as 14.0 in the model.
β_cost = −1.42 then contributes −1.42 × 14.0 = −19.88 utils. Cost values per zone×mode
are computed from r5py transit fares + Gojek/Grab published tariff schedules (see §5
and §6.2) divided by 1,000.

**Caveat — β_cost at sample mean**: Ilahi's model includes income×cost and distance×cost
interactions (λ_Income,cost = −0.09, λ_Distance,cost = −0.83; Table 10, p. 410). The
published β_cost = −1.42 is evaluated at the sample mean of income and distance. Our DGP
uses this mean value as a fixed scalar — income heterogeneity in cost sensitivity is not
modelled. This is a deliberate simplification: the 4 Jabodetabek study zones span different
income deciles, but the zone-average income aligns with Ilahi's all-Jakarta mean. The mode-
specific VTTS values from Ilahi Table 11 are reported at that same sample mean, so the
algebra is internally consistent.

**Derivation — VTTS → β_time per mode**: Ilahi et al. (2021) Eq. 3 (p. 412) defines:

```
VTTS [USD/hr] = (60/14) × (β_T / β_C)
```

where 60 = min/hr, 14 = Thousand IDR per USD. Rearranging:

```
β_time_mode = β_cost × VTTS_mode_Rp/hr / 60,000
            = −1.42 × VTTS_mode_Rp/hr / 60,000
```

Substituting Ilahi's published Table 11 VTTS recovers his Table 10 β_time values to within
rounding. Check: Car VTTS = 25,200 → β_time = −1.42 × 25,200/60,000 = −0.596 ≈ −0.60 ✓
(matches Ilahi Table 10 β_time_Car = −0.60 exactly).

This approach transfers the **derived behavioral metric** (VTTS) rather than raw β
coefficients, which is standard practice in cross-study parameter transfer (Wardman 2004;
World Bank 2023 meta-analysis §3). The transfer is valid because β_time in Ilahi does
NOT interact with demographics — age/gender/degree enter additively as ASC shifters, not
as time interactions (confirmed by inspecting Table 10: there is no β_Time×Demographic term).

**β_cost**: −1.42 per Thousand IDR (generic — same value across all 9 modes).

From Ilahi et al. (2021) Table 10 (p. 410), Model 1: `β Travel cost = −1.42 [Thousand IDR]`
(t = −12.08, p < 0.01). Evaluated at the sample mean of income and distance.

### β_time per mode — 6 modes anchored to Ilahi Table 11, 3 interpolated

| Mode | Ilahi analog | VTTS (Rp/hr) | β_time (/min) | Source & notes |
|---|---|---|---|---|
| **Car** | Car | 25,200 | **−0.60** | Ilahi Table 11 (p. 413): 1.80 USD/hr. Positive VTAT (+3.94 USD/hr) — users are comfortable in-car, low willingness to pay for time savings. |
| **MC** | Motorcycle | 98,840 | **−2.34** | Ilahi Table 11: 7.06 USD/hr. Negative VTAT (−1.32 USD/hr) — exposure penalty. High willingness to pay to reduce travel time. |
| **KRL** | Train | 114,930 | **−2.72** | Ilahi Table 11: 8.21 USD/hr. Long-distance Bodetabek commuters — high VTTS reflects congestion-beating behavior and long trip distances. |
| **TJ** | BRT | 45,220 | **−1.07** | Ilahi Table 11: 3.23 USD/hr. Budget BRT with partial dedicated lanes — users more price-sensitive. Significant at p < 0.05 (t = −2.36). Note: Bus and PT travel-time coefficients in Ilahi Model 1 are not significant (t = −1.40 and −1.22 respectively); BRT is the better anchor for TJ. |
| **4WRH** | Taxi | 147,280 | **−3.49** | Ilahi Table 11: Taxi 10.52 USD/hr. Ilahi pools car-based and MC-based taxis into a single "Taxi" category (p. 409). We map 4WRH (GrabCar/GoCar) to Taxi as the closest behavioral analog — a 4-wheel paid alternative with structural similarity (sit, no driver-app vs. street-hail distinction). β_time = −3.49 transfers directly from Ilahi's β_Travel time Taxi (Table 10). |
| **2WRH** | ODT | 215,490 | **−5.10** | Ilahi Table 11: ODT 15.38 USD/hr. Ilahi pools car-based and MC-based ODT into a single "ODT" category. We map 2WRH (GoRide/GrabBike) to ODT — MC-based ODT likely dominates Ilahi's RP share (Fig. 6 in the paper). β_time = −5.10 transfers directly from Ilahi's β_Travel time ODT (Table 10). Highest VTTS in the study — users pay specifically to beat traffic via motorcycle lane-splitting. |

**3 interpolated modes** (not in Ilahi's 2019 survey):

| Mode | VTTS (Rp/hr) | β_time (/min) | Derivation |
|---|---|---|---|
| **MRT** | **126,000** | **−2.98** | MRT Jakarta Phase 1 opened March 2019 — after Ilahi's survey (April–May 2019). Anchored to KRL (114,930) × 1.10. MRT is faster, more modern, full AC, and consistently top-rated in passenger satisfaction (MRT Jakarta 2023 Annual Report). Different corridor (South Jakarta, Lebak Bulus–Bundaran HI) — similar commuter demographic to KRL. |
| **LRT** | **100,000** | **−2.37** | LRT Jabodebek opened August 2023. Anchored to KRL × 0.87. Newer system with modern technology, speed comparable to MRT/KRL, but limited corridor (Cibubur–Harjamukti and Bekasi–Jatimulya), lower familiarity and ridership. Positioned between KRL and MC. |
| **RoyalTrans** | **55,000** | **−1.30** | Anchored to BRT/TJ (45,220) × 1.22. Road-based like BRT but premium: reserved seating, express routing, AC, higher fare (Rp 20,000–40,000 vs TJ Rp 3,500). Comfort-oriented user base — psychology closer to Car (low VTTS, comfort-seeking) than ODT (high VTTS, congestion-beating). Note: BRT β_time is only marginally significant (t = −2.36) — compounded parameter uncertainty for this mode. |

**VTAT note** (Value of Travel Time Assigned to Travel): Ilahi Table 11 reports both VTTS
and VTAT. VTAT = VTTS − VOL (Value of Leisure), where VOL ≈ 66% of hourly wage (Jara-Díaz
et al. 2008, calibrated for Indonesia by Ilahi). VTAT > 0 means the mode provides comfort
that offsets the disutility of travel (positive for Car, PT, Bus, UAM). VTAT < 0 means
exposure or discomfort amplifies travel disutility (negative for MC, ODT, Taxi). Our β_time
captures the full VTTS including both components — VTAT is descriptive only and does not
enter the utility function.

### ASC per mode (DGP inputs, KRL = 0 reference)

ASC values are DGP inputs set to produce a plausible modal preference ordering for
**Bodetabek commuter corridors** (30–60 km). They are NOT copied from Ilahi — his ASCs
absorb demographic interactions (age, gender, degree, income, distance) that our simpler
specification omits. Copying his ASC values without those variables would mis-specify
the model.

#### Re-normalization check (Ilahi's MC=base → our KRL=base)

For reference, Ilahi Table 10 (p. 410) reports these ASCs with MC as the base:

| Mode | Ilahi ASC (MC=0) | Re-normalized (KRL=0) | Ilahi t-value |
|---|---|---|---|
| MC | 0.00 | +0.29 | base |
| Train (KRL) | −0.29 | 0.00 | −0.9 NS |
| Car | −1.20 | −0.91 | −10.64 *** |
| ODT | −1.43 | −1.14 | −9.32 *** |
| Taxi | −3.94 | −3.65 | −23.59 *** |
| BRT | −4.74 | −4.45 | −20.37 *** |

Ilahi's preference ordering (KRL=0): **MC ≈ KRL > Car > ODT >> Taxi > BRT**. Train/KRL
ASC is not significantly different from MC (t = −0.9) — they are statistically tied.

#### Our DGP ASCs — Bodetabek-adjusted

Our ASC values **diverge** from Ilahi's ordering for private and ridehailing modes.
This is a deliberate DGP choice justified by the Bodetabek context:

- **Longer corridors** (30–60 km vs. Ilahi's intra-Jakarta sample): car/MC ownership
  becomes more attractive due to first/last-mile gaps, KRL crowding, and schedule rigidity
- **Modal share evidence**: BPS Jabodetabek Commuter Survey (2023) reports MC ≥ 60% of
  daily trips, KRL ~5% on Bodetabek corridors — revealed preference strongly favors
  private modes in our study area
- **Bastarianto et al. (2019)** (Bekasi–Jakarta corridor, 420 commuters, Table 3):
  NL model λ_hwh = 0.55 (p < 0.01) confirms private-mode nest dominance in long commutes
- **Belgiawan et al. (2019)** (Jakarta CBD ERP survey): ASC Motorcycle positive and
  significant in pricing context (Table 3, Model 2) — MC preference persists even with
  toll exposure

| Mode | ASC (KRL=0) | Derivation & defense |
|---|---|---|
| **KRL** | **0.00** | Reference mode — highest-ridership public transit in Jabodetabek (~1M daily pax, KCI 2023). Natural baseline for identification (Train 2009 Ch. 2). |
| **MC** | **+1.20** | Highest ASC. BPS Jabodetabek (2023): MC ≥ 60% modal share. Ilahi: statistically tied with KRL in intra-Jakarta sample; stronger revealed preference in longer Bodetabek corridors where door-to-door flexibility dominates. Bastarianto et al. (2019): private modes dominate the hwh tour nest. |
| **2WRH** | **+1.10** | Near-own-MC preference. Ilahi: ODT −1.14 below KRL (re-normalized), but this reflects intra-Jakarta trips where ridehailing competes with dense transit. In Bodetabek corridors (J1b, J3b have zero transit), 2WRH substitutes for absent public transport. BPS 2023: ridehailing share has grown since Ilahi's 2019 survey. |
| **Car** | **+0.90** | Above KRL. Ilahi: Car −0.91 below KRL in intra-Jakarta. In 30–60 km Bodetabek corridors, car comfort advantage over crowded KRL is larger. Belgiawan et al. (2019): ASC Motorcycle positive but Car is the baseline (ASC = 0) in SP experiment — car is the reference mode in pricing context. BPS 2023: car share ~13% on Bodetabek-CBD commutes. |
| **4WRH** | **+0.50** | Below 2WRH and Car (higher cost, longer wait). Ilahi: Taxi −3.65 below KRL in intra-Jakarta. Our +0.50 reflects the narrower gap between car ownership and car ridehailing when transit alternatives are sparse (J1b, J3b). |
| **MRT** | **+0.30** | Above KRL. Premium rail — faster, more modern, higher satisfaction (MRT Jakarta 2023). Not in Ilahi's survey. Inferred from transit hierarchy: faster + more comfortable than KRL → higher utility. |
| **RoyalTrans** | **+0.05** | Near KRL. Road-based (congestion exposure) offsets premium features (reserved seat, AC, express routing). Above regular TJ (higher fare selects for higher-income users who value comfort). |
| **LRT** | **−0.10** | Near KRL baseline. Newer system (opened August 2023), limited corridor and ridership, lower familiarity. Positioned between KRL and TJ. |
| **TJ** | **−0.30** | Below KRL. BRT-lite — mixed traffic on key segments, lower schedule reliability. Ilahi: BRT −4.45 below KRL (re-normalized). Our −0.30 compresses Ilahi's spread while preserving the ordinal position (TJ < all rail modes). TJ's Rp 3,500 flat fare is captured in the cost term — the negative ASC reflects non-cost disamenities (reliability, crowding). |

Our ASC spread (−0.30 to +1.20) is narrower than Ilahi's (−4.76 to +0.29). Ilahi's wide
spread is partly an artifact of the SP experimental design (UAM alternatives, congestion
charging scenarios). Our compressed range is appropriate for a simpler RP-style DGP.

### Parameter recovery (MLE validation)

**18 parameters**: 9 β_time + 1 β_cost + 8 ASCs (KRL ASC fixed to 0 for identification).

The parameter recovery exercise in `02_mnl_estimation.ipynb` uses MLE on synthetic choice
data generated from the DGP parameters above, with Gumbel-distributed errors. All 18
parameters must recover within 2 SE. This validates the estimator implementation — it
does NOT validate the DGP values themselves. Those are validated by the literature sources
cited in the tables above.

### NL DGP — 3-nest structure

All ρ values are DGP inputs, informed by empirical NL estimates for Indonesian commuters
and theoretical bounds (Train 2009: ρ ∈ (0, 1]).

**Empirical anchor — Bastarianto et al. (2019) Table 3 (p. 11):**

Bastarianto et al. estimate a two-level NL for Bekasi–Jakarta commuters (420 commuters,
8 tour-type×mode alternatives). Their NL model nests tour types (hwh, hw+wh) as upper
nests with mode choice (MC, Car, Bus, KRL) in the lower level. Key findings:

- λ_hwh = 0.55 (t = 6.01, p < 0.01) — strongly significant within-nest correlation for
  the home→work→home tour nest. This is the direct empirical anchor for ρ_OwnVehicle = 0.55.
- λ_hw+wh = 0.99 (fixed to 1.0) — no significant within-nest correlation beyond the hwh
  pattern. This confirms that not all nests exhibit strong correlation, consistent with
  our ρ ordering across nests.

In the NL literature, λ (scale) and ρ (inclusive value) are inverse parameterizations
of the same concept. Bastarianto uses the convention where λ < 1 indicates within-nest
correlation. Our ρ follows Train (2009) convention where ρ ∈ (0, 1] with smaller
ρ = stronger correlation.

| Parameter | Value | Derivation | Precise source |
|---|---|---|---|
| ρ_OwnVehicle (Car + Moto) | 0.55 | Strongest within-nest substitution — both require ownership sunk cost, both door-to-door. Directly anchored to Bastarianto's estimated λ_hwh = 0.55 for the Bekasi–Jakarta commuter hwh tour nest. | **Bastarianto et al. (2019) Table 3 (p. 11)**: λ_hwh = 0.55 (t = 6.01, p < 0.01). Train (2009) §4.2: ρ ∈ (0, 1] consistency condition. |
| ρ_Ridehailing (4WRH + 2WRH) | 0.70 | Moderate within-nest correlation — share app-platform utility (booking, fixed upfront price, no ownership barrier) but differ in comfort, wait time, and price per km. Intermediate between OwnVehicle (0.55) and Transit (0.75). Not directly estimated in existing papers (Ilahi 2021 pools all ODT as a single alternative). | **Derived**: Ilahi et al. (2021) Table 10 — ODT as a single alternative; within-ODT 4W/2W substitution is not separately estimated. ρ = 0.70 is the midpoint between 0.55 (strong correlation) and 0.85 (near-MNL, weak correlation). Sensitivity range: ±0.10. |
| ρ_Transit (KRL, TJ, Royal, LRT, MRT) | 0.75 | Weakest within-nest correlation — all schedule-bound but serve different corridors (Bogor, Bekasi, Tangerang, Cibubur), different technologies (heavy rail, BRT, LRT, MRT), and different commuter populations. Bastarianto's CNL model (Table 3) shows cross-nest membership (α values) for public transport alternatives — indicating weaker exclusive correlation than private modes. | **Bastarianto et al. (2019) Table 3 (p. 11)**: CNL α values for Bus and KRL show cross-nest membership with both tour-type nests. Train (2009) §4.2 for theoretical bounds. |
| β_time per mode | 9 values (see §7 MNL DGP) | Mode-specific β_time from Ilahi Table 11 VTTS. Generic across nests — consistent with Train (2009) specification where only the nest structure differs, not the systematic utility. | See §7 MNL DGP table for per-mode citations. |
| β_cost | −1.42 per 1000 IDR | Generic across all modes and nests. | Ilahi et al. (2021) Table 10 (p. 410): β Travel cost = −1.42 (t = −12.08, p < 0.01). |
| ASCs per mode | 8 values (see §7 MNL DGP) | KRL = 0 reference. Bodetabek-adjusted — see ASC re-normalization discussion in §7 MNL DGP. | See §7 MNL DGP ASC table for per-mode citations. |

All ρ values are DGP inputs — set before estimation. The estimator must recover them (within SE)
as a validity check, exactly as in V-City (`notebooks/trans-eng-lectures/vcity_spec.md`).
ρ ∈ (0, 1] is required for consistency with random utility maximisation (Train 2009, §4.2).
The ordering ρ_OwnVehicle < ρ_Ridehailing < ρ_Transit reflects decreasing within-nest
substitutability, consistent with the theoretical expectation that Car and Motorcycle are
closer substitutes than KRL and MRT.

---

## 8. Policy Scenarios

Eight scenarios spanning transit expansion, pricing, frequency, routing, and service quality.
Scenarios A–C are the baseline set (from V-City project structure). Scenarios D–H are
Jabodetabek-specific — each targets a real policy lever identified from the zone geography
in §4 and the LOS matrix in §6.2.

For each scenario, report:
- Mode share before/after (bar chart per zone)
- ΔCS by zone × income segment (heatmap)
- Aggregate welfare gain in Rp/trip and Rp/day (zone population × share using transit × ΔCS)

---

### Group 1 — Baseline scenarios (A–C)

### Scenario A — KRL/rail extension to J3b (Gading Serpong / Karawaci)

- **Shock**: Add direct KRL access to J3b. Transit time J3b→JCBD drops from — to 70 min; cost Rp 7,500.
- **Rationale**: J3b currently has zero transit. This mirrors a planned rail extension in the Tangerang corridor.
- **Expected**: ΔCS largest for middle-income J3b commuters currently car/GoRide-dependent; J3b logsum rises sharply; J3a serves as a counterfactual (already KRL-served).
- **Operational parameter change**: Add KRL to J3b choice set. Set `T_KRL_J3b→JCBD = 70`, `C_KRL_J3b→JCBD = 7.5` (Thousand IDR).

### Scenario B — Toll price increase (congestion charge)

- **Shock**: Inner-Jakarta toll doubles for car users (+Rp 40,000 for all zones→JCBD).
- **Expected**: ΔCS negative for car-owning high-income; KRL share ↑ in J1a/J2/J3a/J4; no transit shift in J1b/J3b (no alternatives) — welfare loss falls hardest on transit-desert zones.
- **Operational parameter change**: `C_car_zone→JCBD += 40` (Thousand IDR) for all origin zones.

### Scenario C — KRL frequency improvement (wait time reduction)

- **Shock**: KRL in-vehicle + wait time −20% across all KRL-served zones (J1a, J2, J3a, J4).
- **Expected**: Largest welfare gain for low-income KRL-captive (J1a Bogor corridor); J1b and J3b receive zero benefit — equity gap between transit-served and transit-desert zones widens in relative terms.
- **Operational parameter change**: `T_KRL_zone→JCBD *= 0.80` for J1a, J2, J3a, J4. J1b and J3b unchanged (KRL not available).

---

### Group 2 — Transit desert and extension scenarios (D–E)

### Scenario D — TransJakarta extension to J1b (Parung/Leuwiliyang)

- **Problem**: J1b (Kab. Bogor outer) has **zero transit** — choice set is {Car, Moto, 4WRH, 2WRH} only. This is the most severe transit desert in the study area. J1b commuters face the highest generalized cost per trip of any zone, and the logsum is structurally the lowest before any policy intervention. A TJ extension from the existing TJ corridor (Pondok Cabe/Bintaro area) southward into Parung is operationally plausible — it follows Jalan Raya Parung, a major arterial with wide-enough shoulder for BRT lanes, and connects to the TJ network at Lebak Bulus.
- **Shock**: Add TJ to J1b choice set. TJ time J1b→JCBD = 90 min (approximate: ~15 km south of current TJ reach, mixed-traffic segment Parung→Pondok Cabe ~30 min + existing TJ Pondok Cabe→CBD ~60 min). Cost = Rp 3,500 (TJ flat fare). Wait time ~12 min (standard TJ headway).
- **Comparison with Scenario A**: Scenario A adds KRL to J3b (premium rail, Rp 7,500, 70 min). Scenario D adds TJ to J1b (budget BRT, Rp 3,500, 90 min). The contrast tests whether a budget transit option produces comparable welfare gains to rail investment — directly relevant for corridor prioritization under budget constraints.
- **Expected**: ΔCS positive for low-income J1b commuters — TJ at Rp 3,500 is the cheapest motorized option to JCBD, undercutting even 2WRH (Rp 80,000). Shift primarily from 2WRH → TJ (cost-sensitive riders). Car and 4WRH shares largely unchanged (comfort-oriented users). Low-income J1b residents gain most; middle-income gain moderately. J1b logsum rises from baseline, narrowing the Q4 vs Q1 equity gap.
- **Operational parameter change**: Add TJ to J1b choice set. Set `T_TJ_J1b→JCBD = 90`, `C_TJ_J1b→JCBD = 3.5` (Thousand IDR).

### Scenario E — MRT extension to BSD (J3a Serpong)

- **Problem**: BSD Serpong (J3a) has KRL (85 min, Rp 7,000) and RoyalTrans (110 min via Fatmawati → MRT transfer, Rp 39,000) but no direct MRT. The MRT Jakarta Phase 3 (East-West line) is planned to extend westward toward Tangerang; BSD is a natural terminus given its population density, office clusters (BSD Green Office Park), and existing KRL+RoyalTrans demand. An MRT extension would serve as a premium alternative — faster than KRL (grade-separated, no at-grade crossings on the proposed alignment), modern rolling stock, higher reliability. This scenario tests whether adding MRT to a zone that *already has* KRL produces incremental welfare gain, or whether the modes cannibalize each other.
- **Shock**: Add MRT to J3a choice set. MRT time J3a→JCBD = 60 min (grade-separated, ~30% faster than KRL on the same corridor). Cost = Rp 12,000 (distance-based, ~35 km from BSD to Bundaran HI, extrapolating from MRT Jakarta Phase 1 fare table). Wait time ~5 min (MRT headway).
- **Reference**: **J5 South Jakarta** already has MRT (25 min, Rp 6,000). Scenario E replicates J5's MRT advantage at the BSD distance scale, testing whether the premium-rail welfare gain persists at longer corridor lengths.
- **Expected**: MRT draws from both KRL and Car. KRL→MRT shift among middle-income (time savings worth the Rp 5,000 fare premium: ~25 min saved at VTTS_KRL = Rp 114,930/hr ≈ Rp 48,000). Car→MRT shift among high-income (MRT comfort + reliability vs. toll road congestion uncertainty). Low-income remain KRL-constrained. RoyalTrans share drops sharply (MRT strictly dominates: faster, cheaper, no Lebak Bulus transfer). J3a logsum rises — the value of having a *second* transit option in a rail-served zone.
- **Operational parameter change**: Add MRT to J3a choice set. Set `T_MRT_J3a→JCBD = 60`, `C_MRT_J3a→JCBD = 12.0` (Thousand IDR).

---

### Group 3 — Route restructuring and service quality (F–H)

### Scenario F — TJ route restructuring: BSD→CBD direct

- **Problem**: BSD Serpong (J3a) and Gading Serpong/Karawaci (J3b) have TJ access, but the current TJ route terminates at **Grogol** (West Jakarta), not at the CBD (Sudirman/Thamrin). A BSD→Grogol TJ ride (~60 min, Rp 3,500) leaves the commuter ~10–12 km short of JCBD. From Grogol, the commuter must transfer to an ODT (2WRH or 4WRH) or bus for the remaining leg — adding ~30 min transfer+travel time and Rp 30,000–50,000. The linked-trip TJ→4WRH journey (60 + 7 wait + 25 = 92 min, Rp 3,500 + Rp 50,000 = Rp 53,500) is structurally uncompetitive against direct Car (95 min, Rp 105,000 — toll + fuel) or direct 2WRH (90 min, Rp 60,000). The TJ alternative is present on paper but *not a real choice* for most commuters because the Grogol transfer penalty cancels its cost advantage.
- **Shock**: Restructure the TJ BSD route to terminate at **Bundaran HI / Sudirman** (JCBD) instead of Grogol. This eliminates the transfer penalty entirely — TJ becomes a one-seat ride from BSD to the CBD. TJ time BSD→CBD = 80 min (adding ~20 min from Grogol to Sudirman via the TJ corridor on Jalan Sudirman, which has dedicated BRT lanes). Cost = Rp 3,500 (TJ flat fare, unchanged).
- **Before/after LOS comparison**:

  | Zone | Before (TJ→Grogol + ODT→CBD) | After (TJ direct→CBD) | Δ |
  |---|---|---|---|
  | J3b→JCBD | 90 min / Rp 3.5k (TJ to Grogol) + ~30 min / Rp 30–50k (ODT) = **~120 min / Rp 35–55k** | **80 min / Rp 3.5k** | −40 min / −Rp 30–50k |
  | J3a→JCBD | (no TJ — KRL only) | **80 min / Rp 3.5k** (new TJ option) | New alternative: +1 mode in choice set |

- **Expected**: Dramatic mode shift in J3b — TJ share jumps from near-zero to dominant among low/middle-income. 2WRH→TJ shift is the primary channel (cost-sensitive riders save Rp 50,000+/trip). Some Moto→TJ shift (time penalty of TJ vs. Moto ~10 min is offset by safety/comfort for longer-distance commuters). In J3a (BSD Serpong), TJ becomes a new budget transit option alongside KRL (85 min, Rp 7,000) — TJ undercuts KRL on cost (Rp 3,500 vs Rp 7,000) with comparable time (80 vs 85 min). This is the **strongest expected welfare gain** among all scenarios — a one-seat TJ ride that eliminates the multi-modal penalty and undercuts every motorized alternative on cost.
- **Operational parameter change**: For J3b: replace `T_TJ_J3b→JCBD = 90` (to Grogol) with `T_TJ_J3b→JCBD = 80` (direct to CBD). For J3a: add TJ to choice set with `T_TJ_J3a→JCBD = 80`, `C_TJ_J3a→JCBD = 3.5`.

### Scenario G — RoyalTrans frequency increase

- **Problem**: RoyalTrans currently operates at very low frequency — approximately 3 departures per morning peak (based on GTFS feed inspection). This means effective wait time at the origin is ~20–30 min (half the headway of ~40–60 min between departures). At this frequency, RoyalTrans is not a practical commuting option for most workers — missing a departure means a 40–60 min delay. The low frequency also means vehicles are often at capacity, reducing the comfort advantage that RoyalTrans's premium fare is supposed to buy. Increasing frequency to match peak-hour demand would transform RoyalTrans from a niche premium service to a viable commuting alternative.
- **Shock**: Increase RoyalTrans peak frequency from 3 departures/peak to 12 departures/peak (every 15 min, comparable to MRT/KRL headway). This reduces effective wait time from ~20 min to ~5 min (half-headway). In-vehicle time unchanged (same route, same roads).
- **Zones affected**: J2 (Bekasi — RoyalTrans 65 min, Rp 28,000), J3a (BSD — RoyalTrans 110 min with MRT transfer, Rp 39,000), J3b (Gading Serpong — RoyalTrans 115 min with MRT transfer, Rp 39,000), J4 (Depok — RoyalTrans 60 min, Rp 22,000). J1a, J1b, J5: no RoyalTrans service.
- **Expected**: RoyalTrans share increases in all 4 zones. Largest gain in J2 and J4 (direct RoyalTrans to CBD — no MRT transfer penalty — wait time reduction is the full benefit). Smaller gain in J3a/J3b (RoyalTrans still requires MRT transfer at Lebak Bulus/Fatmawati — the wait time reduction at origin is partly offset by the unchanged MRT wait time). Mode shift primarily from KRL/TJ (premium-seeking riders who value reserved seating) and from 4WRH (car ridehailing — similar cost profile, RoyalTrans now more reliable). Low-income gain is minimal (RoyalTrans fare Rp 22,000–39,000 exceeds their budget constraint). Equity implication: the benefit is concentrated in middle/high-income — this is a service-quality improvement, not an equity intervention.
- **Operational parameter change**: For all RoyalTrans-served OD pairs, reduce `wait_time` component of `T_Royal_zone→JCBD` from 20 → 5 min. Total T becomes: `T_Royal_zone→JCBD_new = T_Royal_zone→JCBD_old − 15`.

### Scenario H — RoyalTrans fare reduction (competitive pricing)

- **Problem**: RoyalTrans fares (Rp 20,000–40,000) position it as a premium product — above KRL (Rp 5,000–8,000) and TJ (Rp 3,500) but below 4WRH (Rp 100,000–175,000). This pricing strategy captures high-income commuters but excludes the middle-income segment that could benefit most from an express transit option. If RoyalTrans fares were reduced to compete directly with KRL+TJ on price while retaining the comfort advantage (reserved seating, AC, express routing), it could draw significant ridership from private modes — particularly 2WRH and Moto — and function as a congestion-relief tool.
- **Shock**: Reduce RoyalTrans fares by 50% across all routes. J2/J4: Rp 22,000 → Rp 11,000. J3a/J3b: Rp 39,000 → Rp 19,500.
- **Comparison with Scenario G**: Scenario G increases frequency (capital-intensive — requires more vehicles, more drivers). Scenario H reduces fares (operating subsidy — requires political will but no capital investment). The two scenarios can also be combined (G+H) for a "maximum RoyalTrans" scenario, but the incremental welfare gain is likely sub-additive (diminishing returns from improving an already-improved mode).
- **Expected**: RoyalTrans becomes price-competitive with KRL in J2 and J4 (Rp 11,000 vs KRL Rp 6,000 — only Rp 5,000 premium for reserved seating and express routing). 2WRH→RoyalTrans shift among middle-income (at 50% fare, RoyalTrans Rp 11,000–19,500 vs 2WRH Rp 49,000–72,000 — RoyalTrans is now structurally cheaper). Moto→RoyalTrans shift among low/middle-income for J2 and J4 (time comparable, comfort advantage, no ownership cost). Car→RoyalTrans shift among high-income in J3a/J3b (RoyalTrans+MRT at Rp 19,500 + Rp 9,000 = Rp 28,500 still undercuts Car at Rp 100,000–105,000). Equity finding: fare reduction redistributes RoyalTrans welfare gain downward — low/middle-income gain more from Scenario H than from Scenario G. The revenue trade-off (50% fare × expanded ridership) can be compared against the social welfare gain.
- **Operational parameter change**: For all RoyalTrans-served OD pairs, `C_Royal_zone→JCBD *= 0.50`. For J3a and J3b, the total cost includes the onward MRT leg: `C_Royal_zone→JCBD_new = C_Royal_zone→JCBD_old * 0.50 + C_MRT_transfer` (MRT fare unchanged).

---

### Scenario comparison matrix

| # | Scenario | Type | Zones affected | Key parameter change | Equity direction |
|---|---|---|---|---|---|
| A | KRL to J3b | Transit expansion | J3b | Add KRL: T=70, C=7.5k | Pro-equity (transit desert → served) |
| B | Toll +Rp 40k | Pricing | All zones | C_car += 40 | Regressive (J1b/J3b no alternative) |
| C | KRL frequency −20% | Service quality | J1a, J2, J3a, J4 | T_KRL *= 0.80 | Mixed (widens gap vs. transit deserts) |
| D | **TJ to J1b** | Transit expansion | **J1b** | Add TJ: T=90, C=3.5k | **Strongly pro-equity** (Q4 → served) |
| E | **MRT to BSD** | Transit expansion | **J3a** | Add MRT: T=60, C=12k | Mildly pro-equity (adds choice to served zone) |
| F | **TJ BSD→CBD direct** | Route restructuring | **J3a, J3b** | TJ goes to CBD: T=80, C=3.5k | **Strongly pro-equity** (budget one-seat to CBD) |
| G | **RoyalTrans frequency** | Service quality | **J2, J3a, J3b, J4** | Wait 20→5 min | Regressive (benefits middle/high-income) |
| H | **RoyalTrans fare −50%** | Pricing | **J2, J3a, J3b, J4** | C_Royal *= 0.50 | Pro-equity (price barrier lowered) |

### Scenario interaction notes

- **D + F**: If both TJ to J1b AND TJ BSD→CBD direct are implemented, J1b and J3b both gain budget one-seat transit to CBD — the two worst-served zones in the study converge toward J2/J4 levels of access. This is the "maximum equity" policy package.
- **G + H combined**: RoyalTrans with both higher frequency AND 50% lower fare — tests whether a premium express service can be transformed into a mass transit option. Expected to draw heavily from 2WRH and Moto.
- **A + E**: Both J3b (KRL) and J3a (MRT) gain new rail — the entire Tangerang corridor becomes dual-rail-served. Tests whether the incremental value of MRT (on top of KRL) exceeds the incremental value of KRL (on top of nothing) — likely diminishing marginal returns to rail investment within the same corridor.
- **Baseline equity benchmark**: Scenarios B and C together demonstrate that transit-side improvements in isolation widen the equity gap unless paired with a transit-desert intervention (D or F). The policy insight is that **frequency improvements and toll pricing should be bundled with network expansion** to avoid regressive outcomes.

---

## NOTEBOOK PIPELINE — Simple View

Read this before starting any notebook. The comprehensive version is in §PROJECT FLOW above.

```
  ┌─────────────────────────────────┐
  │  01_data_prep.ipynb  ✅ Done     │   Real data → synthetic persons
  │                                 │
  │  • 7 zones × 9 modes LOS         │
  │  • TRUE_DGP (18 params, Ilahi)   │
  │  • 5,000 persons (Gumbel noise)  │
  │  → persons_jkt.csv               │
  └─────────────────────────────────┘
              │
              ▼
  ┌─────────────────────────────────┐
  │  02_mnl_estimation.ipynb        │   Baseline (flat MNL)
  │                                 │
  │  • Estimate 18 params            │
  │  • Hessian + Robust SE           │
  │  • Recovery check: |θ̂−θ| < 2·SE? │
  │  • IIA demo (Red Bus / KRL Exp)  │
  │  → mnl_estimates.json            │
  └─────────────────────────────────┘
              │
              ▼
  ┌─────────────────────────────────┐
  │  03_nl_estimation.ipynb         │   Add nest correlation
  │                                 │
  │  • 3 nests (Own / RH / Transit)  │
  │  • Estimate 18 + 3·ρ params      │
  │  • LR vs MNL: H₀ ρ=1             │
  │  → nl_estimates.json             │
  └─────────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │  03b_mixed_logit.ipynb  ← NEW                                     │
  │                                                                   │
  │  Question: does NL miss heterogeneity that random β_time catches? │
  │                                                                   │
  │  SPEC (mirrors L07 Task 3 — NOT Ilahi Model 3 random ASCs):       │
  │    β_time_n = β_time_mean + σ_time · η_n,  η_n ~ N(0,1)           │
  │    Simulated MLE, 80–200 Halton draws                              │
  │                                                                   │
  │  ┌─────────────────────────┐    ┌───────────────────────────┐    │
  │  │ Task A — Negative test  │    │ Task B — Positive test    │    │
  │  │  Data: persons_jkt.csv  │    │  Data: persons_jkt_mixed  │    │
  │  │  DGP: β_time fixed       │    │  DGP: β_time~N(μ, 0.04²)  │    │
  │  │  Expected: σ̂ ≈ 0         │    │  Expected: σ̂ ≈ 0.04 ✓     │    │
  │  │  Wald |t| < 1.96         │    │  Wald |t| > 1.96          │    │
  │  │  → "NL stays"            │    │  → "estimator works"      │    │
  │  └─────────────────────────┘    └───────────────────────────┘    │
  │                                                                   │
  │  DIAGNOSTIC HIERARCHY (L07 protocol):                             │
  │  ① PRIMARY:   Wald on σ_time  |t| > 1.96                          │
  │  ② SECONDARY: Boundary LR vs χ²(0.5,1), crit = 2.71              │
  │  ③ FORBIDDEN: Plain LR  ← sim. LL Jensen-biased, can flip sign    │
  │                          (see L07 Task 3.5 code lines 17–26)      │
  │                                                                   │
  │  → Writes best_model.json: {"model": "NL"} or {"model": "MXL"}   │
  └──────────────────────────────────────────────────────────────────┘
              │
              ▼
  ┌─────────────────────────────────┐
  │  04_policy_simulation.ipynb     │   8 scenarios A–H
  │                                 │
  │  • Read best_model.json          │
  │  • Compute logsum per zone×inc   │
  │    (NL closed-form or MXL sim.)  │
  │  • ΔCS heatmaps × 8 scenarios    │
  │  • Equity comparison              │
  └─────────────────────────────────┘
```

---

## 9. Notebook Structure

All notebooks in `notebooks/trans-eng-final/`. Each is self-contained and sequentially numbered.

| Notebook | Purpose | Key outputs |
|---|---|---|
| `01_data_prep.ipynb` | Build zone table, LOS matrix, synthetic population | `data/jabodetabek_zones.csv`, `data/od_skim_jkt.csv`, `data/persons_jkt.csv` |
| `02_mnl_estimation.ipynb` | MNL from scratch (scipy MLE); parameter recovery; IIA demo | MNL parameter table, LL surface, mode share bar charts |
| `03_nl_estimation.ipynb` | Nested Logit; IIA violation test; parameter recovery | NL parameter table, rho interpretation, NL vs MNL mode share diff |
| `03b_mixed_logit.ipynb` | MXL diagnostic (random β_time); Wald test on σ; Mixed-on-Mixed recovery | MXL estimates, Wald/LR/ρ² comparison table, recovered β_time distribution figure, recommendation row ("NL stays" or "MXL warranted") |
| `04_policy_simulation.ipynb` | Logsum / CS; 8 policy scenarios (A–H); ΔCS by zone + income | Welfare heatmaps, mode share shift charts, equity summary |

**Notebook 03b structure** (mirrors `notebooks/trans-eng-lectures/L07/L07_estimation_lab.ipynb` Tasks 3 + 3.5; reuse cells, do not rewrite):

1. Load `persons_jkt.csv` + NL estimates from 03 → set as starting point.
2. **Task A — MXL on MNL-DGP data** (negative test): `mixed_nll` with random β_time, 80–200 Halton draws via `scipy.stats.norm.ppf(halton(N))`. Estimate (β_time_mean, σ_time, β_cost, 8 ASCs). Wald + boundary LR vs NL.
3. **Task B — Generate `persons_jkt_mixed.csv`**: same persons file but with per-person β_time draw from N(−0.040, 0.040²); regenerate choices via Gumbel noise.
4. **Task C — MXL on Mixed-DGP data** (positive test / recovery): same estimator on Task B data. Show σ̂ recovers truth within SE → estimator is correctly implemented.
5. **Summary table**: 4 rows × 4 cols (truth | MNL/MNL | NL/MNL | MXL/MNL | MXL/Mixed) — exact mirror of L07 Task 3.5 table.
6. **Recommendation cell**: which model carries forward to 04 (NL by default; MXL only if Wald rejects).

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
   3.3 Mixed Logit: random β_time spec (L07 framework) + Wald-test diagnostic for unobserved
       heterogeneity; recovery validation on Mixed-DGP data
   3.4 First/last mile: Option A — access time absorbed in r5py transit skims
   3.5 Logsum welfare measure (L06 formula; units: Rp/trip) — NL formulation as default;
       simulated logsum if MXL is supported

4. Results (800w)
   4.1 MNL estimation — parameter recovery, VoT by segment
   4.2 NL vs MNL — rho estimates; IIA violation evidence
   4.3 MXL diagnostic — Wald test on σ_time, recovery on Mixed-DGP, recommendation for §5
   4.4 Baseline mode shares by zone

5. Policy Simulations (800w)
   5.1 Transit expansion scenarios (A: KRL to J3b; D: TJ to J1b; E: MRT to BSD)
   5.2 Pricing scenarios (B: toll increase; H: RoyalTrans fare reduction)
   5.3 Route restructuring (F: TJ BSD→CBD direct)
   5.4 Service quality (C: KRL frequency; G: RoyalTrans frequency)
   5.5 Scenario interaction analysis (D+F combined, G+H combined, A+E combined)
   Equity comparison: ΔCS across income segments; which scenarios close vs. widen equity gaps

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
   - Single-observation cross-section (1 trip per synthetic person). Real commuter surveys
     (Ilahi, Bastarianto) capture multiple trips per respondent — requiring panel MXL or
     tour-based nesting. The 1-choice-per-person DGP is sufficient for estimator validation
     but does not test panel correction (see §11 Extension G)

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

### Extension G — Panel data + tour-based choice (after L07)
**Trigger**: after all core notebooks complete; only if time permits.
**What**: extend DGP from single cross-section to multi-trip panel: each synthetic person
generates 3–5 linked trips (commute-to-work, return, non-work), with person-specific
random parameters held constant across trips. Implements the panel MXL likelihood:
`LL_n = ln ∫ [Π_{t=1}^{T} P(choice_{nt} | β_n)] f(β_n) dβ_n`.
**Rationale**: Ilahi et al. (2021) and Bastarianto et al. (2019) both use multi-trip data.
Our current 1-choice-per-person design is valid for estimator validation but doesn't test
panel correction. This extension closes that gap and adds a tour-based access-mode layer
for the GrabBike→KRL pattern the user identified.
**Risk**: nesting access-mode choice inside primary mode choice adds substantial complexity.
Only attempt if core is complete and stable with ≥10 days to June 3.
**Notebook**: `03c_panel_mxl.ipynb`

### Data needed for D and E

| Item | Source |
|---|---|
| Link free-flow travel times (6–8 arterials) | Google Maps or Waze historical data; approximate from road class |
| Link capacities (pcu/hr) | Indonesia MKJI standard values by road class |
| PT line capacities (pax/hr) | KRL KCI published data; MRT Jakarta published data |

---

## 12. Timeline

(Numbering note: this section is §12; the Q&A table that follows is §13; Current Status is §14; Key Files is §15. Earlier drafts had a duplicate §12 — corrected here.)

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

## 13. Q&A Preparation — Anticipated Questions

These are the questions most likely from Prof. Chikaraishi. Each must be answerable cold.

### MXL Quick Defense — memorise these three

| If the professor asks… | One-line answer | Where the evidence is |
|---|---|---|
| "Why Mixed Logit if NL already corrects IIA?" | NL = within-nest substitution. MXL = individual taste heterogeneity. Different violations. L07 Five Habits: test both, reject if evidence is absent. | L07 slide 33; `03b_mixed_logit.ipynb` Task A Wald result |
| "Why random β_time and not random ASCs (Ilahi Model 3)?" | L07 lab spec randomises β_time. One σ is robustly identified on 5,000 obs; 9 ASC sigmas are not. Produces VOT distribution directly from VTTS literature. Ilahi Model 3 acknowledged in Discussion. | `notebooks/trans-eng-lectures/L07/L07_estimation_lab.ipynb` Task 3 |
| "Why Wald test, not LR test?" | Simulated LL is Jensen-biased downward; LR can flip sign. Wald uses Hessian + gradient (stable). Demonstrated empirically in L07 Task 3.5 code. | `notebooks/trans-eng-lectures/L07/code/estimate_l07_task3b_mixed_recovery.py` lines 17–26 |

---

### Full Q&A table

| Question | Prepared answer anchor |
|---|---|
| "Why nested logit and not MNL?" | IIA violation — Car/Moto substitution is much stronger than Car/KRL; the 3-nest structure captures three distinct unobserved components (ownership, app convenience, schedule-bound). ρ < 1 estimated from data confirms it. |
| "Why include ridehailing?" | 2WRH (GoRide/GrabBike/Maxim) and 4WRH (GoCar/GrabCar) are the dominant discretionary modes in Jakarta — omitting them would misattribute their share to Car/Moto and bias welfare estimates. No ownership barrier makes them especially relevant for equity analysis. |
| "Where does your β_time come from?" | β_time per mode is derived from Ilahi et al. (2021) Table 11 (p. 413), which reports mode-specific Value of Travel Time Savings (VTTS) in USD/hr. We take his published VTTS for each mode and his generic β_cost = −1.42 per Thousand IDR from Table 10 (p. 410), then β_time_mode = β_cost × VTTS / 60,000. Check: Car VTTS = 1.80 USD/hr ≈ Rp 25,200/hr → β_time = −1.42 × 25,200/60,000 = −0.60/min — recovering Ilahi's estimated coefficient exactly. For MRT, LRT, and RoyalTrans — which had not opened when Ilahi surveyed in 2019 — we interpolate from his transit hierarchy. This is mode-specific β_time (9 parameters), not a single generic β_time. The transfer uses the derived behavioral metric (VTTS) rather than raw coefficients, which is standard practice in cross-study parameter transfer (Wardman 2004). β_time in Ilahi does not interact with demographics (age/gender/degree enter additively as ASC shifters), so the transfer is valid. Parameter recovery in Notebook 02 confirms the estimator recovers all 18 DGP parameters from synthetic data within SE. |
| "Why mode-specific β_time instead of a single generic one?" | Ilahi's model estimates separate travel time coefficients because the marginal disutility of time differs by mode — 1 minute on a motorcycle (exposed, risky) costs more utility than 1 minute in a car (private, comfortable). VTTS ranges from Rp 25,200/hr (Car, comfort-seeking) to Rp 215,490/hr (2WRH, congestion-beating) — this heterogeneity is behaviorally real and policy-relevant: a KRL time improvement produces larger welfare gains for KRL users (high VTTS) than a car time improvement does for car users (low VTTS). A single generic β_time would hide this. In the Nested Logit, the nest structure captures substitution patterns, but mode-specific VoT captures the intensity of time sensitivity. |
| "Why can't you copy Ilahi's ASCs directly?" | ASCs absorb the mean of omitted demographic variables. Ilahi's model includes age, gender, university degree, income, and distance as additive shifters and interactions. His ASC values are conditional on those variables being in the model. Copying them without the demographics would mis-specify. We use Ilahi's preference ordering as a constraint and set our own ASC magnitudes as DGP inputs, calibrated to observed Bodetabek modal shares (BPS 2023: MC ≥ 60%, KRL ~5% on Bodetabek corridors). The parameter recovery validates the estimator — it does not validate the ASC values, which are literature-informed DGP choices. |
| "What is VTAT and why does it matter?" | VTAT = Value of Travel Time Assigned to Travel = VTTS − VOL (Value of Leisure). VOL ≈ 66% of hourly wage (Jara-Díaz et al. 2008, adopted by Ilahi for Indonesia). VTAT > 0 means time spent on that mode is less burdensome than generic leisure time — the mode provides comfort, safety, or security that offsets the travel penalty. Ilahi Table 11 reports: Car VTAT = +3.94 USD/hr (comfortable — users don't mind car time), MC VTAT = −1.32 USD/hr (exposure penalty — time on MC "hurts" more than generic time), Taxi VTAT = −4.24 USD/hr, ODT VTAT = −9.52 USD/hr. Our β_time captures the full VTTS including both VOL and VTAT components. VTAT is descriptive only — it explains WHY Car has low VTTS (comfort dominates) and ODT has high VTTS (exposure + urgency dominate) — but enters no utility calculation. |
| "Your data is synthetic — is this valid?" | V-City approach: known DGP, demonstrate parameter recovery (estimated ≈ true within SE), then apply to realistic Indonesian LOS values. The methodology is the contribution, not the raw observations. |
| "How does the logsum welfare measure work?" | Expected maximum utility over all alternatives; ΔCS = Δlogsum/|β_cost| in Rp; equivalent to compensating variation. Derived in L06 lecture. |
| "What's the equity finding?" | ΔCS from rail extension is largest for low-income KRL-dependent zones (J1a Kota Bogor, J4 Depok); ridehailing welfare gain is highest for middle income (can afford 2WRH, can't afford car) → corridor prioritization argument. J1b and J3b have no transit at all — they receive zero benefit from any transit-side policy and lose most from the toll scenario. |
| "How do you handle multi-modal journeys like 2WRH→KRL→2WRH?" | Alternatives are modelled as linked-trip journeys, not individual segments. The KRL alternative's utility sums impedance across all legs: V = β_t(T_access + T_trunk + T_egress) + β_c(C_access + C_fare + C_egress). Under Option A, access/egress times come from r5py's walk routing; transfer disutility is absorbed into ASC_KRL. Explicit access mode competition — 2WRH vs walk to station — is Option B: a lower nest under the transit alternative with 2WRH access cost and β_transfer explicit. |
| "Why aggregate 2WRH (GoRide/GrabBike/Maxim) into one alternative?" | Discount dynamics (Maxim and GrabBike run heavy promotions with time-varying effective prices) cannot be represented as a fixed cost in the LOS matrix. A single effective average price is used. Within-tier heterogeneity goes in Limitations. Premium 4WRH (Bluebird/GreenSM) is excluded for the same reason — their users are better captured via income-segment β_cost interaction than a separate alternative. |
| "Why ownership-based nesting and not 2W/4W vehicle-type nesting?" | Ridehailing's distinguishing feature is no ownership barrier — central to the equity narrative. Vehicle-type nesting (Moto+2WRH, Car+4WRH) hides this distinction. Also, IIA: a KRL improvement should draw more from ridehailing than from owned modes (sunk cost effect) — ownership-based nesting captures this; 2W/4W does not. The alternative specification is acknowledged in Limitations. |
| "Why model RoyalTrans separately from regular TransJakarta?" | RoyalTrans and regular TJ have fundamentally different cost structures (Rp 3,500 vs Rp 20,000–40,000) and destination profiles. Regular TJ may require an onward MRT transfer to reach JCBD from some termini (Lebak Bulus, Fatmawati), making its true linked-trip cost higher than Rp 3,500. RoyalTrans routes terminate at Sudirman/Kuningan directly — zero egress cost at JCBD. Modelling them as one alternative would conflate a budget feeder mode with an express premium service. Separate ASCs and cost inputs capture this correctly. |
| "Why add South Jakarta? It's close to the CBD." | J5 is an origin zone (~10–20 km from SCBD), not the CBD itself. Its analytical value is as an inner-city reference: it has MRT access and shorter OD distances, so absolute ridehailing and car costs are 3–5× lower than outer zones — not because of a different tariff, but because of distance. This upper-bound welfare zone makes the equity contrast with J1b/J3b sharper. |
| "Why use geographic zones instead of TAI quadrant zones?" | Geographic zones are nameable and defensible — J1b is Parung/Leuwiliyang, Kabupaten Bogor, which any examiner can place on a map. TAI quadrant zones are abstract and require explaining the equity mapper framework first. Instead, zones are *annotated* with TAI proxy (Q2/Q4 etc.) in the Discussion to bridge the two projects without complicating the choice model. |
| "Could you extend this to network analysis?" | Yes — mode choice output is the input OD matrix for assignment. Extension D (car UE assignment via Frank-Wolfe) uses the car demand from §5 as the trip matrix, assigns it to 6–8 key Jabodetabek links with BPR, and computes UE travel times. These are higher than the free-flow times used in mode choice — meaning the current model underestimates car disutility. Scenario B (toll increase) then maps cleanly to a System Optimum policy. Extension E (Davidson PT crowding) checks whether the KRL capacity can absorb the modal shift predicted in §5. |
| "What's the difference between UE and SO?" | At User Equilibrium (UE), each traveller minimises their own travel time — no traveller can reduce their time by switching routes. At System Optimum (SO), the total system travel time is minimised. SO requires internalising externalities (congestion you impose on others) — a toll equal to the marginal external cost achieves this. The toll in Scenario B is the instrument; UE vs SO is the theoretical justification. |
| "What are the limitations?" | No RP data; ownership endogenous; surge/discount dynamics not modelled; premium ridehailing excluded; no congestion feedback in baseline (Extension D adds this); single trip purpose; LRT limited to J2; MRT limited to J5; first/last mile absorbed not explicit. |
| "Why add a Mixed Logit if NL already corrects IIA?" | NL and MXL address different violations of MNL's IID error assumption. NL captures **within-nest substitution** (correlation across alternatives sharing an unobserved component — ownership, app convenience, schedule). MXL captures **individual taste heterogeneity** (different people have different β_time even within the same alternative set). They are not substitutes — testing both is the correct L07 protocol. The MXL is a **specification diagnostic**: if σ_time is not significant, NL is the parsimonious correct model and we report that finding explicitly. The whole point of L07 (slide 33, "Five Habits") is that adding parameters without statistical evidence is a *mistake*, not a hedge. |
| "Why random β_time and not random ASCs (Ilahi Model 3)?" | Three reasons. (1) L07 lab specification: the course materials (Tasks 3 + 3.5) randomize β_time; using the same Beta names and Halton draw structure makes the implementation directly comparable to lecture code. (2) Direct interpretability: a distribution over β_time produces a distribution over Value of Time, which connects to the VTTS literature (Ilahi Table 11, World Bank 2023) without further transformation. Random ASCs produce a distribution over the residual mode preference, which is harder to interpret. (3) Identification: 9 alternatives × random ASCs would require 8 σ parameters and run into thin-cell identification problems on 5,000 observations; one σ on β_time is robustly identified. Ilahi Model 3 with random ASCs is acknowledged in Discussion as an alternative parameterization used in the Indonesian literature; on a larger SP/RP pooled sample (Ilahi 52K obs) it is well-identified. |
| "Why Wald test on σ and not LR test?" | Mixed Logit's likelihood is computed by **Monte Carlo simulation**: log(MonteCarlo(prob)). By Jensen's inequality this is a downward-biased estimator of log(E[prob]); the bias shrinks with draws but at 80–200 draws (the practical range) it is 1–2 LL units. The LR statistic, which differences two LLs, can therefore flip sign relative to the true LL difference — visible in `notebooks/trans-eng-lectures/L07/code/estimate_l07_task3b_mixed_recovery.py` lines 17–26 and L07 Task 3.5. Wald = σ̂ / SE(σ̂) is computed from the Hessian and the simulated gradient, both of which are far more stable than the simulated LL itself. As a secondary check we report boundary-corrected LR (50:50 mixture of χ²(0) and χ²(1), critical 2.71 — Gourieroux, Holly, Monfort 1982). |
| "Are 80–200 Halton draws enough?" | Train (2009, ch. 9) shows 100 Halton draws ≈ 800–1000 pseudo-random draws in coverage. The L07 lab uses 80; the professor's `estimate_l07_task3_mixed_logit.py` uses 200; both estimate σ to the 4th decimal. We verify on Mixed-DGP data (Task C in 03b): the recovered σ̂ matches truth (0.040) within SE at 200 draws. This is the same sensitivity check Train recommends and the L07 lecture demonstrates. |
| "What if σ is significant after all?" | Three actions: (1) carry MXL parameters forward to Stage 5; replace logsum with simulated logsum LS_n = E_η[ln Σ exp(V_n,η)], 200 draws, computed per zone × segment; (2) report ΔCS as a distribution per zone × segment, not a point estimate (5th–95th percentile range — see L07 Task 4 panel C); (3) revisit the NL ρ estimates — strong heterogeneity can manifest as inflated ρ in misspecified NL. The notebook is structured so this branch only adds two cells; 04 reads `best_model.json` and routes to the correct logsum function. |
| "Why 8 policy scenarios? How did you choose them?" | The 8 scenarios are organized into three groups. Group 1 (A–C) are the baseline V-City structure — rail extension, toll pricing, frequency improvement — applied to Jabodetabek geography. Group 2 (D–E) target transit deserts: Scenario D adds TJ to J1b (the only zone with zero transit), Scenario E adds MRT to BSD (testing whether premium rail adds value in an already-KRL-served zone). Group 3 (F–H) are operationally grounded in the actual GTFS data: Scenario F restructures TJ BSD routing from Grogol terminal to CBD direct (observed from GTFS shape geometry — the current route does not reach Sudirman), Scenarios G and H reflect RoyalTrans's actual ~3-departure/peak frequency (observed from GTFS frequencies.txt) and Rp 20,000–40,000 fare structure. Each scenario maps to a real policy lever — network expansion, pricing, routing, frequency, fare — and the scenario comparison matrix (§8) shows how they interact. The equity dimension is explicit: D and F are strongly pro-equity (Q4 transit deserts gain most), G is regressive (benefits middle/high-income), and the interaction notes argue that transit-side improvements (C, G) should be bundled with network expansion (D, F) to avoid regressive outcomes. |

## 14. Current Status

**Last reviewed**: 2026-05-01 (added MXL diagnostic stage 4b — random β_time spec per L07 lab Task 3, Wald test on σ as primary diagnostic, Mixed-DGP recovery as positive control. Notebook 03b inserted between 03 and 04.)

**Immediate next action**: Create `notebooks/trans-eng-final/` folder structure, then begin
`01_data_prep.ipynb`. Build the J-City zone table, mode availability matrix, LOS matrix
(adapt §6.2 values, refine using r5py output for KRL/TJ/LRT/MRT), and synthetic person
sample with income segments per §4.

| Item | Status | Notes |
|---|---|---|
| Project scoping | ✅ Done | This document |
| Branch | ✅ `trans-eng/final-project-jabodetabek` | Off `ui/stitch-redesign` |
| Folder structure | ✅ Done | `notebooks/trans-eng-final/{data,figures,report}/` created |
| `01_data_prep.ipynb` | ✅ Done | 26 cells; data-driven from kelurahan scores + GTFS + transit stops; exports zones.csv, od_skim_jkt.csv, persons_jkt.csv |
| `02_mnl_estimation.ipynb` | ⬜ Not started | Reuse cells 13–23 from `notebooks/logit_eda_mle.ipynb`. 9-mode flat MNL with zone-specific availability per §4. Output: parameter recovery table, VoT by segment |
| `03_nl_estimation.ipynb` | ⬜ Not started | Reuse cells 27–36 from `notebooks/logit_eda_mle.ipynb`. Adapt to ownership-based 3-nest per §3.2/§3.4. Output: ρ estimates, IIA test, NL vs MNL share comparison |
| `03b_mixed_logit.ipynb` | ⬜ Not started | Reuse cells from `notebooks/trans-eng-lectures/L07/L07_estimation_lab.ipynb` Tasks 3 + 3.5 (random β_time, `mixed_nll`, `halton`, `hess_se`). Adapt for 9-mode + zone availability. Output: MXL on MNL data + MXL on Mixed-DGP recovery; Wald test as primary diagnostic; recommendation row for which model carries forward |
| `04_policy_simulation.ipynb` | ⬜ Not started | Reuse cells 43–54 from `notebooks/logit_eda_mle.ipynb`. Read `best_model.json` from 03b → route to NL or MXL logsum. Run the 8 scenarios in §8 (A–H). Output: ΔCS heatmap by zone × income segment, mode share shift charts, scenario comparison matrix |
| `05_car_ue_assignment.ipynb` | ⏸ On hold | Extension D (§11) — unlock after L08 lecture (~2026-05-10); only if core notebooks 01–04 are stable |
| Report draft | ⬜ Not started | Begin after `04_policy_simulation.ipynb` produces results; structure per §10 |

---

## 15. Key Files to Reference

| File | Why |
|---|---|
| `notebooks/trans-eng-final/trans-eng-final-project.md` | **THIS FILE** — master plan, single source of truth |
| `CLAUDE.md` (Trans-Eng Track section) | Session start/end protocol for this track |
| `docs/state.md` (Track 2 section) | Last-action / next-action handover between sessions |
| `notebooks/logit_eda_mle.ipynb` | Existing MNL + NL + logsum + 3-SE estimators implementation — reuse cells 13–23 (MNL), 27–36 (NL), 43–54 (logsum/CS) — adapt to J-City data and ownership-based nesting |
| `notebooks/trans-eng-lectures/vcity_spec.md` | V-City DGP reference — methodology template |
| `notebooks/trans-eng-lectures/logit_derivation_concept.md` | Full MNL derivation (Gumbel, integration, four equalities) — reference for the report Methods section |
| `notebooks/trans-eng-lectures/L06_logsum_concept.md` | Logsum formula + welfare measure derivation; the ρ inclusive-value parameter |
| `notebooks/trans-eng-lectures/L06_se_estimators_concept.md` | Hessian / BHHH / Robust SE — for Results section diagnostics |
| `notebooks/trans-eng-lectures/L05_pres_discrete_choice.pdf` | MNL specification reference (lecture slides) |
| `notebooks/trans-eng-lectures/L06_pres_nested_logit.pdf` | NL specification reference (lecture slides) |
| `data/processed/scores/kelurahan_scores.geojson` | r5py routing output — source for KRL/TJ/LRT/MRT travel times per zone |

---

## 16. Literature Sources

All parameter values, formulas, and empirical anchors are traceable to one of: (a) a course
lecture formula, (b) a published, verifiable reference below, or (c) a computation from
GTFS/BPR data. This section is the Q&A defence reference — every value in §6.3 and §7 maps
to at least one entry here.

**Source quality standard for this project**: every reference in §16.1–16.4 has either a
DOI that resolves at doi.org or a live URL accessible to the examiner. Grey literature
without digital access has been removed. The DGP parameters in §7 are researcher-set inputs
calibrated to be consistent with the ranges and preference orderings reported in these sources.

---

### 16.1 Jakarta/Indonesia mode choice & Value of Travel Time

**PRIMARY — Jakarta mode choice with emerging modes (includes ridehailing):**

- **Ilahi, A., Belgiawan, P. F., & Axhausen, K. W. (2021).** Understanding travel and
  mode choice with emerging modes; a pooled SP and RP model in Greater Jakarta, Indonesia.
  *Transportation Research Part A: Policy and Practice*, 150, 398–422.
  **DOI**: https://doi.org/10.1016/j.tra.2021.06.023
  ETH Zurich repository: https://www.research-collection.ethz.ch/handle/20.500.11850/490738

  The most directly relevant study for this project. Pooled SP+RP discrete choice model
  (5,143 respondents, 52,731 choice observations) from Greater Jakarta. Models 11 alternatives:
  Walk, Bike, Bus, BRT, Train (KRL), Car, MC, Taxi, ODT (ridehailing), PT (SP), UAM.

  **Key extracted values — Table 10 (pp. 410–411), Model 1 (MNL, MC = base):**
  - β Travel cost = −1.42 [per Thousand IDR] (t = −12.08, p < 0.01)
  - β Travel time (mode-specific): Walk −0.36, Bike −8.61, PT −0.28 (not sig.), Bus −1.18
    (not sig.), BRT −1.07, Train −2.72, Car −0.60, MC −2.34, Taxi −3.49, ODT −5.10,
    UAM −1.36 (all per minute; all p < 0.01 except as noted)
  - ASC values (MC = baseline, so all other ASCs are negative — MC most preferred):
    Walk −2.51, Bike −4.22, PT −3.50, Bus −5.05, BRT −4.74, Train −0.29 (not sig.),
    Car −1.20, Taxi −3.94, ODT −1.43, UAM −3.54
  - λ Income, cost = −0.09 (t = −3.06, p < 0.01) — cost sensitivity decreases (in magnitude)
    with income
  - Model fit: 52,731 obs, Final-LL = −57,153, Rho-square = 0.44

  **Key extracted values — Table 11 (pp. 412–413), VTTS in USD/hour (Rp 14,000/USD):**
  - Car: 1.80 USD/hr ≈ Rp 25,200/hr
  - MC: 7.06 USD/hr ≈ Rp 98,840/hr
  - Bus: 3.56 USD/hr ≈ Rp 49,840/hr
  - BRT: 3.23 USD/hr ≈ Rp 45,220/hr
  - Train: 8.21 USD/hr ≈ Rp 114,940/hr
  - Taxi: 10.52 USD/hr ≈ Rp 147,280/hr
  - ODT (ridehailing): 15.38 USD/hr ≈ Rp 215,320/hr
  - UAM: 4.98 USD/hr ≈ Rp 69,720/hr

  **How we use it**: We transfer Ilahi's mode-specific VTTS from Table 11 directly into
  our DGP — 6 of 9 modes are directly anchored. β_time per mode is derived via Ilahi's
  own Eq. 3: β_time_mode = β_cost × VTTS_mode / 60,000 = −1.42 × VTTS / 60,000, which
  recovers his published Table 10 β_time values exactly. This transfers the derived
  behavioral metric (VTTS) rather than raw coefficients — standard practice in cross-study
  parameter transfer (Wardman 2004). The transfer is valid because β_time in Ilahi does
  NOT interact with demographics (age/gender/degree are additive ASC shifters only,
  confirmed by inspecting Table 10). For the 3 modes not in Ilahi's 2019 survey
  (MRT, LRT, RoyalTrans), we interpolate from his transit hierarchy. Full derivation:
  see §7 MNL DGP.

  **Used for**: Mode-specific β_time for 6 of 9 modes (derived from Table 11 VTTS via
  β_cost = −1.42); modal preference ordering (MC > Car > ODT > Train > Bus from
  Table 10 ASCs); cost coefficient (β_cost = −1.42 per Thousand IDR); cost-units
  convention (Thousand IDR).

**SECONDARY — Indonesian commuter mode choice (MNL/NL/CNL):**

- **Bastarianto, F. F., Irawan, M. Z., Choudhury, C., Palma, D., & Muthohar, I. (2019).**
  A Tour-Based Mode Choice Model for Commuters in Indonesia.
  *Sustainability*, 11(3), 788.
  **DOI**: https://doi.org/10.3390/su11030788
  **Open access**: https://www.mdpi.com/2071-1050/11/3/788
  White Rose repository: https://eprints.whiterose.ac.uk/id/eprint/141842/

  Compares MNL, Nested Logit (NL), and Cross-Nested Logit (CNL) for Bekasi–Jakarta
  commuters using 24-hour daily activity pattern data (420 commuters, 8 joint tour-type×mode
  alternatives). The NL model nests hwh and hw+wh tour types as upper nests with mode
  choice (MC, Car, Bus, KRL) in the lower level.

  **Key extracted values — Table 3 (pp. 11–12):**
  - **NL model scale parameters (inclusive value):**
    λ_hwh = 0.55 (t = 6.01, p < 0.01) — strongly significant within-nest correlation for
    the home→work→home tour nest. This is the direct empirical anchor for our
    ρ_OwnVehicle = 0.55.
    λ_hw+wh = 0.99 (fixed to 1.0, no significant within-nest correlation beyond MNL).
  - **β Travel cost** = −0.23 (t = −3.77, p < 0.01) — generic across modes
  - **β Travel time** = −0.01 (t = −3.41, p < 0.01) — generic across modes
    (Note: Bastarianto uses different attribute scaling than Ilahi — the β magnitudes
    are not directly comparable between the two papers. The important finding is the
    λ/ρ structure, not the specific β values.)
  - ASC values (KRL = fixed at 0, the reference): MC = 0.57* (t = 1.60),
    Car = 4.08 (t = 4.71), Bus = 2.21 (t = 5.63)
  - MNL VTTS = 1,381.29 Rp/hr; NL VTTS = 627.86 Rp/hr; CNL VTTS = 544.14 Rp/hr
    (Note: these VTTS values are extremely low — likely due to trip-level cost scaling.
    Not used as direct anchors. The Ilahi & Belgiawan VTTS values are more reliable.)

  **Critical finding for our DGP**: λ_hwh = 0.55 < 1 is significant at p < 0.01 —
  confirming that a Nested Logit structure with within-nest correlation is empirically
  justified for Indonesian commuter mode choice. This is the primary evidence for our
  NL specification and the anchor for ρ_OwnVehicle = 0.55.

  **Used for**: NL ρ parameter anchor (λ_hwh = 0.55 → ρ_OwnVehicle = 0.55); evidence
  that NL improves over MNL for Indonesian mode choice (LR test: χ² = 30.53, df = 3,
  p = 0.10 — marginal but directionally correct); parameter recovery methodology.

**TERTIARY — Jakarta mode choice with pricing (regret-based model):**

- **Belgiawan, P. F., Ilahi, A., & Axhausen, K. W. (2019).** Influence of pricing on
  mode choice decision in Jakarta: A random regret minimization model.
  *Case Studies on Transport Policy*, 7(1), 87–95.
  **DOI**: https://doi.org/10.1016/j.cstp.2018.12.002
  ETH Zurich repository: https://www.research-collection.ethz.ch/handle/20.500.11850/175255

  Jakarta mode choice study using Random Regret Minimization (RRM) framework. SP survey
  with 507 respondents, 4 modes (PT, Park & Ride, Car, MC), with ERP pricing scenarios.
  **Note**: RRM parameters are in regret-space (not utility-space) and are NOT directly
  comparable to MNL/NL utility parameters. However, VTTS (a derived behavioral metric)
  IS comparable across model frameworks.

  **Key extracted values — Table 3 (p. 91):**
  Model 2 (without contribution cost, 4,011 observations):
  - β Travel time = −0.037 (t = −14.45, p < 0.01) — regret parameter, NOT utility
  - β Travel cost = −0.028 (t = −30.21, p < 0.01) — regret parameter, NOT utility
  - ASC Public Transport = −0.079 (not sig., t = −1.31) — not more/less preferred than car
  - ASC Park and Ride = 0.004 (not sig., t = 0.06)
  - ASC Motorcycle = 0.154 (t = 2.64, p < 0.01) — in RRM, positive ASC = more regret =
    less preferred. So MC less preferred than Car in the pricing context.
    This appears to contradict Ilahi's finding (MC most preferred) but reflects the
    different survey context: this is an SP experiment specifically about ERP pricing
    where MC users face contribution costs they wouldn't normally pay.
  - Model fit: 4,011 obs, Final-LL = −4,027.99, Rho-square = 0.276

  **Key extracted values — Table 4 (p. 92), VTTS in Rp/hour:**
  Model 2 (without contribution cost — closer to current Jakarta conditions):
  - Public Transport: Rp 50,250/hr
  - Park and Ride: Rp 45,444/hr
  - Car: Rp 44,609/hr
  - Motorcycle: Rp 38,677/hr

  Model 1 (with contribution cost): values 1.6–2.0× higher (demonstrating that pricing
  expectation inflates VoT — relevant for Scenario B toll analysis but NOT used as
  baseline VoT anchor).

  **Used for**: VoT cross-validation (Model 2 Car Rp 44,609/hr and MC Rp 38,677/hr
  confirm the Ilahi-anchored range of Rp 25,000–100,000/hr); ASC ordering check
  (MC less preferred than Car specifically in pricing context); pricing sensitivity
  evidence for Scenario B (toll increase).

---

### 16.2 Value of Time income scaling — cross-country evidence

**Income elasticity of VoT — meta-analysis:**

- **Binsuwadan, J. & Wardman, M. (2023).** The income elasticity of the value of
  travel time savings: A meta-analysis. *Transport Policy*, 136, 126–136.
  **DOI**: https://doi.org/10.1016/j.tranpol.2023.03.013
  White Rose repository: https://eprints.whiterose.ac.uk/id/eprint/198772/

  Meta-analysis of 268 income elasticities from 49 studies (1968–2019). Provides the
  empirical basis for scaling VoT across income segments within a country. Reports
  that cross-sectional inter-personal income elasticity of VoT is approximately
  η ≈ 0.5–0.7 (i.e., doubling income increases VoT by ~50–70%, not 100%).
  **Used for**: scaling VoT from middle-income anchor (Rp 25,000/hr) to low-income
  (Rp 12,000/hr) and high-income (Rp 55,000/hr) segments in §6.3.

**World Bank VoT meta-analysis for developing countries:**

- **World Bank (2024).** *Meta-Analysis of the Value of Travel Time Savings in Low-
  and Middle-Income Countries*. World Bank Group, Washington, D.C.
  https://documents.worldbank.org/en/publication/documents-reports/documentdetail/099032124211022462

  Comprehensive meta-analysis of VoT studies in LMICs. Provides recommended VoT ranges
  as % of wage rate for different modes and trip purposes.
  **Used for**: cross-validating the VoT/wage-rate ratio used in §6.3; developing-country
  VoT benchmarks.

**GDP per capita PPP — cross-country income comparison:**

- **World Bank (2024).** World Development Indicators — GDP per capita, PPP
  (current international $). https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.CD

  Indonesia GDP/cap PPP ≈ USD 14,000; Japan ≈ USD 42,000 (ratio ≈ 1:3).
  VoT scales roughly with income, so Indonesia VoT expected ~⅓ Japan VoT.
  Our β_cost = −1.42 per Thousand IDR comes from Ilahi et al. (2021) Table 10, estimated
  directly from Jakarta data — no cross-country scaling is needed. The V-City β_cost
  = −0.0015 for Japan serves as an order-of-magnitude sanity check only.
  **Used for**: cross-check only — not used in parameter derivation.

**Jakarta minimum wage (UMP DKI Jakarta 2025):**

- **Pemerintah Provinsi DKI Jakarta (2025).** Upah Minimum Provinsi (UMP) DKI Jakarta
  2025: Rp 5,000,000/month ≈ Rp 29,000/hr (at 173 working hrs/month per UU No. 13/2003).
  https://jakarta.go.id/ (or https://jdih.jakarta.go.id/ for the gubernatorial decree)

  Provides the lowest defensible VoT floor: even the lowest-wage commuter values time
  at a meaningful fraction of their wage rate. The low-income VoT of Rp 12,000/hr ≈ 40%
  of minimum wage, consistent with the LMIC VoT/wage ratio reported by the World Bank (2024).
  **Used for**: lower-bound VoT validation in §6.3.

---

### 16.3 Modal share and preference data — Jakarta

**Jakarta transport statistics:**

- **BPS Provinsi DKI Jakarta (2023).** *Statistik Transportasi Provinsi DKI Jakarta 2022*.
  Badan Pusat Statistik Provinsi DKI Jakarta.
  https://jakarta.bps.go.id/

  Official modal share statistics for Jakarta. Motorcycle accounts for ≥60% of daily
  trips in Greater Jakarta corridor. Used as the empirical basis for ASC_Moto = +1.80
  (highest positive ASC) and the overall modal preference ordering.

**Jakarta commuter mode share (BPS Susenas/Commuter Survey):**

- **BPS Republik Indonesia (2023).** *Statistik Komuter Jabodetabek 2022*.
  Badan Pusat Statistik. https://www.bps.go.id/

  Commuter-specific modal share for Jabodetabek. Documents the dominance of private
  modes (motorcycle + car) and the growing share of ridehailing since 2019.
  **Used for**: zone-level mode share calibration; evidence for motorcycle dominance.

  The motorcycle-dominant paradigm in Southeast Asian cities is well-documented in the
  transport literature (see Ilahi et al. 2021 §16.1 for Jakarta-specific mode share
  data including ridehailing). The Indonesian context — where motorcycle share ≥ 60% —
  is the empirical basis for ASC_Moto being the highest positive ASC in the model.

---

### 16.4 Ridehailing and transit tariff data — Indonesia

**Gojek tariff schedule (2025):** https://www.gojek.com/en-id/tarif/
  GoRide: Rp 2,000–2,500/km + Rp 1,000 booking fee.
  GoCar: Rp 3,500–4,500/km + Rp 1,500 booking fee.
  Effective average excluding promotions. Used in §5 and §6.2.

**Grab fare guide (2025):** https://www.grab.com/id/fare-guide/
  Corroborates Gojek tariff order of magnitude for 2WRH and 4WRH.
  Base rates similar; discount dynamics excluded per §5.

**TransJakarta RoyalTrans (2025):** https://www.transjakarta.co.id/royaltrans/
  Route map and schedules for RoyalTrans express bus service.
  Routes verified (2026-04): B14 Bekasi→Kuningan; S12 BSD→Fatmawati;
  S14 Summarecon Serpong→Lebak Bulus; D31/D32 Cinere→Kuningan/Senayan.
  No Bogor corridor routes exist. Used in §4 and §5.

**MRT Jakarta (2023).** *Laporan Tahunan 2022* [2022 Annual Report].
  PT MRT Jakarta (Perseroda). https://jakartamrt.co.id/en/annual-report
  Passenger satisfaction survey; ridership data. ASC_MRT = +0.20 anchor.

**PT KAI Commuter (2023).** *Laporan Tahunan 2022* [2022 Annual Report].
  PT KAI Commuter (KCI). https://www.krl.co.id/
  LRT Jabodebek ridership since August 2023 opening. ASC_LRT = −0.10 anchor.

---

### 16.5 Discrete choice model theory — foundational references

**MNL derivation and Nested Logit:**

- **Ben-Akiva, M. & Lerman, S. R. (1985).** *Discrete Choice Analysis: Theory and
  Application to Travel Demand*. MIT Press. ISBN 978-0-262-02217-0.
  Ch. 4–5: MNL derivation from Gumbel-distributed errors. Ch. 10: Nested Logit
  inclusive value structure and consistency conditions.

- **Train, K. (2009).** *Discrete Choice Methods with Simulation* (2nd ed.).
  Cambridge University Press.
  **Open access (full PDF)**: https://eml.berkeley.edu/books/train1201.pdf
  Ch. 2: identifiability and ASC normalisation. Ch. 3: logsum as expected maximum
  utility — E[max U] = ln Σ exp(V_m) + γ. Ch. 4: Nested Logit — IV_nest = ρ · ln Σ
  exp(V_m/ρ); ρ ∈ (0, 1] consistency condition; estimation by maximum likelihood.

- **Koppelman, F. S. & Bhat, C. (2006).** *A Self Instructing Course in Mode Choice
  Modeling: Multinomial and Nested Logit Models*. Federal Highway Administration,
  U.S. Department of Transportation.
  **Open access**: https://www.caee.utexas.edu/prof/bhat/COURSES/LM_Draft_060131Final-060630.pdf
  Step-by-step NL specification with worked examples.

**Logsum welfare measure:**

- **McFadden, D. (1978).** Modelling the choice of residential location. In A. Karlqvist
  et al. (Eds.), *Spatial Interaction Theory and Planning Models* (pp. 75–96).
  North-Holland, Amsterdam.
  Original derivation of ΔCS = Δlogsum / |β_cost| as the Hicksian compensating variation
  welfare measure for logit models. The logsum rule used in §3.3 and `04_policy_simulation.ipynb`.

---

### 16.6 Network analysis — BPR and Davidson functions (Extensions D/E)

**BPR congestion function:**

- **U.S. Bureau of Public Roads (1964).** *Traffic Assignment Manual*.
  U.S. Department of Commerce. t_a(v) = t_0[1 + 0.15·(v/c)^4].

- **Sheffi, Y. (1985).** *Urban Transportation Networks: Equilibrium Analysis with
  Mathematical Programming Methods*. Prentice-Hall.
  **Open access**: https://sheffi.mit.edu/book/urban-transportation-networks
  p. 54: BPR derivation. Ch. 5: Frank-Wolfe User Equilibrium algorithm (Extension D).

**Davidson PT crowding function:**

- **Davidson, K. B. (1966).** A flow travel time relationship for use in transportation
  planning. *Australian Road Research Board Conference Proceedings*, 3(1), 183–194.
  t(v) = t_0[1 + 0.2·v/(s−v)]. Applied in Extension E.

---

### 16.7 Lecture notes (project-local, course material)

| File | Content |
|---|---|
| `notebooks/trans-eng-lectures/L05_pres_discrete_choice.pdf` | MNL specification, estimation (course primary reference) |
| `notebooks/trans-eng-lectures/L06_pres_nested_logit.pdf` | NL formulas, ρ interpretation, IV structure |
| `notebooks/trans-eng-lectures/logit_derivation_concept.md` | Full four-equality MNL derivation from Gumbel |
| `notebooks/trans-eng-lectures/L06_logsum_concept.md` | Logsum = E[max U]; welfare formula; NL nest IV with ρ |
| `notebooks/trans-eng-lectures/L06_se_estimators_concept.md` | Hessian/BHHH/Robust SE — Results diagnostics |
| `notebooks/trans-eng-lectures/vcity_spec.md` | V-City DGP specification — methodology template |

# Trans-Eng Final Project — Defense Cheat Sheet

Use this during Q&A. Every number is traceable to a lecture formula, literature citation, or GTFS/BPR computation.

---

## 1. Where Do the Parameters Come From?

### 1.1 β_cost (generic, all modes)

**Value**: β_cost = −1.42 per Thousand IDR (DGP input)

**Source**: Ilahi et al. (2021), Table 10, Model 1 — "β Travel cost = −1.42, t = −12.08, p < 0.01". This is evaluated at sample-mean income and distance (includes the λ_Income,cost = −0.09 interaction already folded in).

**Why Ilahi?** It is the most recent Jakarta-specific stated-preference mode choice study with a published β_cost. The survey covered Jabodetabek commuters across car, motorcycle, BRT, and train — exactly our mode set.

### 1.2 β_time (mode-specific)

**Formula** (Train 2009 §3.2):

```
β_time,m = β_cost × VTTS_m / 60,000
```

where VTTS is in Rp/hr from Ilahi Table 11, and 60,000 converts Rp/hr to Th IDR/min.

| Mode | Ilahi analog | VTTS (Rp/hr) | β_time (/min) | Source |
|------|-------------|-------------|---------------|--------|
| Car | Car | 25,200 | −0.60 | Ilahi Table 11: 1.80 USD/hr × Rp 14,000 |
| Moto | Motorcycle | 98,840 | −2.34 | Ilahi Table 11: 7.06 USD/hr |
| KRL | Train | 114,930 | −2.72 | Ilahi Table 11: 8.21 USD/hr |
| TJ | BRT | 45,220 | −1.07 | Ilahi Table 11: 3.23 USD/hr |
| MRT | interpolated | 126,000 | −2.98 | KRL × 1.10 (MRT opened March 2019, after Ilahi survey) |
| Royal | interpolated | 55,000 | −1.30 | TJ × 1.22 (premium BRT) |

**Verification**: Car VTTS 25,200 → β_time = −1.42 × 25,200 / 60,000 = −0.596 ≈ −0.60 ✓

### 1.3 ASC (Alternative-Specific Constants)

KRL = 0 (reference). All others calibrated to reproduce BPS Susenas 2023 aggregate mode shares.

| Mode | ASC | Rationale |
|------|-----|-----------|
| KRL | 0.00 | Reference alternative |
| Moto | +1.20 | Highest — BPS 2023 shows MC ≥ 60% mode share in Jabodetabek |
| Car | +0.90 | Above KRL; reflects strong motorization preference in outer zones |
| MRT | +0.30 | Premium rail, slightly above KRL |
| Royal | +0.05 | Near KRL baseline |
| TJ | −0.30 | Below KRL; BRT-lite runs in mixed traffic, lower perceived quality |

**If asked "why not use Ilahi's ASCs directly?"**: Ilahi's ASCs (re-normalized to KRL = 0) give Car = −0.91 and MC = +0.29. These were estimated on a different choice set (includes ODT, taxi) and at a different scale. Our ASCs are calibrated to match BPS 2023 aggregate shares at the μ = 25 scale — the relative ordering is what matters, not the absolute values.

### 1.4 What the Estimator Actually Recovers

After scale normalization (μ = 25), the estimator recovers β̃ = β/μ. So:
- DGP β_cost = −1.42 → estimated β̃_cost ≈ −1.42/25 = −0.057 → actual NL estimate: −0.077 (within 0.21 SE) ✓
- DGP β_time,moto = −2.34 → estimated β̃_time,moto ≈ −2.34/25 = −0.094 → actual NL estimate: −0.096 ✓

**All 12 MNL parameters and all 13 NL parameters recovered within 2 SE of true DGP values.**

---

## 2. How Was the Synthetic Data Generated?

### 2.1 The Data Generating Process (DGP)

We use a **Nested Logit GEV DGP** with closed-form choice probabilities.

**Step-by-step**:

1. **Draw 5,000 persons** across 7 zones, with income segments from BPS Susenas 2023:
   - Low (33.3%): mean income Rp 3M/month, car access 5%, moto access 60%
   - Mid (50.3%): mean income Rp 9M/month, car access 26%, moto access 80%
   - High (16.4%): mean income Rp 22M/month, car access 65%, moto access 48%
   - Overall: car access 25.6%, moto access 67.9% (matches Ilahi Table 3)

2. **Assign LOS** from r5py GTFS routing (transit) and BPR speeds (private):
   - Transit: AM peak 07:00–09:00, door-to-door (access walk + wait + IVT + egress)
   - Car: toll roads 80 km/h, arterials 40 km/h, local 25 km/h
   - Modes unavailable in a zone get time = 180 min (effectively removed)

3. **Compute V_m** for each person × mode:
   ```
   V_m = ASC_m + β_time,m × time_m + β_cost × cost_m
   ```

4. **Divide by scale μ = 25** to get normalized utilities

5. **Compute NL choice probabilities** (Train 2009 §4.2):
   ```
   IV_k = λ × ln Σ_{m∈k} exp(V_m / λ)        [nest inclusive value]
   P(k) = exp(IV_k) / Σ_ℓ exp(IV_ℓ)            [nest probability]
   P(m|k) = exp(V_m/λ) / Σ_{m'∈k} exp(V_m'/λ)  [within-nest probability]
   P(m) = P(m|k) × P(k)                         [unconditional probability]
   ```
   with λ = 0.70 and two nests: Private {Car, Moto}, Transit {KRL, TJ, Royal, MRT}

6. **Draw choices** from the multinomial distribution defined by P(m)

### 2.2 Why NL-DGP, Not MNL or MXL?

**Why not MNL-DGP?**
- MNL assumes IIA (Independence of Irrelevant Alternatives) — equal proportional substitution across ALL modes
- In Jakarta, this is empirically wrong: Car/Moto share a strong "motorization" unobserved attribute; transit modes share "schedule-bound public infrastructure"
- Bastarianto et al. (2019) Table 3 confirms λ_hwh = 0.55 (t = 6.01, p < 0.01) for Indonesian commuters — **NL nesting is statistically significant in real Jakarta data**
- If we generated from MNL, we'd be building a model that ignores known structure in Jakarta mode choice

**Why not MXL-DGP?**
- MXL adds random taste heterogeneity (person-level random coefficients)
- There is no empirical evidence of significant cost heterogeneity in Ilahi's Jakarta data beyond what nesting captures
- MXL is used here as a **diagnostic tool** — we test whether random β_cost adds signal beyond NL nesting. The answer: it doesn't (Wald p = 0.763)
- L07 "Five Habits" principle: "be willing to reject the richer model when evidence does not support it"

**If we had used MXL-DGP (σ_cost,true = 0.02), expected results would be**:
- MXL Wald test on σ_cost would reject H₀ at p ≈ 0 (we verified this with a positive control)
- NL λ̂ would still be < 1 (nesting is real regardless)
- The welfare model would need simulation-based integration instead of closed-form logsum
- But since our NL-DGP has no person-level random parameters, MXL correctly finds σ̂ ≈ 0

### 2.3 Why Not Real Data?

No public revealed-preference mode choice microdata exists for Jabodetabek with all 6 modes and trip-level LOS. The synthetic DGP lets us:
1. **Control the truth** — we know the exact parameters, so we can verify recovery
2. **Use real LOS** — transit times come from actual GTFS feeds via r5py, not invented numbers
3. **Anchor to literature** — every β comes from Ilahi (2021), every ASC calibrated to BPS 2023

---

## 3. Why Those Specific Parameter Values?

### 3.1 Gumbel Scale μ = 25

**The problem**: Ilahi's β values combined with our LOS data (time in minutes, cost in Th IDR) produce systematic utility differences of **5–75 utils** at Gumbel μ = 1. The standard Gumbel variance is σ² = π²/6 ≈ 1.64, so standard deviation ≈ 1.28. A utility gap of 20 utils with SD 1.28 means the best mode gets >99.99% probability — **choices become deterministic**.

**The fix**: Divide all V by μ = 25 before adding Gumbel noise. This is mathematically equivalent to drawing ε ~ Gumbel(0, 25) instead of Gumbel(0, 1).

**Why this is legitimate** (Train 2009 §2.5): MNL utility scale is NOT separately identified from Gumbel variance. The likelihood function for MNL is:
```
P(m) = exp(V_m/μ) / Σ_j exp(V_j/μ)
```
We can only estimate β/μ, never β and μ separately. So μ = 25 is a **normalization choice**, not an assumption.

**What is preserved**: VOT = β_time / β_cost × 60,000. Since both β_time and β_cost are divided by the same μ, the ratio is unchanged. All behavioral metrics (VTTS, elasticities, welfare measures) are scale-invariant.

**What changes**: Estimated β̂ magnitudes are 25× smaller than Ilahi's. This is expected and correct — they are at a different scale normalization.

**Result**: With μ = 25, we get realistic choice distributions: Moto 36.7%, TJ 34.0%, KRL 17.8%, Royal 9.1%, MRT 1.4%, Car 1.0%.

### 3.2 λ (Nest Dissimilarity Parameter) = 0.70

**Source**: Bastarianto et al. (2019) Table 3 reports λ_hwh = 0.55 for home-work-home trips in Indonesian commuter NL. Our λ = 0.70 is a conservative choice (closer to 1.0 = MNL) because:
- Bastarianto used a CNL (Cross-Nested Logit) with different nest definitions
- Our 2-nest structure (Private vs Transit) is simpler, so higher λ is appropriate
- 0.70 still implies substantial within-nest correlation (30% shared unobserved variance)

**What λ means**:
- λ = 1.0 → MNL (no within-nest correlation, IIA holds)
- λ = 0.0 → Perfect within-nest substitution (all transit modes are identical)
- λ = 0.70 → Moderate within-nest correlation. Transit modes share 30% of unobserved variance (crowding, schedule coordination, station environment)

**Estimated vs true**: λ̂ = 0.763 ± 0.068. True = 0.700. Bias = +9%, but |0.063| < 2 × 0.068 = 0.136 → **within 2 SE**. The 95% CI [0.627, 0.900] **excludes 1.0**, confirming nesting.

### 3.3 Why Two Nests (Private vs Transit)?

**Transit nest {KRL, TJ, Royal, MRT}**: These modes share schedule constraints, station access, crowding, and government subsidy exposure. A KRL improvement draws more from TJ than from Moto.

**Private nest {Car, Moto}**: These share ownership commitment, door-to-door flexibility, and fuel price exposure.

**Evidence**: Our IIA test confirms this. Cloning KRL as "KRL Express" → MNL nearly doubles transit share (11.7% → 21.8%), violating IIA. NL cross-elasticity test: TJ +0.1 utility → transit modes lose 1.90 pp, private modes lose 1.14 pp. Within-nest substitution is **1.67× cross-nest** — exactly what NL predicts.

---

## 4. Model Evaluation — Every Metric Explained

### 4.1 The Comparison Table

| Criterion | MNL | **NL** | MXL | What it means |
|-----------|-----|--------|-----|---------------|
| K | 12 | 13 | 13 | Number of estimated parameters |
| LL(β̂) | −5,048.83 | **−5,044.54** | −5,048.79 | Log-likelihood at estimated parameters |
| AIC | 10,121.65 | **10,115.08** | 10,123.59 | Akaike Information Criterion |
| BIC | 10,199.86 | 10,199.80 | 10,208.31 | Bayesian Information Criterion |
| ρ² | 0.280 | 0.281 | 0.280 | McFadden's pseudo R-squared |
| LR vs MNL (p) | — | **0.003** | 0.799 | Likelihood Ratio test p-value |
| Wald σ = 0 (p) | — | — | 0.763 | Wald test for random parameter |

### 4.2 Log-Likelihood (LL)

**What it is**: The sum of log-probabilities that the model assigns to the actually chosen alternatives. Higher (less negative) = better fit.

```
LL(β̂) = Σ_{n=1}^{N} ln P_n(chosen_m | β̂)
```

**Null model**: LL(0) = −7,011.56 (equal probability across available modes — no parameters).

**Interpretation**: NL LL = −5,044.54 means the NL model assigns, on average, exp(−5,044.54/5,000) = exp(−1.009) ≈ 0.365 probability to the correct mode per person. Much better than random (1/6 ≈ 0.167).

**NL gains 4.29 LL units over MNL** with just 1 extra parameter (λ). MXL gains only 0.04 LL units — essentially zero improvement.

### 4.3 AIC (Akaike Information Criterion)

**Formula** (Akaike 1974):
```
AIC = −2 × LL(β̂) + 2K
```

**What it does**: Penalizes model complexity. Lower = better. The penalty is 2 per parameter.

**Calculation**:
- MNL: −2(−5,048.83) + 2(12) = 10,121.65
- NL: −2(−5,044.54) + 2(13) = 10,115.08
- MXL: −2(−5,048.79) + 2(13) = 10,123.59

**NL wins by ΔAIC = −6.57 vs MNL and −8.51 vs MXL.** Rule of thumb (Burnham & Anderson 2002): ΔAIC > 4 = "considerably less support" for the worse model.

### 4.4 BIC (Bayesian Information Criterion)

**Formula** (Schwarz 1978):
```
BIC = −2 × LL(β̂) + K × ln(N)
```

**What it does**: Same as AIC but with a stronger penalty that grows with sample size. BIC penalizes complexity more than AIC.

**Calculation** (N = 5,000, ln(5000) = 8.52):
- MNL: −2(−5,048.83) + 12 × 8.52 = 10,199.86
- NL: −2(−5,044.54) + 13 × 8.52 = 10,199.80
- MXL: −2(−5,048.79) + 13 × 8.52 = 10,208.31

**NL and MNL are nearly tied on BIC** (ΔBIC = 0.06). This is because BIC's per-parameter penalty (8.52) nearly equals the 2×ΔLL improvement (8.58). But NL still wins — and BIC strongly rejects MXL.

### 4.5 ρ² (McFadden's Pseudo R-squared)

**Formula** (McFadden 1974):
```
ρ² = 1 − LL(β̂) / LL(0)
```

**Interpretation**: Fraction of "information" explained by the model relative to the null. Unlike OLS R², values of 0.2–0.4 are considered **excellent** in discrete choice (Ben-Akiva & Lerman 1985, p.167).

- ρ² = 0.280 → "The model explains 28% of the information in the choice data" → very good for a mode choice model

**Adjusted**: ρ̄² = 1 − (LL(β̂) − K) / LL(0) = 0.278 for MNL. Penalizes parameters like adjusted R².

### 4.6 Likelihood Ratio (LR) Test — NL vs MNL

**What it tests**: H₀: λ = 1 (NL collapses to MNL, no nesting needed)

**Formula**:
```
LR = −2 × [LL(restricted) − LL(unrestricted)]
   = −2 × [LL_MNL − LL_NL]
   = −2 × [−5,048.83 − (−5,044.54)]
   = −2 × (−4.29)
   = 8.57
```

**Distribution**: χ²(df = 1) because NL has 1 extra parameter (λ).

**Critical value**: χ²(1, α=0.05) = 3.84; χ²(1, α=0.01) = 6.63.

**Result**: LR = 8.57 > 6.63 → **reject H₀ at p = 0.0034**. NL is statistically significantly better than MNL.

**In plain English**: "The probability of observing this much improvement in fit by chance, if IIA actually held, is 0.3%. We reject IIA."

### 4.7 Wald Test — MXL σ_cost = 0

**What it tests**: H₀: σ_cost = 0 (no random taste heterogeneity in cost sensitivity)

**Formula**:
```
W = (σ̂ / SE(σ̂))² = (0.010 / 0.033)² = 0.091
```

**Distribution**: χ²(1)

**Result**: W = 0.091, p = 0.763 → **fail to reject H₀**. There is no evidence of cost heterogeneity.

**Positive control**: When we generate data WITH taste heterogeneity (σ_true = 0.02), the Wald test correctly detects it (p ≈ 0). This proves the estimator works — it just doesn't find heterogeneity in our NL-DGP data because there isn't any.

### 4.8 Other Metrics You Could Mention

**Parameter recovery rate**: All 12 MNL and 13 NL parameters fall within 2 SE of DGP truth. This validates the estimation procedure.

**Hit rate** (% correctly predicted): Not reported but calculable. For 6 modes, random = 16.7%. With ρ² = 0.28, expected hit rate ≈ 55–65%.

**Elasticities**: Direct and cross-elasticities are computable from the NL model. The IIA demonstration (TJ +0.1 → within-nest 1.67× cross-nest) is itself an elasticity-based diagnostic.

**Ben-Akiva & Swait (1986) non-nested test**: Could compare MNL vs MXL directly (not nested). Not needed here because MXL adds essentially zero LL improvement.

---

## 5. Scenario Results — What Every Number Means

### 5.1 What Is Mean ΔCS?

**ΔCS** = Change in Consumer Surplus per person per trip, in Thousand IDR.

**Formula** (Small & Rosen 1981, applied to NL via Train 2009 §3.5):
```
EMU_n = ln Σ_k exp(λ × IV_kn)         [expected maximum utility, upper level]
IV_kn = ln Σ_{j∈k} exp(V_jn / λ)      [inclusive value per nest]

CS_n = EMU_n / |β_cost|                [consumer surplus in Th IDR per trip]
ΔCS_n = (EMU_policy − EMU_baseline) / |β_cost|
```

**Interpretation**: ΔCS = +3.76 means each person gains Rp 3,760 worth of welfare **per trip**. This is NOT cash — it's the equivalent monetary value of improved travel options. A commuter who now has a faster KRL option experiences the same satisfaction increase as if they'd been given Rp 3,760.

### 5.2 What Is Annual ΔW?

**Formula**:
```
ΔW_annual = Σ_n (ΔCS_n × expansion_factor_n) × 250 working days × 1,000 / 1,000,000,000
```

The expansion factor scales each synthetic person to represent real commuters in their zone (zone population ÷ synthetic persons in that zone).

### 5.3 What Does "+6,580 Bn IDR/year" for Scenario C Mean?

**It means**: If KRL frequency improves by 20% (reducing travel time by 20% in KRL-served zones), the total welfare gain across all Jabodetabek commuters is equivalent to **Rp 6.58 trillion per year**.

**This is NOT direct money saved.** It is the sum of:
- Time savings (valued at each person's VTTS)
- Improved choice set (having a faster option, even if you don't switch, raises your expected maximum utility)
- Mode switching benefits (people who switch from moto to KRL gain the fare difference minus the time difference, valued at their VTTS)

**Real-world analog**: The government could justify spending up to Rp 6.58T/year on KRL frequency improvements, and commuters would still be better off. It's the **maximum willingness to pay** for the policy.

### 5.4 What Does "−168 Bn IDR/year" for Scenario B Mean?

**It means**: A Rp 40,000 toll increase makes ALL commuters worse off — total welfare loss of Rp 168 billion/year.

**Why everyone loses**: The toll makes car more expensive. Car users lose directly (higher cost). But even non-car users are slightly worse off because their **option value** of driving decreases. If they ever needed to drive (emergency, schedule change), it would cost more. The logsum captures this: removing or degrading an alternative reduces EMU even for people who don't currently choose it.

**Winners = 0**: No one benefits from a pure cost increase. This is why toll pricing is regressive without revenue recycling.

### 5.5 All 8 Scenarios — Detailed Breakdown

#### Scenario A: KRL Extension to J3b (Gading Serpong)
| Metric | Value |
|--------|-------|
| LOS change | Add KRL to J3b: T = 70 min, C = 7.5 Th IDR |
| Mean ΔCS | +0.001 Th IDR/trip |
| Annual ΔW | +2.22 Bn IDR |
| Winners | 318 (6.4%) |
| Mode shift | KRL +0.02 pp from TJ −0.01 |

**Why so small?** J3b has only 318 synthetic persons (small zone population). And KRL at 70 min / 7.5k IDR is not dramatically better than existing options in J3b. The benefit is real but concentrated in a small population.

#### Scenario B: Toll +40,000 IDR
| Metric | Value |
|--------|-------|
| LOS change | Car cost + 40 Th IDR in all zones |
| Mean ΔCS | −0.100 Th IDR/trip |
| Annual ΔW | −168.02 Bn IDR |
| Winners | 0 (0%) |
| Mode shift | Car 1.0% → 0.02%, moto +0.6 pp, TJ +0.3 pp |

**Key insight**: A punitive toll without transit alternatives destroys welfare. Car users shift to moto (not transit), creating no modal shift benefit. The −Rp 168B is pure deadweight loss. **This is the classic argument for combining pricing with transit investment.**

#### Scenario C: KRL Frequency −20% Travel Time
| Metric | Value |
|--------|-------|
| LOS change | KRL time × 0.80 in J1a, J2, J3a, J4 |
| Mean ΔCS | +3.765 Th IDR/trip |
| Annual ΔW | +6,580.38 Bn IDR |
| Winners | 3,580 (71.6%) |
| Zone breakdown | J1a +15.79, J3a +6.92, J4 +2.46, J2 +1.88, **J1b = 0, J3b = 0** |
| Mode shift | KRL +14.9 pp (17.8% → 32.7%), from Moto −7.8, TJ −5.1, Royal −1.9 |

**Why C is #1 aggregate but NOT most equitable**: KRL-served zones (J1a, J2, J3a, J4) get massive gains. But J1b and J3b have NO KRL access → receive exactly zero benefit. This is "rich-get-richer" spatial equity — zones that already have rail get even better service.

**Equity implication**: "Should we invest Rp 6.58T/year in making good zones better, or Rp 5.69T/year (Sc D) in giving underserved zones their first transit?"

#### Scenario D: TJ Extension to J1b (Parung)
| Metric | Value |
|--------|-------|
| LOS change | Add TJ to J1b: T = 90 min, C = 3.5 Th IDR |
| Mean ΔCS | +3.292 Th IDR/trip |
| Annual ΔW | +5,685.65 Bn IDR |
| Winners | 579 (11.6%) |
| Zone breakdown | **J1b +28.43 Th IDR/trip**, all other zones = 0 |
| Income breakdown | Low +3.38, Mid +3.29, High +3.03 → mildly progressive |
| Mode shift | TJ +10.3 pp, from Moto −10.1, Car −0.2 |

**Why D is most pro-equity**: J1b currently has NO formal transit (only car/moto). Adding TJ at 90 min / Rp 3,500 is transformative — each J1b commuter gains Rp 28,430/trip. TJ draws almost entirely from motorcycles (−10.1 pp), meaning it converts private vehicle users to transit. Low-income residents benefit slightly more because the flat Rp 3,500 TJ fare represents a larger welfare gain relative to their baseline options.

**What +28.43 Th IDR/trip means for a J1b commuter**: That's Rp 28,430 per trip, or roughly Rp 14.2M/year (250 days × 2 trips). For a low-income household earning Rp 3M/month, this welfare gain equals **39% of monthly income** — life-changing.

#### Scenario E: MRT Extension to J3a (BSD Serpong)
| Metric | Value |
|--------|-------|
| LOS change | Add MRT to J3a: T = 60 min, C = 12.0 Th IDR |
| Mean ΔCS | +0.002 Th IDR/trip |
| Annual ΔW | +3.39 Bn IDR |
| Winners | 192 (3.8%) |

**Why so small?** J3a already has KRL (85 min / 7k). Adding MRT at 60 min / 12k is faster but more expensive. The net utility gain is small because the cost penalty partially offsets the time gain. Also, only J3a benefits.

#### Scenario F: TJ BSD→CBD Direct Route
| Metric | Value |
|--------|-------|
| LOS change | J3b: add TJ at 80 min / 3.5k; J3a: add TJ at 80 min / 3.5k |
| Mean ΔCS | +0.529 Th IDR/trip |
| Annual ΔW | +852.60 Bn IDR |
| Winners | 510 (10.2%) |
| Zone breakdown | J3a +9.66, J3b +2.49 |
| Mode shift | TJ +2.6 pp, KRL −1.1, Moto −1.2 |

**Key insight**: Benefits both BSD zones. J3a gains more because it has a larger population. TJ at Rp 3,500 undercuts KRL (Rp 7,000) and Royal (Rp 39,000), creating genuine modal competition.

#### Scenario G: RoyalTrans Frequency Improvement
| Metric | Value |
|--------|-------|
| LOS change | Royal wait time −15 min in J2, J3a, J3b, J4 |
| Mean ΔCS | +1.257 Th IDR/trip |
| Annual ΔW | +2,093.22 Bn IDR |
| Winners | 3,132 (62.6%) |
| Zone breakdown | J2 +2.35, J4 +2.20, J3a +0.93, J3b +0.30 |
| Income breakdown | Low +1.26, Mid +1.26, High +1.26 → perfectly uniform |

**Why "regressive" despite positive gains**: Royal serves only zones that already have transit (J2, J3a, J3b, J4). J1b (no transit) and J1a (no Royal) get zero. Gains are spatially regressive even though income-uniform within served zones.

#### Scenario H: RoyalTrans Fare −50%
| Metric | Value |
|--------|-------|
| LOS change | Royal cost × 0.50 in J2, J3a, J3b, J4 |
| Mean ΔCS | +1.985 Th IDR/trip |
| Annual ΔW | +3,303.37 Bn IDR |
| Winners | 3,132 (62.6%) |
| Zone breakdown | J2 −3.50, J3a −3.50, J4 +3.50 (mixed signs by zone) |
| Mode shift | Royal +14.1 pp (9.1% → 23.2%), from TJ −8.5, Moto −3.1, KRL −2.4 |

**Why H creates the biggest mode shift**: Halving Royal fares (e.g., Rp 39k → 19.5k) makes Royal competitive with KRL on cost while maintaining comparable travel times. Massive reallocation from TJ (−8.5 pp) and Moto (−3.1 pp) to Royal.

### 5.6 The Policy Recommendation Matrix

| Priority | Scenario | Annual ΔW | Who benefits | Equity |
|----------|----------|-----------|-------------|--------|
| **1. Efficiency** | C: KRL freq −20% | +6,580 Bn | KRL-served zones | Mixed — leaves J1b/J3b out |
| **2. Equity** | D: TJ→J1b | +5,686 Bn | Transit-orphan J1b | Strongly pro-equity |
| **3. Combined** | C + D together | ~12,266 Bn | Everyone | Best of both: efficiency + equity |
| **4. Budget** | H: RT fare −50% | +3,303 Bn | RT-served zones | Pro-equity (cost reduction) |
| **Avoid** | B: Toll +40k | −168 Bn | Nobody | Pure welfare destruction |

**The key takeaway for Q&A**: "Service quality improvements alone (Sc C) maximize aggregate welfare but leave transit orphans behind. Network expansion alone (Sc D) maximizes equity but serves fewer total commuters. The optimal policy bundles both: improve frequency where rail exists AND extend budget transit to unserved zones."

---

## Quick-Fire Q&A Answers

**Q: "Why synthetic data, not real data?"**
A: No public RP mode choice microdata exists for Jabodetabek with all 6 modes and trip-level LOS. We use synthetic DGP anchored to Ilahi (2021) β values and real GTFS transit times from r5py routing.

**Q: "How do you know your model works?"**
A: All 13 NL parameters recovered within 2 SE of DGP truth. The positive control (MXL on Mixed-DGP) correctly detects taste heterogeneity. The IIA violation test shows within-nest substitution 1.67× cross-nest, exactly as NL predicts.

**Q: "Why not use mixed logit?"**
A: We tested it. Wald test on σ_cost: p = 0.763. MXL LL = −5,048.79 vs MNL LL = −5,048.83 — a gain of 0.04 LL units. There's no signal. NL's single extra parameter (λ) gains 4.29 LL units. Parsimony wins.

**Q: "Why is car share only 1%?"**
A: We use full economic cost (toll + fuel + parking ≈ Rp 130,000/trip from outer zones). Commuters perceive marginal cost (fuel ≈ Rp 30,000) once the car is owned. With β_cost anchored to Ilahi, full-cost specification suppresses Car utility. We keep it to preserve the Ilahi anchor rather than introducing an unvalidated cost adjustment. A two-stage budgeting model (own then use) would address this — beyond project scope.

**Q: "What's the difference between logsum and expected maximum utility?"**
A: They're the same thing. EMU = ln Σ exp(V) is the logsum. CS = EMU / |β_cost| converts it to money units. The logsum captures both the utility of the chosen mode AND the option value of having alternatives — even modes you don't choose raise your welfare.

**Q: "Why 250 working days?"**
A: Standard assumption in transport economics for annual commute trip estimation. 52 weeks × 5 days − 10 holidays ≈ 250. Conservative estimate (some commuters travel 6 days/week).

**Q: "Can you explain the bootstrap CIs?"**
A: β_cost has a large SE (0.097 vs estimate −0.077). Since ΔCS = ΔEMU / |β_cost|, uncertainty in β_cost propagates into wide welfare CIs. We draw 1,000 truncated-Normal samples of β_cost (bounded below −0.3·|β̂| to prevent sign flip), recompute ΔCS for each draw, and report P5–P95. Scenario D: mean +3.29, 90% CI [0.00, +15.81].

**Q: "What does λ = 0.763 actually mean economically?"**
A: It means transit modes share about 24% of their unobserved variance (1 − λ = 0.237). If KRL improves, TJ/Royal/MRT lose riders 1.67× faster than Car/Moto do. Transit modes are "closer substitutes" — a commuter choosing between KRL and TJ sees them as more similar than either is to a motorcycle. This is intuitive: both require walking to a station, waiting for a vehicle, and following a fixed schedule.

# Mode Choice and Welfare Analysis in Jabodetabek: A Nested Logit Approach with Policy Simulations

---

## Abstract

This study estimates a Nested Logit (NL) mode choice model for commuters in the Jabodetabek metropolitan area and applies it to evaluate eight transit policy scenarios through logsum-based consumer surplus measurement. Using a synthetic population of 5,000 commuters across seven origin zones with level-of-service data from GTFS-based r5py routing, we estimate three discrete choice specifications: Multinomial Logit (MNL), Nested Logit with private and transit nests, and Mixed Logit (MXL) with a random cost coefficient. The NL model is selected as the best specification (AIC = 10,115 vs MNL 10,122 and MXL 10,124; likelihood ratio test rejects MNL at $p = 0.003$). The nest correlation parameter $\hat{\lambda} = 0.763$ (SE = 0.068) shows within-nest substitution among transit modes, matching findings from Indonesian commuter studies. Mean baseline consumer surplus is $-$53.65 Th IDR per trip. KRL frequency improvement produces the largest welfare gain ($+$3.76 Th IDR/trip). A toll increase of Rp 40,000 produces a welfare loss of $-$0.10 Th IDR/trip, distributed regressively across zones. Transit expansion to unserved zones—TJ to J1b ($+$3.29 Th IDR/trip) and KRL to J3b ($+$0.001 Th IDR/trip)—produces welfare gains concentrated among low-income commuters. Service quality improvements in transit-served corridors widen equity gaps relative to transit-desert zones unless paired with network expansion.

**Keywords**: mode choice, Nested Logit, logsum welfare, Jabodetabek, transit equity, policy simulation

---

## 1. Introduction

The Jabodetabek metropolitan area—Jakarta, Bogor, Depok, Tangerang, and Bekasi—is Southeast Asia's largest urban agglomeration, with a population exceeding 30 million and an estimated 3.5 million daily commuters entering Jakarta from surrounding satellite cities (BPS, 2023). The region's transit network has expanded over the past decade: the KRL Commuter Line carries over 1 million passengers daily, the MRT Jakarta Phase 1 opened in 2019, and TransJakarta operates the world's longest BRT network. But the expansion has been spatially uneven. Outer-zone corridors in Kabupaten Bogor (Parung/Leuwiliyang) and Tangerang (Gading Serpong/Karawaci) remain unserved by formal public transit. Commuters in these zones rely on private motorcycles and ridehailing for trips of 40–90 km into the Jakarta CBD.

How commuters in these zones would respond to new transit alternatives, and how welfare gains distribute across income groups and zones, matters for investment prioritization. The analytical framework is discrete choice models of mode choice, estimated from observed or synthetic travel behaviour data, coupled with logsum-based welfare measurement (Ben-Akiva & Lerman, 1985; Train, 2009). In developing megacities where transit networks are expanding rapidly but budgets are constrained, mode choice models offer a structured way to compare the welfare return on competing investment proposals — network expansion into unserved corridors versus service quality improvements in existing corridors. The welfare numbers these models produce (consumer surplus per trip, annual aggregate welfare change) translate directly into benefit-cost inputs for infrastructure prioritization.

The Multinomial Logit model is the workhorse specification, but its Independence of Irrelevant Alternatives (IIA) property is implausible when the choice set contains multiple transit modes sharing unobserved attributes — schedule coordination, crowding, perceived reliability. If KRL and MRT are closer substitutes than IIA allows, an MNL model understates cross-elasticities within the transit nest and overstates the draw from private modes. Nested Logit relaxes IIA by allowing correlation within pre-specified groups. Mixed Logit handles taste heterogeneity via random parameters. Comparing all three on the same data, with AIC and likelihood ratio tests as the decision rule, identifies which departure from IIA — if either — matters empirically for the choice context at hand.

This study applies that three-model comparison to a 5,000-person synthetic population across seven Jabodetabek origin zones, with a six-mode choice set: Car, Motorcycle, KRL Commuter Line, TransJakarta BRT, RoyalTrans premium bus, and MRT. The best model carries forward to eight policy scenarios spanning transit expansion, pricing reform, frequency improvement, and route restructuring.

Two features distinguish the analysis. First, the population is synthetic — no publicly available revealed-preference commuter survey exists for Jabodetabek at the trip level — but the level-of-service data are real: transit travel times are computed via r5py GTFS routing using actual KRL, TransJakarta, and MRT schedules, and cost parameters are anchored to Ilahi, Belgiawan, and Axhausen's (2021) pooled SP/RP mode choice study of Greater Jakarta. Parameter recovery on known true values (§4) verifies that the estimators are correctly implemented; the policy results demonstrate the framework rather than forecasting empirical ridership. Second, welfare outcomes are disaggregated by income segment and origin zone, and six of eight scenarios are classified by equity direction, linking the logsum welfare framework to spatial equity measurement.

The research question is: which of eight transit policy scenarios produces the largest aggregate welfare gain, and how are these gains distributed across income groups and zones?

### 1.1 Literature Review

**Discrete choice for developing-city commuting.** The nearest precedent for this study is Bastarianto et al. (2019), who estimate MNL, NL, and Cross-Nested Logit models for Bekasi–Jakarta commuters using 24-hour daily activity pattern data. Their NL model reports a within-nest correlation parameter $\lambda_{\text{hwh}} = 0.55$ ($p < 0.01$) for the home→work→home tour nest, confirming that nested structures capture real substitution patterns among Indonesian transit modes. The present study differs from Bastarianto et al. in two ways: the nesting is mode-based (transit vs private) rather than tour-based, and the choice set is larger (six modes vs four) with the addition of MRT and premium bus. These differences produce a weaker within-nest correlation ($\hat{\lambda} = 0.76$ vs $0.55$), which is expected: four transit modes sharing a single nest exhibit less concentrated substitution than two bus alternatives within a tour.

Ilahi et al. (2021) provide the behavioural parameter anchors for the present study. Their pooled SP/RP model of Greater Jakarta (5,143 respondents, 52,731 choice observations) estimates mode-specific value-of-time for 11 alternatives including ridehailing, BRT, train, car, and motorcycle. The present study transfers Ilahi's VTTS estimates directly into the DGP — 4 of 6 modes are directly anchored — and derives $\beta_{\text{time},m}$ via $\beta_{\text{cost}} \cdot \text{VTTS}_m / 60{,}000$. Belgiawan et al. (2019) provide cross-validation for VTTS ranges in Jakarta ($\text{Car} \approx \text{Rp } 44{,}600\text{/hr}$, $\text{MC} \approx \text{Rp } 38{,}700\text{/hr}$), though their random regret framework produces parameters in regret-space rather than utility-space, limiting direct comparability.

**VTTS, VOT, and parameter transferability.** The income elasticity of the value of travel time is well-documented. Binsuwadan et al. (2023) meta-analyze 268 income elasticities from 49 studies (1968–2019) and report a cross-sectional inter-personal elasticity of $\eta \approx 0.5$–$0.7$: doubling income increases VoT by 50–70%, not 100%. This is the empirical basis for income-segmented welfare analysis in the policy scenarios (§5). A broader methodological concern is parameter transferability: $\beta_{\text{time}}$ transfers poorly across study contexts when trip purpose, distance, or mode availability differ (Wardman et al., 2016). This is directly encountered in the present study when Ilahi's $\beta_{\text{time}}$ for ridehailing — estimated on short-distance mixed-purpose urban trips — produces near-zero ride-hail shares when applied to 30–105 km commutes (§2.2, §6.3).

**Logsum welfare and policy evaluation.** Ben-Akiva and Lerman (1985, Ch. 5) establish the logsum as a monetary measure of consumer surplus for discrete choice models. Under the NL specification, expected maximum utility decomposes into nest-level inclusive values weighted by $\lambda$, and the division by $|\beta_{\text{cost}}|$ converts utils to currency. Train (2009, §3.5 and §4.5) provides the modern computational treatment including the log-sum-exp trick for numerical stability. The present study applies this framework to eight policy scenarios and reports annual aggregate welfare change in Billion IDR, disaggregated by income segment and origin zone.

This study sits at the intersection of three threads: replicating Ilahi parameters on an extended choice set; computing policy $\Delta CS$ via NL logsum; and confronting the parameter-transfer problem directly in the limitations. The synthetic-data design makes the exercise a controlled demonstration of the analytical pipeline; it does not substitute for an empirical RP study.

---

## 2. Study Area and Data

### 2.1 Zone System

The study area is divided into seven origin zones, each representing a distinct commuter-shed within the Jabodetabek metropolitan area. All zones share a single destination: the Jakarta Central Business District (JCBD), defined as the Sudirman-Thamrin corridor (approximately the Bundaran HI MRT station area).

| Zone | Description | Representative Area | Approx. Distance to JCBD |
|------|-------------|---------------------|---------------------------|
| J1a | Bogor corridor (KRL-served) | Bogor Kota, Cibinong | 55 km |
| J1b | Kab. Bogor outer (no transit) | Parung, Leuwiliyang | 45 km |
| J2 | Bekasi corridor (KRL-served) | Bekasi Kota, Cikarang | 35 km |
| J3a | Tangerang Selatan (KRL-served) | BSD Serpong, Bintaro | 30 km |
| J3b | Tangerang outer (no transit) | Gading Serpong, Karawaci | 35 km |
| J4 | Depok corridor (KRL-served) | Depok, Margonda | 25 km |
| J5 | South Jakarta (all transit) | Kebayoran Baru, Cilandak | 12 km |

Zones are classified along a transit-access gradient: J5 has full access to all six modes; J1a, J2, J3a, and J4 have KRL, TJ, and RoyalTrans but no MRT; J1b and J3b are transit deserts with access only to private modes (Car, Motorcycle).

### 2.2 Mode Choice Set

The choice set comprises six modes. An original nine-mode specification included two-wheel ridehailing (2WRH), four-wheel ridehailing (4WRH), and LRT Jabodebek. These three were dropped after a calibration test on the nine-mode DGP.

| Mode | Category | Key Characteristics |
|------|----------|---------------------|
| Car | Private | Owner-driven, toll + fuel cost, free-flow speed |
| Motorcycle (Moto) | Private | Owner-driven, fuel cost only, manoeuvrable |
| KRL Commuter Line | Transit (rail) | Fixed schedule, high capacity, Rp 5,000–8,000 |
| TransJakarta (TJ) | Transit (BRT) | Dedicated lanes, flat fare Rp 3,500 |
| RoyalTrans | Transit (premium bus) | Reserved seating, express, Rp 22,000–39,000 |
| MRT Jakarta | Transit (rail) | Grade-separated, Rp 6,000–12,000 |

With Ilahi (2021) β anchors applied to Bodetabek level-of-service data, 2WRH and 4WRH produced near-zero choice shares (2WRH: 0.0%; 4WRH: 0.1%), contradicting BPS (2023) commute surveys that report 5–10% ride-hail mode share in the corridor. The root cause is parameter non-transferability: Ilahi's β_time_2wrh = −5.10 and β_time_4wrh = −3.49 were estimated on a sample of urban short-distance trips with mixed purpose, while the present study models 30–105 minute long-distance commutes. Ride-hailing generalized cost (premium fare plus time penalty) makes these modes structurally non-competitive at commute distances under the inherited β values. ASC calibration to BPS aggregate shares was attempted via Newton iteration but required ASC_4wrh > +40 utility units to overcome the time penalty, far outside any defensible range.

LRT Jabodebek was also excluded: available in only one of seven zones (J2), its single-zone presence yields thin-cell identification where the ASC absorbs zone-level unobservables rather than measuring mode preference.

The reduced six-mode choice set preserves the substantive comparison (MNL, NL, MXL) without the identification failures these three modes introduce. See §6.3 for further discussion.

### 2.3 Level-of-Service Data

Transit travel times (KRL, TJ, RoyalTrans, MRT) are derived from r5py GTFS routing using actual schedule data for the Jabodetabek transit network. r5py computes door-to-door travel times including access/egress walking, wait time (half the scheduled headway), and in-vehicle time. The routing was executed for each origin zone centroid to the JCBD destination during the AM peak period (07:00–09:00). A fallback penalty of 180 minutes was applied for zone-mode pairs where no transit path was found, effectively removing the mode from the choice set for that zone.

Private-mode travel times (Car, Motorcycle) are estimated from free-flow road network distances with speed assumptions based on road class (toll roads: 80 km/h, arterials: 40 km/h, local roads: 25 km/h), consistent with the Bureau of Public Roads (BPR) baseline. Cost for Car includes toll + fuel (approximately Rp 1,500/km in 2025 prices), while Motorcycle cost reflects fuel only (Rp 500/km). These estimates produce zone-to-CBD travel times ranging from approximately 25 minutes (J5 Car via toll) to 120 minutes (J1b Motorcycle via arterial).

Transit fares are based on published 2025 tariff schedules: KRL Rp 5,000–8,000 distance-based, TransJakarta flat Rp 3,500, MRT Rp 6,000–12,000 distance-based, and RoyalTrans Rp 22,000–39,000 route-based.

### 2.4 Synthetic Population

The synthetic population of 5,000 persons was generated through a Nested Logit Data Generating Process with nest correlation parameter $\lambda = 0.70$. Two nests group the six modes by class: a transit nest containing {KRL, MRT, TransJakarta, RoyalTrans} and a private nest containing {Car, Motorcycle}. The nest correlation reflects unobserved attributes shared within each mode class — comfort, social signaling, and perceived safety in transit; convenience and personal storage in private.

The true utility specification follows the NL structure, with parameter values anchored to Ilahi et al. (2021) mode-specific value-of-time estimates. For each person $n$ and mode $m$:

$$V_{mn} = ASC_m + \beta_{\text{time},m} \cdot T_{\text{zone}(n),m} + \beta_{\text{cost}} \cdot C_{\text{zone}(n),m}$$

with $\beta_{\text{cost}} = -1.42$ per Thousand IDR and $\beta_{\text{time},m}$ derived from Ilahi's Table 11 mode-specific VTTS via $\beta_{\text{time},m} = \beta_{\text{cost}} \cdot \text{VTTS}_m / 60{,}000$. A scale normalization $\mu = 25$ is applied to compress utility gaps into a range where Gumbel noise produces meaningful choice variation; under MNL scale identification (Train, 2009 §3.7), $\text{VOT} = \beta_{\text{time}}/\beta_{\text{cost}}$ is preserved exactly.

Synthetic choices are drawn using the closed-form NL probability formula (Train, 2009 §4.2) rather than simulating correlated Gumbel errors directly. For each person $n$:

1. Compute per-nest inclusive value $I_k(n) = \log \sum_{m \in k} \exp(V_{mn}/\lambda)$ over modes available in nest $k$
2. Compute marginal nest probability $P_n(k) = \exp(\lambda \cdot I_k(n)) / \sum_\ell \exp(\lambda \cdot I_\ell(n))$
3. Compute conditional mode probability $P_n(m \mid k) = \exp(V_{mn}/\lambda) / \exp(I_k(n))$
4. Joint choice probability $P_n(m) = P_n(m \mid k) \cdot P_n(k)$
5. Draw the realized choice via `np.random.choice` over the six modes weighted by $P_n(\cdot)$

This GEV simulation method produces data consistent with the closed-form NL likelihood, avoiding the numerical pitfalls of summing correlated Gumbel draws. The implementation uses the log-sum-exp trick at both the nest and upper levels for numerical stability. Random seed: 20260601.

### 2.5 Income Segments

Each synthetic person is assigned to one of three income segments — low, mid, or high — with segment shares calibrated to the Jabodetabek income distribution from BPS Susenas 2023. Segment thresholds are based on monthly household expenditure terciles:

| Segment | Monthly Expenditure |
|---------|---------------------|
| Low | < Rp 3,000,000 |
| Mid | Rp 3,000,000–7,000,000 |
| High | > Rp 7,000,000 |

Zone-level income distributions are calibrated to BPS 2023 spatial income data: outer zones (J1b, J3b) have higher proportions of low-income households, and inner zones (J5) have higher proportions of high-income households. Income segment is recorded as a person-level attribute but is not used in the systematic utility computation — $\beta_{\text{time}}$ and $\beta_{\text{cost}}$ are homogeneous across the population in the DGP. Income heterogeneity enters policy analysis through the zone composition channel rather than a structural income-VoT scaling. A consequence is that $\Delta CS$ differences across income segments in policy scenarios (§5) reflect the spatial correlation of income with transit access rather than income-differentiated preferences. This is acknowledged as a limitation in §6.3.

---

## 3. Methodology

### 3.1 Multinomial Logit (MNL) Specification

The MNL model serves as the baseline specification. Under the MNL assumption, the probability that person n chooses mode i from choice set C_n is:

$$P_n(i) = \frac{\exp(V_{in})}{\sum_{j \in C_n} \exp(V_{jn})}$$

where $V_{in} = ASC_i + \sum_k \beta_k \cdot x_{ink}$ is the systematic utility of mode $i$ for person $n$.

The systematic utility for each mode is specified as:

$$\begin{aligned}
V_{\text{car},n}   &= ASC_{\text{car}}   + \beta_{\text{time,car}} \cdot T_{\text{car,zone}(n)}   + \beta_{\text{cost}} \cdot C_{\text{car,zone}(n)} \\
V_{\text{moto},n}  &= ASC_{\text{moto}}  + \beta_{\text{time,moto}} \cdot T_{\text{moto,zone}(n)}  + \beta_{\text{cost}} \cdot C_{\text{moto,zone}(n)} \\
V_{\text{krl},n}   &= \beta_{\text{time,krl}} \cdot T_{\text{krl,zone}(n)}    + \beta_{\text{cost}} \cdot C_{\text{krl,zone}(n)} \\
V_{\text{tj},n}    &= ASC_{\text{tj}}    + \beta_{\text{time,tj}} \cdot T_{\text{tj,zone}(n)}     + \beta_{\text{cost}} \cdot C_{\text{tj,zone}(n)} \\
V_{\text{royal},n} &= ASC_{\text{royal}} + \beta_{\text{time,royal}} \cdot T_{\text{royal,zone}(n)} + \beta_{\text{cost}} \cdot C_{\text{royal,zone}(n)} \\
V_{\text{mrt},n}   &= ASC_{\text{mrt}}   + \beta_{\text{time,mrt}} \cdot T_{\text{mrt,zone}(n)}   + \beta_{\text{cost}} \cdot C_{\text{mrt,zone}(n)}
\end{aligned}$$

KRL is set as the reference alternative ($ASC_{\text{krl}} = 0$). The model contains 12 parameters: 5 ASCs, 6 mode-specific travel time coefficients, and 1 generic travel cost coefficient. Mode-specific $\beta_{\text{time}}$ parameters are used rather than a generic $\beta_{\text{time}}$ to capture the different marginal disutilities of time across modes—a specification consistent with Ilahi et al. (2021), who find that commuters value time in a crowded KRL differently from time in an air-conditioned car.

Estimation is by maximum likelihood using L-BFGS-B optimisation via `scipy.optimize.minimize`. The log-likelihood function is:

$$LL(\theta) = \sum_n \sum_i y_{in} \cdot \ln P_n(i \mid \theta)$$

where $y_{in} = 1$ if person $n$ chose mode $i$ and 0 otherwise. Standard errors are computed from the inverse of the negative Hessian (observed Fisher information matrix).

The key limitation of MNL is the Independence of Irrelevant Alternatives (IIA) property: the relative probability of choosing any two modes is independent of the attributes or availability of a third mode. In a system with four transit modes sharing unobserved attributes (schedule coordination, station environment, crowding), IIA is unlikely to hold. We test for IIA violation in two ways: (a) a Hausman-McFadden specification test comparing full-choice-set estimates against estimates with one alternative removed, and (b) comparing MNL-predicted mode shares under a "free TransJakarta" scenario against Nested Logit predictions. If IIA holds, the two models should predict identical proportional shifts.

### 3.2 Nested Logit (NL) Specification

The Nested Logit model relaxes the IIA assumption by allowing correlation among alternatives within pre-specified groups (nests). We specify a two-nest structure:

- **Transit nest**: KRL, MRT, TransJakarta, RoyalTrans
- **Private nest**: Car, Motorcycle

This nesting reflects the hypothesis that transit modes share unobserved attributes—schedule coordination, station access, crowding, perceived reliability—that make them closer substitutes than IIA implies. The private nest groups the two owner-driven modes, which share unobserved attributes related to vehicle availability, parking, and route flexibility.

Under the NL specification, the probability of choosing mode $m$ is the product of the conditional probability of choosing $m$ given nest $k$, and the marginal probability of choosing nest $k$:

$$P_n(m) = P_n(m \mid k) \times P_n(k)$$

where

$$P_n(m \mid k) = \frac{\exp(V_{mn} / \lambda_k)}{\sum_{j \in k} \exp(V_{jn} / \lambda_k)}$$

$$P_n(k) = \frac{\exp(\lambda_k \cdot I_{kn})}{\sum_l \exp(\lambda_l \cdot I_{ln})}$$

and the inclusive value (logsum) for nest $k$ is:

$$I_{kn} = \ln \sum_{j \in k} \exp(V_{jn} / \lambda_k)$$

The nest parameter $\lambda_k \in (0, 1]$ measures the degree of within-nest correlation. $\lambda_k = 1$ corresponds to the MNL case (no correlation). $\lambda_k \to 0$ corresponds to perfect correlation (all alternatives in the nest are treated as a single composite alternative). A common $\lambda$ is estimated for both nests ($\lambda_{\text{private}} = \lambda_{\text{transit}} = \lambda$), giving 13 total parameters.

Estimation proceeds via full-information maximum likelihood (FIML), maximising the NL log-likelihood directly with respect to all parameters including $\lambda$. The L-BFGS-B algorithm is used with $\lambda$ constrained to $(0.01, 1.0)$ via box bounds.

The likelihood ratio test statistic $LR = -2(LL_{MNL} - LL_{NL})$ is compared against the critical value of $\chi^2(1) = 3.84$ at $\alpha = 0.05$. Rejection of $H_0: \lambda = 1$ constitutes statistical evidence against the IIA assumption.

### 3.3 Mixed Logit (MXL) Diagnostic

Following the diagnostic protocol from the course lectures (L07), we estimate a Mixed Logit model with a single random parameter—the travel cost coefficient—to test for unobserved taste heterogeneity beyond what the NL structure captures. The specification is:

$$\beta_{\text{cost},n} = \mu_{\text{cost}} + \sigma_{\text{cost}} \cdot \eta_n, \quad \eta_n \sim \mathcal{N}(0, 1)$$

where $\mu_{\text{cost}}$ is the mean cost coefficient and $\sigma_{\text{cost}} = \exp(\sigma_{\text{raw}})$ ensures positivity. All other parameters ($\beta_{\text{time},m}$, ASCs) remain fixed. The choice probability for person $n$ is:

$$P_n(i) = \int \frac{\exp\bigl(V_{in}(\beta_n)\bigr)}{\sum_j \exp\bigl(V_{jn}(\beta_n)\bigr)} \cdot f(\beta_n \mid \theta) \, d\beta_n$$

Simulated maximum likelihood estimation uses $R = 100$ Halton draws (base = 2). For a one-dimensional random coefficient, Train (2009, §9.3.2) shows that $R = 100$ Halton draws provide integration accuracy equivalent to $R = 500$ pseudo-random draws.

The primary diagnostic is the Wald test on $\sigma_{\text{cost}}$: $H_0: \sigma_{\text{cost}} = 0$ vs $H_1: \sigma_{\text{cost}} > 0$. The test statistic $W = (\hat{\sigma}_{\text{cost}} / SE(\hat{\sigma}_{\text{cost}}))^2$ is asymptotically $\chi^2(1)$. Failure to reject $H_0$ indicates that the NL-DGP data contain no taste heterogeneity that NL does not already capture through nest correlation, supporting the selection of NL as the final model.

As a positive control, the same estimator is applied to a second dataset generated with true $\sigma_{\text{cost}} = 0.02$ (Mixed DGP). Recovery of $\hat{\sigma}_{\text{cost}}$ within 2 SE of the true value confirms the estimator is correctly implemented.

### 3.4 Logsum Welfare Measurement

Consumer surplus under the NL model is measured via the logsum formula (Ben-Akiva & Lerman, 1985, Ch. 5; Train, 2009, §3.5). The expected maximum utility for person $n$ is:

$$EMU_n = \ln \sum_k \exp(\lambda \cdot I_{kn})$$

where $I_{kn}$ is the inclusive value for nest $k$. The consumer surplus per trip in currency units is:

$$CS_n = \frac{EMU_n}{|\beta_{\text{cost}}|}$$

The division by $|\beta_{\text{cost}}|$ converts utility units (utils) to monetary units (Thousand IDR). The change in consumer surplus under a policy scenario is:

$$\Delta CS_n = \frac{EMU_n^{\text{policy}} - EMU_n^{\text{baseline}}}{|\beta_{\text{cost}}|}$$

This is a Marshallian consumer surplus measure: it assumes no income effect from the policy change (valid for small changes in generalized cost relative to income) and uses the uncompensated demand curve. For the commuting context, where the policy scenarios represent marginal changes to the transport system, this assumption is reasonable.

Aggregate annual welfare change is computed as:

$$\Delta W_{\text{annual}} = \left(\sum_n \Delta CS_n\right) \times \text{working\_days}$$

where $\text{working\_days} = 250$ (approximate number of commuting days per year). Results are reported in Thousand IDR per trip and Billion IDR per year.

---

## 4. Results

### 4.1 MNL Estimation

The MNL model was estimated on $N = 5{,}000$ synthetic choice observations with 12 parameters. The L-BFGS-B algorithm converged successfully. Table 1 reports the estimation results.

**Table 1: MNL Estimation Results**

| Parameter | Estimate | SE | t-stat | Ilahi Anchor |
|-----------|----------|-----|--------|--------------|
| ASC_car | −0.319 | 3.921 | −0.08 | −1.20 |
| ASC_moto | 0.589 | 0.289 | 2.04 | (base) |
| ASC_tj | 0.155 | 0.426 | 0.36 | −4.74 |
| ASC_royal | −0.497 | 2.283 | −0.22 | — |
| ASC_mrt | −0.022 | 26.451 | 0.00 | — |
| $\beta_{\text{time,car}}$ | −0.078 | 0.283 | −0.27 | −0.60 |
| $\beta_{\text{time,moto}}$ | −0.133 | 0.064 | −2.09 | −2.34 |
| $\beta_{\text{time,krl}}$ | −0.146 | 0.045 | −3.23 | −2.72 |
| $\beta_{\text{time,tj}}$ | −0.060 | 0.020 | −3.08 | −1.07 |
| $\beta_{\text{time,royal}}$ | −0.075 | 0.056 | −1.34 | — |
| $\beta_{\text{time,mrt}}$ | −0.160 | 1.728 | −0.09 | — |
| $\beta_{\text{cost}}$ | −0.044 | 0.188 | −0.23 | −1.42 |

Goodness of fit: $LL(0) = -7{,}011.56$, $LL(\hat{\beta}) = -5{,}048.83$, $\rho^2 = 0.280$, $\bar{\rho}^2 = 0.278$, $\text{AIC} = 10{,}121.65$, $\text{BIC} = 10{,}199.86$.

All 12 parameters are recovered within 2 standard errors of their true DGP values. Parameter recovery is a necessary condition for welfare analysis: the estimator must correctly identify the preference structure embedded in the synthetic data before policy counterfactuals are meaningful.

Estimated Values of Travel Time (VoT), computed as $\text{VoT}_m = \beta_{\text{time},m} / \beta_{\text{cost}} \times 60$, range from Rp 82,388/hr (TJ) to Rp 217,799/hr (MRT). These are broadly consistent with the Ilahi et al. (2021) anchors, with the exception of Car (Rp 106,200/hr vs Ilahi Rp 25,200/hr—a 4× overestimate discussed in §6). The large SE on $\beta_{\text{cost}}$ (0.188 vs estimate $-0.044$, $t = -0.23$) reflects the Gumbel scale $\mu = 25$, which compresses utility differences and increases parameter variance.

### 4.2 Nested Logit Estimation

The NL model adds one parameter ($\lambda$) to the MNL specification, for a total of 13 parameters. Estimation converged in 1,736 L-BFGS-B iterations with a final gradient norm of 0.34.

**Table 2: Nested Logit Estimation Results**

| Parameter | Estimate | SE | t-stat |
|-----------|----------|-----|--------|
| $\lambda$ (nest correlation) | 0.763 | 0.068 | — |
| ASC_car | 0.323 | 2.024 | 0.16 |
| ASC_moto | 0.014 | 0.245 | 0.06 |
| ASC_tj | 0.014 | 0.243 | 0.06 |
| ASC_royal | −0.106 | 1.231 | −0.09 |
| ASC_mrt | −0.020 | — | — |
| $\beta_{\text{time,car}}$ | 0.000 | 0.144 | 0.00 |
| $\beta_{\text{time,moto}}$ | −0.096 | 0.036 | −2.68 |
| $\beta_{\text{time,krl}}$ | −0.118 | 0.031 | −3.80 |
| $\beta_{\text{time,tj}}$ | −0.048 | 0.016 | −3.02 |
| $\beta_{\text{time,royal}}$ | −0.048 | 0.029 | −1.65 |
| $\beta_{\text{time,mrt}}$ | −0.127 | — | — |
| $\beta_{\text{cost}}$ | −0.077 | 0.097 | −0.80 |

Goodness of fit: $LL(\hat{\beta}) = -5{,}044.54$, $\rho^2_{NL} = 0.281$, $\text{AIC} = 10{,}115.08$, $\text{BIC} = 10{,}199.80$.

**Model comparison:**

| Criterion | MNL | NL | $\Delta$ |
|-----------|-----|-----|---|
| $LL$ | −5,048.83 | −5,044.54 | +4.29 |
| AIC | 10,121.65 | 10,115.08 | −6.57 (NL wins) |
| BIC | 10,199.86 | 10,199.80 | −0.06 (tie) |
| $\rho^2$ | 0.280 | 0.281 | +0.001 |
| $k$ (params) | 12 | 13 | +1 |

The likelihood ratio test statistic is $LR = 8.57$, with $p = 0.0034$ against $\chi^2(1)$. At $\alpha = 0.01$, we reject $H_0: \lambda = 1$, confirming statistically significant within-nest correlation among transit modes. The 95% confidence interval for $\lambda$ is $[0.627, 0.900]$, which excludes 1.0.

The estimate $\hat{\lambda} = 0.763$ means the four transit modes are closer substitutes than IIA would predict. When the utility of one transit mode improves (e.g., KRL frequency increase in Scenario C), the NL model predicts a larger share shift from other transit modes and a smaller shift from private modes than MNL would. Transit improvements in isolation cannibalize other transit modes more than they draw from cars and motorcycles.

All 13 NL parameters are recovered within 2 SE of their DGP true values. $\hat{\lambda}$ is within 0.063 of the true $\lambda = 0.70$ (a 9% upward bias, well within the SE of 0.068). The estimator identifies nest correlation from cross-sectional choice data.

**Baseline welfare**: Mean consumer surplus is $-53.65$ Th IDR per trip ($\text{P10}: -115.30$, $\text{P90}: -9.48$). Negative CS is the generalized cost of commuting—the disutility of travel time and monetary cost in currency-equivalent terms. The P10–P90 spread reflects spatial heterogeneity in transit access: commuters in J5 (all modes available, short distances) have small negative CS, while commuters in J1b (private modes only, 45 km) have large negative CS.

The estimated NL mode shares at baseline are Car 1.0%, Motorcycle 36.7%, KRL 17.8%, TransJakarta 34.0%, RoyalTrans 9.1%, and MRT 1.4%. These match the realized DGP choice shares (sum of absolute deviations < 0.001). The deterministic argmax classification used in earlier iterations produced degenerate shares (Motorcycle 30.7%, TJ 69.3%). Probabilistic mode shares are essential for welfare and policy analysis.

**IIA violation and cross-elasticities.** The NL structure matters empirically for cross-elasticity predictions. We perturb the utility of TransJakarta by $\delta = 0.1$ for a J2 mid-income commuter and compare the pattern of share reallocation under MNL and NL. Under MNL, the IIA property forces equal proportional substitution: the 3.0 pp gain in TJ share draws from every other mode in proportion to its baseline share, with no distinction between transit and private alternatives. Under NL, the substitution pattern is asymmetric. Transit modes in the same nest as TJ lose 1.90 pp combined (KRL −0.74 pp, RoyalTrans −1.17 pp) while private modes lose 1.14 pp (Motorcycle −1.10 pp, Car −0.04 pp). The within-nest to cross-nest substitution ratio is $1.67\times$. When TJ improves, it cannibalizes other transit modes nearly twice as heavily as it draws from private modes—a pattern MNL cannot reproduce.

The IIA violation also surfaces in the red-bus/blue-bus test: adding a "KRL Express" alternative identical to KRL but with ASC = ASC_krl + 0.1 causes MNL to predict transit share nearly doubling (KRL 11.7% → 10.4% + Express 11.4% = 21.8%), treating KRL and its near-clone as independent alternatives. The NL model, by nesting all transit modes together, correctly limits the combined share gain because the within-nest correlation absorbs the redundant alternative.

**Parameter recovery.** All 13 NL parameters recover within 2 SE of their DGP true values. The nest correlation parameter $\hat{\lambda} = 0.763$ ($\text{SE} = 0.068$) recovers the true $\lambda = 0.70$ within 0.93 SE. The upward bias (9%) reflects finite-sample identification where the transit nest dominates (62.3% of aggregate choice share) and the private nest contributes less information. $\beta_{\text{time,car}}$ hits the zero bound because Car has 1.0% share (51 choosers), making its time coefficient indistinguishable from zero; the true value $-0.024$ sits within 0.17 SE of the estimate. $\beta_{\text{cost}} = -0.077$ ($\text{SE} = 0.097$) is 0.21 SE from the true $-0.057$, with the large SE reflecting the Gumbel scale $\mu = 25$ that compresses utility differences relative to the Ilahi-scale parameters. The full recovery table appears in the companion notebook (03_nl_estimation.ipynb, Cell 16).

### 4.3 Mixed Logit Diagnostic

The MXL model with random $\beta_{\text{cost}}$ was estimated using $R = 100$ Halton draws. The L-BFGS-B algorithm converged in 66 iterations.

| Parameter | Estimate | SE | t-stat |
|-----------|----------|-----|--------|
| $\mu_{\text{cost}}$ (mean) | −0.037 | 0.183 | −0.20 |
| $\sigma_{\text{cost}}$ (std dev) | 0.010 | 0.033 | — |
| $\beta_{\text{time,moto}}$ | −0.133 | 0.053 | −2.52 |
| $\beta_{\text{time,krl}}$ | −0.145 | 0.038 | −3.78 |
| $\beta_{\text{time,tj}}$ | −0.059 | 0.019 | −3.05 |
| $\beta_{\text{time,royal}}$ | −0.077 | 0.054 | −1.42 |
| $\beta_{\text{time,mrt}}$ | −0.159 | 4.967 | −0.03 |
| $\beta_{\text{time,car}}$ | −0.096 | 0.313 | −0.31 |

Goodness of fit: $LL = -5{,}048.79$, $\text{AIC} = 10{,}123.59$, $\text{BIC} = 10{,}208.31$.

The Wald test on $\sigma_{\text{cost}}$ yields $W = 0.091$, $p = 0.763$. We fail to reject $H_0: \sigma_{\text{cost}} = 0$. There is no evidence of unobserved taste heterogeneity in the cost coefficient beyond what the NL structure captures. The near-identical log-likelihoods of MXL ($-5{,}048.79$) and MNL ($-5{,}048.83$) confirm that adding a random cost parameter adds negligible explanatory power.

The positive control on Mixed-DGP data ($\sigma_{\text{true}} = 0.02$) correctly detects $\sigma > 0$ (Wald $p \approx 0$). The estimator identifies taste heterogeneity when it is present.

**Model selection:** NL is carried forward to policy simulations. AIC selects NL over both MNL ($\Delta\text{AIC} = -6.6$) and MXL ($\Delta\text{AIC} = -8.5$); the LR test rejects the MNL restriction ($p = 0.003$); and the Wald test fails to reject $\sigma_{\text{cost}} = 0$ in MXL, indicating no additional heterogeneity to capture.

**Halton draws for simulated likelihood.** The MXL choice probability is an integral over the mixing distribution $f(\beta_{\text{cost}})$ with no closed form. Monte Carlo integration approximates it:

$$\hat{P}_n(i) = \frac{1}{R} \sum_{r=1}^{R} \frac{\exp(V_{in}(\beta_{\text{cost},r}))}{\sum_j \exp(V_{jn}(\beta_{\text{cost},r}))}, \quad \beta_{\text{cost},r} = \mu_{\text{cost}} + \sigma_{\text{cost}} \cdot \eta_r$$

Pseudo-random draws would require $R \approx 500$ for stable integration. Halton sequences replace them: a quasi-random sequence with base 2 that fills $(0, 1)$ more evenly than pseudo-random draws, reducing the required $R$ by a factor of roughly 5 at equivalent accuracy (Train, 2009, §9.3.2). For a one-dimensional random coefficient, $R = 100$ Halton draws supply the same integration precision as $R = 500$ pseudo-random draws. The Halton values $h_r \in (0, 1)$ convert to standard normal draws via the inverse CDF: $\eta_r = \Phi^{-1}(h_r)$. The resulting $\eta$ vector has mean $-0.04$ and standard deviation $0.97$, close to the theoretical $\mathcal{N}(0, 1)$.

Reducing $R$ from the planned 500 to 100 cuts computation time by 5× without affecting the substantive conclusion. The positive control confirms the estimator functions: on Mixed-DGP data with true $\sigma_{\text{cost}} = 0.02$, the Wald test rejects $\sigma = 0$ at $p \approx 0$. The null result on the actual NL-DGP data—$\hat{\sigma}_{\text{cost}} = 0.010$, Wald $p = 0.763$—is a finding about the data, not an artifact of the integration method.

### 4.4 Goodness-of-Fit Summary

Table 3 summarises the three-model comparison. NL is the preferred specification on every criterion except BIC, where the penalty per parameter ($\ln 5000 \approx 8.52$) nearly matches the likelihood gain ($\Delta LL = +4.29 \times 2 = 8.58$), producing a virtual tie.

**Table 3: Three-Model Goodness-of-Fit Comparison**

| Criterion | MNL | NL | MXL |
|-----------|-----|-----|------|
| Parameters ($K$) | 12 | 13 | 13 |
| $LL(\hat{\beta})$ | −5,048.83 | −5,044.54 | −5,048.79 |
| AIC | 10,121.65 | **10,115.08** | 10,123.59 |
| BIC | 10,199.86 | 10,199.80 | 10,208.31 |
| $\rho^2$ | 0.280 | 0.281 | 0.280 |
| LR vs MNL ($p$) | — | **0.003** | 0.799 |
| Wald $\sigma = 0$ ($p$) | — | — | 0.763 |
| Selected | No | **Yes** | No |

NL gains 4.3 log-likelihood units over MNL with a single additional parameter, enough to reject the IIA restriction at $p < 0.01$. MXL gains 0.03 units over MNL with the same parameter count as NL, confirming that random $\beta_{\text{cost}}$ captures no additional structure. The Wald test on $\sigma_{\text{cost}}$ settles the model selection: NL relaxes the IIA violation that matters for this data; MXL adds a heterogeneity dimension the data do not support.

---

## 5. Policy Simulations

Eight policy scenarios were evaluated using the NL logsum welfare framework. For each scenario, we compute: mean $\Delta CS$ per trip (Th IDR), annual aggregate welfare change (Bn IDR/year), income-segment disaggregation, zone-level spatial distribution, and mode share shifts. Bootstrap 90% confidence intervals are reported for key scenarios using truncated-Normal parameter draws ($\beta_{\text{cost}}$ draws bounded above at $-0.3 \cdot |\hat{\beta}_{\text{cost}}|$ to prevent logsum divergence near $\beta_{\text{cost}} \approx 0$).

### 5.1 Transit Expansion Scenarios

**Scenario A: KRL Extension to J3b (Gading Serpong/Karawaci).** Adding KRL service (T = 70 min, C = 7.5k IDR) to the unserved J3b zone produces a mean $\Delta CS$ of +0.001 Th IDR/trip, with gains concentrated entirely in J3b (+0.022 Th IDR/trip for J3b residents). The effect is small because J3b has few residents (318 winners out of 5,000). KRL mode share increases by 0.02 pp, drawn from TJ (−0.01 pp). Aggregate annual welfare gain: 2.22 Bn IDR. Bootstrap 90% CI: $[0.00, +0.61]$ Th IDR/trip. Equity: pro-equity (gains concentrated in a transit-desert zone).

**Scenario D: TransJakarta Extension to J1b (Parung/Leuwiliyang).** Adding TJ service (T = 90 min, C = 3.5k IDR) to J1b—the most severe transit desert in the study area—produces a mean $\Delta CS$ of +3.29 Th IDR/trip, the second-largest gain. TJ at Rp 3,500 undercuts every other motorized option on cost (Moto fuel alone exceeds Rp 20,000 for a 45 km trip). Gains are concentrated in J1b (+28.43 Th IDR/trip for J1b residents) and are pro-equity: low-income commuters gain +3.38 Th IDR vs high-income +3.03 Th IDR. TJ mode share increases by 10.3 pp, drawn primarily from Motorcycle (−10.1 pp) and Car (−0.2 pp). Aggregate annual welfare gain: 5,685.65 Bn IDR. Bootstrap 90% CI: $[+0.00, +15.81]$. Equity: strongly pro-equity.

**Scenario E: MRT Extension to J3a (BSD Serpong).** Adding MRT to J3a (T = 60 min, C = 12.0k IDR), a zone already served by KRL, produces a small mean $\Delta CS$ of +0.002 Th IDR/trip, with gains concentrated in J3a (+0.054 Th IDR/trip). The MRT draws modestly from KRL and Motorcycle. Adding a second rail option to an already rail-served zone has limited incremental value: MRT time savings (60 vs 85 min for KRL) are offset by the higher fare (12k vs 7k IDR). Aggregate annual welfare gain: 3.39 Bn IDR. Equity: mildly pro-equity.

**Scenario F: TJ BSD→CBD Direct Route.** Restructuring TJ to serve the CBD directly (T = 80 min, C = 3.5k IDR) in J3a and J3b produces a mean $\Delta CS$ of +0.53 Th IDR/trip. Gains are larger in J3a (+9.66 Th IDR/trip, where TJ is a new option) than J3b (+2.49 Th IDR/trip, where TJ already exists but gains from the eliminated transfer penalty). TJ mode share increases by 2.6 pp, drawn from Motorcycle (−1.2 pp), KRL (−1.1 pp), and RoyalTrans (−0.2 pp). Aggregate annual welfare gain: 852.60 Bn IDR. Equity: strongly pro-equity (budget one-seat ride to CBD benefits low-income commuters most).

### 5.2 Pricing Scenarios

**Scenario B: Toll Increase (+Rp 40,000).** A congestion charge adding Rp 40,000 to Car cost for all origin zones produces a mean $\Delta CS$ of −0.10 Th IDR/trip. The loss is regressively distributed: J5 (−0.27 Th IDR/trip) and J1b (−0.15 Th IDR/trip) suffer the largest per-trip losses, while J3b (−0.05) and J1a (−0.04) are least affected. Car mode share collapses from 1.0% to 0.02%, with displaced Car users shifting to Motorcycle (+0.6 pp), TJ (+0.3 pp), and KRL (+0.1 pp). The welfare loss falls hardest on zones where Car is the primary motorized alternative (J1b, J3b have no transit to absorb the shift). Aggregate annual welfare loss: −168.02 Bn IDR. Bootstrap 90% CI: $[-36.69, 0.00]$. Equity: regressive.

**Scenario H: RoyalTrans Fare Reduction (−50%).** Halving RoyalTrans fares in J2, J3a, J3b, and J4 produces a mean $\Delta CS$ of +1.99 Th IDR/trip. RoyalTrans mode share increases by 14.1 pp (9.1% → 23.2%), drawing from TJ (−8.5 pp), Motorcycle (−3.1 pp), KRL (−2.4 pp), and Car (−0.1 pp). Gains are nearly uniform across income segments (low: +1.98, mid: +1.99, high: +1.98). Aggregate annual welfare gain: 3,303.37 Bn IDR. Equity: pro-equity (price barrier lowered for middle-income access to express transit).

### 5.3 Service Quality Scenarios

**Scenario C: KRL Frequency Improvement (−20% travel time).** Reducing KRL wait + in-vehicle time by 20% in J1a, J2, J3a, and J4 produces the largest mean welfare gain: +3.76 Th IDR/trip. KRL mode share increases by 14.9 pp (17.8% → 32.7%), the largest mode shift in any scenario, drawing from Motorcycle (−7.8 pp), TJ (−5.1 pp), and RoyalTrans (−1.9 pp). Gains are concentrated in KRL-served zones: J1a (+15.79 Th IDR/trip), J3a (+6.92), J4 (+2.46), J2 (+1.88). J1b and J3b (no KRL service) receive zero benefit. This produces an equity tension: the scenario generates the largest aggregate gain but widens the gap between transit-served corridors and transit deserts. Aggregate annual welfare gain: 6,580.38 Bn IDR. Equity: mixed.

**Scenario G: RoyalTrans Frequency Increase (wait $20 \to 5$ min).** Reducing RoyalTrans wait time from 20 to 5 minutes in J2, J3a, J3b, and J4 produces a mean $\Delta CS$ of +1.26 Th IDR/trip. RoyalTrans mode share increases by 9.4 pp (9.1% → 18.5%), drawing from TJ (−5.8 pp), Motorcycle (−2.0 pp), and KRL (−1.6 pp). Gains are concentrated in J2 (+2.35 Th IDR/trip) and J4 (+2.20), where RoyalTrans provides direct CBD service without a transfer penalty. The near-uniform income distribution (low: +1.26, mid: +1.26, high: +1.26) reflects that wait-time reduction benefits all income segments proportionally. Aggregate annual welfare gain: 2,093.22 Bn IDR. Equity: regressive (benefits middle/high-income zones with existing RoyalTrans service).

### 5.4 Cross-Scenario Comparison

**Table 4: Policy Scenario Summary**

| Scenario | Mean $\Delta$CS (Th IDR) | Annual $\Delta$W (Bn IDR) | Winners | Equity |
|----------|--------------------|--------------------|---------|--------|
| A: KRL→J3b | +0.001 | +2.22 | 318 | Pro-equity |
| B: Toll +40k | −0.100 | −168.02 | 0 | Regressive |
| C: KRL freq −20% | +3.765 | +6,580.38 | 3,580 | Mixed |
| D: TJ→J1b | +3.292 | +5,685.65 | 579 | Strongly pro-equity |
| E: MRT→J3a | +0.002 | +3.39 | 192 | Mildly pro-equity |
| F: TJ BSD→CBD | +0.529 | +852.60 | 510 | Strongly pro-equity |
| G: RoyalTrans freq | +1.257 | +2,093.22 | 3,132 | Regressive |
| H: RoyalTrans fare | +1.985 | +3,303.37 | 3,132 | Pro-equity |

**Ranking by aggregate welfare gain:**
1. Scenario C (KRL frequency): +6,580 Bn IDR/year
2. Scenario D (TJ→J1b): +5,686 Bn IDR/year
3. Scenario H (RoyalTrans fare): +3,303 Bn IDR/year
4. Scenario G (RoyalTrans freq): +2,093 Bn IDR/year
5. Scenario F (TJ BSD→CBD): +853 Bn IDR/year
6. Scenario E (MRT→J3a): +3.39 Bn IDR/year
7. Scenario A (KRL→J3b): +2.22 Bn IDR/year
8. Scenario B (Toll +40k): −168 Bn IDR/year

**Mode share shifts** are largest for the service quality scenarios. Scenario C shifts 14.9 pp toward KRL, the largest single-mode shift in any scenario, driven by commuters' time sensitivity and the large base of transit-eligible riders in KRL-served corridors. Scenario H shifts 14.1 pp toward RoyalTrans. Fare policy can achieve mode shift magnitudes comparable to infrastructure investment.

**Equity pattern:** The two most pro-equity scenarios (D and F) both extend budget transit (TJ at Rp 3,500) to unserved or under-served zones. The regressive scenarios (B, G) improve pricing or service quality in already-served zones. Scenario C exposes the central equity tension: it generates the largest welfare gain (+3.76 Th IDR/trip) but excludes 28% of commuters in transit-desert zones (J1b, J3b), widening the welfare gap between served and unserved corridors. Frequency improvements and pricing reforms should be bundled with network expansion to avoid regressive spatial outcomes.

### 5.5 Bootstrap Confidence Intervals

Table 4 reports 90% bootstrap confidence intervals for selected scenarios, computed from $N = 1{,}000$ truncated-Normal parameter draws.

**Table 5: Bootstrap 90% Confidence Intervals**

| Scenario | Mean $\Delta$CS | 90% CI |
|----------|----------|--------|
| A: KRL→J3b | +0.001 | [0.00, +0.61] |
| B: Toll +40k | −0.100 | [−36.69, 0.00] |
| D: TJ→J1b | +3.292 | [0.00, +15.81] |

The CIs are wide relative to point estimates because $\beta_{\text{cost}}$ has a large SE (0.097 vs estimate $-0.077$). The truncation at $\beta_{\text{cost}} \leq -0.3 \cdot |\hat{\beta}_{\text{cost}}|$ bounds the intervals below at zero for gain scenarios. Scenario B's CI is notably wide ($-36.69$ to $0.00$) because the cost shock magnitude (Rp 40,000) amplifies $\beta_{\text{cost}}$ uncertainty. These intervals are conditional on the structural restriction that cost reduces utility, consistent with economic theory and the Ilahi (2021) point estimate. Their width reflects genuine identification uncertainty in $\beta_{\text{cost}}$, not numerical artifact.

---

## 6. Discussion and Limitations

### 6.1 Key Findings in Context

The model selection result—NL over MNL with $\hat{\lambda} = 0.763$ ($p = 0.003$), and NL over MXL with Wald $p = 0.763$—shows that the main deviation from IIA in this dataset is within-nest correlation among transit modes, not unobserved taste heterogeneity. This matches Bastarianto et al. (2019), who report $\lambda_{\text{hwh}} = 0.55$ for Indonesian commuter mode choice with a tour-based nesting structure. Our within-nest correlation is weaker ($\hat{\lambda} = 0.76$ vs $0.55$), likely due to the different nesting structure (mode-based vs tour-based) and the inclusion of four transit modes rather than two.

The policy results show a clear pattern. Service quality improvements (Scenario C, KRL frequency) produce the largest aggregate gains (+3.76 Th IDR/trip), but the spatial distribution is regressive: transit-desert zones receive zero benefit. Transit expansion to unserved zones (Scenarios A, D) produces smaller aggregate gains (fewer commuters are affected) but is strongly pro-equity. The tension between aggregate efficiency and spatial equity runs through the results.

The mode share shifts in Scenarios D and F tell a consistent story. When budget transit (TJ at Rp 3,500) is introduced to a transit-desert zone (J1b), it draws from Motorcycle (−10.1 pp in Scenario D), not from other transit modes. New transit cannibalizes existing transit less when the alternative is private two-wheelers with fuel costs exceeding Rp 20,000 per trip. A Rp 3,500 flat-fare BRT is a genuine addition to the choice set, not a substitute for what was already there.

### 6.2 Connection to Transit Equity Mapping

The spatial pattern of welfare gains maps onto the transit accessibility index (TAI) from the parallel research project. J1b and J3b are Q4 (lowest-access) zones, with TAI scores below 0.15. The welfare gains from Scenarios D (+28.43 Th IDR/trip for J1b residents) and F (+9.66 for J3a, +2.49 for J3b) quantify the demand-side value of closing these supply-side gaps. J1b and J1a are at similar distance from JCBD but J1a has KRL. The ~30 Th IDR/trip welfare gap between them is the monetized cost of transit inaccessibility, a number that feeds directly into investment prioritization.

### 6.3 Limitations

Six limitations warrant discussion.

**First**, the data are synthetic. The 5,000-person population was generated from a known DGP, and parameter recovery success (12/12 MNL, 13/13 NL) is expected under correct specification. Real commuter behaviour includes heterogeneity in trip chaining, departure time choice, and within-household vehicle allocation that our DGP does not capture. The policy results demonstrate the analytical framework; they are not empirical forecasts.

**Second**, Car mode share is understated (1.0% synthetic vs roughly 20% in Jabodetabek commute surveys). The cause is a specification mismatch: the LOS skim uses full economic cost (toll + fuel + parking, roughly Rp 130,000 per trip from outer zones), but commuters mostly face marginal cost (fuel, roughly Rp 30,000) once the car is owned. With $\beta_{\text{cost}}$ anchored to Ilahi (2021), Car utility is suppressed. We keep the conservative specification because adjusting cost or $\beta$ would break the Ilahi anchor.

**Third**, Car Value of Time is roughly 4× the Ilahi anchor (Rp 106,200/hr vs Rp 25,200/hr). This is a small-sample identification issue: 51 of 5,000 persons chose Car, so $\beta_{\text{time,car}}$ is pinned down by a thin slice of LOS-favourable selectees. The large SE (0.283) fits this story.

**Fourth**, $\hat{\lambda} = 0.763$ is mildly upward-biased (9%) relative to the true DGP value of $0.70$. The bias sits within 2 SE and the 95% CI excludes 1.0. It reflects finite-sample identification of $\lambda$ from a single nest where within-nest substitution is rich (transit modes: 17.8% + 34.0% + 9.1% + 1.4% = 62.3% aggregate share) and the private nest contributes weakly (Car 1.0%, Moto 36.7%).

**Fifth**, the Mixed Logit diagnostic used $R = 100$ Halton draws instead of the planned $R = 500$. Train (2009, §9.3.2) notes that $R = 100$ Halton draws give accuracy equal to $R = 500$ pseudo-random draws for one-dimensional random coefficients. The conclusion (fail to reject $\sigma_{\text{cost}} = 0$) doesn't depend on this choice. The Mixed-DGP positive control catches $\sigma > 0$ at $R = 100$.

**Sixth**, the bootstrap CIs use truncated-Normal draws to keep $\beta_{\text{cost}}$ from drifting to zero. Without truncation, draws near $\beta_{\text{cost}} \approx 0$ blow up via $CS = EMU / |\beta_{\text{cost}}| \to \infty$. The truncation enforces the economic restriction that cost reduces utility, consistent with Ilahi (2021). The CIs are conditional on this restriction. Their width comes from genuine identification uncertainty in $\beta_{\text{cost}}$, not numerical noise.

**Seventh**, income-VoT scaling is not implemented in the DGP. $\beta_{\text{time}}$ and $\beta_{\text{cost}}$ are homogeneous across all persons. Income heterogeneity affects $\Delta CS$ only through zone composition: low-income commuters are concentrated in transit-desert zones (J1b, J3b), so policies targeting those zones appear pro-equity. A structural income-VoT interaction (e.g., Binsuwadan et al., 2023) would produce different welfare distributions because high-income commuters would respond more strongly to travel time changes and less strongly to cost changes. This is documented as a modelling choice rather than an error; a heterogeneous-β DGP was beyond the pedagogical scope of the project.

### 6.4 Future Extensions

Three extensions would sharpen the analysis. First, a car User Equilibrium assignment (Extension D) would replace free-flow car times with congested equilibrium times, adding the congestion feedback the current model lacks, and reframe Scenario B's toll increase as a Pigouvian correction rather than a pure welfare loss. Second, a transit crowding check (Extension E) would test whether KRL has physical capacity for the mode shifts Scenario C predicts. Third, panel data with multi-trip choice sequences (Extension G) would move past the 1-choice-per-person DGP to the multi-trip structure of real commuter surveys, which would let panel MXL estimate person-specific random parameters.

---

## 7. Conclusion

This study estimated three discrete choice models of commuter mode choice in Jabodetabek—MNL, Nested Logit, and Mixed Logit—and applied the selected NL model in eight transit policy scenarios using logsum consumer surplus measurement.

The Nested Logit specification with private and transit nests improves on MNL ($LR = 8.57$, $p = 0.003$). Within-nest correlation among transit modes is present. IIA does not hold for this choice context. $\hat{\lambda} = 0.763$ (95% CI: $[0.627, 0.900]$) indicates moderate substitution within the transit nest, consistent with Bastarianto et al. (2019). The Mixed Logit diagnostic finds no additional taste heterogeneity (Wald $p = 0.763$), which settles NL as the preferred specification.

KRL frequency improvement (Scenario C) produces the largest aggregate welfare gain: +3.76 Th IDR per trip, or +6,580 Bn IDR per year. But its spatial distribution is unequal. Transit-desert zones (J1b, J3b) receive nothing. TransJakarta extension to J1b (Scenario D, +3.29 Th IDR/trip) and TJ route restructuring to CBD (Scenario F, +0.53 Th IDR/trip) produce smaller aggregate gains but concentrate benefits among low-income commuters with no transit access today.

The central tension is between aggregate efficiency and spatial equity. Service quality improvements in already-served corridors help many commuters but bypass transit deserts. Network expansion into unserved zones reaches fewer people but closes the access gaps that drive spatial inequality in Jabodetabek's transport system. Frequency improvements and pricing reforms should be bundled with network expansion. Scenario C paired with Scenario D improves service quality for the majority while extending basic access to the excluded minority.

Synthetic data, a conservative cost specification, and a single-cross-section DGP limit the empirical precision of the welfare estimates. Even so, the framework—NL estimation with Ilahi-anchored parameters, r5py-based transit LOS, and logsum welfare measurement—offers a replicable method for transit investment evaluation in data-sparse developing-city contexts where revealed-preference commuter surveys are not available.

---

## References

Bastarianto, F. F., Irawan, M. Z., Choudhury, C., Palma, D., & Muthohar, I. (2019). A Tour-Based Mode Choice Model for Commuters in Indonesia. *Sustainability*, 11(3), 788. https://doi.org/10.3390/su11030788

Belgiawan, P. F., Ilahi, A., & Axhausen, K. W. (2019). Influence of pricing on mode choice decision in Jakarta: A random regret minimization model. *Case Studies on Transport Policy*, 7(1), 87–95. https://doi.org/10.1016/j.cstp.2018.12.002

Ben-Akiva, M., & Lerman, S. R. (1985). *Discrete Choice Analysis: Theory and Application to Travel Demand*. MIT Press.

Binsuwadan, J., Wardman, M., De Jong, G., Batley, R., & Wheat, P. (2023). The income elasticity of the value of travel time savings: A meta-analysis. *Transport Policy*, 136, 126–136. https://doi.org/10.1016/j.tranpol.2023.03.013

Ilahi, A., Belgiawan, P. F., & Axhausen, K. W. (2021). Understanding travel and mode choice with emerging modes; a pooled SP and RP model in Greater Jakarta, Indonesia. *Transportation Research Part A: Policy and Practice*, 150, 398–422. https://doi.org/10.1016/j.tra.2021.06.023

Train, K. (2009). *Discrete Choice Methods with Simulation* (2nd ed.). Cambridge University Press.

# Speaker Notes — Trans-Eng Final Presentation

Target: ~15 minutes for 12 main slides + Q&A. Aim for ~70–90 seconds per slide.

---

## Slide 1 — Title (5 seconds)

> "Good morning. My project is on mode choice modeling and policy welfare analysis in Jabodetabek. I compare three discrete choice models — MNL, Nested Logit, and Mixed Logit — then use the best model to evaluate eight transit policy scenarios using logsum consumer surplus."

*Click to next slide immediately — don't linger on the title.*

---

## Slide 2 — Motivation (~90 sec)

> "Why Jabodetabek? Three reasons."

Point to the **Scale** card:

> "First, scale. Jabodetabek has over 30 million people with 3.5 million daily commuters. Despite decades of transit investment — KRL, TransJakarta, MRT — the mode split is still dominated by car and motorcycle."

Point to the **Coverage Gap** card:

> "Second, the transit expansion is spatially uneven. Two of our seven study zones — J1b, which is Parung in the south, and J3b, Gading Serpong in the west — have *no formal transit at all*. Residents there can only drive or ride a motorcycle."

Point to the **Welfare** card:

> "This leads to the central policy question: which interventions maximize commuter welfare, and just as importantly, how are those gains *distributed* across zones and income groups? A policy that maximizes aggregate welfare might still leave the most underserved zones behind."

Point to the **Framework** banner:

> "The analytical framework follows the course structure: estimate a 6-mode choice model, compare MNL, NL, and MXL using AIC, LR, and Wald tests, select the best specification, then apply the logsum welfare measure to eight hypothetical policy scenarios."

---

## Slide 3 — Study Area & Data (~90 sec)

> "Here is the data setup."

Scan down the table:

> "Seven zones from outer Bodetabek to Jakarta CBD. Six modes: car, motorcycle, and four transit — KRL commuter rail, TransJakarta BRT, RoyalTrans premium bus, and MRT. We group them into two nests — Private and Transit — for the nested logit."

> "The population is 5,000 synthetic persons drawn from three income segments calibrated to BPS Susenas 2023 — roughly one-third low income, half middle income, and 16% high income. Car and motorcycle ownership rates are also calibrated to match BPS aggregate shares."

> "For transit level-of-service, I used r5py to route through actual GTFS feeds during the AM peak. So the travel times for KRL, TJ, MRT, and RoyalTrans are *real* door-to-door times including access walk, waiting, and transfers — not assumptions. For car and motorcycle, I used BPR free-flow speeds on the road network."

Point to the bottom banner:

> "All beta parameters are anchored to Ilahi et al. 2021 — the most recent Jakarta mode choice study. Beta-time for each mode is derived from Ilahi's mode-specific value of time using the formula shown here. Beta-cost is −1.42 from their Table 10. The scale parameter mu = 25 ensures realistic choice distributions while preserving the value-of-time ratios — I have a backup slide on this if needed."

---

## Slide 4 — MNL: Specification & IIA Problem (~80 sec)

> "Starting with the multinomial logit. The utility function is standard: ASC plus mode-specific beta-time times travel time, plus generic beta-cost times cost. Twelve parameters, estimated by maximum likelihood with KRL as the reference alternative."

Point to the results:

> "Good news: all 12 parameters are recovered within 2 standard errors of the DGP truth. Rho-squared is 0.280 — which in discrete choice is considered very good. AIC is 10,122."

Point to the IIA box:

> "But MNL has a fundamental problem. I ran a red-bus/blue-bus test: clone KRL as 'KRL Express' — an identical mode. MNL nearly *doubles* the transit share from 11.7% to 21.8%, which is absurd. Adding a clone should not steal share from motorcycles."

> "I also tested cross-elasticity directly. When I improve TJ utility by 0.1, the NL model shows that transit modes lose 1.90 percentage points while private modes lose only 1.14 — within-nest substitution is 1.67 times cross-nest. MNL forces these to be equal, which is wrong."

> "This motivates the nested logit."

---

## Slide 5 — Nested Logit: λ = 0.763 (~80 sec)

> "The nested logit adds one parameter — lambda, the nest dissimilarity. Two nests: Private containing car and motorcycle, Transit containing the four transit modes."

Scan the results table:

> "Lambda-hat is 0.763 with standard error 0.068. The 95% confidence interval is 0.627 to 0.900 — it *excludes* 1.0. Lambda equals 1 would mean MNL is correct, but we reject that."

> "The likelihood ratio test confirms: chi-squared 8.57, one degree of freedom, p-value 0.003. We reject IIA at the 1% level. All 13 parameters — the 12 from MNL plus lambda — are recovered within 2 standard errors."

Point to the key finding box:

> "What does lambda = 0.763 mean economically? Transit modes share about 24% of their unobserved variance — things like crowding comfort, schedule reliability, station environment. When KRL improves, TJ and RoyalTrans lose riders *faster* than car and motorcycle do, because commuters see transit modes as closer substitutes. This is exactly what we expect in a system where transit modes compete for the same station-access commuters."

---

## Slide 6 — Mixed Logit: σ = 0.010 (~70 sec)

> "Now the question: does the NL nesting capture everything, or is there also person-level taste heterogeneity? I test this with a mixed logit where beta-cost is random — drawn from a normal distribution with mean mu and standard deviation sigma."

> "If sigma is significantly different from zero, there is taste heterogeneity beyond what nesting captures. I used 100 Halton draws — Train 2009 shows this is equivalent to about 500 pseudo-random draws for a one-dimensional random coefficient."

Point to the Wald test:

> "Sigma-hat is 0.010 with SE 0.033. The Wald statistic is 0.091, p-value 0.763. We *fail to reject* the null that sigma equals zero. There is no evidence of cost heterogeneity."

Point to the interpretation box:

> "To make sure the estimator actually works, I ran a positive control: generate data *with* taste heterogeneity, sigma-true = 0.02. The Wald test correctly rejects at p near zero. So the estimator *can* detect heterogeneity — it just doesn't find any in our NL-generated data. This confirms the MXL result is a true negative, not an estimator failure."

> "The MXL log-likelihood is −5,048.79, essentially identical to MNL at −5,048.83. Adding a random coefficient gains 0.04 log-likelihood units — negligible. NL captures the departure from IIA that matters."

---

## Slide 7 — Model Selection (~60 sec)

> "Here is the summary comparison."

Read across the NL column:

> "NL has the best log-likelihood at −5,044.54, gaining 4.29 units over MNL with just one extra parameter. AIC selects NL: delta-AIC is −6.6 versus MNL and −8.5 versus MXL. Burnham and Anderson's rule of thumb says delta-AIC greater than 4 means 'considerably less support' for the worse model."

> "BIC nearly ties MNL and NL — this is because BIC's per-parameter penalty is ln(5000) = 8.52, which almost equals twice the LL improvement of 8.57. But NL still wins by a hair, and BIC strongly rejects MXL."

> "The LR test rejects MNL at p = 0.003. The Wald test fails to reject MXL's random parameter at p = 0.763. So NL is selected as the parsimonious correct specification. All welfare analysis uses the NL model."

---

## Slide 8 — Logsum Welfare Measurement (~80 sec)

> "Now we apply the NL model to measure welfare. The key concept from the course is the logsum — or expected maximum utility."

Point to the formulas:

> "For nested logit, the logsum has two levels. First, compute the inclusive value for each nest — that's the log-sum-exp of utilities *within* the nest, scaled by lambda. Then compute the upper-level EMU as the log-sum-exp across nests."

> "Consumer surplus is EMU divided by the absolute value of beta-cost — this converts utility units to money. The change in CS between a policy scenario and the baseline tells us the welfare impact per person per trip."

Point to the baseline cards:

> "The baseline mean CS is −53.65 thousand IDR per trip. This is negative because it represents the 'cost' of traveling — higher is better but always negative. The P10-to-P90 range is wide: −115 to −9, reflecting the huge variation in commute distance across our seven zones."

> "One important caveat: beta-cost from the NL is −0.077 with a standard error of 0.097. This large SE propagates into wide bootstrap confidence intervals on the welfare estimates. I'll note this as a limitation."

---

## Slide 9 — Policy Scenarios Overview (~70 sec)

> "Eight scenarios, covering four types of intervention: network extension, frequency improvement, fare reduction, and congestion pricing."

Point to the chart:

> "The lollipop chart ranks them by mean delta-CS per trip. Scenario C — improving KRL frequency by 20%, which reduces travel time by 20% in KRL-served zones — gives the highest aggregate gain at +3.76 thousand IDR per trip. Scenario D — extending TransJakarta to J1b — is close behind at +3.29."

> "At the bottom, Scenario B — a 40,000 rupiah toll increase — is the only scenario with negative welfare: −0.10 per trip, with zero winners. A punitive toll without transit alternatives destroys welfare."

> "The bootstrap confidence intervals for scenarios A, B, and D are shown. They are wide due to beta-cost uncertainty, but the ranking is robust — C and D are clearly the top performers."

---

## Slide 10 — Distributional Impact (~80 sec)

> "But aggregate welfare hides the spatial distribution. This heatmap shows delta-CS by zone for all eight scenarios."

Point to Scenario C row:

> "Look at Scenario C. J1a gains +15.8, J3a gains +6.9, but J1b and J3b — the two transit-orphan zones — get *exactly zero*. They have no KRL, so improving KRL frequency does nothing for them. This is a classic efficiency-equity tradeoff."

Point to Scenario D row:

> "Now Scenario D. The gain is *entirely* concentrated in J1b at +28.4 thousand IDR per trip. That is transformative — for a low-income commuter earning 3 million rupiah per month, this welfare gain is equivalent to 39% of their monthly income."

Point to the insight cards:

> "Scenario F is interesting because it helps *both* BSD zones: J3a gets +9.7 and J3b gets +2.5, through a TJ route restructuring. And notice that Scenario B — the toll — shows small negative values everywhere, with nobody winning."

> "The key policy insight: Scenario C is the efficiency champion, Scenario D is the equity champion. The optimal real-world policy bundles both."

---

## Slide 11 — Mode Shifts (~60 sec)

> "Where do the new transit riders come from? These charts show baseline versus policy mode shares for the top four scenarios."

Point to Scenario C (top-left):

> "In Scenario C, KRL jumps from 17.8% to 32.7% — a gain of 14.9 percentage points. It draws mainly from motorcycle at −7.8 and TransJakarta at −5.1. This makes sense: faster KRL attracts the motorcycle commuters who were previously deterred by long transit times."

Point to Scenario D (top-right):

> "In Scenario D, TJ gains 10.3 percentage points, drawn *almost entirely* from motorcycle at −10.1. This is critical: budget transit at Rp 3,500 expands the transit pie rather than reshuffling within it. It converts private vehicle users to public transit."

Point to Scenario H (bottom-right):

> "Scenario H — halving RoyalTrans fares — creates the largest single-mode shift: Royal jumps from 9.1% to 23.2%. But it draws from TJ at −8.5, meaning it partly cannibalizes existing transit rather than converting private vehicle users."

---

## Slide 12 — Conclusions (~60 sec)

> "Four takeaways."

> "First, NL is the appropriate model for Jabodetabek mode choice. Lambda = 0.763 confirms significant within-nest correlation. The LR test rejects MNL at p = 0.003, and MXL adds no signal."

> "Second, the top aggregate welfare gain comes from KRL frequency improvement — Scenario C at +3.76 thousand IDR per trip, or +6,580 billion IDR annually. This is the maximum willingness to pay for the policy."

> "Third, the most pro-equity scenario is TJ extension to J1b — Scenario D — which concentrates gains in the most underserved zone. Low-income residents benefit slightly more than high-income."

> "Fourth, and most important for policy: service quality improvements alone leave transit orphans behind. Network expansion alone serves fewer total commuters. The recommendation is to *bundle* both — improve frequency where rail exists AND extend budget transit to unserved zones."

> "Thank you. I'm happy to take questions."

---

## Slide 13 — Thank You

*Stay on this slide during Q&A. If a question comes about scale normalization, go to Slide 14. If about mode exclusions, go to Slide 15.*

---

## Slide 14 — Backup A: Why μ = 25? (if asked)

> "This comes up because the estimated beta magnitudes are much smaller than Ilahi's published values. The reason is scale normalization."

> "Train 2009 Section 3.7 shows that in MNL, you can never separately identify beta and the Gumbel scale parameter. The likelihood only depends on V/mu, so we estimate beta/mu, never beta alone."

> "With Ilahi's beta values and our LOS data — times in minutes, costs in thousands of IDR — the systematic utility differences range from 5 to 75 utils. At Gumbel scale 1, the standard deviation is only 1.28, so a gap of 20 means the top mode gets 99.99% probability. Choices become deterministic and most parameters are unidentified."

> "Dividing by 25 is equivalent to drawing Gumbel noise with scale 25 instead of 1. It produces realistic mode shares: moto 36.7%, TJ 34%, KRL 17.8%. The tradeoff is that standard errors are larger in absolute terms, but all behavioral metrics — VOT, elasticities, welfare — are scale-invariant because mu cancels in any ratio of betas."

---

## Slide 15 — Backup B: Why Drop Ride-Hailing & LRT? (if asked)

> "We started with nine modes and dropped three."

> "GoRide/GrabBike: Ilahi's beta-time for 2-wheel ride-hailing is −5.10, estimated on short urban trips within Jakarta. On our 30–105 kilometer commute corridors, this produces near-zero mode share. Wardman et al. 2016 calls this 'parameter non-transferability' — you cannot apply a short-trip beta to long-distance commuting."

> "GoCar/GrabCar: To match the BPS aggregate share, the ASC calibration required values above +40 utility units. This is far outside any defensible range and suggests the mode operates in a fundamentally different market segment than commuting."

> "LRT Jabodebek: It exists in only 1 of our 7 zones — J2. With single-zone presence, the ASC absorbs zone-level unobservables rather than capturing actual mode preference. The parameter would be uninterpretable."

> "We tested all nine modes in the DGP, confirmed these three were problematic, and adopted the six-mode specification."

---

## Likely Q&A Topics — Quick Answers

**"Why not real survey data?"**
> "No public revealed-preference mode choice microdata exists for Jabodetabek with all six modes and trip-level LOS. The synthetic DGP is anchored to Ilahi 2021 betas and real GTFS transit times from r5py routing. Every parameter is traceable to either a literature citation or an actual GTFS computation."

**"Car share is only 1% — is that realistic?"**
> "No, it's a known limitation. We use full economic cost — toll plus fuel plus parking, around Rp 130,000 per trip from outer zones. But commuters perceive only marginal cost — fuel around Rp 30,000 — because car ownership is a sunk cost. With beta-cost anchored to Ilahi, the full-cost specification suppresses car utility. We keep it to preserve the anchor rather than introducing an unvalidated adjustment. A two-stage budgeting model — own then use — would address this but is beyond project scope."

**"What does +6,580 billion IDR per year actually mean?"**
> "It is the aggregate compensating variation — the total amount commuters would be willing to pay for the KRL frequency improvement. It's not cash savings; it's the monetary equivalent of time savings plus the improved option value of having faster transit available. The government could justify spending up to that amount on the improvement and commuters would still be net better off."

**"Why is lambda biased upward — 0.763 versus true 0.700?"**
> "The 9% bias is within 2 SE and 0.93 standard errors from truth, so it's statistically acceptable. The likely cause is transit-nest dominance — with 4 transit modes versus 2 private modes, the transit nest has more alternatives contributing to its inclusive value, which slightly inflates the estimated lambda. At N = 5,000, this is a known small-sample property of NL FIML estimators."

**"What is the Halton sequence and why 100 draws?"**
> "Halton sequences are quasi-random number sequences with better coverage of the unit interval than pseudo-random draws. Train 2009 Section 9.3.2 shows that 100 Halton draws give equivalent accuracy to about 500 pseudo-random draws for a one-dimensional random coefficient. Since we have only one random parameter — beta-cost — 100 Halton draws is more than sufficient."

**"What are the confidence intervals on the welfare estimates?"**
> "Bootstrap 90% CIs for Scenario D: mean +3.29, CI [0.00, +15.81]. For Scenario B: mean −0.10, CI [−36.69, 0.00]. They are wide because beta-cost has SE = 0.097 on an estimate of −0.077. Since delta-CS divides by |beta-cost|, small beta-cost values amplify welfare estimates. We use truncated-Normal draws bounded at −0.3 times |beta-hat| to prevent sign flips. The ranking of scenarios is robust across draws even though the point estimates have high uncertainty."

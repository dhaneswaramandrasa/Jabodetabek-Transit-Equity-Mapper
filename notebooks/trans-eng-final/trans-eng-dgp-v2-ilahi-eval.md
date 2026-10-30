# DGP v2 — Ilahi (2021) Implementation Evaluation

**Status**: REVIEW — evaluates `trans-eng-final-project.md` (merged into main spec) against Ilahi et al. (2021)
**Date**: 2026-04-30
**Source paper**: `docs/literature/2021_ilahi_understanding_travel.pdf` (TRA Part A 150, 398–422)
**Verdict**: **Approach is fundamentally correct** with three real methodological caveats (M1–M3) and four documentation/Q&A gaps (D1–D4). One ASC sign-flip (M4) needs re-examination before applying to §7.

---

## TL;DR

| Decision | Verdict |
|---|---|
| Use Ilahi Table 11 VTTS to derive mode-specific β_time | ✅ Correct in principle |
| Use β_cost = −1.42/Thousand IDR as generic | ⚠️ **Conditionally correct** — only at sample mean (income, distance interactions ignored) |
| Algebra: β_time = β_cost × VTTS / 60,000 | ✅ Recovers Ilahi's published β_time exactly |
| Map 4WRH → Ilahi "Taxi", 2WRH → Ilahi "ODT" | ⚠️ **Misaligned with Ilahi's pooling** — Model 1 pools car+MC, so VTTS is not vehicle-specific |
| Interpolate VTTS for MRT, LRT, RoyalTrans | ✅ Acceptable as DGP choice; no empirical anchor (acknowledged) |
| Re-normalize ASCs from MC-base to KRL-base | ✅ Re-normalization arithmetic is correct |
| Specific ASC magnitudes (Car +0.90, MC +1.20, etc.) | ⚠️ **Sign flips vs. Ilahi** — Car/2WRH/4WRH/TJ all flipped from negative to positive; needs explicit defense |

---

## What the Ilahi paper actually reports

### Table 10 (p. 410) — pooled SP+RP MNL, MC = base, n = 52,731

**Generic cost coefficient:**
`β_cost = −1.42 per Thousand IDR (t = −12.08, p < 0.01)`

**But cost is interacted:**
- `λ Income, cost = −0.09` (t = −3.06, p < 0.01)
- `λ Distance, cost = −0.83` (t = −19.16, p < 0.01)

The published β_cost = −1.42 is the base level *at the sample mean* of income and distance.
The marginal disutility of cost in Ilahi's model is actually:
```
β_cost_effective = −1.42 + interactions(ln Income, ln Distance)
```

**Mode-specific β_time (Model 1):**
| Mode | β_time/min | t-value | Significant? |
|---|---|---|---|
| Walk | −0.36 | −6.82 | ✅ |
| Bike | −8.61 | −4.55 | ✅ |
| PT (SP) | −0.28 | −1.22 | ❌ NS |
| Bus | −1.18 | −1.40 | ❌ NS |
| BRT | −1.07 | −2.36 | ✅ p<0.05 |
| Train | −2.72 | −6.39 | ✅ |
| Car | −0.60 | −3.64 | ✅ |
| MC | −2.34 | −10.25 | ✅ |
| Taxi | −3.49 | −8.03 | ✅ |
| ODT | −5.10 | −15.27 | ✅ |
| UAM | −1.36 | −31.83 | ✅ |

**Demographic interactions enter on ASC, NOT on β_time** — confirmed by inspecting Table 10. Variables like β_Age_MC, β_University_degree_ODT shift the ASC; there is no β_Time_x_Demographic term. ✅ The draft's claim "β_time in Ilahi does NOT interact with demographics" is correct.

### Table 11 (p. 413) — VTTS at sample mean (USD/hour)

VTTS formula (Eq. 3, p. 412):
```
VTTS [USD/hr] = (60 / 14) × (β_T / β_C)
```
where 60 = min/hr, 14 = Thousand IDR per USD (paper rounds the 14,400 IDR/USD spot rate).

Recovery check: Car VTTS = (60 × 0.60)/(14 × 1.42) = 36/19.88 = **1.81 USD/hr** ✓ (Table 11 reports 1.80).

| Mode | VTTS USD/hr | Implied Rp/hr (×14,000) |
|---|---|---|
| PT | 0.86 | 12,040 |
| Bus | 3.56 | 49,840 |
| BRT | 3.23 | 45,220 |
| Train | 8.21 | 114,940 |
| Car | 1.80 | 25,200 |
| MC | 7.06 | 98,840 |
| Taxi | 10.52 | 147,280 |
| ODT | 15.38 | 215,320 |
| UAM | 4.98 | 69,720 |

The draft's Rp values (col 3 of §7 MNL DGP table) match these to within rounding. ✅

---

## Verification of the draft's algebra

The draft's formula:
```
β_time_mode = β_cost × VTTS_mode / (1000 × 60)
            = −1.42 × VTTS_mode_Rp/hr / 60,000
```

Algebraically equivalent to inverting Ilahi's Eq. 3:
```
VTTS_USD/hr = (60/14) × (β_T / β_C)
⇒ β_T = β_C × VTTS_USD/hr × 14 / 60
⇒ β_T = β_C × VTTS_Rp/hr / 60,000   [since 14×1000 = 14,000 IDR per USD]
```

✅ **Correct.** Substituting β_cost = −1.42 and Ilahi's published Table 11 VTTS recovers his Table 10 β_time values to 2 decimal places. This is the right derivation — using the *derived behavioral metric* (VTTS) plus a single anchored coefficient (β_cost) is a standard practice in transferring discrete-choice parameters across studies (cf. Wardman 2004; World Bank 2023 meta-analysis §3).

---

## Methodological caveats

### M1. β_cost is "generic" only at the sample mean

The draft asserts: *"β_cost is generic in Ilahi's model — same across all modes (Table 10, col 'Model 1')."*

This is correct **as written** — Ilahi does not estimate mode-specific β_cost. But the draft's framing is incomplete because the model also includes:
- `λ Income, cost = −0.09` (cost interacts with log income)
- `λ Distance, cost = −0.83` (cost interacts with log distance)

The reported β_cost = −1.42 is the value at `Income = AverageIncome, Distance = AverageDistance`. For respondents far from these means, the effective β_cost differs.

**Implication for DGP v2:** When the draft uses β_cost = −1.42 as a fixed scalar in the synthetic DGP, it implicitly assumes all simulated travelers are at Ilahi's sample-mean income and distance. The mode-specific VTTS values from Table 11 are reported at that same mean, so the algebra is internally consistent — but the draft must explicitly acknowledge:

> "We use β_cost = −1.42 and Table 11 VTTS as evaluated at Ilahi's sample mean. The DGP does not preserve the income×cost or distance×cost interactions Ilahi estimated."

**Q&A risk:** "Why didn't you use Ilahi's income-cost interaction?" — without an explicit answer, this looks like cherry-picking.

**Fix:** Add a paragraph to the draft explaining this trade-off. Two defensible answers:
1. *DGP scope:* "We focus on mode-specific time/cost trade-offs at the population mean. Modeling income heterogeneity in cost sensitivity is a Phase 2 extension."
2. *Coverage:* "Our 4 study zones span income deciles already; running a single DGP at sample mean is a conservative choice when the four-zone average aligns with Ilahi's all-Jakarta mean."

### M2. Mode mapping for ridehailing is misaligned with Ilahi's pooling

The draft maps:
- **4WRH (Gojek/Grab car) → Ilahi "Taxi" (10.52 USD/hr)**
- **2WRH (GoRide/GrabBike) → Ilahi "ODT" (15.38 USD/hr)**

But §6 of Ilahi's paper (p. 409) states:
> "MC-based and car-based taxis were converted to taxi, and MC-based and car-based ODT were converted to ODT."

So in Model 1:
- **"Taxi" = pooled (Car Taxi + MC Taxi)** — not a 4-wheel-only category
- **"ODT" = pooled (Car ODT + MC ODT)** — includes BOTH 4WRH and 2WRH ridehailing

The "right" mapping under Ilahi's definitions:
- 4WRH (Gojek car / GrabCar) is a **car-based ODT** → falls within Ilahi's "ODT" pooled category
- 2WRH (GoRide / GrabBike) is an **MC-based ODT** → also within Ilahi's "ODT" pooled category

Both 4WRH and 2WRH should arguably draw from VTTS_ODT = 15.38 USD/hr if we follow Ilahi's mode definitions strictly.

**The draft's choice appears to be:**
- 4WRH → "Taxi" because conventional taxi (Bluebird) is a major 4-wheel paid alternative in Jakarta and structurally resembles GrabCar (sit, paid, no driver-app vs. street hail distinction)
- 2WRH → "ODT" because Ilahi's "MC ODT" is the closest behavioral analog and likely dominates his ODT pool (RP share of MC ODT > Car ODT in Fig. 6)

**Verdict:** The mapping is *defensible* but does not strictly follow Ilahi's pooled categories. If asked in Q&A, the answer should be:
> "Ilahi pools car+MC into single Taxi and ODT categories. We split them by the dominant behavioral analog: Bluebird-like taxi for 4WRH (10.52), MC-based ODT for 2WRH (15.38). This preserves the Car-vs-MC VTTS spread Ilahi estimated separately in his Model 1 individual β_time (Car −0.60 vs. MC −2.34)."

**Alternative defense (cleaner):** Use β_time directly, not VTTS:
- For 4WRH, use Ilahi's "β_Travel time Taxi = −3.49" → VTTS = 10.52 USD/hr
- For 2WRH, use Ilahi's "β_Travel time ODT = −5.10" → VTTS = 15.38 USD/hr

This is what the draft *implicitly* does (recovering −3.49 and −5.10) but the framing should foreground "we are transferring β_time directly, VTTS is just the human-readable form."

### M3. Travel-time on PT and Bus is not significant in Model 1

`β_PT = −0.28 (t = −1.22, NS)` and `β_Bus = −1.18 (t = −1.40, NS)`.

The draft uses Ilahi's BRT (β = −1.07, p<0.05) and Train (β = −2.72, p<0.01), both significant. ✅ Good choice — those are the two PT modes the draft anchors on (TJ ← BRT, KRL ← Train).

**Caveat for RoyalTrans interpolation:** RoyalTrans is anchored to BRT × 1.22 = β_time = −1.30/min. BRT itself is only marginally significant (t = −2.36). This compounds parameter uncertainty. Acknowledge in the Q&A.

### M4. ASC re-normalization is arithmetically correct, but specific ASC magnitudes flip Ilahi's signs

**Re-normalization (MC=0 → KRL=0)** — verified arithmetically:

| Mode | Ilahi ASC (MC=0) | Re-normalized (KRL=0) | t-value |
|---|---|---|---|
| MC | 0.00 | +0.29 | (base) |
| Train (KRL) | −0.29 | 0.00 | −0.9 NS |
| Car | −1.20 | −0.91 | −10.64 *** |
| ODT | −1.43 | −1.14 | −9.32 *** |
| Taxi | −3.94 | −3.65 | −23.59 *** |
| BRT | −4.74 | −4.45 | −20.37 *** |
| Bus | −5.05 | −4.76 | −13.47 *** |

Ilahi's preference ordering after time/cost controlled (KRL=0):
**MC ≈ KRL > Car > ODT >> Taxi > BRT > Bus**

**The draft's chosen ASCs:**
| Mode | Draft ASC (KRL=0) | Implied ordering vs. Ilahi |
|---|---|---|
| MC | +1.20 | ↑ vs. Ilahi +0.29 |
| 2WRH | +1.10 | **flipped** from −1.14 to +1.10 |
| Car | +0.90 | **flipped** from −0.91 to +0.90 |
| 4WRH | +0.50 | **flipped** from −3.65 to +0.50 |
| MRT | +0.30 | new (no Ilahi anchor) |
| RoyalTrans | +0.05 | new (no Ilahi anchor) |
| KRL | 0.00 | reference |
| LRT | −0.10 | new (no Ilahi anchor) |
| TJ | −0.30 | softened from −4.45 |

**This is a major DGP choice that deviates from Ilahi's empirical ordering.** Ilahi found Car/Taxi/BRT all *less preferred* than rail (Train/KRL) once time and cost are controlled. The draft assumes Car/2WRH/4WRH all *more preferred* than KRL.

**Why this might be defensible (Bodetabek context):**
- Ilahi's sample is geographically intra-Jakarta — his Train alternative is short-distance KRL trips where rail is convenient
- Bodetabek corridors (Bogor → CBD, Bekasi → CBD) are 30–60 km, where car/MC ownership becomes more attractive due to first/last-mile, schedule rigidity, and crowding on KRL
- Modal share data from BPS Jabodetabek 2023 (cited in draft) shows MC ≥ 60% and KRL ~5% — implying private modes are revealed-preferred

**Why this is a Q&A risk:**
- Reviewers will ask: "Ilahi's data shows Car ASC = −0.91 below KRL. Your DGP has Car +0.90 above KRL. That's a 1.81-utility-unit swing. What empirical evidence supports this reversal?"
- The draft's current answer ("stronger car preference in longer Bodetabek corridors") is plausible but unsupported by a citation

**Fix options:**
1. **Cite Belgiawan et al. (2019) Bodetabek-specific RP** — they survey similar long-corridor commutes; check if their ASCs show Car preference.
2. **Cite Bastarianto et al. (2019)** — tour-based mode choice in Jabodetabek; estimates λ_hwh = 0.55 for OwnVehicle nest, suggests private mode is the dominant tour anchor.
3. **Anchor the modal share** — if BPS 2023 reports MC > Car > KRL on Bodetabek-CBD trips, derive ASCs by inverse-logit from observed shares + time/cost controls. This is a defensible procedure.
4. **Soften the claim**: say "DGP-specified, motivated by observed Bodetabek modal share" rather than "informed by Ilahi's preference ordering" — because the *signs* are not informed by Ilahi.

**Recommendation:** Update the §7 ASC table commentary to make the deviation from Ilahi *explicit and defended*, rather than presenting it as "informed by Ilahi's ordering" (which it is for Bus < BRT < Taxi but not for Car/MC vs. rail).

---

## Documentation gaps

### D1. β_cost units convention not stated in §7

When the draft says `β_cost = −1.42 per Thousand IDR`, the synthetic DGP code must scale all cost variables to Thousand IDR before applying β. If `cost_KRL = 14,000 Rp`, the model uses `cost = 14.0` (in Thousand IDR), so `β_cost × cost = −1.42 × 14.0 = −19.88` utils. **Add a note in §7 stating the cost scale convention** before the parameter recovery section.

### D2. VTAT vs. VTTS distinction not used

Ilahi reports both VTTS (Table 11 col 5) *and* VTAT (Value of Time Assigned to Travel = positive part). E.g., Car VTAT = +3.94 USD/hr meaning users actively *enjoy* car time relative to leisure foregone. MC VTAT = −1.32 (exposure penalty).

The draft mentions VTAT only for Car. **For Q&A defense**, add a brief explanation:
> "VTAT = VTTS − VOL (Value of Leisure). VTAT > 0 means the user finds time-on-mode less burdensome than generic leisure (comfort/safety dominates). Our derived β_time captures the full VTTS, which is what enters utility — VTAT is descriptive only."

This shows the student understands the comfort-vs-time trade-off, which is a likely Q&A topic.

### D3. The ".5 — .8 km / Rp 5–10k" cost segments assumption is undocumented

Ilahi's Table 8 shows SP attribute levels by distance bucket (0–1.5, 1.5–5, 5–15, 15–25, >25 km). The draft does not state whether the synthetic DGP draws costs from these buckets, computes them per-zone via r5py + tariff schedule, or uses a single representative value. **Add a sentence** to §7 stating the cost-generation procedure.

### D4. §6.3 income-segment VoT vs. §7 mode-specific VTTS — clarify which is used

The draft retains a population-segment VoT table in §6.3 (low 12k / mid 25k / high 55k Rp/hr), then states "These are population segments, not mode-specific. Mode-specific VTTS comes from Ilahi Table 11 directly."

**Risk:** A reader may assume the DGP applies *both* — segment-by-mode VoT. Clarify that:
- §6.3 table is for **welfare interpretation only** (used in logsum CS section if applicable)
- §7 MNL DGP uses **only mode-specific VTTS** from Ilahi Table 11
- Income heterogeneity is **not** modeled in the MNL DGP (this is the M1 caveat)

If §6.3 segment VoT is not used anywhere in the DGP or the welfare section, **delete it** — it confuses the parameter audit trail.

---

## Summary of fixes before applying to `notebooks/trans-eng-final/trans-eng-final-project.md`

| # | Fix | Where | Priority |
|---|---|---|---|
| 1 | Add explicit caveat: β_cost = −1.42 evaluated at sample mean; income/distance interactions dropped | §7 preamble, before β_cost row | **High** (Q&A defense) |
| 2 | Reframe 4WRH/2WRH mapping as "transferring Ilahi's mode-specific β_time directly, VTTS is the readable form" — acknowledge Model 1 pools car+MC | §7 footnote on 4WRH and 2WRH rows | **High** |
| 3 | Replace "informed by Ilahi's preference ordering" with explicit deviation acknowledgement for Car/2WRH/4WRH/TJ ASCs | §7 ASC table commentary | **High** |
| 4 | Cite empirical anchor for Bodetabek modal-share-based ASC choices (Belgiawan 2019, Bastarianto 2019, or BPS 2023) | §7 ASC derivation column | **Medium** |
| 5 | State cost-units convention (Thousand IDR) before parameter recovery section | §7 immediately before "Parameter recovery" | **Medium** |
| 6 | Add VTAT explanation paragraph for Q&A robustness | §13 Q&A new entry | **Medium** |
| 7 | State cost-generation procedure (r5py + tariff schedule? Table 8 buckets?) | §7 preamble | **Medium** |
| 8 | Clarify or delete §6.3 segment VoT — confirm it's not used in MNL DGP | §6.3 closing sentence | **Low** |
| 9 | Note compounded uncertainty for RoyalTrans (BRT base only marginally sig) | §7 RoyalTrans row | **Low** |

---

## Overall assessment

**Is this the right way to implement Ilahi (2021)?**

**Yes, with caveats.** The draft's core technical move — derive mode-specific β_time per mode by combining Ilahi's published VTTS (Table 11) with his generic β_cost (Table 10) — is methodologically sound. The algebra exactly recovers Ilahi's individual β_time estimates, which validates the parameter transfer.

The three substantive concerns are:
1. **Ignored cost interactions (M1)** — defensible if framed as "DGP at sample mean", risky if presented as "we use Ilahi's full model"
2. **Mode mapping for 4WRH/2WRH (M2)** — defensible after reframing as "direct β_time transfer with vehicle-type analog choice"
3. **ASC sign flips (M4)** — needs an explicit Bodetabek-modal-share defense, not an "informed by Ilahi" framing

The interpolated VTTS for MRT/LRT/RoyalTrans (M5) is a reasonable DGP choice given those modes weren't in Ilahi's 2019 survey; transparent acknowledgement is sufficient.

**Bottom line:** The mathematical core is correct and recovers Ilahi exactly. What needs work is the *presentation* — making the boundary between "transferred from Ilahi" and "DGP-specified for our context" crisp enough to survive a 50%-weighted Q&A grade.

---

## Files referenced

- `trans-eng-final-project.md` (merged into main spec) — draft under review
- `docs/literature/2021_ilahi_understanding_travel.pdf` — source paper, Tables 8 (p. 408), 9 (p. 409), 10 (p. 411), 11 (p. 413)
- `docs/literature/2019_bastrianto_tour_based_mode_choice.pdf` — referenced for NL nesting parameter ρ_OwnVehicle = 0.55
- `docs/literature/2019_belgiawan_influence_pricing_mode_choice.pdf` — Bodetabek-specific RP, candidate for ASC validation
- `docs/literature/2023_world_bank_meta-analysis.pdf` — VTTS transfer methodology reference

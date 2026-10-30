# Mixed Logit Addition — Trans-Eng Final Project

**Date**: 2026-05-01
**Status**: PROPOSAL — pending review before updating `notebooks/trans-eng-final/trans-eng-final-project.md`

---

## What This Adds

A **Mixed Logit (MXL) diagnostic** as notebook `03b_mixed_logit.ipynb`, inserted between
NL estimation (03) and policy simulation (04).

## Model Progression

```
01_data_prep  →  02_mnl  →  03_nl  →  03b_mixed_logit  →  04_policy
                                  ↑
                            NEW — heterogeneity diagnostic
```

| Notebook | Model | What it tests |
|---|---|---|
| 02 | MNL | Baseline — 18 params, mode-specific β_time |
| 03 | NL | Nest correlation — fixes IIA, 3 ownership-based nests |
| **03b** | **Mixed Logit** | **Unobserved heterogeneity — random ASCs (Ilahi Model 3)** |
| 04 | Policy | Logsum welfare from the best-supported model |

## Specification (Ilahi 2021 Model 3 pattern)

Ilahi's Model 3 uses random ASCs with MXL:

$$U_{i,n} = ASC_i + η_{i,n} + β_{time,i} · t_{i,n} + β_{cost} · c_{i,n} + ε_{i,n}$$

where $η_{i,n} \sim N(0, σ_i^2)$ is an individual-specific random intercept for
alternative $i$. This captures unobserved preference heterogeneity — some people
inherently like transit more than the average, others dislike it more, beyond what
time and cost explain.

**Implementation:**
- Random ASCs on 3 key alternatives (Car, Moto, TJ) — the modes with largest shares
- Fixed ASCs on remaining 6 modes (identification — too many random params with 9 modes)
- Estimation: Simulated MLE with 200 Halton draws (quasi-random, more efficient than pseudo-random)
- 5,000 persons × 9 modes × 200 draws × zone-specific availability

## What It Tests (L07 Five Habits Framework)

| Habit | This project |
|---|---|
| ① Estimate baseline | MNL (02) |
| ② Diagnose with multiple tools | LR test, SE dispersion, ρ² comparison across specs |
| ③ Test the right layer | NL tests within-nest correlation; MXL tests unobserved heterogeneity |
| ④ Report distribution | VOT distribution across population; ΔCS distribution per zone×segment |
| ⑤ Reject if unwarranted | **Key**: LR test may fail to reject NL — that's the correct answer if DGP has no heterogeneity |

## Diagnostic Value

The Mixed Logit serves as a **specification test**:

1. **LR test**: Mixed Logit (−2×(LL_NL − LL_MXL)) vs χ² with df = number of random params
   - Significant → unobserved heterogeneity exists beyond nest correlation → use MXL for policy
   - Not significant → NL is sufficient → report "no evidence of unobserved heterogeneity"

2. **SD of random ASCs**: t-test on σ_Car, σ_Moto, σ_TJ
   - |t| > 1.96 → significant taste variation for that alternative
   - |t| < 1.96 → preference is homogeneous for that alternative

3. **VOT distribution**: If random β_time is added (Layer 2), VOT becomes a distribution
   rather than a point estimate — richer equity analysis

## Expected Outcome on Synthetic Data

The DGP generates choices with fixed parameters (no built-in heterogeneity in the
person-level utility). On this data:
- Random ASC SDs should be **small and not significant**
- LR test should **fail to reject NL**
- This is the **correct result** — it demonstrates the L07 lesson that richer models
  are not always better, and statistical tests protect against over-parameterization

## Q&A Defense

**"Why Mixed Logit?"**
> Ilahi et al. (2021) Model 3 uses Mixed Logit with random ASCs for Greater Jakarta
> mode choice. L07 lectures cover three layers of heterogeneity. I applied the Mixed
> Logit as a diagnostic: test whether unobserved preference heterogeneity exists
> beyond the nest correlation captured by NL. The LR test [did/did not] find evidence
> of random taste variation.

**"How did you choose which parameters to randomize?"**
> Following Ilahi Model 3, I randomized ASCs — the alternative-specific constants.
> ASCs capture the average preference for each mode not explained by time and cost.
> Random ASCs let this preference vary across individuals. I limited randomization
> to the three modes with largest sample shares (Car, Moto, TJ) to keep the model
> identified. This mirrors Ilahi's approach where not all ASCs are random.

**"200 Halton draws — is that enough?"**
> Train (2009) shows 125–200 Halton draws achieve integration accuracy equivalent
> to ~1,000 pseudo-random draws. Ilahi used 1,000 Halton draws on a much larger
> dataset (52K obs, pooled SP/RP). For 5,000 synthetic observations, 200 draws
> are sufficient for stable simulated likelihood.

**"How does this relate to the Nested Logit?"**
> NL captures **within-nest substitution** (IIA violation across nests). Mixed Logit
> captures **individual taste heterogeneity** (some people like transit more than others).
> They address different violations of the MNL's IID error assumption. Testing both
> shows which violation matters more in this context.

## References

- Ilahi et al. (2021) Model 3 — Mixed Logit with random ASCs, Greater Jakarta
- Train (2009) — Halton sequences, simulated MLE, identification of random parameters
- L07 lecture — Three layers of heterogeneity (observed, unobserved, combined)
- Bastarianto et al. (2019) — NL ρ values used in 03

## Next Steps

1. Review this proposal
2. If approved: update `notebooks/trans-eng-final/trans-eng-final-project.md` §2 (flow diagram), §7 (add MXL DGP), §13 (notebook status)
3. Build `notebooks/trans-eng-final/03b_mixed_logit.ipynb`
4. Update `trans-eng-professor-qa.md` Q2 to reflect 4-stage model

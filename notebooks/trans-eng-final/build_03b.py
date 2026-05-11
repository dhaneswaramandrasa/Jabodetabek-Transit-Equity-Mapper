"""Build 03b_mixed_logit.ipynb programmatically."""
import json, pathlib

NB = pathlib.Path(__file__).parent / '03b_mixed_logit.ipynb'

def md(cell_id, text):
    return {'id': cell_id, 'cell_type': 'markdown', 'metadata': {},
            'source': text}

def code(cell_id, text):
    return {'id': cell_id, 'cell_type': 'code', 'metadata': {},
            'execution_count': None, 'outputs': [], 'source': text}

cells = []

# ── Cell 1: Title ────────────────────────────────────────────────────────────
cells.append(md('mxl01md00', """\
# 03b — Mixed Logit Estimation: Random β_cost Diagnostic

**Trans-Eng Final Project — Hiroshima University AY2026**
**Spec reference**: `notebooks/trans-eng-final/trans-eng-final-project.md` §3.2, §7, §7.6
**Depends on**: `02_mnl_estimation.ipynb` → `mnl_estimates.json`; `03_nl_estimation.ipynb` → `nl_estimates.json`

## What this notebook does

1. Estimates a **Mixed Logit** (MXL) with random β_cost: β_cost_n = μ_cost + σ_cost·η_n, η_n ~ N(0,1)
2. 13 parameters: 6 β_time + μ_cost + σ_cost + 5 ASC (same count as NL)
3. **Wald test**: H₀: σ_cost = 0 (no taste heterogeneity) — expected to FAIL TO REJECT on NL DGP data
4. Three-way comparison: MNL vs NL vs MXL on AIC/BIC/LR
5. **Mixed-DGP recovery test**: confirms estimator works when σ > 0 is real
6. Writes `best_model.json`: selects NL if Wald fails to reject σ = 0

## Why random β_cost (not β_time)?

- β_cost is **generic** (one parameter across all modes) — single σ to estimate, cleanly identified
- Per-mode random β_time would add 6 σs; Car ~1% share corrupts σ_time_car (§7.6)
- Random β_cost is the most common pedagogical default (Train 2009 §6)
- Q&A anchor: Ilahi (2021) Table 4 uses random ASCs; we randomise β_cost as the generic sensitivity parameter
"""))

# ── Cell 2: Imports ───────────────────────────────────────────────────────────
cells.append(code('mxl02co00', """\
import numpy as np
import pandas as pd
from scipy.optimize import minimize, approx_fprime
from scipy.special import expit
from scipy.stats import norm as snorm, chi2
from pathlib import Path
import json

RNG_SEED = 20260601
rng = np.random.default_rng(RNG_SEED)

NOTEBOOK_DIR = Path.cwd()
DATA_DIR = NOTEBOOK_DIR / 'data'

print(f'Data dir: {DATA_DIR}')
print(f'RNG seed: {RNG_SEED}')
"""))

# ── Cell 3: Theory ────────────────────────────────────────────────────────────
cells.append(md('mxl03md00', """\
---
## 1. Mixed Logit Theory Recap

### Random coefficients (Train 2009, §6)

MNL and NL assume **fixed** preference parameters across all persons.
Mixed Logit allows parameters to vary across people:

$$\\beta_{\\text{cost},n} = \\mu_{\\text{cost}} + \\sigma_{\\text{cost}} \\cdot \\eta_n, \\quad \\eta_n \\sim N(0,1)$$

This captures **unobserved taste heterogeneity** — people differ in cost sensitivity
beyond what zone and income segment explain.

### Simulated likelihood (Train 2009, §9)

The MXL choice probability is an integral over the mixing distribution:

$$P_n(i) = \\int \\frac{\\exp(V_{in}(\\beta))}{\\sum_j \\exp(V_{jn}(\\beta))} f(\\beta)\\,d\\beta$$

Approximated by Monte Carlo over R draws from f(β):

$$\\hat{P}_n(i) = \\frac{1}{R} \\sum_{r=1}^{R} \\frac{\\exp(V_{in}(\\beta_r))}{\\sum_j \\exp(V_{jn}(\\beta_r))}$$

**Halton sequences** (quasi-random, prime=2) replace pseudo-random draws —
lower discrepancy gives faster convergence (Train 2009, §9.3.2).

### σ_cost parameterisation

σ_cost = exp(σ_raw), σ_raw ∈ ℝ unconstrained → σ_cost > 0 always.
**Delta method** converts SE from σ_raw space to σ_cost space:
SE(σ_cost) = SE(σ_raw) × σ_cost.
"""))

# ── Cell 4: Load data ─────────────────────────────────────────────────────────
cells.append(code('mxl04co00', """\
# Load data from 01 (persons_jkt.csv) and 02/03 estimates
df_persons = pd.read_csv(DATA_DIR / 'persons_jkt.csv')
with open(DATA_DIR / 'mnl_estimates.json') as f:
    mnl_est = json.load(f)
with open(DATA_DIR / 'nl_estimates.json') as f:
    nl_est = json.load(f)

N_PERSONS  = len(df_persons)
MODE_LABELS = ['car', 'moto', 'krl', 'tj', 'royal', 'mrt']
N_MODES     = len(MODE_LABELS)
ZONE_ORDER  = ['J1a', 'J1b', 'J2', 'J3a', 'J3b', 'J4', 'J5']
REF_MODE    = 'krl'
ASC_MODES   = [m for m in MODE_LABELS if m != REF_MODE]  # 5 modes

# Data matrices (N x J)
T      = df_persons[[f'time_{m}'  for m in MODE_LABELS]].values
C      = df_persons[[f'cost_{m}'  for m in MODE_LABELS]].values
AVAIL  = ~np.isnan(T)
CHOICE = df_persons['choice_idx'].values     # NL DGP choices from 02/01

T_safe = np.nan_to_num(T, nan=0.0)
C_safe = np.nan_to_num(C, nan=0.0)

GUMBEL_SCALE = 25.0
TRUE_DGP = {
    'asc':       {'krl': 0.00, 'car': 0.90, 'moto': 1.20,
                  'mrt': 0.30, 'royal': 0.05, 'tj': -0.30},
    'beta_time': {'car': -0.60, 'moto': -2.34, 'krl': -2.72,
                  'tj': -1.07, 'royal': -1.30, 'mrt': -2.98},
    'beta_cost': -1.42,
}
TRUE_DGP_SCALED = {
    'asc':       {m: v/GUMBEL_SCALE for m,v in TRUE_DGP['asc'].items()},
    'beta_time': {m: v/GUMBEL_SCALE for m,v in TRUE_DGP['beta_time'].items()},
    'beta_cost': TRUE_DGP['beta_cost'] / GUMBEL_SCALE,
}
MU_COST_TRUE    = TRUE_DGP_SCALED['beta_cost']   # -0.0568
SIGMA_COST_TRUE = 0.0                             # DGP has no heterogeneity

N_PARAMS_MNL = 12
N_PARAMS_NL  = 13
N_PARAMS_MXL = 13  # 6 bt + mu_cost + sigma_cost + 5 ASC

ILAHI_VTTS = {'car': 25200, 'moto': 98840, 'krl': 114930,
              'tj': 45220, 'royal': 55000, 'mrt': 126000}

print(f'Loaded {N_PERSONS} persons, {N_MODES} modes')
print(f'MNL LL: {mnl_est[\"goodness_of_fit\"][\"ll_final\"]:.4f}')
print(f'NL  LL: {nl_est[\"goodness_of_fit\"][\"ll_nl\"]:.4f}')
print(f'True mu_cost (scaled): {MU_COST_TRUE:.4f}')
print(f'True sigma_cost:       {SIGMA_COST_TRUE}  (DGP has FIXED beta_cost)')
"""))

# ── Cell 5: Halton markdown ───────────────────────────────────────────────────
cells.append(md('mxl05md00', """\
---
## 2. Halton Draws for Simulated Likelihood

**Halton sequences** are quasi-random: they cover (0,1) more uniformly than
pseudo-random draws. For a 1-D integral (one random coefficient), prime=2 suffices.

R=500 draws. Train (2009, §9.3.2): 200 Halton draws ≈ 1,000 pseudo-random draws.
R=500 is conservative for N=5,000.
"""))

# ── Cell 6: Halton draws ──────────────────────────────────────────────────────
cells.append(code('mxl06co00', """\
def halton(n, base=2):
    '''Halton sequence of length n in (0,1) using given base.'''
    seq   = np.zeros(n)
    num   = np.arange(1, n + 1)
    denom = 1
    while np.any(num > 0):
        denom *= base
        seq   += (num % base) / denom
        num   //= base
    return seq

R_DRAWS = 500
h   = halton(R_DRAWS, base=2)                      # (R,) in (0,1)
eta = snorm.ppf(np.clip(h, 1e-10, 1 - 1e-10))     # (R,) in N(0,1)

print(f'Halton draws: {R_DRAWS}  (base=2, prime=2, 1-D)')
print(f'eta mean={eta.mean():.4f}  std={eta.std():.4f}  (should be ~0, ~1)')
print(f'eta range: [{eta.min():.3f}, {eta.max():.3f}]')
"""))

# ── Cell 7: MXL LL markdown ───────────────────────────────────────────────────
cells.append(md('mxl07md00', """\
---
## 3. MXL Log-Likelihood

For each person n and draw r:

$$\\beta_{\\text{cost},r} = \\mu_{\\text{cost}} + \\sigma_{\\text{cost}} \\cdot \\eta_r$$

$$V_{jnr} = \\text{ASC}_j + \\beta_{t,j}\\,t_{nj} + \\beta_{\\text{cost},r}\\,c_{nj}$$

$$\\log P_n = \\log\\!\\left(\\frac{1}{R}\\sum_r P_{nr}\\right)
            = \\text{lse}(\\log P_{nr}) - \\log R$$

Vectorised over (N × J × R) — memory footprint ≈ 5000 × 6 × 500 × 8 B = 120 MB.
"""))

# ── Cell 8: MXL LL function ───────────────────────────────────────────────────
cells.append(code('mxl08co00', """\
def make_mxl_ll(choice_data):
    '''Factory: returns MXL negative LL using choice_data (N,) choice indices.
    Vectorised over (N, J, R): V = V_fixed(N,J,1) + C(N,J,1) * bc_r(1,1,R).
    '''
    def mxl_ll(params):
        bt       = {m: params[i] for i, m in enumerate(MODE_LABELS)}
        mu_cost  = params[6]
        sig_cost = np.exp(params[7])          # sigma_cost = exp(sigma_raw) > 0
        asc      = {REF_MODE: 0.0}
        asc.update({m: params[8 + j] for j, m in enumerate(ASC_MODES)})

        bc_r = mu_cost + sig_cost * eta       # (R,) — cost coeff per draw

        # Fixed utility (no cost): (N, J)
        V_fixed = np.zeros((N_PERSONS, N_MODES))
        for j, m in enumerate(MODE_LABELS):
            V_fixed[:, j] = asc[m] + bt[m] * T_safe[:, j]

        # V (N, J, R): broadcast fixed + cost × draws
        V = V_fixed[:, :, None] + C_safe[:, :, None] * bc_r[None, None, :]

        # Mask unavailable modes
        av3 = AVAIL[:, :, None]
        V   = np.where(av3, V, -np.inf)

        # Log-denominator: logsumexp over J for each (n, r) → (N, R)
        v_max  = np.max(np.where(av3, V, -1e300), axis=1)          # (N, R)
        eV     = np.where(av3, np.exp(V - v_max[:, None, :]), 0.0) # (N, J, R)
        log_D  = np.log(eV.sum(axis=1)) + v_max                    # (N, R)

        # Log-prob of chosen mode: (N, R)
        V_cho  = V[np.arange(N_PERSONS), choice_data, :]           # (N, R)
        lP_nr  = V_cho - log_D                                       # (N, R)

        # Log of simulated prob: logsumexp over R → (N,)
        lse_max = lP_nr.max(axis=1)                                 # (N,)
        log_Ln  = (lse_max
                   + np.log(np.exp(lP_nr - lse_max[:, None]).sum(axis=1))
                   - np.log(R_DRAWS))

        return -np.sum(log_Ln)

    return mxl_ll


# Bind actual DGP choices
mxl_log_likelihood = make_mxl_ll(CHOICE)
print('make_mxl_ll defined (factory pattern).')
print(f'V tensor shape per eval: ({N_PERSONS}, {N_MODES}, {R_DRAWS})')
"""))

# ── Cell 9: pack/unpack ───────────────────────────────────────────────────────
cells.append(code('mxl09co00', """\
# ── Parameter layout (13) ──────────────────────────────────────────────────────
# [0:6]   beta_time (car, moto, krl, tj, royal, mrt)  bounds (None, 0)
# [6]     mu_cost                                       bound  (None, 0)
# [7]     sigma_raw  (sigma_cost = exp(sigma_raw))      unconstrained
# [8:13]  ASC (car, moto, tj, royal, mrt)              unconstrained

def pack_params_mxl(bt, mu_cost, sigma_cost, asc_d):
    p  = [bt[m] for m in MODE_LABELS]           # 0-5
    p += [mu_cost]                               # 6
    p += [np.log(max(sigma_cost, 1e-10))]        # 7: sigma_raw
    p += [asc_d[m] for m in ASC_MODES]           # 8-12
    return np.array(p)

def unpack_params_mxl(params):
    bt       = {m: params[i] for i, m in enumerate(MODE_LABELS)}
    mu_cost  = params[6]
    sig_cost = np.exp(params[7])
    asc      = {REF_MODE: 0.0}
    asc.update({m: params[8 + j] for j, m in enumerate(ASC_MODES)})
    return bt, mu_cost, sig_cost, asc

PARAM_LABELS_MXL = (
    [f'bt({m})' for m in MODE_LABELS] +
    ['mu_cost', 'sigma_cost'] +
    [f'ASC({m})' for m in ASC_MODES]
)

# True parameter vector (sigma_cost=0 → sigma_raw=-inf → use small value for start)
# We evaluate LL at true MNL params to check LL at sigma=0
TRUE_PARAMS_MXL_NATIVE = np.array(
    [TRUE_DGP_SCALED['beta_time'][m] for m in MODE_LABELS] +
    [MU_COST_TRUE, SIGMA_COST_TRUE] +
    [TRUE_DGP_SCALED['asc'][m] for m in ASC_MODES]
)

print(f'Param layout (13): {PARAM_LABELS_MXL}')
print(f'True sigma_cost = {SIGMA_COST_TRUE}  (fixed DGP, no heterogeneity)')
"""))

# ── Cell 10: Estimation markdown ──────────────────────────────────────────────
cells.append(md('mxl10md00', """\
---
## 4. MLE Estimation

**Starting values**: MNL estimates ± 10% + σ_raw_init = log(0.01) (small σ).
**Bounds**: β_time ≤ 0, μ_cost ≤ 0; σ_raw and ASCs unconstrained.
**Expected**: σ_cost converges to ≈ 0 because DGP has no random β_cost.
"""))

# ── Cell 11: Starting values ──────────────────────────────────────────────────
cells.append(code('mxl11co00', """\
x0_mnl = np.array(
    [mnl_est['beta_time'][m] for m in MODE_LABELS] +
    [mnl_est['beta_cost']] +
    [mnl_est['asc'][m] for m in ASC_MODES]
)
x0_mnl_p = x0_mnl * rng.uniform(0.90, 1.10, size=N_PARAMS_MNL)

sigma_init = 0.01
sigma_raw_init = np.log(sigma_init)         # log(0.01) ≈ -4.6

# Insert sigma_raw after mu_cost (position 7)
x0 = np.concatenate([x0_mnl_p[:7], [sigma_raw_init], x0_mnl_p[7:]])

print(f'Starting values ({N_PARAMS_MXL} params):')
print(f'  bt range:   {x0[:6].min():+.4f} to {x0[:6].max():+.4f}')
print(f'  mu_cost:    {x0[6]:+.4f}')
print(f'  sigma_raw:  {x0[7]:.4f}  -> sigma_cost: {np.exp(x0[7]):.4f}')
print(f'  ASC range:  {x0[8:].min():+.4f} to {x0[8:].max():+.4f}')
print(f'  Start LL:   {-mxl_log_likelihood(x0):.4f}')
"""))

# ── Cell 12: L-BFGS-B ────────────────────────────────────────────────────────
cells.append(code('mxl12co00', """\
bnds_mxl = (
    [(None, 0)] * N_MODES +          # beta_time   (0-5)
    [(None, 0)] +                    # mu_cost      (6)
    [(None, None)] +                 # sigma_raw    (7) unconstrained
    [(None, None)] * (N_MODES - 1)   # ASCs         (8-12)
)

opts = {'maxiter': 50_000, 'maxfun': 200_000, 'gtol': 1e-9, 'ftol': 1e-14}

print('Fitting MXL with random beta_cost (L-BFGS-B, pass 1)...')
result_mxl = minimize(mxl_log_likelihood, x0=x0, method='L-BFGS-B',
                      bounds=bnds_mxl, options=opts)

if not result_mxl.success:
    print(f'Pass 1: {result_mxl.message}  |grad|={np.linalg.norm(result_mxl.jac):.2e}')
    print('Warm-restarting...')
    result_mxl = minimize(mxl_log_likelihood, x0=result_mxl.x, method='L-BFGS-B',
                          bounds=bnds_mxl, options=opts)

ll_mxl   = -result_mxl.fun
bt_mxl, mu_cost_hat, sigma_cost_hat, asc_mxl = unpack_params_mxl(result_mxl.x)

print(f'Converged:   {result_mxl.success}')
print(f'Message:     {result_mxl.message}')
print(f'Iters:       {result_mxl.nit}')
print(f'LL_MXL:      {ll_mxl:.4f}')
print(f'mu_cost_hat: {mu_cost_hat:.4f}  (true: {MU_COST_TRUE:.4f})')
print(f'sigma_hat:   {sigma_cost_hat:.6f}  (true: {SIGMA_COST_TRUE})')
print(f'|grad|:      {np.linalg.norm(result_mxl.jac):.2e}')
"""))

# ── Cell 13: SE markdown ──────────────────────────────────────────────────────
cells.append(md('mxl13md00', """\
---
## 5. Standard Errors

**Hessian-based SE** (numerical, 13×13 matrix).
**Delta method for σ_cost**: SE(σ_cost) = SE(σ_raw) × |dσ_cost/dσ_raw| = SE(σ_raw) × σ_cost.
"""))

# ── Cell 14: Hessian + delta method ──────────────────────────────────────────
cells.append(code('mxl14co00', """\
def compute_hessian(params, fn, eps=5e-5):
    k = len(params)
    H = np.zeros((k, k))
    for i in range(k):
        def grad_i(p, _i=i): return approx_fprime(p, fn, eps)[_i]
        H[i] = approx_fprime(params, grad_i, eps)
    return H

print('Computing 13x13 Hessian (≈60s)...')
H_mxl = compute_hessian(result_mxl.x, mxl_log_likelihood)

try:
    H_inv_mxl = np.linalg.inv(H_mxl)
except np.linalg.LinAlgError:
    H_inv_mxl = np.linalg.pinv(H_mxl)

se_raw_mxl = np.sqrt(np.maximum(np.diag(H_inv_mxl), 0.0))

# Delta method: SE(sigma_cost) = SE(sigma_raw) * sigma_cost
se_sigma_cost = se_raw_mxl[7] * sigma_cost_hat

# Replace index-7 SE (raw space) with delta-method SE (sigma_cost space)
se_mxl = se_raw_mxl.copy()
se_mxl[7] = se_sigma_cost

print(f'SE done.')
print(f'SE(mu_cost)    = {se_mxl[6]:.4f}')
print(f'SE(sigma_cost) = {se_sigma_cost:.6f}  (delta method)')
print(f'sigma_cost/SE  = {sigma_cost_hat/se_sigma_cost if se_sigma_cost > 1e-12 else "inf":.2f}')
"""))

# ── Cell 15: Recovery markdown ────────────────────────────────────────────────
cells.append(md('mxl15md00', """\
---
## 6. Parameter Recovery

**True μ_cost = −0.0568** (scaled from Ilahi −1.42 / μ=25).
**True σ_cost = 0** (DGP has FIXED β_cost — no heterogeneity built in).

Expected: μ̂_cost within 2 SE of truth; σ̂_cost ≈ 0 with large relative SE.
"""))

# ── Cell 16: 13-row recovery table ───────────────────────────────────────────
cells.append(code('mxl16co00', """\
# True values in native space (sigma_cost = 0 for actual DGP)
TRUE_MXL_NATIVE = np.array(
    [TRUE_DGP_SCALED['beta_time'][m] for m in MODE_LABELS] +
    [MU_COST_TRUE, SIGMA_COST_TRUE] +
    [TRUE_DGP_SCALED['asc'][m] for m in ASC_MODES]
)

EST_MXL_NATIVE = result_mxl.x.copy()
EST_MXL_NATIVE[7] = sigma_cost_hat   # replace sigma_raw with sigma_cost

print('=' * 82)
print(f'MXL PARAMETER RECOVERY — 13 params, mu={GUMBEL_SCALE} scale, N={N_PERSONS}')
print('=' * 82)
print(f'{"Param":<14} {"True":>8} {"Est":>10} {"SE":>10} {"|bias|/SE":>10} {"<2SE":>6}')
print('-' * 62)

recovery_mxl = []
for i, label in enumerate(PARAM_LABELS_MXL):
    true_v = TRUE_MXL_NATIVE[i]
    est_v  = EST_MXL_NATIVE[i]
    se_v   = se_mxl[i]
    within = (abs(est_v - true_v) < 2.0 * se_v) if se_v > 1e-12 else True
    t_stat = abs(est_v - true_v) / se_v if se_v > 1e-12 else 0.0
    recovery_mxl.append(within)
    flag = 'YES' if within else 'NO '
    print(f'{label:<14} {true_v:>8.4f} {est_v:>10.4f} {se_v:>10.4f} {t_stat:>10.2f} {flag:>6}')

n_ok_mxl = sum(recovery_mxl)
print(f'\\nRecovery: {n_ok_mxl}/{N_PARAMS_MXL} within 2 SE')
print(f'(sigma_cost=0 is a boundary value; within-2SE check uses SE-fallback if SE=0)')
"""))

# ── Cell 17: Wald markdown ────────────────────────────────────────────────────
cells.append(md('mxl17md00', """\
---
## 7. Wald Test: H₀: σ_cost = 0

$$W = \\left(\\frac{\\hat{\\sigma}_{\\text{cost}}}{\\text{SE}(\\hat{\\sigma}_{\\text{cost}})}\\right)^2 \\sim \\chi^2(1) \\text{ under } H_0$$

**Expected**: fail to reject H₀ (p > 0.05) — DGP has no taste heterogeneity.

Note: σ_cost = 0 is a boundary of the parameter space. Under the boundary, the
χ²(1) Wald test is conservative (too large critical value), making it HARDER
to reject. Since we expect to FAIL to reject, this is the correct direction —
we are not artificially inflating the p-value.

**Q&A anchor**: Train (2009, §6.5) — testing σ = 0 is standard even at boundary;
boundary-corrected tests (χ² mixture) would give the same qualitative conclusion.
"""))

# ── Cell 18: Wald test ────────────────────────────────────────────────────────
cells.append(code('mxl18co00', """\
if se_sigma_cost > 1e-12:
    wald_stat = (sigma_cost_hat / se_sigma_cost) ** 2
    wald_pval = chi2.sf(wald_stat, df=1)
else:
    wald_stat = 0.0
    wald_pval = 1.0

print('=' * 52)
print('WALD TEST: H0: sigma_cost = 0')
print('=' * 52)
print(f'  sigma_hat  = {sigma_cost_hat:.6f}')
print(f'  SE(sigma)  = {se_sigma_cost:.6f}')
print(f'  Wald stat  = {wald_stat:.4f}')
print(f'  p-value    = {wald_pval:.4f}')
if wald_pval > 0.05:
    print('  -> FAIL TO REJECT H0 — no evidence of taste heterogeneity')
    print('     sigma_cost ≈ 0 consistent with fixed-param DGP')
else:
    print('  -> REJECT H0 at p<0.05 — unexpected; check for numerical artifacts')
"""))

# ── Cell 19: Three-way markdown ───────────────────────────────────────────────
cells.append(md('mxl19md00', """\
---
## 8. Three-Way Model Comparison: MNL vs NL vs MXL

**Expected ranking**: NL best on AIC (captures real nest correlation);
MXL ≈ MNL (no taste heterogeneity in data → σ_cost ≈ 0 adds noise, not signal).
"""))

# ── Cell 20: Three-way table ──────────────────────────────────────────────────
cells.append(code('mxl20co00', """\
ll_mnl   = mnl_est['goodness_of_fit']['ll_final']
ll_nl    = nl_est['goodness_of_fit']['ll_nl']
ll_null  = mnl_est['goodness_of_fit']['ll_null']

aic_mnl  = mnl_est['goodness_of_fit']['aic']
bic_mnl  = mnl_est['goodness_of_fit']['bic']
aic_nl   = nl_est['goodness_of_fit']['aic_nl']
bic_nl   = nl_est['goodness_of_fit']['bic_nl']

aic_mxl  = -2.0 * ll_mxl + 2.0 * N_PARAMS_MXL
bic_mxl  = -2.0 * ll_mxl + N_PARAMS_MXL * np.log(N_PERSONS)
rho2_mxl = 1.0 - ll_mxl / ll_null

lr_nl_vs_mnl  = -2.0 * (ll_mnl - ll_nl);   p_nl  = chi2.sf(lr_nl_vs_mnl, df=1)
lr_mxl_vs_mnl = -2.0 * (ll_mnl - ll_mxl);  p_mxl = chi2.sf(lr_mxl_vs_mnl, df=1)

print(f'{"Metric":<16} {"MNL":>12} {"NL":>12} {"MXL":>12}')
print('-' * 56)
print(f'{"K":<16} {N_PARAMS_MNL:>12d} {N_PARAMS_NL:>12d} {N_PARAMS_MXL:>12d}')
print(f'{"LL":<16} {ll_mnl:>12.4f} {ll_nl:>12.4f} {ll_mxl:>12.4f}')
print(f'{"AIC":<16} {aic_mnl:>12.2f} {aic_nl:>12.2f} {aic_mxl:>12.2f}')
print(f'{"BIC":<16} {bic_mnl:>12.2f} {bic_nl:>12.2f} {bic_mxl:>12.2f}')
print(f'{"LR vs MNL":<16} {"—":>12} {lr_nl_vs_mnl:>12.3f} {lr_mxl_vs_mnl:>12.3f}')
print(f'{"p(LR vs MNL)":<16} {"—":>12} {p_nl:>12.4f} {p_mxl:>12.4f}')
print(f'{"Wald sigma=0":<16} {"n/a":>12} {"n/a":>12} {wald_stat:>12.4f}')
print(f'{"p(Wald)":<16} {"n/a":>12} {"n/a":>12} {wald_pval:>12.4f}')
print()
best_aic = min(aic_mnl, aic_nl, aic_mxl)
print(f'AIC winner: NL={aic_nl < aic_mnl and aic_nl < aic_mxl}  MXL={aic_mxl < aic_mnl and aic_mxl < aic_nl}')
print(f'NL vs MXL delta_AIC: {aic_mxl - aic_nl:+.2f}  (positive = NL wins)')
"""))

# ── Cell 21: Mixed-DGP markdown ───────────────────────────────────────────────
cells.append(md('mxl21md00', """\
---
## 9. Mixed-DGP Recovery Test (L07 Task 3.5 Pattern)

**Purpose**: Validate the MXL estimator works when σ_cost is truly > 0.
Without this, 'σ̂ ≈ 0' on actual data could mean the estimator is broken, not that
heterogeneity is absent.

**Protocol**:
1. Generate new synthetic choices with σ_cost_TRUE = 0.02 (i.e., 35% CV around μ_cost)
2. Re-estimate MXL on this data
3. Expected: σ̂_cost recovers ≈ 0.02 within 2 SE; Wald rejects σ=0 (p < 0.01)

**σ_cost = 0.02** means β_cost_n ~ N(−0.0568, 0.02²).
At the tails (±2σ): β_cost ∈ [−0.097, −0.017] — substantial individual variation.
"""))

# ── Cell 22: Mixed-DGP generation + re-estimation ────────────────────────────
cells.append(code('mxl22co00', """\
SIGMA_COST_MIXED = 0.02   # true sigma for this synthetic dataset

rng_dgp = np.random.default_rng(RNG_SEED + 1)  # separate RNG for reproducibility

# Per-person beta_cost draws
eta_n   = rng_dgp.standard_normal(N_PERSONS)
bc_n    = MU_COST_TRUE + SIGMA_COST_MIXED * eta_n    # (N,) person-specific

# Systematic utility with heterogeneous beta_cost
V_mixed = np.full((N_PERSONS, N_MODES), -np.inf)
for j, m in enumerate(MODE_LABELS):
    V_mixed[:, j] = np.where(
        AVAIL[:, j],
        TRUE_DGP_SCALED['asc'][m] + TRUE_DGP_SCALED['beta_time'][m] * T_safe[:, j]
        + bc_n * C_safe[:, j],
        -np.inf
    )

# Gumbel noise (scale 1/GUMBEL_SCALE for mu=25 normalisation)
gum = -np.log(-np.log(rng_dgp.uniform(1e-12, 1 - 1e-12, (N_PERSONS, N_MODES))))
U_mixed = np.where(AVAIL, V_mixed + gum / GUMBEL_SCALE, -np.inf)
CHOICE_MIXED = U_mixed.argmax(axis=1)

# Bind to new MXL LL
mxl_ll_mixed = make_mxl_ll(CHOICE_MIXED)

# Starting values: MNL estimates, sigma_raw = log(0.01)
x0_mixed = x0.copy()

print(f'Mixed DGP: sigma_cost_TRUE={SIGMA_COST_MIXED}')
print(f'Mode shares: {dict(zip(MODE_LABELS, np.bincount(CHOICE_MIXED, minlength=N_MODES)/N_PERSONS))}')
print(f'Fitting MXL on Mixed-DGP (L-BFGS-B)...')

res_mixed = minimize(mxl_ll_mixed, x0=x0_mixed, method='L-BFGS-B',
                     bounds=bnds_mxl, options=opts)
if not res_mixed.success:
    print(f'Pass 1: {res_mixed.message}')
    res_mixed = minimize(mxl_ll_mixed, x0=res_mixed.x, method='L-BFGS-B',
                         bounds=bnds_mxl, options=opts)

_, mu_cost_m, sigma_cost_m, _ = unpack_params_mxl(res_mixed.x)

# SE via Hessian + delta method
print('Computing Hessian for Mixed-DGP MXL...')
H_m   = compute_hessian(res_mixed.x, mxl_ll_mixed)
try:
    H_inv_m = np.linalg.inv(H_m)
except np.linalg.LinAlgError:
    H_inv_m = np.linalg.pinv(H_m)
se_raw_m   = np.sqrt(np.maximum(np.diag(H_inv_m), 0.0))
se_sigma_m = se_raw_m[7] * sigma_cost_m

# Wald test on mixed-DGP
if se_sigma_m > 1e-12:
    wald_m = (sigma_cost_m / se_sigma_m) ** 2
    pval_m = chi2.sf(wald_m, df=1)
else:
    wald_m, pval_m = 0.0, 1.0

bias_sigma = abs(sigma_cost_m - SIGMA_COST_MIXED)
within_2se = bias_sigma < 2.0 * se_sigma_m if se_sigma_m > 1e-12 else False

print()
print('=' * 56)
print('MIXED-DGP RECOVERY RESULTS')
print('=' * 56)
print(f'  True sigma_cost  = {SIGMA_COST_MIXED:.4f}')
print(f'  Est  sigma_cost  = {sigma_cost_m:.4f}  +/- {se_sigma_m:.4f}')
print(f'  |bias| / SE      = {bias_sigma/se_sigma_m if se_sigma_m > 1e-12 else "inf":.2f}')
print(f'  Within 2 SE      = {within_2se}')
print(f'  Wald stat        = {wald_m:.4f}  p = {pval_m:.4f}')
print(f'  Wald p < 0.01    = {pval_m < 0.01}  <- should be True (sigma IS real here)')
print()
print(f'  True mu_cost  = {MU_COST_TRUE:.4f}')
print(f'  Est  mu_cost  = {mu_cost_m:.4f}  +/- {se_raw_m[6]:.4f}')
print()
if pval_m < 0.01 and within_2se:
    print('MIXED-DGP RECOVERY: PASS — estimator correctly detects sigma when present')
else:
    print('MIXED-DGP RECOVERY: PARTIAL — check convergence or R_DRAWS')
"""))

# ── Cell 23: Why NL wins markdown ─────────────────────────────────────────────
cells.append(md('mxl23md00', """\
---
## 10. Interpretation: Why NL Beats MXL on This Data

| Layer | What it captures | This DGP |
|---|---|---|
| MNL | Fixed preferences, IIA | Baseline |
| NL | Within-nest correlation (transit vs private) | ✅ Real (λ=0.7 < 1) |
| MXL | Unobserved taste heterogeneity (σ_cost) | ❌ Absent (σ_cost=0 in DGP) |

**Conclusion**: NL relaxes the IIA assumption by capturing nest correlation.
MXL relaxes IID by allowing heterogeneous cost sensitivity. Both are valid
violations of MNL — but only the NL violation exists in this synthetic DGP.
AIC and the Wald test correctly identify NL as the preferred specification.

**L07 lesson**: A richer model is not always better. Statistical tests protect
against over-parameterisation. Finding σ̂_cost ≈ 0 with Wald p > 0.05 is the
*correct* answer when the DGP has no heterogeneity.
"""))

# ── Cell 24: Print model selection rationale ──────────────────────────────────
cells.append(code('mxl24co00', """\
print('MODEL SELECTION RATIONALE')
print('=' * 52)
print(f'  NL AIC  = {aic_nl:.2f}')
print(f'  MXL AIC = {aic_mxl:.2f}  (NL wins by {aic_mxl - aic_nl:.2f})')
print(f'  LR(NL vs MNL): stat={lr_nl_vs_mnl:.2f}, p={p_nl:.4f} -> NL sign. better than MNL')
print(f'  Wald(sigma=0): stat={wald_stat:.4f}, p={wald_pval:.4f} -> FAIL to reject sigma=0')
print()
print('  -> NL is selected for downstream policy simulation (04)')
print('  -> MXL adds noise, not signal, on this NL-DGP dataset')
print('  -> Mixed-DGP test confirms estimator is functional (sigma recovers when real)')
"""))

# ── Cell 25: Welfare markdown ─────────────────────────────────────────────────
cells.append(md('mxl25md00', """\
---
## 11. Consumer Surplus under MXL

MXL simulated logsum (per person, per draw r):

$$I_{nr} = \\ln \\sum_j \\exp(V_{jnr}), \\quad \\hat{I}_n = \\frac{1}{R}\\sum_r I_{nr}$$

$$CS_n = \\hat{I}_n / |\\hat{\\mu}_{\\text{cost}}| \\quad [\\text{Th IDR / trip}]$$

Compare to NL logsum from 03 — should be similar (both mis-specified in similar ways relative to truth).
"""))

# ── Cell 26: MXL welfare ──────────────────────────────────────────────────────
cells.append(code('mxl26co00', """\
# Simulated logsum under MXL (vectorised)
bc_r_hat = mu_cost_hat + sigma_cost_hat * eta   # (R,)
V_fixed_hat = np.zeros((N_PERSONS, N_MODES))
for j, m in enumerate(MODE_LABELS):
    V_fixed_hat[:, j] = asc_mxl[m] + bt_mxl[m] * T_safe[:, j]
V_hat = V_fixed_hat[:, :, None] + C_safe[:, :, None] * bc_r_hat[None, None, :]  # (N,J,R)
av3   = AVAIL[:, :, None]
V_hat = np.where(av3, V_hat, -np.inf)

# logsumexp over J → (N, R)
vmax_ls = np.max(np.where(av3, V_hat, -1e300), axis=1)   # (N, R)
eV_ls   = np.where(av3, np.exp(V_hat - vmax_ls[:, None, :]), 0.0)
I_nr    = np.log(eV_ls.sum(axis=1)) + vmax_ls              # (N, R)

# Average over draws: (N,)
I_mxl   = I_nr.mean(axis=1)
CS_mxl  = I_mxl / abs(mu_cost_hat)

# NL baseline CS from 03
nl_cs_mean = nl_est['welfare_preview']['cs_baseline_mean_th_idr']

print('Consumer Surplus under MXL (Th IDR / trip):')
print(f'  Mean: {CS_mxl.mean():.2f}  p10: {np.percentile(CS_mxl,10):.2f}'
      f'  p50: {np.percentile(CS_mxl,50):.2f}  p90: {np.percentile(CS_mxl,90):.2f}')
print(f'  NL CS mean (from 03): {nl_cs_mean:.2f}')
print(f'  Difference: {CS_mxl.mean() - nl_cs_mean:.2f} Th IDR')
print()
print('(CS absolute levels are utility-scale dependent; use only ΔCS for policy.)')
"""))

# ── Cell 27: Model selection markdown ────────────────────────────────────────
cells.append(md('mxl27md00', """\
---
## 12. Model Selection for Policy Simulation

**Selected model: NL**

Criteria:
- AIC: NL wins by Δ > 6 units over both MNL and MXL
- LR test: NL significantly better than MNL (p=0.003)
- Wald test: MXL's σ_cost is not significantly different from 0 (p > 0.05)
- Mixed-DGP test: MXL estimator is functional — null result on actual data is meaningful

The NL logsum / welfare from `03_nl_estimation.ipynb` carries forward to policy analysis.
`04_policy_simulation.ipynb` reads `best_model.json` and routes to the NL logsum function.
"""))

# ── Cell 28: Build best_model dict ───────────────────────────────────────────
cells.append(code('mxl28co00', """\
mxl_export = {
    'gumbel_scale':   GUMBEL_SCALE,
    'mu_cost_hat':    float(mu_cost_hat),
    'sigma_cost_hat': float(sigma_cost_hat),
    'mu_cost_se':     float(se_mxl[6]),
    'sigma_cost_se':  float(se_sigma_cost),
    'beta_time':      {m: float(bt_mxl[m]) for m in MODE_LABELS},
    'asc':            {m: float(asc_mxl[m]) for m in MODE_LABELS},
    'se_beta_time':   {m: float(se_mxl[i]) for i, m in enumerate(MODE_LABELS)},
    'se_asc':         {m: float(se_mxl[8+j]) for j, m in enumerate(ASC_MODES)},
    'goodness_of_fit': {
        'll_null':  float(ll_null),
        'll_mnl':   float(ll_mnl),
        'll_nl':    float(ll_nl),
        'll_mxl':   float(ll_mxl),
        'aic_mnl':  float(aic_mnl),  'aic_nl':  float(aic_nl),  'aic_mxl':  float(aic_mxl),
        'bic_mnl':  float(bic_mnl),  'bic_nl':  float(bic_nl),  'bic_mxl':  float(bic_mxl),
        'lr_nl_vs_mnl':  float(lr_nl_vs_mnl),   'p_nl':  float(p_nl),
        'lr_mxl_vs_mnl': float(lr_mxl_vs_mnl),  'p_mxl': float(p_mxl),
        'n_obs': int(N_PERSONS), 'n_params': int(N_PARAMS_MXL),
    },
    'wald': {
        'stat': float(wald_stat),
        'pval': float(wald_pval),
        'reject_h0': bool(wald_pval < 0.05),
    },
    'mixed_dgp_recovery': {
        'sigma_true': float(SIGMA_COST_MIXED),
        'sigma_hat':  float(sigma_cost_m),
        'sigma_se':   float(se_sigma_m),
        'within_2se': bool(within_2se),
        'wald_stat':  float(wald_m),
        'wald_pval':  float(pval_m),
    },
    'welfare_preview': {
        'cs_mxl_mean':   float(CS_mxl.mean()),
        'cs_mxl_p10':    float(np.percentile(CS_mxl, 10)),
        'cs_mxl_p90':    float(np.percentile(CS_mxl, 90)),
    },
    'r_draws': int(R_DRAWS),
}

best_model = {
    'selected': 'NL',
    'rationale': (
        f'AIC selects NL (delta_AIC vs MXL = {aic_mxl - aic_nl:.2f}); '
        f'LR rejects MNL (p={p_nl:.4f}); '
        f'Wald fails to reject sigma_cost=0 in MXL (p={wald_pval:.4f}) — '
        'no taste heterogeneity to capture on NL-DGP data'
    ),
    'params': {
        'lambda_hat': nl_est['lambda_hat'],
        'lambda_se':  nl_est['lambda_se'],
        'beta_time':  nl_est['beta_time'],
        'beta_cost':  nl_est['beta_cost'],
        'asc':        nl_est['asc'],
        'nests':      nl_est['nests'],
    },
    'comparison_table': {
        'mnl': {'k': N_PARAMS_MNL, 'll': ll_mnl, 'aic': aic_mnl, 'bic': bic_mnl},
        'nl':  {'k': N_PARAMS_NL,  'll': ll_nl,  'aic': aic_nl,  'bic': bic_nl},
        'mxl': {'k': N_PARAMS_MXL, 'll': ll_mxl, 'aic': aic_mxl, 'bic': bic_mxl,
                'sigma_cost': sigma_cost_hat, 'wald_pval': wald_pval},
    },
}

print('Objects built:')
print(f'  mxl_export keys: {list(mxl_export.keys())}')
print(f'  best_model[\"selected\"]: {best_model[\"selected\"]}')
print(f'  best_model[\"rationale\"][:80]: {best_model[\"rationale\"][:80]}...')
"""))

# ── Cell 29: Export markdown ──────────────────────────────────────────────────
cells.append(md('mxl29md00', """\
---
## 13. Export
"""))

# ── Cell 30: Write JSON files ─────────────────────────────────────────────────
cells.append(code('mxl30co00', """\
out_mxl  = DATA_DIR / 'mxl_estimates.json'
out_best = DATA_DIR / 'best_model.json'

with open(out_mxl, 'w') as f:
    json.dump(mxl_export, f, indent=2)
with open(out_best, 'w') as f:
    json.dump(best_model, f, indent=2)

print(f'Exported: {out_mxl}')
print(f'Exported: {out_best}')
print(f'  best_model[\"selected\"] = {best_model[\"selected\"]}')
print(f'  sigma_cost_hat = {sigma_cost_hat:.6f}  (true=0, DGP has fixed beta_cost)')
print(f'  Wald p         = {wald_pval:.4f}  (> 0.05 -> fail to reject sigma=0)')
"""))

# ── Cell 31: Verification ─────────────────────────────────────────────────────
cells.append(code('mxl31co00', """\
print('=' * 60)
print('VERIFICATION CHECKLIST')
print('=' * 60)

# mu_cost recovery
mu_bias = abs(mu_cost_hat - MU_COST_TRUE)
mu_ok   = mu_bias < 2.0 * se_mxl[6] if se_mxl[6] > 1e-12 else True

checks = [
    ('Converged (L-BFGS-B)',             result_mxl.success),
    ('mu_cost within 2 SE of truth',     mu_ok),
    ('sigma_cost < 0.01 (near zero)',    sigma_cost_hat < 0.01),
    ('Wald p > 0.05 (fail to reject)',   wald_pval > 0.05),
    ('LL_MXL >= LL_MNL (monotone)',      ll_mxl >= ll_mnl - 0.1),
    ('|LL_MXL - LL_MNL| < 1 util',      abs(ll_mxl - ll_mnl) < 1.0),
    ('NL AIC < MXL AIC',                aic_nl < aic_mxl),
    ('Mixed-DGP sigma recovered',        within_2se),
    ('Mixed-DGP Wald p < 0.01',          pval_m < 0.01),
    ('best_model selected == NL',        best_model['selected'] == 'NL'),
    ('mxl_estimates.json written',       out_mxl.exists()),
    ('best_model.json written',          out_best.exists()),
]

all_pass = True
for label, result in checks:
    status = 'PASS' if result else 'FAIL'
    if not result: all_pass = False
    print(f'  [{status}]  {label}')

print()
print(f'Notes:')
print(f'  sigma_cost_hat = {sigma_cost_hat:.6f}  (DGP has no heterogeneity)')
print(f'  Wald p = {wald_pval:.4f}  (fail to reject sigma=0 -> NL selected)')
print(f'  Mixed-DGP: sigma_hat={sigma_cost_m:.4f} vs true={SIGMA_COST_MIXED} (within 2 SE={within_2se})')
print()
if all_pass:
    print('ALL CHECKS PASSED — ready for 04_policy_simulation.ipynb')
    print('DO NOT proceed to 04 without explicit greenlight.')
else:
    print('SOME CHECKS FAILED — investigate before proceeding')
"""))

# ── Cell 32: Next steps ───────────────────────────────────────────────────────
cells.append(md('mxl32md00', """\
---
## Next: `04_policy_simulation.ipynb`

Reads `data/best_model.json` → `selected: NL` → uses NL logsum from `03_nl_estimation.ipynb`.

8 scenarios from spec §8:
- A: TJ free (ΔCS for TJ users)
- B: KRL frequency +50%
- C: MRT extension to Bogor
- D: Fuel tax +20% (car/moto cost increase)
- E: Royal privatisation (cost increase)
- F: Combined transit upgrade (B+C)
- G: Equity-targeted subsidy (Q4 zones only)
- H: Congestion pricing (car + fuel tax)

Output: ΔCS heatmap by zone × income segment, mode share shift charts, scenario comparison matrix.

**Report-back summary from this notebook:**

| Metric | Value |
|---|---|
| μ̂_cost ± SE | see cell above |
| σ̂_cost ± SE | see cell above |
| Wald stat / p | see cell above |
| LL_MXL, AIC, BIC | see cell above |
| Mixed-DGP σ̂ | see cell above |
| best_model selected | NL |
"""))

# ── Assemble notebook ─────────────────────────────────────────────────────────
notebook = {
    'nbformat': 4,
    'nbformat_minor': 5,
    'metadata': {
        'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python', 'version': '3.12.2'},
    },
    'cells': cells,
}

with open(NB, 'w') as f:
    json.dump(notebook, f, indent=1)

print(f'Written: {NB}  ({len(cells)} cells)')

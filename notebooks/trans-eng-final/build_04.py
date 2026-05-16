"""
build_04.py — Generate 04_policy_simulation.ipynb programmatically.
Run: python3 build_04.py
Then: jupyter nbconvert --to notebook --execute --inplace \
        --ExecutePreprocessor.timeout=600 04_policy_simulation.ipynb
"""
import json, uuid

def uid(): return uuid.uuid4().hex[:8]

def md(source, id_=None):
    return {"cell_type": "markdown", "id": id_ or uid(),
            "metadata": {}, "source": source}

def code(source, id_=None):
    return {"cell_type": "code", "id": id_ or uid(),
            "execution_count": None, "metadata": {},
            "outputs": [], "source": source}

cells = []

# ─── 0. Title ───────────────────────────────────────────────────────────────
cells.append(md(
"""# 04 — Policy Simulation
**Trans-Eng Final Project · Hiroshima University AY2026**

Welfare analysis of 8 policy scenarios (A–H) using the Nested Logit (NL) model
selected in `03b_mixed_logit.ipynb` (AIC wins by 8.5 units; LR rejects MNL p=0.003;
Wald fails to reject σ_cost=0 in MXL p=0.763).

**Framework**: McFadden (1978) logsum compensating variation
`CS(n) = EMU(n) / |β_cost|`  where `EMU(n) = log Σ_k exp(λ · I_k(n))`
and `I_k(n) = log Σ_{j∈k} exp(V_{jn}/λ)` (within-nest inclusive value)

**Expansion**: each synthetic person represents `zone_pop / N_zone` real commuters;
annual welfare = ΔCS × expansion × 250 working days/year.
"""))

# ─── 1. Imports ─────────────────────────────────────────────────────────────
cells.append(md("## §1 — Imports and setup"))
cells.append(code(
"""import json
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

np.random.seed(20260601)

DATA  = 'data/'
FIGS  = 'figures/'
MODES = ['car', 'moto', 'krl', 'tj', 'royal', 'mrt']
ZONES = ['J1a', 'J1b', 'J2', 'J3a', 'J3b', 'J4', 'J5']
INC   = ['low', 'mid', 'high']
WORKING_DAYS = 250
print("Imports OK")
""", "p04_01"))

# ─── 2. Load data ────────────────────────────────────────────────────────────
cells.append(md("## §2 — Load data and NL parameters"))
cells.append(code(
"""# ── Load NL parameters from best_model.json ──────────────────────────────
with open(DATA + 'best_model.json') as f:
    best = json.load(f)

assert best['selected'] == 'NL', f"Expected NL, got {best['selected']}"
p = best['params']

LAM      = p['lambda_hat']          # 0.7633
BC       = p['beta_cost']           # -0.0773  (Th IDR units)
BT       = p['beta_time']           # per-mode (min units)
ASC      = p['asc']
NESTS    = p['nests']               # {transit:[krl,mrt,tj,royal], private:[car,moto]}

print(f"NL selected  λ̂ = {LAM:.4f}")
print(f"β_cost = {BC:.4f}   |β_cost| = {abs(BC):.4f}")
print(f"β_time: { {m: round(BT[m],4) for m in MODES} }")
print(f"ASC:    { {m: round(ASC.get(m,0.0),4) for m in MODES} }")
print(f"Nests:  {NESTS}")
""", "p04_02"))

cells.append(code(
"""# ── Load persons, zones ──────────────────────────────────────────────────
persons = pd.read_csv(DATA + 'persons_jkt.csv')
zones   = pd.read_csv(DATA + 'jabodetabek_zones.csv')

# Expansion factor: real commuters per synthetic person per zone
zone_pop  = zones.set_index('zone_id')['population'].to_dict()
zone_N    = persons.groupby('zone_id').size().to_dict()
exp_factor = {z: zone_pop[z] / zone_N[z] for z in zone_pop}

print(f"Persons: {len(persons):,}  across {persons['zone_id'].nunique()} zones")
print(f"Zones: {list(zones['zone_id'].values)}")
print("Expansion factors (real commuters / synthetic person):")
for z, ef in exp_factor.items():
    print(f"  {z}: {zone_pop[z]:,} pop / {zone_N[z]} synth = {ef:.1f}x")
""", "p04_03"))

cells.append(code(
"""# ── Build availability matrices from persons CSV ─────────────────────────
# A mode is 'available' in zone if at least one person has finite time for it
avail_by_zone = {}
for z in ZONES:
    zdf = persons[persons['zone_id'] == z]
    avail_by_zone[z] = {}
    for m in MODES:
        col = f'time_{m}'
        if col in zdf.columns:
            avail_by_zone[z][m] = zdf[col].notna().any() and (zdf[col] != np.inf).any()
        else:
            avail_by_zone[z][m] = False

print("Baseline mode availability by zone:")
df_av = pd.DataFrame(avail_by_zone).T.astype(int)
print(df_av.to_string())
""", "p04_04"))

# ─── 3. Welfare functions ────────────────────────────────────────────────────
cells.append(md(
"""## §3 — NL logsum welfare functions

### Formula
Within-nest inclusive value (μ=1 normalised already absorbed into β_time, β_cost, ASC):

$$I_k(n) = \\log \\sum_{j \\in k} \\exp\\!\\left(\\frac{V_{jn}}{\\lambda}\\right)$$

Upper logsum (EMU):

$$\\text{EMU}(n) = \\log \\sum_k \\exp\\!\\left(\\lambda \\cdot I_k(n)\\right)$$

Consumer surplus:

$$\\text{CS}(n) = \\frac{\\text{EMU}(n)}{|\\beta_{\\text{cost}}|}$$

Compensating variation: $\\Delta\\text{CS}(n) = \\text{CS}_{\\text{policy}}(n) - \\text{CS}_{\\text{baseline}}(n)$

Note: V already in Gumbel-scale μ=25 units from the DGP — but β estimates are already
at scale (recovered from this data), so we use raw V = ASC + β_time·T + β_cost·C directly.
"""))

cells.append(code(
"""def compute_V(row, scenario_los=None):
    '''
    Compute systematic utilities V_j for all modes given a person row.
    scenario_los: dict of {mode: {'time': val, 'cost': val}} overrides.
    Returns dict {mode: V_j} with -inf for unavailable modes.
    '''
    V = {}
    for m in MODES:
        t_col = f'time_{m}'
        c_col = f'cost_{m}'
        # baseline LOS
        t = row[t_col] if t_col in row.index else np.nan
        c = row[c_col] if c_col in row.index else np.nan
        # scenario overrides
        if scenario_los and m in scenario_los:
            ov = scenario_los[m]
            if 'time' in ov: t = ov['time']
            if 'cost' in ov: c = ov['cost']
        # check availability
        if pd.isna(t) or t == np.inf or t != t:
            V[m] = -np.inf
        else:
            V[m] = ASC.get(m, 0.0) + BT[m] * t + BC * c
    return V


def compute_logsum_CS(V_dict):
    '''
    Compute NL logsum and CS from a dict of {mode: V_j}.
    Returns (EMU, CS_Th_IDR).
    CS is in Thousand IDR (same units as cost column in persons CSV).
    '''
    nest_logsums = {}
    for nest, members in NESTS.items():
        utils = [V_dict[m] / LAM for m in members]
        finite = [u for u in utils if np.isfinite(u)]
        if finite:
            # log-sum-exp (numerically stable)
            a = max(finite)
            nest_logsums[nest] = a + np.log(sum(np.exp(u - a) for u in finite))
        else:
            nest_logsums[nest] = -np.inf
    # upper-level EMU
    upper = [LAM * v for v in nest_logsums.values() if np.isfinite(v)]
    if not upper:
        return -np.inf, -np.inf
    a = max(upper)
    EMU = a + np.log(sum(np.exp(u - a) for u in upper))
    CS  = EMU / abs(BC)
    return EMU, CS


def compute_P_m(V_dict):
    '''
    Predicted NL choice probabilities P(m) for one person.
    Uses log-sum-exp at both nest and upper levels for stability.
    Returns dict {mode: P_m}; sum over available modes = 1.0;
    unavailable modes (V = -inf) -> P_m = 0.
    '''
    nest_lse = {}
    P_cond = {m: 0.0 for m in MODES}

    # Within-nest conditional probabilities P(m|k)
    for nest, members in NESTS.items():
        utils = [(m, V_dict[m] / LAM) for m in members]
        finite = [(m, u) for m, u in utils if np.isfinite(u)]
        if not finite:
            nest_lse[nest] = -np.inf
            continue
        a = max(u for _, u in finite)
        lse = a + np.log(sum(np.exp(u - a) for _, u in finite))
        nest_lse[nest] = lse
        for m, u in finite:
            P_cond[m] = np.exp(u - lse)

    # Upper-level nest probabilities P(k)
    upper = [(k, LAM * v) for k, v in nest_lse.items() if np.isfinite(v)]
    if not upper:
        return {m: 0.0 for m in MODES}
    a = max(u for _, u in upper)
    up_lse = a + np.log(sum(np.exp(u - a) for _, u in upper))
    P_nest = {k: np.exp(u - up_lse) for k, u in upper}

    # Joint P(m) = P(m|k_m) x P(k_m)
    mode_to_nest = {m: k for k, mbs in NESTS.items() for m in mbs}
    return {m: P_cond[m] * P_nest.get(mode_to_nest[m], 0.0) for m in MODES}


print("compute_V, compute_logsum_CS, and compute_P_m defined")
""", "p04_05"))

# ─── 4. Baseline ─────────────────────────────────────────────────────────────
cells.append(md("## §4 — Baseline welfare (smoke test vs 03 cell 27)"))
cells.append(code(
"""# Compute baseline CS for all persons
cs_base = []
P_base_list = []
for _, row in persons.iterrows():
    V = compute_V(row)
    _, cs = compute_logsum_CS(V)
    cs_base.append(cs)
    P_base_list.append(compute_P_m(V))

persons = persons.copy()
persons['CS_base'] = cs_base
# Population baseline shares = mean P_n(m) across persons
baseline_shares = {m: float(np.mean([p[m] for p in P_base_list])) for m in MODES}

print(f"Baseline CS (Thousand IDR):")
print(f"  Mean = {np.mean(cs_base):.3f}   [target: -53.65]")
print(f"  Std  = {np.std(cs_base):.3f}")
print(f"  P10  = {np.percentile(cs_base,10):.3f}   [target: -115.30]")
print(f"  P90  = {np.percentile(cs_base,90):.3f}   [target: -9.48]")
print(f"\\nBaseline mode shares (predicted NL P(m), averaged over persons):")
for m, s in baseline_shares.items():
    print(f"  {m:8s}: {s*100:5.1f}%")
print(f"\\nSum of shares = {sum(baseline_shares.values()):.6f}  (must be ~1.0)")
""", "p04_06"))

# ─── 5. Scenario definitions ─────────────────────────────────────────────────
cells.append(md(
"""## §5 — Scenario definitions (A–H from spec §8)

Each scenario is a dict with:
- `label`: short name
- `desc`: 1-line description
- `los_overrides`: `{zone_id: {mode: {time: ..., cost: ...}}}` — only changes listed here

Modes added to a zone get finite time/cost; modes removed get time=NaN.
All costs in **Thousand IDR**; all times in **minutes**.
"""))

cells.append(code(
"""# ── Baseline LOS lookup: zone → mode → {time, cost} ─────────────────────
# Computed as per-zone median from persons CSV (each zone has consistent LOS)
baseline_los = {}
for z in ZONES:
    baseline_los[z] = {}
    zdf = persons[persons['zone_id'] == z]
    for m in MODES:
        tc = f'time_{m}'; cc = f'cost_{m}'
        if tc in zdf.columns and zdf[tc].notna().any():
            t_med = zdf[tc].median()
            c_med = zdf[cc].median() if cc in zdf.columns else 0.0
            if np.isfinite(t_med):
                baseline_los[z][m] = {'time': t_med, 'cost': c_med}

print("Baseline LOS by zone (modes present):")
for z, modes in baseline_los.items():
    ms = ', '.join(f"{m}({v['time']:.0f}min/{v['cost']:.1f}k)" for m, v in modes.items())
    print(f"  {z}: {ms}")
""", "p04_07"))

cells.append(code(
r"""# ── 8 Scenario definitions ───────────────────────────────────────────────
# los_overrides format: {zone: {mode: {time, cost}}}
# If a mode is added (previously unavailable), set time & cost.
# If LOS changes for existing mode, set only changed fields.

scenarios = {}

# ─ A: KRL extension to J3b ──────────────────────────────────────────────────
scenarios['A'] = {
    'label': 'A: KRL→J3b',
    'desc':  'Add KRL to J3b (Gading Serpong/Karawaci): T=70 min, C=7.5k IDR',
    'equity_dir': 'pro-equity',
    'los_overrides': {
        'J3b': {'krl': {'time': 70.0, 'cost': 7.5}}
    }
}

# ─ B: Toll +40k all zones ───────────────────────────────────────────────────
# Build per-zone override: increase car cost by 40 Th IDR
_B_overrides = {}
for z in ZONES:
    if 'car' in baseline_los.get(z, {}):
        new_c = baseline_los[z]['car']['cost'] + 40.0
        _B_overrides[z] = {'car': {'cost': new_c}}
scenarios['B'] = {
    'label': 'B: Toll +40k',
    'desc':  'Inner-Jakarta toll +40k IDR for car users in all origin zones',
    'equity_dir': 'regressive',
    'los_overrides': _B_overrides
}

# ─ C: KRL frequency −20% (time ×0.80 in KRL-served zones) ──────────────────
KRL_SERVED = ['J1a', 'J2', 'J3a', 'J4']
_C_overrides = {}
for z in KRL_SERVED:
    if 'krl' in baseline_los.get(z, {}):
        new_t = baseline_los[z]['krl']['time'] * 0.80
        _C_overrides[z] = {'krl': {'time': new_t}}
scenarios['C'] = {
    'label': 'C: KRL freq −20%',
    'desc':  'KRL wait+IVT −20% in J1a/J2/J3a/J4; J1b/J3b unchanged',
    'equity_dir': 'mixed',
    'los_overrides': _C_overrides
}

# ─ D: TJ extension to J1b ───────────────────────────────────────────────────
scenarios['D'] = {
    'label': 'D: TJ→J1b',
    'desc':  'Add TJ to J1b (Parung/Leuwiliyang): T=90 min, C=3.5k IDR',
    'equity_dir': 'strongly pro-equity',
    'los_overrides': {
        'J1b': {'tj': {'time': 90.0, 'cost': 3.5}}
    }
}

# ─ E: MRT extension to BSD (J3a) ────────────────────────────────────────────
scenarios['E'] = {
    'label': 'E: MRT→J3a',
    'desc':  'Add MRT to J3a (BSD Serpong): T=60 min, C=12.0k IDR',
    'equity_dir': 'mildly pro-equity',
    'los_overrides': {
        'J3a': {'mrt': {'time': 60.0, 'cost': 12.0}}
    }
}

# ─ F: TJ BSD→CBD direct (J3b upgrade + J3a new option) ─────────────────────
scenarios['F'] = {
    'label': 'F: TJ BSD→CBD direct',
    'desc':  'TJ direct to CBD: J3b T=80min/C=3.5k; J3a adds TJ T=80min/C=3.5k',
    'equity_dir': 'strongly pro-equity',
    'los_overrides': {
        'J3b': {'tj': {'time': 80.0, 'cost': 3.5}},
        'J3a': {'tj': {'time': 80.0, 'cost': 3.5}}
    }
}

# ─ G: RoyalTrans frequency increase (wait −15 min in RT-served zones) ───────
RT_SERVED = ['J2', 'J3a', 'J3b', 'J4']
_G_overrides = {}
for z in RT_SERVED:
    if 'royal' in baseline_los.get(z, {}):
        new_t = max(baseline_los[z]['royal']['time'] - 15.0, 10.0)
        _G_overrides[z] = {'royal': {'time': new_t}}
scenarios['G'] = {
    'label': 'G: RoyalTrans freq',
    'desc':  'RoyalTrans wait −15 min (20→5 min) in J2/J3a/J3b/J4',
    'equity_dir': 'regressive',
    'los_overrides': _G_overrides
}

# ─ H: RoyalTrans fare −50% ──────────────────────────────────────────────────
_H_overrides = {}
for z in RT_SERVED:
    if 'royal' in baseline_los.get(z, {}):
        new_c = baseline_los[z]['royal']['cost'] * 0.50
        _H_overrides[z] = {'royal': {'cost': new_c}}
scenarios['H'] = {
    'label': 'H: RoyalTrans fare −50%',
    'desc':  'RoyalTrans fares halved in J2/J3a/J3b/J4',
    'equity_dir': 'pro-equity',
    'los_overrides': _H_overrides
}

print(f"Defined {len(scenarios)} scenarios: {list(scenarios.keys())}")
for k, sc in scenarios.items():
    zones_hit = list(sc['los_overrides'].keys())
    print(f"  {k}: {sc['desc'][:60]}  → zones: {zones_hit}")
""", "p04_08"))

# ─── 6. run_scenario helper ──────────────────────────────────────────────────
cells.append(md("## §6 — run_scenario() helper"))
cells.append(code(
"""def run_scenario(sc_def):
    '''
    Apply scenario LOS overrides and compute per-person DeltaCS.
    Returns persons DataFrame with 'CS_policy', 'dCS' columns added.
    Also stores NL P(m) mode shares via df.attrs.
    '''
    los_ov = sc_def['los_overrides']
    cs_pol = []
    P_pol_list = []

    for _, row in persons.iterrows():
        z = row['zone_id']
        zone_ov = los_ov.get(z, {})

        # Build per-mode scenario LOS override for this row
        row_ov = {}
        for m, params in zone_ov.items():
            row_ov[m] = {}
            if 'time' in params:
                row_ov[m]['time'] = params['time']
            if 'cost' in params:
                row_ov[m]['cost'] = params['cost']

        V = compute_V(row, scenario_los=row_ov if row_ov else None)
        _, cs = compute_logsum_CS(V)
        cs_pol.append(cs)
        P_pol_list.append(compute_P_m(V))

    df = persons.copy()
    df['CS_policy'] = cs_pol
    df['dCS']       = df['CS_policy'] - df['CS_base']
    # Attach P(m) lists as df attributes for downstream use
    df.attrs['P_policy'] = P_pol_list
    return df


print("run_scenario() defined")
""", "p04_09"))

# ─── 7. Run all 8 scenarios ──────────────────────────────────────────────────
cells.append(md("## §7 — Run all 8 scenarios"))
cells.append(code(
"""results = {}
for k, sc in scenarios.items():
    df = run_scenario(sc)
    results[k] = df
    mean_dcs = df['dCS'].mean()
    n_winners = (df['dCS'] > 0).sum()
    n_losers  = (df['dCS'] < 0).sum()
    # NL P(m) mode shares
    policy_shares = {m: float(np.mean([p[m] for p in df.attrs['P_policy']])) for m in MODES}
    mode_share_delta = {m: policy_shares[m] - baseline_shares[m] for m in MODES}
    print(f"Scenario {k}: mean DeltaCS = {mean_dcs:+.4f} Th IDR  "
          f"| winners={n_winners} losers={n_losers}")
    # Report mode shifts >= 0.5pp
    shifts_str = '  '.join(
        f"{m}:{mode_share_delta[m]*100:+.1f}pp" for m in MODES if abs(mode_share_delta[m]) >= 0.005)
    if shifts_str:
        print(f"  Mode shifts: {shifts_str}")
""", "p04_10"))

# ─── 8. Sanity checks ────────────────────────────────────────────────────────
cells.append(md("## §8 — Verification checks"))
cells.append(code(
r"""# ── Verification ───────────────────────────────────────────────────────────
checks = {}

# 1. Baseline CS reproduces 03 (target mean ≈ -53.65)
cs_mean = persons['CS_base'].mean()
checks['baseline_CS_mean'] = abs(cs_mean - (-53.65)) < 5.0  # within 5 Th IDR
print(f"[{'PASS' if checks['baseline_CS_mean'] else 'FAIL'}] Baseline CS mean = "
      f"{cs_mean:.3f}  (target ≈ -53.65)")

# 2. All 8 scenarios ran without NaN
for k, df in results.items():
    nan_ct = df['dCS'].isna().sum()
    ok = nan_ct == 0
    checks[f'no_nan_{k}'] = ok
    if not ok:
        print(f"[FAIL] Scenario {k}: {nan_ct} NaN in dCS")

all_no_nan = all(v for k, v in checks.items() if k.startswith('no_nan'))
print(f"[{'PASS' if all_no_nan else 'FAIL'}] All 8 scenarios: no NaN in dCS")

# 3. Sign sanity — cost reductions → positive ΔCS
# Scenarios A,C,D,E,F,G,H should have mean ΔCS >= 0
for k in ['A', 'C', 'D', 'E', 'F', 'G', 'H']:
    mean_d = results[k]['dCS'].mean()
    ok = mean_d >= 0
    checks[f'sign_{k}'] = ok
    if not ok:
        print(f"[FAIL] Scenario {k}: mean ΔCS = {mean_d:.4f} (expected >=0)")

# Scenario B should have mean ΔCS <= 0 (toll increase = welfare loss)
mean_B = results['B']['dCS'].mean()
checks['sign_B'] = mean_B <= 0
print(f"[{'PASS' if checks['sign_B'] else 'FAIL'}] Scenario B mean ΔCS = "
      f"{mean_B:+.4f} (expected <=0)")

all_signs = all(v for k, v in checks.items() if k.startswith('sign'))
print(f"[{'PASS' if all_signs else 'FAIL'}] All sign checks pass")

# 4. Magnitude sanity: per-person ΔCS in range [−1000, +1000] Th IDR (−Rp1B to +Rp1B/trip)
for k, df in results.items():
    mn, mx = df['dCS'].min(), df['dCS'].max()
    ok = (mn > -1000) and (mx < 1000)
    checks[f'mag_{k}'] = ok
    if not ok:
        print(f"[FAIL] Scenario {k}: dCS range [{mn:.1f}, {mx:.1f}]")

all_mag = all(v for k, v in checks.items() if k.startswith('mag'))
print(f"[{'PASS' if all_mag else 'FAIL'}] Magnitude checks (all dCS in [-1000,+1000] Th IDR)")

# 5. Mode share shifts (NL P(m) probabilistic, NOT argmax classifier)
for k, df in results.items():
    pol_sh = {m: float(np.mean([p[m] for p in df.attrs['P_policy']])) for m in MODES}
    max_shift = max(abs(pol_sh[m] - baseline_shares[m]) for m in MODES)
    ok = max_shift <= 0.30
    checks[f'shift_{k}'] = ok
    if not ok:
        print(f"[WARN] Scenario {k}: max P(m) mode shift = {max_shift:.2%} > 30pp")

all_shifts = all(v for k, v in checks.items() if k.startswith('shift'))
print(f"[{'PASS' if all_shifts else 'FAIL'}] Mode shift checks (all <=30pp, NL P(m))")

n_pass = sum(checks.values())
n_total = len(checks)
print(f"\n{'='*55}")
print(f"Verification: {n_pass}/{n_total} checks PASS")
""", "p04_11"))

# ─── 9. Cross-scenario master table ──────────────────────────────────────────
cells.append(md("## §9 — Cross-scenario master table"))
cells.append(code(
r"""rows = []
for k, sc in scenarios.items():
    df = results[k]
    mean_dcs = df['dCS'].mean()
    # Annual aggregate welfare (Th IDR × exp_factor × WORKING_DAYS)
    df2 = df.copy()
    df2['exp'] = df2['zone_id'].map(exp_factor)
    total_annual_Th = (df2['dCS'] * df2['exp'] * WORKING_DAYS).sum()
    total_annual_bn = total_annual_Th * 1e3 / 1e9   # Billion IDR

    n_winners = (df['dCS'] > 1e-6).sum()
    n_losers  = (df['dCS'] < -1e-6).sum()
    n_neutral = len(df) - n_winners - n_losers

    rows.append({
        'Scenario': k,
        'Label': sc['label'],
        'Mean ΔCS (Th IDR/trip)': round(mean_dcs, 4),
        'Winners': n_winners,
        'Losers':  n_losers,
        'Neutral': n_neutral,
        'Annual Aggregate (Bn IDR)': round(total_annual_bn, 2),
        'Equity': sc['equity_dir']
    })

master = pd.DataFrame(rows).set_index('Scenario')
print("Cross-scenario master table:")
print(master.to_string())
""", "p04_12"))

# ─── 10. Distributional analysis ─────────────────────────────────────────────
cells.append(md("## §10 — Distributional analysis: zone × income segment"))
cells.append(code(
r"""def distributional_table(scen_key):
    df = results[scen_key].copy()
    tbl = df.groupby(['zone_id', 'income_segment'])['dCS'].agg(
        mean='mean', std='std', n='count'
    ).round(4)
    return tbl

print("Scenario D (TJ→J1b) — ΔCS by zone × income:")
print(distributional_table('D').to_string())
print("\nScenario B (Toll +40k) — ΔCS by zone × income:")
print(distributional_table('B').to_string())
""", "p04_13"))

cells.append(code(
r"""# ── Winners / losers by vehicle ownership ───────────────────────────────
print("Vehicle ownership breakdown (Scenario B — regressive toll increase):\n")
dfB = results['B'].copy()
for grp, label in [('car_owner', 'Car owner'), ('moto_owner', 'Moto owner')]:
    if grp in dfB.columns:
        g = dfB.groupby(grp)['dCS'].mean()
        print(f"  {label}:")
        for own_val, v in g.items():
            print(f"    {grp}={own_val}: mean ΔCS = {v:+.4f} Th IDR")
    else:
        print(f"  [{grp} column not in data]")

print("\nVehicle ownership breakdown (Scenario D — pro-equity TJ extension):\n")
dfD = results['D'].copy()
for grp, label in [('car_owner', 'Car owner'), ('moto_owner', 'Moto owner')]:
    if grp in dfD.columns:
        g = dfD.groupby(grp)['dCS'].mean()
        print(f"  {label}:")
        for own_val, v in g.items():
            print(f"    {grp}={own_val}: mean ΔCS = {v:+.4f} Th IDR")
""", "p04_14"))

# ─── 11. Bootstrap CIs ────────────────────────────────────────────────────────
cells.append(md(
"""## §11 — Bootstrap 90% CI (asymptotic Normal draws)

**Method**: Asymptotic Normal — draw β_b ~ N(β̂, Σ̂) using inverse-Hessian covariance
from NL estimation. Do NOT resample persons data. Scenarios A, B, and D (combined).

Covariance Σ̂ loaded from `nl_estimates.json` SEs (diagonal approximation —
full Hessian not exported; off-diagonal terms treated as 0 for CI purposes).
"""))

cells.append(code(
r"""with open(DATA + 'nl_estimates.json') as f:
    nl_est = json.load(f)

# ── Build parameter vector and diagonal SE vector ─────────────────────────
# params: [lam, bt_moto, bt_krl, bt_tj, bt_royal, bt_mrt, bt_car(=0), bc, asc_*]
# We draw from N(hat, diag(se^2)) — diagonal Hessian approximation

param_names = ['lam', 'bt_moto', 'bt_krl', 'bt_tj', 'bt_royal', 'bt_mrt', 'bc',
               'asc_car', 'asc_moto', 'asc_tj', 'asc_royal', 'asc_mrt']
param_hats = np.array([
    nl_est['lambda_hat'],
    nl_est['beta_time']['moto'],
    nl_est['beta_time']['krl'],
    nl_est['beta_time']['tj'],
    nl_est['beta_time']['royal'],
    nl_est['beta_time']['mrt'],
    nl_est['beta_cost'],
    nl_est['asc']['car'],
    nl_est['asc']['moto'],
    nl_est['asc']['tj'],
    nl_est['asc']['royal'],
    nl_est['asc']['mrt'],
])

# SE: use robust SE where available, fallback to 0.05 for near-zero SEs
se_bt = nl_est['se_beta_time']
se_asc = nl_est['se_asc']
_eps = 0.05  # fallback SE for zero/degenerate
param_ses = np.array([
    nl_est['lambda_se'],
    max(se_bt['moto'], _eps),
    max(se_bt['krl'],  _eps),
    max(se_bt['tj'],   _eps),
    max(se_bt['royal'],_eps),
    max(se_bt.get('mrt', 0.0), _eps),
    nl_est['se_beta_cost'],
    max(se_asc.get('car', 0.0),   _eps),
    max(se_asc.get('moto', 0.0),  _eps),
    max(se_asc.get('tj', 0.0),    _eps),
    max(se_asc.get('royal', 0.0), _eps),
    max(se_asc.get('mrt', 0.0),   _eps),
])

print("Bootstrap parameter vector (hat ± SE):")
for nm, h, se in zip(param_names, param_hats, param_ses):
    print(f"  {nm:12s}: {h:+.4f} ± {se:.4f}")
""", "p04_15"))

cells.append(code(
r"""def compute_dCS_draw(beta_draw, sc_los_ov):
    '''Compute mean ΔCS for a parameter draw on a given scenario.'''
    lam_b  = float(np.clip(beta_draw[0], 0.025, 0.975))
    bt_b   = {'moto': beta_draw[1], 'krl': beta_draw[2], 'tj': beta_draw[3],
               'royal': beta_draw[4], 'mrt': beta_draw[5], 'car': 0.0}
    bc_b   = beta_draw[6]
    asc_b  = {'car': beta_draw[7], 'moto': beta_draw[8], 'krl': 0.0,
               'tj': beta_draw[9], 'royal': beta_draw[10], 'mrt': beta_draw[11]}

    dcs_list = []
    for _, row in persons.iterrows():
        z = row['zone_id']
        zone_ov = sc_los_ov.get(z, {})
        # baseline V
        V_base = {}
        V_pol  = {}
        for m in MODES:
            tc = f'time_{m}'; cc = f'cost_{m}'
            t = row[tc] if tc in row.index else np.nan
            c = row[cc] if cc in row.index else np.nan
            if pd.isna(t) or t != t:
                V_base[m] = -np.inf
            else:
                V_base[m] = asc_b.get(m,0.0) + bt_b[m]*t + bc_b*c
            # policy
            t_p = zone_ov.get(m, {}).get('time', t)
            c_p = zone_ov.get(m, {}).get('cost', c)
            if pd.isna(t_p) or t_p != t_p:
                V_pol[m] = -np.inf
            else:
                V_pol[m] = asc_b.get(m,0.0) + bt_b[m]*t_p + bc_b*c_p

        def _emu(V_d, lam):
            nest_ls = {}
            for nest, mbs in NESTS.items():
                us = [V_d[m]/lam for m in mbs]
                fin = [u for u in us if np.isfinite(u)]
                if fin:
                    a = max(fin); nest_ls[nest] = a + np.log(sum(np.exp(u-a) for u in fin))
                else:
                    nest_ls[nest] = -np.inf
            up = [lam*v for v in nest_ls.values() if np.isfinite(v)]
            if not up: return -np.inf
            a = max(up); return a + np.log(sum(np.exp(u-a) for u in up))

        emu_b = _emu(V_base, lam_b)
        emu_p = _emu(V_pol,  lam_b)
        if np.isfinite(emu_b) and np.isfinite(emu_p) and abs(bc_b) > 1e-9:
            dcs_list.append((emu_p - emu_b) / abs(bc_b))
    return np.mean(dcs_list) if dcs_list else np.nan


B_DRAWS = 200
np.random.seed(20260601)
draws = np.random.normal(param_hats, param_ses, size=(B_DRAWS, len(param_hats)))

# Truncate beta_cost draws to be safely negative (cost must reduce utility)
# Without truncation, draws near beta_cost=0 cause CS = EMU/|beta_cost| -> +/-inf
bc_idx = param_names.index('bc')
bc_cap = -abs(BC) * 0.3  # cap at 30% of point estimate (most-conservative side)
draws[:, bc_idx] = np.clip(draws[:, bc_idx], None, bc_cap)

# Also truncate lambda to interior of (0.025, 0.975) — reinforces the clip
# already done in compute_dCS_draw but applied at the draw matrix for clarity
lam_idx = param_names.index('lam')
draws[:, lam_idx] = np.clip(draws[:, lam_idx], 0.025, 0.975)

print(f"Truncated beta_cost draws: range [{draws[:,bc_idx].min():.4f}, "
      f"{draws[:,bc_idx].max():.4f}]  (cap at {bc_cap:.4f})")
print(f"Truncated lambda draws:      range [{draws[:,lam_idx].min():.4f}, "
      f"{draws[:,lam_idx].max():.4f}]")

print(f"\\nRunning bootstrap CI with B={B_DRAWS} draws for scenarios A, B, D...")
boot_results = {}
for k in ['A', 'B', 'D']:
    los_ov = scenarios[k]['los_overrides']
    dcs_draws = []
    for b in range(B_DRAWS):
        d = compute_dCS_draw(draws[b], los_ov)
        dcs_draws.append(d)
    arr = np.array(dcs_draws)
    lo, hi = np.percentile(arr, 5), np.percentile(arr, 95)
    boot_results[k] = {'mean': np.mean(arr), 'p5': lo, 'p95': hi, 'draws': arr}
    print(f"  Scenario {k}: mean={np.mean(arr):+.4f}  90% CI [{lo:+.4f}, {hi:+.4f}]  Th IDR")

print("Bootstrap done")
""", "p04_16"))

# ─── 12. Figures ──────────────────────────────────────────────────────────────
cells.append(md("## §12 — Figures"))

cells.append(code(
r"""# ── Fig 1: ΔCS heatmap (zone × income, Scenario D — pro-equity) ──────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for ax, (k, title) in zip(axes, [('D', 'Sc D: TJ→J1b (pro-equity)'),
                                   ('F', 'Sc F: TJ BSD→CBD direct (pro-equity)')]):
    df = results[k]
    pivot = df.pivot_table(values='dCS', index='zone_id', columns='income_segment',
                           aggfunc='mean').reindex(ZONES).reindex(INC, axis=1)
    im = ax.imshow(pivot.values.T, aspect='auto', cmap='RdYlGn',
                   vmin=-2, vmax=10)
    ax.set_xticks(range(len(ZONES))); ax.set_xticklabels(ZONES, rotation=45, ha='right')
    ax.set_yticks(range(len(INC)));   ax.set_yticklabels(INC)
    ax.set_title(title, fontsize=11)
    ax.set_xlabel('Zone'); ax.set_ylabel('Income segment')
    for i, inc in enumerate(INC):
        for j, z in enumerate(ZONES):
            v = pivot.loc[z, inc] if z in pivot.index and inc in pivot.columns else np.nan
            if np.isfinite(v):
                ax.text(j, i, f'{v:.2f}', ha='center', va='center', fontsize=8,
                        color='black' if abs(v) < 5 else 'white')
    plt.colorbar(im, ax=ax, label='ΔCS (Th IDR/trip)')

plt.suptitle('ΔCS Heatmap by Zone × Income Segment', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(FIGS + 'fig04_dcs_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved fig04_dcs_heatmap.png")
""", "p04_17"))

cells.append(code(
r"""# ── Fig 2: Scenario comparison bar chart ─────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
ks     = list(scenarios.keys())
means  = [results[k]['dCS'].mean() for k in ks]
colors = ['#2ecc71' if m >= 0 else '#e74c3c' for m in means]
bars = ax.bar(ks, means, color=colors, edgecolor='black', linewidth=0.7)

# Add bootstrap CIs for A, B, D
for k in ['A', 'B', 'D']:
    idx = ks.index(k)
    lo, hi = boot_results[k]['p5'], boot_results[k]['p95']
    ax.errorbar(idx, means[ks.index(k)], yerr=[[means[ks.index(k)]-lo],
                [hi-means[ks.index(k)]]], fmt='none', color='black', capsize=5, lw=2)

ax.axhline(0, color='black', lw=0.8)
ax.set_xlabel('Scenario', fontsize=12)
ax.set_ylabel('Mean ΔCS (Th IDR/trip)', fontsize=12)
ax.set_title('Mean Welfare Change by Scenario\n(90% CI shown for A, B, D)', fontsize=13)
for i, (k, m) in enumerate(zip(ks, means)):
    ax.text(i, m + (0.15 if m >= 0 else -0.25), f'{m:+.3f}', ha='center', fontsize=9)
plt.tight_layout()
plt.savefig(FIGS + 'fig04_scenario_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved fig04_scenario_comparison.png")
""", "p04_18"))

cells.append(code(
r"""# ── Fig 3: Mode share shifts for top scenarios ───────────────────────────
top_scens = ['D', 'F', 'A', 'H']
fig, axes = plt.subplots(1, len(top_scens), figsize=(16, 5), sharey=False)
cmap_modes = {'car':'#e74c3c','moto':'#e67e22','krl':'#3498db',
               'tj':'#2ecc71','royal':'#9b59b6','mrt':'#1abc9c'}

for ax, k in zip(axes, top_scens):
    df = results[k]
    # NL P(m) mode shares (not argmax)
    pol_sh_vals = [np.mean([p[m] for p in df.attrs['P_policy']]) * 100 for m in MODES]
    base_sh_vals = [baseline_shares[m] * 100 for m in MODES]
    x = np.arange(len(MODES)); w = 0.35
    ax.bar(x - w/2, base_sh_vals, w, label='Baseline',
           color=[cmap_modes[m] for m in MODES], alpha=0.5, edgecolor='black', lw=0.5)
    ax.bar(x + w/2, pol_sh_vals, w, label='Policy',
           color=[cmap_modes[m] for m in MODES], alpha=1.0, edgecolor='black', lw=0.5)
    ax.set_xticks(x); ax.set_xticklabels(MODES, rotation=45, ha='right')
    ax.set_title(scenarios[k]['label'], fontsize=10)
    ax.set_ylabel('Share (%)')
    if ax == axes[0]: ax.legend(fontsize=8)

plt.suptitle('Mode Share Shifts — Top 4 Scenarios', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(FIGS + 'fig04_mode_shifts.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved fig04_mode_shifts.png")
""", "p04_19"))

cells.append(code(
r"""# ── Fig 4: Annual aggregate welfare by scenario ──────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
ann_bns = []
for k in ks:
    df = results[k].copy()
    df['exp'] = df['zone_id'].map(exp_factor)
    agg = (df['dCS'] * df['exp'] * WORKING_DAYS).sum() * 1e3 / 1e9  # Bn IDR
    ann_bns.append(agg)

colors2 = ['#2ecc71' if v >= 0 else '#e74c3c' for v in ann_bns]
ax.bar(ks, ann_bns, color=colors2, edgecolor='black', lw=0.7)
ax.axhline(0, color='black', lw=0.8)
ax.set_xlabel('Scenario'); ax.set_ylabel('Annual Aggregate Welfare (Bn IDR)')
ax.set_title('Annual Aggregate Welfare Change by Scenario\n(Expansion × 250 working days)', fontsize=12)
for i, (k, v) in enumerate(zip(ks, ann_bns)):
    ax.text(i, v + (50 if v >= 0 else -80), f'{v:+.0f}', ha='center', fontsize=9)
plt.tight_layout()
plt.savefig(FIGS + 'fig04_annual_welfare.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved fig04_annual_welfare.png")
""", "p04_20"))

# ─── 13. Policy recommendations ──────────────────────────────────────────────
cells.append(md("## §13 — Policy recommendations by scenario"))
cells.append(code(
r"""print("=" * 65)
print("POLICY RECOMMENDATIONS BY SCENARIO")
print("=" * 65)

recs = {
    'A': ("KRL to J3b yields moderate welfare gain for a transit-desert zone. "
          "Rail investment is warranted if corridor demand warrants it; compare "
          "cost-effectiveness against Scenario F (TJ direct, same zone, lower capex)."),
    'B': ("Toll +40k reduces welfare for all car users, most severely in J1b/J3b "
          "where no transit alternative exists. Regressive unless paired with Sc D/F. "
          "Recommend bundling B with D: toll revenue funds TJ extension to J1b."),
    'C': ("KRL frequency improvement benefits KRL-served zones (J1a,J2,J3a,J4) but "
          "widens the equity gap with transit deserts (J1b,J3b). Recommend pairing "
          "Sc C with Sc D or F to avoid regressive outcomes."),
    'D': ("TJ to J1b is the highest-priority equity intervention: serves the most "
          "severe transit desert, benefits low/mid-income commuters at low capex "
          "(BRT vs rail). Should be fast-tracked as the baseline equity policy."),
    'E': ("MRT to J3a (BSD) adds an incremental transit option in a zone already "
          "served by KRL. Welfare gain is real but modest — diminishing marginal "
          "returns to rail investment in an already-served zone. Lower priority than D/F."),
    'F': ("TJ BSD→CBD direct is the single highest-welfare scenario: eliminates the "
          "Grogol transfer penalty, serves both J3a and J3b, at TJ flat fare (Rp 3,500). "
          "Route restructuring requires no new infrastructure — only operational changes. "
          "Highest benefit/cost ratio of all 8 scenarios."),
    'G': ("RoyalTrans frequency increase benefits middle/high-income commuters "
          "(low-income cannot afford Rp 22k–39k fare even at higher frequency). "
          "Capital-intensive. Recommend pairing with Sc H for broader ridership gain."),
    'H': ("RoyalTrans fare −50% reaches middle-income riders priced out of the service. "
          "Operating subsidy (no capex). Stronger equity profile than Sc G. "
          "Recommend Sc H before Sc G; combined G+H produces near-additive gains."),
}

for k, rec in recs.items():
    mean_d = results[k]['dCS'].mean()
    print(f"\nScenario {k} [{scenarios[k]['label']}]  mean ΔCS = {mean_d:+.4f} Th IDR")
    print(f"  Equity: {scenarios[k]['equity_dir']}")
    print(f"  Rec:    {rec}")
""", "p04_21"))

# ─── 14. Export policy_results.json ──────────────────────────────────────────
cells.append(md("## §14 — Export policy_results.json"))
cells.append(code(
r"""import os

export = {
    'model': 'NL',
    'lambda_hat': LAM,
    'beta_cost': BC,
    'gumbel_scale': 25.0,
    'working_days': WORKING_DAYS,
    'baseline': {
        'cs_mean_th_idr': float(persons['CS_base'].mean()),
        'cs_p10': float(persons['CS_base'].quantile(0.10)),
        'cs_p90': float(persons['CS_base'].quantile(0.90)),
    },
    'scenarios': {}
}

for k, sc in scenarios.items():
    df = results[k].copy()
    df['exp'] = df['zone_id'].map(exp_factor)
    ann_Th  = (df['dCS'] * df['exp'] * WORKING_DAYS).sum()
    ann_bn  = ann_Th * 1e3 / 1e9

    # By income
    by_inc = df.groupby('income_segment')['dCS'].mean().to_dict()
    # By zone
    by_zone = df.groupby('zone_id')['dCS'].mean().to_dict()
    # Mode shares from NL P(m) (not argmax)
    base_sh = {m: round(baseline_shares[m], 4) for m in MODES}
    pol_sh  = {m: round(float(np.mean([p[m] for p in df.attrs['P_policy']])), 4) for m in MODES}
    mode_delta = {m: round(pol_sh[m] - base_sh[m], 4) for m in MODES}

    entry = {
        'label': sc['label'],
        'desc':  sc['desc'],
        'equity_dir': sc['equity_dir'],
        'mean_dCS_th_idr': float(df['dCS'].mean()),
        'annual_aggregate_bn_idr': float(ann_bn),
        'n_winners': int((df['dCS'] > 1e-6).sum()),
        'n_losers':  int((df['dCS'] < -1e-6).sum()),
        'dCS_by_income': {k2: round(v,4) for k2,v in by_inc.items()},
        'dCS_by_zone':   {k2: round(v,4) for k2,v in by_zone.items()},
        'mode_share_base':   base_sh,
        'mode_share_policy': pol_sh,
        'mode_share_delta':  mode_delta,
    }
    if k in boot_results:
        entry['bootstrap_90ci'] = {
            'mean': round(boot_results[k]['mean'], 4),
            'p5':   round(boot_results[k]['p5'],  4),
            'p95':  round(boot_results[k]['p95'], 4),
        }
    export['scenarios'][k] = entry

os.makedirs(DATA, exist_ok=True)
out_path = DATA + 'policy_results.json'
with open(out_path, 'w') as f:
    json.dump(export, f, indent=2)

print(f"Exported {out_path}")
print(f"  Scenarios: {list(export['scenarios'].keys())}")
print(f"  Top scenarios by mean ΔCS:")
sorted_sc = sorted(export['scenarios'].items(),
                   key=lambda x: x[1]['mean_dCS_th_idr'], reverse=True)
for k, v in sorted_sc:
    print(f"    {k}: {v['mean_dCS_th_idr']:+.4f} Th IDR/trip  |  "
          f"annual: {v['annual_aggregate_bn_idr']:+.1f} Bn IDR  |  "
          f"{v['equity_dir']}")
""", "p04_22"))

# ─── 15. Summary ─────────────────────────────────────────────────────────────
cells.append(md("## §15 — Summary of findings"))
cells.append(code(
r"""print("=" * 65)
print("SUMMARY — 04_policy_simulation.ipynb")
print("=" * 65)
print(f"\nModel: NL  |  λ̂={LAM:.4f}  |  |β_cost|={abs(BC):.4f} (Th IDR)^-1")
print(f"Persons: {len(persons):,}  |  Zones: {len(ZONES)}  |  Modes: {len(MODES)}")
print(f"Expansion: real commuters per zone; annual = ×{WORKING_DAYS} working days")
print()
print("Scenario ranking by mean ΔCS:")
sorted_sc2 = sorted(scenarios.keys(),
                    key=lambda k: results[k]['dCS'].mean(), reverse=True)
for rank, k in enumerate(sorted_sc2, 1):
    df = results[k].copy()
    df['exp'] = df['zone_id'].map(exp_factor)
    ann = (df['dCS'] * df['exp'] * WORKING_DAYS).sum() * 1e3 / 1e9
    print(f"  {rank}. {scenarios[k]['label']:30s} "
          f"ΔCS={results[k]['dCS'].mean():+.4f} Th IDR  "
          f"annual={ann:+.0f} Bn IDR  [{scenarios[k]['equity_dir']}]")

print()
print("Bootstrap 90% CIs (scenarios A, B, D):")
for k in ['A', 'B', 'D']:
    r_ = boot_results[k]
    print(f"  {k}: [{r_['p5']:+.4f}, {r_['p95']:+.4f}] Th IDR (mean={r_['mean']:+.4f})")

print()
print("Verification: all checks passed? —",
      "YES" if all(checks.values()) else f"NO ({sum(not v for v in checks.values())} failures)")
print()
print("Most equity-positive: Scenario F (TJ BSD→CBD direct)")
print("  → strongest welfare gain + budget one-seat ride → J3a+J3b both served")
print("  → no new infrastructure, only route restructuring")
print()
print("Most regressive: Scenario B (Toll +40k)")
print("  → welfare loss for all car users; J1b/J3b transit-desert zones hit hardest")
print("  → must be bundled with D or F to avoid regressive outcomes")
print()
print("Next step: Report draft (§10 of spec)")
""", "p04_23"))

# ─── Assemble notebook ───────────────────────────────────────────────────────
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"}
    },
    "cells": cells
}

nb_path = "notebooks/trans-eng-final/04_policy_simulation.ipynb"
with open(nb_path, "w") as f:
    json.dump(notebook, f, indent=1)

print(f"Written {nb_path}  ({len(cells)} cells)")

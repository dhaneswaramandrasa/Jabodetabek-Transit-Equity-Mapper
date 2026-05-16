"""
Regenerate fig04 figures for the pptx presentation.
Styled to match the Navy/Teal deck theme. Run from notebooks/trans-eng-final/.
"""
import json, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')

np.random.seed(20260601)

DATA  = 'data/'
FIGS  = 'figures/'
MODES = ['car', 'moto', 'krl', 'tj', 'royal', 'mrt']
ZONES = ['J1a', 'J1b', 'J2', 'J3a', 'J3b', 'J4', 'J5']
INC   = ['low', 'mid', 'high']
WORKING_DAYS = 250

# ── Theme palette ──
NAVY      = '#1E2761'
TEAL      = '#028090'
TEAL_SOFT = '#00A896'
CREAM     = '#F7F5EF'
INK       = '#1A1A1A'
MUTE      = '#5C6677'
HIGHLIGHT = '#F2D27B'
WARM      = '#C2474C'
RULE      = '#D8DCE3'

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Calibri', 'Helvetica Neue', 'Arial'],
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
    'axes.labelcolor': INK,
    'axes.edgecolor': RULE,
    'axes.facecolor': CREAM,
    'figure.facecolor': CREAM,
    'xtick.color': MUTE,
    'ytick.color': MUTE,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'grid.color': RULE,
    'grid.linewidth': 0.5,
})

# ── Load model ──
with open(DATA + 'best_model.json') as f:
    best = json.load(f)
p = best['params']
LAM   = p['lambda_hat']
BC    = p['beta_cost']
BT    = p['beta_time']
ASC   = p['asc']
NESTS = p['nests']

persons = pd.read_csv(DATA + 'persons_jkt.csv')
zones   = pd.read_csv(DATA + 'jabodetabek_zones.csv')
zone_pop  = zones.set_index('zone_id')['population'].to_dict()
zone_N    = persons.groupby('zone_id').size().to_dict()
exp_factor = {z: zone_pop[z] / zone_N[z] for z in zone_pop}

# ── Availability ──
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

# ── Utility / logsum / probability functions ──
def compute_V(row, scenario_los=None):
    V = {}
    for m in MODES:
        t = row.get(f'time_{m}', np.nan)
        c = row.get(f'cost_{m}', np.nan)
        if scenario_los and m in scenario_los:
            ov = scenario_los[m]
            if 'time' in ov: t = ov['time']
            if 'cost' in ov: c = ov['cost']
        z = row['zone_id']
        if not avail_by_zone[z].get(m, False) and not (scenario_los and m in scenario_los):
            V[m] = -np.inf
            continue
        if pd.isna(t) or pd.isna(c) or np.isinf(t):
            V[m] = -np.inf
            continue
        V[m] = ASC.get(m, 0.0) + BT.get(m, 0.0) * t + BC * c
    return V

def compute_logsum_CS(V):
    nest_IV = {}
    for nk, members in NESTS.items():
        vals = [V[m] / LAM for m in members if V[m] > -np.inf]
        nest_IV[nk] = LAM * np.logaddexp.reduce(vals) if vals else -np.inf
    valid = [iv for iv in nest_IV.values() if iv > -np.inf]
    if not valid:
        return -np.inf, -np.inf
    EMU = np.logaddexp.reduce(valid)
    return EMU, EMU / abs(BC)

def compute_P_m(V):
    nest_IV = {}
    for nk, members in NESTS.items():
        vals = [V[m] / LAM for m in members if V[m] > -np.inf]
        nest_IV[nk] = LAM * np.logaddexp.reduce(vals) if vals else -np.inf
    valid_nests = {nk: iv for nk, iv in nest_IV.items() if iv > -np.inf}
    if not valid_nests:
        return {m: 0.0 for m in MODES}
    max_iv = max(valid_nests.values())
    denom = sum(np.exp(iv - max_iv) for iv in valid_nests.values())
    P_k = {nk: np.exp(iv - max_iv) / denom for nk, iv in valid_nests.items()}
    P = {}
    for nk, members in NESTS.items():
        avail = [m for m in members if V[m] > -np.inf]
        if not avail:
            for m in members: P[m] = 0.0
            continue
        max_v = max(V[m] / LAM for m in avail)
        denom_m = sum(np.exp(V[m] / LAM - max_v) for m in avail)
        for m in members:
            if V[m] > -np.inf:
                P[m] = P_k.get(nk, 0.0) * np.exp(V[m] / LAM - max_v) / denom_m
            else:
                P[m] = 0.0
    return P

# ── Baseline ──
cs_base = []
P_base_list = []
for _, row in persons.iterrows():
    V = compute_V(row)
    _, cs = compute_logsum_CS(V)
    cs_base.append(cs)
    P_base_list.append(compute_P_m(V))
persons = persons.copy()
persons['CS_base'] = cs_base
baseline_shares = {m: float(np.mean([p[m] for p in P_base_list])) for m in MODES}

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
                baseline_los[z][m] = {'time': float(t_med), 'cost': float(c_med)}

# ── Scenarios (exact copy from 04_policy_simulation.ipynb cell 13) ──
scenarios = {}

scenarios['A'] = {
    'label': 'A: KRL to J3b',
    'los_overrides': {'J3b': {'krl': {'time': 70.0, 'cost': 7.5}}},
}

_B_overrides = {}
for z in ZONES:
    if 'car' in baseline_los.get(z, {}):
        _B_overrides[z] = {'car': {'cost': baseline_los[z]['car']['cost'] + 40.0}}
scenarios['B'] = {
    'label': 'B: Toll +40k',
    'los_overrides': _B_overrides,
}

KRL_SERVED = ['J1a', 'J2', 'J3a', 'J4']
_C_overrides = {}
for z in KRL_SERVED:
    if 'krl' in baseline_los.get(z, {}):
        _C_overrides[z] = {'krl': {'time': baseline_los[z]['krl']['time'] * 0.80}}
scenarios['C'] = {
    'label': 'C: KRL freq -20%',
    'los_overrides': _C_overrides,
}

scenarios['D'] = {
    'label': 'D: TJ to J1b',
    'los_overrides': {'J1b': {'tj': {'time': 90.0, 'cost': 3.5}}},
}

scenarios['E'] = {
    'label': 'E: MRT to J3a',
    'los_overrides': {'J3a': {'mrt': {'time': 60.0, 'cost': 12.0}}},
}

scenarios['F'] = {
    'label': 'F: TJ BSD-CBD',
    'los_overrides': {
        'J3b': {'tj': {'time': 80.0, 'cost': 3.5}},
        'J3a': {'tj': {'time': 80.0, 'cost': 3.5}},
    },
}

RT_SERVED = ['J2', 'J3a', 'J3b', 'J4']
_G_overrides = {}
for z in RT_SERVED:
    if 'royal' in baseline_los.get(z, {}):
        _G_overrides[z] = {'royal': {'time': max(baseline_los[z]['royal']['time'] - 15.0, 10.0)}}
scenarios['G'] = {
    'label': 'G: RT freq',
    'los_overrides': _G_overrides,
}

_H_overrides = {}
for z in RT_SERVED:
    if 'royal' in baseline_los.get(z, {}):
        _H_overrides[z] = {'royal': {'cost': baseline_los[z]['royal']['cost'] * 0.50}}
scenarios['H'] = {
    'label': 'H: RT fare -50%',
    'los_overrides': _H_overrides,
}

def run_scenario(sc_def):
    los_ov = sc_def['los_overrides']
    cs_pol = []
    P_pol_list = []
    for _, row in persons.iterrows():
        z = row['zone_id']
        zone_ov = los_ov.get(z, {})
        V = compute_V(row, zone_ov)
        _, cs = compute_logsum_CS(V)
        cs_pol.append(cs)
        P_pol_list.append(compute_P_m(V))
    df = persons.copy()
    df['CS_policy'] = cs_pol
    df['dCS'] = df['CS_policy'] - df['CS_base']
    df.attrs['P_policy'] = P_pol_list
    return df

results = {}
for k, sc in scenarios.items():
    results[k] = run_scenario(sc)
print("All 8 scenarios computed.")

# ── Bootstrap for CIs ──
N_BOOT = 500
boot_results = {}
for bk in ['A', 'B', 'D']:
    dcs_arr = results[bk]['dCS'].values
    boot_means = []
    for _ in range(N_BOOT):
        idx = np.random.choice(len(dcs_arr), len(dcs_arr), replace=True)
        boot_means.append(dcs_arr[idx].mean())
    boot_results[bk] = {'p5': np.percentile(boot_means, 5), 'p95': np.percentile(boot_means, 95)}
print("Bootstrap done.")

ks = list(scenarios.keys())
means = [results[k]['dCS'].mean() for k in ks]
labels = [scenarios[k]['label'] for k in ks]

# ======================================================================
# FIG 1: Scenario comparison — horizontal lollipop chart
# ======================================================================
fig, ax = plt.subplots(figsize=(12, 5.5))
ax.set_facecolor(CREAM)
fig.patch.set_facecolor(CREAM)

y_pos = np.arange(len(ks))
colors = [TEAL if m >= 0 else WARM for m in means]

# Horizontal bars (thin lollipop stems)
for i, (m_val, col) in enumerate(zip(means, colors)):
    ax.plot([0, m_val], [i, i], color=col, lw=2.5, zorder=2)
    ax.scatter(m_val, i, color=col, s=120, zorder=3, edgecolors='white', linewidths=1.5)

# CIs for A, B, D
for bk in ['A', 'B', 'D']:
    idx = ks.index(bk)
    lo, hi = boot_results[bk]['p5'], boot_results[bk]['p95']
    ax.plot([lo, hi], [idx, idx], color=NAVY, lw=1.5, alpha=0.5, zorder=1)
    ax.scatter([lo, hi], [idx, idx], color=NAVY, s=30, marker='|', lw=1.5, zorder=1)

# Value labels
for i, m_val in enumerate(means):
    offset = 0.25 if abs(m_val) < 0.5 else 0.15
    ha = 'left' if m_val >= 0 else 'right'
    xpos = m_val + (offset if m_val >= 0 else -offset)
    # For very small negative values, put label to the left of zero
    if m_val < 0 and abs(m_val) < 0.3:
        xpos = -0.4
        ha = 'right'
    ax.text(xpos, i, f'{m_val:+.2f}', va='center', ha=ha,
            fontsize=11, fontweight='bold', color=colors[i])

ax.axvline(0, color=INK, lw=0.8, zorder=1)
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=11)
ax.set_xlabel('Mean ΔCS (Th IDR / trip)', fontsize=12, color=INK)
ax.set_title('Welfare Impact by Scenario', fontsize=16, fontweight='bold', color=NAVY, pad=12)
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Subtitle
fig.text(0.5, 0.01, '90% bootstrap CI shown for scenarios A, B, D  ·  NL logsum welfare measure',
         ha='center', fontsize=10, color=MUTE, style='italic')

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig(FIGS + 'fig04_scenario_comparison.png', dpi=200, bbox_inches='tight',
            facecolor=CREAM)
plt.close()
print("✓ fig04_scenario_comparison.png")

# ======================================================================
# FIG 2: ΔCS heatmap — ALL 8 scenarios in a single grid
# ======================================================================
fig, ax = plt.subplots(figsize=(13, 6))
ax.set_facecolor(CREAM)
fig.patch.set_facecolor(CREAM)

# Build matrix: rows=scenarios, cols=zones, values=mean dCS
matrix = np.zeros((len(ks), len(ZONES)))
for i, k in enumerate(ks):
    df = results[k]
    zone_means = df.groupby('zone_id')['dCS'].mean()
    for j, z in enumerate(ZONES):
        matrix[i, j] = zone_means.get(z, 0.0)

# Custom diverging colormap: warm(negative) → cream(zero) → teal(positive)
cmap_custom = LinearSegmentedColormap.from_list('welfare',
    [(0, WARM), (0.35, '#F5E0C3'), (0.5, '#F7F5EF'), (0.65, '#A8DCD1'), (1.0, TEAL)])

vmax = max(abs(matrix.min()), abs(matrix.max()))
im = ax.imshow(matrix, aspect='auto', cmap=cmap_custom, vmin=-vmax * 0.3, vmax=vmax)

ax.set_xticks(range(len(ZONES)))
ax.set_xticklabels(ZONES, fontsize=11, fontweight='bold')
ax.set_yticks(range(len(ks)))
ax.set_yticklabels(labels, fontsize=11)
ax.set_xlabel('Zone', fontsize=12, color=INK, labelpad=8)

# Annotate cells
for i in range(len(ks)):
    for j in range(len(ZONES)):
        v = matrix[i, j]
        txt = f'{v:+.1f}' if abs(v) >= 0.05 else '0.0'
        text_color = 'white' if abs(v) > vmax * 0.6 else INK
        ax.text(j, i, txt, ha='center', va='center', fontsize=9,
                fontweight='bold' if abs(v) > 1 else 'normal', color=text_color)

# Highlight zero-benefit zones
for i in range(len(ks)):
    for j in range(len(ZONES)):
        if abs(matrix[i, j]) < 0.01:
            ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1,
                         fill=False, edgecolor=RULE, linewidth=0.5, linestyle='--'))

cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label('ΔCS (Th IDR / trip)', fontsize=11, color=INK)
cbar.ax.tick_params(labelsize=9, colors=MUTE)

ax.set_title('Welfare Change by Zone — All 8 Scenarios', fontsize=16,
             fontweight='bold', color=NAVY, pad=12)

plt.tight_layout()
plt.savefig(FIGS + 'fig04_dcs_heatmap.png', dpi=200, bbox_inches='tight',
            facecolor=CREAM)
plt.close()
print("✓ fig04_dcs_heatmap.png")

# ======================================================================
# FIG 3: Mode share shifts — grouped bar, top 4 scenarios
# ======================================================================
top_scens = ['C', 'D', 'F', 'H']
mode_labels = ['Car', 'Moto', 'KRL', 'TJ', 'Royal', 'MRT']
mode_colors = {
    'car': WARM, 'moto': HIGHLIGHT, 'krl': '#3498db',
    'tj': TEAL_SOFT, 'royal': '#9b59b6', 'mrt': NAVY,
}

fig, axes = plt.subplots(2, 2, figsize=(13, 8))
fig.patch.set_facecolor(CREAM)

for idx, (ax, k) in enumerate(zip(axes.flat, top_scens)):
    ax.set_facecolor(CREAM)
    df = results[k]
    pol_shares = [np.mean([p[m] for p in df.attrs['P_policy']]) * 100 for m in MODES]
    base_shares_pct = [baseline_shares[m] * 100 for m in MODES]
    deltas = [pol - base for pol, base in zip(pol_shares, base_shares_pct)]

    x = np.arange(len(MODES))
    w = 0.35

    bars_base = ax.bar(x - w/2, base_shares_pct, w, label='Baseline',
                       color=[mode_colors[m] for m in MODES], alpha=0.35,
                       edgecolor='white', linewidth=0.8)
    bars_pol = ax.bar(x + w/2, pol_shares, w, label='Policy',
                      color=[mode_colors[m] for m in MODES], alpha=1.0,
                      edgecolor='white', linewidth=0.8)

    # Delta annotations on policy bars
    for i, (d, ps) in enumerate(zip(deltas, pol_shares)):
        if abs(d) > 0.3:
            color = TEAL if d > 0 else WARM
            ax.text(i + w/2, ps + 0.8, f'{d:+.1f}', ha='center', va='bottom',
                    fontsize=8, fontweight='bold', color=color)

    ax.set_xticks(x)
    ax.set_xticklabels(mode_labels, fontsize=10)
    ax.set_ylabel('Share (%)', fontsize=10, color=MUTE)
    ax.set_title(scenarios[k]['label'], fontsize=13, fontweight='bold', color=NAVY, pad=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    if idx == 0:
        ax.legend(fontsize=9, framealpha=0.8, loc='upper right')

fig.suptitle('Mode Share Shifts — Top 4 Welfare Scenarios', fontsize=16,
             fontweight='bold', color=NAVY, y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(FIGS + 'fig04_mode_shifts.png', dpi=200, bbox_inches='tight',
            facecolor=CREAM)
plt.close()
print("✓ fig04_mode_shifts.png")

print("\nAll 3 figures regenerated.")

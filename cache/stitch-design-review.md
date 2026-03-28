# Stitch Design Review — MVP-93

**Date**: 2026-03-28
**Ticket**: [MVP-93](https://linear.app/dhaneswaramandrasa/issue/MVP-93/design-review-cross-check-stitch-persona-screens-against-e7e8-acs)
**Stitch Project**: 16070191183689970351
**Screens reviewed**: 4 persona screens + MVP-90 entry screen

---

## Summary Scorecard

| Screen | Tickets | AC Coverage | Risk | Critical Gaps |
|---|---|---|---|---|
| Choose Your Lens (Entry) | MVP-90 | 60% | 🟡 Medium | Routing targets, mobile layout |
| Commuter Lens | MVP-91 | 7/7 ✅ | 🟢 Low | Destination override, mobile, transit leg detail |
| Planner/Ops Lens | MVP-28/29/31/32 | ~15% | 🔴 **CRITICAL** | Wrong map type — shows POI heatmap not quadrant choropleth |
| Researcher Lens | MVP-29/30 | 38% | 🔴 High | Gini/LISA/Lorenz missing, incomplete resolution comparison |

---

## Agent 1 — MVP-90: Persona Entry Screen

**Design**: "Choose Your Lens: Persona Selection"

### AC Assessment

| AC | Status | Notes |
|---|---|---|
| 4 goal cards: Plan My Commute, Explore Transit Equity, Analyze & Download, Plan Infrastructure | ✅ | All 4 cards present with exact titles |
| Each card routes to distinct initial map state | ⚠️ | Cards have CTA buttons; routing targets and pre-opened panels NOT annotated |
| "Skip — show full tool" option | ✅ | Link present below grid |
| `selectedPersona` Zustand field | ⚠️ | Implementation detail; enum mapping not visible in design |
| localStorage persistence for returning users | ⚠️ | Chip "Returning? Your last session was…" shown; auto-load flow not specified |
| Mobile-responsive layout | ⚠️ | Desktop 2×2 grid; no mobile breakpoint variant shown |

**Persona Mapping**:
- Rina → Plan Infrastructure ✅
- Adi → Analyze & Download ✅
- Budi → Plan Infrastructure ⚠️ (same card as Rina; ops manager role not explicit)
- Sari Mode A → Plan My Commute ✅
- Sari Mode B → Explore Transit Equity ✅

### Gaps to Fix in Stitch
1. Annotate each card with its routing target + which panels open on load
2. Add mobile breakpoint variant (2×2 → 1-column stack)
3. Clarify returning-user chip: auto-load last session or just context?

### Gaps to Fix in Ticket AC (MVP-90)
1. Map card titles → Zustand enum values explicitly (`'planner'`, `'researcher'`, `'commuter'`, `'explorer'`)
2. Specify which panels pre-open per persona (e.g., "Plan Infrastructure" → What-If Simulator panel open)
3. Define mobile breakpoint threshold

---

## Agent 2 — Commuter Lens: MVP-91

**Design**: "JTEM: Commuter Lens" | **Persona**: Sari (§4.4)

### MVP-91 AC Assessment

| AC | Status | Notes |
|---|---|---|
| Origin pin (click or type) → snapped to nearest H3 centroid | ✅ | Both interaction modes shown |
| Destination pin → defaults to Sudirman–Thamrin CBD | ✅ | Default shown |
| Results panel: Transit / GoRide / GoCar side by side with time + cost | ✅ | All 3 modes side-by-side |
| "Recommended" badge on lowest-cost mode | ✅ | Badge concept present |
| Transit legs polyline on map | ✅ | Path visualization indicated |
| "View equity context" link → Q1–Q4 quadrant | ✅ | Link present in Mode A results |
| Disclaimer on ride-hailing estimates | ✅ | Disclaimer awareness shown |

**7/7 MVP-91 ACs covered ✅** — Best coverage of all screens.

### Gaps to Fix in Stitch
1. **Destination override**: Show explicit "Change destination" button — PRD §5.10 requires user can change
2. **Mobile breakpoint**: Stacked layout for phone (map above, results below)
3. **Transit legs detail**: Expand leg-by-leg breakdown panel (first-mile walk → station → ride → transfer → last-mile)
4. **Equity context panel**: Sketch Q1–Q4 detail pop-over that "View equity context" opens

### Implementation Notes (Code Scope)
- `lib/journey-planner.ts` must encode GoRide (Rp 5K base + Rp 2K/km) and GoCar (Rp 10K base + Rp 3.5K/km)
- H3 centroid snapping must use geodetic distance, not Euclidean
- PRD §7 constraint: fully static — no real-time routing API calls

---

## Agent 3 — Planner/Ops Lens: MVP-28/29/31/32 ⚠️ CRITICAL

**Design**: "JTEM: Planner & Ops Manager Lens" | **Personas**: Rina (§4.1) + Budi (§4.3)

### MVP-28 AC Assessment (Road Network + Cost Comparison)

| AC | Status | Notes |
|---|---|---|
| Road network deck.gl layer (highway class, toggleable) | ❌ | No road network rendering. Satellite base only. |
| CBD zone polygons on map | ❌ | Not visible |
| Three-way GC card (transit/car/motorcycle) | ❌ | No cost comparison card. `gc_transit_idr`, `gc_car_idr`, `gc_motorcycle_idr` absent. |
| Transit competitive zone badge | ❌ | No `transit_competitive_zone` enum badge |
| 5-layer TAI breakdown (L1–L5) | ❌ | No TAI layer panel |
| First-mile quality indicators | ⚠️ | "Pedestrian Connectivity Index" legend shown; but no `road_density_km_per_km2`, `pct_footway_pedestrian`, `network_connectivity` |

**MVP-28: 0/6 ACs ❌**

### MVP-29 AC Assessment (Quadrant Map + Toggle)

| AC | Status | Notes |
|---|---|---|
| Quadrant choropleth at kelurahan level (4 colors) | ❌ | Design shows POI accessibility heatmap, NOT Q1/Q2/Q3/Q4 quadrant map |
| Toggle to H3 hexagon view | ❌ | No resolution toggle UI |
| Color legend with quadrant descriptions | ❌ | Legend is "Pedestrian Connectivity Index", not Q1–Q4 |
| Click → detail panel (TNI, TAI, 5 layers, equity gap, quadrant) | ⚠️ | Analytics Dashboard sidebar present; specific fields not confirmed |
| Smooth resolution transitions | ❌ | Not shown |

**MVP-29: 0.5/5 ACs ❌**

### MVP-31 AC Assessment (What-If Simulator)

| AC | Status | Notes |
|---|---|---|
| Click map to place hypothetical station | ✅ | Location coordinates input present |
| Select mode type (KRL/MRT/BRT/Mikrotrans) | ⚠️ | "LRT Phase 3 - New Hub" shown as example; no explicit 4-option dropdown |
| Configurable catchment (1km walk, 3km feeder) | ✅ | Buffer radius slider present (250m–1200m) |
| Before/after: quadrant changes, Gini delta, affected population | ⚠️ | Delta metrics shown (Equity Gap Δ, Transit Desert Mitigation) but not framed as before/after comparison |
| Labeled as "scenario simulation, not prediction" | ❌ | Disclaimer missing |

**MVP-31: 2/5 ACs ⚠️**

### MVP-32 AC Assessment (Transit Competitive Zone Map)

| AC | Status | Notes |
|---|---|---|
| 3-color choropleth (transit_wins/swing/private_wins/transit_not_available) | ❌ | Not present |
| Toggle TCR_vs_car / TCR_vs_motorcycle / TCR_combined | ❌ | No TCR toggle controls |
| Click shows full GC breakdown | ❌ | Not present |
| Distance-to-CBD rings (5/10/15/20/30km) | ❌ | Not present |
| Summary: % population per competitive zone | ❌ | Not present |

**MVP-32: 0/5 ACs ❌**

### Critical Finding

> **The Planner/Ops Lens design shows a "scenario simulator dashboard" (what-if + ops metrics: ridership forecast, catchment, peak saturation). It does NOT show the quadrant map, transit competitive zones, road network, or cost comparison — which are the primary features for Rina and Budi.**

This misrepresents the product vision:
- PRD §5.1 says quadrant classification is the **PRIMARY** view
- H1/H2/H3 hypothesis testing requires the quadrant map visible
- Rina's primary need is "quadrant map showing High Need, Low Access zones"

### Fixes Required in Stitch (Planner/Ops Lens)

1. **Add quadrant choropleth as primary map layer** — replace or layer over POI heatmap
   - Q1 (#2A9D8F), Q2 (#457B9D), Q3 (#6B8F71), Q4 (#E63946)
   - Add "Map Mode" toggle: Quadrant Analysis ↔ Pedestrian Reach ↔ Transit Zones
2. **Add resolution toggle** (kelurahan ↔ H3)
3. **Add cost comparison card** — `gc_transit_idr`, `gc_car_idr`, `gc_motorcycle_idr` + `transit_competitive_zone` badge
4. **Add road network layer toggle** — highway class color-coding
5. **Add transit competitive zone map mode** — 3-color choropleth + TCR toggles + CBD rings
6. **Add 5-layer TAI breakdown** in detail panel click
7. **Add what-if disclaimer**: "⚠️ Scenario Simulation, Not Prediction"
8. **Fix mode selector** in what-if panel: explicit KRL/MRT/BRT/Mikrotrans dropdown

---

## Agent 4 — Researcher Lens: MVP-29/30

**Design**: "JTEM: Researcher Lens" | **Persona**: Adi (§4.2)

### MVP-29 AC Assessment

| AC | Status | Notes |
|---|---|---|
| Quadrant choropleth at kelurahan level | ✅ | Shown |
| Toggle to H3 hexagon view | ✅ | Toggle visible |
| Color legend with quadrant descriptions | ⚠️ | Legend shown; descriptions (Q1=Well-Served etc.) not confirmed |
| Click → detail panel (TNI/TAI/5-layers/equity_gap/quadrant) | ✅ | Detail panel present |
| Smooth resolution transitions | ⚠️ | Not specified in design |
| Summary stats per resolution (% units per Q, Gini) | ❌ | Missing |
| Resolution comparison panel (reclassified unit count) | ❌ | Missing |
| Visual highlight of reclassified areas | ❌ | Missing |

**MVP-29: 5/8 ACs (62%)**

### MVP-30 AC Assessment

| AC | Status | Notes |
|---|---|---|
| Journey legs: first-mile → station → ride → transfer → last-mile | ✅ | Shown |
| Each leg: mode, time, fare | ✅ | Shown |
| Path polyline on map | ✅ | Shown |
| Side panel: transit vs car vs motorcycle GC | ⚠️ | GC comparison present; unclear if 3-way or 5-way |
| Five-way comparison (+ GoRide + GoCar) | ❌ | MVP-30 AC says 3-way; PRD §5.3 requires 5-way |
| Transit competitive zone badge | ❌ | Not mentioned |
| "Lowest cost" highlight across all modes | ❌ | Not shown |

**MVP-30: 3/7 ACs (43%)**

### Equity Dashboard (PRD §5.8) — CRITICAL for Adi

| Feature | Status |
|---|---|
| Gini coefficient (TAI, both resolutions) | ❌ Missing |
| Lorenz curve visualization | ❌ Missing |
| LISA cluster map (HH/HL/LH/LL/NS) | ❌ Missing |
| Quadrant % population distribution | ⚠️ Partial |
| Resolution comparison summary | ⚠️ Partial |

> **Adi cannot produce evidence-based equity reports without Gini/LISA/Lorenz. These are the core metrics of the research paper.**

### Data Download (PRD §5.9)

| Feature | Status |
|---|---|
| Download kelurahan + H3 GeoJSON | ✅ |
| Download equity_summary.json | ⚠️ Unclear |
| Paper PDF link | ⚠️ Unclear |
| CC BY 4.0 license notice | ❌ Missing |

### Fixes Required in Stitch (Researcher Lens)

1. **Add Equity Summary Dashboard panel** (or link to separate screen):
   - Gini coefficient (kelurahan vs H3 side-by-side)
   - Lorenz curve (D3 line chart)
   - LISA cluster table (HH/HL/LH/LL/NS counts + % population)
2. **Add resolution comparison stats** to toggle:
   - "X units reclassified between resolutions"
   - Visual layer for reclassified areas (distinct color/hatching)
3. **Extend GC comparison to 5-way** — add GoRide + GoCar rows
4. **Add `transit_competitive_zone` badge** to journey chain panel
5. **Add "Lowest cost" highlight** row in GC comparison table
6. **Add download structure**:
   - Explicit file options (`kelurahan_scores.geojson`, `h3_scores.geojson`, `equity_summary.json`)
   - CC BY 4.0 license notice + README link

### New Tickets Recommended (Researcher lens scope gaps)

- **New MVP-94**: Implement Equity Summary Dashboard (Gini + Lorenz + LISA) — blocked by MVP-27
- **New MVP-95**: Structured Data Export modal with CC BY 4.0 + README — blocked by MVP-27

---

## Schema Field Validation Summary

| Layer | Required Fields | Covered in Any Design | Status |
|---|---|---|---|
| Quadrant | `quadrant` (Q1/Q2/Q3/Q4) | Researcher + Entry ✅ | ✅ |
| TNI | `tni_score`, 5 sub-indicators | Partial (Researcher) | ⚠️ |
| TAI L1–L5 | `tai_score`, layer breakdowns | Missing from Planner, partial elsewhere | ⚠️ |
| GC | `gc_transit_idr`, `gc_car_idr`, `gc_motorcycle_idr` | ❌ | ❌ Critical |
| TCR | `tcr_vs_car`, `tcr_vs_motorcycle`, `tcr_combined`, `transit_competitive_zone` | ❌ | ❌ Critical |
| Equity | `equity_gap`, `gini_kelurahan`, `gini_h3`, `lisa_cluster` | ❌ | ❌ Critical |
| Journey | `est_cbd_journey_time_min`, `est_cbd_journey_fare_idr` | Partial (Commuter) | ⚠️ |

---

## Action Plan

### Immediate (before MVP-27 implementation starts)

| # | Action | Screen | Ticket |
|---|---|---|---|
| 1 | Rework Planner/Ops Lens — add quadrant choropleth as primary layer | Planner/Ops | MVP-29 blocks MVP-28 |
| 2 | Annotate MVP-90 cards with routing targets + panel states | Entry | MVP-90 |
| 3 | Add mobile variants to MVP-90 + Commuter Lens | Entry + Commuter | MVP-90, MVP-91 |
| 4 | Add equity dashboard panel to Researcher Lens (Gini/LISA/Lorenz) | Researcher | New MVP-94 |
| 5 | Add 5-way GC comparison + TCR badge to CBD Journey Chain panels | Both | MVP-30, MVP-92 |

### New Tickets to Create

| Ticket | Title | Blocked by | Epic |
|---|---|---|---|
| MVP-94 | Implement Equity Summary Dashboard (Gini + Lorenz + LISA) | MVP-27 | E8 |
| MVP-95 | Structured Data Export modal with CC BY 4.0 + field README | MVP-27 | E8 |

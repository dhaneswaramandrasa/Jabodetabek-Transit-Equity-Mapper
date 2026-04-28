# Claude Design Prompt — JTEM Journey Planner (v3)

**Project**: JTEM — Jabodetabek Transit Equity Mapper
**Stitch Project ID**: `16070191183689970351`
**Date**: 2026-04-26
**Scope**: Full origin→destination journey planner — Landing → Pin Placement → Journey Results + Savings Calculator, dual light/dark theme

---

## 0. Design System (apply project-wide)

### Creative North Star: "The Cartographic Oracle"
An editorial intelligence experience — high-end tactical tool, not a consumer dashboard. Asymmetric depth, glassmorphism, tonal layering.

### Dual Theme
Generate every screen in **both dark and light mode**. Use Stitch design system variables so users can toggle.

| Token | Dark | Light |
|---|---|---|
| `surface` | `#111125` | `#F5F5F0` |
| `surface_container` | `#1E1E32` | `#FFFFFF` |
| `surface_container_low` | `#1A1A2E` | `#F0F0E8` |
| `on_surface` | `#E2E0FC` | `#1A1A2E` |
| `primary` | `#6FD8C8` | `#006A60` |
| `primary_container` | `#00211D` | `#8CF5E4` |
| `outline_variant` | `#47464C` | `#C8C5CD` |

### Typography
- **Headlines**: Inter (Semi Bold for display, Medium for titles)
- **Body**: Inter (Regular)
- **Data/numbers**: JetBrains Mono (all percentages, costs, scores, coordinates)
- **Labels/microcopy**: Space Grotesk (category tags, sort labels, section headers)

### Surface Rules
- **No 1px solid borders** for sectioning — use tonal background shifts instead
- Glass panels: `backdrop-blur-md`, `bg-surface/85`
- Ghost borders only when necessary: `outline_variant` at 15% opacity
- **No pure black (#000) or pure white (#FFF)**
- Corner roundness: `rounded-lg` (8px) max — engineered, architectural feel

### Color Semantics (data only)
- Q1 Well-Served: `#2A9D8F` (green)
- Q4 Transit Desert: `#E63946` (red)
- Q2 Over-Served: `#457B9D` (blue)
- Q3 Car Suburb: `#F4A261` (amber)
- Transit modes: `#06D6A0`
- Private modes: `#EF476F`

---

## 1. Landing Screen

### Layout
Full-viewport interactive map (Jabodetabek region) with a centered floating glass panel overlay.

### Floating Panel Content
```
┌─────────────────────────────────────┐
│  [JTEM wordmark]                    │
│                                     │
│  What's the best way to get        │
│  around Jabodetabek?               │  ← Inter Display, large
│                                     │
│  Compare transit, ride-hailing,     │
│  and private modes for any trip     │  ← Inter Body, on-surface/60
│  across Greater Jakarta. See how    │
│  much you could save.              │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 📍 Set starting point       │   │  ← Primary action, prominent
│  │    e.g., Bojong Gede        │   │    Icon + label + placeholder
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 📍 Set destination          │   │  ← Secondary, ghost border
│  │    e.g., Sudirman           │   │
│  └─────────────────────────────┘   │
│                                     │
│  Or click the map to explore        │  ← Link, on-surface/40
│  transit equity across Jabodetabek  │
│                                     │
│  ─────────────────────────────      │
│  💡 Based on nested logit mode      │  ← Micro-copy, on-surface/30
│  choice with real GTFS transit data │
└─────────────────────────────────────┘
```

### Panel Style
- Glassmorphism: `bg-surface/85 backdrop-blur-md`
- Centered both axes initially
- Subtle ambient shadow (no hard outline)
- Animate entrance with slight scale + fade

### Map State
- Jabodetabek viewport
- H3 hexagon layer visible at low opacity
- No pins yet

---

## 2. Pin Placement (Active State)

When user clicks "Set starting point" or "Set destination", the panel transitions:

### Active Pin Row
```
┌─────────────────────────────────────┐
│  Click the map to set your starting │  ← Banner with crosshair cursor hint
│  point                              │
│                                     │
│  ● 📍 Bojong Gede, Bogor      [✕]  │  ← Active row, primary border
│                                     │    Shows reverse-geocoded name
│  ○ 📍 Set destination               │  ← Inactive row, muted
│                                     │
│  [Cancel]     [Confirm →]          │
└─────────────────────────────────────┘
```

### Key UX details
- **Reverse geocoding**: After click, show actual kelurahan/kecamatan name (not literal "Home")
- Active row highlighted with `border-primary/30 bg-primary/5`
- Map cursor changes to crosshair during pin mode
- Unknown zone warning if clicked area has no H3 data: "Unknown area — estimates may be approximate" in amber

---

## 3. Journey Results Panel (after both pins set)

This is the main screen — a right-side sliding panel (380-420px wide) over the map.

### Panel Structure (top to bottom)

```
┌──────────────────────────────────┐
│ HEADER                           │
│ 📍 Bojong Gede → 📍 Sudirman    │  ← Location names (reverse-geocoded)
│ ● Transit Desert                 │  ← Zone quadrant badge
│                        [← Back]  │
│                                  │
│ SORT BY  [Best bet] [Cheapest] [Fastest]  │  ← Sort toggle pills
├──────────────────────────────────┤
│                                  │
│ EQUITY CONTEXT CARD              │  ← ABOVE mode cards (product differentiator)
│ ┌────────────────────────────┐  │
│ │ YOUR ORIGIN ZONE           │  │  ← Uppercase label, Space Grotesk
│ │                            │  │
│ │ ● Transit Desert           │  │  ← Quadrant color dot + label
│ │ Transit access score: 23/100│  │  ← JetBrains Mono number
│ │                            │  │
│ │ Transit Desert — limited   │  │  ← Contextual description
│ │ frequency and coverage in  │  │    (Q4: red text, Q1: emerald)
│ │ this zone. First/last mile │  │
│ │ is critical.               │  │
│ └────────────────────────────┘  │
│                                  │
│ MODE CARDS (sorted per toggle)   │
│                                  │
│ ┌────────────────────────────┐  │
│ │ 🚌 Transit + Feeders       │  │  ← Icon + Mode label
│ │ GoRide → KRL → Walk        │  │  ← Chain label (multi-modal!)
│ │                    45 min  │  │  ← Total time
│ │                    Rp 12k  │  │  ← Total cost
│ │                            │  │
│ │ ████████████░░░░░░  52%    │  │  ← Probability bar
│ │                            │  │
│ │ [expanded view on tap]     │  │
│ │  🚶 Walk 0.8 km → station │  │  ← First mile leg
│ │  🚆 KRL Bojong Gede→Sudirman 25 min  │
│ │  🚶 Walk 0.3 km → dest    │  │  ← Last mile leg
│ │  ─────────────────────     │  │
│ │  Total  45 min · Rp 12,000 │  │
│ └────────────────────────────┘  │
│                                  │
│ ┌────────────────────────────┐  │
│ │ 🏍 GoRide                  │  │
│ │ Door-to-door               │  │
│ │                    30 min  │  │
│ │                    Rp 25k  │  │
│ │ ████████░░░░░░░░  35%     │  │
│ │ ℹ Estimated — actual varies│  │  ← Ride-hailing disclaimer
│ │   with surge pricing       │  │
│ └────────────────────────────┘  │
│                                  │
│ ┌────────────────────────────┐  │
│ │ 🚗 GoCar                   │  │
│ │ Door-to-door               │  │
│ │                    40 min  │  │
│ │                    Rp 45k  │  │
│ │ ███░░░░░░░░░░░░░   8%     │  │
│ │ ℹ Estimated — actual varies│  │
│ └────────────────────────────┘  │
│                                  │
│ ┌────────────────────────────┐  │
│ │ 🏍 Motorcycle (private)    │  │
│ │                    28 min  │  │
│ │                     Rp 8k  │  │
│ │ ██░░░░░░░░░░░░░░   4%     │  │
│ └────────────────────────────┘  │
│                                  │
│ ┌────────────────────────────┐  │
│ │ 🚗 Car (private)           │  │
│ │                    55 min  │  │
│ │                    Rp 35k  │  │
│ │ █░░░░░░░░░░░░░░░   1%     │  │
│ └────────────────────────────┘  │
│                                  │
│ SAVINGS CALCULATOR               │  ← NEW — financial comparison
│ ┌────────────────────────────┐  │
│ │ YOUR TRIP, YOUR MONEY      │  │
│ │                            │  │
│ │ Best bet per trip:         │  │
│ │ Transit + Feeders  Rp 12k  │  │  ← Optimal mode + cost
│ │                            │  │
│ │ If you took this trip      │  │
│ │ 22 days/month (round-trip):│  │
│ │                            │  │
│ │ ┌──────────────────────┐  │  │
│ │ │ Mode          Monthly  Annual │  │
│ │ │ Transit+Feeders Rp 528k  Rp 6.3M │  │  ← Optimal row, highlighted
│ │ │ GoRide        Rp 1.1M  Rp 13.2M │  │
│ │ │ GoCar         Rp 1.98M Rp 23.8M │  │
│ │ │ Motorcycle    Rp 352k  Rp 4.2M  │  │
│ │ │ Car           Rp 1.54M Rp 18.5M │  │
│ │ └──────────────────────┘  │  │
│ │                            │  │
│ │ You save up to             │  │
│ │ Rp 1.45M/month             │  │  ← Hero number, large, primary
│ │ vs always using GoCar      │  │
│ │                            │  │
│ │ ─────────────────────      │  │
│ │ MIXED STRATEGY             │  │  ← Collapsible subsection
│ │                            │  │
│ │ What if you mix modes?     │  │
│ │                            │  │
│ │ Transit + Feeders  ──●── 60%  │  │  ← Sliders, sum must = 100%
│ │ GoRide            ──●── 20%  │  │
│ │ Motorcycle        ──●── 15%  │  │
│ │ GoCar             ──●──  5%  │  │
│ │ Car               ──●──  0%  │  │
│ │                     Σ 100%   │  │
│ │                            │  │
│ │ Mixed monthly:  Rp 720k    │  │  ← Blended cost
│ │ vs always GoRide: save Rp 380k/month │
│ │                            │  │
│ │ Annual savings: Rp 4.6M    │  │  ← Bold, JetBrains Mono
│ └────────────────────────────┘  │
│                                  │
│ WHAT-IF (collapsible)            │
│ ┌────────────────────────────┐  │
│ │ + Add hypothetical transit  │  │  ← Expandable section
│ │                            │  │
│ │ [expanded]                 │  │
│ │ What if there were a...    │  │
│ │                            │  │
│ │ [TransJakarta ▼] route     │  │  ← Mode dropdown
│ │ [1.0 km ▼] from origin     │  │  ← Distance sliders
│ │ [0.5 km ▼] from destination│  │
│ │                            │  │
│ │ [Recalculate]              │  │
│ │                            │  │
│ │ New probabilities:         │  │
│ │ Transit + Feeders: 52% → 68% ▲  │  ← Before/after comparison
│ │ GoRide: 35% → 22% ▼       │  │
│ │                            │  │
│ │ New monthly savings:       │  │
│ │ Rp 1.8M vs GoCar 🎉        │  │
│ └────────────────────────────┘  │
│                                  │
│ Probabilities from nested logit  │  ← Footer note, subtle
│ model. Estimates only — not     │
│ GTFS trip-planning.             │
└──────────────────────────────────┘
```

### Mode Card Design Details

Each mode card is a tappable row with progressive disclosure:

**Collapsed state:**
- Left: Material icon (directions_transit, two_wheeler, directions_car)
- Center: Mode label + chain label (e.g., "GoRide → KRL → Walk")
- Tags: "Cheapest" (emerald pill), "Fastest" (blue pill) when applicable
- Right: Time (bold) + Cost (smaller, muted)
- Below: Probability bar with percentage

**Highest probability card (>30%)**: Subtle primary border highlight (`border-primary/30 bg-primary/5`)

**Expanded state (on tap):**
- Leg-by-leg breakdown with icons, labels, duration, distance
- Each leg shows: icon → description → time + distance → cost
- Total row at bottom with border-top separator
- Method note in italic if applicable

**Unavailable modes**: 40% opacity, "Not available" red tag, not clickable

### Sort Toggle
- Three pill buttons: "Best bet" (probability), "Cheapest" (cost), "Fastest" (time)
- Active pill: `bg-primary/15 text-primary`
- Inactive: `text-on-surface/40 hover:text-on-surface/70`
- Re-sorts mode cards in real-time

### Equity Context Card
- Placed **above** mode cards — this is the product's unique differentiator
- Quadrant color dot + label
- TAI score in JetBrains Mono (e.g., "23/100")
- Context-aware description:
  - Q4: "Transit Desert — limited frequency and coverage in this zone. First/last mile is critical."
  - Q1: "Well-served — transit is competitive here. Your commute has good options."
  - Q2/Q3: appropriate neutral descriptions

### What-If Section (collapsible, at bottom)
- Default collapsed: "＋ Add hypothetical transit" button
- Expanded: mode dropdown (TransJakarta / MRT / LRT / KRL), distance sliders (0.5–5 km from home, 0.5–5 km from office)
- Shows before/after probability comparison with ▲▼ arrows
- New hypothetical option inserted into the choice set and nested logit re-run

### Savings Calculator

A financial comparison card between mode cards and what-if section. This turns probabilities into actionable rupiah decisions.

**Assumptions (shown as subtle footnote):**
- Round-trip = 2× one-way cost
- 22 working days per month, 12 months per year
- Does not include vehicle ownership costs (depreciation, insurance, parking)

**Comparison Table:**
- Columns: Mode | Monthly cost | Annual cost
- Rows: All 5 modes (transit chain + GoRide + GoCar + motorcycle + car)
- Optimal mode row highlighted with subtle primary background
- All costs in JetBrains Mono, right-aligned
- Indonesian number formatting (Rp 528.000, not Rp 528000)

**Hero Savings Number:**
- Large display: "You save up to Rp X/month vs always using [most expensive mode]"
- Primary color, large type (Inter Display)
- Dynamically picks the biggest savings delta

**Mixed Strategy (collapsible subsection):**
- Header: "What if you mix modes?" with info tooltip
- Slider per available mode (5 sliders)
  - Range: 0-100%, step 5%
  - Visual: `primary` fill track, ghost border
  - Label shows mode name + current %
  - Sliders auto-normalize or show validation when sum ≠ 100%
- "Σ 100%" indicator — green when balanced, amber when off
- Result row: "Mixed monthly: Rp X" with JetBrains Mono
- Comparison: "vs always [mode]: save Rp X/month"
- Annual projection: bold, larger

**Edge cases:**
- If only 1 mode available: show simpler "Your only option" message, no sliders
- If all modes unavailable: hide savings calculator entirely
- Decimal percentages round to nearest 5% on sliders

### Ride-Hailing Disclaimers
- Shown for GoRide and GoCar modes only
- Small text: "Estimated fare — actual varies with surge pricing and traffic."
- Placement: below probability bar, above leg breakdown

### Map (background)
- H3 hex layer with quadrant colors (Q1-Q4)
- Home pin (filled circle) and office pin (filled square) rendered on map
- Journey polyline connecting home → transit stops → office (dashed for walk legs, solid for transit/ride legs)

---

## 4. Loading / Transition States

When user confirms both pins, brief transition before journey panel slides in:

### Loading
- Brief spinner or skeleton (under 800ms — journey is computed synchronously)
- Dark theme tokens ONLY (no light-theme flash)
- Simple: "Computing journey options..." with subtle animated dots

### Empty State (no route data)
```
┌──────────────────────────────────┐
│                                  │
│     No route data available      │
│       for this zone.             │
│                                  │
│  Try a location closer to the    │
│  transit network.                │
└──────────────────────────────────┘
```

### Unknown Zone Warning
- Amber warning text: "Unknown area — estimates are approximate."
- Shown when H3 zone lookup returns null
- Still shows mode cards (fallback estimates)

---

## 5. App Shell (persistent chrome)

### Top Bar (fixed, 56px)
- Left: "JTEM" wordmark (primary color, bold)
- Center tabs (optional, can be hidden for commuter MVP): Explorer | Insights | Archive
- Right: Theme toggle (☀️/🌙), Notifications, Settings, Avatar

### Sidebar (fixed left, collapsed to icons)
- Width: 80px collapsed → 256px on hover (smooth transition)
- Icons only when collapsed, labels appear on hover
- Nav items: Commuter (active), Researcher, Planner, Stats
- Active item: `bg-surface-container text-primary border-r-4 border-primary`
- Bottom: "Download Data" button (visible on hover), Docs/Feedback links
- **UX note**: Only Commuter is wired in MVP. Other nav items should visually indicate "coming soon" (reduced opacity, tooltip) rather than being fully interactive but broken.

### Glass & Depth
- Top bar: `bg-surface_container_low/90 backdrop-blur-md`
- Sidebar: `bg-surface_container_low/90 backdrop-blur-md`
- Ghost border between chrome and map: `outline_variant` at 10% opacity

---

## 6. Map Layer States

### Hex Layer
- H3 resolution 8 hexagons across Jabodetabek
- Color by quadrant: Q1 green, Q2 blue, Q3 amber, Q4 red
- Opacity: 0.6 fill, no stroke (or ghost stroke at 5%)
- Highlighted hex on hover: brighter, subtle scale pulse

### Pins
- Origin: filled circle, primary color, 12px radius
- Destination: filled square, tertiary color, 10px
- Both with subtle pulse animation on placement

### Journey Polyline
- Walk legs: dashed line, on-surface/40
- Transit legs: solid line, primary color, 2px
- Ride-hailing/drive legs: solid line, on-surface/60, 1.5px
- Animated dash-array on render

---

## 7. Dark/Light Variants

Every screen component should render correctly in both modes. Key differences:

| Element | Dark | Light |
|---|---|---|
| Map base | `#0C0C1F` (surface_container_lowest) | `#F5F5F0` (surface) |
| Glass panels | `rgba(15,15,26,0.85)` | `rgba(255,255,255,0.85)` |
| Text primary | `#E2E0FC` | `#1A1A2E` |
| Text muted | `#E2E0FC` at 40% | `#1A1A2E` at 50% |
| Card bg | `#1E1E32` (surface_container) | `#FFFFFF` |
| Card hover | `rgba(255,255,255,0.06)` | `rgba(0,0,0,0.04)` |
| Ghost border | `#47464C` at 15% | `#C8C5CD` at 25% |
| Probability bar bg | `rgba(255,255,255,0.08)` | `rgba(0,0,0,0.06)` |

---

## 8. Screen Inventory (what to generate)

Generate the following screens in **both dark and light themes**:

| # | Screen | Description |
|---|---|---|
| 1 | **Landing** | Map + centered glass panel with origin/destination inputs |
| 2 | **Pin Active** | Origin row active, map crosshair, "Click the map" banner |
| 3 | **Journey Results (Q4)** | Transit Desert origin — equity card, 5 mode cards, probability bars, savings calculator |
| 4 | **Journey Results (Q1)** | Well-served origin — different equity messaging, different probabilities, different savings |
| 5 | **Mode Expanded** | Transit chain expanded showing all legs (walk → KRL → walk) |
| 6 | **Savings Calculator — Mixed Strategy** | Sliders adjusted, blended monthly cost, annual projection |
| 7 | **What-If Expanded** | Hypothetical transit section open, before/after probability + new savings |
| 8 | **Empty State** | No route data available for zone |
| 9 | **Loading Transition** | Brief loading state between pin confirm and results |

# UX Review — Commuter Journey (MVP)

**Date**: 2026-04-26
**Branch**: `ui/stitch-redesign`
**Reviewer**: UX Researcher agent (4-persona PRD evaluation)
**Scope**: Commuter dual-pin flow — Landing → Pin placement → Results (JourneyPanel)

---

## Strengths

1. **Familiar interaction pattern.** Dual-pin origin/destination mirrors Gojek, Grab, and Google Maps. Zero learning curve for Jakarta commuters. Row connector line reinforces directionality.

2. **Clear pin-mode affordance.** Banner ("Click the map to set your home/office") with Cancel. Active row highlights with `border-primary bg-primary/10`. Map cursor switches to crosshair.

3. **Tag system on mode cards.** Cheapest/Fastest/Best Value tags with distinct color tokens (emerald/blue/teal) enable instant scanning of the 5-mode list.

4. **Progressive disclosure on mode cards.** Legs breakdown hidden behind tap/click, keeping initial list scannable while providing detail on demand.

5. **Zone equity context card.** Connects personal commute to the research question. For Dewi living in a Transit Desert, knowing that context is empowering — this is the product's unique value over ride-hailing apps.

6. **localStorage persistence of home pin.** Repeat commuters don't need to re-pin. Good touch for daily use.

7. **Scientifically grounded estimation.** GC formula, BPR banded speeds, two-zone composite — invisible to Dewi but valuable for researcher/planner personas if surfaced.

8. **Typography hierarchy.** Headline scannable in one glance. Italic "to get to work" emphasizes commuter framing. Stat badges appropriately recede.

---

## Problems

### P1: No reverse geocoding — pins show literal "Home" / "Office"

**Location**: `AccessibilityMap.tsx:289-292`, `store.ts` `setHomePin`/`setOfficePin`

The click handler calls `setHomePin([lng, lat])` with no second argument. The store defaults to the string `"Home"`. There is no reverse geocoding step.

**Impact**: After clicking Bojong Gede on the map, the row reads "Home." This destroys trust immediately — if the app doesn't know where she lives, how can it compute her commute? This is the first data the user sees after placing a pin, and it's wrong 100% of the time.

**Fix**: Use the H3 hex lookup result's `kelurahan_name` or `kecamatan_name` field. Fallback: Nominatim reverse geocode.

### P1: Three of four personas completely unserved

**Location**: `AppShell.tsx:11-16`, `ResultsLayout.tsx:7-10`

The sidebar shows Commuter, Researcher, Planner, Stats. Only Commuter has a wired path. The three lens components are commented out. Top tabs (Explorer, Insights, Archive) are all cosmetic. Rina can't see the quadrant equity map. Adi can't see Gini coefficients. Budi can't run what-if scenarios.

**The sidebar is making promises the app cannot keep.** The original persona entry screen was removed (correct for MVP focus), but the multi-persona sidebar was kept — worst of both worlds. Either restore the persona entry screen and wire the lenses, or reduce the sidebar to match actual capabilities.

### P2: LoadingSequence uses light-theme colors in dark-theme app

**Location**: `LoadingSequence.tsx:69, 93-99, 109, 113`

Uses `text-slate-800`, `text-blue-600`, `text-emerald-600`, `bg-slate-100`, `bg-white/40` — all light-theme tokens. After the dark glassmorphism landing panel, this is a jarring visual discontinuity.

**Fix**: Replace with theme tokens (`text-on-surface`, `text-primary`, `bg-surface/40`).

### P2: "Or click the map directly" launches unexplained alternate flow

**Location**: `LandingOverlay.tsx:259`

Clicking the map while not in pin mode triggers the zone-analysis flow (CardGrid with TransitScoreCard, DemographicsCard, etc.) — a completely different UI with no explanation. For Dewi asking "what's the cheapest way to get to work," getting an academic equity dashboard instead is confusing.

**Fix**: Rephrase to "Explore transit equity across Jabodetabek" to set context for the zone-analysis flow.

### P2: No journey polyline rendered on map

**Location**: `JourneyPanel.tsx` — no map rendering logic

Journey panel shows text legs but nothing is drawn on the map. The PRD calls for transit journey polyline rendering. Infrastructure exists (PathLayer, RouteData type) but is unused.

**Fix**: Pass journey waypoints to map state and render PathLayer.

### P3: "Recommended" badge uses Generalized Cost, not financial cost

**Location**: `journey.ts:471-474`

The `recommended` flag sorts by `generalizedCostIdr` which includes VOT (Rp 500/min) + walk/wait penalties. Dewi's budget is Rp 50k/day — she optimizes for rupiah, not academic mode-choice models. If transit costs Rp 10k but takes 90 min vs GoRide at Rp 25k / 30 min, GC might favor GoRide (lower time penalty) while Dewi can only afford transit.

**Fix**: Label as "Best Value" and explain. Add sort toggle by cost/time.

### P3: Zone equity context buried below mode cards

**Location**: `JourneyPanel.tsx:226-265`

The equity context card (quadrant + TAI score) sits after all 5 mode cards. This is the product's unique differentiator but is visually the least prominent element.

**Fix**: Move it above the mode cards or make it a prominent first card.

### P4: 5 modes may overwhelm budget-constrained commuters

Dewi doesn't own a car. The Car and Motorcycle rows are noise she can't use. Consider filtering by vehicle ownership data or hiding behind "Show all modes."

### P4: Loading stages describe equity analysis, not journey computation

**Location**: `LoadingSequence.tsx:7-11`

The four loading stages ("Resolving location...", "Finding reachable places...", etc.) describe the zone-analysis flow, not the commuter journey. The journey is computed synchronously in `useMemo` — there are no async stages to display. The 1.8-second delay is purely aesthetic.

**Fix**: Reduce to a brief spinner, or make stages match what the app is actually doing.

### P4: No validation of pin bounds

**Location**: `AccessibilityMap.tsx:276-295`

No check that clicked coordinates fall within the Jabodetabek study area. A click in Central Java will still set pins and produce meaningless results.

**Fix**: Bounding box check with toast: "This location is outside the Jabodetabek study area."

---

## Persona Coverage

| Persona | PRD Goal | Current Status | Missing |
|---|---|---|---|
| **Dewi (Commuter)** | Compare transit vs ride-hailing costs | Served but broken | Reverse geocoding, map route rendering, cost-based sorting |
| **Rina (Planner)** | Justify budget for Q4 zones | Not served | Quadrant choropleth, what-if simulator, data download |
| **Adi (Researcher)** | Gini coefficients, resolution comparison | Not served | Dual-resolution toggle, LISA clusters, raw data export |
| **Budi (Transit Ops)** | What-if feeder route placement | Partially served | What-if simulator exists but not wired from commuter flow |

The MVP delivers for exactly 1 of 4 personas.

---

## Recommendations

### Immediate (before next deploy)

| # | Recommendation | Effort | Files |
|---|---|---|---|
| R1 | Add reverse geocoding — use H3 zone `kelurahan_name` | 1-2h | `AccessibilityMap.tsx`, `LandingOverlay.tsx` |
| R2 | Either remove inactive sidebar nav items or wire Researcher lens minimally | 1-3h | `AppShell.tsx`, `ResultsLayout.tsx` |
| R3 | Fix LoadingSequence colors to dark theme tokens | 30m | `LoadingSequence.tsx` |
| R4 | Rephrase "Or click the map directly" → set context for zone-analysis flow | 15m | `LandingOverlay.tsx:259` |

### Short-term (this sprint)

| # | Recommendation | Effort | Files |
|---|---|---|---|
| R5 | Render transit journey as polyline on map | 2-4h | `JourneyPanel.tsx`, `AccessibilityMap.tsx` |
| R6 | Change "Recommended" → "Best Value", add cost/time sort toggle | 1-2h | `JourneyPanel.tsx`, `journey.ts` |
| R7 | Validate pin coordinates against study area bounding box | 30m | `AccessibilityMap.tsx` |
| R8 | Move zone equity card above mode cards | 30m | `JourneyPanel.tsx` |

### Medium-term (next sprint)

| # | Recommendation | Effort |
|---|---|---|
| R9 | Restore persona entry screen as optional overlay (default: commuter, skip available) | 4-6h |
| R10 | Add "Analyze this zone" + "Research view" entry points from commuter flow | 3-5h |
| R11 | Hide Car/Motorcycle behind "Show other modes" toggle | 1h |
| R12 | Replace fake loading sequence with brief spinner or real async tracker | 1h |

---

## Quick Wins (< 1 hour)

| # | Fix | Why |
|---|---|---|
| Q1 | Placeholder: "Set home location (e.g., Bojong Gede)" | Anchors in Dewi's world |
| Q2 | Disclaimer on GoRide/GoCar: "Estimated — actual fare varies with surge" | PRD requirement, currently missing |
| Q3 | Warning when `homeZone` is null: "Unknown area — estimates may be inaccurate" | Better than silent "No route data available" |
| Q4 | Reduce loading delay from 1.8s to 0.8s or remove entirely | Deceptive UX — journey is synchronous |
| Q5 | `role="button"` + keyboard handlers on mode cards | Accessibility (PRD §8) |
| Q6 | Truncation fix: `max-w-[120px]` clips longer kelurahan names | Location names are key trust signals |

---

## On the Persona Entry Screen Decision

**Removing the persona entry screen was the right call for MVP.** A multi-goal entry screen adds a click and cognitive decision before the user reaches their goal. "Find the cheapest way to get to work" is universally understood and benefits from zero-friction entry.

**But the sidebar should have been reduced to match.** The current state — 4 persona nav items, 3 dead, cosmetic top tabs, commented-out lenses — signals capabilities that don't exist. Users clicking Researcher and getting nothing will lose trust.

**Recommendation**: Keep commuter-first landing. Reduce sidebar to Commuter + "Explore" (CardGrid). Add unobtrusive "Switch to Research Mode" link revealing other lenses. Wire at least one non-commuter view before next deploy.

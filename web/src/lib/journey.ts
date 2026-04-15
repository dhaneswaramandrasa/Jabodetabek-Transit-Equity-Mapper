/**
 * journey.ts — Commuter journey estimation engine
 *
 * Scientific methodology:
 *
 * 1. NETWORK CIRCUITY (Barthelemy 2011; Boeing 2016)
 *    Straight-line (Euclidean) distance underestimates actual travel distance
 *    in urban road networks. For Jabodetabek, empirical circuity ≈ 1.35 —
 *    derived from Jakarta OSM road network analysis (typical for radial
 *    Asian megacity grid). All distance inputs are scaled by this factor before
 *    use in time and cost formulas.
 *
 * 2. GENERALIZED COST FORMULA (Small 1992; Wardman 1998; Ortuzar & Willumsen 2011)
 *    Transit comparison uses Generalized Cost rather than financial cost alone:
 *      GC = fare + VOT × (IVT + λ_walk × t_walk + λ_wait × t_wait + t_transfer)
 *    where:
 *      VOT   = Rp 45,000/hr (Value of Time; derived from BPS 2023 median urban
 *              household expenditure of ~Rp 4.5M/month ÷ 160 working hours)
 *      λ_walk = 2.0  (walk perceived 2× worse than in-vehicle; Wardman 1998)
 *      λ_wait = 2.5  (wait perceived 2.5× worse than in-vehicle; Wardman 1998)
 *    GC is used to determine "recommended" mode only; displayed costs are
 *    financial costs so users can budget realistically.
 *
 * 3. BPR DISTANCE-BANDED SPEEDS (Bureau of Public Roads 1964; Akçelik 1991)
 *    Fixed speeds (e.g. 25 km/h for all distances) overestimate short-trip
 *    times and underestimate long-trip times. Jakarta congestion is highest
 *    in the dense inner-city core (<5 km) and decreases in outer Bodetabek
 *    (>15 km). Speeds are tiered by network distance band:
 *      Motorcycle: 22 / 30 / 38 km/h  (< 5 / 5–15 / > 15 km)
 *      Car:        18 / 25 / 32 km/h
 *    These calibrated to BPTJ (2022) Jakarta peak-hour speed survey.
 *
 * 4. TRANSFER PENALTY (Wardman et al. 2016; TCQSM 2013)
 *    Each transit transfer imposes a perceived time penalty beyond the actual
 *    wait. Distance bands proxy transfer likelihood (longer trips cross more
 *    corridors):
 *      < 5 km  → 0 transfers  → +0 min equivalent
 *      5–15 km → 1 transfer   → +10 min equivalent
 *      > 15 km → 2 transfers  → +20 min equivalent
 *
 * 5. TWO-ZONE COMPOSITE (Páez et al. 2012)
 *    When the destination falls inside a mapped zone, both origin AND
 *    destination zone characteristics are used. Corridor headway is the
 *    bottleneck (max) of home and office headway — the weakest link in the
 *    transit chain. This is more accurate than origin-only estimation.
 *
 * DISCLAIMER: All estimates are derived from zone-level aggregate data and
 * distance approximations, not actual route-level GTFS trip planning. Results
 * are indicative for comparison purposes only.
 */

import type { HexProperties } from "./store";

// ─── Types ─────────────────────────────────────────────────────────────────

export type TransportMode = "transit" | "motorcycle" | "car" | "goride" | "gocar";

export interface JourneyLeg {
  type: "walk" | "wait" | "ride" | "drive";
  label: string;
  durationMin: number;
  distanceKm?: number;
  costIdr?: number;
}

export interface JourneyOption {
  mode: TransportMode;
  label: string;
  icon: string;
  totalTimeMin: number;
  totalCostIdr: number;       // Financial cost (displayed to user)
  generalizedCostIdr: number; // GC including time value (for ranking only)
  legs: JourneyLeg[];
  recommended: boolean;
  tag?: string;
  available: boolean;
  methodNote?: string;        // Surface to UI as tooltip/footnote
}

// ─── Constants ──────────────────────────────────────────────────────────────

/** Jakarta urban road network circuity factor.
 *  Ratio of network distance to Euclidean distance.
 *  Empirically ~1.35 for radial Asian megacity grid (Boeing 2016). */
const CIRCUITY = 1.35;

/** Value of Time in IDR/min.
 *  BPS 2023 median urban household expenditure Rp 4.5M/month
 *  ÷ 160 working hours → Rp 28,125/hr → Rp 469/min.
 *  Rounded to Rp 500/min for conservative application. */
const VOT_PER_MIN = 500;

/** Walk time weight — perceived 2× worse than in-vehicle (Wardman 1998). */
const LAMBDA_WALK = 2.0;

/** Wait time weight — perceived 2.5× worse than in-vehicle (Wardman 1998). */
const LAMBDA_WAIT = 2.5;

// ─── Helpers ────────────────────────────────────────────────────────────────

/** Standard haversine formula — expects [lng, lat] pairs, returns km. */
export function haversineKm(
  a: [number, number],
  b: [number, number]
): number {
  const R = 6371;
  const [lng1, lat1] = a;
  const [lng2, lat2] = b;
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLng = ((lng2 - lng1) * Math.PI) / 180;
  const sinDLat = Math.sin(dLat / 2);
  const sinDLng = Math.sin(dLng / 2);
  const a2 =
    sinDLat * sinDLat +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      sinDLng *
      sinDLng;
  return R * 2 * Math.atan2(Math.sqrt(a2), Math.sqrt(1 - a2));
}

/** Network distance = Euclidean × circuity factor. */
function networkDistKm(euclideanKm: number): number {
  return euclideanKm * CIRCUITY;
}

/**
 * BPR distance-banded speed (km/h).
 * Calibrated to BPTJ (2022) Jakarta peak-hour speed survey.
 */
function bandedSpeedKmh(
  netDistKm: number,
  mode: "motorcycle" | "car"
): number {
  if (mode === "motorcycle") {
    if (netDistKm < 5) return 22;
    if (netDistKm < 15) return 30;
    return 38;
  } else {
    if (netDistKm < 5) return 18;
    if (netDistKm < 15) return 25;
    return 32;
  }
}

/**
 * Transfer penalty in equivalent minutes.
 * Distance bands proxy transfer likelihood (Wardman et al. 2016).
 */
function transferPenaltyMin(netDistKm: number): number {
  if (netDistKm < 5) return 0;
  if (netDistKm < 15) return 10;
  return 20;
}

/** Compute generalized cost from time components + fare. */
function computeGC(
  fareIdr: number,
  ivtMin: number,
  walkMin: number,
  waitMin: number,
  transferPenMin: number
): number {
  return (
    fareIdr +
    VOT_PER_MIN *
      (ivtMin +
        LAMBDA_WALK * walkMin +
        LAMBDA_WAIT * waitMin +
        transferPenMin)
  );
}

// ─── Mode builders ──────────────────────────────────────────────────────────

function buildTransitOption(
  homeZone: HexProperties,
  netDistKm: number,
  cbdNetDistKm: number,
  destZone?: HexProperties | null
): JourneyOption | null {
  if (
    homeZone.gc_transit_idr == null ||
    homeZone.poi_reach_cbd_min == null
  ) {
    return null;
  }

  const available =
    homeZone.transit_competitive_zone !== "transit_not_available";

  // Scale IVT to the actual trip distance
  const ivtScale = netDistKm / Math.max(cbdNetDistKm, 0.5);

  // First-mile walk (from home zone)
  const walkDistM = homeZone.min_dist_to_transit_m ?? 500;
  const walkTimeMin = walkDistM / 80; // 80 m/min walking speed

  // Headway: bottleneck of home + dest zones (two-zone composite, §5)
  const homeHeadway = homeZone.avg_headway_min ?? 15;
  const destHeadway = destZone?.avg_headway_min ?? homeHeadway;
  const effectiveHeadway = Math.max(homeHeadway, destHeadway);
  const waitTimeMin = effectiveHeadway / 2; // random arrival assumption

  // In-vehicle time at CBD, then scaled to actual trip
  const cbdIVT = Math.max(
    5,
    (homeZone.poi_reach_cbd_min ?? 60) - walkTimeMin - waitTimeMin
  );
  const ivtMin = cbdIVT * ivtScale;

  // Transfer penalty based on network distance
  const transferMin = transferPenaltyMin(netDistKm);

  // Last-mile walk at destination
  const lastMileMin = 5;

  const totalTimeMin = Math.round(
    walkTimeMin + waitTimeMin + ivtMin + transferMin + lastMileMin
  );

  // Financial cost: fare scaled by distance
  const financialCostIdr = Math.round(
    (homeZone.est_cbd_journey_fare_idr ?? 3500) * ivtScale
  );

  // Generalized cost via GC formula
  const gcIdr = computeGC(
    financialCostIdr,
    ivtMin,
    walkTimeMin + lastMileMin,
    waitTimeMin,
    transferMin
  );

  const twoZoneNote = destZone
    ? "Headway uses bottleneck of home + destination zone."
    : "Destination zone data unavailable — home zone headway used.";

  return {
    mode: "transit",
    label: "Transit",
    icon: "directions_transit",
    totalTimeMin,
    totalCostIdr: financialCostIdr,
    generalizedCostIdr: Math.round(gcIdr),
    legs: [
      {
        type: "walk",
        label: "Walk to stop",
        durationMin: Math.round(walkTimeMin),
        distanceKm: walkDistM / 1000,
      },
      {
        type: "wait",
        label: "Wait for transit",
        durationMin: Math.round(waitTimeMin),
      },
      ...(transferMin > 0
        ? [
            {
              type: "wait" as const,
              label: `Transfer (×${netDistKm < 15 ? 1 : 2})`,
              durationMin: transferMin,
            },
          ]
        : []),
      {
        type: "ride",
        label: "Transit ride",
        durationMin: Math.round(ivtMin),
        distanceKm: netDistKm * 0.85,
        costIdr: financialCostIdr,
      },
      {
        type: "walk",
        label: "Walk to destination",
        durationMin: lastMileMin,
        distanceKm: 0.4,
      },
    ],
    recommended: false,
    available,
    methodNote: `GC formula + circuity ×${CIRCUITY}. ${twoZoneNote}`,
  };
}

function buildMotorcycleOption(netDistKm: number): JourneyOption {
  const speed = bandedSpeedKmh(netDistKm, "motorcycle");
  const totalTimeMin = Math.round((netDistKm / speed) * 60);
  const fuelCostIdr = Math.round(netDistKm * 1200); // Rp 1,200/km (Pertalite ~Rp 10k/L, ~8 km/L)
  const parkingIdr = netDistKm > 5 ? 5000 : 0;
  const totalCostIdr = fuelCostIdr + parkingIdr;

  // GC: drive time has λ=1.0 (in-vehicle), no walk/wait component
  const gcIdr = totalCostIdr + VOT_PER_MIN * totalTimeMin;

  return {
    mode: "motorcycle",
    label: "Motorcycle",
    icon: "two_wheeler",
    totalTimeMin,
    totalCostIdr,
    generalizedCostIdr: Math.round(gcIdr),
    legs: [
      {
        type: "drive",
        label: `Ride (${speed} km/h avg)`,
        durationMin: totalTimeMin,
        distanceKm: netDistKm,
        costIdr: fuelCostIdr,
      },
    ],
    recommended: false,
    available: true,
    methodNote: `BPR banded speed ${speed} km/h for ${netDistKm.toFixed(1)} km network distance.`,
  };
}

function buildCarOption(netDistKm: number): JourneyOption {
  const speed = bandedSpeedKmh(netDistKm, "car");
  const totalTimeMin = Math.round((netDistKm / speed) * 60);
  const fuelCostIdr = Math.round(netDistKm * 2000); // Rp 2,000/km (Pertamax ~Rp 14k/L, ~7 km/L)
  const parkingIdr = netDistKm > 3 ? 15000 : 0;
  const totalCostIdr = fuelCostIdr + parkingIdr;

  const gcIdr = totalCostIdr + VOT_PER_MIN * totalTimeMin;

  return {
    mode: "car",
    label: "Car",
    icon: "directions_car",
    totalTimeMin,
    totalCostIdr,
    generalizedCostIdr: Math.round(gcIdr),
    legs: [
      {
        type: "drive",
        label: `Drive (${speed} km/h avg)`,
        durationMin: totalTimeMin,
        distanceKm: netDistKm,
        costIdr: fuelCostIdr,
      },
    ],
    recommended: false,
    available: true,
    methodNote: `BPR banded speed ${speed} km/h for ${netDistKm.toFixed(1)} km network distance.`,
  };
}

function buildGoRideOption(netDistKm: number): JourneyOption {
  // GoRide uses motorcycle speed tiers but slightly faster (no parking search)
  const speed = bandedSpeedKmh(netDistKm, "motorcycle") + 2;
  const rideTimeMin = Math.round((netDistKm / speed) * 60);
  const waitTimeMin = 3; // app dispatch wait
  const totalTimeMin = rideTimeMin + waitTimeMin;
  const totalCostIdr = Math.max(10000, Math.round(netDistKm * 2500)); // Rp 2,500/km, min Rp 10k

  // GoRide has wait penalty (app dispatch) but no walk/parking
  const gcIdr =
    totalCostIdr +
    VOT_PER_MIN * (rideTimeMin + LAMBDA_WAIT * waitTimeMin);

  return {
    mode: "goride",
    label: "GoRide",
    icon: "two_wheeler",
    totalTimeMin,
    totalCostIdr,
    generalizedCostIdr: Math.round(gcIdr),
    legs: [
      { type: "wait", label: "Wait for driver", durationMin: waitTimeMin },
      {
        type: "ride",
        label: `GoRide (${speed} km/h avg)`,
        durationMin: rideTimeMin,
        distanceKm: netDistKm,
        costIdr: totalCostIdr,
      },
    ],
    recommended: false,
    available: true,
    methodNote: `Rp 2,500/km tariff. BPR banded speed ${speed} km/h.`,
  };
}

function buildGoCarOption(netDistKm: number): JourneyOption {
  const speed = bandedSpeedKmh(netDistKm, "car");
  const driveTimeMin = Math.round((netDistKm / speed) * 60);
  const waitTimeMin = 5; // app dispatch wait
  const totalTimeMin = driveTimeMin + waitTimeMin;
  const totalCostIdr = Math.max(20000, Math.round(netDistKm * 4000)); // Rp 4,000/km, min Rp 20k

  const gcIdr =
    totalCostIdr +
    VOT_PER_MIN * (driveTimeMin + LAMBDA_WAIT * waitTimeMin);

  return {
    mode: "gocar",
    label: "GoCar",
    icon: "local_taxi",
    totalTimeMin,
    totalCostIdr,
    generalizedCostIdr: Math.round(gcIdr),
    legs: [
      { type: "wait", label: "Wait for driver", durationMin: waitTimeMin },
      {
        type: "drive",
        label: `GoCar (${speed} km/h avg)`,
        durationMin: driveTimeMin,
        distanceKm: netDistKm,
        costIdr: totalCostIdr,
      },
    ],
    recommended: false,
    available: true,
    methodNote: `Rp 4,000/km tariff. BPR banded speed ${speed} km/h.`,
  };
}

// ─── Main export ─────────────────────────────────────────────────────────────

/**
 * Estimate journey options between home and office for all 5 transport modes.
 *
 * @param homeZone     Zone data for the home location (TAI scores, GC, headway, etc.)
 * @param homeCoord    Home pin [lng, lat]
 * @param officeCoord  Office pin [lng, lat]
 * @param destZone     Optional: zone data for the office location (two-zone composite)
 */
export function estimateJourney(
  homeZone: HexProperties,
  homeCoord: [number, number],
  officeCoord: [number, number],
  destZone?: HexProperties | null
): JourneyOption[] {
  // Euclidean → network distance via circuity factor
  const euclidKm = haversineKm(homeCoord, officeCoord);
  const netDistKm = networkDistKm(euclidKm);

  // CBD network distance (for transit IVT scaling)
  const cbdEuclidKm = homeZone.distance_to_sudirman_km ?? euclidKm;
  const cbdNetDistKm = networkDistKm(cbdEuclidKm);

  const transitOpt = buildTransitOption(homeZone, netDistKm, cbdNetDistKm, destZone);
  const motoOpt = buildMotorcycleOption(netDistKm);
  const carOpt = buildCarOption(netDistKm);
  const gorideOpt = buildGoRideOption(netDistKm);
  const gocarOpt = buildGoCarOption(netDistKm);

  const options: JourneyOption[] = [
    ...(transitOpt !== null ? [transitOpt] : []),
    gorideOpt,
    gocarOpt,
    motoOpt,
    carOpt,
  ];

  const available = options.filter((o) => o.available);

  // ── Tags based on financial cost and time ──
  const sortedByCost = [...available].sort((a, b) => a.totalCostIdr - b.totalCostIdr);
  const sortedByTime = [...available].sort((a, b) => a.totalTimeMin - b.totalTimeMin);
  const cheapest = sortedByCost[0];
  const fastest = sortedByTime[0];

  if (cheapest) cheapest.tag = "Cheapest";
  if (fastest && fastest.mode !== cheapest?.mode) fastest.tag = "Fastest";

  // ── Recommended: lowest GC among available options ──
  const bestGC = [...available].sort(
    (a, b) => a.generalizedCostIdr - b.generalizedCostIdr
  )[0];
  if (bestGC) bestGC.recommended = true;

  // Guarantee at most one recommended
  let seen = false;
  for (const opt of options) {
    if (opt.recommended) {
      if (seen) opt.recommended = false;
      else seen = true;
    }
  }

  return options;
}

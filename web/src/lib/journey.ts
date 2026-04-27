/**
 * journey.ts — Commuter journey estimation with Nested Logit mode choice
 *
 * Methodology:
 *   Ortuzar & Willumsen (2011) Ch.7 — Nested logit for correlated alternatives
 *   Ben-Akiva & Lerman (1985) — Discrete Choice Analysis
 *   Small (1992) — Value of time; Wardman (1998) — walk/wait weights
 *   Barthelemy (2011), Boeing (2016) — Network circuity
 *   BPR (1964), Akçelik (1991) — Distance-banded speeds
 *
 * Key distinction from prior GC-only approach:
 *   This model outputs choice PROBABILITIES rather than a single "best" mode.
 *   It accounts for correlation between similar alternatives (e.g. GoRide
 *   and private motorcycle share riding posture/weather exposure) using a
 *   nested logit structure, avoiding the IIA (blue bus/red bus) problem of
 *   multinomial logit.
 *
 * Nesting structure:
 *   Root
 *   ├── Transit Chain Nest (μ_t = 0.50)
 *   │   └── [auto-detected from first/last mile distances]
 *   ├── Two-Wheeler Nest   (μ_w = 0.45)
 *   │   ├── GoRide door-to-door
 *   │   └── Motorcycle (private)
 *   └── Four-Wheeler Nest  (μ_c = 0.60)
 *       ├── GoCar door-to-door
 *       └── Car (private)
 *
 * First/last mile logic:
 *   min_dist_to_transit_m ≤ 500 → walk (free, λ=2.0 weight)
 *   min_dist_to_transit_m > 500 → GoRide feeder (Rp 2,500/km, λ=1.0 weight)
 *
 * DISCLAIMER: Zone-level aggregate estimates — not GTFS trip-planning.
 */

import type { HexProperties } from "./store";

// ─── Types ──────────────────────────────────────────────────────────────────

export type TransportMode =
  | "transit_chain"
  | "goride"
  | "motorcycle"
  | "gocar"
  | "car";

/** Nest membership for logit computation. */
export type NestLabel = "transit" | "two_wheeler" | "four_wheeler";

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
  chainLabel: string; // e.g. "GoRide → KRL → Walk"
  nest: NestLabel;
  icon: string;
  totalTimeMin: number;
  totalCostIdr: number; // Financial cost (displayed to user)
  generalizedCostIdr: number; // GC (for ranking)
  /** Nested logit choice probability [0, 1] — sums to 1 across all options. */
  probability: number;
  legs: JourneyLeg[];
  /** Brief tag for quick scanning: "Cheapest" | "Fastest" */
  tag?: string;
  available: boolean;
  methodNote?: string;
}

// ─── Constants ───────────────────────────────────────────────────────────────

const CIRCUITY = 1.35;

/** Value of Time in IDR/min.
 *  BPS 2023 urban median household expenditure Rp 4.5M/month
 *  ÷ 160 working hours → Rp 28,125/hr → Rp 469/min → rounded Rp 500/min. */
const VOT_PER_MIN = 500;

/** Walk time perception — 2× worse than in-vehicle (Wardman 1998). */
const LAMBDA_WALK = 2.0;

/** Wait time perception — 2.5× worse than in-vehicle (Wardman 1998). */
const LAMBDA_WAIT = 2.5;

/** Walking speed — m/min (TCQSM 2013). */
const WALK_SPEED_MPM = 80;

/** Distance threshold for walk vs GoRide first/last mile (metres). */
const WALK_LASTMILE_THRESHOLD_M = 500;

/** GoRide feeder cost per km (Rp). */
const GORIDE_FEEDER_RATE = 2500;

/** GoRide door-to-door cost per km (Rp). */
const GORIDE_RATE = 2500;

/** GoCar cost per km (Rp). */
const GOCAR_RATE = 4000;

/** Private motorcycle fuel cost per km (Rp). Pertalite ~Rp 10k/L, ~8 km/L. */
const MOTO_FUEL_RATE = 1200;

/** Private car fuel cost per km (Rp). Pertamax ~Rp 14k/L, ~7 km/L. */
const CAR_FUEL_RATE = 2000;

/** GoRide minimum fare (Rp). */
const GORIDE_MIN_FARE = 10000;

/** GoCar minimum fare (Rp). */
const GOCAR_MIN_FARE = 20000;

/** App dispatch wait for GoRide (min). */
const GORIDE_DISPATCH_MIN = 3;

/** App dispatch wait for GoCar (min). */
const GOCAR_DISPATCH_MIN = 5;

/** Car CBD parking (Rp). */
const CAR_PARKING = 15000;

/** Motorcycle CBD parking (Rp). */
const MOTO_PARKING = 5000;

/** Default last-mile walk at destination (min) — when station ≤500m from office. */
const DEFAULT_LASTMILE_WALK_MIN = 5;

// Nest dissimilarity parameters (Ortuzar & Willumsen 2011, Ch.7; Hensher et al. 2015)
// μ ∈ (0, 1]. Lower μ → stronger within-nest correlation. μ = 1 collapses to MNL.
const MU_TRANSIT = 0.50; // transit chains share schedule/crowding unobservables
const MU_TWO_WHEELER = 0.45; // GoRide + private motorcycle share riding posture, weather exposure
const MU_FOUR_WHEELER = 0.60; // GoCar + private car share comfort but differ on parking/ownership

// Scale for utility computation (normalises GC to reasonable exp values).
const UTILITY_SCALE = 1000;

// ─── Helpers ─────────────────────────────────────────────────────────────────

function haversineKm(a: [number, number], b: [number, number]): number {
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

function networkDistKm(euclideanKm: number): number {
  return euclideanKm * CIRCUITY;
}

/** BPR distance-banded speed (km/h). From BPTJ (2022) Jakarta peak-hour survey. */
function bandedSpeedKmh(netDistKm: number, mode: "motorcycle" | "car"): number {
  if (mode === "motorcycle") {
    if (netDistKm < 5) return 22;
    if (netDistKm < 15) return 30;
    return 38;
  }
  // car
  if (netDistKm < 5) return 18;
  if (netDistKm < 15) return 25;
  return 32;
}

/** Transfer penalty in equivalent minutes (distance-band proxy). */
function transferPenaltyMin(netDistKm: number): number {
  if (netDistKm < 5) return 0;
  if (netDistKm < 15) return 10;
  return 20;
}

/** Compute GC from components using the standard formula. */
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
      (ivtMin + LAMBDA_WALK * walkMin + LAMBDA_WAIT * waitMin + transferPenMin)
  );
}

/** Systematic utility: higher = better (negative normalised GC). */
function utility(gcIdr: number): number {
  return -gcIdr / UTILITY_SCALE;
}

// ─── First / Last Mile Detection ─────────────────────────────────────────────

function buildFirstMile(
  minDistToTransitM: number | null | undefined,
  netDistToStationKm: number
): { legs: JourneyLeg[]; gcIdr: number; label: string } {
  const distM = minDistToTransitM ?? 1000;
  if (distM <= WALK_LASTMILE_THRESHOLD_M) {
    const walkMin = distM / WALK_SPEED_MPM;
    const gc = VOT_PER_MIN * LAMBDA_WALK * walkMin; // no fare
    return {
      legs: [
        {
          type: "walk",
          label: `Walk to station (${Math.round(distM)}m)`,
          durationMin: Math.round(walkMin),
          distanceKm: distM / 1000,
          costIdr: 0,
        },
      ],
      gcIdr: Math.round(gc),
      label: "Walk",
    };
  }
  // GoRide feeder
  const rideTimeMin = Math.round((netDistToStationKm / 30) * 60); // 30 km/h avg for short feeder
  const waitTimeMin = GORIDE_DISPATCH_MIN;
  const fare = Math.round(netDistToStationKm * GORIDE_FEEDER_RATE);
  const gc =
    fare +
    VOT_PER_MIN * (rideTimeMin + LAMBDA_WAIT * waitTimeMin);
  return {
    legs: [
      {
        type: "wait",
        label: "Wait for GoRide",
        durationMin: waitTimeMin,
      },
      {
        type: "ride",
        label: `GoRide to station (${netDistToStationKm.toFixed(1)} km)`,
        durationMin: rideTimeMin,
        distanceKm: netDistToStationKm,
        costIdr: fare,
      },
    ],
    gcIdr: Math.round(gc),
    label: "GoRide",
  };
}

function buildLastMile(
  minDistToTransitM: number | null | undefined,
  netDistFromStationKm: number
): { legs: JourneyLeg[]; gcIdr: number; label: string } {
  const distM = minDistToTransitM ?? 200;
  if (distM <= WALK_LASTMILE_THRESHOLD_M) {
    const walkMin = Math.max(3, distM / WALK_SPEED_MPM);
    const gc = VOT_PER_MIN * LAMBDA_WALK * walkMin;
    return {
      legs: [
        {
          type: "walk",
          label: `Walk to office (${Math.round(distM)}m)`,
          durationMin: Math.round(walkMin),
          distanceKm: distM / 1000,
          costIdr: 0,
        },
      ],
      gcIdr: Math.round(gc),
      label: "Walk",
    };
  }
  // GoRide from station
  const rideTimeMin = Math.round((netDistFromStationKm / 30) * 60);
  const waitTimeMin = GORIDE_DISPATCH_MIN;
  const fare = Math.round(netDistFromStationKm * GORIDE_FEEDER_RATE);
  const gc =
    fare +
    VOT_PER_MIN * (rideTimeMin + LAMBDA_WAIT * waitTimeMin);
  return {
    legs: [
      {
        type: "wait",
        label: "Wait for GoRide",
        durationMin: waitTimeMin,
      },
      {
        type: "ride",
        label: `GoRide to office (${netDistFromStationKm.toFixed(1)} km)`,
        durationMin: rideTimeMin,
        distanceKm: netDistFromStationKm,
        costIdr: fare,
      },
    ],
    gcIdr: Math.round(gc),
    label: "GoRide",
  };
}

// ─── Mode Builders ────────────────────────────────────────────────────────────

interface TransitChainResult {
  option: JourneyOption;
  gcIdr: number;
}

function buildTransitChain(
  homeZone: HexProperties,
  officeDistKm: number, // euclidean origin→dest
  cbdDistKm: number, // euclidean origin→CBD (for IVT scaling)
  destZone?: HexProperties | null
): TransitChainResult | null {
  if (
    homeZone.gc_transit_idr == null ||
    homeZone.poi_reach_cbd_min == null
  ) {
    return null;
  }

  const available =
    homeZone.transit_competitive_zone !== "transit_not_available";

  const netDistKm = networkDistKm(officeDistKm);
  const cbdNetDistKm = networkDistKm(Math.max(cbdDistKm, 0.5));
  const ivtScale = netDistKm / Math.max(cbdNetDistKm, 0.5);

  // ── First mile ──
  const distToStationKm = (homeZone.min_dist_to_transit_m ?? 500) / 1000;
  const firstMile = buildFirstMile(
    homeZone.min_dist_to_transit_m,
    Math.max(distToStationKm, 0.05)
  );

  // ── Transit ride (IVT) ──
  const homeHeadway = homeZone.avg_headway_min ?? 15;
  const destHeadway = destZone?.avg_headway_min ?? homeHeadway;
  const effectiveHeadway = Math.max(homeHeadway, destHeadway);
  const waitTimeMin = effectiveHeadway / 2;

  const walkToStationMin =
    (homeZone.min_dist_to_transit_m ?? 500) <= WALK_LASTMILE_THRESHOLD_M
      ? (homeZone.min_dist_to_transit_m ?? 500) / WALK_SPEED_MPM
      : 1; // ojek feeder — negligible station-side walk

  const cbdIVT = Math.max(
    5,
    (homeZone.poi_reach_cbd_min ?? 60) - walkToStationMin - waitTimeMin
  );
  const ivtMin = cbdIVT * ivtScale;

  const transferMin = transferPenaltyMin(netDistKm);
  const fareIdr = Math.round(
    Math.max(3500, (homeZone.est_cbd_journey_fare_idr ?? 3500) * ivtScale)
  );

  // ── Last mile ──
  const distFromStationKm =
    destZone?.min_dist_to_transit_m != null
      ? destZone.min_dist_to_transit_m / 1000
      : 0.5;
  const lastMile = buildLastMile(
    destZone?.min_dist_to_transit_m,
    Math.max(distFromStationKm, 0.05)
  );

  // ── Assemble chain ──
  const allLegs = [
    ...firstMile.legs,
    {
      type: "wait" as const,
      label: `Wait for transit (~${effectiveHeadway} min headway)`,
      durationMin: Math.round(waitTimeMin),
    },
    ...(transferMin > 0
      ? [
          {
            type: "wait" as const,
            label: `Transfer${netDistKm < 15 ? " (×1)" : " (×2)"}`,
            durationMin: transferMin,
          },
        ]
      : []),
    {
      type: "ride" as const,
      label: "Transit ride",
      durationMin: Math.round(ivtMin),
      distanceKm: Math.round(netDistKm * 0.85 * 10) / 10,
      costIdr: fareIdr,
    },
    ...lastMile.legs,
  ];

  const totalTimeMin = allLegs.reduce((s, l) => s + l.durationMin, 0);
  const totalCostIdr =
    firstMile.legs.reduce((s, l) => s + (l.costIdr ?? 0), 0) +
    fareIdr +
    lastMile.legs.reduce((s, l) => s + (l.costIdr ?? 0), 0);

  // GC for the entire chain
  const gcRide = computeGC(fareIdr, ivtMin, 0, waitTimeMin, transferMin);
  const gcIdr = firstMile.gcIdr + gcRide + lastMile.gcIdr;

  const chainLabel = `${firstMile.label} → Transit → ${lastMile.label}`;

  return {
    gcIdr,
    option: {
      mode: "transit_chain",
      label: "Transit",
      chainLabel,
      nest: "transit",
      icon: "directions_transit",
      totalTimeMin,
      totalCostIdr,
      generalizedCostIdr: Math.round(gcIdr),
      probability: 0, // filled by nested logit
      legs: allLegs,
      available,
      methodNote: `First mile: ${firstMile.label}. Headway: bottleneck of home + dest. GC via nested logit (μ=${MU_TRANSIT}).`,
    },
  };
}

function buildGoRideOption(
  officeDistKm: number
): { option: JourneyOption; gcIdr: number } {
  const netDistKm = networkDistKm(officeDistKm);
  const speed = bandedSpeedKmh(netDistKm, "motorcycle") + 2; // slightly faster — no parking
  const rideTimeMin = Math.round((netDistKm / speed) * 60);
  const waitTimeMin = GORIDE_DISPATCH_MIN;
  const totalTimeMin = rideTimeMin + waitTimeMin;
  const totalCostIdr = Math.max(
    GORIDE_MIN_FARE,
    Math.round(netDistKm * GORIDE_RATE)
  );
  const gcIdr =
    totalCostIdr +
    VOT_PER_MIN * (rideTimeMin + LAMBDA_WAIT * waitTimeMin);

  return {
    gcIdr: Math.round(gcIdr),
    option: {
      mode: "goride",
      label: "GoRide",
      chainLabel: "GoRide door-to-door",
      nest: "two_wheeler",
      icon: "two_wheeler",
      totalTimeMin,
      totalCostIdr,
      generalizedCostIdr: Math.round(gcIdr),
      probability: 0,
      legs: [
        {
          type: "wait",
          label: `Wait for driver (${waitTimeMin} min)`,
          durationMin: waitTimeMin,
        },
        {
          type: "ride",
          label: `GoRide (${speed} km/h avg)`,
          durationMin: rideTimeMin,
          distanceKm: netDistKm,
          costIdr: totalCostIdr,
        },
      ],
      available: true,
      methodNote: `Rp ${GORIDE_RATE.toLocaleString("id-ID")}/km tariff. BPR banded speed ${speed} km/h. Nest μ=${MU_TWO_WHEELER}.`,
    },
  };
}

function buildMotorcycleOption(
  officeDistKm: number
): { option: JourneyOption; gcIdr: number } {
  const netDistKm = networkDistKm(officeDistKm);
  const speed = bandedSpeedKmh(netDistKm, "motorcycle");
  const totalTimeMin = Math.round((netDistKm / speed) * 60);
  const fuelCostIdr = Math.round(netDistKm * MOTO_FUEL_RATE);
  const parkingIdr = netDistKm > 5 ? MOTO_PARKING : 0;
  const totalCostIdr = fuelCostIdr + parkingIdr;
  const gcIdr = totalCostIdr + VOT_PER_MIN * totalTimeMin;

  return {
    gcIdr: Math.round(gcIdr),
    option: {
      mode: "motorcycle",
      label: "Motorcycle",
      chainLabel: "Motorcycle door-to-door",
      nest: "two_wheeler",
      icon: "two_wheeler",
      totalTimeMin,
      totalCostIdr,
      generalizedCostIdr: Math.round(gcIdr),
      probability: 0,
      legs: [
        {
          type: "drive",
          label: `Ride (${speed} km/h avg)`,
          durationMin: totalTimeMin,
          distanceKm: netDistKm,
          costIdr: fuelCostIdr,
        },
      ],
      available: true,
      methodNote: `Rp ${MOTO_FUEL_RATE}/km fuel. BPR banded speed ${speed} km/h. Nest μ=${MU_TWO_WHEELER}.`,
    },
  };
}

function buildGoCarOption(
  officeDistKm: number
): { option: JourneyOption; gcIdr: number } {
  const netDistKm = networkDistKm(officeDistKm);
  const speed = bandedSpeedKmh(netDistKm, "car");
  const driveTimeMin = Math.round((netDistKm / speed) * 60);
  const waitTimeMin = GOCAR_DISPATCH_MIN;
  const totalTimeMin = driveTimeMin + waitTimeMin;
  const totalCostIdr = Math.max(
    GOCAR_MIN_FARE,
    Math.round(netDistKm * GOCAR_RATE)
  );
  const gcIdr =
    totalCostIdr +
    VOT_PER_MIN * (driveTimeMin + LAMBDA_WAIT * waitTimeMin);

  return {
    gcIdr: Math.round(gcIdr),
    option: {
      mode: "gocar",
      label: "GoCar",
      chainLabel: "GoCar door-to-door",
      nest: "four_wheeler",
      icon: "local_taxi",
      totalTimeMin,
      totalCostIdr,
      generalizedCostIdr: Math.round(gcIdr),
      probability: 0,
      legs: [
        {
          type: "wait",
          label: `Wait for driver (${waitTimeMin} min)`,
          durationMin: waitTimeMin,
        },
        {
          type: "drive",
          label: `GoCar (${speed} km/h avg)`,
          durationMin: driveTimeMin,
          distanceKm: netDistKm,
          costIdr: totalCostIdr,
        },
      ],
      available: true,
      methodNote: `Rp ${GOCAR_RATE.toLocaleString("id-ID")}/km tariff. BPR banded speed ${speed} km/h. Nest μ=${MU_FOUR_WHEELER}.`,
    },
  };
}

function buildCarOption(
  officeDistKm: number
): { option: JourneyOption; gcIdr: number } {
  const netDistKm = networkDistKm(officeDistKm);
  const speed = bandedSpeedKmh(netDistKm, "car");
  const totalTimeMin = Math.round((netDistKm / speed) * 60);
  const fuelCostIdr = Math.round(netDistKm * CAR_FUEL_RATE);
  const parkingIdr = netDistKm > 3 ? CAR_PARKING : 0;
  const totalCostIdr = fuelCostIdr + parkingIdr;
  const gcIdr = totalCostIdr + VOT_PER_MIN * totalTimeMin;

  return {
    gcIdr: Math.round(gcIdr),
    option: {
      mode: "car",
      label: "Car",
      chainLabel: "Car door-to-door",
      nest: "four_wheeler",
      icon: "directions_car",
      totalTimeMin,
      totalCostIdr,
      generalizedCostIdr: Math.round(gcIdr),
      probability: 0,
      legs: [
        {
          type: "drive",
          label: `Drive (${speed} km/h avg)`,
          durationMin: totalTimeMin,
          distanceKm: netDistKm,
          costIdr: fuelCostIdr,
        },
      ],
      available: true,
      methodNote: `Rp ${CAR_FUEL_RATE}/km fuel + Rp ${CAR_PARKING.toLocaleString("id-ID")} parking. BPR banded speed ${speed} km/h. Nest μ=${MU_FOUR_WHEELER}.`,
    },
  };
}

// ─── Nested Logit Engine ─────────────────────────────────────────────────────

interface NestEntry {
  utility: number;
  mu: number; // dissimilarity parameter for this entry's nest
}

/**
 * Compute nested logit choice probabilities.
 *
 * Structure:
 *   Transit chain   — degenerate nest (single alternative), μ = MU_TRANSIT
 *   Two-wheeler     — {GoRide, Motorcycle},           μ = MU_TWO_WHEELER
 *   Four-wheeler    — {GoCar, Car},                    μ = MU_FOUR_WHEELER
 *
 * Steps:
 *   1. Systematic utility: V_i = -GC_i / UTILITY_SCALE
 *   2. Within-nest conditional probabilities (only for multi-alternative nests)
 *   3. Log-sum (inclusive value) for each nest
 *   4. Marginal nest probabilities
 *   5. Unconditional choice probabilities
 */
function computeNestedLogit(options: JourneyOption[]): JourneyOption[] {
  const available = options.filter((o) => o.available);
  if (available.length === 0) return options;

  // Group by nest
  const transitOpt = available.find((o) => o.nest === "transit");
  const twoWheelers = available.filter((o) => o.nest === "two_wheeler");
  const fourWheelers = available.filter((o) => o.nest === "four_wheeler");

  // Step 1: systematic utilities
  const V = new Map<string, number>();
  for (const opt of available) {
    V.set(opt.mode, utility(opt.generalizedCostIdr));
  }

  // Step 2: within-nest conditional probabilities & log-sums

  // Transit — degenerate nest (single alternative, no within-nest competition)
  const V_t = transitOpt ? V.get(transitOpt.mode)! / MU_TRANSIT : -Infinity;
  const IV_t = V_t; // log(exp(V_t)) = V_t for single alternative

  // Two-wheeler nest
  let IV_w = -Infinity;
  const condProb_w = new Map<string, number>();
  if (twoWheelers.length > 0) {
    let sumExp = 0;
    for (const opt of twoWheelers) {
      const v = Math.exp(V.get(opt.mode)! / MU_TWO_WHEELER);
      condProb_w.set(opt.mode, v);
      sumExp += v;
    }
    for (const opt of twoWheelers) {
      condProb_w.set(opt.mode, condProb_w.get(opt.mode)! / sumExp);
    }
    IV_w = Math.log(Math.max(sumExp, 1e-10)); // inclusive value
  }

  // Four-wheeler nest
  let IV_c = -Infinity;
  const condProb_c = new Map<string, number>();
  if (fourWheelers.length > 0) {
    let sumExp = 0;
    for (const opt of fourWheelers) {
      const v = Math.exp(V.get(opt.mode)! / MU_FOUR_WHEELER);
      condProb_c.set(opt.mode, v);
      sumExp += v;
    }
    for (const opt of fourWheelers) {
      condProb_c.set(opt.mode, condProb_c.get(opt.mode)! / sumExp);
    }
    IV_c = Math.log(Math.max(sumExp, 1e-10));
  }

  // Step 3: marginal nest probabilities
  const denomTransit =
    (transitOpt ? Math.exp(MU_TRANSIT * IV_t) : 0) +
    (twoWheelers.length > 0 ? Math.exp(MU_TWO_WHEELER * IV_w) : 0) +
    (fourWheelers.length > 0 ? Math.exp(MU_FOUR_WHEELER * IV_c) : 0);

  const P_transit = transitOpt
    ? Math.exp(MU_TRANSIT * IV_t) / denomTransit
    : 0;
  const P_twoWheeler =
    twoWheelers.length > 0
      ? Math.exp(MU_TWO_WHEELER * IV_w) / denomTransit
      : 0;
  const P_fourWheeler =
    fourWheelers.length > 0
      ? Math.exp(MU_FOUR_WHEELER * IV_c) / denomTransit
      : 0;

  // Step 4: unconditional choice probabilities
  const probs = new Map<string, number>();
  if (transitOpt) {
    probs.set(transitOpt.mode, P_transit); // degenerate nest: P(mode | nest) = 1
  }
  for (const opt of twoWheelers) {
    probs.set(opt.mode, (condProb_w.get(opt.mode) ?? 0) * P_twoWheeler);
  }
  for (const opt of fourWheelers) {
    probs.set(opt.mode, (condProb_c.get(opt.mode) ?? 0) * P_fourWheeler);
  }

  // Assign probabilities back to options
  for (const opt of options) {
    opt.probability = opt.available ? (probs.get(opt.mode) ?? 0) : 0;
  }

  return options;
}

// ─── Main Export ─────────────────────────────────────────────────────────────

/**
 * Estimate journey options with nested logit mode choice probabilities.
 *
 * @param homeZone    Zone data for the home location.
 * @param homeCoord   Home pin [lng, lat].
 * @param officeCoord Office pin [lng, lat].
 * @param destZone    Optional: zone data for the office location (two-zone composite).
 * @returns 5 mode options sorted by probability descending, each with a
 *          [0,1] `probability` field summing to 1 across available modes.
 */
export function estimateJourney(
  homeZone: HexProperties,
  homeCoord: [number, number],
  officeCoord: [number, number],
  destZone?: HexProperties | null
): JourneyOption[] {
  const euclidKm = haversineKm(homeCoord, officeCoord);
  const netDistKm = networkDistKm(euclidKm);

  const cbdEuclidKm = homeZone.distance_to_sudirman_km ?? euclidKm;

  // Build all five alternatives
  const transitResult = buildTransitChain(
    homeZone,
    euclidKm,
    cbdEuclidKm,
    destZone
  );
  const gorideResult = buildGoRideOption(euclidKm);
  const motoResult = buildMotorcycleOption(euclidKm);
  const gocarResult = buildGoCarOption(euclidKm);
  const carResult = buildCarOption(euclidKm);

  const rawOptions: JourneyOption[] = [
    ...(transitResult ? [transitResult.option] : []),
    gorideResult.option,
    motoResult.option,
    gocarResult.option,
    carResult.option,
  ];

  // Nested logit probabilities
  const options = computeNestedLogit(rawOptions);

  // ── Tags (financial cost / time) ──
  const available = options.filter((o) => o.available);
  const sortedByCost = [...available].sort(
    (a, b) => a.totalCostIdr - b.totalCostIdr
  );
  const sortedByTime = [...available].sort(
    (a, b) => a.totalTimeMin - b.totalTimeMin
  );
  const cheapest = sortedByCost[0];
  const fastest = sortedByTime[0];

  if (cheapest) cheapest.tag = "Cheapest";
  if (fastest && fastest.mode !== cheapest?.mode) fastest.tag = "Fastest";

  // Sort by probability descending
  return options.sort((a, b) => b.probability - a.probability);
}

/**
 * Expose dissimilarity parameters for UI or sensitivity analysis.
 */
export const NEST_PARAMS = {
  mu_transit: MU_TRANSIT,
  mu_two_wheeler: MU_TWO_WHEELER,
  mu_four_wheeler: MU_FOUR_WHEELER,
  utility_scale: UTILITY_SCALE,
};

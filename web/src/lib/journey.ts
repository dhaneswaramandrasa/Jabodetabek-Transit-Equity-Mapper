import type { HexProperties } from "./store";

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
  totalCostIdr: number;
  legs: JourneyLeg[];
  recommended: boolean;
  tag?: string;
  available: boolean;
}

// Standard haversine — expects [lng, lat] pairs, returns km
function haversineKm(a: [number, number], b: [number, number]): number {
  const R = 6371;
  const [lng1, lat1] = a;
  const [lng2, lat2] = b;
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLng = ((lng2 - lng1) * Math.PI) / 180;
  const sinDLat = Math.sin(dLat / 2);
  const sinDLng = Math.sin(dLng / 2);
  const aVal =
    sinDLat * sinDLat +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      sinDLng *
      sinDLng;
  return R * 2 * Math.atan2(Math.sqrt(aVal), Math.sqrt(1 - aVal));
}

function buildTransitOption(
  homeZone: HexProperties,
  distKm: number,
  scale: number
): JourneyOption | null {
  if (
    homeZone.gc_transit_idr == null ||
    homeZone.poi_reach_cbd_min == null
  ) {
    return null;
  }

  const available =
    homeZone.transit_competitive_zone !== "transit_not_available";

  const totalTimeMin = Math.round((homeZone.poi_reach_cbd_min ?? 60) * scale);
  const totalCostIdr = Math.round((homeZone.gc_transit_idr ?? 10000) * scale);

  const walkDistM = homeZone.min_dist_to_transit_m ?? 500;
  const walkLeg: JourneyLeg = {
    type: "walk",
    label: "Walk to stop",
    durationMin: Math.round(walkDistM / 80),
    distanceKm: walkDistM / 1000,
  };
  const waitLeg: JourneyLeg = {
    type: "wait",
    label: "Wait for transit",
    durationMin: Math.round((homeZone.avg_headway_min ?? 15) / 2),
  };
  const rideDuration = Math.max(
    5,
    totalTimeMin - walkLeg.durationMin - waitLeg.durationMin - 5
  );
  const rideLeg: JourneyLeg = {
    type: "ride",
    label: "Transit ride",
    durationMin: rideDuration,
    distanceKm: distKm * 0.85,
    costIdr: homeZone.est_cbd_journey_fare_idr ?? 3500,
  };
  const lastMileLeg: JourneyLeg = {
    type: "walk",
    label: "Walk to destination",
    durationMin: 5,
    distanceKm: 0.4,
  };

  return {
    mode: "transit",
    label: "Transit",
    icon: "directions_transit",
    totalTimeMin,
    totalCostIdr,
    legs: [walkLeg, waitLeg, rideLeg, lastMileLeg],
    recommended: false,
    available,
  };
}

function buildMotorcycleOption(distKm: number): JourneyOption {
  const totalTimeMin = Math.round((distKm / 30) * 60);
  const parkingCost = distKm > 5 ? 5000 : 0;
  const totalCostIdr = Math.round(distKm * 1200 + parkingCost);

  return {
    mode: "motorcycle",
    label: "Motorcycle",
    icon: "two_wheeler",
    totalTimeMin,
    totalCostIdr,
    legs: [
      {
        type: "drive",
        label: "Ride to destination",
        durationMin: totalTimeMin,
        distanceKm: distKm,
      },
    ],
    recommended: false,
    available: true,
  };
}

function buildCarOption(distKm: number): JourneyOption {
  const totalTimeMin = Math.round((distKm / 25) * 60);
  const parkingCost = distKm > 3 ? 15000 : 0;
  const totalCostIdr = Math.round(distKm * 2000 + parkingCost);

  return {
    mode: "car",
    label: "Car",
    icon: "directions_car",
    totalTimeMin,
    totalCostIdr,
    legs: [
      {
        type: "drive",
        label: "Drive to destination",
        durationMin: totalTimeMin,
        distanceKm: distKm,
      },
    ],
    recommended: false,
    available: true,
  };
}

function buildGoRideOption(distKm: number): JourneyOption {
  const rideTime = Math.round((distKm / 32) * 60);
  const totalTimeMin = rideTime + 3;
  const totalCostIdr = Math.max(10000, Math.round(distKm * 2500));

  return {
    mode: "goride",
    label: "GoRide",
    icon: "two_wheeler",
    totalTimeMin,
    totalCostIdr,
    legs: [
      { type: "wait", label: "Wait for driver", durationMin: 3 },
      {
        type: "ride",
        label: "GoRide",
        durationMin: rideTime,
        distanceKm: distKm,
        costIdr: totalCostIdr,
      },
    ],
    recommended: false,
    available: true,
  };
}

function buildGoCarOption(distKm: number): JourneyOption {
  const driveTime = Math.round((distKm / 25) * 60);
  const totalTimeMin = driveTime + 5;
  const totalCostIdr = Math.max(20000, Math.round(distKm * 4000));

  return {
    mode: "gocar",
    label: "GoCar",
    icon: "local_taxi",
    totalTimeMin,
    totalCostIdr,
    legs: [
      { type: "wait", label: "Wait for driver", durationMin: 5 },
      {
        type: "drive",
        label: "GoCar",
        durationMin: driveTime,
        distanceKm: distKm,
        costIdr: totalCostIdr,
      },
    ],
    recommended: false,
    available: true,
  };
}

export function estimateJourney(
  homeZone: HexProperties,
  homeCoord: [number, number],
  officeCoord: [number, number]
): JourneyOption[] {
  const distKm = haversineKm(homeCoord, officeCoord);
  const cbdDistKm = homeZone.distance_to_sudirman_km ?? distKm;
  const scale = distKm / Math.max(cbdDistKm, 0.5);

  const transitOpt = buildTransitOption(homeZone, distKm, scale);
  const motoOpt = buildMotorcycleOption(distKm);
  const carOpt = buildCarOption(distKm);
  const gorideOpt = buildGoRideOption(distKm);
  const gocarOpt = buildGoCarOption(distKm);

  const options: JourneyOption[] = [
    ...(transitOpt !== null ? [transitOpt] : []),
    gorideOpt,
    gocarOpt,
    motoOpt,
    carOpt,
  ];

  const available = options.filter((o) => o.available);

  // Find cheapest among available
  const sortedByCost = [...available].sort(
    (a, b) => a.totalCostIdr - b.totalCostIdr
  );
  const sortedByTime = [...available].sort(
    (a, b) => a.totalTimeMin - b.totalTimeMin
  );
  const cheapest = sortedByCost[0];
  const fastest = sortedByTime[0];

  if (cheapest) {
    cheapest.tag = "Cheapest";
  }
  if (fastest && fastest.mode !== cheapest?.mode) {
    fastest.tag = "Fastest";
  }

  // Best value: lowest cost among options within 1.5x transit time
  const transitTime =
    transitOpt?.available && transitOpt.totalTimeMin
      ? transitOpt.totalTimeMin
      : Infinity;
  const timeThreshold = transitTime * 1.5;
  const withinTime = available.filter((o) => o.totalTimeMin < timeThreshold);
  const bestValue = withinTime.sort((a, b) => a.totalCostIdr - b.totalCostIdr)[0];

  // Assign recommended
  if (
    transitOpt?.available &&
    cheapest &&
    transitOpt.totalCostIdr <= cheapest.totalCostIdr * 1.3
  ) {
    transitOpt.recommended = true;
  } else if (!transitOpt?.available) {
    gorideOpt.recommended = true;
  } else if (bestValue) {
    bestValue.recommended = true;
  }

  // Ensure at most one recommended
  let hasRecommended = false;
  for (const opt of options) {
    if (opt.recommended) {
      if (hasRecommended) opt.recommended = false;
      else hasRecommended = true;
    }
  }

  return options;
}

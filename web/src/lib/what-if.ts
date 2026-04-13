import type { EquityQuadrant } from "./store";

// ===== Parameter + Scenario types =====

export interface WhatIfParams {
  mode: "transjakarta" | "krl" | "mrt" | "lrt" | "mikrotrans";
  fareIdr: number;
  headwayMin: number;
  coverageRadiusKm: number;
}

export interface WhatIfRouteScenario {
  id: string;
  type: "route";
  label: string;
  waypoints: [number, number][]; // [lng, lat]
  params: WhatIfParams;
}

export interface WhatIfStationScenario {
  id: string;
  type: "station";
  label: string;
  point: [number, number]; // [lng, lat]
  params: WhatIfParams;
}

export type WhatIfScenario = WhatIfRouteScenario | WhatIfStationScenario;

export interface ZoneImpact {
  h3_index: string;
  population: number;
  oldQuadrant: EquityQuadrant;
  newQuadrant: EquityQuadrant;
  taiDelta: number;
}

export interface WhatIfResult {
  scenarioId: string;
  zonesAffected: number;
  populationAffected: number;
  quadrantChanges: Record<string, number>; // "Q4->Q1": 3
  estimatedGiniDelta: number;
  zoneImpacts: ZoneImpact[];
}

// ===== Geometry helpers =====

/** Haversine distance in km between two [lng, lat] points */
export function haversineKm(
  a: [number, number],
  b: [number, number]
): number {
  const R = 6371;
  const toRad = (deg: number) => (deg * Math.PI) / 180;
  const dLat = toRad(b[1] - a[1]);
  const dLng = toRad(b[0] - a[0]);
  const sinDLat = Math.sin(dLat / 2);
  const sinDLng = Math.sin(dLng / 2);
  const c =
    sinDLat * sinDLat +
    Math.cos(toRad(a[1])) * Math.cos(toRad(b[1])) * sinDLng * sinDLng;
  return R * 2 * Math.atan2(Math.sqrt(c), Math.sqrt(1 - c));
}

/** Minimum distance in km from a point to any segment of a route polyline */
export function pointToRouteDistanceKm(
  point: [number, number],
  waypoints: [number, number][]
): number {
  if (waypoints.length === 0) return Infinity;
  if (waypoints.length === 1) return haversineKm(point, waypoints[0]);

  let minDist = Infinity;
  for (let i = 0; i < waypoints.length - 1; i++) {
    const segDist = pointToSegmentDistanceKm(point, waypoints[i], waypoints[i + 1]);
    if (segDist < minDist) minDist = segDist;
  }
  return minDist;
}

/** Distance from point P to segment AB, all in [lng, lat] */
function pointToSegmentDistanceKm(
  p: [number, number],
  a: [number, number],
  b: [number, number]
): number {
  const ab = [b[0] - a[0], b[1] - a[1]];
  const ap = [p[0] - a[0], p[1] - a[1]];
  const abLenSq = ab[0] * ab[0] + ab[1] * ab[1];

  if (abLenSq === 0) return haversineKm(p, a);

  const t = Math.max(0, Math.min(1, (ap[0] * ab[0] + ap[1] * ab[1]) / abLenSq));
  const closest: [number, number] = [a[0] + t * ab[0], a[1] + t * ab[1]];
  return haversineKm(p, closest);
}

/** Get approximate centroid of a GeoJSON polygon/multipolygon geometry */
export function getFeatureCentroid(
  geometry: { type: string; coordinates: unknown }
): [number, number] | null {
  if (geometry.type === "Polygon") {
    const ring = (geometry.coordinates as [number, number][][])[0];
    if (!ring || ring.length === 0) return null;
    const sum = ring.reduce(
      (acc, c) => [acc[0] + c[0], acc[1] + c[1]],
      [0, 0]
    );
    return [sum[0] / ring.length, sum[1] / ring.length];
  }
  if (geometry.type === "MultiPolygon") {
    const polys = geometry.coordinates as [number, number][][][];
    const firstRing = polys[0]?.[0];
    if (!firstRing || firstRing.length === 0) return null;
    const sum = firstRing.reduce(
      (acc, c) => [acc[0] + c[0], acc[1] + c[1]],
      [0, 0]
    );
    return [sum[0] / firstRing.length, sum[1] / firstRing.length];
  }
  if (geometry.type === "Point") {
    return geometry.coordinates as [number, number];
  }
  return null;
}

// ===== Quadrant re-classification =====

function classifyQuadrant(tai: number, tni: number): EquityQuadrant {
  if (tai > 0.5 && tni > 0.5) return "Q1";
  if (tai > 0.5 && tni <= 0.5) return "Q2";
  if (tai <= 0.5 && tni > 0.5) return "Q4";
  return "Q3";
}

// ===== Main simulation engine =====

export function computeScenarioImpact(
  scenario: WhatIfScenario,
  features: Array<{
    properties: Record<string, unknown>;
    geometry: Record<string, unknown>;
  }>,
  totalZoneCount: number
): WhatIfResult {
  const { params } = scenario;
  const radius = params.coverageRadiusKm;

  const impacts: ZoneImpact[] = [];
  let populationAffected = 0;
  let improvedCount = 0;
  const quadrantChanges: Record<string, number> = {};

  for (const feature of features) {
    const centroid = getFeatureCentroid(
      feature.geometry as { type: string; coordinates: unknown }
    );
    if (!centroid) continue;

    const dist =
      scenario.type === "route"
        ? pointToRouteDistanceKm(centroid, scenario.waypoints)
        : haversineKm(centroid, scenario.point);

    if (dist > radius) continue;

    const p = feature.properties;
    const taiScore = (p.tai_score as number | null) ?? 0;
    const tniScore = (p.tni_score as number | null) ?? 0;
    const oldQuadrant = (p.quadrant as EquityQuadrant | null) ?? classifyQuadrant(taiScore, tniScore);
    const population = (p.population as number | null) ?? 0;

    const taiL1 = (p.tai_l1_first_mile as number | null) ?? 0;
    const taiL2 = (p.tai_l2_service_quality as number | null) ?? 0;
    const taiL5 = (p.tai_l5_cost_competitiveness as number | null) ?? 0;
    const avgHeadway = (p.avg_headway_min as number | null) ?? 30;
    const fare = (p.est_cbd_journey_fare_idr as number | null) ?? 20000;

    const distanceFactor = Math.max(0, Math.min(1, 1 - dist / radius));

    // L1: first mile improvement
    const l1Delta = Math.min(1 - taiL1, 0.3 * distanceFactor);

    // L2: service frequency improvement
    const headwayRatio = Math.max(
      0,
      (avgHeadway - params.headwayMin) / avgHeadway
    );
    const l2Delta = Math.min(1 - taiL2, headwayRatio * 0.2 * distanceFactor);

    // L5: fare competitiveness improvement
    const fareRatio = Math.max(0, (fare - params.fareIdr) / fare);
    const l5Delta = Math.min(1 - taiL5, fareRatio * 0.15 * distanceFactor);

    const taiDelta = (l1Delta + l2Delta + l5Delta) / 5;
    const newTai = Math.max(0, Math.min(1, taiScore + taiDelta));
    const newQuadrant = classifyQuadrant(newTai, tniScore);

    populationAffected += population;

    if (newQuadrant !== oldQuadrant) {
      const key = `${oldQuadrant}->${newQuadrant}`;
      quadrantChanges[key] = (quadrantChanges[key] ?? 0) + 1;
      improvedCount++;
    }

    impacts.push({
      h3_index: (p.h3_index as string | null) ?? String(Math.random()),
      population,
      oldQuadrant,
      newQuadrant,
      taiDelta,
    });
  }

  const estimatedGiniDelta =
    totalZoneCount > 0 ? -(improvedCount / totalZoneCount) * 0.08 : 0;

  return {
    scenarioId: scenario.id,
    zonesAffected: impacts.length,
    populationAffected,
    quadrantChanges,
    estimatedGiniDelta,
    zoneImpacts: impacts,
  };
}

"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import maplibregl from "maplibre-gl";

// ── Types ──
interface ScenarioData {
  label: string;
  desc: string;
  equity_dir: string;
  mean_dCS_th_idr: number;
  annual_aggregate_bn_idr: number;
  n_winners: number;
  n_losers: number;
  dCS_by_income: Record<string, number>;
  dCS_by_zone: Record<string, number>;
  mode_share_base: Record<string, number>;
  mode_share_policy: Record<string, number>;
  mode_share_delta: Record<string, number>;
}

interface PolicyResults {
  model: string;
  lambda_hat: number;
  beta_cost: number;
  baseline: { cs_mean_th_idr: number; cs_p10: number; cs_p90: number };
  scenarios: Record<string, ScenarioData>;
}

// ── Constants ──
const SCENARIO_KEYS = ["A", "B", "C", "D", "E", "F", "G", "H"] as const;
const MODE_LABELS: Record<string, string> = {
  car: "Car",
  moto: "Moto",
  krl: "KRL",
  tj: "TJ",
  royal: "Royal",
  mrt: "MRT",
};
const MODE_COLORS: Record<string, string> = {
  car: "#64748b",
  moto: "#f59e0b",
  krl: "#028090",
  tj: "#ef4444",
  royal: "#8b5cf6",
  mrt: "#1E2761",
};

const EQUITY_COLORS: Record<string, string> = {
  "pro-equity": "#00A896",
  "strongly pro-equity": "#028090",
  "mildly pro-equity": "#5eead4",
  mixed: "#f59e0b",
  regressive: "#ef4444",
};

// ── Color interpolation for map ──
function interpolateColor(value: number, min: number, max: number): string {
  if (max === min) return "rgb(255,255,255)";
  if (value === 0) return "rgb(245,245,240)";
  if (value < 0) {
    const t = Math.min(1, Math.abs(value) / Math.abs(min));
    const r = Math.round(245 + (239 - 245) * t);
    const g = Math.round(245 + (68 - 245) * t);
    const b = Math.round(240 + (68 - 240) * t);
    return `rgb(${r},${g},${b})`;
  }
  const t = Math.min(1, value / max);
  const r = Math.round(245 + (2 - 245) * t);
  const g = Math.round(245 + (128 - 245) * t);
  const b = Math.round(240 + (144 - 240) * t);
  return `rgb(${r},${g},${b})`;
}

function buildFillColor(
  dCS_by_zone: Record<string, number>
): maplibregl.ExpressionSpecification {
  const values = Object.values(dCS_by_zone);
  const min = Math.min(...values);
  const max = Math.max(...values);

  const stops: (string | maplibregl.ExpressionSpecification)[] = [];
  for (const [zoneId, val] of Object.entries(dCS_by_zone)) {
    stops.push(zoneId);
    stops.push(interpolateColor(val, min, max));
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  return ["match", ["get", "zone_id"], ...stops, "#e5e7eb"] as any;
}

// ── Formatter ──
function fmt(n: number, decimals = 2): string {
  if (Math.abs(n) >= 1000) return n.toLocaleString("en", { maximumFractionDigits: 0 });
  return n.toFixed(decimals);
}

function signedFmt(n: number, decimals = 2): string {
  const prefix = n > 0 ? "+" : "";
  return prefix + fmt(n, decimals);
}

// ── Components ──

function ScenarioButton({
  scKey,
  scenario,
  active,
  onClick,
}: {
  scKey: string;
  scenario: ScenarioData;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left px-3 py-2 rounded-lg border transition-all text-sm ${
        active
          ? "bg-navy text-white border-navy shadow-md"
          : "bg-white text-gray-700 border-gray-200 hover:border-teal hover:shadow-sm"
      }`}
    >
      <span className="font-bold">{scKey}</span>
      <span className="ml-1.5 text-xs opacity-75">
        {scenario.label.replace(`${scKey}: `, "")}
      </span>
      <span
        className={`float-right font-mono text-xs ${
          active
            ? "text-yellow-300"
            : scenario.mean_dCS_th_idr >= 0
            ? "text-teal"
            : "text-red-500"
        }`}
      >
        {signedFmt(scenario.mean_dCS_th_idr)}
      </span>
    </button>
  );
}

function ModeShareBar({
  base,
  policy,
  delta,
}: {
  base: Record<string, number>;
  policy: Record<string, number>;
  delta: Record<string, number>;
}) {
  const modes = Object.keys(base);
  return (
    <div className="space-y-2">
      <div className="text-xs font-bold text-gray-500 uppercase tracking-wider">
        Mode Share Shift
      </div>
      {/* Base bar */}
      <div>
        <div className="text-xs text-gray-400 mb-0.5">Baseline</div>
        <div className="flex h-5 rounded overflow-hidden">
          {modes.map((m) => (
            <div
              key={m}
              style={{
                width: `${base[m] * 100}%`,
                backgroundColor: MODE_COLORS[m],
              }}
              title={`${MODE_LABELS[m]}: ${(base[m] * 100).toFixed(1)}%`}
            />
          ))}
        </div>
      </div>
      {/* Policy bar */}
      <div>
        <div className="text-xs text-gray-400 mb-0.5">Policy</div>
        <div className="flex h-5 rounded overflow-hidden">
          {modes.map((m) => (
            <div
              key={m}
              style={{
                width: `${policy[m] * 100}%`,
                backgroundColor: MODE_COLORS[m],
              }}
              title={`${MODE_LABELS[m]}: ${(policy[m] * 100).toFixed(1)}%`}
            />
          ))}
        </div>
      </div>
      {/* Legend */}
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {modes.map((m) => {
          const d = delta[m] * 100;
          return (
            <div key={m} className="flex items-center gap-1 text-xs">
              <span
                className="w-2.5 h-2.5 rounded-sm inline-block"
                style={{ backgroundColor: MODE_COLORS[m] }}
              />
              <span className="text-gray-600">{MODE_LABELS[m]}</span>
              <span
                className={`font-mono ${
                  d > 0.05
                    ? "text-teal"
                    : d < -0.05
                    ? "text-red-500"
                    : "text-gray-400"
                }`}
              >
                {d > 0 ? "+" : ""}
                {d.toFixed(1)}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function ZoneTable({
  dCS_by_zone,
}: {
  dCS_by_zone: Record<string, number>;
}) {
  const sorted = Object.entries(dCS_by_zone).sort(
    ([, a], [, b]) => b - a
  );
  const max = Math.max(...Object.values(dCS_by_zone).map(Math.abs), 0.01);

  return (
    <div>
      <div className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1.5">
        Welfare by Zone (Th IDR/trip)
      </div>
      <div className="space-y-1">
        {sorted.map(([zone, val]) => (
          <div key={zone} className="flex items-center gap-2 text-xs">
            <span className="w-8 font-bold text-navy">{zone}</span>
            <div className="flex-1 h-4 bg-gray-100 rounded relative overflow-hidden">
              {val !== 0 && (
                <div
                  className={`absolute top-0 h-full rounded ${
                    val > 0 ? "bg-teal/30" : "bg-red-400/30"
                  }`}
                  style={{
                    width: `${(Math.abs(val) / max) * 100}%`,
                    left: val < 0 ? undefined : 0,
                    right: val < 0 ? 0 : undefined,
                  }}
                />
              )}
            </div>
            <span
              className={`w-16 text-right font-mono ${
                val > 0
                  ? "text-teal"
                  : val < 0
                  ? "text-red-500"
                  : "text-gray-400"
              }`}
            >
              {val === 0 ? "0" : signedFmt(val, 2)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Main Page ──
export default function Home() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const popupRef = useRef<maplibregl.Popup | null>(null);
  const [policyData, setPolicyData] = useState<PolicyResults | null>(null);
  const [selectedScenario, setSelectedScenario] = useState<string>("C");
  const [mapReady, setMapReady] = useState(false);
  const selectedScenarioRef = useRef(selectedScenario);

  // Load data
  useEffect(() => {
    fetch("/data/policy_results.json")
      .then((r) => r.json())
      .then(setPolicyData);
  }, []);

  // Initialize map
  useEffect(() => {
    if (!mapContainer.current || mapRef.current) return;

    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          osm: {
            type: "raster",
            tiles: [
              "https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png",
            ],
            tileSize: 256,
            attribution: "&copy; CartoDB &copy; OSM",
          },
        },
        layers: [
          {
            id: "osm",
            type: "raster",
            source: "osm",
          },
        ],
      },
      center: [106.85, -6.55],
      zoom: 9.5,
      maxZoom: 14,
      minZoom: 8,
    });

    map.addControl(new maplibregl.NavigationControl(), "bottom-right");

    map.on("load", () => {
      map.addSource("zones", {
        type: "geojson",
        data: "/data/zones.geojson",
      });

      map.addLayer({
        id: "zone-fill",
        type: "fill",
        source: "zones",
        paint: {
          "fill-color": "#e5e7eb",
          "fill-opacity": 0.75,
        },
      });

      map.addLayer({
        id: "zone-border",
        type: "line",
        source: "zones",
        paint: {
          "line-color": "#1E2761",
          "line-width": [
            "case",
            ["boolean", ["feature-state", "hover"], false],
            3,
            1.5,
          ],
        },
      });

      map.addLayer({
        id: "zone-label",
        type: "symbol",
        source: "zones",
        layout: {
          "text-field": ["get", "zone_id"],
          "text-size": 13,
          "text-font": ["Open Sans Bold"],
          "text-allow-overlap": true,
        },
        paint: {
          "text-color": "#1E2761",
          "text-halo-color": "#ffffff",
          "text-halo-width": 1.5,
        },
      });

      // Hover effect
      let hoveredId: string | null = null;

      map.on("mousemove", "zone-fill", (e) => {
        if (e.features && e.features.length > 0) {
          if (hoveredId !== null) {
            map.setFeatureState(
              { source: "zones", id: hoveredId },
              { hover: false }
            );
          }
          hoveredId = e.features[0].id as string;
          map.setFeatureState(
            { source: "zones", id: hoveredId },
            { hover: true }
          );
          map.getCanvas().style.cursor = "pointer";
        }
      });

      map.on("mouseleave", "zone-fill", () => {
        if (hoveredId !== null) {
          map.setFeatureState(
            { source: "zones", id: hoveredId },
            { hover: false }
          );
        }
        hoveredId = null;
        map.getCanvas().style.cursor = "";
      });

      setMapReady(true);

      // Click popup
      map.on("click", "zone-fill", (e) => {
        if (!e.features || !e.features.length) return;
        const props = e.features[0].properties;
        if (!props) return;

        const zoneId = props.zone_id;
        const zoneName = props.zone_name;
        const pop = Number(props.population).toLocaleString();
        const dcs = props[`dcs_${selectedScenarioRef.current.toLowerCase()}`] || 0;

        // Build transit availability string
        const transit: string[] = [];
        if (props.avail_krl) transit.push("KRL");
        if (props.avail_tj) transit.push("TJ");
        if (props.avail_royal) transit.push("Royal");
        if (props.avail_mrt) transit.push("MRT");
        const transitStr = transit.length ? transit.join(", ") : "None";

        if (popupRef.current) popupRef.current.remove();

        popupRef.current = new maplibregl.Popup({
          closeButton: true,
          maxWidth: "260px",
        })
          .setLngLat(e.lngLat)
          .setHTML(
            `<div style="font-family:Calibri,sans-serif;font-size:13px;">
              <div style="font-weight:bold;font-size:15px;color:#1E2761;margin-bottom:4px;">${zoneId} — ${zoneName}</div>
              <div style="color:#5C6677;margin-bottom:6px;">Pop: ${pop} · Transit: ${transitStr}</div>
              <div style="font-size:18px;font-weight:bold;color:${Number(dcs) >= 0 ? "#028090" : "#ef4444"};">
                ${signedFmt(Number(dcs))} Th IDR/trip
              </div>
            </div>`
          )
          .addTo(map);
      });
    });

    mapRef.current = map;

    return () => map.remove();
  }, []);

  // Keep ref in sync
  useEffect(() => {
    selectedScenarioRef.current = selectedScenario;
  }, [selectedScenario]);

  // Update map colors when scenario changes
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !policyData || !mapReady) return;

    const scenario = policyData.scenarios[selectedScenario];
    if (!scenario) return;

    const fillColor = buildFillColor(scenario.dCS_by_zone);

    try {
      if (map.getLayer("zone-fill")) {
        map.setPaintProperty("zone-fill", "fill-color", fillColor);
      }
    } catch {
      // map not ready yet
    }
  }, [selectedScenario, policyData, mapReady]);

  const scenario = policyData?.scenarios[selectedScenario];

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <header className="bg-navy-deep text-white px-6 py-3 flex items-center justify-between shrink-0">
        <div>
          <h1 className="text-lg font-bold tracking-tight">
            Mode Choice & Policy Welfare in Jabodetabek
          </h1>
          <p className="text-xs text-gray-300 mt-0.5">
            Nested Logit (lambda = 0.763) · 7 zones · 6 modes · 8 policy
            scenarios · Logsum consumer surplus
          </p>
        </div>
        <div className="text-right text-xs text-gray-400">
          <div>Transportation Engineering · Hiroshima University</div>
          <div>Dhaneswaramandrasa · AY2026</div>
        </div>
      </header>

      {/* Main content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Map */}
        <div className="flex-1 relative">
          <div ref={mapContainer} className="absolute inset-0" />

          {/* Legend */}
          {scenario && (
            <div className="absolute bottom-8 left-4 bg-white/95 backdrop-blur rounded-lg shadow-lg px-3 py-2 text-xs">
              <div className="font-bold text-navy mb-1">
                Delta CS (Th IDR/trip)
              </div>
              <div className="flex items-center gap-1">
                <span className="text-red-500">
                  {fmt(
                    Math.min(...Object.values(scenario.dCS_by_zone)),
                    1
                  )}
                </span>
                <div className="flex h-3">
                  {[
                    "rgb(239,68,68)",
                    "rgb(252,165,165)",
                    "rgb(245,245,240)",
                    "rgb(153,216,201)",
                    "rgb(2,128,144)",
                  ].map((c, i) => (
                    <div
                      key={i}
                      className="w-6 h-full"
                      style={{ backgroundColor: c }}
                    />
                  ))}
                </div>
                <span className="text-teal">
                  +
                  {fmt(
                    Math.max(...Object.values(scenario.dCS_by_zone)),
                    1
                  )}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <aside className="w-[380px] bg-white border-l border-gray-200 flex flex-col overflow-hidden shrink-0">
          {/* Scenario picker */}
          <div className="p-4 border-b border-gray-100">
            <div className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">
              Select Policy Scenario
            </div>
            <div className="grid grid-cols-2 gap-1.5">
              {policyData &&
                SCENARIO_KEYS.map((k) => (
                  <ScenarioButton
                    key={k}
                    scKey={k}
                    scenario={policyData.scenarios[k]}
                    active={selectedScenario === k}
                    onClick={() => setSelectedScenario(k)}
                  />
                ))}
            </div>
          </div>

          {/* Scenario details */}
          {scenario && (
            <div className="flex-1 overflow-y-auto sidebar-scroll p-4 space-y-5">
              {/* Summary card */}
              <div className="bg-cream rounded-lg p-3 space-y-2">
                <div className="font-bold text-navy text-sm">
                  {scenario.label}
                </div>
                <div className="text-xs text-gray-600">{scenario.desc}</div>

                <div className="grid grid-cols-2 gap-2 mt-2">
                  <div>
                    <div className="text-xs text-gray-400">Mean Delta CS</div>
                    <div
                      className={`text-lg font-bold font-mono ${
                        scenario.mean_dCS_th_idr >= 0
                          ? "text-teal"
                          : "text-red-500"
                      }`}
                    >
                      {signedFmt(scenario.mean_dCS_th_idr)}
                    </div>
                    <div className="text-xs text-gray-400">Th IDR/trip</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-400">Annual Welfare</div>
                    <div
                      className={`text-lg font-bold font-mono ${
                        scenario.annual_aggregate_bn_idr >= 0
                          ? "text-teal"
                          : "text-red-500"
                      }`}
                    >
                      {signedFmt(scenario.annual_aggregate_bn_idr, 0)}
                    </div>
                    <div className="text-xs text-gray-400">Bn IDR/year</div>
                  </div>
                </div>

                <div className="flex items-center justify-between mt-1 pt-2 border-t border-gray-200">
                  <div className="text-xs">
                    <span className="text-gray-400">Winners: </span>
                    <span className="font-bold text-navy">
                      {scenario.n_winners.toLocaleString()}
                    </span>
                    <span className="text-gray-400"> / 5,000</span>
                  </div>
                  <span
                    className="text-xs font-bold px-2 py-0.5 rounded-full"
                    style={{
                      backgroundColor:
                        (EQUITY_COLORS[scenario.equity_dir] || "#9ca3af") + "20",
                      color:
                        EQUITY_COLORS[scenario.equity_dir] || "#6b7280",
                    }}
                  >
                    {scenario.equity_dir}
                  </span>
                </div>
              </div>

              {/* Income breakdown */}
              <div>
                <div className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-1.5">
                  Welfare by Income
                </div>
                <div className="flex gap-2">
                  {Object.entries(scenario.dCS_by_income).map(
                    ([seg, val]) => (
                      <div
                        key={seg}
                        className="flex-1 bg-cream rounded p-2 text-center"
                      >
                        <div className="text-xs text-gray-500 capitalize">
                          {seg}
                        </div>
                        <div
                          className={`text-sm font-bold font-mono ${
                            val >= 0 ? "text-teal" : "text-red-500"
                          }`}
                        >
                          {signedFmt(val, 2)}
                        </div>
                      </div>
                    )
                  )}
                </div>
              </div>

              {/* Mode share */}
              <ModeShareBar
                base={scenario.mode_share_base}
                policy={scenario.mode_share_policy}
                delta={scenario.mode_share_delta}
              />

              {/* Zone table */}
              <ZoneTable dCS_by_zone={scenario.dCS_by_zone} />
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}

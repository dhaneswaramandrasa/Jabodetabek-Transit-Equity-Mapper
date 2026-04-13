"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useAccessibilityStore } from "@/lib/store";
import { computeScenarioImpact, type WhatIfScenario } from "@/lib/what-if";
import WhatIfParamsPanel from "@/components/WhatIfParams";
import WhatIfResultsPanel from "@/components/WhatIfResults";

const MODE_LABELS: Record<string, string> = {
  transjakarta: "TransJakarta",
  krl: "KRL",
  mrt: "MRT",
  lrt: "LRT",
  mikrotrans: "Mikrotrans",
};

interface Props {
  onClose: () => void;
}

export default function WhatIfSimulator({ onClose }: Props) {
  const {
    whatIfSimMode, setWhatIfSimMode,
    whatIfIsPlacing, setWhatIfIsPlacing,
    whatIfWaypoints, clearWhatIfWaypoints,
    whatIfStationPoint, setWhatIfStationPoint,
    whatIfParams,
    whatIfScenarios, addWhatIfScenario,
    whatIfCurrentResult, setWhatIfCurrentResult,
    setWhatIfHighlightedZones,
  } = useAccessibilityStore();

  const [simLoading, setSimLoading] = useState(false);

  const canSimulate =
    whatIfSimMode === "route"
      ? whatIfWaypoints.length >= 2
      : whatIfStationPoint !== null;

  async function handleSimulate() {
    setSimLoading(true);
    try {
      const res = await fetch("/data/kelurahan_scores.geojson");
      const geojson = await res.json() as {
        features: Array<{
          properties: Record<string, unknown>;
          geometry: Record<string, unknown>;
        }>;
      };

      const scenario: WhatIfScenario =
        whatIfSimMode === "route"
          ? {
              id: `route-${Date.now()}`,
              type: "route",
              label: `${MODE_LABELS[whatIfParams.mode]} Route`,
              waypoints: whatIfWaypoints,
              params: whatIfParams,
            }
          : {
              id: `station-${Date.now()}`,
              type: "station",
              label: `${MODE_LABELS[whatIfParams.mode]} Station`,
              point: whatIfStationPoint!,
              params: whatIfParams,
            };

      const result = computeScenarioImpact(
        scenario,
        geojson.features,
        geojson.features.length
      );
      setWhatIfCurrentResult(result);
      setWhatIfHighlightedZones(
        new Set(result.zoneImpacts.map((z) => z.h3_index))
      );
    } catch (err) {
      console.error("What-if simulation failed:", err);
    } finally {
      setSimLoading(false);
    }
  }

  function handleSaveScenario() {
    if (!whatIfCurrentResult) return;
    const timestamp = new Date().toLocaleTimeString();
    const scenario: WhatIfScenario =
      whatIfSimMode === "route"
        ? {
            id: whatIfCurrentResult.scenarioId,
            type: "route",
            label: `${MODE_LABELS[whatIfParams.mode]} Route (${timestamp})`,
            waypoints: whatIfWaypoints,
            params: whatIfParams,
          }
        : {
            id: whatIfCurrentResult.scenarioId,
            type: "station",
            label: `${MODE_LABELS[whatIfParams.mode]} Station (${timestamp})`,
            point: whatIfStationPoint!,
            params: whatIfParams,
          };
    addWhatIfScenario(scenario);
  }

  function handleClear() {
    clearWhatIfWaypoints();
    setWhatIfStationPoint(null);
    setWhatIfCurrentResult(null);
    setWhatIfHighlightedZones(new Set());
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{ duration: 0.22 }}
      className="absolute bottom-24 left-4 z-30 w-80 bg-white/95 dark:bg-dark-low/95 backdrop-blur-md border border-slate-200 dark:border-white/10 rounded-2xl shadow-xl overflow-hidden"
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-100 dark:border-white/10">
        <div>
          <h3 className="text-sm font-semibold text-slate-800 dark:text-[#e2e0fc]">
            What-If Simulator
          </h3>
          <p className="text-[9px] text-amber-500 font-medium mt-0.5">
            Scenario simulation — not a prediction
          </p>
        </div>
        <button
          onClick={onClose}
          className="text-slate-400 hover:text-slate-600 dark:hover:text-white text-xs px-2 py-1 rounded-lg hover:bg-slate-100 dark:hover:bg-white/10 transition-colors"
        >
          ✕
        </button>
      </div>

      <div className="p-4 space-y-4 max-h-[500px] overflow-y-auto">
        {/* Mode toggle */}
        <div className="flex gap-1 bg-slate-100 dark:bg-white/5 rounded-xl p-1">
          {(["route", "station"] as const).map((m) => (
            <button
              key={m}
              onClick={() => setWhatIfSimMode(m)}
              className={`flex-1 py-1.5 text-[11px] font-semibold rounded-lg transition-colors ${
                whatIfSimMode === m
                  ? "bg-white dark:bg-dark-container text-indigo-600 dark:text-indigo-400 shadow-sm"
                  : "text-slate-500 dark:text-[#c8c5cd] hover:text-slate-700"
              }`}
            >
              {m === "route" ? "Route Mode" : "Station Mode"}
            </button>
          ))}
        </div>

        <WhatIfParamsPanel />

        {/* Drawing controls */}
        <div className="space-y-2">
          <p className="text-[10px] font-semibold text-slate-400 dark:text-[#c8c5cd] uppercase tracking-wide">
            {whatIfSimMode === "route" ? "Route Waypoints" : "Station Point"}
          </p>

          {whatIfSimMode === "route" ? (
            <>
              <div
                className={`text-[11px] text-center py-2 px-3 rounded-lg border transition-colors ${
                  whatIfIsPlacing
                    ? "bg-indigo-50 dark:bg-indigo-950/40 border-indigo-300 dark:border-indigo-600 text-indigo-600 dark:text-indigo-400"
                    : "bg-slate-50 dark:bg-white/5 border-slate-200 dark:border-white/10 text-slate-500 dark:text-[#c8c5cd]"
                }`}
              >
                {whatIfIsPlacing
                  ? `Placing... ${whatIfWaypoints.length} waypoint(s) added`
                  : "Enable placing to add waypoints"}
              </div>
              {whatIfWaypoints.length > 0 && (
                <div className="space-y-0.5 max-h-20 overflow-y-auto">
                  {whatIfWaypoints.map((w, i) => (
                    <div
                      key={i}
                      className="text-[9px] font-mono text-slate-400 dark:text-[#c8c5cd] px-2"
                    >
                      {i + 1}. {w[0].toFixed(4)}, {w[1].toFixed(4)}
                    </div>
                  ))}
                </div>
              )}
            </>
          ) : (
            <div
              className={`text-[11px] text-center py-2 px-3 rounded-lg border transition-colors ${
                whatIfStationPoint
                  ? "bg-emerald-50 dark:bg-emerald-950/40 border-emerald-300 dark:border-emerald-600 text-emerald-600 dark:text-emerald-400"
                  : "bg-slate-50 dark:bg-white/5 border-slate-200 dark:border-white/10 text-slate-500 dark:text-[#c8c5cd]"
              }`}
            >
              {whatIfStationPoint
                ? `Station at ${whatIfStationPoint[0].toFixed(4)}, ${whatIfStationPoint[1].toFixed(4)}`
                : whatIfIsPlacing
                ? "Click map to place station"
                : "Enable placing to position station"}
            </div>
          )}

          <div className="flex gap-2">
            <button
              onClick={() => setWhatIfIsPlacing(!whatIfIsPlacing)}
              className={`flex-1 text-[11px] font-semibold py-1.5 rounded-lg border transition-colors ${
                whatIfIsPlacing
                  ? "bg-indigo-500 text-white border-indigo-600"
                  : "bg-white dark:bg-dark-container border-slate-200 dark:border-white/10 text-slate-600 dark:text-[#e2e0fc] hover:border-indigo-300"
              }`}
            >
              {whatIfIsPlacing ? "Stop Placing" : "Start Placing"}
            </button>
            <button
              onClick={handleClear}
              className="px-3 text-[11px] text-slate-400 dark:text-[#c8c5cd] border border-slate-200 dark:border-white/10 rounded-lg hover:bg-slate-50 dark:hover:bg-white/5 transition-colors"
            >
              Clear
            </button>
          </div>

          <button
            onClick={handleSimulate}
            disabled={!canSimulate || simLoading}
            className="w-full py-2 text-[12px] font-semibold bg-indigo-500 hover:bg-indigo-600 disabled:bg-slate-200 dark:disabled:bg-white/10 disabled:text-slate-400 text-white rounded-lg transition-colors"
          >
            {simLoading ? "Simulating..." : "Simulate"}
          </button>
        </div>

        {/* Results + saved scenarios */}
        {whatIfCurrentResult && (
          <WhatIfResultsPanel
            result={whatIfCurrentResult}
            onSave={handleSaveScenario}
          />
        )}

      </div>
    </motion.div>
  );
}

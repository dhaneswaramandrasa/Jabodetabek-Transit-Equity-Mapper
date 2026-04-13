"use client";

import { useAccessibilityStore } from "@/lib/store";
import type { WhatIfResult } from "@/lib/what-if";

const QUADRANT_CHANGE_COLORS: Record<string, string> = {
  "Q4->Q1": "bg-emerald-100 text-emerald-700",
  "Q4->Q2": "bg-blue-100 text-blue-700",
  "Q4->Q3": "bg-amber-100 text-amber-700",
  "Q3->Q1": "bg-emerald-100 text-emerald-700",
  "Q3->Q2": "bg-blue-100 text-blue-700",
  "Q2->Q1": "bg-emerald-100 text-emerald-700",
};

interface Props {
  result: WhatIfResult;
  onSave: () => void;
}

export default function WhatIfResults({ result, onSave }: Props) {
  const { whatIfScenarios, removeWhatIfScenario } = useAccessibilityStore();

  function handleExportJson() {
    const blob = new Blob([JSON.stringify(whatIfScenarios, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "jtem-whatif-scenarios.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <>
      {/* Current result */}
      <div className="space-y-2 border-t border-slate-100 dark:border-white/10 pt-3">
        <p className="text-[10px] font-semibold text-slate-400 dark:text-[#c8c5cd] uppercase tracking-wide">
          Simulation Results
        </p>
        <div className="bg-indigo-50 dark:bg-indigo-950/30 rounded-xl p-3 space-y-1">
          <p className="text-[11px] text-slate-700 dark:text-[#e2e0fc]">
            <span className="font-bold text-indigo-600 dark:text-indigo-400">
              {result.zonesAffected.toLocaleString()}
            </span>{" "}
            zones affected
            {" · "}
            <span className="font-bold text-indigo-600 dark:text-indigo-400">
              {(result.populationAffected / 1000).toFixed(0)}k
            </span>{" "}
            population
          </p>
          <p className="text-[11px] text-slate-600 dark:text-[#c8c5cd]">
            Estimated Gini{" "}
            <span
              className={
                result.estimatedGiniDelta <= 0
                  ? "font-bold text-emerald-600 dark:text-emerald-400"
                  : "font-bold text-red-500"
              }
            >
              {result.estimatedGiniDelta >= 0 ? "+" : ""}
              {result.estimatedGiniDelta.toFixed(3)}
            </span>
          </p>
          {Object.entries(result.quadrantChanges).length > 0 && (
            <div className="flex flex-wrap gap-1 pt-1">
              {Object.entries(result.quadrantChanges).map(([key, count]) => (
                <span
                  key={key}
                  className={`text-[9px] font-semibold px-2 py-0.5 rounded-full ${
                    QUADRANT_CHANGE_COLORS[key] ?? "bg-slate-100 text-slate-600"
                  }`}
                >
                  {key}: {count}
                </span>
              ))}
            </div>
          )}
        </div>
        <button
          onClick={onSave}
          disabled={whatIfScenarios.length >= 3}
          className="w-full py-1.5 text-[11px] font-semibold border border-indigo-300 dark:border-indigo-700 text-indigo-600 dark:text-indigo-400 rounded-lg hover:bg-indigo-50 dark:hover:bg-indigo-950/30 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          {whatIfScenarios.length >= 3 ? "Max 3 scenarios saved" : "Save Scenario"}
        </button>
      </div>

      {/* Saved scenarios */}
      {whatIfScenarios.length > 0 && (
        <div className="space-y-2 border-t border-slate-100 dark:border-white/10 pt-3">
          <p className="text-[10px] font-semibold text-slate-400 dark:text-[#c8c5cd] uppercase tracking-wide">
            Saved Scenarios
          </p>
          <div className="space-y-1">
            {whatIfScenarios.map((s) => (
              <div
                key={s.id}
                className="flex items-center justify-between bg-slate-50 dark:bg-white/5 rounded-lg px-3 py-2"
              >
                <span className="text-[11px] text-slate-700 dark:text-[#e2e0fc] truncate flex-1">
                  {s.label}
                </span>
                <button
                  onClick={() => removeWhatIfScenario(s.id)}
                  className="ml-2 text-slate-400 hover:text-red-500 text-[10px] transition-colors"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
          <button
            onClick={handleExportJson}
            className="w-full py-1.5 text-[11px] font-semibold border border-slate-200 dark:border-white/10 text-slate-600 dark:text-[#e2e0fc] rounded-lg hover:bg-slate-50 dark:hover:bg-white/5 transition-colors"
          >
            Export All JSON
          </button>
        </div>
      )}
    </>
  );
}

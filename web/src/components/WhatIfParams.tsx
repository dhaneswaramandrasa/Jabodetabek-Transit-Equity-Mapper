"use client";

import { useAccessibilityStore } from "@/lib/store";

const MODE_LABELS: Record<string, string> = {
  transjakarta: "TransJakarta",
  krl: "KRL",
  mrt: "MRT",
  lrt: "LRT",
  mikrotrans: "Mikrotrans",
};

export default function WhatIfParams() {
  const { whatIfParams, setWhatIfParams } = useAccessibilityStore();

  return (
    <div className="space-y-2">
      <p className="text-[10px] font-semibold text-slate-400 dark:text-[#c8c5cd] uppercase tracking-wide">
        Parameters
      </p>
      <div className="grid grid-cols-2 gap-2">
        {/* Mode selector */}
        <div className="col-span-2">
          <label className="text-[10px] text-slate-500 dark:text-[#c8c5cd] block mb-1">
            Transit Mode
          </label>
          <select
            value={whatIfParams.mode}
            onChange={(e) =>
              setWhatIfParams({
                mode: e.target.value as
                  | "transjakarta"
                  | "krl"
                  | "mrt"
                  | "lrt"
                  | "mikrotrans",
              })
            }
            className="w-full text-xs border border-slate-200 dark:border-white/10 rounded-lg px-2 py-1.5 bg-white dark:bg-dark-container text-slate-700 dark:text-[#e2e0fc]"
          >
            {Object.entries(MODE_LABELS).map(([v, l]) => (
              <option key={v} value={v}>
                {l}
              </option>
            ))}
          </select>
        </div>

        {/* Fare */}
        <div>
          <label className="text-[10px] text-slate-500 dark:text-[#c8c5cd] block mb-1">
            Fare (Rp)
          </label>
          <input
            type="number"
            min={0}
            value={whatIfParams.fareIdr}
            onChange={(e) =>
              setWhatIfParams({ fareIdr: Number(e.target.value) })
            }
            className="w-full text-xs border border-slate-200 dark:border-white/10 rounded-lg px-2 py-1.5 bg-white dark:bg-dark-container text-slate-700 dark:text-[#e2e0fc]"
          />
        </div>

        {/* Headway */}
        <div>
          <label className="text-[10px] text-slate-500 dark:text-[#c8c5cd] block mb-1">
            Headway (min)
          </label>
          <input
            type="number"
            min={1}
            value={whatIfParams.headwayMin}
            onChange={(e) =>
              setWhatIfParams({ headwayMin: Number(e.target.value) })
            }
            className="w-full text-xs border border-slate-200 dark:border-white/10 rounded-lg px-2 py-1.5 bg-white dark:bg-dark-container text-slate-700 dark:text-[#e2e0fc]"
          />
        </div>

        {/* Coverage radius */}
        <div className="col-span-2">
          <label className="text-[10px] text-slate-500 dark:text-[#c8c5cd] block mb-1">
            Coverage radius:{" "}
            <span className="font-semibold text-indigo-500">
              {Math.round(whatIfParams.coverageRadiusKm * 1000)} m
            </span>
          </label>
          <input
            type="range"
            min={300}
            max={2000}
            step={100}
            value={Math.round(whatIfParams.coverageRadiusKm * 1000)}
            onChange={(e) =>
              setWhatIfParams({
                coverageRadiusKm: Number(e.target.value) / 1000,
              })
            }
            className="w-full accent-indigo-500"
          />
        </div>
      </div>
    </div>
  );
}

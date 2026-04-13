"use client";

import { useAccessibilityStore } from "@/lib/store";
import GlassPanel from "@/components/ui/GlassPanel";

const MODE_ICONS: Record<string, string> = {
  walk: "🚶‍♂️", wait: "⏱", transjakarta: "🚌", krl: "🚆", mrt: "🚇", lrt: "🚈",
};

function fmt(val: number | null | undefined): string {
  if (val == null) return "—";
  if (val >= 1_000_000) return `Rp ${(val / 1_000_000).toFixed(1)}M`;
  if (val >= 1_000) return `Rp ${Math.round(val / 1_000)}K`;
  return `Rp ${Math.round(val)}`;
}

interface Leg { mode: string; label: string; detail: string; time: number; fare: number | null; }

function LegRow({ leg }: { leg: Leg }) {
  return (
    <div className="flex items-start gap-2.5 py-2 border-b border-slate-100 dark:border-white/8 last:border-0">
      <span className="text-base mt-0.5 w-5 flex-shrink-0">{MODE_ICONS[leg.mode] ?? "🚌"}</span>
      <div className="flex-1 min-w-0">
        <p className="text-[11px] font-semibold text-slate-700 dark:text-[#e2e0fc] truncate">{leg.label}</p>
        {leg.detail && <p className="text-[10px] text-slate-400 dark:text-[#c8c5cd] truncate">{leg.detail}</p>}
      </div>
      <div className="flex items-center gap-1.5 flex-shrink-0">
        <span className="text-[10px] font-mono bg-slate-100 dark:bg-dark-high text-slate-600 dark:text-[#c8c5cd] rounded-full px-2 py-0.5">
          {leg.time} min
        </span>
        {leg.fare != null && leg.fare > 0 && (
          <span className="text-[10px] font-mono bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-teal rounded-full px-2 py-0.5">
            {fmt(leg.fare)}
          </span>
        )}
      </div>
    </div>
  );
}

export default function CBDJourneyCard({ delay = 0 }: { delay?: number }) {
  const { selectedHex, nearbyTransitStops } = useAccessibilityStore();
  if (!selectedHex) return null;

  if (selectedHex.poi_reach_cbd_min == null) {
    return (
      <GlassPanel delay={delay} className="p-5">
        <h3 className="text-xs font-semibold text-slate-400 dark:text-[#c8c5cd] uppercase tracking-wider mb-3">
          CBD Journey
        </h3>
        <p className="text-xs text-slate-400 dark:text-[#c8c5cd] text-center py-3">
          Journey data not available for this zone
        </p>
      </GlassPanel>
    );
  }

  const firstStop = nearbyTransitStops[0];
  const transitMode = firstStop?.type ?? "transjakarta";
  const walkDist = selectedHex.min_dist_to_transit_m ?? 500;
  const walkTime = Math.round(walkDist / 80);
  const waitTime = Math.round((selectedHex.avg_headway_min ?? 15) / 2);
  const rideTime = Math.max(5, selectedHex.poi_reach_cbd_min - walkTime - waitTime - 8);
  const fare = selectedHex.est_cbd_journey_fare_idr ?? null;
  const totalTime = walkTime + waitTime + rideTime + 8;

  const legs: Leg[] = [
    { mode: "walk", label: "Walk to stop", detail: `${Math.round(walkDist)}m to nearest stop`, time: walkTime, fare: null },
    { mode: "wait", label: "Wait at stop", detail: `avg headway: ${selectedHex.avg_headway_min ?? 15} min`, time: waitTime, fare: null },
    { mode: transitMode, label: `${transitMode.charAt(0).toUpperCase() + transitMode.slice(1)} to CBD`, detail: firstStop?.line ?? "CBD-bound service", time: rideTime, fare },
    { mode: "walk", label: "Walk to destination", detail: "Last mile to Sudirman-Thamrin", time: 8, fare: null },
  ];

  const { distance_to_sudirman_km: distKm, gc_transit_idr: gcT, gc_car_idr: gcC, gc_motorcycle_idr: gcM } = selectedHex;

  return (
    <GlassPanel delay={delay} className="p-5">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-xs font-semibold text-slate-400 dark:text-[#c8c5cd] uppercase tracking-wider">CBD Journey</h3>
        <span className="text-[10px] font-semibold bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-300 rounded-full px-2.5 py-0.5">
          ~{totalTime} min total
        </span>
      </div>

      <div className="space-y-0 mb-3">
        {legs.map((leg, i) => <LegRow key={i} leg={leg} />)}
      </div>

      <div className="border-t border-slate-100 dark:border-white/10 pt-3 space-y-2">
        {distKm != null && (
          <p className="text-[10px] text-slate-400 dark:text-[#c8c5cd] text-center">~{distKm.toFixed(1)} km from Sudirman</p>
        )}
        {(gcT != null || gcC != null || gcM != null) && (
          <div className="flex justify-around text-center">
            {gcT != null && <div><p className="text-[9px] text-slate-400 dark:text-[#c8c5cd]">🚌 Transit</p><p className="text-[10px] font-mono font-semibold text-blue-600 dark:text-teal">{fmt(gcT)}</p></div>}
            {gcC != null && <div><p className="text-[9px] text-slate-400 dark:text-[#c8c5cd]">🚗 Car</p><p className="text-[10px] font-mono font-semibold text-slate-600 dark:text-[#e2e0fc]">{fmt(gcC)}</p></div>}
            {gcM != null && <div><p className="text-[9px] text-slate-400 dark:text-[#c8c5cd]">🛵 Moto</p><p className="text-[10px] font-mono font-semibold text-orange-500 dark:text-orange-400">{fmt(gcM)}</p></div>}
          </div>
        )}
      </div>
    </GlassPanel>
  );
}

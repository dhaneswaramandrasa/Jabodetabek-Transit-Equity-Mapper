"use client";

import { useAccessibilityStore } from "@/lib/store";
import GlassPanel from "@/components/ui/GlassPanel";

// Transit competitive zone config
const ZONE_CONFIG = {
  transit_wins: {
    label: "Transit Wins",
    color: "text-emerald-600 dark:text-emerald-400",
    bg: "bg-emerald-50 dark:bg-emerald-900/20",
    dot: "bg-emerald-500",
  },
  swing: {
    label: "Swing Zone",
    color: "text-amber-600 dark:text-amber-400",
    bg: "bg-amber-50 dark:bg-amber-900/20",
    dot: "bg-amber-500",
  },
  private_wins: {
    label: "Private Wins",
    color: "text-red-600 dark:text-red-400",
    bg: "bg-red-50 dark:bg-red-900/20",
    dot: "bg-red-500",
  },
  transit_not_available: {
    label: "No Transit",
    color: "text-slate-500 dark:text-slate-400",
    bg: "bg-slate-100 dark:bg-slate-800/40",
    dot: "bg-slate-400",
  },
} as const;

function formatIdr(val: number | null | undefined): string {
  if (val == null) return "—";
  if (val >= 1_000_000) return `Rp ${(val / 1_000_000).toFixed(1)}M`;
  if (val >= 1_000) return `Rp ${Math.round(val / 1_000)}K`;
  return `Rp ${Math.round(val)}`;
}

function CostBar({
  label,
  value,
  maxValue,
  color,
  formatted,
}: {
  label: string;
  value: number;
  maxValue: number;
  color: string;
  formatted: string;
}) {
  const pct = maxValue > 0 ? Math.min((value / maxValue) * 100, 100) : 0;
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-[11px]">
        <span className="text-slate-500 dark:text-[#c8c5cd]">{label}</span>
        <span className="font-mono font-semibold text-slate-700 dark:text-[#e2e0fc]">{formatted}</span>
      </div>
      <div className="h-2 bg-slate-100 dark:bg-dark-high rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

export default function CostComparisonCard({ delay = 0 }: { delay?: number }) {
  const { selectedHex } = useAccessibilityStore();

  if (!selectedHex) return null;

  const gcTransit = selectedHex.gc_transit_idr;
  const gcCar = selectedHex.gc_car_idr;
  const gcMoto = selectedHex.gc_motorcycle_idr;
  const tcrCar = selectedHex.tcr_vs_car;
  const tcrMoto = selectedHex.tcr_vs_motorcycle;
  const zone = selectedHex.transit_competitive_zone;

  // If no cost data available at all, show placeholder
  const hasData = gcTransit != null || gcCar != null || gcMoto != null;

  const maxGc = Math.max(gcTransit ?? 0, gcCar ?? 0, gcMoto ?? 0);
  const zoneConfig = zone ? ZONE_CONFIG[zone] : null;

  return (
    <GlassPanel delay={delay} className="p-5">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xs font-semibold text-slate-400 dark:text-[#c8c5cd] uppercase tracking-wider">
          Cost Comparison
        </h3>
        {zoneConfig && (
          <span className={`flex items-center gap-1.5 text-[10px] font-semibold px-2 py-0.5 rounded-full ${zoneConfig.bg} ${zoneConfig.color}`}>
            <span className={`w-1.5 h-1.5 rounded-full ${zoneConfig.dot}`} />
            {zoneConfig.label}
          </span>
        )}
      </div>

      {!hasData ? (
        <p className="text-xs text-slate-400 dark:text-[#c8c5cd] text-center py-3">
          Cost data not available at this resolution
        </p>
      ) : (
        <div className="space-y-3">
          {/* Generalized cost bars */}
          <div className="space-y-2.5">
            <CostBar
              label="🚌 Transit (GC)"
              value={gcTransit ?? 0}
              maxValue={maxGc}
              color="bg-blue-500"
              formatted={formatIdr(gcTransit)}
            />
            <CostBar
              label="🚗 Car (GC)"
              value={gcCar ?? 0}
              maxValue={maxGc}
              color="bg-slate-400"
              formatted={formatIdr(gcCar)}
            />
            <CostBar
              label="🛵 Motorcycle (GC)"
              value={gcMoto ?? 0}
              maxValue={maxGc}
              color="bg-orange-400"
              formatted={formatIdr(gcMoto)}
            />
          </div>

          {/* TCR ratios */}
          {(tcrCar != null || tcrMoto != null) && (
            <div className="border-t border-slate-100 dark:border-white/10 pt-3 space-y-1.5">
              <p className="text-[10px] font-semibold text-slate-400 dark:text-[#c8c5cd] uppercase tracking-wide mb-2">
                Transit Cost Ratio (TCR)
              </p>
              {tcrCar != null && (
                <div className="flex justify-between text-[11px]">
                  <span className="text-slate-500 dark:text-[#c8c5cd]">vs Car</span>
                  <span className={`font-mono font-semibold ${
                    tcrCar < 1 ? "text-emerald-600 dark:text-emerald-400" :
                    tcrCar < 1.5 ? "text-amber-600 dark:text-amber-400" :
                    "text-red-600 dark:text-red-400"
                  }`}>
                    {tcrCar.toFixed(2)}×
                    {tcrCar < 1 ? " ✓ cheaper" : tcrCar < 1.5 ? " ~ similar" : " ✗ pricier"}
                  </span>
                </div>
              )}
              {tcrMoto != null && (
                <div className="flex justify-between text-[11px]">
                  <span className="text-slate-500 dark:text-[#c8c5cd]">vs Motorcycle</span>
                  <span className={`font-mono font-semibold ${
                    tcrMoto < 1 ? "text-emerald-600 dark:text-emerald-400" :
                    tcrMoto < 1.5 ? "text-amber-600 dark:text-amber-400" :
                    "text-red-600 dark:text-red-400"
                  }`}>
                    {tcrMoto.toFixed(2)}×
                    {tcrMoto < 1 ? " ✓ cheaper" : tcrMoto < 1.5 ? " ~ similar" : " ✗ pricier"}
                  </span>
                </div>
              )}
            </div>
          )}

          {/* Fare note */}
          {selectedHex.est_cbd_journey_fare_idr != null && (
            <div className="bg-blue-50/60 dark:bg-dark-high rounded-lg p-2.5 text-center">
              <p className="text-[10px] text-slate-500 dark:text-[#c8c5cd]">Est. CBD journey fare</p>
              <p className="text-sm font-bold font-mono text-blue-600 dark:text-teal">
                {formatIdr(selectedHex.est_cbd_journey_fare_idr)}
              </p>
            </div>
          )}
        </div>
      )}
    </GlassPanel>
  );
}

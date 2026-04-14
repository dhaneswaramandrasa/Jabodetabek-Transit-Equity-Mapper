"use client";

import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import { useAccessibilityStore, QUADRANT_COLORS, QUADRANT_LABELS } from "@/lib/store";
import { estimateJourney, type JourneyOption, type JourneyLeg } from "@/lib/journey";

function formatIdr(cost: number): string {
  return new Intl.NumberFormat("id-ID").format(cost);
}

function LegIcon({ type }: { type: JourneyLeg["type"] }) {
  const iconMap: Record<JourneyLeg["type"], string> = {
    walk: "directions_walk",
    wait: "schedule",
    ride: "two_wheeler",
    drive: "directions_car",
  };
  return (
    <span className="material-symbols-outlined text-on-surface/40 text-sm">
      {iconMap[type]}
    </span>
  );
}

function ModeCard({
  option,
  expanded,
  onToggle,
}: {
  option: JourneyOption;
  expanded: boolean;
  onToggle: () => void;
}) {
  const tagColors: Record<string, string> = {
    Cheapest: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
    Fastest: "bg-blue-500/20 text-blue-400 border-blue-500/30",
    "Best Value": "bg-primary/20 text-primary border-primary/30",
  };

  return (
    <button
      onClick={onToggle}
      disabled={!option.available}
      className={`w-full text-left rounded-lg border p-4 transition-all ${
        option.recommended
          ? "border-primary/40 bg-primary/5"
          : "border-white/8 bg-white/3 hover:bg-white/6"
      } ${!option.available ? "opacity-40 cursor-not-allowed" : "cursor-pointer"}`}
    >
      <div className="flex items-center gap-3">
        <span className="material-symbols-outlined text-on-surface/60 text-xl">
          {option.icon}
        </span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-0.5">
            <span className="text-sm font-semibold text-on-surface">
              {option.label}
            </span>
            {option.tag && (
              <span
                className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                  tagColors[option.tag] ?? tagColors["Best Value"]
                }`}
              >
                {option.tag}
              </span>
            )}
            {!option.available && (
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full border border-red-500/30 bg-red-500/10 text-red-400">
                Not available
              </span>
            )}
          </div>
          <div className="flex items-center gap-3 text-xs text-on-surface/50">
            <span>
              {option.legs
                .slice(0, 3)
                .map((l) => l.type.charAt(0).toUpperCase() + l.type.slice(1))
                .join(" → ")}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          <div className="text-sm font-bold text-on-surface">
            {option.totalTimeMin} min
          </div>
          <div className="text-xs text-on-surface/50">
            Rp {formatIdr(option.totalCostIdr)}
          </div>
        </div>
      </div>

      {/* Expanded legs breakdown */}
      {expanded && option.available && (
        <div className="mt-4 pt-3 border-t border-white/8 space-y-2">
          {option.legs.map((leg, i) => (
            <div key={i} className="flex items-center gap-2 text-xs">
              <LegIcon type={leg.type} />
              <span className="flex-1 text-on-surface/70">{leg.label}</span>
              <span className="font-mono text-on-surface/50 tabular-nums">
                {leg.durationMin} min
                {leg.distanceKm != null
                  ? ` · ${leg.distanceKm.toFixed(1)} km`
                  : ""}
              </span>
              {leg.costIdr != null && (
                <span className="font-mono text-on-surface/40 tabular-nums">
                  Rp {formatIdr(leg.costIdr)}
                </span>
              )}
            </div>
          ))}
          <div className="flex justify-between pt-2 border-t border-white/8 text-xs font-bold text-on-surface/80 mt-1">
            <span>Total</span>
            <span>
              {option.totalTimeMin} min · Rp {formatIdr(option.totalCostIdr)}
            </span>
          </div>
        </div>
      )}
    </button>
  );
}

export default function JourneyPanel() {
  const homeZone = useAccessibilityStore((s) => s.homeZone);
  const homeCoord = useAccessibilityStore((s) => s.homeCoord);
  const officeCoord = useAccessibilityStore((s) => s.officeCoord);
  const homeName = useAccessibilityStore((s) => s.homeName);
  const officeName = useAccessibilityStore((s) => s.officeName);
  const journeyReady = useAccessibilityStore((s) => s.journeyReady);
  const clearJourney = useAccessibilityStore((s) => s.clearJourney);

  const [expandedMode, setExpandedMode] = useState<string | null>(null);

  const options = useMemo<JourneyOption[]>(() => {
    if (!homeZone || !homeCoord || !officeCoord || !journeyReady) return [];
    return estimateJourney(homeZone, homeCoord, officeCoord);
  }, [homeZone, homeCoord, officeCoord, journeyReady]);

  if (!journeyReady || !homeCoord || !officeCoord) {
    return (
      <div className="h-full flex items-center justify-center p-8">
        <p className="text-on-surface/40 text-sm text-center">
          Set both home and office pins to compare journey options.
        </p>
      </div>
    );
  }

  const quadrant = homeZone?.quadrant;
  const quadrantColor = quadrant ? QUADRANT_COLORS[quadrant] : null;
  const quadrantLabel = quadrant ? QUADRANT_LABELS[quadrant] : null;
  const taiScore = homeZone?.tai_score;

  const handleToggle = (mode: string) => {
    setExpandedMode((prev) => (prev === mode ? null : mode));
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.35 }}
      className="h-full flex flex-col bg-surface/90 backdrop-blur-md border-l border-outline-variant/10 pointer-events-auto"
    >
      {/* Header */}
      <div className="px-5 py-4 border-b border-outline-variant/10 bg-surface-container/80 backdrop-blur-md">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <div className="flex items-center gap-1.5 text-xs text-on-surface/60 mb-1 flex-wrap">
              <span className="material-symbols-outlined text-sm">home</span>
              <span className="font-medium text-on-surface truncate max-w-[120px]">
                {homeName}
              </span>
              <span className="text-on-surface/30">→</span>
              <span className="material-symbols-outlined text-sm">business</span>
              <span className="font-medium text-on-surface truncate max-w-[120px]">
                {officeName}
              </span>
            </div>
            {quadrant && quadrantColor && (
              <div className="flex items-center gap-2">
                <span
                  className="inline-block w-2 h-2 rounded-full"
                  style={{
                    backgroundColor: `rgb(${quadrantColor.join(",")})`,
                  }}
                />
                <span className="text-xs text-on-surface/50">
                  {quadrantLabel}
                </span>
              </div>
            )}
          </div>
          <button
            onClick={clearJourney}
            className="shrink-0 px-2.5 py-1.5 text-xs bg-surface-container-high text-on-surface-variant hover:bg-surface-bright rounded font-medium transition-colors"
          >
            ← Back
          </button>
        </div>
      </div>

      {/* Mode cards */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {options.length === 0 ? (
          <p className="text-on-surface/40 text-sm text-center py-8">
            No route data available for this zone.
          </p>
        ) : (
          options.map((opt) => (
            <ModeCard
              key={opt.mode}
              option={opt}
              expanded={expandedMode === opt.mode}
              onToggle={() => handleToggle(opt.mode)}
            />
          ))
        )}

        {/* Equity context card */}
        {homeZone && (
          <div className="mt-4 rounded-lg border border-white/8 bg-white/3 p-4 space-y-2">
            <p className="text-xs font-semibold text-on-surface/60 uppercase tracking-widest">
              Zone equity context
            </p>
            {quadrant && quadrantColor && (
              <div className="flex items-center gap-2">
                <span
                  className="inline-block w-2.5 h-2.5 rounded-full shrink-0"
                  style={{
                    backgroundColor: `rgb(${quadrantColor.join(",")})`,
                  }}
                />
                <span className="text-sm text-on-surface font-medium">
                  {quadrantLabel}
                </span>
              </div>
            )}
            {taiScore != null && (
              <div className="flex items-center gap-2">
                <span className="text-xs text-on-surface/50">
                  Transit access score:
                </span>
                <span className="text-xs font-mono font-bold text-on-surface">
                  {Math.round(taiScore * 100)}/100
                </span>
              </div>
            )}
            {quadrant === "Q4" && (
              <p className="text-xs text-red-400/80 leading-relaxed">
                Transit Desert — limited frequency and coverage in this zone
              </p>
            )}
            {quadrant === "Q1" && (
              <p className="text-xs text-emerald-400/80 leading-relaxed">
                Well-served — transit is competitive here
              </p>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
}

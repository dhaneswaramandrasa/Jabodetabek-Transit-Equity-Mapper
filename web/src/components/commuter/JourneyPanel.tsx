"use client";

import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import {
  useAccessibilityStore,
  QUADRANT_COLORS,
  QUADRANT_LABELS,
} from "@/lib/store";
import {
  estimateJourney,
  type JourneyOption,
  type JourneyLeg,
} from "@/lib/journey";

type SortKey = "probability" | "cost" | "time";

function formatIdr(cost: number): string {
  return new Intl.NumberFormat("id-ID").format(cost);
}

function formatPct(p: number): string {
  return `${Math.round(p * 100)}%`;
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

function ProbabilityBar({ probability }: { probability: number }) {
  const width = Math.max(probability * 100, 3); // min 3% for visibility
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 rounded-full bg-white/8 overflow-hidden">
        <div
          className="h-full rounded-full bg-primary/60 transition-all duration-500"
          style={{ width: `${width}%` }}
        />
      </div>
      <span className="font-mono text-[11px] font-bold text-on-surface/60 tabular-nums w-9 text-right">
        {formatPct(probability)}
      </span>
    </div>
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
  };

  const isHighestProb = option.probability > 0.3;

  return (
    <button
      onClick={onToggle}
      disabled={!option.available}
      role="button"
      className={`w-full text-left rounded-lg border p-4 transition-all ${
        isHighestProb
          ? "border-primary/30 bg-primary/5"
          : "border-white/8 bg-white/3 hover:bg-white/6"
      } ${
        !option.available ? "opacity-40 cursor-not-allowed" : "cursor-pointer"
      }`}
    >
      {/* Top row: icon, label, tags, time, cost */}
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
                  tagColors[option.tag] ?? ""
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
          <div className="text-[11px] text-on-surface/40 font-label">
            {option.chainLabel}
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

      {/* Probability bar */}
      {option.available && option.probability > 0 && (
        <div className="mt-3">
          <ProbabilityBar probability={option.probability} />
        </div>
      )}

      {/* Ride-hailing disclaimer */}
      {(option.mode === "goride" || option.mode === "gocar") && (
        <p className="text-[10px] text-on-surface/30 mt-2 leading-relaxed">
          Estimated fare — actual varies with surge pricing and traffic.
        </p>
      )}

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
          {option.methodNote && (
            <p className="text-[10px] text-on-surface/30 mt-1 leading-relaxed italic">
              {option.methodNote}
            </p>
          )}
        </div>
      )}
    </button>
  );
}

function EquityContextCard({
  quadrant,
  quadrantColor,
  quadrantLabel,
  taiScore,
}: {
  quadrant: string | undefined;
  quadrantColor: [number, number, number] | null;
  quadrantLabel: string | null | undefined;
  taiScore: number | null | undefined;
}) {
  if (!quadrant || !quadrantColor) return null;

  return (
    <div className="rounded-lg border border-white/8 bg-white/3 p-4 space-y-2">
      <p className="text-xs font-semibold text-on-surface/60 uppercase tracking-widest">
        Your zone
      </p>
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
          Transit Desert — limited frequency and coverage in this zone.
          Transit may still be your best option, but first/last mile is
          critical.
        </p>
      )}
      {quadrant === "Q1" && (
        <p className="text-xs text-emerald-400/80 leading-relaxed">
          Well-served — transit is competitive here. Your commute has good
          options.
        </p>
      )}
    </div>
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
  const destZone = useAccessibilityStore((s) => s.selectedHex);

  const [expandedMode, setExpandedMode] = useState<string | null>(null);
  const [sortKey, setSortKey] = useState<SortKey>("probability");

  const options = useMemo<JourneyOption[]>(() => {
    if (!homeZone || !homeCoord || !officeCoord || !journeyReady) return [];
    const raw = estimateJourney(homeZone, homeCoord, officeCoord, destZone);
    // re-sort
    if (sortKey === "cost") {
      return [...raw].sort((a, b) => a.totalCostIdr - b.totalCostIdr);
    }
    if (sortKey === "time") {
      return [...raw].sort((a, b) => a.totalTimeMin - b.totalTimeMin);
    }
    return raw; // already probability-descending from estimateJourney
  }, [homeZone, homeCoord, officeCoord, journeyReady, destZone, sortKey]);

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
              <span className="font-medium text-on-surface truncate max-w-[140px]">
                {homeName}
              </span>
              <span className="text-on-surface/30">→</span>
              <span className="material-symbols-outlined text-sm">
                business
              </span>
              <span className="font-medium text-on-surface truncate max-w-[140px]">
                {officeName}
              </span>
            </div>
            {homeZone && quadrant && quadrantColor && (
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
            {!homeZone && (
              <p className="text-[10px] text-amber-400/70 mt-1">
                Unknown zone — estimates are approximate.
              </p>
            )}
          </div>
          <button
            onClick={clearJourney}
            className="shrink-0 px-2.5 py-1.5 text-xs bg-surface-container-high text-on-surface-variant hover:bg-surface-bright rounded font-medium transition-colors"
          >
            ← Back
          </button>
        </div>

        {/* Sort toggle */}
        <div className="flex items-center gap-1 mt-3 pt-2 border-t border-white/5">
          <span className="text-[10px] text-on-surface/40 font-label uppercase tracking-widest mr-2">
            Sort by
          </span>
          {([
            ["probability", "Best bet"],
            ["cost", "Cheapest"],
            ["time", "Fastest"],
          ] as [SortKey, string][]).map(([key, label]) => (
            <button
              key={key}
              onClick={() => setSortKey(key)}
              className={`text-[10px] font-semibold px-2 py-1 rounded transition-colors ${
                sortKey === key
                  ? "bg-primary/15 text-primary"
                  : "text-on-surface/40 hover:text-on-surface/70"
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {/* Equity context — above mode cards (the product's differentiator) */}
        <EquityContextCard
          quadrant={quadrant}
          quadrantColor={quadrantColor}
          quadrantLabel={quadrantLabel}
          taiScore={taiScore}
        />

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

        {/* Bottom note */}
        <p className="text-[10px] text-on-surface/25 text-center pt-2">
          Probabilities from nested logit model. Estimates only — not GTFS
          trip-planning.
        </p>
      </div>
    </motion.div>
  );
}

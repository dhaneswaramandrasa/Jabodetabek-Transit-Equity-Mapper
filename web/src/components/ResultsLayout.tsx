"use client";

import { motion } from "framer-motion";
import { useAccessibilityStore } from "@/lib/store";
import CardGrid from "./results/CardGrid";
import CommuterLens from "./results/lenses/CommuterLens";
import ResearcherLens from "./results/lenses/ResearcherLens";
import PlannerLens from "./results/lenses/PlannerLens";

export default function ResultsLayout() {
  const appPhase = useAccessibilityStore((s) => s.appPhase);
  const selectedPersona = useAccessibilityStore((s) => s.selectedPersona);
  const resetForNewAnalysis = useAccessibilityStore((s) => s.resetForNewAnalysis);

  if (appPhase !== "results") return null;

  // Researcher lens uses fixed sidebars — different layout pattern
  if (selectedPersona === "researcher") {
    return (
      <motion.div
        key="researcher"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
        className="absolute inset-0 z-10 pointer-events-none"
      >
        <ResearcherLens />
      </motion.div>
    );
  }

  if (selectedPersona === "commuter") {
    return (
      <motion.div
        key="commuter"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
        className="absolute inset-0 z-10 pointer-events-none"
      >
        <CommuterLens />
      </motion.div>
    );
  }

  if (selectedPersona === "planner") {
    return (
      <motion.div
        key="planner"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
        className="absolute inset-0 z-10 pointer-events-none"
      >
        <PlannerLens />
      </motion.div>
    );
  }

  // Default / null persona — minimal right panel with CardGrid
  return (
    <motion.div
      key="default"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.35 }}
      className="absolute top-0 right-0 z-10 h-full w-full md:w-[520px] lg:w-[560px] flex flex-col bg-surface/90 backdrop-blur-md border-l border-outline-variant/10"
    >
      {/* Top bar */}
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-outline-variant/10 bg-surface-container/80 backdrop-blur-md">
        <span className="text-sm font-semibold text-on-surface">
          Analysis Results
        </span>
        <button
          onClick={resetForNewAnalysis}
          className="px-2.5 py-1.5 text-xs bg-surface-container-high text-on-surface-variant hover:bg-surface-bright rounded font-medium transition-colors"
        >
          ✕
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <CardGrid />
      </div>
    </motion.div>
  );
}

"use client";

import TransitScoreCard from "./TransitScoreCard";
import POIAccessCard from "./POIAccessCard";
import DemographicsCard from "./DemographicsCard";
import TransitLinesCard from "./TransitLinesCard";
import AIAnalysisCard from "./AIAnalysisCard";
import CostComparisonCard from "./CostComparisonCard";
import CBDJourneyCard from "./CBDJourneyCard";

export default function CardGrid() {
  return (
    <div className="space-y-4">
      {/* Row 1: Score + Demographics side by side */}
      <div className="grid grid-cols-2 gap-4">
        <TransitScoreCard delay={0.1} />
        <DemographicsCard delay={0.15} />
      </div>

      {/* Row 2: Cost comparison (full width) */}
      <CostComparisonCard delay={0.18} />

      {/* Row 3: CBD Journey chain (full width) */}
      <CBDJourneyCard delay={0.2} />

      {/* Row 4: What can you reach? (full width) */}
      <POIAccessCard delay={0.22} />

      {/* Row 5: Transit + AI side by side */}
      <div className="grid grid-cols-2 gap-4">
        <TransitLinesCard delay={0.25} />
        <AIAnalysisCard delay={0.3} />
      </div>
    </div>
  );
}

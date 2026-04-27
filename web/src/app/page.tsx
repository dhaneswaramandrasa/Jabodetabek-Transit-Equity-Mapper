"use client";

import dynamic from "next/dynamic";
import LandingOverlay from "@/components/landing/LandingOverlay";
import LoadingSequence from "@/components/loading/LoadingSequence";
import ResultsLayout from "@/components/ResultsLayout";
import AppShell from "@/components/AppShell";
import ThemeProvider from "@/components/ThemeProvider";
import { useAISummary } from "@/hooks/useAISummary";
import { useAccessibilityStore } from "@/lib/store";

// deck.gl / luma.gl require WebGL — must skip SSR
const AccessibilityMap = dynamic(
  () => import("@/components/AccessibilityMap"),
  {
    ssr: false,
    loading: () => (
      <div className="w-full h-full flex items-center justify-center bg-surface">
        <div className="text-on-surface/40 text-sm animate-pulse font-label">
          Loading map...
        </div>
      </div>
    ),
  }
);

export default function Home() {
  useAISummary();

  const appPhase = useAccessibilityStore((s) => s.appPhase);

  const inApp = appPhase === "loading" || appPhase === "results";

  return (
    <div className="h-screen w-screen relative overflow-hidden bg-surface">
      {/* Theme initialiser */}
      <ThemeProvider />

      {/* Map always renders underneath, full screen */}
      <div className="absolute inset-0">
        <AccessibilityMap />
      </div>

      {/* Landing overlay */}
      <LandingOverlay />

      {/* Loading sequence */}
      <LoadingSequence />

      {/* App shell — fixed nav + sidebar for in-app phases */}
      {inApp && <AppShell />}

      {/* Results panels — offset below top-nav (h-14) and right of sidebar (w-20) */}
      {appPhase === "results" && (
        <div className="absolute top-14 left-20 right-0 bottom-0 pointer-events-none">
          <ResultsLayout />
        </div>
      )}
    </div>
  );
}

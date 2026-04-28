"use client";

import { useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useAccessibilityStore } from "@/lib/store";

export default function LandingOverlay() {
  const appPhase = useAccessibilityStore((s) => s.appPhase);
  const setBoundaryMode = useAccessibilityStore((s) => s.setBoundaryMode);
  const setHexLayerVisible = useAccessibilityStore((s) => s.setHexLayerVisible);
  const setAppPhase = useAccessibilityStore((s) => s.setAppPhase);

  const pinMode = useAccessibilityStore((s) => s.pinMode);
  const setPinMode = useAccessibilityStore((s) => s.setPinMode);
  const homeCoord = useAccessibilityStore((s) => s.homeCoord);
  const homeName = useAccessibilityStore((s) => s.homeName);
  const officeCoord = useAccessibilityStore((s) => s.officeCoord);
  const officeName = useAccessibilityStore((s) => s.officeName);
  const journeyReady = useAccessibilityStore((s) => s.journeyReady);
  const setHomePin = useAccessibilityStore((s) => s.setHomePin);
  const setOfficePin = useAccessibilityStore((s) => s.setOfficePin);

  // Restore last home coord from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem("jtm_home");
      if (stored) {
        const coord = JSON.parse(stored) as [number, number];
        setHomePin(coord, "Home (saved)");
      }
    } catch {
      // ignore parse errors
    }
  }, [setHomePin]);

  // Persist homeCoord to localStorage whenever it changes
  useEffect(() => {
    if (homeCoord) {
      try {
        localStorage.setItem("jtm_home", JSON.stringify(homeCoord));
      } catch {
        // ignore storage errors
      }
    }
  }, [homeCoord]);

  const handleCompare = () => {
    setBoundaryMode("kelurahan");
    setHexLayerVisible(true);
    setAppPhase("loading");
    setTimeout(() => setAppPhase("results"), 1800);
  };

  const handleClearHome = () => {
    useAccessibilityStore.setState({
      homeCoord: null,
      homeZone: null,
      homeName: "",
      journeyReady: false,
    });
    localStorage.removeItem("jtm_home");
    setPinMode("home");
  };

  const handleClearOffice = () => {
    useAccessibilityStore.setState({
      officeCoord: null,
      officeName: "",
      journeyReady: false,
    });
    setPinMode("office");
  };

  return (
    <AnimatePresence>
      {appPhase === "landing" && (
        <motion.div
          key="landing"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.4 }}
          className="fixed inset-0 z-20 flex flex-col"
        >
          {/* Glow border frame */}
          <div className="fixed inset-4 pointer-events-none z-50 rounded-2xl glow-border" />

          {/* Map background overlays */}
          <div className="fixed inset-0 z-0 pointer-events-none">
            <div className="absolute inset-0 h3-overlay opacity-40" />
            <div className="absolute inset-0 bg-gradient-to-tr from-surface via-transparent to-surface/20" />
          </div>

          {/* Top navigation */}
          <nav className="relative z-50 flex justify-between items-center px-12 h-20 bg-transparent">
            <div className="flex items-center gap-10">
              <span className="text-xl font-black text-primary tracking-tighter font-headline">
                JTEM
              </span>
              <div className="hidden md:flex items-center gap-8">
                <a className="text-on-surface/60 font-medium text-xs uppercase tracking-widest hover:text-primary transition-colors cursor-pointer">
                  Methodology
                </a>
                <a className="text-on-surface/60 font-medium text-xs uppercase tracking-widest hover:text-primary transition-colors cursor-pointer">
                  Research Paper
                </a>
                <a className="text-on-surface/60 font-medium text-xs uppercase tracking-widest hover:text-primary transition-colors cursor-pointer">
                  How it works
                </a>
              </div>
            </div>
          </nav>

          {/* Center glass panel */}
          <main className="flex-1 relative z-10 flex items-center justify-center px-8 pb-12">
            <div className="main-glass-panel w-full max-w-2xl rounded-2xl p-10 flex flex-col items-center shadow-2xl relative overflow-hidden">
              {/* Pin mode banner */}
              <AnimatePresence>
                {pinMode !== null && (
                  <motion.div
                    key="pin-banner"
                    initial={{ opacity: 0, y: -8 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -8 }}
                    className="w-full mb-6 flex items-center justify-between gap-3 bg-primary/10 border border-primary/30 rounded-lg px-4 py-2.5"
                  >
                    <div className="flex items-center gap-2">
                      <span className="material-symbols-outlined text-primary text-base">
                        location_on
                      </span>
                      <span className="text-primary text-xs font-medium">
                        Click the map to set your{" "}
                        <strong>{pinMode === "home" ? "home" : "office"}</strong>
                      </span>
                    </div>
                    <button
                      onClick={() => setPinMode(null)}
                      className="text-on-surface/40 hover:text-on-surface/80 text-xs font-bold transition-colors"
                    >
                      Cancel
                    </button>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Badge */}
              <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/5 rounded-full mb-6 border border-white/10">
                <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
                <span className="font-label text-[10px] uppercase tracking-[0.2em] text-on-surface-variant">
                  Commute Planner · Jabodetabek
                </span>
              </div>

              <h1 className="text-3xl md:text-4xl font-black tracking-tighter font-headline mb-3 text-center leading-tight text-on-surface">
                Find the cheapest way{" "}
                <span className="text-primary italic">to get to work</span>
              </h1>

              <p className="text-on-surface-variant text-sm max-w-md mb-8 leading-relaxed opacity-80 text-center">
                Compare transit, GoRide, GoCar, and more for your exact commute
              </p>

              {/* Pin input rows */}
              <div className="w-full flex flex-col gap-3 mb-6">
                {/* Home row */}
                <button
                  onClick={() => setPinMode("home")}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg border transition-all text-left ${
                    pinMode === "home"
                      ? "border-primary bg-primary/10"
                      : "border-white/10 bg-white/5 hover:bg-white/8 hover:border-white/20"
                  }`}
                >
                  <span className="text-lg select-none">🏠</span>
                  <span
                    className={`flex-1 text-sm ${
                      homeCoord
                        ? "text-on-surface font-medium"
                        : "text-on-surface/40"
                    }`}
                  >
                    {homeCoord ? homeName : "Set home location..."}
                  </span>
                  {homeCoord ? (
                    <span
                      role="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleClearHome();
                      }}
                      className="material-symbols-outlined text-on-surface/40 hover:text-primary text-base transition-colors cursor-pointer"
                    >
                      edit_location
                    </span>
                  ) : (
                    <span className="material-symbols-outlined text-on-surface/30 text-base">
                      add_location
                    </span>
                  )}
                </button>

                {/* Connector line */}
                <div className="flex justify-center">
                  <div className="w-px h-4 bg-white/10" />
                </div>

                {/* Office row */}
                <button
                  onClick={() => setPinMode("office")}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg border transition-all text-left ${
                    pinMode === "office"
                      ? "border-primary bg-primary/10"
                      : "border-white/10 bg-white/5 hover:bg-white/8 hover:border-white/20"
                  }`}
                >
                  <span className="text-lg select-none">🏢</span>
                  <span
                    className={`flex-1 text-sm ${
                      officeCoord
                        ? "text-on-surface font-medium"
                        : "text-on-surface/40"
                    }`}
                  >
                    {officeCoord ? officeName : "Set office location..."}
                  </span>
                  {officeCoord ? (
                    <span
                      role="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleClearOffice();
                      }}
                      className="material-symbols-outlined text-on-surface/40 hover:text-primary text-base transition-colors cursor-pointer"
                    >
                      edit_location
                    </span>
                  ) : (
                    <span className="material-symbols-outlined text-on-surface/30 text-base">
                      add_location
                    </span>
                  )}
                </button>
              </div>

              {/* CTA */}
              <button
                onClick={handleCompare}
                disabled={!journeyReady}
                className={`w-full py-3.5 rounded-sm font-label text-sm font-black tracking-[0.2em] uppercase transition-all ${
                  journeyReady
                    ? "bg-primary text-on-primary hover:brightness-110 shadow-[0_0_30px_rgba(111,216,200,0.2)]"
                    : "bg-white/5 text-on-surface/20 cursor-not-allowed border border-white/10"
                }`}
              >
                Compare Options
              </button>

              <p className="text-on-surface/30 text-xs mt-4 text-center">
                Or click the map directly
              </p>

              {/* Bottom stat badges */}
              <div className="flex gap-4 mt-8 flex-wrap justify-center">
                {[
                  "30.4M residents",
                  "5 transit modes",
                  "Real 2024 data",
                ].map((s) => (
                  <span
                    key={s}
                    className="px-3 py-1 rounded-full bg-white/5 border border-white/10 text-on-surface/50 text-xs font-mono"
                  >
                    {s}
                  </span>
                ))}
              </div>
            </div>
          </main>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

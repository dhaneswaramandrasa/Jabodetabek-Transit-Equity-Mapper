"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useAccessibilityStore, type Persona } from "@/lib/store";
import SearchBar from "./SearchBar";

interface PersonaCard {
  id: Persona;
  icon: string;
  label: string;
  title: string;
  desc: string;
}

const PERSONA_CARDS: PersonaCard[] = [
  {
    id: "commuter",
    icon: "train",
    label: "Daily Commuter",
    title: "Route Intelligence",
    desc: "Find the fastest transit path and compare costs vs driving.",
  },
  {
    id: "planner",
    icon: "dashboard",
    label: "Urban Planner",
    title: "Scenario Simulation",
    desc: "Model infrastructure investments and measure equity impact.",
  },
  {
    id: "researcher",
    icon: "biotech",
    label: "Researcher",
    title: "Spatial Statistics",
    desc: "Gini coefficients, LISA clusters, and multi-layer TAI data.",
  },
];

export default function LandingOverlay() {
  const appPhase = useAccessibilityStore((s) => s.appPhase);
  const selectedPersona = useAccessibilityStore((s) => s.selectedPersona);
  const setSelectedPersona = useAccessibilityStore((s) => s.setSelectedPersona);
  const setBoundaryMode = useAccessibilityStore((s) => s.setBoundaryMode);
  const setHexLayerVisible = useAccessibilityStore((s) => s.setHexLayerVisible);
  const setAppPhase = useAccessibilityStore((s) => s.setAppPhase);

  const handleEnter = () => {
    setBoundaryMode("kelurahan");
    setHexLayerVisible(true);
    setAppPhase("loading");
    setTimeout(() => setAppPhase("results"), 1800);
  };

  const handlePersonaClick = (id: Persona) => {
    setSelectedPersona(id);
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
          {/* Outer glow border frame */}
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
                  Contact
                </a>
              </div>
            </div>
            <div className="flex items-center gap-6">
              <button
                onClick={handleEnter}
                className="bg-primary text-on-primary px-5 py-2 rounded-sm font-label text-xs font-bold tracking-widest hover:brightness-110 transition-all uppercase"
              >
                Enter Engine
              </button>
            </div>
          </nav>

          {/* Main central shell */}
          <main className="flex-1 relative z-10 flex items-center justify-center px-8 pb-12">
            <div className="main-glass-panel w-full max-w-5xl rounded-2xl p-12 md:p-16 flex flex-col items-center text-center shadow-2xl relative overflow-hidden">
              {/* Pulse badge */}
              <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/5 rounded-full mb-10 border border-white/10">
                <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
                <span className="font-label text-[10px] uppercase tracking-[0.2em] text-on-surface-variant">
                  Map Interactive Mode
                </span>
              </div>

              <h1 className="text-4xl md:text-6xl font-black tracking-tighter font-headline mb-4 max-w-3xl leading-tight text-on-surface">
                A Data-Driven Diagnostic for
                <br />
                <span className="text-primary italic">Transit Equity</span> in
                Jabodetabek
              </h1>

              <p className="text-on-surface-variant text-sm md:text-base max-w-2xl mb-16 leading-relaxed opacity-80">
                Click anywhere on the map to begin spatial diagnostics for
                Indonesia&apos;s capital region. Visualize connectivity,
                identify deserts, and simulate infrastructure impact.
              </p>

              {/* Persona cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full mb-16">
                {PERSONA_CARDS.map((card) => (
                  <button
                    key={card.id}
                    onClick={() => handlePersonaClick(card.id)}
                    className={`card-glass p-6 rounded-xl text-left group cursor-pointer transition-all ${
                      selectedPersona === card.id
                        ? "border-primary bg-white/6"
                        : ""
                    }`}
                  >
                    <span className="material-symbols-outlined text-primary mb-3 block text-2xl">
                      {card.icon}
                    </span>
                    <p className="font-label text-[10px] uppercase tracking-widest font-bold text-on-surface-variant group-hover:text-primary mb-1 transition-colors">
                      {card.label}
                    </p>
                    <p className="font-headline font-bold text-on-surface text-sm mb-1">
                      {card.title}
                    </p>
                    <p className="text-on-surface-variant text-xs leading-relaxed opacity-70">
                      {card.desc}
                    </p>
                  </button>
                ))}
              </div>

              {/* CTA */}
              <div className="flex flex-col md:flex-row items-center gap-8">
                <button
                  onClick={handleEnter}
                  className="bg-primary text-on-primary px-10 py-4 rounded-sm font-label text-sm font-black tracking-[0.2em] uppercase hover:brightness-110 transition-all shadow-[0_0_30px_rgba(111,216,200,0.2)]"
                >
                  Start Analysis
                </button>
                <span className="font-mono text-[10px] tracking-widest text-on-surface/40 uppercase">
                  Waiting for input...
                </span>
              </div>
            </div>
          </main>

          {/* Bottom stats bar */}
          <footer className="relative z-50 flex flex-col md:flex-row justify-between items-center px-12 py-6 bg-surface/80 backdrop-blur-md border-t border-white/5">
            <div className="flex gap-12">
              <div>
                <span className="font-label text-[9px] uppercase tracking-widest text-on-surface/40">
                  Population
                </span>
                <span className="font-mono text-sm font-bold text-on-surface block">
                  30.4M
                </span>
              </div>
              <div>
                <span className="font-label text-[9px] uppercase tracking-widest text-on-surface/40">
                  Kelurahan
                </span>
                <span className="font-mono text-sm font-bold text-on-surface block">
                  2,670
                </span>
              </div>
              <div>
                <span className="font-label text-[9px] uppercase tracking-widest text-on-surface/40">
                  Transit Desert
                </span>
                <span className="font-mono text-sm font-bold text-primary block">
                  42%
                </span>
              </div>
            </div>
            <span className="font-mono text-[9px] text-on-surface/30 uppercase tracking-[0.2em]">
              EPSG:3857 | Jabodetabek Metropolitan Area
            </span>
          </footer>

          {/* Floating search — visual shell; SearchBar handles geocoding logic */}
          <div className="fixed top-24 left-1/2 -translate-x-1/2 z-40 w-full max-w-lg px-6 pointer-events-auto">
            <div className="relative">
              <SearchBar />
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

"use client";

import { useAccessibilityStore, type Persona } from "@/lib/store";

interface NavItem {
  id: Persona;
  icon: string;
  label: string;
}

const NAV_ITEMS: NavItem[] = [
  { id: "commuter", icon: "directions_transit", label: "Commuter" },
  { id: "explorer", icon: "travel_explore", label: "Explore" },
];

const COMING_SOON: NavItem[] = [
  { id: "researcher", icon: "analytics", label: "Researcher" },
  { id: "planner", icon: "map", label: "Planner" },
];

const TOP_TABS = ["Explorer", "Insights", "Archive"] as const;

export default function AppShell() {
  const selectedPersona = useAccessibilityStore((s) => s.selectedPersona);
  const setSelectedPersona = useAccessibilityStore((s) => s.setSelectedPersona);
  const resetForNewAnalysis = useAccessibilityStore((s) => s.resetForNewAnalysis);

  return (
    <>
      {/* Fixed top nav — h-14 */}
      <div className="fixed top-0 left-0 right-0 h-14 z-30 bg-surface-container-low border-b border-outline-variant/10 flex items-center justify-between px-4">
        {/* Left: logo + tabs */}
        <div className="flex items-center gap-6">
          <button
            onClick={resetForNewAnalysis}
            className="text-base font-black text-primary tracking-tighter font-headline shrink-0"
          >
            JTEM
          </button>
          <nav className="hidden md:flex items-center gap-1 h-14">
            {TOP_TABS.map((tab) => (
              <button
                key={tab}
                className={`px-4 h-full text-xs font-label font-semibold tracking-wide transition-colors border-b-2 ${
                  tab === "Explorer"
                    ? "text-primary border-primary"
                    : "text-on-surface/40 border-transparent hover:text-on-surface/70"
                }`}
              >
                {tab}
              </button>
            ))}
          </nav>
        </div>

        {/* Right: icons + avatar */}
        <div className="flex items-center gap-3">
          <button className="text-on-surface/40 hover:text-on-surface transition-colors p-1.5">
            <span className="material-symbols-outlined text-base">contrast</span>
          </button>
          <button className="text-on-surface/40 hover:text-on-surface transition-colors p-1.5">
            <span className="material-symbols-outlined text-base">notifications</span>
          </button>
          <button className="text-on-surface/40 hover:text-on-surface transition-colors p-1.5">
            <span className="material-symbols-outlined text-base">settings</span>
          </button>
          <div className="w-7 h-7 rounded-full bg-primary/20 border border-primary/40 flex items-center justify-center ml-1">
            <span className="material-symbols-outlined text-primary" style={{ fontSize: 14 }}>
              person
            </span>
          </div>
        </div>
      </div>

      {/* Fixed left sidebar — w-20, expands to w-64 on hover */}
      <div className="fixed top-14 left-0 bottom-0 z-20 w-20 hover:w-64 transition-all duration-300 bg-surface-container-low border-r border-outline-variant/10 flex flex-col overflow-hidden group">
        {/* Brand area */}
        <div className="flex items-center gap-3 px-5 py-4 border-b border-outline-variant/10 shrink-0 min-w-[256px]">
          <span className="material-symbols-outlined text-primary shrink-0" style={{ fontSize: 18 }}>
            terminal
          </span>
          <span className="font-label text-[10px] uppercase tracking-widest text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap">
            Tactical Intel
          </span>
        </div>

        {/* Nav items */}
        <nav className="flex-1 py-3">
          {NAV_ITEMS.map((item) => {
            const isActive = selectedPersona === item.id;
            return (
              <button
                key={item.label}
                onClick={() => setSelectedPersona(item.id)}
                className={`w-full flex items-center gap-4 px-5 py-3 transition-colors border-r-4 ${
                  isActive
                    ? "bg-surface-container text-primary border-primary"
                    : "text-on-surface/40 border-transparent hover:bg-surface-container/50 hover:text-on-surface"
                }`}
              >
                <span
                  className="material-symbols-outlined shrink-0"
                  style={{ fontSize: 20 }}
                >
                  {item.icon}
                </span>
                <span className="font-label text-xs font-semibold whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                  {item.label}
                </span>
              </button>
            );
          })}

          {/* Divider */}
          <div className="mx-4 my-2 border-t border-outline-variant/5 opacity-0 group-hover:opacity-100 transition-opacity duration-200" />

          {/* Coming soon items */}
          {COMING_SOON.map((item) => (
            <button
              key={item.label}
              disabled
              title={`${item.label} — coming soon`}
              className="w-full flex items-center gap-4 px-5 py-3 transition-colors border-r-4 border-transparent text-on-surface/20 cursor-not-allowed"
            >
              <span
                className="material-symbols-outlined shrink-0"
                style={{ fontSize: 20 }}
              >
                {item.icon}
              </span>
              <span className="font-label text-xs font-semibold whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                {item.label}
              </span>
            </button>
          ))}
        </nav>

        {/* Bottom actions — visible on hover */}
        <div className="py-4 border-t border-outline-variant/10 px-4 min-w-[256px]">
          <button className="w-full opacity-0 group-hover:opacity-100 transition-opacity duration-200 bg-primary/10 text-primary border border-primary/20 rounded-sm py-2 text-xs font-label font-bold tracking-widest uppercase mb-3 hover:bg-primary/20 transition-colors">
            Download Data
          </button>
          <div className="flex gap-4 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <button className="text-on-surface/30 text-[10px] font-label hover:text-on-surface/60 transition-colors">
              Docs
            </button>
            <button className="text-on-surface/30 text-[10px] font-label hover:text-on-surface/60 transition-colors">
              Feedback
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

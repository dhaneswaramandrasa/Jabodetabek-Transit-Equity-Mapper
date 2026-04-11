"use client";

import { useEffect } from "react";
import { useAccessibilityStore } from "@/lib/store";

/**
 * Reads jtm_theme from localStorage on first mount and syncs it to both
 * the Zustand store and the `dark` class on <html>.
 * Must be rendered inside the app (not layout.tsx) so it has access to the store.
 */
export default function ThemeProvider() {
  const { theme, toggleTheme } = useAccessibilityStore();

  useEffect(() => {
    const stored = localStorage.getItem("jtm_theme") as "light" | "dark" | null;
    if (stored && stored !== theme) {
      toggleTheme(); // toggles from current → stored value
    } else if (!stored) {
      // Default to system preference
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      if (prefersDark && theme === "light") toggleTheme();
    }
    // Apply class immediately to avoid flash
    document.documentElement.classList.toggle("dark", (stored ?? theme) === "dark");
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return null;
}

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "primary": "#6fd8c8",
        "primary-fixed": "#8cf5e4",
        "primary-container": "#00211d",
        "on-primary": "#003731",
        "on-primary-fixed": "#00201c",
        "secondary": "#98cdf2",
        "secondary-container": "#0b4e6e",
        "on-secondary-container": "#8abfe4",
        "surface": "#111125",
        "surface-dim": "#111125",
        "surface-container-lowest": "#0c0c1f",
        "surface-container-low": "#1a1a2e",
        "surface-container": "#1e1e32",
        "surface-container-high": "#28283d",
        "surface-container-highest": "#333348",
        "surface-bright": "#37374d",
        "surface-variant": "#333348",
        "background": "#111125",
        "on-surface": "#e2e0fc",
        "on-surface-variant": "#c8c5cd",
        "on-background": "#e2e0fc",
        "outline": "#929097",
        "outline-variant": "#47464c",
        "error": "#ffb4ab",
        "tertiary": "#ffb3b1",
        "inverse-surface": "#e2e0fc",
        "inverse-on-surface": "#2f2e43",
        // Legacy aliases — keep for backward compat
        "teal": {
          DEFAULT: "#6fd8c8",
          dim: "#6fd8c8",
          fixed: "#8cf5e4",
          on: "#003731",
        },
        "dark": {
          base: "#111125",
          low: "#1a1a2e",
          container: "#1e1e32",
          high: "#28283d",
          highest: "#333348",
          bright: "#37374d",
        },
      },
      fontFamily: {
        "headline": ["Inter", "sans-serif"],
        "body": ["Inter", "sans-serif"],
        "label": ["Space Grotesk", "sans-serif"],
        "mono": ["JetBrains Mono", "ui-monospace", "monospace"],
      },
      borderRadius: {
        DEFAULT: "0.125rem",
        lg: "0.25rem",
        xl: "0.5rem",
        "2xl": "0.75rem",
        full: "9999px",
      },
      keyframes: {
        fadeInUp: {
          "0%": { opacity: "0", transform: "translateY(16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        scaleIn: {
          "0%": { opacity: "0", transform: "scale(0.9)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        slideInRight: {
          "0%": { opacity: "0", transform: "translateX(24px)" },
          "100%": { opacity: "1", transform: "translateX(0)" },
        },
        pulse: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
        spin: {
          from: { transform: "rotate(0deg)" },
          to: { transform: "rotate(360deg)" },
        },
      },
      animation: {
        "fade-in-up": "fadeInUp 0.5s ease-out forwards",
        "scale-in": "scaleIn 0.4s ease-out forwards",
        "slide-in-right": "slideInRight 0.4s ease-out forwards",
        pulse: "pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        spin: "spin 1s linear infinite",
      },
      backdropBlur: {
        xs: "2px",
      },
    },
  },
  plugins: [],
};

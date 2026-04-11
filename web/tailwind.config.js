/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // Light theme surfaces
        surface: {
          DEFAULT: "#ffffff",
          raised: "#f8fafc",
          overlay: "#f1f5f9",
        },
        // Dark theme surfaces (Stitch design system)
        dark: {
          base:       "#111125",
          low:        "#1a1a2e",
          container:  "#1e1e32",
          high:       "#28283d",
          highest:    "#333348",
          bright:     "#37374d",
        },
        // Stitch primary
        teal: {
          DEFAULT: "#6fd8c8",
          dim:     "#6fd8c8",
          fixed:   "#8cf5e4",
          on:      "#003731",
        },
      },
      fontFamily: {
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
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

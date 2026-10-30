/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        navy: { DEFAULT: "#1E2761", deep: "#151B3F" },
        teal: { DEFAULT: "#028090", soft: "#00A896" },
        cream: "#F7F5EF",
      },
    },
  },
  plugins: [],
};

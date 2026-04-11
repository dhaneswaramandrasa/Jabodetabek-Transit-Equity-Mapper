import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  weight: ["400", "500", "600"],
});

export const metadata: Metadata = {
  title: "Transit Accessibility Index — Jabodetabek",
  description:
    "Interactive map scoring every kelurahan and H3 hexagon in Jabodetabek on transit accessibility. Explore equity gaps, Gini coefficients, and LISA clusters.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        className={`${inter.variable} ${jetbrainsMono.variable} font-sans bg-slate-50 dark:bg-dark-base text-slate-800 dark:text-[#e2e0fc] antialiased`}
      >
        {children}
      </body>
    </html>
  );
}

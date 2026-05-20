import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Mode Choice & Policy Welfare in Jabodetabek",
  description:
    "Interactive map of transit policy welfare impacts across 7 Jabodetabek zones. MNL/NL/MXL comparison with logsum consumer surplus.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full">
      <body className="h-full bg-cream">{children}</body>
    </html>
  );
}

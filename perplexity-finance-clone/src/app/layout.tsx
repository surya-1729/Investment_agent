import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "OracleIQ Finance",
    template: "%s | OracleIQ Finance",
  },
  description:
    "AI-native finance copilot inspired by Perplexity Finance. Aggregate fundamentals, market data, and news into actionable insight in seconds.",
  keywords: [
    "perplexity finance clone",
    "financial copilot",
    "market intelligence",
    "ai investing assistant",
  ],
  openGraph: {
    title: "OracleIQ Finance – Perplexity Finance SaaS Clone",
    description:
      "Ask natural-language finance questions and receive curated insights, market data, and sourced commentary in real time.",
    type: "website",
  },
  metadataBase: new URL("https://example.com"),
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
      <html lang="en" className="h-full bg-zinc-950">
      <body
          className={`${geistSans.variable} ${geistMono.variable} h-full bg-zinc-50 text-zinc-900 antialiased`}
      >
        {children}
      </body>
    </html>
  );
}

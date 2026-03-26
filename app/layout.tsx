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
  title: "Africa x Caribbean Live — The Global Watch Room",
  description:
    "The ultimate virtual stadium experience. Connect with fans across the globe for the biggest diaspora matchup of the year. Join the live Discord stadium for FIFA World Cup playoff action.",
  openGraph: {
    title: "Africa vs Caribbean — Virtual Watch Party 2026",
    description:
      "One match. One global room. Fans from everywhere. Join the live Discord stadium for FIFA World Cup playoff action.",
    type: "website",
    images: [{ url: "/og-image.png", width: 1200, height: 630 }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Africa vs Caribbean — Virtual Watch Party 2026",
    description:
      "The ultimate virtual stadium. Join fans worldwide for the biggest diaspora matchup of the year.",
    images: ["/og-image.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-slate-950 text-white">
        {children}
      </body>
    </html>
  );
}

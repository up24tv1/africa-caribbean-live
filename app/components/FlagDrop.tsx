"use client";

import { Share2, Users } from "lucide-react";

const flags = ["🇳🇬", "🇯🇲", "🇬🇭", "🇹🇹", "🇸🇳", "🇭🇹", "🇨🇲", "🇧🇧", "🇨🇩", "🇩🇴"];

export default function FlagDrop() {
  return (
    <section className="pb-32 px-4 text-center">
      <div className="max-w-xl mx-auto">
        <h3 className="text-sm font-black text-slate-500 uppercase tracking-[0.3em] mb-12">
          Support Your Nation
        </h3>
        <div className="flex flex-wrap justify-center gap-8 mb-16 grayscale opacity-40 hover:grayscale-0 hover:opacity-100 transition-all duration-700">
          {flags.map((flag, i) => (
            <span
              key={i}
              className="text-5xl hover:scale-125 cursor-default transition-transform inline-block"
            >
              {flag}
            </span>
          ))}
        </div>
        <div className="inline-flex gap-4 items-center">
          <a
            href={`https://x.com/intent/tweet?text=${encodeURIComponent(
              "I just joined the Africa x Caribbean Live global watch room for the FIFA World Cup playoffs! DR Congo, Jamaica, and fans worldwide in one digital stadium."
            )}`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 bg-white/5 border border-white/10 px-6 py-3 rounded-full text-slate-300 font-bold hover:bg-white/10 transition-all"
          >
            <Share2 className="w-4 h-4" /> Share Hub
          </a>
          <div className="h-12 w-px bg-white/10 mx-2" />
          <div className="flex items-center gap-2 text-slate-500 text-sm font-bold italic">
            <Users className="w-4 h-4" /> 12k+ Total Fans
          </div>
        </div>
      </div>
    </section>
  );
}

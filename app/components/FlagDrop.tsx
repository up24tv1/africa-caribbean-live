"use client";

import { Share2, Users } from "lucide-react";

const flags = ["🇳🇬", "🇯🇲", "🇬🇭", "🇹🇹", "🇸🇳", "🇭🇹", "🇨🇲", "🇧🇧", "🇨🇩", "🇩🇴"];
const extraFlags = ["🇪🇬", "🇲🇦", "🇨🇮", "🇦🇬", "🇬🇩", "🇱🇨", "🇬🇾", "🇸🇷", "🇧🇿", "🇹🇬"];
const allFlags = [...flags, ...extraFlags];
// Double for seamless loop
const paradeFlags = [...allFlags, ...allFlags];

export default function FlagDrop() {
  return (
    <section className="pb-32 px-4 text-center overflow-hidden">
      <div className="max-w-4xl mx-auto">
        <h3 className="text-sm font-black text-slate-500 uppercase tracking-[0.3em] mb-8">
          Support Your Nation
        </h3>

        {/* Flag Parade - continuous horizontal scroll */}
        <div className="relative mb-8 overflow-hidden py-4">
          {/* Fade edges */}
          <div className="absolute left-0 top-0 bottom-0 w-20 bg-gradient-to-r from-[#020617] to-transparent z-10 pointer-events-none" />
          <div className="absolute right-0 top-0 bottom-0 w-20 bg-gradient-to-l from-[#020617] to-transparent z-10 pointer-events-none" />

          <div className="flag-parade whitespace-nowrap">
            {paradeFlags.map((flag, i) => (
              <span
                key={i}
                className="inline-block text-6xl mx-4 hover:scale-150 transition-transform duration-300 cursor-default animate-wave"
                style={{ animationDelay: `${i * 0.15}s`, animationPlayState: "paused" }}
                onMouseEnter={(e) => { (e.target as HTMLElement).style.animationPlayState = "running"; }}
                onMouseLeave={(e) => { (e.target as HTMLElement).style.animationPlayState = "paused"; }}
              >
                {flag}
              </span>
            ))}
          </div>
        </div>

        {/* Interactive flag grid */}
        <div className="flex flex-wrap justify-center gap-6 mb-16">
          {flags.map((flag, i) => (
            <div
              key={i}
              className="group relative"
            >
              <div className="absolute -inset-2 rounded-2xl bg-gradient-to-br from-orange-500/20 to-blue-500/20 opacity-0 group-hover:opacity-100 blur-md transition-all duration-500" />
              <span
                className="relative text-5xl hover:scale-125 cursor-default transition-all duration-300 inline-block hover:drop-shadow-[0_0_12px_rgba(249,115,22,0.5)]"
                style={{ animationDelay: `${i * 0.1}s` }}
              >
                {flag}
              </span>
            </div>
          ))}
        </div>

        {/* VS Badge */}
        <div className="flex items-center justify-center gap-6 mb-12">
          <div className="flex items-center gap-3">
            <span className="text-4xl animate-float" style={{ animationDelay: "0s" }}>🇨🇩</span>
            <span className="text-sm font-black text-slate-500 uppercase tracking-widest">DR Congo</span>
          </div>
          <div className="relative">
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-orange-500 to-blue-500 flex items-center justify-center font-black text-sm rotate-glow">
              VS
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-sm font-black text-slate-500 uppercase tracking-widest">Jamaica</span>
            <span className="text-4xl animate-float" style={{ animationDelay: "1s" }}>🇯🇲</span>
          </div>
        </div>

        <div className="inline-flex gap-4 items-center">
          <a
            href={`https://x.com/intent/tweet?text=${encodeURIComponent(
              "I just joined the Africa x Caribbean Live global watch room for the FIFA World Cup playoffs! DR Congo, Jamaica, and fans worldwide in one digital stadium."
            )}`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 bg-white/5 border border-white/10 px-6 py-3 rounded-full text-slate-300 font-bold hover:bg-white/10 hover:border-orange-500/30 transition-all hover:shadow-[0_0_20px_rgba(249,115,22,0.15)]"
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

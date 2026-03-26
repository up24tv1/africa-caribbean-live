"use client";

import { useState } from "react";
import { Flame, Waves, Globe, CheckCircle2, ChevronRight } from "lucide-react";

const DISCORD_INVITE = process.env.NEXT_PUBLIC_DISCORD_INVITE_URL || "https://discord.gg/Vt6P4BFD";

const roles = [
  {
    id: "africa",
    name: "Team Africa",
    desc: "Pride & Power",
    icon: <Flame className="w-8 h-8" />,
    color: "from-orange-600 to-red-700",
    tagline: "Join the Lions & Eagles",
    accent: "text-orange-500",
    bgImage: "/team-africa-card.png",
  },
  {
    id: "caribbean",
    name: "Team Caribbean",
    desc: "Vibes & Skills",
    icon: <Waves className="w-8 h-8" />,
    color: "from-cyan-500 to-blue-600",
    tagline: "Join the Reggae Boyz",
    accent: "text-cyan-400",
    bgImage: "/team-caribbean-card.png",
  },
  {
    id: "neutral",
    name: "Neutral Fan",
    desc: "Just Football",
    icon: <Globe className="w-8 h-8" />,
    color: "from-gray-600 to-slate-800",
    tagline: "Watch the drama unfold",
    accent: "text-slate-400",
    bgImage: null,
  },
];

export default function TribeSelector() {
  const [selectedRole, setSelectedRole] = useState<string | null>(null);

  return (
    <section id="onboarding" className="max-w-6xl mx-auto px-4 py-24 relative z-20">
      <div className="text-center mb-16">
        <h2 className="text-4xl md:text-5xl font-black mb-4 italic uppercase">
          1. Choose Your Tribe
        </h2>
        <p className="text-slate-400 font-medium">
          Select your side to unlock your team-specific channels in Discord.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        {roles.map((role) => (
          <button
            key={role.id}
            onClick={() => setSelectedRole(role.id)}
            className={`group relative overflow-hidden p-8 rounded-3xl border-2 transition-all duration-500 text-left flex flex-col h-full card-3d ${
              selectedRole === role.id
                ? "border-white shadow-[0_0_40px_rgba(255,255,255,0.1)] scale-[1.05]"
                : "border-white/5 hover:border-white/20 bg-white/5"
            }`}
          >
            {role.bgImage && (
              <img
                src={role.bgImage}
                alt=""
                className="absolute inset-0 w-full h-full object-cover opacity-15 group-hover:opacity-25 transition-opacity"
              />
            )}
            <div
              className={`absolute inset-0 bg-gradient-to-br ${role.color} opacity-0 group-hover:opacity-10 transition-opacity`}
            />
            {selectedRole === role.id && (
              <div
                className={`absolute inset-0 bg-gradient-to-br ${role.color} opacity-25`}
              />
            )}

            <div className="relative z-10 flex flex-col h-full">
              <div
                className={`mb-6 inline-flex w-16 h-16 items-center justify-center rounded-2xl bg-white/10 text-white ${
                  selectedRole === role.id ? "scale-110 shadow-lg" : ""
                } transition-transform`}
              >
                {role.icon}
              </div>
              <h3 className="text-3xl font-black mb-1">{role.name}</h3>
              <p
                className={`text-sm font-black uppercase tracking-widest mb-4 ${role.accent}`}
              >
                {role.desc}
              </p>
              <p className="text-slate-400 italic text-sm mb-8 leading-relaxed">
                {role.tagline}
              </p>

              <div className="mt-auto pt-6 border-t border-white/10">
                <div className="flex items-center justify-between text-[10px] font-bold uppercase text-slate-500 tracking-tighter">
                  <span>Access Level</span>
                  <span className="text-white">Full Access</span>
                </div>
              </div>
            </div>
            {selectedRole === role.id && (
              <div className="absolute top-6 right-6 bg-white rounded-full p-1">
                <CheckCircle2 className="w-5 h-5 text-slate-900" />
              </div>
            )}
          </button>
        ))}
      </div>

      <div className="mt-16 text-center">
        <a
          href={selectedRole ? DISCORD_INVITE : undefined}
          target={selectedRole ? "_blank" : undefined}
          rel={selectedRole ? "noopener noreferrer" : undefined}
          className={`group inline-flex items-center gap-4 px-12 py-6 rounded-full text-2xl font-black transition-all ${
            selectedRole
              ? "bg-indigo-600 hover:bg-indigo-500 scale-105 shadow-2xl shadow-indigo-500/40 cursor-pointer"
              : "bg-slate-800 text-slate-500 cursor-not-allowed"
          }`}
          onClick={(e) => {
            if (!selectedRole) e.preventDefault();
          }}
        >
          JOIN THE DISCORD{" "}
          <ChevronRight className="w-8 h-8 transition-transform group-hover:translate-x-1" />
        </a>
        <div className="flex items-center justify-center gap-6 mt-8">
          <div className="flex -space-x-3">
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className="w-8 h-8 rounded-full border-2 border-slate-950 bg-slate-700 flex items-center justify-center overflow-hidden text-xs font-bold"
              >
                {["🇳🇬", "🇯🇲", "🇨🇩", "🇹🇹"][i - 1]}
              </div>
            ))}
          </div>
          <p className="text-slate-500 text-sm font-bold uppercase tracking-widest">
            +420 Fans joined this hour
          </p>
        </div>
      </div>
    </section>
  );
}

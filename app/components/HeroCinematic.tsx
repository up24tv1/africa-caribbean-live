"use client";

import { useState, useEffect } from "react";
import { Users, Bell, ChevronRight } from "lucide-react";

const MATCH_DATE = new Date("2026-03-26T20:00:00Z");

function getTimeLeft(target: Date) {
  const diff = target.getTime() - Date.now();
  if (diff <= 0) return { days: 0, hours: 0, minutes: 0, seconds: 0 };
  return {
    days: Math.floor(diff / (1000 * 60 * 60 * 24)),
    hours: Math.floor((diff / (1000 * 60 * 60)) % 24),
    minutes: Math.floor((diff / (1000 * 60)) % 60),
    seconds: Math.floor((diff / 1000) % 60),
  };
}

export default function HeroCinematic() {
  const [timeLeft, setTimeLeft] = useState(getTimeLeft(MATCH_DATE));
  const [hypeLevel, setHypeLevel] = useState(85);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(getTimeLeft(MATCH_DATE));
      setHypeLevel((prev) =>
        Math.min(100, Math.max(80, prev + (Math.random() * 4 - 2)))
      );
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const isPast = MATCH_DATE.getTime() <= Date.now();

  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center pt-12 pb-24 px-4 overflow-hidden">
      {/* Animated Background Gradients */}
      <div className="absolute top-0 left-0 w-full h-full opacity-30 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-orange-600 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-600 rounded-full blur-[120px] animate-pulse" />
      </div>

      <div className="max-w-6xl mx-auto grid lg:grid-cols-2 gap-12 items-center relative z-10">
        <div className="text-center lg:text-left">
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md px-4 py-1.5 rounded-full border border-white/20 mb-8">
            <span className="w-2 h-2 bg-red-500 rounded-full animate-ping" />
            <span className="text-xs font-bold tracking-widest uppercase">
              {isPast ? "Live Now" : "2026 World Cup Qualifiers"}
            </span>
          </div>

          <h1 className="text-5xl md:text-8xl font-black mb-6 tracking-tighter leading-none uppercase italic">
            <span className="text-white">AFRICA</span> <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-blue-500">
              VERSUS
            </span>{" "}
            <br />
            <span className="text-white">CARIBBEAN</span>
          </h1>

          <p className="text-xl text-slate-300 mb-10 font-medium max-w-xl mx-auto lg:mx-0">
            The ultimate virtual stadium experience. Connect with fans across
            the globe for the biggest diaspora matchup of the year.
          </p>

          {/* Countdown Grid */}
          <div className="flex justify-center lg:justify-start gap-4 mb-12">
            {[
              { label: "Days", val: timeLeft.days },
              { label: "Hrs", val: timeLeft.hours },
              { label: "Min", val: timeLeft.minutes },
              { label: "Sec", val: timeLeft.seconds },
            ].map((unit, i) => (
              <div
                key={i}
                className="bg-white/5 border border-white/10 rounded-xl p-3 min-w-[70px] backdrop-blur-sm"
              >
                <div className="text-3xl font-black">
                  {String(unit.val).padStart(2, "0")}
                </div>
                <div className="text-[10px] uppercase tracking-wider text-slate-400 font-bold">
                  {unit.label}
                </div>
              </div>
            ))}
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
            <a
              href="#onboarding"
              className="bg-orange-600 hover:bg-orange-500 text-white px-8 py-4 rounded-full font-black text-lg transition-all transform hover:scale-105 flex items-center justify-center gap-2"
            >
              JOIN THE PARTY <ChevronRight className="w-5 h-5" />
            </a>
            <a
              href="#remind-me"
              className="bg-white/10 hover:bg-white/20 border border-white/20 text-white px-8 py-4 rounded-full font-black text-lg transition-all flex items-center justify-center gap-2"
            >
              REMIND ME <Bell className="w-5 h-5" />
            </a>
          </div>
        </div>

        {/* Visual Asset: The Poster */}
        <div className="relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-orange-600 to-blue-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200" />
          <div className="relative rounded-2xl overflow-hidden border border-white/10 shadow-2xl">
            <img
              src="/image.png"
              alt="Watch Party Poster"
              className="w-full h-auto transform group-hover:scale-[1.02] transition-transform duration-700"
              onError={(e) => {
                const target = e.target as HTMLImageElement;
                target.style.display = "none";
                if (target.parentElement) {
                  target.parentElement.innerHTML =
                    '<div class="h-[600px] flex items-center justify-center bg-slate-900 text-slate-500 font-bold italic text-center p-8"><div><div class="text-6xl mb-4">⚽</div><div class="text-2xl">AFRICA vs CARIBBEAN</div><div class="text-sm mt-2">March 26, 2026</div></div></div>';
                }
              }}
            />
            {/* Live Overlay UI */}
            <div className="absolute bottom-6 left-6 right-6 p-4 bg-black/60 backdrop-blur-xl rounded-xl border border-white/10 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-orange-600 flex items-center justify-center">
                  <Users className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                    {isPast ? "Live Now" : "Fans Waiting"}
                  </p>
                  <p className="text-sm font-black">2.4k Fans</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                  Current Hype
                </p>
                <div className="w-24 h-1.5 bg-white/10 rounded-full mt-1 overflow-hidden">
                  <div
                    className="h-full bg-orange-500 transition-all duration-1000"
                    style={{ width: `${hypeLevel}%` }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

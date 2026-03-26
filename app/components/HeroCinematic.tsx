"use client";

import { useState, useEffect } from "react";
import { Users, Bell, ChevronRight } from "lucide-react";
import Football3D from "./Football3D";

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
  const [fanCount, setFanCount] = useState(2400);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(getTimeLeft(MATCH_DATE));
      setHypeLevel((prev) =>
        Math.min(100, Math.max(80, prev + (Math.random() * 4 - 2)))
      );
      // Randomly increment fan count
      if (Math.random() < 0.3) {
        setFanCount((prev) => prev + Math.floor(Math.random() * 3));
      }
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
        {/* Extra green glow center */}
        <div className="absolute top-[40%] left-[40%] w-[30%] h-[30%] bg-green-600 rounded-full blur-[150px] opacity-20 animate-pulse" style={{ animationDelay: "1s" }} />
      </div>

      {/* Stadium light sweep overlay */}
      <div className="absolute inset-0 stadium-sweep pointer-events-none" />

      <div className="max-w-6xl mx-auto grid lg:grid-cols-2 gap-12 items-center relative z-10">
        <div className="text-center lg:text-left">
          {/* Live badge */}
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md px-4 py-1.5 rounded-full border border-white/20 mb-8 animate-slide-up">
            <span className="w-2 h-2 bg-red-500 rounded-full animate-ping" />
            <span className="text-xs font-bold tracking-widest uppercase">
              {isPast ? "Live Now" : "2026 World Cup Qualifiers"}
            </span>
          </div>

          {/* Title with staggered animation */}
          <h1 className="text-5xl md:text-8xl font-black mb-6 tracking-tighter leading-none uppercase italic">
            <span className="text-white animate-slide-left inline-block">AFRICA</span>{" "}
            <br />
            <span className="shimmer-text animate-scale-in inline-block delay-200">
              VERSUS
            </span>{" "}
            <br />
            <span className="text-white animate-slide-right inline-block delay-400">CARIBBEAN</span>
          </h1>

          <p className="text-xl text-slate-300 mb-10 font-medium max-w-xl mx-auto lg:mx-0 animate-slide-up delay-500">
            The ultimate virtual stadium experience. Connect with fans across
            the globe for the biggest diaspora matchup of the year.
          </p>

          {/* Countdown Grid with pulse effect */}
          <div className="flex justify-center lg:justify-start gap-4 mb-12 animate-slide-up delay-600">
            {[
              { label: "Days", val: timeLeft.days },
              { label: "Hrs", val: timeLeft.hours },
              { label: "Min", val: timeLeft.minutes },
              { label: "Sec", val: timeLeft.seconds },
            ].map((unit, i) => (
              <div
                key={i}
                className="bg-white/5 border border-white/10 rounded-xl p-3 min-w-[70px] backdrop-blur-sm hover:bg-white/10 hover:border-orange-500/30 transition-all duration-300 hover:scale-105"
              >
                <div className="text-3xl font-black tabular-nums">
                  {String(unit.val).padStart(2, "0")}
                </div>
                <div className="text-[10px] uppercase tracking-wider text-slate-400 font-bold">
                  {unit.label}
                </div>
              </div>
            ))}
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start animate-slide-up delay-700">
            <a
              href="#onboarding"
              className="bg-orange-600 hover:bg-orange-500 text-white px-8 py-4 rounded-full font-black text-lg transition-all transform hover:scale-105 hover:shadow-[0_0_30px_rgba(249,115,22,0.4)] flex items-center justify-center gap-2"
            >
              JOIN THE PARTY <ChevronRight className="w-5 h-5" />
            </a>
            <a
              href="#remind-me"
              className="bg-white/10 hover:bg-white/20 border border-white/20 text-white px-8 py-4 rounded-full font-black text-lg transition-all flex items-center justify-center gap-2 hover:border-white/40"
            >
              REMIND ME <Bell className="w-5 h-5" />
            </a>
          </div>
        </div>

        {/* 3D Football Animation replacing static poster */}
        <div className="relative group animate-scale-in delay-300">
          {/* Rotating glow ring behind */}
          <div className="absolute -inset-8 pointer-events-none">
            <div className="w-full h-full rounded-full rotate-glow" style={{
              background: "conic-gradient(from 0deg, transparent, rgba(249,115,22,0.15), transparent, rgba(59,130,246,0.15), transparent)"
            }} />
          </div>

          <div className="relative rounded-2xl overflow-hidden border border-white/10 shadow-2xl bg-slate-900/50 backdrop-blur-sm">
            {/* 3D Football Canvas */}
            <div className="h-[400px] lg:h-[500px] relative">
              <Football3D />

              {/* Match info overlay */}
              <div className="absolute top-6 left-6 right-6 flex justify-between items-start">
                <div className="bg-black/40 backdrop-blur-md rounded-lg px-4 py-2 border border-white/10">
                  <div className="text-[10px] text-slate-400 uppercase tracking-widest font-bold">Match</div>
                  <div className="text-sm font-black">JAM vs NCL</div>
                </div>
                <div className="bg-black/40 backdrop-blur-md rounded-lg px-4 py-2 border border-white/10">
                  <div className="text-[10px] text-slate-400 uppercase tracking-widest font-bold">Round</div>
                  <div className="text-sm font-black">Playoff R4</div>
                </div>
              </div>

              {/* Floating country flags around the ball */}
              <div className="absolute top-1/4 left-8 text-4xl animate-float opacity-60" style={{ animationDelay: "0s" }}>🇯🇲</div>
              <div className="absolute top-1/3 right-8 text-4xl animate-float opacity-60" style={{ animationDelay: "1.5s" }}>🇨🇩</div>
              <div className="absolute bottom-1/3 left-12 text-3xl animate-float opacity-40" style={{ animationDelay: "0.8s" }}>🇳🇬</div>
              <div className="absolute bottom-1/4 right-12 text-3xl animate-float opacity-40" style={{ animationDelay: "2.2s" }}>🇹🇹</div>
            </div>

            {/* Live Overlay UI */}
            <div className="absolute bottom-6 left-6 right-6 p-4 bg-black/60 backdrop-blur-xl rounded-xl border border-white/10 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-orange-600 flex items-center justify-center animate-pulse">
                  <Users className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                    {isPast ? "Live Now" : "Fans Waiting"}
                  </p>
                  <p className="text-sm font-black tabular-nums">{fanCount.toLocaleString()} Fans</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                  Current Hype
                </p>
                <div className="w-24 h-1.5 bg-white/10 rounded-full mt-1 overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-1000"
                    style={{
                      width: `${hypeLevel}%`,
                      background: `linear-gradient(90deg, #F97316, #EF4444)`,
                    }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce opacity-40">
        <div className="w-6 h-10 rounded-full border-2 border-white/30 flex justify-center pt-2">
          <div className="w-1 h-3 bg-white/60 rounded-full animate-pulse" />
        </div>
      </div>
    </section>
  );
}

"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";

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

function CountdownUnit({ value, label }: { value: number; label: string }) {
  return (
    <div className="flex flex-col items-center">
      <div className="glass rounded-xl w-16 h-16 sm:w-20 sm:h-20 flex items-center justify-center">
        <span className="text-2xl sm:text-3xl font-bold text-gold">
          {String(value).padStart(2, "0")}
        </span>
      </div>
      <span className="text-xs sm:text-sm text-text-dim mt-2 uppercase tracking-widest">
        {label}
      </span>
    </div>
  );
}

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.6, ease: "easeOut" as const },
  }),
};

export default function Hero() {
  const [timeLeft, setTimeLeft] = useState(getTimeLeft(MATCH_DATE));

  useEffect(() => {
    const timer = setInterval(() => setTimeLeft(getTimeLeft(MATCH_DATE)), 1000);
    return () => clearInterval(timer);
  }, []);

  const isPast = MATCH_DATE.getTime() <= Date.now();

  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center px-4 py-20 bg-grid overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-green/5 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] rounded-full bg-teal/5 blur-[100px] pointer-events-none" />

      <motion.div
        className="relative z-10 flex flex-col items-center text-center max-w-4xl mx-auto"
        initial="hidden"
        animate="visible"
      >
        {/* Badge */}
        <motion.div custom={0} variants={fadeUp}>
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass text-sm font-medium text-gold uppercase tracking-wider">
            <span className="w-2 h-2 rounded-full bg-red animate-pulse-live" />
            {isPast ? "Live Now" : "Live Watch Party — March 26"}
          </span>
        </motion.div>

        {/* Title */}
        <motion.h1
          custom={1}
          variants={fadeUp}
          className="mt-8 font-black tracking-tight leading-none"
        >
          <span className="block md:inline text-4xl md:text-6xl lg:text-8xl gradient-text">AFRICA</span>
          <span className="hidden md:inline text-text-dim mx-3 lg:mx-4 text-4xl lg:text-6xl">x</span>
          <span className="block md:inline text-4xl md:text-6xl lg:text-8xl gradient-text-teal mt-1 md:mt-0">CARIBBEAN</span>
          <span className="text-foreground text-2xl sm:text-4xl lg:text-5xl font-bold mt-3 block">
            LIVE
          </span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          custom={2}
          variants={fadeUp}
          className="mt-6 text-lg sm:text-xl text-text-dim max-w-2xl"
        >
          The Global Watch Room. One match. One global room. Fans from everywhere.
          Pay what you feel, represent your country, experience the match together live.
        </motion.p>

        {/* Countdown */}
        <motion.div custom={3} variants={fadeUp} className="mt-10">
          {isPast ? (
            <p className="text-2xl font-bold text-green">The match is LIVE!</p>
          ) : (
            <div className="flex gap-4 sm:gap-6">
              <CountdownUnit value={timeLeft.days} label="Days" />
              <CountdownUnit value={timeLeft.hours} label="Hours" />
              <CountdownUnit value={timeLeft.minutes} label="Min" />
              <CountdownUnit value={timeLeft.seconds} label="Sec" />
            </div>
          )}
        </motion.div>

        {/* CTA */}
        <motion.div custom={4} variants={fadeUp} className="mt-10 flex flex-col sm:flex-row gap-4">
          <a
            href="#join"
            className="px-8 py-4 rounded-full bg-green text-white font-bold text-lg hover:brightness-110 transition-all glow-green"
          >
            Join the Watch Room
          </a>
          <a
            href="#matches"
            className="px-8 py-4 rounded-full glass text-foreground font-medium text-lg hover:bg-white/5 transition-all"
          >
            View Matches
          </a>
        </motion.div>
      </motion.div>
    </section>
  );
}

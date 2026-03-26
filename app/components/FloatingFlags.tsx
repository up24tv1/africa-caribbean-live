"use client";

import { useEffect, useState } from "react";

const ALL_FLAGS = [
  "🇯🇲", "🇨🇩", "🇳🇬", "🇬🇭", "🇹🇹", "🇸🇳", "🇭🇹", "🇨🇲", "🇧🇧", "🇩🇴",
  "🇪🇬", "🇲🇦", "🇨🇮", "🇦🇬", "🇬🇩", "🇱🇨", "🇬🇾", "🇸🇷", "🇧🇿", "🇹🇬",
];

interface FlagParticle {
  id: number;
  flag: string;
  x: number;
  delay: number;
  duration: number;
  size: number;
  wobble: number;
}

export default function FloatingFlags() {
  const [particles, setParticles] = useState<FlagParticle[]>([]);

  useEffect(() => {
    const flags: FlagParticle[] = Array.from({ length: 25 }, (_, i) => ({
      id: i,
      flag: ALL_FLAGS[i % ALL_FLAGS.length],
      x: Math.random() * 100,
      delay: Math.random() * 20,
      duration: 12 + Math.random() * 18,
      size: 20 + Math.random() * 28,
      wobble: Math.random() * 40 - 20,
    }));
    setParticles(flags);
  }, []);

  if (particles.length === 0) return null;

  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden" aria-hidden="true">
      {particles.map((p) => (
        <span
          key={p.id}
          className="absolute"
          style={{
            left: `${p.x}%`,
            fontSize: `${p.size}px`,
            animation: `flagFall ${p.duration}s linear ${p.delay}s infinite`,
            opacity: 0.12,
            filter: "blur(0.5px)",
          }}
        >
          {p.flag}
        </span>
      ))}
    </div>
  );
}

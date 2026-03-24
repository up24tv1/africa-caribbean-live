"use client";

import { motion } from "framer-motion";

interface Match {
  homeTeam: string;
  homeFlag: string;
  awayTeam: string;
  awayFlag: string;
  date: string;
  time: string;
  stage: string;
  status: "upcoming" | "live" | "coming-soon";
}

const matches: Match[] = [
  {
    homeTeam: "Jamaica",
    homeFlag: "\u{1F1EF}\u{1F1F2}",
    awayTeam: "New Caledonia",
    awayFlag: "\u{1F1F3}\u{1F1E8}",
    date: "March 26, 2026",
    time: "8:00 PM UTC",
    stage: "FIFA World Cup Playoff — Round 1",
    status: "upcoming",
  },
  {
    homeTeam: "DR Congo",
    homeFlag: "\u{1F1E8}\u{1F1E9}",
    awayTeam: "Winner of Round 1",
    awayFlag: "\u{1F3C6}",
    date: "March 31, 2026",
    time: "TBD",
    stage: "FIFA World Cup Playoff — Final Round",
    status: "coming-soon",
  },
];

function MatchCardItem({ match, index }: { match: Match; index: number }) {
  const isLive = match.status === "live";
  const isUpcoming = match.status === "upcoming";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.15, duration: 0.5 }}
      className={`glass rounded-2xl p-6 sm:p-8 flex-1 relative overflow-hidden ${
        isUpcoming ? "glow-green" : ""
      }`}
    >
      {/* Status badge */}
      <div className="flex items-center justify-between mb-6">
        <span className="text-sm text-text-dim uppercase tracking-wider font-medium">
          {match.stage}
        </span>
        {isLive && (
          <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-red/20 text-red text-xs font-bold uppercase">
            <span className="w-1.5 h-1.5 rounded-full bg-red animate-pulse-live" />
            Live
          </span>
        )}
        {isUpcoming && (
          <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-green/20 text-green text-xs font-bold uppercase">
            Next Up
          </span>
        )}
        {match.status === "coming-soon" && (
          <span className="px-3 py-1 rounded-full bg-gold/10 text-gold text-xs font-bold uppercase">
            Coming Soon
          </span>
        )}
      </div>

      {/* Teams */}
      <div className="flex items-center justify-between gap-4">
        <div className="flex flex-col items-center text-center flex-1">
          <span className="text-4xl sm:text-5xl">{match.homeFlag}</span>
          <span className="mt-2 text-lg sm:text-xl font-bold">{match.homeTeam}</span>
        </div>
        <div className="flex flex-col items-center">
          <span className="text-2xl font-black text-text-dim">VS</span>
        </div>
        <div className="flex flex-col items-center text-center flex-1">
          <span className="text-4xl sm:text-5xl">{match.awayFlag}</span>
          <span className="mt-2 text-lg sm:text-xl font-bold">{match.awayTeam}</span>
        </div>
      </div>

      {/* Date / Time */}
      <div className="mt-6 flex items-center justify-center gap-3 text-sm text-text-dim">
        <span>{match.date}</span>
        <span className="w-1 h-1 rounded-full bg-text-dim" />
        <span>{match.time}</span>
      </div>
    </motion.div>
  );
}

export default function MatchCards() {
  return (
    <section id="matches" className="px-4 py-20 max-w-5xl mx-auto">
      <h2 className="text-3xl sm:text-4xl font-black text-center mb-12">
        The <span className="gradient-text">Matches</span>
      </h2>
      <div className="grid md:grid-cols-2 gap-6">
        {matches.map((match, i) => (
          <MatchCardItem key={match.homeTeam} match={match} index={i} />
        ))}
      </div>
    </section>
  );
}

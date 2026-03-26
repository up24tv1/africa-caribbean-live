"use client";

import { MessageSquare, Trophy, Zap, Star, Play } from "lucide-react";

export default function FeatureHighlights() {
  return (
    <section className="bg-white/5 py-24 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div>
            <h2 className="text-4xl font-black mb-8 leading-tight italic uppercase">
              Experience the match <br /> like never{" "}
              <span className="text-orange-500">before.</span>
            </h2>
            <div className="space-y-4">
              {[
                {
                  icon: <MessageSquare className="text-orange-400" />,
                  title: "Live Fan Banter",
                  desc: "Settle the debate once and for all in dedicated fan voice rooms.",
                },
                {
                  icon: <Trophy className="text-yellow-400" />,
                  title: "Prediction League",
                  desc: "Climb the leaderboard and win custom digital badges.",
                },
                {
                  icon: <Zap className="text-cyan-400" />,
                  title: "Halftime Trivia",
                  desc: "Win instant prizes during the 15-minute halftime rush.",
                },
                {
                  icon: <Star className="text-indigo-400" />,
                  title: "Exclusive Rewards",
                  desc: "Giveaways for small prizes like gift cards and custom wallpapers.",
                },
              ].map((item, i) => (
                <div
                  key={i}
                  className="flex gap-5 p-6 rounded-2xl bg-slate-900 border border-white/5 hover:border-white/20 transition-all"
                >
                  <div className="p-3 bg-white/5 rounded-xl h-fit">
                    {item.icon}
                  </div>
                  <div>
                    <h4 className="font-black text-xl mb-1">{item.title}</h4>
                    <p className="text-slate-400 leading-relaxed text-sm">
                      {item.desc}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* How It Works */}
          <div className="relative">
            <div className="bg-slate-900 border border-white/10 rounded-3xl p-10 shadow-2xl overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-orange-600/10 blur-3xl rounded-full" />
              <div className="relative z-10">
                <h3 className="text-2xl font-black mb-6 flex items-center gap-3">
                  <Play className="fill-orange-500 text-orange-500" /> HOW IT
                  WORKS
                </h3>
                <div className="space-y-6">
                  <div className="p-4 bg-white/5 rounded-2xl border border-white/5">
                    <p className="font-bold text-white mb-2">1. Sync Clocks</p>
                    <p className="text-sm text-slate-400">
                      At kickoff, we provide a master timer to ensure all fans
                      are reacting to the same moment.
                    </p>
                  </div>
                  <div className="p-4 bg-white/5 rounded-2xl border border-white/5">
                    <p className="font-bold text-white mb-2">
                      2. Watch Legally
                    </p>
                    <p className="text-sm text-slate-400 italic font-medium">
                      No match video is streamed in Discord.
                    </p>
                    <p className="text-sm text-slate-400 mt-2">
                      Use your local broadcaster (FIFA+, DStv, SportsMax) while
                      staying connected with us.
                    </p>
                  </div>
                  <div className="p-4 bg-white/5 rounded-2xl border border-white/5">
                    <p className="font-bold text-white mb-2">3. React Live</p>
                    <p className="text-sm text-slate-400">
                      The Discord becomes the &ldquo;stadium noise.&rdquo; Use
                      text channels or join the Voice Lounges.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

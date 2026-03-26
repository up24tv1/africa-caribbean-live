"use client";

import { useState } from "react";
import { Bell, CheckCircle2 } from "lucide-react";

export default function EmailCapture() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleJoin = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) setSubmitted(true);
  };

  return (
    <section id="remind-me" className="max-w-4xl mx-auto px-4 py-32">
      <div className="relative bg-gradient-to-br from-orange-600/30 via-slate-900 to-blue-600/30 rounded-[40px] p-12 md:p-20 border border-white/10 text-center overflow-hidden">
        <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-3xl -z-10" />

        {!submitted ? (
          <>
            <div className="inline-block p-4 bg-white/5 rounded-full mb-8">
              <Bell className="w-10 h-10 text-orange-500" />
            </div>
            <h2 className="text-4xl md:text-5xl font-black mb-6 italic uppercase tracking-tight">
              The Hype starts <br className="hidden md:block" /> 1 hour before
              kickoff.
            </h2>
            <p className="text-slate-300 mb-12 max-w-lg mx-auto text-lg font-medium leading-relaxed">
              Join 2,000+ fans on our priority notification list. Get the match
              blueprints, legal links, and secret prediction poll.
            </p>
            <form
              onSubmit={handleJoin}
              className="flex flex-col md:flex-row gap-4 max-w-lg mx-auto"
            >
              <input
                type="email"
                required
                placeholder="your@email.com"
                className="bg-white/5 border border-white/10 rounded-full px-8 py-5 flex-grow outline-none focus:border-orange-500 transition-all font-bold text-lg"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <button
                type="submit"
                className="bg-white text-black font-black px-10 py-5 rounded-full hover:bg-slate-200 transition-all uppercase tracking-tighter whitespace-nowrap shadow-xl"
              >
                Remind Me
              </button>
            </form>
            <p className="mt-6 text-slate-500 text-xs font-bold uppercase tracking-[0.2em]">
              Zero Spam &bull; Only Match Vibes
            </p>
          </>
        ) : (
          <div>
            <div className="w-20 h-20 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-8 shadow-[0_0_40px_rgba(34,197,94,0.3)]">
              <CheckCircle2 className="w-10 h-10 text-white" />
            </div>
            <h2 className="text-4xl font-black mb-4 italic uppercase">
              WELCOME TO THE TEAM!
            </h2>
            <p className="text-slate-300 text-lg mb-10">
              We&apos;ll send your invite package shortly. Check your inbox.
            </p>
            <button
              onClick={() => setSubmitted(false)}
              className="text-slate-500 hover:text-white transition-colors underline underline-offset-4 font-bold text-sm"
            >
              Use a different email
            </button>
          </div>
        )}
      </div>
    </section>
  );
}

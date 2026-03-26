"use client";

import { motion } from "framer-motion";

const DISCORD_INVITE = process.env.NEXT_PUBLIC_DISCORD_INVITE_URL || "https://discord.gg/Vt6P4BFD";

const steps = [
  {
    number: "1",
    title: "Join the Discord Server",
    description: "Click the button below to join the Africa x Caribbean Live server.",
  },
  {
    number: "2",
    title: "Go to #prove-your-country",
    description:
      "Tell us your country, your city, and where you are watching from. We will assign your passport role.",
  },
  {
    number: "3",
    title: "Pick Your Voice Room",
    description:
      "Jamaica room? DR Congo room? Neutral room? Jump in and rep your flag on match day.",
  },
  {
    number: "4",
    title: "Drop Your Predictions",
    description:
      "Head to #predictions before kickoff. Call the score, first goal scorer, and man of the match.",
  },
];

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.5 },
  }),
};

export default function SuccessPage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-4 py-20 bg-grid">
      {/* Background glow */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[500px] h-[500px] rounded-full bg-green/8 blur-[120px] pointer-events-none" />

      <motion.div
        className="relative z-10 max-w-xl w-full text-center"
        initial="hidden"
        animate="visible"
      >
        {/* Success icon */}
        <motion.div custom={0} variants={fadeUp} className="text-6xl mb-6">
          {"🎉"}
        </motion.div>

        <motion.h1
          custom={1}
          variants={fadeUp}
          className="text-4xl sm:text-5xl font-black"
        >
          You&apos;re <span className="gradient-text">In!</span>
        </motion.h1>

        <motion.p
          custom={2}
          variants={fadeUp}
          className="mt-4 text-lg text-text-dim"
        >
          Your payment is confirmed. Welcome to the Global Watch Room. Follow these steps to get set up.
        </motion.p>

        {/* Join Discord CTA */}
        <motion.div custom={3} variants={fadeUp} className="mt-8">
          <a
            href={DISCORD_INVITE}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-3 px-8 py-4 rounded-full bg-[#5865F2] text-white font-bold text-lg hover:brightness-110 transition-all shadow-lg shadow-[#5865F2]/20"
          >
            <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.095 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.095 2.157 2.42 0 1.333-.947 2.418-2.157 2.418z" />
            </svg>
            Join the Discord Server
          </a>
        </motion.div>

        {/* Steps */}
        <motion.div custom={4} variants={fadeUp} className="mt-12 text-left space-y-4">
          {steps.map((step) => (
            <div key={step.number} className="glass rounded-xl p-4 flex gap-4 items-start">
              <div className="w-8 h-8 rounded-full bg-green/20 text-green flex items-center justify-center font-bold text-sm shrink-0">
                {step.number}
              </div>
              <div>
                <h3 className="font-bold text-sm">{step.title}</h3>
                <p className="text-sm text-text-dim mt-0.5">{step.description}</p>
              </div>
            </div>
          ))}
        </motion.div>

        {/* Share on X */}
        <motion.div custom={5} variants={fadeUp} className="mt-10">
          <a
            href={`https://x.com/intent/tweet?text=${encodeURIComponent(
              "I just joined the Africa x Caribbean Live global watch room for the FIFA World Cup playoffs! DR Congo, Jamaica, and fans worldwide in one digital stadium. 🌍⚽🔥"
            )}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full glass text-sm font-medium hover:bg-white/5 transition-all"
          >
            Share on X
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
            </svg>
          </a>
        </motion.div>
      </motion.div>
    </main>
  );
}

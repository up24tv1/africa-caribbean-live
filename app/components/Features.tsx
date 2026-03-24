"use client";

import { motion } from "framer-motion";

const features = [
  {
    icon: "\u{1F3DF}\u{FE0F}",
    title: "The Digital Stadium",
    description:
      "Main Stage Channel with hosts, co-hosts, and featured fan speakers. Feel the energy of a real stadium.",
  },
  {
    icon: "\u{1F30D}",
    title: "Country Voice Rooms",
    description:
      "DR Congo room. Jamaica room. Caribbean room. Diaspora room. Neutral room. Rep your flag.",
  },
  {
    icon: "\u{1F3AF}",
    title: "Prediction Game",
    description:
      "Call the first goal scorer, final score, and man of the match. Winners get free next-event access.",
  },
  {
    icon: "\u{1F399}\u{FE0F}",
    title: "Halftime Takeover",
    description:
      "Best reactions go on stage at halftime. Best Jamaica voice. Best Congo voice. Best neutral take.",
  },
  {
    icon: "\u{1F525}",
    title: "Fan Battles",
    description:
      "Best chant battle. Best flag setup. Best diaspora story. Fastest goal reaction. Best meme before 60'.",
  },
  {
    icon: "\u{1F4B0}",
    title: "Donation Wall",
    description:
      'Live appreciation wall: "Mathieu from Austin gave $5 for Congo pride." Your name. Your city. Your flag.',
  },
  {
    icon: "\u{1F3C6}",
    title: "Post-Match Locker Room",
    description:
      "Instant fan reactions, clips, screenshots, and vote for the next matchup event.",
  },
  {
    icon: "\u{1F6C2}",
    title: "Passport Onboarding",
    description:
      'Choose your country, language, and city. Get auto-assigned: "Kinshasa," "Kingston," "Paris Congolais."',
  },
];

export default function Features() {
  return (
    <section className="px-4 py-20 max-w-5xl mx-auto">
      <div className="text-center mb-12">
        <h2 className="text-3xl sm:text-4xl font-black">
          More Than a <span className="gradient-text-teal">Watch Party</span>
        </h2>
        <p className="mt-4 text-text-dim text-lg max-w-xl mx-auto">
          A digital stadium with culture, identity, and live football energy. Here is what you get.
        </p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {features.map((feature, i) => (
          <motion.div
            key={feature.title}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.05, duration: 0.5 }}
            className="glass rounded-2xl p-5"
          >
            <span className="text-3xl">{feature.icon}</span>
            <h3 className="mt-3 text-base font-bold">{feature.title}</h3>
            <p className="mt-2 text-sm text-text-dim leading-relaxed">{feature.description}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}

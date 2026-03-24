"use client";

import { motion } from "framer-motion";

interface Tier {
  name: string;
  amount: string;
  cents: number;
  description: string;
  featured?: boolean;
  link: string;
}

const tiers: Tier[] = [
  {
    name: "Supporter",
    amount: "$1",
    cents: 100,
    description: "Access the global watch room, text channels, and voice rooms.",
    link: "#", // Replace with Stripe Payment Link
  },
  {
    name: "Super Fan",
    amount: "$3",
    cents: 300,
    description: "Everything in Supporter + highlighted role and prediction game entry.",
    link: "#",
  },
  {
    name: "Fam",
    amount: "$5",
    cents: 500,
    description: "Everything in Super Fan + halftime stage priority and pinned shoutout.",
    featured: true,
    link: "#",
  },
  {
    name: "Captain",
    amount: "$10",
    cents: 1000,
    description: "Everything in Fam + Donation Wall feature, digital badge, and free next event.",
    link: "#",
  },
];

export default function PaySection() {
  return (
    <section id="join" className="px-4 py-20 max-w-5xl mx-auto">
      <div className="text-center mb-12">
        <h2 className="text-3xl sm:text-4xl font-black">
          Pay What You <span className="gradient-text">Feel</span>
        </h2>
        <p className="mt-4 text-text-dim text-lg max-w-xl mx-auto">
          Support the room, join the global crowd. Minimum $1. Every contribution gets you full access.
        </p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {tiers.map((tier, i) => (
          <motion.div
            key={tier.name}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1, duration: 0.5 }}
            className={`rounded-2xl p-6 flex flex-col relative ${
              tier.featured ? "glass-gold glow-gold" : "glass"
            }`}
          >
            {tier.featured && (
              <span className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-gold text-black text-xs font-bold uppercase">
                Most Popular
              </span>
            )}

            <div className="mb-4">
              <span className="text-sm text-text-dim uppercase tracking-wider font-medium">
                {tier.name}
              </span>
              <div className="mt-2 text-4xl font-black text-foreground">{tier.amount}</div>
            </div>

            <p className="text-sm text-text-dim flex-1">{tier.description}</p>

            <a
              href={tier.link}
              className={`mt-6 block text-center py-3 rounded-full font-bold text-sm transition-all ${
                tier.featured
                  ? "bg-gold text-black hover:brightness-110"
                  : "bg-white/10 text-foreground hover:bg-white/15"
              }`}
            >
              Join for {tier.amount}
            </a>
          </motion.div>
        ))}
      </div>

      <p className="text-center mt-8 text-sm text-text-dim">
        Powered by Stripe. Secure payments. Instant Discord access after payment.
      </p>
    </section>
  );
}

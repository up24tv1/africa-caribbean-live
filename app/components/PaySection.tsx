"use client";

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
    description:
      "Access the global watch room, text channels, and voice rooms.",
    link: "https://buy.stripe.com/4gM28r7E251Y5iIcGO4gg0o",
  },
  {
    name: "Super Fan",
    amount: "$3",
    cents: 300,
    description:
      "Everything in Supporter + highlighted role and prediction game entry.",
    link: "https://buy.stripe.com/aFa28r4rQbqmaD2fT04gg0p",
  },
  {
    name: "Fam",
    amount: "$5",
    cents: 500,
    description:
      "Everything in Super Fan + halftime stage priority and pinned shoutout.",
    featured: true,
    link: "https://buy.stripe.com/fZu00jgay9ie5iI8qy4gg0q",
  },
  {
    name: "Captain",
    amount: "$10",
    cents: 1000,
    description:
      "Everything in Fam + Donation Wall feature, digital badge, and free next event.",
    link: "https://buy.stripe.com/8x2dR94rQ3XUfXm9uC4gg0r",
  },
];

export default function PaySection() {
  return (
    <section id="join" className="px-4 py-24 max-w-5xl mx-auto">
      <div className="text-center mb-12">
        <h2 className="text-4xl md:text-5xl font-black italic uppercase mb-4">
          Support the{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-yellow-400">
            Stadium
          </span>
        </h2>
        <p className="text-slate-400 text-lg max-w-xl mx-auto font-medium">
          Discord access is free. Optional donations unlock premium roles, badges, and perks.
        </p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {tiers.map((tier) => (
          <div
            key={tier.name}
            className={`rounded-2xl p-6 flex flex-col relative border transition-all hover:scale-[1.02] ${
              tier.featured
                ? "bg-orange-500/5 border-orange-500/30 shadow-[0_0_40px_rgba(249,115,22,0.1)]"
                : "bg-white/5 border-white/10 hover:border-white/20"
            }`}
          >
            {tier.featured && (
              <span className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-orange-500 text-white text-xs font-bold uppercase">
                Most Popular
              </span>
            )}

            <div className="mb-4">
              <span className="text-sm text-slate-500 uppercase tracking-wider font-bold">
                {tier.name}
              </span>
              <div className="mt-2 text-4xl font-black text-white">
                {tier.amount}
              </div>
            </div>

            <p className="text-sm text-slate-400 flex-1 leading-relaxed">
              {tier.description}
            </p>

            <a
              href={tier.link}
              className={`mt-6 block text-center py-3 rounded-full font-bold text-sm transition-all ${
                tier.featured
                  ? "bg-orange-500 text-white hover:bg-orange-400"
                  : "bg-white/10 text-white hover:bg-white/15"
              }`}
            >
              Donate {tier.amount}
            </a>
          </div>
        ))}
      </div>

      <p className="text-center mt-8 text-sm text-slate-500">
        Powered by Stripe. Secure payments. Premium roles assigned automatically.
      </p>
    </section>
  );
}

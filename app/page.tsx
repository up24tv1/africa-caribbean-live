import Hero from "./components/Hero";
import MatchCards from "./components/MatchCard";
import PaySection from "./components/PaySection";
import Features from "./components/Features";
import Footer from "./components/Footer";

export default function Home() {
  return (
    <main className="flex-1">
      <Hero />
      <MatchCards />
      <Features />
      <PaySection />
      <Footer />
    </main>
  );
}

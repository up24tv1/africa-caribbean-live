import HeroCinematic from "./components/HeroCinematic";
import TribeSelector from "./components/TribeSelector";
import FeatureHighlights from "./components/FeatureHighlights";
import PaySection from "./components/PaySection";
import EmailCapture from "./components/EmailCapture";
import FlagDrop from "./components/FlagDrop";
import Footer from "./components/Footer";
import FloatingFlags from "./components/FloatingFlags";

export default function Home() {
  return (
    <main className="flex-1 relative">
      <FloatingFlags />
      <HeroCinematic />
      <TribeSelector />
      <FeatureHighlights />
      <PaySection />
      <EmailCapture />
      <FlagDrop />
      <Footer />
    </main>
  );
}

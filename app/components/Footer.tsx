export default function Footer() {
  return (
    <footer className="border-t border-white/5 py-16 px-4 text-center">
      <div className="flex justify-center gap-8 mb-8 opacity-50">
        <div className="text-xl font-black italic">FIFA</div>
        <div className="text-xl font-black italic">CAF</div>
        <div className="text-xl font-black italic">CONCACAF</div>
      </div>
      <p className="mb-4 font-black uppercase tracking-[0.5em] text-[10px] text-orange-500">
        Virtual Watch Party 2026
      </p>
      <p className="text-sm italic text-slate-600 max-w-md mx-auto">
        Created by fans, for fans. This event is not officially affiliated with
        FIFA or any national football association.
      </p>
      <p className="mt-6 text-slate-700 text-xs">
        A{" "}
        <span className="text-slate-400 font-medium">Leopards USA</span>{" "}
        experience
      </p>
    </footer>
  );
}

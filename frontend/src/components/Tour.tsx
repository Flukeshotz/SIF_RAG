import { useState } from 'react';

interface TourProps {
  onComplete: () => void;
}

export default function Tour({ onComplete }: TourProps) {
  const [step, setStep] = useState(1);
  const totalSteps = 4;

  const steps = [
    {
      title: "Welcome to SIF Copilot",
      desc: "An institutional-grade RAG workspace. Let's take a quick tour.",
      icon: "rocket_launch"
    },
    {
      title: "1. The Search Engine",
      desc: "Ask any question about Specialized Investment Funds. We'll search across 2,000+ indexed SEBI documents, Factsheets, and KIMs.",
      icon: "search"
    },
    {
      title: "2. Verifiable Citations",
      desc: "Every claim is backed by a [Source N] pill. The LLM cannot hallucinate answers without providing a direct pointer to the source chunk.",
      icon: "verified"
    },
    {
      title: "3. Evidence Explorer",
      desc: "Clicking a citation opens the Evidence Explorer, revealing the exact document, page number, and text used to generate the answer.",
      icon: "menu_book"
    }
  ];

  const handleNext = () => {
    if (step < totalSteps) setStep(step + 1);
    else onComplete();
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="bg-[#051424] border border-[#152238] rounded-2xl shadow-2xl p-8 max-w-md w-full relative animate-scale-in">
        <button 
          onClick={onComplete}
          className="absolute top-4 right-4 text-on-surface-variant hover:text-on-surface p-1 rounded-full bg-[#020617]"
        >
          <span className="material-symbols-outlined text-sm block">close</span>
        </button>
        
        <div className="flex flex-col items-center text-center">
          <div className="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center mb-6 border border-primary/30">
            <span className="material-symbols-outlined text-3xl text-primary">{steps[step-1].icon}</span>
          </div>
          
          <h2 className="font-headline-lg text-2xl text-on-surface mb-4">{steps[step-1].title}</h2>
          <p className="text-on-surface-variant mb-8 leading-relaxed font-body-lg">
            {steps[step-1].desc}
          </p>
          
          <div className="flex items-center justify-between w-full mt-4">
            <div className="flex gap-2">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className={`w-2 h-2 rounded-full ${step === i ? 'bg-primary' : 'bg-[#152238]'}`}></div>
              ))}
            </div>
            
            <button 
              onClick={handleNext}
              className="bg-primary text-on-primary px-6 py-2 rounded-lg font-semibold hover:bg-primary/90 transition-colors shadow-md flex items-center gap-2"
            >
              {step === totalSteps ? 'Get Started' : 'Next'}
              {step !== totalSteps && <span className="material-symbols-outlined text-sm">arrow_forward</span>}
            </button>
          </div>
          
          {step !== totalSteps && (
             <button onClick={onComplete} className="text-sm text-on-surface-variant underline mt-4 hover:text-on-surface transition-colors">
               Skip Tour
             </button>
          )}
        </div>
      </div>
    </div>
  );
}

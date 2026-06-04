import { useState } from 'react';

export default function Architecture() {
  const [activeStep, setActiveStep] = useState<number>(0);

  const pipeline = [
    {
      title: "Document Acquisition",
      icon: "cloud_download",
      detail: "The pipeline monitors SEBI portals, AMC websites, and repository feeds. It pulls 2,000+ authoritative PDFs including ISIDs, KIMs, and Master Circulars while explicitly filtering out marketing materials."
    },
    {
      title: "Processing & OCR",
      icon: "document_scanner",
      detail: "Raw PDFs are processed using PyMuPDF and Tabula. Scanned documents undergo OCR. Crucially, noise (like fund manager commentary and disclosures) is sanitized to prevent LLM hallucinations."
    },
    {
      title: "Contextual Chunking",
      icon: "segment",
      detail: "Documents are split into overlapping chunks, maintaining strict hierarchical metadata (Section, Title, Page). Tables are preserved as indivisible objects to prevent data tearing."
    },
    {
      title: "Embedding Generation",
      icon: "data_object",
      detail: "Chunks are passed through the BAAI/bge-small-en-v1.5 embedding model to generate 384-dimensional dense vectors representing the semantic meaning of the text."
    },
    {
      title: "Vector Database (Qdrant)",
      icon: "database",
      detail: "Vectors are stored in Qdrant alongside their full metadata payloads. This allows for hyper-fast cosine similarity search with hard metadata filtering (e.g., only search 'SEBI Circulars')."
    },
    {
      title: "Generation Engine (Groq)",
      icon: "memory",
      detail: "The top 5 chunks are retrieved and assembled into a deterministic context window. A strict prompt forces Llama-3.1-8b (running on Groq LPUs) to synthesize an answer exclusively from the provided chunks, eliminating hallucination."
    }
  ];

  return (
    <div className="p-lg lg:p-xl max-w-5xl mx-auto w-full pb-32">
      <div className="mb-lg border-b border-[#152238] pb-md">
        <h1 className="font-headline-lg text-headline-lg text-on-surface mb-2 flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-3xl">route</span>
          How SIF Copilot Works
        </h1>
        <p className="text-on-surface-variant text-lg max-w-3xl">
          SIF Copilot employs a "Hybrid Imperative" RAG architecture. It completely separates qualitative text from quantitative tables, ensuring 100% verifiable citations.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 relative">
        
        {/* Pipeline Steps */}
        <div className="lg:col-span-1 space-y-3 relative z-10">
          {pipeline.map((step, idx) => (
            <button
              key={idx}
              onClick={() => setActiveStep(idx)}
              className={`w-full text-left p-4 rounded-xl border transition-all duration-300 flex items-center gap-4 group ${
                activeStep === idx 
                  ? 'bg-[#020617] border-primary shadow-[0_0_15px_rgba(173,198,255,0.15)]' 
                  : 'bg-surface-container-low border-[#152238] hover:border-primary/50'
              }`}
            >
              <div className={`w-10 h-10 rounded-full flex items-center justify-center transition-colors ${
                activeStep === idx ? 'bg-primary text-on-primary' : 'bg-surface-variant text-on-surface-variant group-hover:text-primary'
              }`}>
                <span className="material-symbols-outlined">{step.icon}</span>
              </div>
              <div className="flex-1">
                <h3 className={`font-semibold ${activeStep === idx ? 'text-primary' : 'text-on-surface'}`}>
                  {idx + 1}. {step.title}
                </h3>
              </div>
              <span className={`material-symbols-outlined text-sm transition-opacity ${activeStep === idx ? 'opacity-100 text-primary' : 'opacity-0'}`}>
                arrow_forward_ios
              </span>
            </button>
          ))}
        </div>

        {/* Storytelling Canvas */}
        <div className="lg:col-span-2">
          <div className="bg-[#020617] border border-[#152238] rounded-2xl p-8 h-full min-h-[400px] flex flex-col shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary to-secondary"></div>
            
            <div className="flex items-center gap-4 mb-8 pb-6 border-b border-[#152238]">
              <span className="material-symbols-outlined text-5xl text-primary">{pipeline[activeStep].icon}</span>
              <h2 className="text-3xl font-headline-md text-on-surface">{pipeline[activeStep].title}</h2>
            </div>
            
            <p className="text-on-surface-variant text-lg leading-relaxed font-body-lg">
              {pipeline[activeStep].detail}
            </p>

            <div className="mt-auto pt-8 flex items-center justify-between border-t border-[#152238]/50">
              <span className="text-xs font-mono-data text-on-surface-variant uppercase tracking-wider">Step {activeStep + 1} of {pipeline.length}</span>
              <div className="flex gap-2">
                <button 
                  onClick={() => setActiveStep(Math.max(0, activeStep - 1))}
                  disabled={activeStep === 0}
                  className="p-2 rounded bg-surface-container hover:bg-surface-variant disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                >
                  <span className="material-symbols-outlined text-on-surface block">arrow_back</span>
                </button>
                <button 
                  onClick={() => setActiveStep(Math.min(pipeline.length - 1, activeStep + 1))}
                  disabled={activeStep === pipeline.length - 1}
                  className="p-2 rounded bg-primary/20 text-primary hover:bg-primary/30 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                >
                  <span className="material-symbols-outlined block">arrow_forward</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

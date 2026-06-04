import { useState, useEffect } from 'react';
import type { Message } from '../types';
import type { Citation } from '../api';

interface ChatAreaProps {
  messages: Message[];
  onCitationClick: (citationId: string) => void;
  onClear: () => void;
  onSuggestedQuery?: (query: string) => void;
  isPresentationMode?: boolean;
}

const LoadingAnimation = () => {
  const [phase, setPhase] = useState(0);
  const phases = [
    { text: "Searching Qdrant...", icon: "search" },
    { text: "Retrieving evidence...", icon: "database" },
    { text: "Generating answer with Llama 3.1...", icon: "memory" }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setPhase((p) => Math.min(p + 1, phases.length - 1));
    }, 800);
    return () => clearInterval(timer);
  }, []);

  return (
    <p className="text-on-surface font-body-lg text-body-lg leading-relaxed animate-pulse-text flex items-center gap-3">
      <span className="material-symbols-outlined animate-spin text-lg text-primary">{phases[phase].icon}</span>
      {phases[phase].text}
    </p>
  );
};

export default function ChatArea({ messages, onCitationClick, onClear, onSuggestedQuery, isPresentationMode }: ChatAreaProps) {
  const [hoveredCitation, setHoveredCitation] = useState<Citation | null>(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });

  const suggestedQueries = [
    { q: "What is the minimum investment for SIFs?", icon: "payments" },
    { q: "Compare Quant and Tata SIF.", icon: "compare_arrows" },
    { q: "Explain leverage limits.", icon: "balance" },
    { q: "Latest SEBI changes affecting SIFs.", icon: "update" }
  ];

  const handleMouseEnter = (e: React.MouseEvent, citation: Citation) => {
    const rect = (e.target as HTMLElement).getBoundingClientRect();
    setTooltipPos({ x: rect.left, y: rect.top - 8 });
    setHoveredCitation(citation);
  };

  const handleMouseLeave = () => {
    setHoveredCitation(null);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    // Simple visual feedback could be added here
  };

  const printToPDF = () => {
    window.print();
  };

  const renderFormattedText = (text: string, citations?: any[]) => {
    const boldParsed = text.replace(/\*\*(.*?)\*\*/g, '<strong class="text-on-surface">$1</strong>');
    const parts = boldParsed.split(/(\[Source \d+\])/g);
    
    return parts.map((part, index) => {
      const match = part.match(/\[Source (\d+)\]/);
      if (match && citations) {
        const sourceIndex = parseInt(match[1]) - 1;
        const citation = citations[sourceIndex];
        const chunkId = citation?.chunk_id || 'unknown';
        
        return (
          <button 
            key={index} 
            onClick={() => onCitationClick(chunkId)}
            onMouseEnter={(e) => citation && handleMouseEnter(e, citation)}
            onMouseLeave={handleMouseLeave}
            className="inline-flex items-center justify-center min-w-[20px] h-5 rounded text-xs bg-primary/20 text-primary border border-primary cursor-pointer transition-all duration-300 hover:scale-110 hover:bg-primary/30 hover:shadow-[0_0_10px_rgba(173,198,255,0.6)] ml-1 glow-active px-1 relative tour-citation"
            aria-label={`View Source ${sourceIndex + 1}`}
          >
            {part}
          </button>
        );
      }
      return <span key={index} dangerouslySetInnerHTML={{ __html: part }} />;
    });
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-y-auto p-md lg:p-lg pb-32 scroll-smooth" id="printable-area">
      {/* Tooltip Portal / Overlay */}
      {hoveredCitation && (
        <div 
          className="fixed z-50 bg-[#020617] border border-[#152238] rounded-lg shadow-2xl p-3 w-64 transform -translate-y-full -translate-x-1/2 pointer-events-none"
          style={{ top: tooltipPos.y, left: tooltipPos.x + 10 }}
        >
          <div className="flex items-center justify-between mb-2 border-b border-[#152238] pb-1">
            <span className="text-[10px] uppercase font-bold text-primary bg-primary/10 px-1 rounded">{hoveredCitation.document_type}</span>
            <span className="text-[10px] text-secondary font-mono-data">{Math.round(hoveredCitation.confidence * 100)}% Match</span>
          </div>
          <p className="text-xs text-on-surface font-semibold mb-1 truncate">{hoveredCitation.document_title}</p>
          <p className="text-[11px] text-on-surface-variant flex items-center gap-1">
            <span className="material-symbols-outlined text-[12px]">find_in_page</span> Page {hoveredCitation.page_number || 'N/A'}
          </p>
        </div>
      )}

      {/* Header */}
      <div className="flex justify-between items-center mb-lg print:hidden">
        <h1 className="font-headline-lg text-headline-lg text-on-surface">Research Desk</h1>
        {messages.length > 0 && (
          <div className="flex gap-4">
            <button onClick={printToPDF} className="text-sm text-on-surface-variant hover:text-on-surface transition-colors flex items-center gap-1">
              <span className="material-symbols-outlined text-sm">picture_as_pdf</span> Export
            </button>
            <button onClick={onClear} className="text-sm text-on-surface-variant hover:text-error transition-colors flex items-center gap-1">
              <span className="material-symbols-outlined text-sm">delete</span> Clear Chat
            </button>
          </div>
        )}
      </div>

      {messages.length === 0 && (
        <div className="flex-1 flex flex-col items-center justify-center max-w-3xl mx-auto w-full pt-10">
          <div className="bg-surface-container-low border border-[#152238] rounded-2xl p-8 w-full shadow-2xl">
            <div className="flex items-center gap-4 mb-6 border-b border-[#152238] pb-6">
              <div className="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center border border-primary/30">
                <span className="material-symbols-outlined text-2xl text-primary">auto_awesome</span>
              </div>
              <div>
                <h2 className="text-2xl font-headline-md text-on-surface">What would you like to research?</h2>
                <p className="text-on-surface-variant text-sm mt-1">Grounded in 2,000+ verified SEBI documents and AMC factsheets.</p>
              </div>
            </div>
            
            <div className="mb-6">
              <h3 className="text-xs font-mono-data text-on-surface-variant uppercase tracking-wider mb-4">Suggested Questions</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {suggestedQueries.map((q, i) => (
                  <button 
                    key={i}
                    onClick={() => onSuggestedQuery && onSuggestedQuery(q.q)}
                    className="bg-[#020617] border border-[#152238] hover:border-primary/50 hover:bg-[#071122] transition-all p-3 rounded-lg text-left text-sm text-on-surface hover:text-primary group shadow-sm flex items-start gap-3"
                  >
                    <span className="material-symbols-outlined text-primary/70 group-hover:text-primary">{q.icon}</span>
                    <span className="flex-1">{q.q}</span>
                    <span className="material-symbols-outlined text-sm opacity-0 group-hover:opacity-100 transition-opacity">arrow_forward</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-[#020617] border border-secondary/30 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-2">
                <span className="material-symbols-outlined text-secondary text-sm">update</span>
                <span className="text-sm font-semibold text-secondary">Recent Updates</span>
              </div>
              <p className="text-xs text-on-surface-variant">
                The corpus was recently updated with the latest SEBI Master Circular on AIFs (May 2026).
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Message Feed */}
      <div className="space-y-lg max-w-4xl mx-auto w-full">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex flex-col ${msg.type === 'user' ? 'items-end' : 'items-start'}`}>
            {msg.type === 'user' ? (
              <div className="bg-[#122131] border border-[#152238] rounded-xl rounded-tr-sm p-4 max-w-[80%] shadow-md">
                <p className="text-on-surface font-body-lg">{msg.text}</p>
              </div>
            ) : (
              <div className="bg-surface-container-low border border-[#152238] rounded-xl rounded-tl-sm p-lg w-full glow-active relative overflow-hidden glass-panel">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary to-secondary"></div>
                <div className="flex items-center justify-between mb-md border-b border-[#152238] pb-sm">
                  <div className="flex items-center gap-sm text-primary">
                    <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>auto_awesome</span>
                    <h2 className="font-headline-md text-headline-md">Synthesized Analysis</h2>
                  </div>
                  {!msg.loading && (
                    <div className="flex items-center gap-4">
                      <div className="hidden md:flex items-center gap-2 mr-4 border-r border-[#152238] pr-4 print:hidden">
                        <button onClick={() => copyToClipboard(msg.text)} className="text-on-surface-variant hover:text-on-surface transition-colors" title="Copy Answer">
                          <span className="material-symbols-outlined text-[18px]">content_copy</span>
                        </button>
                        <button className="text-on-surface-variant hover:text-on-surface transition-colors" title="Share Session">
                          <span className="material-symbols-outlined text-[18px]">share</span>
                        </button>
                        <button className="text-on-surface-variant hover:text-on-surface transition-colors" title="Save Research">
                          <span className="material-symbols-outlined text-[18px]">bookmark</span>
                        </button>
                      </div>
                      {msg.citations && msg.citations.length > 0 && (
                        <div className="flex items-center gap-xs text-secondary font-mono-data text-mono-data">
                          <span className="material-symbols-outlined text-sm">verified</span>
                          High Confidence
                        </div>
                      )}
                    </div>
                  )}
                </div>
                
                <div className="prose prose-invert prose-sm max-w-none text-on-surface-variant font-body-md space-y-md">
                  {msg.loading ? (
                    <LoadingAnimation />
                  ) : (
                    <>
                      <div className="text-on-surface font-body-lg text-body-lg leading-relaxed whitespace-pre-wrap">
                        {renderFormattedText(msg.text, msg.citations)}
                      </div>
                      
                      {/* Generation Metrics Panel */}
                      {msg.retrieval && !isPresentationMode && (
                        <div className="mt-6 pt-4 border-t border-[#152238] print:hidden">
                          <h4 className="text-xs font-mono-data text-on-surface-variant uppercase tracking-wider mb-3">How this answer was generated</h4>
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div className="bg-[#020617] border border-[#152238] p-3 rounded-lg">
                              <span className="block text-[10px] text-on-surface-variant uppercase mb-1">Retrieved</span>
                              <span className="font-mono-data text-on-surface text-sm flex items-center gap-1"><span className="material-symbols-outlined text-[14px] text-primary">library_books</span> {msg.retrieval.chunks_retrieved} chunks</span>
                            </div>
                            <div className="bg-[#020617] border border-[#152238] p-3 rounded-lg">
                              <span className="block text-[10px] text-on-surface-variant uppercase mb-1">Search</span>
                              <span className="font-mono-data text-on-surface text-sm flex items-center gap-1"><span className="material-symbols-outlined text-[14px] text-secondary">timer</span> {msg.retrieval.search_time_ms}ms</span>
                            </div>
                            <div className="bg-[#020617] border border-[#152238] p-3 rounded-lg">
                              <span className="block text-[10px] text-on-surface-variant uppercase mb-1">Generation</span>
                              <span className="font-mono-data text-on-surface text-sm flex items-center gap-1"><span className="material-symbols-outlined text-[14px] text-primary">memory</span> Groq LPU</span>
                            </div>
                            <div className="bg-[#020617] border border-[#152238] p-3 rounded-lg">
                              <span className="block text-[10px] text-on-surface-variant uppercase mb-1">Confidence</span>
                              <span className="font-mono-data text-secondary text-sm flex items-center gap-1">
                                <span className="material-symbols-outlined text-[14px]">done_all</span> 
                                {msg.citations && msg.citations.length > 0 
                                  ? `${Math.round(msg.citations[0].confidence * 100)}%` 
                                  : 'N/A'}
                              </span>
                            </div>
                          </div>
                        </div>
                      )}
                    </>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

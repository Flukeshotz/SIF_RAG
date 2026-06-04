import { useState, useEffect } from 'react';
import { fetchSource } from '../api';
import type { SourceResponse } from '../api';

interface EvidenceExplorerProps {
  sourceId: string;
  onClose: () => void;
  isDemoMode?: boolean;
}

export default function EvidenceExplorer({ sourceId, onClose, isDemoMode }: EvidenceExplorerProps) {
  const [source, setSource] = useState<SourceResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadSource = async () => {
      setLoading(true);
      setError('');
      
      if (isDemoMode) {
        setTimeout(() => {
          setSource({
            id: sourceId,
            document_title: "Demo SEBI Master Circular",
            document_type: "SEBI Circular",
            organization: "SEBI",
            page_number: 42,
            priority_tier: 1,
            text: "The maximum unhedged short exposure for a Specialized Investment Fund (SIF) shall not exceed 25% of the Net Asset Value (NAV). Furthermore, leverage cannot exceed 2x the fund's equity. This ensures systemic risk is mitigated."
          });
          setLoading(false);
        }, 500);
        return;
      }

      try {
        const data = await fetchSource(sourceId);
        setSource(data);
      } catch (err) {
        setError('Failed to fetch source metadata.');
      } finally {
        setLoading(false);
      }
    };
    loadSource();
  }, [sourceId, isDemoMode]);

  return (
    <div className="w-full md:w-[420px] h-full bg-[#051424] flex flex-col border-l border-[#152238] animate-slide-in-right z-50 shadow-2xl fixed inset-y-0 right-0 md:relative print:hidden">
      {/* App-level Header */}
      <div className="shrink-0 p-md border-b border-[#152238] flex items-center justify-between bg-surface-container-low">
        <div className="flex items-center gap-sm">
          <span className="material-symbols-outlined text-primary">menu_book</span>
          <h3 className="font-headline-md text-headline-md text-on-surface">Evidence Explorer</h3>
        </div>
        <button onClick={onClose} className="text-on-surface-variant hover:text-on-surface transition-colors p-1 bg-[#020617] rounded-full border border-outline-variant hover:bg-error/20 hover:text-error hover:border-error/50 group">
          <span className="material-symbols-outlined text-sm block">close</span>
        </button>
      </div>
      
      {/* Body Area */}
      <div className="flex-1 min-h-0 flex flex-col p-md space-y-md">
        {loading && (
          <div className="flex flex-col items-center justify-center p-8 opacity-50 space-y-4">
            <span className="material-symbols-outlined animate-spin text-4xl text-primary">sync</span>
            <span className="text-sm font-mono-data">Retrieving Immutable Chunk...</span>
          </div>
        )}
        
        {error && (
          <div className="p-4 bg-error-container text-on-error-container rounded-lg text-sm border border-error">
            {error}
          </div>
        )}

        {source && !loading && (
          <div className="flex-1 min-h-0 flex flex-col bg-[#071122] border border-primary/50 rounded-lg overflow-hidden glow-active transition-all duration-300">
            
            {/* Sticky Metadata Header */}
            <div className="shrink-0">
              <div className="bg-primary/10 px-sm py-3 border-b border-primary/20 flex items-center justify-between">
                <div className="flex items-center gap-xs">
                  <span className="inline-flex items-center justify-center px-2 py-1 rounded text-[10px] bg-primary text-on-primary font-bold uppercase tracking-wider shadow-sm">
                    {source.document_type}
                  </span>
                </div>
                
                {/* Confidence Visualizer */}
                <div className="flex items-center gap-2">
                  <div className="flex items-center gap-1">
                    <div className="w-1.5 h-3 bg-secondary rounded-sm"></div>
                    <div className="w-1.5 h-3 bg-secondary rounded-sm"></div>
                    <div className="w-1.5 h-3 bg-secondary rounded-sm"></div>
                    <div className="w-1.5 h-3 bg-secondary/30 rounded-sm"></div>
                  </div>
                  <span className="font-mono-data text-secondary text-[11px] uppercase tracking-wider">98% Match</span>
                </div>
              </div>
              
              <div className="p-sm pb-0 border-b border-[#152238]">
                <h4 className="font-headline-md text-on-surface mb-2">{source.document_title}</h4>
                <div className="text-xs text-on-surface-variant mb-4 font-mono-data flex flex-col gap-1">
                  <span className="flex items-center gap-2"><span className="material-symbols-outlined text-[14px]">corporate_fare</span> {source.organization}</span>
                  <span className="flex items-center gap-2"><span className="material-symbols-outlined text-[14px]">find_in_page</span> Page {source.page_number}</span>
                  <span className="flex items-center gap-2"><span className="material-symbols-outlined text-[14px]">priority_high</span> Tier {source.priority_tier} Source</span>
                </div>
              </div>
            </div>
            
            {/* Independently Scrolling Text */}
            <div className="flex-1 min-h-0 overflow-y-auto p-sm bg-[#020617]">
              <div className="font-body-md text-on-surface text-sm leading-relaxed whitespace-pre-wrap relative group">
                {source.text}
                <button 
                  onClick={() => navigator.clipboard.writeText(source.text)}
                  className="absolute top-0 right-0 opacity-0 group-hover:opacity-100 transition-opacity bg-surface-container-low p-1.5 rounded border border-[#152238] text-on-surface-variant hover:text-primary shadow-lg"
                  title="Copy Chunk"
                >
                  <span className="material-symbols-outlined text-sm block">content_copy</span>
                </button>
              </div>
            </div>
            
            {/* Sticky Footer */}
            <div className="shrink-0 p-sm border-t border-[#152238] bg-[#071122]">
              <div className="flex justify-between gap-sm">
                <button 
                  className="flex-1 py-2 text-xs font-label-md border border-[#152238] rounded bg-surface-container hover:bg-surface-variant text-on-surface transition-colors shadow-sm flex justify-center items-center gap-2"
                >
                  <span className="material-symbols-outlined text-[14px]">link</span> Copy Citation
                </button>
                <button 
                  className="flex-1 py-2 text-xs font-label-md border border-primary/50 rounded bg-primary/10 hover:bg-primary/20 text-primary transition-colors shadow-sm flex justify-center items-center gap-2"
                >
                  <span className="material-symbols-outlined text-[14px]">launch</span> Open Document
                </button>
              </div>
            </div>
            
          </div>
        )}
      </div>
    </div>
  );
}

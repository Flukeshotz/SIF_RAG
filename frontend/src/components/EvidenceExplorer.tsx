import type { Citation } from '../api';

interface EvidenceExplorerProps {
  citation: Citation;
  onClose: () => void;
}

const CONFIDENCE_BARS = 4;

function ConfidenceBars({ score }: { score: number }) {
  const filled = Math.round(score * CONFIDENCE_BARS);
  return (
    <div className="flex items-center gap-1.5">
      <div className="flex items-center gap-0.5">
        {Array.from({ length: CONFIDENCE_BARS }).map((_, i) => (
          <div
            key={i}
            className={`w-1.5 h-3 rounded-sm transition-all ${
              i < filled ? 'bg-secondary' : 'bg-secondary/20'
            }`}
          />
        ))}
      </div>
      <span className="font-mono text-secondary text-[11px] uppercase tracking-wider">
        {Math.round(score * 100)}% Match
      </span>
    </div>
  );
}

export default function EvidenceExplorer({ citation, onClose }: EvidenceExplorerProps) {
  const chunkText = citation.text || 'No source text available for this citation.';

  return (
    <div className="w-full h-full bg-[#051424] flex flex-col border-l border-[#152238] animate-slide-in-right z-50 shadow-2xl">

      {/* Header */}
      <div className="shrink-0 px-4 py-3 border-b border-[#152238] flex items-center justify-between bg-[#071122]">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-[20px]">menu_book</span>
          <h3 className="font-semibold text-sm text-on-surface">Evidence Explorer</h3>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded-full border border-[#152238] bg-[#020617] text-on-surface-variant hover:bg-error/20 hover:text-error hover:border-error/50 transition-colors"
        >
          <span className="material-symbols-outlined text-sm block">close</span>
        </button>
      </div>

      {/* Body */}
      <div className="flex-1 min-h-0 flex flex-col p-4 gap-3">
        <div className="flex-1 min-h-0 flex flex-col bg-[#071122] border border-primary/40 rounded-xl overflow-hidden">

          {/* Metadata strip */}
          <div className="shrink-0 bg-primary/10 px-4 py-2.5 border-b border-primary/20 flex items-center justify-between">
            <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] bg-primary text-on-primary font-bold uppercase tracking-wider">
              {citation.document_type || 'Document'}
            </span>
            <ConfidenceBars score={citation.confidence} />
          </div>

          {/* Doc title + location */}
          <div className="shrink-0 px-4 py-3 border-b border-[#152238]">
            <p className="text-sm font-semibold text-on-surface leading-tight mb-2">
              {citation.document_title}
            </p>
            <div className="flex flex-wrap gap-x-4 gap-y-1 text-[11px] text-on-surface-variant font-mono">
              <span className="flex items-center gap-1">
                <span className="material-symbols-outlined text-[13px]">corporate_fare</span>
                {citation.organization}
              </span>
              {citation.page_number && (
                <span className="flex items-center gap-1">
                  <span className="material-symbols-outlined text-[13px]">find_in_page</span>
                  Page {citation.page_number}
                </span>
              )}
            </div>
          </div>

          {/* The exact chunk text the model read */}
          <div className="flex-1 min-h-0 overflow-y-auto p-4 bg-[#020617] relative group">
            <p className="text-sm text-on-surface leading-relaxed whitespace-pre-wrap">
              {chunkText}
            </p>
            <button
              onClick={() => navigator.clipboard.writeText(chunkText)}
              className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity bg-[#071122] p-1.5 rounded border border-[#152238] text-on-surface-variant hover:text-primary"
              title="Copy chunk text"
            >
              <span className="material-symbols-outlined text-sm block">content_copy</span>
            </button>
          </div>

        </div>
      </div>

    </div>
  );
}

import type { Citation } from '../api';

interface EvidenceExplorerProps {
  citation: Citation;
  onClose: () => void;
}

// Maps document_id → canonical public URL.
// Falls back to a targeted Google search for uncategorized docs.
const DOCUMENT_URL_MAP: Record<string, string> = {
  'sebi-sebi-circular':
    'https://www.sebi.gov.in/legal/circulars/feb-2025/regulatory-framework-for-specialized-investment-funds-sif-_92373.html',
  'sebi-sebi-circular-3':
    'https://www.sebi.gov.in/legal/circulars/mar-2025/guidelines-for-specialized-investment-funds-_92697.html',
  'sebi-sebi-circular-5':
    'https://www.sebi.gov.in/legal/circulars.html',
  'amfi-amfi-circular':
    'https://www.amfiindia.com/research-information/other-data/amfi-circular',
  'amfi-amfi-circular-3':
    'https://www.amfiindia.com/research-information/other-data/amfi-circular',
  'franklin-templeton-kim':
    'https://www.franklintempletonindia.com/investor-education/specialized-investment-funds',
  'quant-mutual-fund-factsheet':
    'https://www.quantmutual.com/factsheets',
  'quant-mutual-fund-isid':
    'https://www.quantmutual.com/specialized-investment-fund',
  'icici-prudential-amc-factsheet':
    'https://www.icicipruamc.com/downloads/factsheet',
  'icici-prudential-amc-kim':
    'https://www.icicipruamc.com/specialized-investment-fund',
  'dsp-mutual-fund-factsheet':
    'https://www.dspim.com/getmedia/factsheet',
  // ISIDs — link to AMFI's SIF ISID listing
  'external--uncategorized-isid':
    'https://www.amfiindia.com/research-information/other-data/sif-isid',
  'external--uncategorized-isid-1':
    'https://www.amfiindia.com/research-information/other-data/sif-isid',
  'external--uncategorized-factsheet':
    'https://www.amfiindia.com/nav-history-download',
};

function getDocumentUrl(docTitle: string, org: string): string {
  if (DOCUMENT_URL_MAP[docTitle]) return DOCUMENT_URL_MAP[docTitle];
  // Smart Google fallback scoped to the organisation
  const q = encodeURIComponent(`${docTitle} ${org} Specialized Investment Fund India`);
  return `https://www.google.com/search?q=${q}`;
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
  const sourceUrl = getDocumentUrl(citation.document_title, citation.organization);

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

          {/* Confidence + type strip */}
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

          {/* Exact chunk text the model read */}
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

          {/* Footer — Open Source button */}
          <div className="shrink-0 p-3 border-t border-[#152238] bg-[#071122]">
            <a
              href={sourceUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2 w-full py-2.5 rounded-lg bg-primary/10 border border-primary/50 text-primary text-xs font-semibold hover:bg-primary/20 transition-colors"
            >
              <span className="material-symbols-outlined text-[16px]">open_in_new</span>
              Open Source Document
            </a>
          </div>

        </div>
      </div>

    </div>
  );
}

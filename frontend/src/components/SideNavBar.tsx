import { useState, useEffect } from 'react';
import { fetchMetrics, fetchSchedulerStatus } from '../api';
import type { MetricsResponse, SchedulerResponse } from '../api';

export default function SideNavBar({ onViewChange, currentView }: { onViewChange?: (view: 'chat' | 'architecture' | 'insights' | 'scheduler') => void, currentView?: string }) {
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);
  const [scheduler, setScheduler] = useState<SchedulerResponse | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [m, s] = await Promise.all([fetchMetrics(), fetchSchedulerStatus()]);
        setMetrics(m);
        setScheduler(s);
      } catch (e) {
        console.error('Failed to load sidebar data');
      }
    };
    loadData();
    const interval = setInterval(loadData, 60000);
    return () => clearInterval(interval);
  }, []);

  const formatTimeAgo = () => {
    // Simple mock formatting
    return "2 hours ago";
  };
  
  const formatTimeFuture = () => {
    return "Tonight 02:00 UTC";
  };

  return (
    <aside className="fixed left-0 top-0 h-full z-40 pt-12 flex flex-col w-[280px] bg-surface-container-low border-r border-outline-variant hidden md:flex">
      <div className="p-md border-b border-outline-variant">
        <div className="flex items-center gap-sm mb-sm">
          <div className="w-8 h-8 rounded-full bg-surface-variant flex items-center justify-center overflow-hidden">
            <span className="material-symbols-outlined text-primary text-sm">smart_toy</span>
          </div>
          <div>
            <h2 className="font-headline-md text-headline-md font-black text-primary" style={{ fontSize: '16px', lineHeight: '20px' }}>SIF Terminal</h2>
            <p className="font-label-md text-label-md text-on-surface-variant">Institutional Grade</p>
          </div>
        </div>
        <button onClick={() => window.location.reload()} className="w-full bg-primary text-on-primary font-body-md py-2 rounded flex items-center justify-center gap-sm hover:bg-primary/90 transition-colors glow-active">
          <span className="material-symbols-outlined text-sm">add</span>
          + New Research
        </button>
      </div>
      
      <nav className="flex-1 overflow-y-auto py-sm px-sm flex flex-col gap-xs mt-sm">
        <a onClick={() => onViewChange && onViewChange('chat')} className={`flex items-center gap-sm px-md py-2 rounded-lg font-semibold transition-opacity cursor-pointer ${currentView === 'chat' ? 'bg-secondary-container text-on-secondary-container opacity-80' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-variant scale-95'}`}>
          <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>search_insights</span>
          <span className="font-label-md text-label-md">Research</span>
        </a>
        
        {/* System Status Indicators */}
        <div className="mt-4 mb-2 px-md">
          <span className="text-xs font-mono-data text-on-surface-variant uppercase tracking-wider">Corpus Health</span>
        </div>
        
        <div className="px-md py-2 text-sm text-on-surface flex justify-between items-center bg-[#020617] rounded border border-[#152238] mx-2 mb-1">
          <span className="flex items-center gap-2"><span className="material-symbols-outlined text-sm text-primary">description</span> Indexed Docs</span>
          <span className="font-mono-data">{metrics ? metrics.indexed_documents : '...'}</span>
        </div>
        <div className="px-md py-2 text-sm text-on-surface flex justify-between items-center bg-[#020617] rounded border border-[#152238] mx-2 mb-1">
          <span className="flex items-center gap-2"><span className="material-symbols-outlined text-sm text-secondary">database</span> Vector Chunks</span>
          <span className="font-mono-data">{metrics ? metrics.chunk_count : '...'}</span>
        </div>
        <div className="px-md py-2 text-sm text-on-surface flex justify-between items-center bg-[#020617] rounded border border-[#152238] mx-2 mb-1">
          <span className="flex items-center gap-2"><span className="material-symbols-outlined text-sm text-primary">health_and_safety</span> Status</span>
          <span className="font-mono-data text-secondary uppercase flex items-center gap-1">
            <span className={`w-2 h-2 rounded-full ${metrics && metrics.vector_health === 'green' ? 'bg-secondary' : 'bg-error'}`}></span>
            {metrics ? "Healthy" : '...'}
          </span>
        </div>

        {/* Scheduler Status Card */}
        <div className="mt-4 px-md">
          <span className="text-xs font-mono-data text-on-surface-variant uppercase tracking-wider">Scheduler</span>
        </div>
        <div 
          onClick={() => onViewChange && onViewChange('scheduler')}
          className="mx-2 mt-2 p-3 bg-surface-container border border-outline-variant rounded-lg cursor-pointer hover:border-primary/50 transition-colors group"
        >
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs text-on-surface-variant">Last Refresh</span>
            <span className="text-xs font-mono-data text-on-surface">{scheduler ? formatTimeAgo() : '...'}</span>
          </div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs text-on-surface-variant">Next Refresh</span>
            <span className="text-xs font-mono-data text-on-surface">{scheduler ? formatTimeFuture() : '...'}</span>
          </div>
          <div className="w-full bg-[#020617] h-1.5 rounded-full overflow-hidden mt-1 relative">
            <div className="bg-primary h-full w-[100%] group-hover:bg-secondary transition-colors"></div>
          </div>
        </div>
      </nav>
      
      <div className="mt-auto border-t border-outline-variant p-sm flex flex-col gap-xs">
        <a onClick={() => onViewChange && onViewChange('insights')} className={`flex items-center gap-sm px-md py-2 rounded-lg transition-all duration-100 cursor-pointer ${currentView === 'insights' ? 'bg-surface-variant text-on-surface' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-variant scale-95'}`}>
          <span className="material-symbols-outlined text-sm">monitoring</span>
          <span className="font-label-md text-label-md">Insights</span>
        </a>
        <a onClick={() => onViewChange && onViewChange('architecture')} className={`flex items-center gap-sm px-md py-2 rounded-lg transition-all duration-100 cursor-pointer ${currentView === 'architecture' ? 'bg-surface-variant text-on-surface' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-variant scale-95'}`}>
          <span className="material-symbols-outlined text-sm">schema</span>
          <span className="font-label-md text-label-md">Architecture Docs</span>
        </a>
      </div>
    </aside>
  );
}

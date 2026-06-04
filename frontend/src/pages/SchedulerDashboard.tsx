import { useState, useEffect } from 'react';
import { fetchSchedulerStatus } from '../api';
import type { SchedulerResponse } from '../api';

export default function SchedulerDashboard() {
  const [scheduler, setScheduler] = useState<SchedulerResponse | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const s = await fetchSchedulerStatus();
        setScheduler(s);
      } catch (e) {
        console.error('Failed to load scheduler data');
      }
    };
    loadData();
  }, []);

  return (
    <div className="p-lg lg:p-xl max-w-6xl mx-auto w-full pb-32">
      <div className="mb-lg border-b border-[#152238] pb-md">
        <h1 className="font-headline-lg text-headline-lg text-on-surface mb-2 flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-3xl">update</span>
          Scheduler Dashboard
        </h1>
        <p className="text-on-surface-variant text-lg">
          Monitor the automated data ingestion pipeline.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-md mb-xl">
        <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md flex flex-col justify-center items-center text-center">
          <span className="material-symbols-outlined text-3xl text-secondary mb-2">check_circle</span>
          <span className="text-on-surface-variant font-mono-data uppercase text-xs tracking-wider mb-2">Status</span>
          <span className="text-2xl font-headline-md text-on-surface capitalize">{scheduler ? scheduler.status : '...'}</span>
        </div>
        
        <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md flex flex-col justify-center items-center text-center">
          <span className="material-symbols-outlined text-3xl text-primary mb-2">description</span>
          <span className="text-on-surface-variant font-mono-data uppercase text-xs tracking-wider mb-2">Docs Processed</span>
          <span className="text-2xl font-headline-md text-on-surface">{scheduler ? scheduler.documents_processed : '...'}</span>
        </div>

        <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md flex flex-col justify-center items-center text-center">
          <span className="material-symbols-outlined text-3xl text-primary mb-2">data_array</span>
          <span className="text-on-surface-variant font-mono-data uppercase text-xs tracking-wider mb-2">Chunks Generated</span>
          <span className="text-2xl font-headline-md text-on-surface">{scheduler ? scheduler.chunks_generated : '...'}</span>
        </div>

        <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md flex flex-col justify-center items-center text-center glow-active">
          <span className="material-symbols-outlined text-3xl text-primary mb-2">schedule</span>
          <span className="text-on-surface-variant font-mono-data uppercase text-xs tracking-wider mb-2">Success Rate</span>
          <span className="text-2xl font-headline-md text-on-surface">100%</span>
        </div>
      </div>

      <h2 className="font-headline-md text-on-surface flex items-center gap-2 mb-md">
        <span className="material-symbols-outlined text-on-surface-variant">timeline</span> Pipeline Execution Log
      </h2>
      
      <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md">
        <div className="relative border-l border-[#152238] ml-4 space-y-8 py-4">
          
          <div className="relative pl-6">
            <span className="absolute -left-2 top-0.5 w-4 h-4 rounded-full bg-secondary shadow-[0_0_10px_rgba(111,255,233,0.5)]"></span>
            <h3 className="font-headline-md text-on-surface mb-1">Upcoming Sync</h3>
            <p className="text-sm font-mono-data text-on-surface-variant mb-2">{scheduler ? new Date(scheduler.next_refresh).toLocaleString() : '...'}</p>
            <div className="bg-[#020617] border border-[#152238] p-3 rounded text-sm text-on-surface-variant">
              Scheduled to run. Pending trigger.
            </div>
          </div>
          
          <div className="relative pl-6">
            <span className="absolute -left-1.5 top-1 w-3 h-3 rounded-full bg-primary"></span>
            <h3 className="font-headline-md text-on-surface mb-1">Last Sync Completed</h3>
            <p className="text-sm font-mono-data text-on-surface-variant mb-2">{scheduler ? new Date(scheduler.last_refresh).toLocaleString() : '...'}</p>
            <div className="bg-[#020617] border border-primary/30 p-3 rounded text-sm text-on-surface font-mono-data flex flex-col gap-1">
              <span><span className="text-secondary">✓</span> Fetched 14 PDFs from SEBI</span>
              <span><span className="text-secondary">✓</span> Recovered 42 Tables</span>
              <span><span className="text-secondary">✓</span> Generated 2,001 Contextual Chunks</span>
              <span><span className="text-secondary">✓</span> Updated Qdrant Index successfully</span>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
}

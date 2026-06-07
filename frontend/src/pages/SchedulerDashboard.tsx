import { useState, useEffect } from 'react';
import { fetchSchedulerStatus, runPipeline } from '../api';
import type { SchedulerResponse } from '../api';

export default function SchedulerDashboard() {
  const [scheduler, setScheduler] = useState<SchedulerResponse | null>(null);
  const [loading, setLoading] = useState(false);
  
  const fetchStatus = async () => {
    try {
      const s = await fetchSchedulerStatus();
      setScheduler(s);
    } catch (e) {
      console.error('Failed to load scheduler data');
    }
  };

  useEffect(() => {
    fetchStatus();
    // Poll every 2 seconds if RUNNING
    const interval = setInterval(() => {
      if (scheduler?.state === 'RUNNING') {
        fetchStatus();
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [scheduler?.state]);

  const handleRunSync = async () => {
    setLoading(true);
    try {
      await runPipeline();
      fetchStatus();
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const formatDur = (secs?: number) => secs ? `${Math.floor(secs / 60)}m ${Math.floor(secs % 60)}s` : '--';
  const stateColor = scheduler?.state === 'SUCCESS' ? 'text-secondary' : scheduler?.state === 'FAILED' ? 'text-red-500' : scheduler?.state === 'RUNNING' ? 'text-yellow-500' : 'text-on-surface';

  return (
    <div className="p-lg lg:p-xl max-w-6xl mx-auto w-full pb-32">
      <div className="mb-lg border-b border-[#152238] pb-md flex justify-between items-center">
        <div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface mb-2 flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-3xl">update</span>
            Pipeline Observability
          </h1>
          <p className="text-on-surface-variant text-lg">
            Monitor the automated data ingestion and embedding pipeline.
          </p>
        </div>
        <button 
          onClick={handleRunSync} 
          disabled={loading || scheduler?.state === 'RUNNING'}
          className="bg-primary hover:bg-primary/90 text-on-primary px-4 py-2 rounded-lg font-headline-md flex items-center gap-2 disabled:opacity-50"
        >
          <span className="material-symbols-outlined">sync</span>
          {scheduler?.state === 'RUNNING' ? 'Sync Running...' : 'Run Sync Now'}
        </button>
      </div>

      {scheduler?.state === 'RUNNING' && (
        <div className="mb-8 bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-4 flex items-center gap-4">
          <span className="material-symbols-outlined text-yellow-500 animate-spin">refresh</span>
          <div>
            <div className="font-headline-md text-yellow-500">Pipeline Running</div>
            <div className="text-sm text-on-surface-variant">Current Stage: {scheduler.current_stage || 'Initializing'} • Elapsed: {scheduler.elapsed_seconds}s</div>
          </div>
        </div>
      )}
      
      {scheduler?.state === 'FAILED' && (
        <div className="mb-8 bg-red-500/10 border border-red-500/30 rounded-xl p-4 flex items-center gap-4">
          <span className="material-symbols-outlined text-red-500">error</span>
          <div>
            <div className="font-headline-md text-red-500">Pipeline Failed</div>
            <div className="text-sm text-on-surface-variant">{scheduler.qdrant_validation?.consistency_error || 'Unknown error occurred'}</div>
          </div>
        </div>
      )}

      {/* Row 1: Pipeline Health */}
      <h2 className="font-headline-md text-on-surface flex items-center gap-2 mb-md mt-4">
        <span className="material-symbols-outlined text-on-surface-variant">health_and_safety</span> Pipeline Health
      </h2>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-md mb-8">
        <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md">
          <div className="text-on-surface-variant font-mono-data uppercase text-xs mb-1">State</div>
          <div className={`text-2xl font-headline-md ${stateColor}`}>{scheduler?.state || 'IDLE'}</div>
        </div>
        <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md">
          <div className="text-on-surface-variant font-mono-data uppercase text-xs mb-1">Last Sync</div>
          <div className="text-lg font-headline-md text-on-surface">{scheduler?.run_id ? new Date(scheduler.run_id).toLocaleString() : '--'}</div>
        </div>
        <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md">
          <div className="text-on-surface-variant font-mono-data uppercase text-xs mb-1">Total Duration</div>
          <div className="text-2xl font-headline-md text-on-surface">{formatDur(scheduler?.total_duration_seconds)}</div>
        </div>
        <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md">
          <div className="text-on-surface-variant font-mono-data uppercase text-xs mb-1">Retrieval Health</div>
          <div className="text-2xl font-headline-md text-on-surface flex items-center gap-2">
            {scheduler?.qdrant_validation?.retrieval_health ? <span className="text-secondary">Healthy</span> : <span className="text-red-500">Degraded</span>}
          </div>
        </div>
      </div>

      {/* Row 2: Corpus & Vector Metrics */}
      <h2 className="font-headline-md text-on-surface flex items-center gap-2 mb-md">
        <span className="material-symbols-outlined text-on-surface-variant">analytics</span> Corpus & Vector Metrics
      </h2>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-md mb-8">
        <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md">
          <div className="text-on-surface-variant font-mono-data uppercase text-xs mb-1">Total Documents</div>
          <div className="text-2xl font-headline-md text-on-surface">{scheduler?.corpus_growth?.total_documents || 0}</div>
          <div className="text-xs text-secondary mt-1">+{scheduler?.corpus_growth?.growth_documents || 0} new docs</div>
        </div>
        <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md">
          <div className="text-on-surface-variant font-mono-data uppercase text-xs mb-1">Total Chunks</div>
          <div className="text-2xl font-headline-md text-on-surface">{scheduler?.corpus_growth?.total_chunks || 0}</div>
          <div className="text-xs text-secondary mt-1">+{scheduler?.corpus_growth?.growth_chunks || 0} new chunks</div>
        </div>
        <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md">
          <div className="text-on-surface-variant font-mono-data uppercase text-xs mb-1">Expected Vectors</div>
          <div className="text-2xl font-headline-md text-on-surface">{scheduler?.qdrant_validation?.expected_vectors || 0}</div>
        </div>
        <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md">
          <div className="text-on-surface-variant font-mono-data uppercase text-xs mb-1">Qdrant Vectors</div>
          <div className="text-2xl font-headline-md text-on-surface">{scheduler?.qdrant_validation?.actual_qdrant_vectors || 0}</div>
        </div>
      </div>

      {/* Failed URLs if any */}
      {scheduler?.failed_urls && scheduler.failed_urls.length > 0 && (
         <div className="mb-8">
           <h2 className="font-headline-md text-red-500 flex items-center gap-2 mb-md">
             <span className="material-symbols-outlined">warning</span> Failed URLs
           </h2>
           <div className="bg-[#020617] border border-red-500/30 p-4 rounded-xl">
             <ul className="list-disc pl-5 text-sm font-mono-data text-red-400">
               {scheduler.failed_urls.map((url, i) => <li key={i}>{url}</li>)}
             </ul>
           </div>
         </div>
      )}

      {/* Row 3: Recent Runs */}
      <h2 className="font-headline-md text-on-surface flex items-center gap-2 mb-md">
        <span className="material-symbols-outlined text-on-surface-variant">history</span> Recent Runs
      </h2>
      <div className="bg-surface-container-low border border-[#152238] rounded-xl overflow-hidden">
        <div className="overflow-x-auto w-full">
          <table className="w-full text-left text-sm text-on-surface-variant font-body-md min-w-[600px]">
            <thead className="bg-[#152238]/50 text-xs uppercase font-mono-data">
              <tr>
                <th className="px-4 py-3">Run ID</th>
                <th className="px-4 py-3">State</th>
                <th className="px-4 py-3">Duration</th>
                <th className="px-4 py-3">Docs Added</th>
                <th className="px-4 py-3">Chunks Added</th>
              </tr>
            </thead>
            <tbody>
              {scheduler?.recent_runs?.map((run, i) => (
                <tr key={i} className="border-b border-[#152238] hover:bg-[#152238]/30">
                  <td className="px-4 py-3 font-mono-data">{new Date(run.run_id).toLocaleString()}</td>
                  <td className={`px-4 py-3 ${run.state === 'SUCCESS' ? 'text-secondary' : run.state === 'FAILED' ? 'text-red-500' : ''}`}>{run.state}</td>
                  <td className="px-4 py-3">{formatDur(run.total_duration_seconds)}</td>
                  <td className="px-4 py-3">+{run.corpus_growth?.growth_documents || 0}</td>
                  <td className="px-4 py-3">+{run.corpus_growth?.growth_chunks || 0}</td>
                </tr>
              ))}
              {(!scheduler?.recent_runs || scheduler.recent_runs.length === 0) && (
                <tr><td colSpan={5} className="px-4 py-6 text-center">No recent runs found.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

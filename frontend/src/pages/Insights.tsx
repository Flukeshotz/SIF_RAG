import { useState, useEffect } from 'react';
import { fetchAnalytics } from '../api';
import type { AnalyticsResponse } from '../api';

export default function Insights() {
  const [analytics, setAnalytics] = useState<AnalyticsResponse | null>(null);

  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        const data = await fetchAnalytics();
        setAnalytics(data);
      } catch (e) {
        console.error('Failed to load analytics');
      }
    };
    loadAnalytics();
  }, []);

  return (
    <div className="p-lg lg:p-xl max-w-6xl mx-auto w-full pb-32">
      <div className="mb-lg border-b border-[#152238] pb-md">
        <h1 className="font-headline-lg text-headline-lg text-on-surface mb-2 flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-3xl">monitoring</span>
          Query Analytics
        </h1>
        <p className="text-on-surface-variant text-lg">
          Monitor system usage, retrieval latency, and RAG performance metrics.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-lg mb-xl">
        <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md flex flex-col justify-center items-center text-center glow-active">
          <span className="material-symbols-outlined text-4xl text-primary mb-2">forum</span>
          <span className="text-on-surface-variant font-mono-data uppercase text-xs tracking-wider mb-2">Total Queries</span>
          <span className="text-4xl font-headline-lg text-on-surface">{analytics ? analytics.total_queries : '...'}</span>
        </div>
        
        <div className="bg-surface-container-low border border-[#152238] rounded-xl p-md flex flex-col justify-center items-center text-center">
          <span className="material-symbols-outlined text-4xl text-secondary mb-2">speed</span>
          <span className="text-on-surface-variant font-mono-data uppercase text-xs tracking-wider mb-2">Avg Retrieval Latency</span>
          <span className="text-4xl font-headline-lg text-on-surface flex items-baseline gap-1">
            {analytics ? analytics.average_latency : '...'}
            <span className="text-xl text-on-surface-variant">ms</span>
          </span>
        </div>
      </div>

      <h2 className="font-headline-md text-on-surface flex items-center gap-2 mb-md">
        <span className="material-symbols-outlined text-on-surface-variant">history</span> Recent Searches
      </h2>
      
      <div className="bg-surface-container-low border border-[#152238] rounded-xl overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-[#020617] border-b border-[#152238]">
              <th className="p-4 text-xs font-mono-data text-on-surface-variant uppercase tracking-wider font-normal">Query</th>
              <th className="p-4 text-xs font-mono-data text-on-surface-variant uppercase tracking-wider font-normal">Timestamp</th>
              <th className="p-4 text-xs font-mono-data text-on-surface-variant uppercase tracking-wider font-normal">Latency</th>
              <th className="p-4 text-xs font-mono-data text-on-surface-variant uppercase tracking-wider font-normal">Sources</th>
            </tr>
          </thead>
          <tbody>
            {analytics?.recent_queries?.length === 0 ? (
              <tr>
                <td colSpan={4} className="p-8 text-center text-on-surface-variant">No queries logged yet. Ask a question to see analytics!</td>
              </tr>
            ) : (
              analytics?.recent_queries?.map((q, i) => (
                <tr key={i} className="border-b border-[#152238]/50 hover:bg-[#071122] transition-colors">
                  <td className="p-4 text-sm text-on-surface font-body-md truncate max-w-[300px]" title={q.query}>{q.query}</td>
                  <td className="p-4 text-xs text-on-surface-variant font-mono-data">{new Date(q.timestamp).toLocaleString()}</td>
                  <td className="p-4 text-sm text-secondary font-mono-data">{q.latency}ms</td>
                  <td className="p-4 text-sm text-on-surface font-mono-data">{q.sources_used}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

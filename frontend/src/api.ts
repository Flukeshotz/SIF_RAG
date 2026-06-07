const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface Citation {
  chunk_id: string;
  document_title: string;
  document_type: string;
  organization: string;
  page_number?: number;
  confidence: number;
  text?: string;
  [key: string]: any;
}

export interface RetrievalMetrics {
  chunks_retrieved: number;
  search_time_ms: number;
  embedding_model: string;
  llm: string;
}

export interface QueryResponse {
  answer: string;
  citations: Citation[];
  retrieval: RetrievalMetrics;
  query_type?: 'rag' | 'discovery' | 'comparison';
  structured_data?: any;
}

export interface MetricsResponse {
  chunk_count: number | string;
  vector_health: string;
  indexed_documents: number | string;
  last_refresh_timestamp: number | string;
}

export interface SchedulerResponse {
  pipeline_version?: string;
  run_id?: string;
  state?: string;
  current_stage?: string;
  elapsed_seconds?: number;
  total_duration_seconds?: number;
  stages?: Record<string, { duration_seconds: number }>;
  corpus_growth?: {
    total_documents: number;
    previous_documents: number;
    growth_documents: number;
    total_chunks: number;
    growth_chunks: number;
  };
  qdrant_validation?: {
    retrieval_health: boolean;
    expected_vectors: number;
    actual_qdrant_vectors: number;
    consistency_error?: string;
  };
  failed_urls?: string[];
  recent_runs?: any[];
  status?: string;
}

export const runPipeline = async (): Promise<{ status: string, message?: string }> => {
  const response = await fetch(`${API_BASE_URL}/admin/run-pipeline`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  if (!response.ok) throw new Error('Failed to start pipeline');
  return response.json();
};

export interface AnalyticsResponse {
  total_queries: number;
  average_latency: number;
  recent_queries: any[];
}

export interface SourceResponse {
  id: string;
  text: string;
  document_title: string;
  document_type: string;
  organization: string;
  page_number: string | number;
  priority_tier: string | number;
}

export const submitQuery = async (query: string): Promise<QueryResponse> => {
  const res = await fetch(`${API_BASE_URL}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) throw new Error('Failed to fetch query response');
  return res.json();
};

export const fetchMetrics = async (): Promise<MetricsResponse> => {
  const res = await fetch(`${API_BASE_URL}/metrics`);
  if (!res.ok) throw new Error('Failed to fetch metrics');
  return res.json();
};

export const fetchSchedulerStatus = async (): Promise<SchedulerResponse> => {
  const res = await fetch(`${API_BASE_URL}/scheduler/status`);
  if (!res.ok) throw new Error('Failed to fetch scheduler status');
  return res.json();
};

export interface NavData {
  fund_id: string;
  ticker: string;
  nav: number;
  change_percent: number;
  last_updated: string;
}

export const fetchNavs = async (): Promise<NavData[]> => {
  const res = await fetch(`${API_BASE_URL}/funds/navs`);
  if (!res.ok) throw new Error('Failed to fetch NAVs');
  return res.json();
};

export interface IntelligenceItem {
  category: string;
  title: string;
  description: string;
  time_ago: string;
  type: 'primary' | 'secondary' | 'error';
}

export const fetchIntelligence = async (): Promise<IntelligenceItem[]> => {
  const res = await fetch(`${API_BASE_URL}/intelligence`);
  if (!res.ok) throw new Error('Failed to fetch intelligence feed');
  return res.json();
};

export const fetchAnalytics = async (): Promise<AnalyticsResponse> => {
  const res = await fetch(`${API_BASE_URL}/analytics`);
  if (!res.ok) throw new Error('Failed to fetch analytics');
  return res.json();
};

export const fetchSource = async (sourceId: string): Promise<SourceResponse> => {
  const res = await fetch(`${API_BASE_URL}/sources/${sourceId}`);
  if (!res.ok) throw new Error('Failed to fetch source details');
  return res.json();
};

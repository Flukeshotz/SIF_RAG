import type { Citation, RetrievalMetrics } from './api';

export interface Message {
  id: string;
  type: 'user' | 'ai';
  text: string;
  citations?: Citation[];
  retrieval?: RetrievalMetrics;
  loading?: boolean;
  query_type?: 'rag' | 'discovery' | 'comparison';
  structured_data?: any;
}

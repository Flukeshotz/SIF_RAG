import type { Citation, RetrievalMetrics } from './api';

export interface Message {
  id: string;
  type: 'user' | 'ai';
  text: string;
  citations?: Citation[];
  retrieval?: RetrievalMetrics;
  loading?: boolean;
}

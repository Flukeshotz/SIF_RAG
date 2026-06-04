# Embedding Model Decision: BAAI/bge-small-en-v1.5

## Decision
We have selected `BAAI/bge-small-en-v1.5` as the primary embedding model for the SIF retrieval pipeline.

## Rejected Alternatives
1. **BGE-M3**: While highly capable and multilingual, its dimensionality (1024) and model size are unnecessarily large given our corpus is entirely in English. The marginal gain in retrieval precision does not justify the 3x increase in memory footprint and latency.
2. **OpenAI `text-embedding-3-small` / `ada-002`**: OpenAI embeddings require shipping sensitive financial and proprietary data over the network, introducing latency, dependency on external APIs, and potential compliance/security risks. Local embedding is preferred.
3. **Cohere Embeddings**: Similar to OpenAI, Cohere requires external API calls. Additionally, Cohere's pricing for high-volume enterprise embedding can become a bottleneck at scale compared to open-source local inference.

## Rationale for `bge-small-en-v1.5`
- **Dimensionality**: 384 dimensions. This keeps the Qdrant memory footprint extremely low and vector search lightning-fast.
- **Performance**: Consistently ranks at the top of the MTEB (Massive Text Embedding Benchmark) leaderboard for models of its size class. 
- **Latency**: Can run inferences on CPU in milliseconds, which is critical for real-time user query processing.
- **Local Execution**: Completely open-source, runs fully offline, and ensures 100% data privacy for sensitive AMFI and SEBI circulars.

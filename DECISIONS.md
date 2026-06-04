# Architectural Decisions

This document records the major architectural decisions made during the design and implementation of SIF Copilot.

## 2026-06-04
**Decision**: MVP Scope
**Chosen**: SIF Copilot (focusing on AIFs/PMSs)
**Reason**: Smaller corpus, faster validation, lower complexity compared to covering all mutual funds.

## 2026-06-04
**Decision**: Vector Database
**Chosen**: Qdrant
**Alternatives**: Chroma, Pinecone, Milvus
**Reason**: Better metadata filtering capabilities (essential for hybrid retrieval) and strong future support for dense+sparse (BM25) hybrid retrieval. Runs easily locally in Docker.

## 2026-06-04
**Decision**: Embedding Model
**Chosen**: BAAI/bge-small-en-v1.5
**Alternatives**: OpenAI text-embedding-3-small, BGE-M3
**Reason**: Cost-effective MVP. The `bge-small-en-v1.5` model is highly efficient (33M params, 384 dimensions) and perfectly sufficient for an English-only corpus of <15K chunks. Avoids the overhead of BGE-M3 until multilingual support is needed.

## 2026-06-04
**Decision**: Retrieval Strategy
**Chosen**: Metadata Filter + Vector Search
**Reason**: Simpler MVP. Deterministic SQL is used for quantitative facts, while vector search is used for qualitative text. BM25 sparse search and cross-encoder reranking are deferred to post-MVP to reduce complexity while still maintaining high accuracy via metadata pre-filtering.

## 2026-06-04
**Decision**: Adopt a Curated MVP Corpus
**Chosen**: The production MVP will use a curated corpus of 36 authoritative documents.
**Reason**: Live ingestion audits demonstrated that a large portion of the 79-source corpus consisted of dynamic marketing pages, duplicate landing pages, and low-information-value content that significantly reduced acquisition reliability. Priority is given to SEBI Circulars, Master Directions, AMFI Guidance, ISIDs, SIDs, KIMs, and Factsheets.
**Expected Benefits**: >90% acquisition reliability, lower parsing complexity, lower OCR workload, smaller vector index, higher retrieval precision, and reduced hallucination risk.

## 2026-06-04
**Decision**: Manual Corpus Acquisition for MVP
**Chosen**: All authoritative documents (SEBI Circulars, ISIDs, KIMs, Factsheets) will be manually acquired and stored locally for the MVP. We are abandoning automated crawling, proxy rotation, and Playwright infrastructures for now.
**Reason**: Repeated acquisition audits failed (60.8% for 79-sources, 58.3% for 36-sources) because the bottleneck is the web acquisition infrastructure (WAFs, bot defenses, connection drops). Since the MVP corpus is fewer than 40 documents, manual acquisition provides near 100% reliability, faster implementation, and much lower engineering complexity.
**Future Considerations**: Automated acquisition can be reintroduced after retrieval quality is validated.

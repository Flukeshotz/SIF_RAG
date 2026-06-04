# SIF Copilot — Architecture Overview

## Hybrid Imperative Architecture

SIF Copilot employs a "Hybrid Imperative" architecture that completely separates quantitative financial data (relational) from qualitative regulatory and descriptive data (vectors). This separation guarantees zero LLM hallucination for hard numerical facts while enabling powerful semantic search for policy and strategy details.

## Core Components

### 1. Ingestion Pipeline
- **Scope:** 2,000+ authoritative documents (SEBI Circulars, ISIDs, KIMs, Factsheets).
- **Processing:** PyMuPDF, Tabula for table recovery, OCR for scanned circulars.
- **Rules:** Zero marketing material, zero third-party blogs.

### 2. Chunking & Embeddings
- **Chunking:** Context-aware slicing. Tables remain indivisible chunks.
- **Model:** `BAAI/bge-small-en-v1.5` (384 dimensions).
- **Metadata Payload:** Every chunk contains `document_type`, `amc`, `fund_name`, and `priority_tier` to enable hard pre-filtering.

### 3. Vector Database
- **Engine:** Qdrant (Local mode for MVP).
- **Distance Metric:** Cosine similarity.
- **Role:** Returns the Top-K most semantically relevant chunks for a given query.

### 4. Generation Engine
- **LLM:** `Llama-3.1-8b-instant` via Groq LPU.
- **Context Window:** Strictly capped at 6,000 tokens per request to ensure dense, highly relevant context.
- **Grounding:** Temperature is set to 0.0. The prompt explicitly blocks the LLM from relying on parametric memory.

### 5. API & Frontend Layers
- **Backend:** FastAPI, orchestrating the RAG pipeline and serving metrics.
- **Frontend:** React + Vite SPA using Tailwind CSS.
- **Design Philosophy:** "Bloomberg-meets-Perplexity." Every claim is cited with a `[Source N]` pill that opens an Evidence Explorer, allowing users to trace claims back to the exact immutable document chunk.

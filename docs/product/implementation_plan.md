# SIF Copilot: Implementation Plan

## Project Overview

- **Project Goal:** Build an AI Wealth Research Assistant (SIF Copilot) for Specialized Investment Funds (SIFs) in India that allows users to understand, compare, and learn about SIFs using only official sources.
- **Supported Functionality:** Factual Q&A, structured fund comparisons, regulatory explanations, and source-backed citations via a Hybrid RAG architecture (PostgreSQL + Qdrant).
- **Non-goals:** The system MUST NOT provide investment advice, recommend funds, predict returns, or generate portfolio recommendations.
- **Architecture Summary:** FastAPI backend orchestrating document ingestion (crawling, parsing, embedding via BGE-M3), deterministic structured storage (PostgreSQL), semantic storage (Qdrant), a Query Router to split tasks, and Groq LLM for fast generation with strict compliance guardrails.

---

## Phase 0 — Project Setup & Governance

**Objective:** Establish the baseline Python project structure, dependency management, and configuration standards for a production-grade FastAPI application.

**Deliverables:**
- Git repository structure initialized
- Python virtual environment setup
- Configuration management (Pydantic settings)
- Standardized logging configured

**Files to Create:**
- `requirements.txt` (FastAPI, Qdrant-client, psycopg2, langchain, etc.)
- `.env.example` (Template for API keys and DB URIs)
- `core/config.py` (Pydantic BaseSettings for env loading)
- `core/logger.py` (Centralized structured logging)
- `main.py` (FastAPI application entry point)
- `tests/conftest.py` (Pytest fixtures)

**Acceptance Criteria:**
- `uvicorn main:app` starts successfully on port 8000.
- Environment variables are validated on startup.

**Tests:**
- Unit test for config loading failure when required `.env` variables are missing.

**Risks:**
- Dependency conflicts between Langchain, Qdrant, and specialized parsing libraries.
- *Mitigation:* Pin exact versions in `requirements.txt`.

---

## Phase 1 — Corpus Management

**Objective:** Create the definitive source-of-truth inventory for all official SIF documents to drive the ingestion pipeline.

**Deliverables:**
- Static CSV inventory and JSON schema definition for sources.

**Files to Create:**
- `data/corpus_inventory.csv` (Target URLs and metadata)
- `data/source_registry.json` (Structured definitions of AMCs and document types)
- `scripts/validate_corpus.py` (Script to verify URLs are well-formed)

**Acceptance Criteria:**
- `corpus_inventory.csv` contains at least 10 valid SIF document entries mapped to their respective Tiers (1 to 5).
- `validate_corpus.py` runs and passes structure checks.

**Tests:**
- Pytest asserting that `source_registry.json` matches a strict Pydantic schema.

**Risks:**
- Malformed URLs in the initial CSV.
- *Mitigation:* Strict regex validation in the test suite.

---

## Phase 2 — Document Ingestion

**Objective:** Download, hash, and store official sources securely to prevent citation decay (URL rot).

**Deliverables:**
- Automated download pipeline with cryptographic hashing for immutable versioning.

**Files to Create:**
- `ingestion/downloader.py` (Requests & Headless Playwright integration)
- `ingestion/hashing.py` (SHA-256 generation logic)
- `ingestion/storage.py` (Local/S3 blob storage abstraction)
- `ingestion/pipeline.py` (Orchestrates download -> hash -> store)

**Acceptance Criteria:**
- Script successfully downloads PDFs from `corpus_inventory.csv`.
- Each file is saved as `<hash>.pdf` in the `storage/raw/` directory.

**Tests:**
- Mock HTTP requests to verify downloading logic.
- Verify identical files produce identical SHA-256 hashes.

**Risks:**
- AMCs blocking automated scraping scripts.
- *Mitigation:* Implement standard User-Agent rotation and retry backoffs.

---

## Phase 3 — Document Parsing

**Objective:** Extract clean text and tabular structures from raw PDFs and HTML files without losing context.

**Deliverables:**
- Parser modules capable of handling Layout-aware PDFs (ISIDs/KIMs) and HTML (Websites/FAQs).

**Files to Create:**
- `parsing/base_parser.py` (Abstract interface)
- `parsing/pdf_parser.py` (LayoutLM or PyMuPDF implementation)
- `parsing/html_parser.py` (BeautifulSoup implementation)
- `parsing/table_extractor.py` (Module specifically for extracting exit loads and allocations)

**Acceptance Criteria:**
- `pdf_parser.py` successfully extracts a continuous text string from a SEBI circular.
- `table_extractor.py` converts a KIM asset allocation table into Markdown format.

**Tests:**
- Pass a known PDF; assert output contains specific string.
- Pass a complex table; assert Markdown output structure is valid.

**Risks:**
- Scanned (image-based) SEBI PDFs failing standard text extraction.
- *Mitigation:* Integrate OCR fallback (Tesseract) for image-only pages.

---

## Phase 4 — Metadata Pipeline

**Objective:** Extract strict, deterministic structured metadata from parsed documents for SQL storage.

**Deliverables:**
- Pydantic models for the metadata schema and extraction logic using Regex/NER.

**Files to Create:**
- `metadata/schema.py` (Pydantic models: `FundMetadata`, `DocumentMetadata`)
- `metadata/extractor.py` (Logic to find Minimum Investment, Exit Loads, Dates)
- `metadata/validator.py` (Ensures SEBI rules, e.g., Min Inv == ₹10 Lakh)

**Acceptance Criteria:**
- Extracting metadata from the "Tata Titanium ISID" returns exactly `{fund_name: "Tata Titanium", minimum_investment: 1000000, category: "Hybrid Long-Short"}`.

**Tests:**
- Unit tests against mocked parsed text to verify Regex hits for percentages and currency.

**Risks:**
- Highly variable language across AMCs breaking Regex rules.
- *Mitigation:* Use lightweight LLM calls (Groq) for metadata extraction if Regex fails.

---

## Phase 5 — Chunking Pipeline

**Objective:** Slice parsed documents into optimal semantic windows for vector search, preserving mathematical tables.

**Deliverables:**
- Chunking strategies mapped to document types (Hierarchical for SEBI, Semantic+Tabular for ISIDs).

**Files to Create:**
- `chunking/strategy.py` (Chunk size and overlap constants)
- `chunking/hierarchical.py` (Maintains SEBI parent section numbering)
- `chunking/semantic.py` (Standard Langchain RecursiveCharacterTextSplitter)
- `chunking/orchestrator.py` (Routes doc to correct chunker)

**Acceptance Criteria:**
- SEBI circular chunks include their parent Section Header in the chunk metadata.
- Tables are kept as single, undivided chunks.

**Tests:**
- Test chunk lengths do not exceed 512 tokens.
- Verify tabular chunks contain complete Markdown table syntax.

**Risks:**
- Chopping sentences in half.
- *Mitigation:* Ensure `RecursiveCharacterTextSplitter` respects sentence boundaries (`. \n`).

---

## Phase 6 — Embedding Pipeline

**Objective:** Convert semantic chunks into high-dimensional vectors using BGE-M3.

**Deliverables:**
- Integration with the embedding model provider (HuggingFace locally or API).

**Files to Create:**
- `embeddings/model.py` (Initializes BGE-M3 via LangChain/SentenceTransformers)
- `embeddings/generator.py` (Batch processing logic for chunks)

**Acceptance Criteria:**
- Passing a list of 10 strings returns a list of 10 vectors of correct dimensionality (1024 for BGE-M3).
- Execution time per batch is within acceptable latency thresholds.

**Tests:**
- Unit test to verify vector dimension size matches expected configuration.

**Risks:**
- High memory usage if running BGE-M3 locally.
- *Mitigation:* Batch chunk generation or offload to a managed inference endpoint if required.

---

## Phase 7 — Vector Database

**Objective:** Establish Qdrant collections to store and search the dense semantic embeddings.

**Deliverables:**
- Configured Qdrant instance with collections optimized for Hybrid Search (Dense + Sparse/BM25).

**Files to Create:**
- `db/qdrant_client.py` (Connection setup and collection initialization)
- `db/vector_store.py` (Upsert and search wrapper functions)

**Acceptance Criteria:**
- Collection `sif_documents` is created successfully.
- Can upsert a batch of 100 embedded chunks with metadata payloads.
- Can successfully perform a cosine similarity search returning top-K results.

**Tests:**
- Mock Qdrant instance to test upsert success.

**Risks:**
- Metadata payload limits exceeded in Qdrant.
- *Mitigation:* Store only essential filtering metadata (tier, category, amc) in Qdrant; keep verbose data in PostgreSQL.

---

## Phase 8 — Structured Database

**Objective:** Build the PostgreSQL relational schema to store deterministic metrics, funds, and source lineages.

**Deliverables:**
- SQL database schema and SQLAlchemy ORM models.

**Files to Create:**
- `db/postgres_client.py` (SQLAlchemy engine and session maker)
- `db/models.py` (Tables: `funds`, `documents`, `metadata`, `citations`)
- `alembic/` (Migration scripts)

**Acceptance Criteria:**
- Alembic successfully creates tables in a local PostgreSQL instance.
- Able to insert a new SIF fund record and query it by `minimum_investment`.

**Tests:**
- Test DB fixtures for CRUD operations.

**Risks:**
- Schema changes breaking the app.
- *Mitigation:* Strictly enforce Alembic migrations for all schema updates.

---

## Phase 9 — Retrieval Layer

**Objective:** Combine Vector Search (Qdrant) and Structured Lookup (PostgreSQL) into a cohesive retrieval engine.

**Deliverables:**
- Hybrid retriever module and Reranking integration.

**Files to Create:**
- `retrieval/hybrid_search.py` (Combines dense and sparse search)
- `retrieval/sql_search.py` (NL2SQL or predefined deterministic queries)
- `retrieval/reranker.py` (Cross-encoder reranking logic)
- `retrieval/engine.py` (Master retrieval orchestrator)

**Acceptance Criteria:**
- A query for "Compare Tata and Quant SIF exit loads" correctly executes a SQL lookup for exit loads and a vector search for qualitative philosophy.

**Tests:**
- Assert vector search returns Tier 1 regulatory documents before Tier 5 websites for compliance queries.

**Risks:**
- High latency during retrieval.
- *Mitigation:* Run SQL and Qdrant queries concurrently (async).

---

## Phase 10 — Query Classification

**Objective:** Dynamically route incoming user queries to the correct retrieval pipeline based on intent.

**Deliverables:**
- Intent classifier handling: Product, Regulatory, Comparison, Risk, Glossary, Advisory.

**Files to Create:**
- `routing/classifier.py` (Uses fast LLM call or zero-shot classifier to tag intent)
- `routing/router.py` (Logic to map intent to specific `retrieval/engine.py` methods)

**Acceptance Criteria:**
- "Which SIF should I buy?" is classified as `Advisory`.
- "What is the SEBI limit on shorting?" is classified as `Regulatory`.

**Tests:**
- Provide a dataset of 50 sample queries; classifier must achieve >95% accuracy.

**Risks:**
- Misclassifying an advisory query as a product query.
- *Mitigation:* Add strict Regex pre-filters for words like "buy, recommend, best" before LLM classification.

---

## Phase 11 — Generation Layer

**Objective:** Synthesize the retrieved context into a natural language response using Groq LLM, enforcing guardrails.

**Deliverables:**
- Prompt templates, context assembly logic, and citation mapping.

**Files to Create:**
- `generation/prompts.py` (Persona and strict guardrail system prompts)
- `generation/assembler.py` (Formats retrieved chunks into string context)
- `generation/llm.py` (Groq API integration for fast generation)
- `generation/citations.py` (Maps output claims to `source_url`)

**Acceptance Criteria:**
- LLM generates a response citing specific documents using the `[Source X]` format.
- If context is empty, LLM outputs the required "I could not find this information" refusal.

**Tests:**
- Mock Groq API response.
- Test that prompt assembly does not exceed maximum token limits.

**Risks:**
- Hallucinations despite context.
- *Mitigation:* Set LLM temperature to 0.0. Strongly penalize out-of-context facts in the system prompt.

---

## Phase 12 — API Layer

**Objective:** Expose backend RAG functionality via REST endpoints for the frontend.

**Deliverables:**
- FastAPI routes and Pydantic request/response schemas.

**Files to Create:**
- `api/schemas.py` (`QueryRequest`, `QueryResponse`, `CitationModel`)
- `api/routes/chat.py` (POST `/api/chat`)
- `api/routes/compare.py` (POST `/api/compare`)
- `api/routes/health.py` (GET `/health`)

**Acceptance Criteria:**
- POST to `/api/chat` with `{"query": "What is a SIF?"}` returns a JSON response containing `answer` and `citations`.
- GET `/health` returns 200 OK.

**Tests:**
- FastAPI `TestClient` tests for all endpoints validating HTTP status codes and JSON schemas.

**Risks:**
- Long processing times causing HTTP timeouts.
- *Mitigation:* Implement streaming responses (Server-Sent Events) for the chat endpoint.

---

## Phase 13 — Frontend

**Objective:** Build a lightweight, interactive user interface (Next.js/React or Streamlit MVP).

**Deliverables:**
- A functional web UI with Chat, Compare, and Discover tabs.

**Files to Create (Assuming Streamlit MVP for speed):**
- `frontend/app.py` (Main Streamlit app)
- `frontend/components/chat.py` (Chat interface)
- `frontend/components/compare.py` (Side-by-side fund comparison table)

**Acceptance Criteria:**
- User can submit a query in the UI and see the streamed LLM response and clickable source links.
- The UI explicitly displays the required disclaimer: "Information provided is for educational purposes only..."

**Tests:**
- Streamlit automated testing or manual UI verification.

**Risks:**
- Poor user experience if latency is high.
- *Mitigation:* Show skeleton loaders and "Analyzing documents..." states during retrieval.

---

## Phase 14 — Evaluation Framework

**Objective:** Quantitatively measure system quality to ensure compliance and accuracy.

**Deliverables:**
- Offline evaluation script using RAGAS/DeepEval metrics.

**Files to Create:**
- `evaluation/dataset.json` (100 Golden Q&A pairs)
- `evaluation/metrics.py` (Faithfulness, Context Precision logic)
- `evaluation/runner.py` (Executes dataset against pipeline and outputs CSV report)

**Acceptance Criteria:**
- Evaluation suite runs and generates a report.
- Pipeline achieves >90% Faithfulness score on the Golden dataset.

**Tests:**
- CI/CD integration to fail PRs if Faithfulness drops below threshold.

**Risks:**
- Evaluation LLM (judge) is biased or inaccurate.
- *Mitigation:* Use a powerful model (GPT-4o or Claude 3.5 Sonnet) specifically for the offline evaluation judge.

---

## Phase 15 — Monitoring & Observability

**Objective:** Track production system health, latency, and corpus freshness.

**Deliverables:**
- Telemetry integration and user feedback collection.

**Files to Create:**
- `monitoring/telemetry.py` (LangSmith tracing setup)
- `api/routes/feedback.py` (POST `/api/feedback` for 👍/👎)

**Acceptance Criteria:**
- Every API request generates a distinct trace in LangSmith containing the retrieved chunks and LLM generation time.
- Thumbs up/down feedback is saved to PostgreSQL.

**Tests:**
- Verify telemetry spans are correctly capturing metadata tags (e.g., query_type).

**Risks:**
- Tracing adds latency to production requests.
- *Mitigation:* Send traces asynchronously in the background.

---

## Phase 16 — Deployment

**Objective:** Package the application for production deployment via Docker.

**Deliverables:**
- Dockerfiles, `docker-compose.yml`, and infrastructure scripts.

**Files to Create:**
- `Dockerfile` (FastAPI backend)
- `frontend/Dockerfile` (Frontend UI)
- `docker-compose.yml` (App, Qdrant, PostgreSQL)

**Acceptance Criteria:**
- `docker-compose up` successfully spins up all services locally.
- Services can communicate over the Docker network.

**Tests:**
- End-to-end integration test running against the spun-up Docker containers.

**Risks:**
- Secret leakage in images.
- *Mitigation:* Use environment variable injection at runtime, never hardcode keys in Dockerfile.

---

## Phase 17 — Daily Refresh Pipeline

**Objective:** Automate the ingestion pipeline to keep the corpus updated with new Factsheets and Circulars.

**Deliverables:**
- Scheduled cron job or Celery worker for daily document checks.

**Files to Create:**
- `jobs/scheduler.py` (APScheduler or Celery config)
- `jobs/refresh_corpus.py` (Logic to check for new files, hash them, and trigger re-indexing)

**Acceptance Criteria:**
- Job runs daily at 00:00 UTC.
- New documents are automatically parsed, embedded, and available for search without system downtime.

**Tests:**
- Unit test simulating a new file drop and verifying database upsert logic.

**Risks:**
- Re-indexing corrupts existing data.
- *Mitigation:* Perform upserts carefully; use transactional rollbacks in PostgreSQL.

---

## Phase 18 — Production Hardening

**Objective:** Secure the API and optimize for public usage.

**Deliverables:**
- Rate limiting, CORS, and robust error handling.

**Files to Create:**
- `core/security.py` (CORS middleware, API key validation)
- `core/rate_limit.py` (Redis-based rate limiting)
- `core/exceptions.py` (Standardized HTTP error responses)

**Acceptance Criteria:**
- Exceeding 10 requests/minute returns a `429 Too Many Requests` error.
- Unhandled backend exceptions return a generic `500 Internal Server Error` without leaking stack traces.

**Tests:**
- Hammer the API with 20 concurrent requests to verify rate limit triggers.

**Risks:**
- Denial of Service (DoS) attacks on expensive LLM endpoints.
- *Mitigation:* Strict IP-based and token-based rate limits.

---

## Phase 19 — Launch Readiness Checklist

**Checklist (Must be 100% complete before go-live):**
- [ ] All 10-15 AMCs' SIF documents ingested and verified in PostgreSQL/Qdrant.
- [ ] Golden dataset evaluation confirms >90% faithfulness and zero advice generation.
- [ ] Disclaimer prominently displayed on all UI screens.
- [ ] Environment variables (API Keys, DB Passwords) secured in secrets manager.
- [ ] Load testing confirms P99 latency < 5 seconds under target concurrent load.
- [ ] Immutable S3 URLs are active and serving PDFs correctly.

---

## Phase 20 — Future Enhancements

- **Phase 20.1: Mutual Funds:** Scale ingestion crawler to handle 10,000+ daily Factsheet/NAV updates. Introduce distributed queuing (Kafka/RabbitMQ).
- **Phase 20.2: PMS:** Add specialized parsers for complex Private Placement Memorandums (PPMs) which lack standardized structures.
- **Phase 20.3: AIF:** Expand PostgreSQL schema to handle illiquid asset metrics and complex drawdown structures.
- **Phase 20.4: Multilingual Support:** Switch LLM prompts and frontend to support Hindi and regional languages using the BGE-M3 multilingual embeddings.
- **Phase 20.5: Agentic Workflows:** Implement ReAct agents capable of chaining multiple searches (e.g., "Find the SIF, check the fund manager's historical MF performance, and summarize").

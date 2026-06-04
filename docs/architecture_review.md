# SIF Copilot — Formal Architecture Review

**Reviewer Role:** Principal AI Architect  
**Review Date:** June 4, 2026  
**Documents Reviewed:** `problem_statement.md`, `research_findings.md`, `architecture.md`, `implementation_plan.md`, `corpus_inventory.csv`  
**Verdict:** **B — Minor Revisions Required** (see Section 10)

---

## 1. Architecture Review

### 1.1 — Overengineered for Corpus Size

**Severity:** HIGH  
**Impact:** Wasted engineering effort, delayed MVP by 4-6 weeks.

The architecture designs for a corpus that does not exist yet. The deep research document explicitly states: **max 7 strategies × ~13 AMCs = ~91 theoretical SIF products.** With ISIDs averaging 50-120 pages and KIMs at 5-15 pages, the *total vector corpus* is roughly **5,000–15,000 chunks.** That is trivially small.

For a corpus this size:
- **Qdrant is fine, but Hybrid Search (Dense + Sparse BM25) is premature.** Dense search alone with metadata filtering will achieve >95% precision on 15K chunks. BM25 adds complexity without meaningful recall improvement at this scale.
- **NL2SQL is overengineered.** With ~91 funds, a simple parameterized SQL query builder (fund name → lookup) is sufficient. NL2SQL introduces hallucination risk (the SQL itself can be wrong) and adds an entire failure mode to the pipeline.
- **Cross-encoder reranking is unnecessary for MVP.** Reranking matters when you retrieve 100+ candidates. At this corpus size, top-10 dense retrieval with metadata pre-filtering will be precise enough.

**Recommendation:**
- Cut BM25 sparse search from MVP. Add in Phase 2 (MF expansion).
- Replace NL2SQL with deterministic parameterized queries.
- Defer reranking to post-MVP.

---

### 1.2 — BGE-M3 is Overkill for MVP

**Severity:** MEDIUM  
**Impact:** High memory usage (~2-3 GB VRAM), slow local inference, unnecessary complexity.

BGE-M3 is a 568M parameter model producing 1024-dim vectors. The multilingual justification is speculative — the entire SIF corpus is in English. For an MVP with <15K chunks:

- `bge-small-en-v1.5` (33M params, 384-dim) will deliver near-identical retrieval quality at 1/17th the memory.
- Alternatively, `text-embedding-3-small` from OpenAI at ~$0.02/M tokens would cost literally **< $0.10** to embed the entire SIF corpus once.

**Recommendation:**
- Use `bge-small-en-v1.5` for MVP. Swap to BGE-M3 only when adding Hindi/Gujarati content.

---

### 1.3 — LayoutLM is Overkill for Most SIF PDFs

**Severity:** MEDIUM  
**Impact:** Adds a heavy ML dependency (transformers, torch) for a problem solvable with simpler tools.

The deep research document identifies that many ISIDs and KIMs are *natively digital PDFs*, not scanned images. For natively digital PDFs:
- **PyMuPDF (fitz)** extracts text with positional coordinates perfectly.
- **pdfplumber** handles table extraction from native PDFs excellently.
- LayoutLM/DocTR is only needed for *scanned image PDFs* (some older SEBI circulars).

**Recommendation:**
- Use PyMuPDF + pdfplumber as the primary parser.
- Add Tesseract OCR as a fallback for image-only pages.
- Defer LayoutLM entirely unless you encounter actual parsing failures.

---

### 1.4 — Missing: Conversation History / Multi-turn

**Severity:** MEDIUM  
**Impact:** Users will ask follow-up questions ("What about its exit load?" after asking about a specific fund). Without session context, the system will fail on these queries.

Neither the architecture nor the implementation plan addresses multi-turn conversation management.

**Recommendation:**
- Add a lightweight session store (in-memory or Redis) that holds the last 3-5 turns.
- Inject conversation history into the prompt for context continuity.

---

### 1.5 — S3 Immutable Storage is Premature

**Severity:** LOW  
**Impact:** Adds AWS cost and configuration overhead for MVP.

For MVP, local filesystem storage with SHA-256 hashing is sufficient. The immutable versioning concern is valid but becomes critical only at production scale with daily factsheet refreshes.

**Recommendation:**
- Use local `storage/raw/<hash>.pdf` for MVP.
- Migrate to S3 with object lock when daily refresh pipeline (Phase 17) is activated.

---

## 2. Retrieval Review

### 2.1 — Chunking Strategy Contradiction

**Severity:** HIGH  
**Impact:** Implementation ambiguity. An AI coding assistant will not know which sizes to use.

The `problem_statement.md` says Parent Chunks: 1500-2500 tokens, Child Chunks: 300-500 tokens.  
The `architecture.md` says SEBI Circulars: Parent 1500, Child 300; ISIDs: 512/128.  
The `implementation_plan.md` Phase 5 says "Test chunk lengths do not exceed 512 tokens."

These are three different and contradictory specifications. Which one is canonical?

**Recommendation:**
- Settle on ONE chunking spec. For MVP, use a flat 512-token chunk with 128-token overlap for everything except tables (kept intact). Parent-child hierarchical chunking is a Phase 2 optimization.

### 2.2 — No Retrieval Fallback Strategy

**Severity:** MEDIUM  
**Impact:** When retrieval returns zero results or low-confidence results, the system behavior is undefined beyond "say I don't know."

What happens when:
- The user asks about a fund not yet in the corpus?
- The user asks a valid SIF question but the relevant ISID hasn't been ingested?
- Vector similarity scores are all below a meaningful threshold?

**Recommendation:**
- Define a minimum similarity threshold (e.g., cosine > 0.65).
- If no chunks pass threshold, return: "This information may not be in our current database. Our corpus covers [X] AMCs as of [date]."
- Log zero-result queries for corpus gap analysis.

### 2.3 — Tier-Based Retrieval Priority is Not Implemented

**Severity:** MEDIUM  
**Impact:** The architecture describes a 5-tier priority system but neither the implementation plan nor the retrieval layer explains *how* tiers affect search ranking.

Simply storing `tier` as metadata does not make Tier 1 results rank higher than Tier 5. You need explicit boosting logic.

**Recommendation:**
- Apply a score multiplier during retrieval: `final_score = cosine_score * tier_weight` where Tier 1 = 1.0, Tier 5 = 0.6.
- Or use Qdrant payload filtering to restrict regulatory queries to Tiers 1-2 only.

---

## 3. Corpus Review

### 3.1 — Corpus Inventory is Dangerously Incomplete

**Severity:** CRITICAL  
**Impact:** The system cannot answer questions about most SIF products.

The `corpus_inventory.csv` contains **12 entries** covering only 7 out of ~13 active AMCs. Missing entirely:
- **Franklin Templeton Sapphire SIF** (mentioned in deep_research.txt but absent from CSV)
- **Aditya Birla Apex SIF** (absent)
- **ITI Diviniti SIF** (absent)
- **Kotak Infinity SIF** (absent)
- **Bandhan** (absent — yet referenced in the example prompt on the Home Screen!)
- **The Wealth Company WSIF** (absent)

The deep research document identifies **75 source URLs.** The corpus inventory captured 12. That is a **16% coverage rate.**

**Recommendation:**
- Before writing a single line of code, complete the corpus inventory to cover ALL active AMCs and ALL document types per AMC (ISID + KIM + Factsheet minimum).
- Remove "Compare SBI Magnum SIF and Bandhan Arudha SIF" from the example prompts until Bandhan is actually in the corpus.

### 3.2 — No SEBI Circular PDF URL

**Severity:** HIGH  
**Impact:** Tier 1 (the most important tier) has no actual downloadable PDF URL in the inventory.

The CSV lists `sebi.gov.in/legal/circulars/...html` but the actual circular is a PDF linked *from* that page. The ingestion pipeline will download an HTML page, not the regulatory document.

**Recommendation:**
- Add the actual PDF URL column to the CSV.
- Verify every URL resolves to the correct document *before* Phase 2 begins.

### 3.3 — SIF-Only MVP is Viable — But Barely

Given the restricted corpus (~91 max products), an SIF-only MVP is viable *if* the corpus inventory is completed. Do NOT expand to Mutual Funds until SIF retrieval quality is proven at >90%. The deep research document's recommendation to immediately build a "Wealth Copilot" should be rejected for MVP — it would multiply scope by 100x.

---

## 4. Data Model Review

### 4.1 — PostgreSQL Schema is Undefined

**Severity:** HIGH  
**Impact:** The implementation plan says "Tables: `funds`, `documents`, `metadata`, `citations`" but provides zero column definitions.

For a plan that claims "No implementation ambiguity should remain," this is a significant gap. An AI coding assistant will invent its own schema, which may not align with the metadata architecture.

**Recommendation:**
- Define the exact DDL for each table before Phase 8 begins:
  - `funds`: id, fund_name, amc, category, strategy_type, risk_band, minimum_investment, benchmark, launch_date
  - `documents`: id, fund_id, document_type, source_url, internal_hash, ingested_at, effective_date
  - `chunks`: id, document_id, content, token_count, chunk_type, parent_chunk_id
  - `exit_loads`: id, fund_id, duration_days, percentage

### 4.2 — Versioning Strategy is Incomplete

**Severity:** MEDIUM  
**Impact:** When an ISID is updated (addendum), how does the system handle the old version vs the new version?

Questions not answered:
- Does the old version get soft-deleted from Qdrant?
- Do chunks from superseded documents get a `deprecated` flag?
- Can users query historical versions?

**Recommendation:**
- Add `version` and `is_active` columns to the documents table.
- When a new version is ingested, set `is_active = false` on the old version.
- Filter Qdrant searches to only return chunks from active documents.

---

## 5. Compliance Review

### 5.1 — Guardrails are Regex-Heavy and Brittle

**Severity:** HIGH  
**Impact:** Regex for "buy, sell, best, recommend" will miss: "Which one gives better returns?", "Where should I put my money?", "Is Fund A worth it?"

Regex-only advisory detection will have a high false-negative rate. Sophisticated users will easily bypass it.

**Recommendation:**
- Use a two-layer approach:
  1. Fast Regex pre-filter for obvious keywords (cheap, instant).
  2. LLM-based intent classification as the authoritative check (already planned in Phase 10, but must be explicitly wired into the compliance layer too).

### 5.2 — Output Guardrails are Underspecified

**Severity:** MEDIUM  
**Impact:** The architecture says "Output Guardrails" exist but doesn't define what they check.

What if the LLM, despite the system prompt, generates: "Based on its strong performance, you should consider investing in Tata Titanium SIF"? The architecture has no post-generation scanner.

**Recommendation:**
- Add a lightweight output scanner that checks the LLM response for advisory language *after* generation.
- If detected, replace the response with the standard compliance refusal.

### 5.3 — Tax Advice Prohibition Needs Nuance

**Severity:** LOW  
**Impact:** The system says "never provide tax advice" but the deep research document extensively discusses taxation (12.5% LTCG, slab rates for debt). Explaining documented tax structures is factual, not advisory.

**Recommendation:**
- Clarify: The system CAN explain documented tax rules (factual). The system CANNOT advise on tax optimization strategies (advisory).

---

## 6. Cost Review

### 6.1 — $500/mo MVP Estimate is Reasonable but Can Be Lower

**Severity:** LOW  

With the recommended simplifications:
- **Embedding:** `bge-small-en-v1.5` runs on CPU. No GPU needed. Saves ~$200/mo in compute.
- **Vector DB:** Qdrant runs locally in Docker. Free.
- **PostgreSQL:** Local Docker. Free.
- **LLM:** Groq free tier provides 30 RPM on Llama models. Sufficient for development and small pilot.
- **Storage:** Local filesystem. $0.

**Realistic MVP cost: $50-100/mo** (a single small VPS or free tier cloud instance + Groq free tier).

---

## 7. Solo Developer Review

### 7.1 — 20 Phases is Too Many

**Severity:** HIGH  
**Impact:** A solo developer will burn out before Phase 10. Analysis paralysis.

**Recommended MVP-Critical Path (8 phases, not 20):**

| Priority | What | Original Phases |
|---|---|---|
| 1 | Project setup + complete corpus inventory | Phase 0 + 1 |
| 2 | Download, parse, chunk, embed all documents | Phase 2 + 3 + 5 + 6 (merge) |
| 3 | PostgreSQL schema + Qdrant setup + data load | Phase 7 + 8 (merge) |
| 4 | Metadata extraction (can be manual for 91 funds) | Phase 4 (simplified) |
| 5 | Basic retrieval (dense search + SQL lookup) | Phase 9 (simplified, no reranker) |
| 6 | Generation with guardrails | Phase 10 + 11 (merge) |
| 7 | API endpoints | Phase 12 |
| 8 | Streamlit frontend | Phase 13 |

**Defer to post-MVP:**
- Phase 14 (Evaluation) — do manual spot-checks first
- Phase 15 (Monitoring) — use print logs initially
- Phase 16 (Docker) — run locally during development
- Phase 17 (Daily Refresh) — manual re-ingestion is fine for <100 docs
- Phase 18 (Hardening) — not needed until users exist

### 7.2 — Metadata Extraction Can Be Semi-Manual for MVP

**Severity:** MEDIUM  

Building NER + Regex pipelines for metadata extraction across heterogeneous AMC documents is a multi-week effort. For ~91 funds, a solo developer can manually populate a `funds.csv` with structured metadata in 2-3 hours. Automate later.

---

## 8. Missing Documents Review

| Missing Document | Why It's Needed |
|---|---|
| `prompt_strategy.md` | The exact system prompt, few-shot examples, and refusal templates are the single most important artifact for LLM quality. Currently undefined. |
| `data_dictionary.md` | No canonical field definitions exist. The metadata section in architecture.md is informal. Need strict types, constraints, and allowed values. |
| `test_cases.md` | 50-100 golden Q&A pairs must be defined BEFORE building the pipeline so retrieval quality can be measured objectively. |
| `retrieval_strategy.md` | The current retrieval description is scattered across architecture.md sections 8, 11, and 12. Consolidate into one document defining the exact search flow. |
| `chunking_spec.md` | Resolve the contradictions identified in Section 2.1 into one canonical chunking specification. |

---

## 9. Launch Readiness Assessment

| Category | Score (1-10) | Reasoning |
|---|---|---|
| **Architecture** | 7/10 | Fundamentally sound hybrid approach. Overengineered for MVP scale. |
| **Retrieval** | 5/10 | Contradictory chunking specs. No similarity threshold. No tier boosting implementation. |
| **Data** | 3/10 | Corpus inventory covers only 16% of known sources. Critical gap. |
| **Compliance** | 6/10 | Good intent but regex-only detection is brittle. No output scanning. |
| **Maintainability** | 7/10 | Clean separation of concerns. Good file structure. |
| **Scalability** | 8/10 | Architecture supports MF/PMS expansion well. Tiered source model is extensible. |
| **Observability** | 4/10 | Mentioned but not designed. No alerting rules, no dashboards defined. |

---

## 10. Final Verdict

### **B — Minor Revisions Required**

The architecture is fundamentally sound. The hybrid PostgreSQL + Qdrant approach is correct. The tiered source prioritization is well-reasoned. The compliance framework has the right intent. However, the system is overengineered for its current corpus size and underspecified in critical implementation details.

### Prioritized Action List Before Coding Begins

| Priority | Action | Blocking? |
|---|---|---|
| **P0** | Complete `corpus_inventory.csv` to cover ALL 13 AMCs with ISID + KIM + Factsheet URLs. Verify every URL resolves. | YES |
| **P0** | Resolve chunking contradictions into ONE canonical spec. | YES |
| **P1** | Define exact PostgreSQL DDL schema. | YES |
| **P1** | Write `prompt_strategy.md` with the exact system prompt, refusal templates, and 5 few-shot examples. | YES |
| **P1** | Create `test_cases.md` with 50 golden Q&A pairs before building the pipeline. | YES |
| **P2** | Downgrade BGE-M3 to `bge-small-en-v1.5` for MVP. | NO |
| **P2** | Replace NL2SQL with parameterized SQL queries. | NO |
| **P2** | Cut BM25 sparse search and cross-encoder reranking from MVP scope. | NO |
| **P2** | Add multi-turn conversation support to the architecture. | NO |
| **P3** | Add post-generation output scanner for compliance. | NO |
| **P3** | Collapse 20 phases into 8 MVP-critical phases. | NO |

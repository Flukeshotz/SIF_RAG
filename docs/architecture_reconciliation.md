# SIF Copilot — Architecture Reconciliation

**Version:** 1.0  
**Owner:** Architecture Review Board  
**Last Updated:** 2026-06-04  
**Purpose:** Resolve all contradictions across project documents and establish canonical specifications.

---

## Conflict 1: Chunking Sizes

**Current State:** Three different chunking specifications exist.

| Document | Specification |
|---|---|
| `problem_statement.md` (L176-178) | Parent: 1500-2500 tokens, Child: 300-500 tokens |
| `architecture.md` (L131-137) | SEBI: Parent 1500 / Child 300. ISIDs: 512/128. Factsheets: 512/DB. FAQs: exact pair. Websites: 768/128 |
| `implementation_plan.md` (L164) | "Test chunk lengths do not exceed 512 tokens" |

**Conflicting Documents:** `problem_statement.md` vs `architecture.md` vs `implementation_plan.md`

**Recommended Resolution:**  
Adopt the `architecture.md` document-type-specific strategy as canonical. The problem statement's "1500-2500 parent" spec was an early design that the architecture refined. The implementation plan's "512 max" test contradicts the SEBI hierarchical parent of 1500 and must be updated.

**Canonical Spec:**

| Document Type | Chunk Size (tokens) | Overlap (tokens) | Strategy |
|---|---|---|---|
| SEBI Circulars | 512 (child), parent header prepended | 128 | Hierarchical with parent context injection |
| ISIDs / KIMs (text) | 512 | 128 | Semantic splitting |
| ISIDs / KIMs (tables) | Entire table (variable) | 0 | Indivisible table chunks |
| Factsheets (commentary) | 512 | 128 | Semantic splitting |
| Factsheets (holdings) | N/A | N/A | Direct to PostgreSQL, not vectorized |
| FAQs | Exact Q&A pair | 0 | Strict boundary chunking |
| AMC Websites | 512 | 128 | Semantic splitting |

**Impact:** Implementation plan Phase 5 acceptance criteria must be updated.  
**Priority:** P0 — Must resolve before Phase 5 begins.

---

## Conflict 2: Embedding Model

**Current State:**

| Document | Specification |
|---|---|
| `problem_statement.md` (L184) | BGE-M3 |
| `architecture.md` (L143) | BGE-M3 |
| `implementation_plan.md` (L175, L185) | BGE-M3 (1024 dimensions) |
| `architecture_review.md` (§1.2) | Recommends downgrading to `bge-small-en-v1.5` (384 dim) for MVP |

**Conflicting Documents:** All original docs agree on BGE-M3. Review recommends `bge-small`.

**Recommended Resolution:**  
Use `bge-small-en-v1.5` for MVP. The corpus is <15K English chunks. BGE-M3's 568M parameters and 1024-dim vectors are unjustified overhead. Swap to BGE-M3 only when adding multilingual content.

**Canonical Spec:**
- **MVP:** `bge-small-en-v1.5` (33M params, 384 dimensions)
- **Post-MVP (multilingual):** `bge-m3` (568M params, 1024 dimensions)

**Impact:** Qdrant collection vector size changes from 1024 to 384. Implementation plan Phase 6 and Phase 7 must update dimension references.  
**Priority:** P2 — Non-blocking but reduces resource requirements significantly.

---

## Conflict 3: Metadata Storage Location

**Current State:**

| Document | Specification |
|---|---|
| `architecture.md` (L71) | PostgreSQL stores "Exit Loads, Min Investment, Fund Manager" |
| `architecture.md` (L171) | Qdrant stores metadata filters for pre-filtering (category, amc) |
| `data_dictionary.md` | Defines all fields but doesn't specify which DB stores what |
| `database_schema.md` | PostgreSQL stores everything in normalized tables |

**Conflicting Documents:** No explicit mapping of which metadata lives in Qdrant payload vs PostgreSQL.

**Recommended Resolution:**  
Define a clear split. Qdrant payload stores ONLY fields needed for search-time filtering. PostgreSQL stores ALL fields.

**Canonical Spec:**

| Field | PostgreSQL | Qdrant Payload |
|---|---|---|
| `fund_name` | ✅ | ✅ (for filtering) |
| `amc` | ✅ | ✅ (for filtering) |
| `category` | ✅ | ✅ (for filtering) |
| `document_type` | ✅ | ✅ (for tier-based boosting) |
| `priority_tier` | ✅ | ✅ (for score weighting) |
| `publication_date` | ✅ | ✅ (for temporal filtering) |
| `risk_band` | ✅ | ❌ |
| `minimum_investment` | ✅ | ❌ |
| `exit_load` | ✅ (normalized table) | ❌ |
| `benchmark` | ✅ | ❌ |
| `fund_manager` | ✅ | ❌ |
| `content_hash` | ✅ | ❌ |
| `is_active` | ✅ | ✅ (mandatory filter) |

**Impact:** Qdrant upsert code must include the 7 payload fields. All other queries go to PostgreSQL.  
**Priority:** P1 — Must be defined before Phase 7 and Phase 8.

---

## Conflict 4: Retrieval Strategy

**Current State:**

| Document | Specification |
|---|---|
| `architecture.md` (L172) | Hybrid: Dense Vector + Sparse BM25 + Reranking |
| `implementation_plan.md` (L255-257) | Hybrid search + SQL search + Reranker |
| `architecture_review.md` (§1.1) | Recommends cutting BM25 and reranking for MVP |

**Conflicting Documents:** Original docs specify full hybrid. Review recommends simplified MVP.

**Recommended Resolution:**  
MVP uses dense vector search with metadata pre-filtering only. No BM25 sparse search. No cross-encoder reranking. These are Phase 2 additions.

**Canonical Spec:**

| Component | MVP | Post-MVP |
|---|---|---|
| Dense Vector Search (Qdrant) | ✅ | ✅ |
| Metadata Pre-filtering | ✅ | ✅ |
| BM25 Sparse Search | ❌ | ✅ |
| Cross-encoder Reranking | ❌ | ✅ |
| NL2SQL | ❌ (use parameterized queries) | ✅ |

**Impact:** Implementation plan Phase 9 is significantly simplified. `retrieval/reranker.py` and `retrieval/hybrid_search.py` (BM25 component) are deferred.  
**Priority:** P2 — Simplification, not blocking.

---

## Conflict 5: SQL Query Strategy

**Current State:**

| Document | Specification |
|---|---|
| `architecture.md` (L181) | NL2SQL Engine routes factoid queries |
| `implementation_plan.md` (L256) | `retrieval/sql_search.py` — "NL2SQL or predefined deterministic queries" |
| `architecture_review.md` (§1.1) | NL2SQL is overengineered for ~91 funds. Use parameterized queries. |

**Recommended Resolution:**  
Use predefined parameterized SQL queries for MVP. With ~91 funds and ~17 metadata fields, the query space is fully enumerable. NL2SQL introduces hallucination risk (malformed SQL).

**Canonical Spec:**
```python
# Predefined query patterns, NOT NL2SQL
def get_fund_by_name(name: str) -> Fund
def get_exit_loads(fund_id: UUID) -> List[ExitLoad]
def get_funds_by_category(category: str) -> List[Fund]
def compare_funds(fund_ids: List[UUID]) -> List[Fund]
def search_funds(filters: FundFilters) -> List[Fund]
```

**Impact:** No NL2SQL engine needed. Removes a complex dependency.  
**Priority:** P2.

---

## Conflict 6: Frontend Technology

**Current State:**

| Document | Specification |
|---|---|
| `architecture.md` (L66) | "Frontend (Next.js / React)" |
| `implementation_plan.md` (L356) | "Assuming Streamlit MVP for speed" |

**Recommended Resolution:**  
Use Streamlit for MVP. It delivers a functional UI in days, not weeks. Migrate to Next.js/React only if the product graduates to production with external users.

**Canonical Spec:**  
- **MVP:** Streamlit  
- **Production (if needed):** Next.js  

**Impact:** None — implementation plan already assumed Streamlit.  
**Priority:** P3.

---

## Conflict 7: LLM Provider

**Current State:**

| Document | Specification |
|---|---|
| `architecture.md` (L239) | "Gemini 1.5 Flash/Pro via API" |
| `implementation_plan.md` (L8, L306) | "Groq LLM" |

**Conflicting Documents:** Architecture says Gemini, implementation plan says Groq.

**Recommended Resolution:**  
Use Groq for MVP (fast inference, free tier available). The system should be LLM-agnostic with a clean abstraction layer so Gemini, OpenAI, or local models can be swapped.

**Canonical Spec:**  
- **MVP:** Groq (Llama 3.x or Mixtral via Groq API)  
- **Abstraction:** `generation/llm.py` implements a `BaseLLM` interface. Provider is configurable via `.env`.

**Impact:** Architecture document should be updated to reflect Groq as primary with Gemini as alternative.  
**Priority:** P1 — Must agree on LLM before Phase 11.

---

## Duplicate Components Identified

| Component | Appears In | Resolution |
|---|---|---|
| `core/config.py` config loading | Phase 0 (created) + each module re-imports | Single import from `core.config.settings`. No duplication needed. |
| Health check endpoint | `main.py` (created in Phase 0) + `api/routes/health.py` (Phase 12) | Remove from `main.py`. Consolidate into `api/routes/health.py` only. |
| Metadata schema | `metadata/schema.py` (Phase 4) + `db/models.py` (Phase 8) | `metadata/schema.py` defines Pydantic extraction models. `db/models.py` defines SQLAlchemy ORM models. Both are needed — they serve different purposes. Not a true duplicate. |

---

## Missing Dependencies Identified

| Phase | Missing Dependency | Resolution |
|---|---|---|
| Phase 9 (Retrieval) | Needs both Phase 7 (Qdrant) AND Phase 8 (PostgreSQL) complete | Correct — already ordered properly |
| Phase 10 (Classification) | Needs Groq API key configured (Phase 0) | Already satisfied by `.env` setup |
| Phase 11 (Generation) | Needs prompts defined | `prompt_strategy.md` now exists — no longer missing |
| Phase 14 (Evaluation) | Needs golden test cases | `golden_test_cases.md` now exists — no longer missing |
| Phase 8 (PostgreSQL) | Needs exact DDL schema | `database_schema.md` now exists — no longer missing |

---

## Final Canonical Architecture Specification

| Component | Canonical Choice | Document of Record |
|---|---|---|
| Embedding Model (MVP) | `bge-small-en-v1.5` (384-dim) | This document |
| Vector Database | Qdrant (single node, Docker) | `architecture.md` |
| Relational Database | PostgreSQL (Docker) | `database_schema.md` |
| LLM Provider (MVP) | Groq API | This document |
| Frontend (MVP) | Streamlit | `implementation_plan.md` |
| Chunking Strategy | Document-type-specific (see Conflict 1 table) | This document |
| Retrieval (MVP) | Dense vector + metadata filtering. No BM25/reranking. | This document |
| SQL Strategy (MVP) | Parameterized queries. No NL2SQL. | This document |
| Citation Storage | Immutable local files (hash-based). S3 deferred. | `architecture_review.md` |
| Prompts | `prompt_strategy.md` v1.0 | `prompt_strategy.md` |
| Metadata Spec | `data_dictionary.md` v1.0 | `data_dictionary.md` |
| DB Schema | `database_schema.md` v1.0 | `database_schema.md` |
| Test Cases | `golden_test_cases.md` v1.0 (56 cases) | `golden_test_cases.md` |
| Edge Cases | `edge_cases.md` v1.0 | `edge_cases.md` |

# SIF Copilot — Database Schema Design

**Version:** 1.0  
**Owner:** Data Engineering  
**Last Updated:** 2026-06-04

---

## Table: `funds`

**Purpose:** Canonical registry of all SIF products. One row per fund. Source of truth for fund-level structured metadata used in SQL-based deterministic queries.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique fund identifier |
| `fund_name` | VARCHAR(255) | NOT NULL | Official SEBI-registered fund name |
| `amc` | VARCHAR(255) | NOT NULL | Asset Management Company name (canonical enum value) |
| `strategy_type` | VARCHAR(100) | NOT NULL | SEBI-defined SIF strategy (e.g., "Hybrid Long-Short") |
| `category` | VARCHAR(100) | NOT NULL | SEBI regulatory category |
| `risk_band` | INTEGER | NOT NULL, CHECK (risk_band BETWEEN 1 AND 5) | SEBI risk-o-meter rating |
| `benchmark` | VARCHAR(255) | | Official benchmark index |
| `minimum_investment` | BIGINT | NOT NULL, CHECK (minimum_investment >= 1000000) | Minimum investment in INR |
| `fund_manager` | VARCHAR(255) | NOT NULL | Lead fund manager name |
| `subscription_frequency` | VARCHAR(50) | | How often subscriptions are accepted |
| `redemption_frequency` | VARCHAR(50) | | How often redemptions are processed |
| `notice_period_days` | INTEGER | CHECK (notice_period_days BETWEEN 0 AND 15) | Redemption notice period (SEBI max 15 working days) |
| `total_expense_ratio` | DECIMAL(5,4) | CHECK (total_expense_ratio <= 0.0225) | Current TER |
| `launch_date` | DATE | | Fund inception / NFO allotment date |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT true | Whether the fund is currently open |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last modification timestamp |

**Unique Constraint:** `UNIQUE (fund_name, amc)`  
**Indexes:** `idx_funds_amc` on (`amc`), `idx_funds_category` on (`category`), `idx_funds_strategy` on (`strategy_type`)

**Example Record:**
```json
{
  "id": "a1b2c3d4-...",
  "fund_name": "Tata Titanium Hybrid Long-Short Fund",
  "amc": "Tata Mutual Fund",
  "strategy_type": "Hybrid Long-Short",
  "category": "Hybrid Long-Short",
  "risk_band": 5,
  "benchmark": "NIFTY 50 Hybrid Composite Debt 50:50 Index",
  "minimum_investment": 1000000,
  "fund_manager": "Rahul Tiwari",
  "subscription_frequency": "Daily",
  "redemption_frequency": "Weekly",
  "notice_period_days": 10,
  "total_expense_ratio": 0.0200,
  "launch_date": "2025-11-15",
  "is_active": true
}
```

---

## Table: `exit_loads`

**Purpose:** Stores multi-tiered exit load structures per fund as normalized rows (not JSONB) for clean SQL filtering.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `fund_id` | UUID | NOT NULL, REFERENCES funds(id) ON DELETE CASCADE | Parent fund |
| `max_days` | INTEGER | | Upper bound of holding period in days (NULL = no limit / thereafter) |
| `load_percentage` | DECIMAL(5,4) | NOT NULL, CHECK (load_percentage >= 0) | Exit load as decimal (e.g., 0.0050 = 0.50%) |
| `effective_date` | DATE | NOT NULL | When this exit load structure became effective |

**Index:** `idx_exit_loads_fund` on (`fund_id`)

**Example Records (SBI Magnum):**
```
fund_id: <sbi_magnum_id>, max_days: 15, load_percentage: 0.0050, effective_date: 2025-04-01
fund_id: <sbi_magnum_id>, max_days: 30, load_percentage: 0.0025, effective_date: 2025-04-01
fund_id: <sbi_magnum_id>, max_days: NULL, load_percentage: 0.0000, effective_date: 2025-04-01
```

---

## Table: `documents`

**Purpose:** Registry of every ingested source document. Tracks versioning, hashing, and lineage for citation integrity.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique document identifier |
| `fund_id` | UUID | REFERENCES funds(id) ON DELETE SET NULL | Associated fund (NULL for regulatory docs) |
| `document_type` | VARCHAR(50) | NOT NULL | Enum: SEBI_CIRCULAR, AMFI_CIRCULAR, ISID, KIM, FACTSHEET, AMC_WEBSITE, FAQ, etc. |
| `title` | VARCHAR(500) | NOT NULL | Document title |
| `source_url` | TEXT | NOT NULL | Original public URL |
| `internal_path` | TEXT | NOT NULL | Internal storage path (hash-based) |
| `content_hash` | CHAR(64) | NOT NULL, UNIQUE | SHA-256 hash of raw file for deduplication |
| `priority_tier` | INTEGER | NOT NULL, CHECK (priority_tier BETWEEN 1 AND 5) | Source reliability tier |
| `publication_date` | DATE | NOT NULL | Document publication date |
| `effective_date` | DATE | | Date content becomes legally binding |
| `version` | VARCHAR(20) | NOT NULL, DEFAULT '1.0' | Document version |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT true | Active version flag (false = superseded) |
| `page_count` | INTEGER | | Number of pages |
| `token_count` | INTEGER | | Estimated total tokens after parsing |
| `ingested_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When document was ingested |

**Indexes:** `idx_documents_fund` on (`fund_id`), `idx_documents_type` on (`document_type`), `idx_documents_active` on (`is_active`), `idx_documents_hash` on (`content_hash`)

---

## Table: `chunks`

**Purpose:** Stores parsed and chunked text segments with their metadata. Each chunk maps to one vector point in Qdrant. The `qdrant_point_id` links the two systems.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique chunk identifier |
| `document_id` | UUID | NOT NULL, REFERENCES documents(id) ON DELETE CASCADE | Parent document |
| `qdrant_point_id` | UUID | UNIQUE | Corresponding point ID in Qdrant collection |
| `content` | TEXT | NOT NULL | Raw chunk text |
| `chunk_index` | INTEGER | NOT NULL | Position of chunk within the document (0-indexed) |
| `chunk_type` | VARCHAR(50) | NOT NULL | "text", "table", "qa_pair", "heading" |
| `token_count` | INTEGER | NOT NULL | Exact token count of chunk content |
| `parent_chunk_id` | UUID | REFERENCES chunks(id) | Parent chunk ID for hierarchical chunking (nullable) |
| `section_header` | TEXT | | Section heading this chunk belongs to |
| `page_number` | INTEGER | | Source PDF page number |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Chunk creation timestamp |

**Indexes:** `idx_chunks_document` on (`document_id`), `idx_chunks_qdrant` on (`qdrant_point_id`), `idx_chunks_parent` on (`parent_chunk_id`)

---

## Table: `citations`

**Purpose:** Maps generated response claims back to specific chunks and documents. Provides the audit trail for every citation displayed to the user.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique citation identifier |
| `response_id` | UUID | NOT NULL | ID of the API response that used this citation |
| `chunk_id` | UUID | NOT NULL, REFERENCES chunks(id) | Chunk that was cited |
| `document_id` | UUID | NOT NULL, REFERENCES documents(id) | Document containing the chunk |
| `citation_label` | VARCHAR(20) | NOT NULL | Display label (e.g., "Source 1") |
| `claim_text` | TEXT | | The specific claim in the response this citation supports |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When citation was generated |

**Indexes:** `idx_citations_response` on (`response_id`), `idx_citations_chunk` on (`chunk_id`)

---

## Table: `retrieval_logs`

**Purpose:** Logs every retrieval operation for debugging, evaluation, and retrieval quality monitoring.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique log identifier |
| `query_text` | TEXT | NOT NULL | Original user query |
| `query_type` | VARCHAR(50) | NOT NULL | Classified query type (PRODUCT, REGULATORY, etc.) |
| `retrieved_chunk_ids` | UUID[] | | Array of chunk IDs returned by retrieval |
| `top_similarity_score` | DECIMAL(5,4) | | Highest cosine similarity score |
| `metadata_filters_applied` | JSONB | | Filters used (e.g., {"amc": "Tata Mutual Fund"}) |
| `retrieval_method` | VARCHAR(50) | NOT NULL | "vector", "sql", "hybrid" |
| `latency_ms` | INTEGER | NOT NULL | Retrieval time in milliseconds |
| `result_count` | INTEGER | NOT NULL | Number of chunks returned |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Timestamp |

**Index:** `idx_retrieval_logs_created` on (`created_at`), partitioned by month

---

## Table: `feedback`

**Purpose:** Stores user thumbs-up/thumbs-down feedback for evaluating response quality over time.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique feedback identifier |
| `response_id` | UUID | NOT NULL | ID of the API response being rated |
| `query_text` | TEXT | NOT NULL | The original question |
| `rating` | SMALLINT | NOT NULL, CHECK (rating IN (-1, 1)) | -1 = thumbs down, 1 = thumbs up |
| `comment` | TEXT | | Optional user comment |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Timestamp |

**Index:** `idx_feedback_created` on (`created_at`)

---

## Table: `ingestion_jobs`

**Purpose:** Tracks the status and history of document ingestion pipeline runs for monitoring and debugging.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Unique job identifier |
| `job_type` | VARCHAR(50) | NOT NULL | "manual", "scheduled_daily", "on_demand" |
| `status` | VARCHAR(20) | NOT NULL | "pending", "running", "completed", "failed" |
| `documents_processed` | INTEGER | DEFAULT 0 | Count of documents successfully processed |
| `documents_failed` | INTEGER | DEFAULT 0 | Count of documents that failed processing |
| `chunks_created` | INTEGER | DEFAULT 0 | Total chunks generated in this job |
| `vectors_upserted` | INTEGER | DEFAULT 0 | Vectors successfully pushed to Qdrant |
| `error_log` | TEXT | | Error details if job failed |
| `started_at` | TIMESTAMP | NOT NULL | Job start time |
| `completed_at` | TIMESTAMP | | Job completion time |

**Index:** `idx_ingestion_jobs_status` on (`status`), `idx_ingestion_jobs_started` on (`started_at`)

---

## Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│    funds     │──1:N──│    documents     │──1:N──│    chunks    │
│              │       │                  │       │              │
│ id (PK)      │       │ id (PK)          │       │ id (PK)      │
│ fund_name    │       │ fund_id (FK)     │       │ document_id  │
│ amc          │       │ document_type    │       │ qdrant_id    │
│ strategy_type│       │ content_hash     │       │ content      │
│ risk_band    │       │ is_active        │       │ chunk_type   │
│ min_invest   │       │ priority_tier    │       │ parent_id(FK)│
└──────┬───────┘       └────────┬─────────┘       └──────┬───────┘
       │                       │                         │
       │1:N                    │                         │1:N
       ▼                       │                         ▼
┌──────────────┐               │                  ┌──────────────┐
│  exit_loads  │               │                  │  citations   │
│              │               │                  │              │
│ id (PK)      │               │                  │ id (PK)      │
│ fund_id (FK) │               │                  │ chunk_id (FK)│
│ max_days     │               │                  │ document_id  │
│ load_pct     │               │                  │ response_id  │
└──────────────┘               │                  └──────────────┘
                               │
                    ┌──────────┴─────────┐
                    │  retrieval_logs    │       ┌──────────────┐
                    │                    │       │   feedback   │
                    │ id (PK)            │       │              │
                    │ query_text         │       │ id (PK)      │
                    │ query_type         │       │ response_id  │
                    │ chunk_ids[]        │       │ rating       │
                    │ latency_ms         │       └──────────────┘
                    └────────────────────┘
                                                ┌──────────────────┐
                                                │ ingestion_jobs   │
                                                │                  │
                                                │ id (PK)          │
                                                │ status           │
                                                │ docs_processed   │
                                                └──────────────────┘
```

---

## Query Patterns

| Query Pattern | SQL | Frequency |
|---|---|---|
| Look up fund by name | `SELECT * FROM funds WHERE fund_name ILIKE '%titanium%'` | Very High |
| Get exit loads for a fund | `SELECT * FROM exit_loads WHERE fund_id = $1 ORDER BY max_days` | High |
| Compare two funds | `SELECT * FROM funds WHERE fund_name IN ($1, $2)` | High |
| Filter by category | `SELECT * FROM funds WHERE category = $1 AND is_active = true` | Medium |
| Get active documents for a fund | `SELECT * FROM documents WHERE fund_id = $1 AND is_active = true ORDER BY publication_date DESC` | High |
| Resolve citation | `SELECT d.title, d.source_url, d.publication_date FROM citations c JOIN chunks ch ON c.chunk_id = ch.id JOIN documents d ON ch.document_id = d.id WHERE c.response_id = $1` | High |
| Check corpus freshness | `SELECT MAX(ingested_at) FROM documents` | Daily |
| Retrieval quality trend | `SELECT DATE(created_at), AVG(top_similarity_score) FROM retrieval_logs GROUP BY 1 ORDER BY 1 DESC LIMIT 30` | Weekly |

---

## Partitioning Strategy

| Table | Partition Method | Key | Rationale |
|---|---|---|---|
| `retrieval_logs` | Range (monthly) | `created_at` | High-volume logging table. Monthly partitions enable efficient cleanup of old logs. |
| `feedback` | Range (monthly) | `created_at` | Moderate volume. Monthly partitions for analysis. |
| `ingestion_jobs` | None | N/A | Low volume (1-2 per day). No partitioning needed. |
| `funds`, `documents`, `chunks` | None | N/A | Small tables (< 10K rows for SIF MVP). Partitioning is unnecessary overhead. |

---

## Versioning Strategy

1. **Document versioning:** When a new version of an ISID/KIM is ingested, the old `documents` record is set to `is_active = false`. The new version gets `is_active = true`. Old chunks remain for historical citation integrity but are excluded from active retrieval via the `is_active` filter on documents.

2. **Schema versioning:** All schema changes are managed via Alembic migrations. Every migration is forward-only (no down migrations in production). Migration scripts are stored in `alembic/versions/`.

---

## Migration Strategy

1. **Initial setup:** `alembic init alembic` → create initial migration with all tables.
2. **Schema changes:** `alembic revision --autogenerate -m "description"` → review generated migration → `alembic upgrade head`.
3. **Production deployments:** Migrations run automatically as part of the deployment pipeline before the application starts.
4. **Rollback:** Restore from database backup. Down migrations are not supported to prevent data loss.

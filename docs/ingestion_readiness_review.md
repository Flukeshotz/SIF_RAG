# Phase 2 Ingestion Readiness Review

**Review Date:** 2026-06-04  
**Scope:** V2 Corpus Inventory (`corpus_inventory_v2.csv`, `source_registry_v2.json`) readiness for Phase 2 (Ingestion Pipeline).

---

## 1. Quantitative Projections

Based on the 79 normalized sources in the V2 registry and the document profiling from the deep research phase, the following ingestion workloads are expected:

### 1. Expected PDF Count
*   **Direct PDFs:** 28 (Extracted directly in V2)
*   **Obscured PDFs:** ~15-20 (Currently recorded as `landing_url` but likely containing statutory PDFs behind JS modals, particularly for ISIDs/KIMs/SEBI Circulars).
*   **Total Expected:** ~45-50 PDFs.

### 2. Expected HTML Page Count
*   **Direct HTML Scrapes:** ~30-35 (Standard AMC websites, philosophical narratives, FAQs, and NFO brochures).
*   **Total Expected:** 51 URLs currently lack a direct PDF link, requiring Playwright intervention to evaluate the DOM.

### 3. Expected Scanned PDF Count
*   **Total Expected:** ~10-12 (Predominantly Tier 1 SEBI Circulars and Master Directions, which are historically hosted as physical, signed, scanned documents).

### 4. Expected OCR & Parsing Workload
*   **Standard OCR:** Moderate (Required for the ~10 scanned SEBI circulars to reconstruct deep hierarchical numbering).
*   **LayoutLM / Tabular Parsing:** Extreme (Required for the 5 ISIDs, 8 KIMs, and 8 Factsheets to preserve complex exit load structures, asset allocation bounds, and tabular limits without token corruption).

### 5. Expected Storage Requirements
*   **Raw Storage:** ~100MB - 150MB (50 PDFs averaging 2-3MB; HTML blobs are negligible).
*   **Processed Storage:** ~50MB (Markdown / HTML tables extracted from PDFs).

### 6. Expected Document Volume
*   **Total Unique Sources:** 79 registered documents/endpoints.

### 7. Expected Token & Chunk Volume
*   **Token Estimates:**
    *   ISIDs (5) @ ~40,000 tokens = 200,000 tokens
    *   KIMs (8) @ ~5,000 tokens = 40,000 tokens
    *   Factsheets (8) @ ~2,000 tokens = 16,000 tokens
    *   Regulatory (10) @ ~10,000 tokens = 100,000 tokens
    *   Web/Other (48) @ ~2,000 tokens = 96,000 tokens
*   **Total Tokens:** ~450,000 tokens.
*   **Chunk Volume:** At a 512-token chunk size with 128-token overlap, anticipate **~1,000 to 1,200 total chunks**.

### 8. Expected Embedding Volume
*   Using `BAAI/bge-small-en-v1.5` (384 dimensions).
*   ~1,200 chunks × 384 dimensions = Highly manageable vector footprint (easily fits in minimal Qdrant memory).

---

## 2. Ingestion Scenarios & Runtimes

| Scenario | Estimated Runtime | Description |
|---|---|---|
| **Best Case** | ~5-10 Minutes | AMCs do not block Playwright. Direct downloads execute quickly. SEBI circulars contain digital text layers requiring minimal OCR. Layout-aware parsers extract tables on the first pass. |
| **Expected Case** | ~20-30 Minutes | Headless scrapers encounter some JS-rendering delays or modal popups. 10% of PDFs require heavy OCR. Chunking algorithms take time to map table hierarchies. |
| **Worst Case** | ~1.5 - 2 Hours | AMC Web Application Firewalls (WAFs) aggressively block IP/Playwright. SEBI scanned documents are highly degraded requiring OCR retries. Memory constraints cause batch processing slowdowns. |

---

## 3. Ingestion Risks

1.  **Playwright Blocking:** 51 URLs currently rely on `playwright_scrape`. If Tata, Edelweiss, or Quant employ advanced anti-bot (Cloudflare/Akamai), the pipeline will stall.
2.  **DOM Volatility:** Scrapers built to click specific "Download ISID" buttons will break if an AMC updates their frontend UI framework.
3.  **Table Flattening:** If the LayoutLM implementation fails on Factsheets, numeric limit data (e.g., exit load tiers) will be flattened into unstructured text, resulting in fatal retrieval hallucinations later.
4.  **Temporal Drift:** We have static links (e.g., `qsif_Factsheet_May_2026.pdf`). Next month, these will 404. The ingestion pipeline must handle HTTP 404s gracefully without crashing the entire batch.

---

## 4. Readiness Decision

**Verdict: A. Ready for Phase 2**

*Reasoning:* The corpus itself is robust, clean, and normalized. We have achieved comprehensive AMC coverage and isolated the exact regulatory bounds. The identified risks (OCR, Playwright blocking, Table flattening) are not flaws in the *corpus registry*, but rather standard engineering challenges that the Phase 2 (Ingestion) architecture is specifically designed to solve. 

Implementation of the downloader, hasher, and storage modules can begin immediately.

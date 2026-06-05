# SIF Copilot — Phase 1.5 Corpus Expansion Report

**Execution Date:** 2026-06-04  
**Scope:** Expand the corpus inventory from 12 initial documents to a comprehensive, production-ready baseline using the 75 URLs identified in `deep_research.txt`.

---

## 1. Overview of Expansion

The corpus has been successfully expanded, normalized, and strictly aligned with the schema.

*   **Initial Sources:** 12
*   **Expanded Sources (v2):** 79
*   **Excluded URLs:** Non-authoritative community and retail portals (e.g., Reddit, YouTube, Groww, Value Research, ET) were actively filtered out during expansion to protect the primary RAG vector space from hallucination.

## 2. AMC Coverage Additions

The registry now features comprehensive coverage across the Indian financial ecosystem, having added the AMCs identified as missing in the previous Phase 1 review:
*   Franklin Templeton
*   Aditya Birla Sun Life
*   ITI Mutual Fund
*   Kotak Mutual Fund
*   Bandhan Mutual Fund
*   The Wealth Company

This achieves the mandate of 100% known AMC representation.

## 3. Data Normalization Executed

1.  **Organization Names:** Consolidated naming variations (e.g., `wsif`, `wealth company` -> `The Wealth Company`; `edelweiss mf` -> `Edelweiss Mutual Fund`) into a strict canonical format to prevent fragmentation.
2.  **Source Types:** Added `SID` and `Master Direction` to the valid types. Normalized classification based on URL signatures and title taxonomy (e.g., mapping `...-KIM.pdf` to `KIM` rather than `ISID`).
3.  **URL Fields:** Split the primary `url` field into `landing_url` and `pdf_url` depending on the file extension. 
4.  **Removed Relevance Score:** The hardcoded `relevance_score` was dropped from `source_schema.json` as it should be dynamically computed by the retrieval engine at runtime.
5.  **Deduplication:** Ensured that duplicate URLs were merged, favoring entries that provided a direct PDF link.

## 4. Deliverables Generated
*   `data/corpus_inventory_v2.csv`
*   `data/source_registry_v2.json`
*   Updated `data/source_schema.json`

The Phase 1.5 baseline is robust and ready to power the Phase 2 document ingestion and scraping pipeline.

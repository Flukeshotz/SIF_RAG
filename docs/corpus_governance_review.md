# SIF Copilot — Corpus Governance Review

**Review Date:** 2026-06-04  
**Scope:** Phase 1 Data Artifacts (`corpus_inventory.csv`, `source_registry.json`, `document_manifest.json`, `source_schema.json`) vs `research_findings.md` and `deep_research.txt`.

---

## 1. Executive Summary

This governance review assesses the health, completeness, and structural integrity of the SIF Copilot corpus registry established in Phase 1. While the schemas and manifests validate technically, the underlying data exhibits severe coverage gaps (only 16% AMC representation), classification errors, and missing metadata fields in the root CSV.

---

## 2. Findings by Category

### 1. Duplicate Organizations
- **Finding:** Inconsistent naming conventions for Asset Management Companies.
- **Details:** The CSV uses `Edelweiss MF`, `ICICI Prudential`, and `Mirae Asset` alongside `Tata Mutual Fund` and `SBI Mutual Fund`. This fragments the "organization" dimension.
- **Severity:** **MEDIUM**
- **Remediation:** Standardize all AMC names to a canonical format (e.g., "Edelweiss Mutual Fund", "ICICI Prudential AMC") governed by a strict enum in the validation script.

### 2. Duplicate URLs
- **Finding:** Malformed URLs with trailing text.
- **Details:** Row 11 in the CSV contains `https://iiflmf.com/sites/mf/files/2023-10/360ONE-Focused-Equity-Fund-KIM.pdf (Reference Path)`. The trailing text invalidates the URI format and will break the download pipeline.
- **Severity:** **HIGH**
- **Remediation:** Strip trailing text and strictly enforce RFC 3986 URI validation on the `url` column.

### 3. Missing AMC Coverage
- **Finding:** Severe gap in market representation.
- **Details:** The registry only contains 7 AMCs. `deep_research.txt` explicitly identifies 13+ active SIF AMCs. Missing institutions include: Franklin Templeton, Aditya Birla Sun Life, ITI Mutual Fund, Kotak Mutual Fund, Bandhan Mutual Fund, and The Wealth Company.
- **Severity:** **CRITICAL**
- **Remediation:** Expand the CSV to include at least one Tier 3 document (ISID/KIM) for every AMC identified in the deep research.

### 4. Missing Source Categories
- **Finding:** Absence of SIDs and specific regulatory structures.
- **Details:** The registry lacks `SID` (Scheme Information Document) as a defined source type, despite it being a legally distinct and critical document alongside `ISID` and `KIM`. Additionally, Master Directions are missing from the Tier 1 categories.
- **Severity:** **MEDIUM**
- **Remediation:** Update `VALID_SOURCE_TYPES` in the schema and validation script to include `SID` and `Master Direction`.

### 5. Missing Metadata
- **Finding:** The root CSV lacks fields required by the JSON schema.
- **Details:** `corpus_inventory.csv` only tracks `title`, `url`, `source_type`, `organization`, and `priority`. It is missing `pdf_url`, `ingestion_method`, `status`, `relevance_score`, and `last_reviewed`. These were hardcoded during the JSON transformation.
- **Severity:** **HIGH**
- **Remediation:** Expand the CSV columns to exactly match the 11 fields defined in `source_schema.json`.

### 6. Invalid Source Classifications
- **Finding:** Misalignment between titles, types, and actual URLs.
- **Details:** The 360 ONE document is titled "DynaSIF Equity Long-Short ISID" and classified as `source_type: ISID`, but the URL points directly to `360ONE-Focused-Equity-Fund-KIM.pdf`. A KIM is legally distinct from an ISID. 
- **Severity:** **HIGH**
- **Remediation:** Audit and correct the `source_type` classification for 360 ONE. 

### 7. Missing PDF Links
- **Finding:** `pdf_url` is null for highly deterministic Tier 1 and Tier 3 sources.
- **Details:** The SEBI Circular (Tier 1) and ISIDs for Tata, Edelweiss, and 360 ONE point to HTML landing pages rather than direct PDF download links. While Playwright can scrape these, Tier 1 and 3 documents must have direct `pdf_url` paths mapped to guarantee ingestion stability.
- **Severity:** **HIGH**
- **Remediation:** Manually locate and populate the direct `.pdf` URLs for all Tier 1, 2, and 3 sources in the registry.

### 8. Priority Tier Inconsistencies
- **Finding:** Unorthodox combination of source types in the schema.
- **Details:** The schema allows `"AMC Website / Brochure"` as a source type mapped to Tier 5. This blends a medium (Website) with a document format (Brochure).
- **Severity:** **LOW**
- **Remediation:** Split `"AMC Website"` and `"Brochure"` into distinct valid enums, both remaining at Tier 5.

### 9. Relevance Score Inconsistencies
- **Finding:** Relevance scores are arbitrary.
- **Details:** The `relevance_score` field in the JSON registry was populated using hardcoded, assumed values (Tier 1 = 1.0, Tier 5 = 0.5) because the architecture does not formally define a static relevance scoring formula.
- **Severity:** **MEDIUM**
- **Remediation:** Remove `relevance_score` from the static registry. Relevance scoring should be a dynamic, compute-time formula applied during retrieval (e.g., `score = cosine_similarity * tier_weight`), as defined in the retrieval architecture.

### 10. Sources Referenced in Research but Absent from Registry
- **Finding:** High-value documents cited in architectural research are missing.
- **Details:** `deep_research.txt` cites over 75 specific source URLs that establish the foundation of the SIF copilot. Critical missing documents include:
  - Franklin Templeton Sapphire KIM
  - Aditya Birla Apex Hybrid Long-Short NFO/SID
  - Edelweiss Altiva Factsheet (Jan 2026)
  - DSP Endurance Factsheet (Jan 2026)
  - HSBC RedHex Hybrid Long-Short Product Note
  - AMFI NAV historical tracking pages
- **Severity:** **CRITICAL**
- **Remediation:** Execute a complete port of all 75 URLs from `deep_research.txt` into `corpus_inventory.csv` to achieve the required 100% corpus baseline before ingestion begins.

---

## 3. Remediation Plan (Next Steps)

1. **Schema Update:** Remove `relevance_score` from `source_schema.json`. Add `SID` and `Master Direction` to the `source_type` enum.
2. **CSV Expansion:** Add the missing columns (`pdf_url`, `ingestion_method`, `status`, `last_reviewed`) to `data/corpus_inventory.csv`.
3. **Data Porting:** Manually extract the remaining 60+ URLs from `deep_research.txt` into the CSV, ensuring 100% AMC coverage (all 13 AMCs).
4. **Data Cleansing:** Fix the 360 ONE KIM/ISID classification mismatch, standard AMC names, and strip trailing text from URLs.
5. **Re-run Validation:** Execute `python scripts/validate_corpus.py` to ensure the cleansed, expanded CSV passes all checks.
6. **Re-generate JSONs:** Rebuild `source_registry.json` and `document_manifest.json` from the cleansed CSV.

# SIF Copilot — Data Dictionary

**Version:** 1.0  
**Owner:** Data Engineering  
**Last Updated:** 2026-06-04  
**Status:** Source of Truth for all metadata extraction

---

## 1. Metadata Dictionary

### Fund-Level Fields

| Field Name | Data Type | Required | Example Value | Source | Validation Rule | Description |
|---|---|---|---|---|---|---|
| `fund_name` | VARCHAR(255) | YES | "Tata Titanium Hybrid Long-Short Fund" | ISID Title Page | Non-empty, unique per AMC+category combination | Official SEBI-registered fund name as stated in the ISID |
| `amc` | VARCHAR(255) | YES | "Tata Mutual Fund" | ISID, KIM | Must match `AMC_ENUM` values | Asset Management Company operating the fund |
| `strategy_type` | VARCHAR(100) | YES | "Hybrid Long-Short" | ISID Section: Investment Objective | Must match `STRATEGY_ENUM` values | SEBI-defined SIF strategy classification |
| `category` | VARCHAR(100) | YES | "Hybrid Long-Short" | ISID, SEBI Circular | Must match `CATEGORY_ENUM` values | SEBI regulatory category bucket |
| `risk_band` | INTEGER | YES | 5 | KIM Risk-o-meter section | Integer between 1 and 5 inclusive | SEBI-mandated risk-o-meter rating (1=Low, 5=Very High) |
| `benchmark` | VARCHAR(255) | YES | "NIFTY 50 Hybrid Composite Debt 50:50 Index" | ISID, KIM | Non-empty string | Official benchmark index tracked by the fund |
| `minimum_investment` | BIGINT | YES | 1000000 | KIM, ISID | Must be >= 1000000 (₹10 Lakh) for SIFs | Minimum initial investment in INR (paisa-free integer) |
| `exit_load` | JSONB | YES | `[{"days": 90, "pct": 0.50}, {"days": null, "pct": 0.0}]` | KIM Exit Load section | Valid JSON array of {days, pct} objects | Multi-tiered exit load structure |
| `subscription_frequency` | VARCHAR(50) | YES | "Daily" | ISID, KIM | Must match `FREQUENCY_ENUM` | How often new investments are accepted |
| `redemption_frequency` | VARCHAR(50) | YES | "Weekly" | ISID, KIM | Must match `FREQUENCY_ENUM` | How often redemptions are processed |
| `fund_manager` | VARCHAR(255) | YES | "Rahul Tiwari" | ISID Fund Manager section | Non-empty string | Lead fund manager name |
| `launch_date` | DATE | NO | "2025-11-15" | ISID, KIM | Valid date, cannot be before 2025-04-01 | NFO allotment date or fund inception date |
| `total_expense_ratio` | DECIMAL(5,4) | NO | 0.0225 | Factsheet, KIM | Must be between 0.0000 and 0.0225 | Current TER as a decimal (max 2.25% for first ₹500 Cr) |
| `notice_period_days` | INTEGER | NO | 15 | ISID, FAQ | Must be between 0 and 15 | SEBI-mandated maximum working days for redemption notice |

### Document-Level Fields

| Field Name | Data Type | Required | Example Value | Source | Validation Rule | Description |
|---|---|---|---|---|---|---|
| `document_type` | VARCHAR(50) | YES | "ISID" | File classification | Must match `DOCTYPE_ENUM` | Category of the source document |
| `source_url` | TEXT | YES | "https://tatamutualfund.com/..." | Corpus inventory | Valid URL format (https://) | Original public URL where document was found |
| `internal_url` | TEXT | YES | "storage/raw/a1b2c3d4.pdf" | Ingestion pipeline | Must reference existing file hash | Internal immutable storage path |
| `publication_date` | DATE | YES | "2026-02-26" | Document header/footer | Valid date, not in the future | Date the document was published by the source |
| `effective_date` | DATE | NO | "2025-04-01" | SEBI Circulars | Valid date | Date the regulatory rule or document becomes legally binding |
| `version` | VARCHAR(20) | YES | "1.0" | Ingestion pipeline | Semantic version format (X.Y) | Document version for tracking updates |
| `last_updated` | TIMESTAMP | YES | "2026-06-04T10:30:00Z" | System-generated | Auto-generated UTC timestamp | When this record was last modified in the database |
| `content_hash` | CHAR(64) | YES | "e3b0c44298fc1c..." | SHA-256 of raw file | Exactly 64 hex characters | Cryptographic hash for deduplication and immutability |
| `is_active` | BOOLEAN | YES | true | Ingestion pipeline | Boolean | Whether this is the current active version (false = superseded) |
| `priority_tier` | INTEGER | YES | 3 | Corpus inventory mapping | Integer between 1 and 5 | Source reliability tier (1=SEBI, 5=Marketing) |

---

## 2. Enumerations

### `AMC_ENUM`
```
SBI Mutual Fund
Tata Mutual Fund
Edelweiss Mutual Fund
ICICI Prudential Mutual Fund
Quant Mutual Fund
Franklin Templeton Mutual Fund
Aditya Birla Sun Life Mutual Fund
HSBC Mutual Fund
ITI Mutual Fund
360 ONE Mutual Fund
DSP Mutual Fund
Kotak Mutual Fund
Mirae Asset Mutual Fund
Bandhan Mutual Fund
The Wealth Company Mutual Fund
```

### `STRATEGY_ENUM`
```
Hybrid Long-Short
Equity Long-Short
Equity Ex-Top 100 Long-Short
Sector Rotation Long-Short
Debt Long-Short
Sectoral Debt Long-Short
Active Asset Allocator
```

### `CATEGORY_ENUM`
Same as `STRATEGY_ENUM`. SEBI defines one strategy = one category. No fund can hold multiple categories.

### `DOCTYPE_ENUM`
```
SEBI_CIRCULAR
AMFI_CIRCULAR
ISID
KIM
FACTSHEET
AMC_WEBSITE
FAQ
INVESTOR_PRESENTATION
PRODUCT_BROCHURE
```

### `FREQUENCY_ENUM`
```
Daily
Weekly
Fortnightly
Monthly
Quarterly
Interval
```

### `RISK_BAND_ENUM`
| Value | Label |
|---|---|
| 1 | Low |
| 2 | Low to Moderate |
| 3 | Moderate |
| 4 | Moderately High |
| 5 | Very High |

---

## 3. Validation Rules

| Rule ID | Field(s) | Rule | Severity |
|---|---|---|---|
| V001 | `minimum_investment` | Must be >= 1000000 for all SIF funds | ERROR |
| V002 | `risk_band` | Must be integer in range [1, 5] | ERROR |
| V003 | `strategy_type` | Must exist in `STRATEGY_ENUM` | ERROR |
| V004 | `amc` | Must exist in `AMC_ENUM` | ERROR |
| V005 | `publication_date` | Cannot be a future date | ERROR |
| V006 | `launch_date` | Cannot be before 2025-04-01 (SIF framework effective date) | WARNING |
| V007 | `total_expense_ratio` | Must be <= 0.0225 (2.25%) | WARNING |
| V008 | `exit_load` | JSON array must have at least one entry | ERROR |
| V009 | `content_hash` | Must be unique across all active documents | ERROR |
| V010 | `fund_name` + `amc` | Combination must be unique | ERROR |
| V011 | `notice_period_days` | Cannot exceed 15 (SEBI max) | ERROR |
| V012 | `source_url` | Must start with `https://` | WARNING |

---

## 4. Source Mapping

Where each field is extracted from, ordered by extraction reliability:

| Field | Primary Source | Secondary Source | Extraction Method |
|---|---|---|---|
| `fund_name` | ISID Title Page | KIM Header | Regex: first occurrence of fund name pattern |
| `amc` | ISID Cover Page | KIM Header | Regex: "managed by" or AMC logo text |
| `strategy_type` | ISID Investment Objective | SEBI Filing | Enum matching from text classification |
| `risk_band` | KIM Risk-o-meter | ISID Risk Section | OCR + image classification of risk-o-meter graphic |
| `benchmark` | KIM Key Information Table | ISID Benchmark Section | Regex: "Benchmark" row in KIM table |
| `minimum_investment` | KIM Key Information Table | ISID | Regex: currency pattern near "minimum" keyword |
| `exit_load` | KIM Exit Load Table | ISID | Table extraction → JSON transformation |
| `subscription_frequency` | KIM / ISID Transaction Section | FAQ | Keyword extraction: "subscription" context |
| `redemption_frequency` | KIM / ISID Transaction Section | FAQ | Keyword extraction: "redemption" context |
| `fund_manager` | ISID Fund Manager Section | KIM | Regex: names following "Fund Manager" heading |
| `publication_date` | Document header/footer | PDF metadata | Date regex extraction |

---

## 5. Metadata Ownership

| Responsibility | Owner | Update Frequency |
|---|---|---|
| Enum maintenance (new AMCs, strategies) | Data Engineering | On SEBI notification |
| Validation rule updates | Data Engineering | On regulatory change |
| Field additions/changes | Data Architecture (requires review) | Per release cycle |
| Extraction accuracy monitoring | QA / Evaluation | Weekly during pilot, monthly in production |
| Source URL verification | Ingestion Pipeline (automated) | Daily |

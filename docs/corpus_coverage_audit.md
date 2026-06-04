# Phase 2.75 — Corpus Coverage Audit

This document audits the coverage of the 36-source MVP corpus after the deterministic PDF download pass, evaluating which documents are truly necessary for the SIF Copilot MVP.

## 1. Source Coverage Matrix

| Source ID | Type | Status | Criticality |
|----------|----------|----------|----------|
| `sebi-sebi-circular` | SEBI Circular | Downloaded | Critical |
| `sebi-sebi-circular-1` | SEBI Circular | Missing PDF URL | Critical |
| `sebi-sebi-circular-2` | SEBI Circular | Missing PDF URL | Optional |
| `sebi-sebi-circular-3` | SEBI Circular | Downloaded | Critical |
| `sebi-sebi-circular-4` | SEBI Circular | Missing PDF URL | Optional |
| `sebi-sebi-circular-5` | SEBI Circular | Downloaded | Critical |
| `sebi-sebi-circular-6` | SEBI Circular | Missing PDF URL | Optional |
| `sebi-sebi-circular-7` | SEBI Circular | Missing PDF URL | Optional |
| `sebi-sebi-circular-8` | SEBI Circular | Missing PDF URL | Duplicate |
| `amfi-amfi-circular` | AMFI Circular | Downloaded | Critical |
| `amfi-amfi-circular-1` | AMFI Circular | Missing PDF URL | Optional |
| `amfi-amfi-circular-2` | AMFI Circular | Missing PDF URL | Optional |
| `amfi-amfi-circular-3` | AMFI Circular | Downloaded | Duplicate |
| `edelweiss-mutual-fund-isid` | ISID | Failed Download | Critical |
| `tata-mutual-fund-isid` | ISID | Missing PDF URL | Critical |
| `quant-mutual-fund-isid` | ISID | Downloaded | Critical |
| `external--uncategorized-isid` | ISID | Downloaded | Critical |
| `external--uncategorized-isid-1` | ISID | Downloaded | Critical |
| `quant-mutual-fund-sid` | SID | Missing PDF URL | Duplicate |
| `icici-prudential-amc-kim` | KIM | Downloaded | Important |
| `franklin-templeton-kim` | KIM | Downloaded | Important |
| `the-wealth-company-kim` | KIM | Missing PDF URL | Important |
| `360-one-mutual-fund-kim` | KIM | Failed Download | Important |
| `dsp-mutual-fund-factsheet` | Factsheet | Downloaded | Optional |
| `icici-prudential-amc-factsheet` | Factsheet | Downloaded | Optional |
| `quant-mutual-fund-factsheet` | Factsheet | Downloaded | Optional |
| `edelweiss-mutual-fund-factsheet` | Factsheet | Failed Download | Optional |
| `external--uncategorized-factsheet` | Factsheet | Downloaded | Optional |
| `the-wealth-company-factsheet` | Factsheet | Missing PDF URL | Optional |
| `hsbc-mutual-fund-brochure` | Brochure | Missing PDF URL | Optional |
| `sbi-mutual-fund-amc-website` | AMC Website | Missing PDF URL | Optional |
| `mirae-asset-mutual-fund-amc-website` | AMC Website | Missing PDF URL | Optional |
| `iti-mutual-fund-amc-website` | AMC Website | Missing PDF URL | Optional |
| `kotak-mutual-fund-amc-website` | AMC Website | Missing PDF URL | Optional |
| `aditya-birla-sun-life-amc-website` | AMC Website | Missing PDF URL | Optional |
| `bandhan-mutual-fund-amc-website` | AMC Website | Missing PDF URL | Optional |

---

## 2. Answers to Analytical Questions

**1. Which missing documents are truly required for MVP?**
- `edelweiss-mutual-fund-isid` (Failed via WAF, requires manual download)
- `tata-mutual-fund-isid` (Requires manual download of the PDF)
- `360-one-mutual-fund-kim` (Failed, requires manual download)
- `the-wealth-company-kim` (Requires manual download)
We absolutely need the core ISID or KIM for these four AMCs to accurately answer questions about their specific SIF strategies, exit loads, and fund managers. 

**2. Which missing documents are redundant because the same information exists in another document?**
- **Blogs Misclassified as Circulars:** `sebi-sebi-circular-2`, `4`, `6`, and `7` are actually blog posts from Groww, ET Money, and thealtinvestor.in. They are entirely redundant because we successfully downloaded the *actual* SEBI regulatory framework document (`sebi-sebi-circular`).
- **Duplicate SEBI Circulars:** `sebi-sebi-circular-1` and `8` point to the same framework we already possess.
- **YouTube SIDs:** `quant-mutual-fund-sid` is a YouTube link. It is redundant because we successfully downloaded the text PDF `quant-mutual-fund-isid`.
- **AMFI Landing Pages:** `amfi-amfi-circular-1` and `2` are just HTML landing pages. We already have the official `amfi-amfi-circular` PDF.

**3. What is the minimum document set required to answer the core queries?**
- **What is SIF? Who can invest? Taxation?** 
  - Answered completely by: `sebi-sebi-circular` and `amfi-amfi-circular`.
- **Minimum investment? Exit load? Risk band? Fund manager? Strategy differences?**
  - Answered completely by: The ISID (or KIM, if ISID is missing) of each respective AMC. (e.g., `quant-mutual-fund-isid`, `icici-prudential-amc-kim`).

---

## 3. Recommended MVP Corpus

To achieve near 100% retrieval reliability with minimal vector noise, the final MVP corpus should be strictly limited to the following:

### Must Have
- The 3 base regulatory PDFs (`sebi-sebi-circular`, `sebi-sebi-circular-3`, `amfi-amfi-circular`).
- The 5 successfully downloaded ISIDs and KIMs (`quant-mutual-fund-isid`, `external--uncategorized-isid`, `external--uncategorized-isid-1`, `icici-prudential-amc-kim`, `franklin-templeton-kim`).
- The 4 missing critical ISIDs/KIMs that MUST be manually hunted and downloaded (`edelweiss-mutual-fund-isid`, `tata-mutual-fund-isid`, `the-wealth-company-kim`, `360-one-mutual-fund-kim`).
*(Total: 12 Documents)*

### Nice To Have
- The successfully downloaded Factsheets (DSP, ICICI, Quant, External) to provide the LLM with recent AUM sizes and performance benchmarks.
*(Total: ~4-5 Documents)*

### Ignore
- **All** 15+ missing AMC marketing websites, blog posts, ET Money articles, YouTube videos, and HTML landing pages. Including these in the vector database will only induce hallucinations and dilute the authoritative truths defined in the ISIDs and SEBI circulars.

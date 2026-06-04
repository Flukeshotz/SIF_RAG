# Phase 3 Readiness Verdict

**Evaluation Date:** 2026-06-04  
**Scope:** Phase 2.5 Live Acquisition Audit Results

---

## 1. Live Audit Summary

The live ingestion audit against the 79 normalized sources yielded the following hard metrics:
- **Total Sources:** 79
- **Successful Downloads:** 60 (76% success rate)
- **Failed Downloads:** 19 (24% failure rate)
- **PDFs Acquired:** 18
- **HTML Acquired:** 40

### Error Breakdown
- **403 Forbidden:** 5 (Edelweiss Mutual Fund is aggressively blocking `httpx` requests via WAF).
- **Timeouts:** 1 (HSBC)
- **Connection Errors:** 12 (Likely aggressive rate limiting triggered by the batch concurrency of 10 concurrent requests).
- **429 Too Many Requests:** 1 (SEBI)

---

## 2. Architectural Implications for Phase 3

The audit proves that proceeding directly to Phase 3 (Document Parsing / Chunking) with the current acquisition pipeline would be catastrophic. 

1. **WAF Blocking:** Edelweiss and SEBI are blocking or rate-limiting standard Python HTTP clients. We require robust header spoofing, proxy rotation, or full browser emulation (Playwright) to bypass these.
2. **Hidden PDFs:** We only acquired 18 PDFs. Many of the 40 HTML pages successfully downloaded are actually landing pages that obscure the required ISID/KIM PDFs behind JavaScript modals or download buttons. Phase 3 cannot parse a PDF if Phase 2 only handed it the raw HTML of a landing page.
3. **Concurrency Limits:** The 12 connection errors indicate that our naive async concurrency limit of 10 is too aggressive for the notoriously fragile Indian AMC server infrastructure.

---

## 3. Verdict

**Verdict: C. Significant Ingestion Issues**

**Reasoning:** 
A 24% failure rate coupled with the failure to extract the actual PDFs from HTML landing pages means the pipeline is starving. We cannot begin building expensive LayoutLM PDF parsers and complex vector chunking algorithms until we can reliably extract the underlying PDFs from Edelweiss, Tata, and SEBI. 

**Recommended Action:** 
Before starting Phase 3, we must rewrite the Phase 2 `downloader.py` to:
1. Integrate Playwright for `403 Forbidden` bypasses and JS rendering.
2. Implement strict concurrency limits (e.g., max 2 concurrent connections per domain).
3. Introduce DOM parsing logic to extract actual PDF `.href` links from the HTML landing pages.

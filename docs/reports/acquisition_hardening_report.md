# Phase 2.6 Acquisition Hardening Report

**Execution Date:** 2026-06-04  
**Goal:** Increase successful acquisition rate above 90%.

---

## 1. Hardening Measures Implemented

To combat the 24% failure rate discovered in Phase 2.5, we implemented a sophisticated, multi-engine routing matrix:

1. **Playwright Downloader Integration:** We refactored `ingestion/downloader.py` to support headless Chromium via `async_playwright()`. 
2. **Domain-Specific Routing (`config/domain_policies.json`):** We mapped domains to specific routing strategies:
   - `static` (httpx)
   - `dynamic` (Playwright awaiting network idle)
   - `waf` (Playwright with stealth-mimicking artificial delays)
3. **DOM Healing (PDF Discovery):** Built `discover_pdf_links()` utilizing `BeautifulSoup`. If a static HTML page is returned but the architecture demands a PDF (e.g., an ISID), the DOM is parsed to extract the direct `.pdf` blob link automatically.
4. **Domain Semaphores:** Enforced `asyncio.Semaphore` pooling mapped per-domain to strictly regulate concurrent connections and prevent `429 Too Many Requests`.

---

## 2. Hardening Audit Results (V2)

The V2 Live Audit was executed under the new hardening rules. The results were:

- **Total Sources:** 79
- **Successful Downloads:** 48 (60.8%)
- **Failed Downloads:** 31 (39.2%)
- **PDF Count:** 9
- **HTML Count:** 37

### Failure Analysis

Despite the architectural upgrades, the success rate actually *decreased* from 76% to 60.8%. 
1. **Edelweiss WAF Persistence:** The 403 Forbidden blocks remain. Playwright without an advanced stealth plugin (e.g., `playwright-stealth`) or residential proxy rotation is still being aggressively fingerprinted by Edelweiss' CDN (likely Akamai or Cloudflare).
2. **Playwright Instability:** Replacing `httpx` with headless Chromium introduced `unknown_error` failures for several AMCs. Spinning up and tearing down dozens of Chromium contexts asynchronously caused sporadic process failures and timeouts within the 30-60s limit.
3. **Connection Drops:** The final 12 connection errors from Phase 2.5 reappeared exactly as before, indicating that the AMC servers might be blocking the IP level rather than just rate-limiting concurrent bursts.

---

## 3. Verdict

**Verdict: B. More Acquisition Work Needed**

**Reasoning:**
We failed to achieve the >90% success threshold. The pipeline is currently acquiring only 60.8% of the raw documents. Proceeding to Phase 3 (Parsing) with a starving, unstable ingestion engine will result in a crippled Copilot.

**Required Next Steps:**
The native `async_playwright` implementation is insufficient against Enterprise WAFs. We must:
1. Integrate `playwright-stealth` to strip WebDriver flags.
2. Integrate a rotating residential proxy pool (e.g., BrightData / Oxylabs) to distribute the IP footprint and solve the connection drops.
3. Decouple the Playwright architecture into a persistent background queue rather than launching ephemeral browsers per-request.

# SIF Copilot — Acquisition Strategy

## Overview
The Indian Asset Management industry employs aggressive anti-bot protections, web application firewalls (WAFs), and dynamic JavaScript rendering that easily blocks standard HTTP ingestion pipelines. 

To guarantee a >90% raw document acquisition rate for the SIF Copilot corpus, we utilize a hardened, multi-tier routing matrix.

## The Routing Matrix

| Route | Engine | Use Case | Domain Examples |
|---|---|---|---|
| **Static** | `httpx` | Fast, unprotected statutory file hosts. | `nsdl.co.in`, `amfiindia.com` |
| **Dynamic** | Playwright (Headless) | Sites requiring JS to render content or validate headers before serving PDFs. | `tatamutualfund.com`, `qsif.com` |
| **WAF Protected** | Playwright (Stealth) | Sites that actively block bot user agents or IPs. Requires viewport spoofing and forced network idles. | `edelweissmf.com` |

## Discovery Protocol (DOM Healing)
Many SIF "documents" registered in the corpus (e.g., Factsheets, KIMs) are actually URLs pointing to HTML landing pages rather than direct `.pdf` blobs. 

If the architecture expects a PDF (`source_type: ISID`, `KIM`, etc.), but the Downloader receives `text/html`, the engine will intercept the payload. It loads the DOM into BeautifulSoup, searches for `<a>` tags matching signature strings ("ISID", "Download", ".pdf"), and automatically re-routes the ingestion to the discovered binary blob.

## Concurrency Limits
Due to legacy infrastructure, domains like `sebi.gov.in` will aggressively drop connections if hit with >5 concurrent requests. `config/domain_policies.json` maps strict asynchronous Semaphores per domain (e.g., `max_concurrent: 2`) to ensure we gracefully siphon data without triggering DDoS protections.

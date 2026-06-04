# SIF Copilot: UI Discovery & Product Design Audit

## 1. Product Vision
**What product actually exists today?**
SIF Copilot is a highly compliant, Retrieval-Augmented Generation (RAG) intelligence engine powered by a curated, locally-indexed vector database (Qdrant) and LLM synthesis (Llama 3.1 on Groq). It strictly answers financial queries based *only* on a verified corpus of SEBI circulars, ISIDs, KIMs, and Factsheets.
**What user problem does it solve?**
Navigating India’s newly regulated Specialized Investment Fund (SIF) ecosystem is incredibly dense. The product solves the "hallucination and trust" problem in financial AI by guaranteeing that every generative output is backed by an explicit citation linking to an authoritative document, while actively blocking illegal investment advice.
**Who are the users?**
B2B Financial Professionals (Wealth Managers, Mutual Fund Distributors, Research Analysts, Compliance Officers) and sophisticated Retail Investors (HNIs).

---

## 2. User Personas
- **Research Analyst:** Needs rapid extraction of fund manager strategies and asset allocation limits from 100-page ISIDs without reading them manually.
- **Mutual Fund Distributor (MFD):** Needs objective, factual comparisons of SIF products to present to clients without accidentally providing unauthorized portfolio recommendations.
- **Compliance Officer:** Uses the tool to verify SEBI guidelines (e.g., short exposure limits, TER caps) against AMC marketing claims.
- **High Net Worth Individual (HNI):** Wants to understand the mechanics of long-short strategies before committing the ₹10 Lakh minimum investment.

---

## 3. Core User Journeys
- **Regulatory Exploration Workflow:** User asks a SEBI-level question ("What is the max unhedged short exposure?"). The system retrieves Tier 1 SEBI Circulars and answers deterministically.
- **Fund Comparison Workflow:** User asks to compare two specific funds. The system retrieves chunks for both, extracts objective data (exit loads, benchmarks), and outputs a structured Markdown table.
- **Source Verification Workflow:** User receives an answer with a `[Source 1]` citation. They need to seamlessly view the original text, document type, and AMC to trust the claim.
- **Compliance Rejection Workflow:** User asks for investment advice ("Which SIF is safest?"). The system intercepts, fires a standard refusal guardrail, and pivots the user back to educational exploration.

---

## 4. Existing Product Capabilities
The backend already fully supports:
- **Source-backed semantic retrieval:** 384-D vector search via `BAAI/bge-small-en-v1.5`.
- **Context assembly:** Deterministic prompt construction with a hard 6,000-token limit.
- **Citation generation:** Post-processing mapping of LLM markers to Qdrant metadata.
- **Strict Compliance Guardrails:** Deterministic refusals for return prediction, portfolio construction, and advisory queries.
- **Fund comparison support:** Prompt constraints forcing objective markdown tables without declaring winners.

---

## 5. Hidden Product Strengths
- **Chunk-Level Traceability:** The backend doesn't just know the document; it knows the exact `chunk_id` and semantic paragraph the claim came from.
- **Metadata Payload:** Every Qdrant point contains rich filtering metadata (`fund_name`, `organization`, `document_type`, `priority_tier`) which is currently invisible to the end user but incredibly powerful for faceted search.
- **Zero-Hallucination Architecture:** Grounding rules (temperature 0.0, strict retrieval-first prompts) make the engine exceptionally trustworthy.

---

## 6. Product Gaps (Prioritized for UI)
- **P0: Split-Pane Citation Explorer.** The generated `[Source N]` tags are useless unless clicking them surfaces the actual metadata and chunk text.
- **P0: Faceted Pre-Filtering.** Users need UI toggles to restrict their search to specific AMCs or Document Types (e.g., "Search only in SEBI Circulars").
- **P1: Markdown Data Grid Rendering.** Standard markdown tables look poor in chat. The UI must intercept markdown tables and render them as beautiful, sortable data grids.
- **P1: Guardrail Visual States.** When the system refuses a query (Advisory Block), the UI should visually indicate a "Compliance Block" state (e.g., distinct colors/icons) rather than looking like a normal chat failure.
- **P2: Feedback Telemetry (Thumbs Up/Down).**

---

## 7. Information Architecture
*Do NOT design a standard ChatGPT clone. Think Bloomberg Terminal meets Perplexity.*
- **Left Sidebar:** 
  - Corpus Health Widget (Total indexed chunks, last sync date).
  - Quick Filters (Checkboxes for AMC, Document Types, SEBI Categories) mapping directly to Qdrant payload filters.
- **Main Center (Split Pane):**
  - **Left Pane (Search & Feed):** Conversational input, rendering of answers, data grids, and inline citation pills.
  - **Right Pane (Evidence Explorer):** Hidden by default. When a citation pill is clicked, this pane slides in to display the Document Title, AMC, Date, and the exact highlighted chunk text.
- **Top Bar:** 
  - Disclaimer banner: *"Educational Purposes Only. Not Investment Advice."*

---

## 8. UI Recommendation
- **Primary Screen:** The "Research Desk" (Split-pane layout described above).
- **Typography & Color:** Professional Fintech. Dark mode by default (slate/navy tones), high-contrast white text, subtle gold/blue accents for citations.
- **Citation Explorer:** Cards displaying the chunk with a clear hierarchy: `[Tier 1: SEBI Circular]` at the top, followed by the text.
- **Comparison Layout:** When a markdown table is detected in the LLM response, swap the UI component to a full-width React Table with sticky headers.

---

## 9. PM Showcase Opportunities (Recruiter Hooks)
- **"Trust as a Feature":** Highlighting the Evidence Explorer proves you understand that in B2B fintech, transparency *is* the product.
- **"Regulatory Empathy":** Designing distinct UI states for Compliance Refusals shows you understand legal constraints (SEBI RIA rules) over raw AI capabilities.
- **"Metadata Surfacing":** Exposing backend Qdrant filters as frontend sidebar toggles demonstrates deep full-stack product intuition.

---

## 10. Screenshot Strategy
1. **The Hero (Source Verification):** The dual-pane UI. Left side shows an answer about short exposure limits with a clicked `[Source 1]` pill. Right side shows the Evidence Explorer displaying the SEBI Circular chunk.
2. **The Analyst (Data Grid):** The chat window dynamically rendering a beautiful comparison table between Tata Titanium and Quant qSIF based on exit loads.
3. **The Compliance Guard (Refusal State):** A beautifully styled amber/warning response block gracefully refusing the question *"Which SIF should I buy?"* and pivoting the user.
4. **The Dashboard (Faceted Search):** The left sidebar expanded, showing active filters (AMC: ICICI, Type: KIM) modifying the search context, proving the power of hybrid metadata filtering.

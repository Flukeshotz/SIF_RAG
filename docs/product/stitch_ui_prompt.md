# SIF Copilot — Stitch UI Generation Prompt

*Copy and paste the following prompt directly into Stitch (or any advanced UI generator) to build the frontend for SIF Copilot.*

---

**Role:** You are a Staff Product Designer and Expert React/Next.js Frontend Engineer specializing in institutional fintech applications (think Bloomberg Terminal, Pitchbook, or Perplexity). 

**Task:** Build a high-fidelity, interactive, launch-ready single-page application (SPA) for "SIF Copilot" — an AI-powered, retrieval-augmented generation (RAG) research tool for Indian Specialized Investment Funds (SIFs).

### 1. Architecture & Tech Stack
- **Framework:** Next.js (App Router) or React with Vite.
- **Styling:** Tailwind CSS (use a sleek, modern, dark-mode default palette: slate-900 backgrounds, slate-800 panels, slate-300 text, and electric blue/indigo accents for interactions).
- **Icons:** Lucide React.
- **Components:** Radix UI or shadcn/ui primitives (simulate them if using plain Tailwind).

### 2. Layout & Information Architecture
Do NOT build a generic, centered ChatGPT clone. Use a professional, edge-to-edge **Split-Pane Dashboard** layout.

**A. Left Sidebar (Context & Filters)**
- **Header:** "SIF Copilot" logo + small "v1.0 MVP" badge.
- **Disclaimer Widget:** A persistent, professional warning: *"Educational Purposes Only. Not SEBI-registered Investment Advice."*
- **Corpus Health:** A small metadata block showing "Active Sources: 36 | Chunks Indexed: 2,001 | Status: Certified".
- **Faceted Search Filters:** Checkbox groups representing backend Qdrant metadata:
  - **AMC:** Quant, Tata, SBI, ICICI Pru, Edelweiss.
  - **Document Type:** SEBI Circulars (Tier 1), ISIDs, KIMs, Factsheets.
  
**B. Main Center Pane (The Research Feed)**
- A scrollable feed of the user's conversation with the AI.
- **Input Bar:** Fixed at the bottom. Sleek, multi-line, with a submit button.
- **Message Bubbles:** 
  - User messages: Minimalist, right-aligned or distinct background.
  - AI messages: Left-aligned, rich text formatting.

**C. Right Pane (The Evidence Explorer - CRITICAL)**
- This pane is closed by default. 
- When a user clicks a citation pill (e.g., `[Source 1]`) in the AI's response, this pane slides in or takes up 30% of the screen width on the right.
- **Contents:** Displays the raw metadata of the clicked chunk. 
  - Document Title, AMC Name, Document Type (with a colored badge, e.g., Red for SEBI Circular, Blue for ISID).
  - The exact highlighted text chunk that the LLM used to generate the claim.

### 3. Key UI Components & Interactions

**Citation Pills:**
The AI backend generates citations like `[Source 1]`. Render these as highly clickable, interactive pill components (e.g., small blue badges with the number '1'). Hovering should show a tooltip; clicking opens the Evidence Explorer.

**Markdown Data Grids:**
The backend frequently returns Markdown tables comparing funds. The UI must intercept table data and render it as a beautiful, institutional-grade data grid (sticky headers, striped rows, hover states) rather than a plain HTML table.

**Compliance Refusal States:**
The backend has strict guardrails. When the AI returns a refusal (e.g., "I cannot provide personalized investment recommendations..."), render this specific message block with a distinct visual state — an amber or warning border, a shield icon, and distinct typography to show that a regulatory guardrail was triggered, not a system error.

### 4. Mock State to Implement
Pre-populate the UI with the following exact mock interaction to demonstrate the layout:

**User Query:** *"What is the minimum investment for SIFs and what is the maximum unhedged short exposure allowed?"*

**AI Response (Rendered with citation pills):**
*"According to the SEBI framework, the minimum investment required for Specialized Investment Funds (SIFs) is ₹10 Lakh per investor, aggregated at the PAN level. `[Source 1]` Furthermore, SIFs are subject to strict derivative constraints, with the maximum unhedged short exposure capped at 25% of the fund's Net Asset Value (NAV). `[Source 2]`"*

**Evidence Explorer State (Active on Source 2):**
- **Badge:** `SEBI CIRCULAR (Tier 1)`
- **Title:** SEBI SIF Regulatory Framework 2025
- **Publisher:** SEBI
- **Chunk Text:** *"To mitigate systemic risk and restrict leverage, the total unhedged short exposure in a Specialized Investment Fund shall not exceed 25% of the Net Asset Value (NAV) of the scheme at any point in time."*

### 5. Aesthetic Guidelines
- **Vibe:** Trustworthy, precise, institutional, dense but readable.
- **Colors:** Deep navy/slate for backgrounds (`bg-slate-950`). Cards and panes (`bg-slate-900`). Borders (`border-slate-800`). Primary accents (`text-blue-400`, `bg-blue-600/20`).
- **Typography:** Inter or standard sans-serif. Use tight leading and tracking suitable for financial dashboards.

*Execute this prompt and generate the complete, interactive React application.*

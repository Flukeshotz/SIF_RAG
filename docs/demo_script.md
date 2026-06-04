# SIF Copilot — Demo Script

## Preparation
1. Start Backend: `python -m api.main`
2. Start Frontend: `npm run dev`
3. Clear `localStorage` in browser dev tools to reset the Product Tour.
4. Ensure "Presentation Mode" toggle is **ON** (top right corner).

---

## 1. The Hook (0:00 - 0:30)
*Screen: The 4-step Product Tour modal is visible.*

**Speaker:** "Welcome to SIF Copilot. Financial analysts spend hours digging through SEBI circulars and 100-page fund documents. We built an AI workspace that does it instantly—with zero hallucination."

*Click through the tour, highlighting the concept of Verifiable Citations.*

---

## 2. The Wow Moment (0:30 - 1:30)
*Screen: The Research Desk empty state.*

**Speaker:** "We’ve indexed over 2,000 authoritative documents. Let’s ask a hard regulatory question."

*Click the suggested query: "What is the minimum investment for SIFs?"*

**Speaker:** "Notice the phased loading state—it’s actively searching our vector database, Qdrant, retrieving chunks, and synthesizing an answer using Llama 3.1 on Groq LPUs."

*The answer renders.*

**Speaker:** "Here’s the magic. Most LLMs just give you text. SIF Copilot gives you proof."

*Hover over `[Source 1]`.*

**Speaker:** "Without even clicking, I can see this came from a SEBI Circular on Page 42 with a 98% vector match."

*Click `[Source 1]` to slide open the Evidence Explorer.*

**Speaker:** "Clicking it pulls the exact immutable text directly from the database. Total transparency."

---

## 3. The Architecture (1:30 - 2:00)
*Click the 'Architecture Docs' tab.*

**Speaker:** "For the engineers in the room, this isn't just a wrapper. We built a 'Hybrid Imperative' pipeline."

*Click through the interactive pipeline steps.*

**Speaker:** "We scrape PDFs, perform OCR, chunk the data contextually while preserving tables, generate embeddings, and store them in Qdrant. The LLM is strictly constrained to only answer using this retrieved context."

---

## 4. Analytics & Scale (2:00 - 2:30)
*Click the 'Scheduler' tab.*

**Speaker:** "To keep the data fresh, we have an automated ingestion pipeline running nightly to fetch new circulars."

*Click the 'Insights' tab.*

**Speaker:** "And as Product Managers, we track everything. The Insights dashboard logs every query, allowing us to monitor latency and see exactly what regulations our users are struggling with."

---

## 5. The Close (2:30 - 2:45)
**Speaker:** "SIF Copilot is an end-to-end, institutional-grade AI product built for trust, scale, and performance. Thank you."

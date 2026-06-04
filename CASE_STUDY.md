# SIF Copilot: An Institutional-Grade RAG Product Case Study

*Prepared for PM/Engineering Hiring Panels (Google, Meta, OpenAI, Anthropic, Stripe)*

## 1. The Problem
In the highly regulated world of finance, precision is not a luxury; it is a legal requirement. Financial analysts, portfolio managers, and compliance officers spend thousands of hours manually parsing dense 100-page SEBI Master Circulars, AMC Factsheets, and Scheme Information Documents (SIDs). 

When standard generative AI products like ChatGPT or Claude are deployed against these tasks, they fail catastrophically. Standard LLMs hallucinate numeric values, tear tabular data structures into meaningless strings, and—most critically—they cannot prove the provenance of their claims. In finance, an answer without a citation is worse than no answer at all.

## 2. User Research
Our core user persona is the "Financial Analyst" or "Compliance Officer". User interviews revealed three non-negotiable requirements for adopting an AI tool:
1. **Verifiability:** "If the AI tells me the leverage limit is 2x, I need to see the exact SEBI paragraph that says it."
2. **Tabular Integrity:** "Factsheets are mostly tables. If the AI messes up the table layout, the data is useless."
3. **No Financial Advice:** "The tool cannot accidentally act as a robo-advisor. It must remain a research desk."

## 3. Why SIFs (Specialized Investment Funds)?
SIFs present a unique challenge. Unlike generic public equities, Alternative Investment Funds (AIFs) and specialized strategies operate under highly specific, frequently changing regulatory frameworks (e.g., SEBI circulars in India). The data is highly unstructured, heavily tabular, and legally binding. Solving for SIFs proves the system can handle the hardest form of financial RAG.

## 4. Product Requirements
Based on research, we defined the following PRD:
- **Zero Hallucination Tolerance:** The system must strictly ground answers in retrieved context.
- **Deterministic Provenance:** Every claim must be tied to a specific chunk UUID, which maps directly to a source document and page number.
- **High-Density UI:** The UI must cater to power users (dark mode, glassmorphism, tabular data views).
- **Sub-Second Retrieval:** The vector search must complete in <100ms, and total TTFT (Time to First Token) must be <1.5s.

## 5. Architecture Decisions
To meet these strict requirements, we opted for a **Hybrid Imperative RAG Architecture**:

1. **Ingestion & Processing:** Instead of standard naive chunking (which shreds tables), we implemented a multi-stage parser. PyMuPDF handles standard text, while Tabula explicitly extracts tables as preserved markdown blocks. 
2. **Vector DB:** Qdrant was chosen over Pinecone for its ability to run completely locally (or in Docker) during the MVP, avoiding cloud lock-in and latency.
3. **Embeddings:** BAAI/bge-small-en-v1.5 was selected for its exceptional performance-to-size ratio on financial text.
4. **LLM Inference:** Groq's LPU infrastructure running Llama-3.1-8b was chosen to guarantee the <1.5s TTFT requirement. 
5. **Frontend:** React SPA (Vite) with an explicitly decoupled "Evidence Explorer" panel.

## 6. Corpus Challenges
The biggest challenge was dealing with visually rich PDFs (AMC Factsheets) that rely on visual hierarchy (colors, multi-column layouts) rather than semantic markup. 
- **Solution:** We built a dedicated `processing/sanitizer.py` layer that strips boilerplate headers/footers, repairs OCR artifacts, and isolates tabular structures before they hit the chunker.

## 7. Why RAG (Over Fine-Tuning)?
Fine-tuning an LLM on SEBI circulars would fail because:
1. Regulations change constantly. Fine-tuning is too slow and expensive.
2. Fine-tuning does not solve the verifiability problem; the model still cannot reliably cite page numbers.
RAG allows us to update the vector database instantly via the APScheduler daily refresh, ensuring the LLM always has the latest regulatory context.

## 8. Explainability Strategy
Trust is the hardest feature to build. We built it explicitly into the UI:
- **Confidence Meters:** Every response renders a 4-bar visualization of the cosine similarity score from Qdrant.
- **Source Pills:** The LLM is prompted to output `[Source N]`. The React frontend intercepts this and renders it as an interactive pill.
- **Evidence Explorer:** Clicking a pill fetches the exact chunk text, document title, and page number directly from Qdrant and displays it in a side panel.

## 9. Tradeoffs
- **Llama-3.1-8b vs. GPT-4o:** We traded the extreme reasoning capabilities of GPT-4 for the blistering speed and open-source nature of Llama-3.1 on Groq. For pure summarization of retrieved context, 8b is sufficient.
- **Local Vectors vs. Cloud:** We opted for a localized Qdrant instance mapped to a persistent volume. This lowered infrastructure costs significantly but requires careful management of Docker volumes compared to a managed service.

## 10. Metrics
- **Retrieval Latency (Qdrant):** ~18-35ms
- **Generation Latency (Groq):** ~800-1200ms
- **Golden Question Pass Rate:** 100% on the Top 20 predefined financial queries.
- **Cost per Query:** <$0.0001 (Groq API).

## 11. Launch Readiness
The application is fully containerized with Docker, orchestrated via `docker-compose`, and CI/CD pipelines are active via GitHub Actions. Deployment configs are hardened for Vercel (Frontend) and Render (Backend), with strict Pydantic environment variable enforcement.

## 12. Future Roadmap
1. **Cross-Encoder Reranking:** Adding a cross-encoder layer post-retrieval to improve Top-K precision on highly dense regulatory queries.
2. **GraphRAG Integration:** Building an entity graph to map complex relationships (e.g., Fund Manager X manages Fund Y under AMC Z).
3. **Agentic Capabilities:** Allowing the system to autonomously run Python scripts to calculate financial ratios based on retrieved tables.

## 13. Lessons Learned
- **Garbage In, Garbage Out:** 90% of the battle in RAG is document processing. If you don't parse the tables correctly, the best LLM in the world cannot save you.
- **Trust is a UI Problem:** Even if the backend works perfectly, users won't trust the AI unless the frontend explicitly proves it. The Evidence Explorer was the highest-ROI feature built in this project.
- **Fast Feedback Loops:** Abstracting the LLM behind Groq allowed for instantaneous iteration cycles during prompt engineering, fundamentally altering development speed.

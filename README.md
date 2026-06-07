<div align="center">
  <img src="https://via.placeholder.com/150/020617/ADC6FF?text=SIF" alt="SIF Copilot Logo" width="120" />
  <h1>SIF Copilot</h1>
  <p><strong>Institutional-Grade AI Research Desk for Specialized Investment Funds</strong></p>

  <p>
    <a href="https://your-vercel-url.vercel.app"><img src="https://img.shields.io/badge/Live_Demo-Available-success?style=for-the-badge" alt="Live Demo" /></a><br/>
    <em>(Currently optimized for Desktop only)</em>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-Backend-green.svg" alt="FastAPI" />
    <img src="https://img.shields.io/badge/React-Frontend-blue.svg" alt="React" />
    <img src="https://img.shields.io/badge/Qdrant-VectorDB-red.svg" alt="Qdrant" />
    <img src="https://img.shields.io/badge/RAG-Enabled-purple.svg" alt="RAG" />
    <img src="https://img.shields.io/badge/Groq-LPU_Inference-F56565.svg" alt="Groq" />
  </p>
</div>

---

## 📖 The Problem

Financial analysts spend hours navigating dense 100-page SEBI circulars, AMC factsheets, and Scheme Information Documents to verify compliance limits, compare funds, or check regulatory changes. Standard ChatGPT wrappers fail in finance because they hallucinate numbers and cannot prove their claims.

## 💡 The Solution

**SIF Copilot** is a high-performance, hallucination-free Retrieval-Augmented Generation (RAG) workspace designed specifically for India's new Specialized Investment Funds (SIF) framework.

- 🕵️‍♂️ **100% Verifiable Citations**: Every claim points to a specific document, page number, and paragraph via the sliding Evidence Explorer.
- ⚡ **Sub-second Retrieval**: Powered by Groq LPUs and local Qdrant Vector search for <1.5s total generation latency.
- 📊 **Dynamic Trust Metrics**: Instantly view the underlying chunk count, search latency, and cosine-similarity confidence score for every AI response.
- 🎓 **Strict Compliance Guardrails**: Prompt engineering strictly prohibits the model from offering financial advice.

## 📸 Product Tour

### Market Explorer
![Market Explorer](docs/screenshots/market_explorer.png)
*A zero-LLM deterministic routing interface that instantly queries the internal JSON registry for fund discovery.*

### Evidence Explorer & Citations
![Evidence Explorer](docs/screenshots/evidence_explorer.png)
*Side-by-side RAG answer and source document verification. Users can trace every claim back to the exact paragraph in a SEBI circular or ISID.*

## 🏗️ Architecture

SIF Copilot uses a **Hybrid Imperative** architecture. Qualitative text is processed normally, but quantitative tables are extracted and preserved as atomic units to prevent data tearing. It relies on deterministic routing before falling back to the LLM.

```mermaid
graph TD
    %% Define Styles
    classDef source fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#e2e8f0;
    classDef db fill:#1e1b4b,stroke:#8b5cf6,stroke-width:2px,color:#e2e8f0;
    classDef llm fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#e2e8f0;
    classDef output fill:#020617,stroke:#f59e0b,stroke-width:2px,color:#f59e0b;

    UserQuery("User Query"):::source

    %% Routing
    Router{"Query Router\n(Deterministic, <10ms)"}
    
    UserQuery --> Router

    %% Paths
    Router -- "'Show all SIFs'\n(Market Discovery)" --> Registry[("Registry JSON\n(Instant)")]:::db
    Router -- "'Compare A vs B'\n(Comparison)" --> Registry
    Router -- "'Should I invest?'\n(Advisory)" --> Refusal("Compliance Refusal"):::output
    Router -- "'Explain exit load'\n(Regulatory)" --> Qdrant[("Qdrant RAG\n(Semantic Search)")]:::db

    %% RAG Path
    Qdrant --> Groq("Groq LLM (Llama 3.1)"):::llm
    Groq --> FinalAnswer("Cited Answer +\nEvidence Panel"):::output
    Registry --> FinalAnswer
```

## 🧠 Key PM Decisions

- **Deterministic Routing over Pure LLM**: By parsing intents heuristically *before* hitting the LLM, the app answers "Show me all funds" in <10ms by querying a JSON registry. This drastically reduces token costs, eliminates hallucination for structured data, and provides a snappier UX.
- **Source Authority Ranking**: The retrieval engine weights official SEBI regulatory documents higher than marketing factsheets. This prevents the LLM from prioritizing sales copy over legal realities when answering questions about risk bands or exit loads.
- **Aggressive Sanitization**: 163-page factsheets contained massive amounts of historical performance data that overwhelmed the semantic search space. The ingestion pipeline explicitly strips "Performance" and "Historical NAV" sections to guarantee high-precision retrieval on core compliance questions.

## 💻 Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 18, Vite, TailwindCSS | High-density, Bloomberg-style UI |
| **Backend** | Python, FastAPI, Pydantic | Asynchronous API layer |
| **Vector DB** | Qdrant | Local semantic search |
| **Embeddings** | BAAI/bge-small-en-v1.5 | Fast, compact document vectorization |
| **Inference** | Groq Llama-3.1-8b-instant | Ultra-low latency generation |
| **Ingestion** | PyMuPDF, pdfplumber, OCRmyPDF | Table-preserving PDF extraction |

## 🚀 Local Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq API Key

### 1. Backend Setup
```bash
git clone https://github.com/Flukeshotz/SIF_RAG.git
cd SIF_RAG
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.development .env
# Edit .env and add your GROQ_API_KEY

# Start FastAPI server
python -m api.main
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:5173` in your browser.

## 🐳 Docker Deployment
```bash
docker-compose up --build -d
```

## 🗺️ Roadmap
- [ ] Connect Airflow for nightly SEBI RSS feeds.
- [ ] Add Cross-Encoder Reranking for dense regulatory queries.
- [ ] Implement GraphRAG for tracking complex entity relationships (Fund Managers to AMCs).

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

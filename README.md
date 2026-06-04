<div align="center">
  <img src="https://via.placeholder.com/150/020617/ADC6FF?text=SIF" alt="SIF Copilot Logo" width="120" />
  <h1>SIF Copilot</h1>
  <p><strong>Institutional-Grade AI Research Desk for Specialized Investment Funds</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-0.103+-009688.svg" alt="FastAPI" />
    <img src="https://img.shields.io/badge/React-18+-61DAFB.svg" alt="React" />
    <img src="https://img.shields.io/badge/Qdrant-Vector_DB-8B5CF6.svg" alt="Qdrant" />
    <img src="https://img.shields.io/badge/Groq-LPU_Inference-F56565.svg" alt="Groq" />
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License" />
  </p>
</div>

---

## 📖 Product Overview

Financial analysts spend hours navigating dense 100-page SEBI circulars, AMC factsheets, and Scheme Information Documents to verify compliance limits, compare funds, or check regulatory changes. 

**SIF Copilot** is a high-performance, hallucination-free Retrieval-Augmented Generation (RAG) workspace. It indexes over 2,000 verifiable documents and uses Llama-3.1 on Groq LPUs to synthesize instant, source-backed answers.

### Why this exists?
Standard ChatGPT wrappers fail in finance because they hallucinate numbers and cannot prove their claims. SIF Copilot implements a "Hybrid Imperative" architecture that preserves exact table structures, sanitizes noise, and forces the LLM to output verifiable `[Source N]` citations mapped to a 4-bar confidence meter.

## ✨ Features

- 🕵️‍♂️ **100% Verifiable Citations**: Every claim points to a specific document, page number, and paragraph via the sliding **Evidence Explorer**.
- ⚡ **Sub-second Retrieval**: Powered by Groq LPUs and local Qdrant Vector search for <1.5s total generation latency.
- 📊 **Dynamic Trust Metrics**: Instantly view the underlying chunk count, search latency, and cosine-similarity confidence score for every AI response.
- 🎓 **Strict Compliance Guardrails**: Prompt engineering strictly prohibits the model from offering financial advice.
- 🎨 **Bloomberg-Meets-Perplexity UI**: A high-density, dark-mode glassmorphism interface built for power users.
- 🚀 **Presentation Mode**: Built-in Demo Mode and Presentation Mode for flawless, offline-capable live demos.

## 🏗️ Architecture

SIF Copilot splits the pipeline into asynchronous ingestion and real-time retrieval. 

*View the full [Architecture Diagram](docs/architecture_diagram.md).*

## 💻 Tech Stack

- **Frontend**: React 18, Vite, TailwindCSS (Vanilla CSS for aesthetic tokens).
- **Backend**: Python, FastAPI, Pydantic.
- **AI/ML**: BAAI/bge-small-en-v1.5 (Embeddings), Groq Llama-3.1-8b-instant (Inference).
- **Database**: Qdrant (Vector Store).
- **Deployment**: Vercel (Frontend), Render/Docker (Backend).

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

## 👨‍💻 Author
Designed and Engineered as an end-to-end PM & AI showcase.

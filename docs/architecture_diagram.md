# Architecture Diagram

The SIF Copilot relies on a "Hybrid Imperative" Retrieval-Augmented Generation (RAG) architecture. Qualitative text is processed normally, but quantitative tables are extracted and preserved as atomic units to prevent data tearing.

## Data Pipeline

```mermaid
graph TD
    %% Define Styles
    classDef source fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#e2e8f0;
    classDef process fill:#1e293b,stroke:#64748b,stroke-width:1px,color:#e2e8f0;
    classDef db fill:#1e1b4b,stroke:#8b5cf6,stroke-width:2px,color:#e2e8f0;
    classDef llm fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#e2e8f0;
    classDef output fill:#020617,stroke:#f59e0b,stroke-width:2px,color:#f59e0b;

    %% Data Acquisition
    subgraph "1. Document Acquisition"
        A1("SEBI Master Circulars"):::source
        A2("AMC Factsheets"):::source
        A3("ISID / KIMs"):::source
    end

    %% Processing
    subgraph "2. Processing & OCR"
        B1("PyMuPDF Parsing"):::process
        B2("Tabula Table Extraction"):::process
        B3("Noise Sanitization"):::process
    end

    %% Chunking & Embedding
    subgraph "3. Vectorization"
        C1("Contextual Chunking"):::process
        C2("Metadata Enrichment"):::process
        C3("BAAI/bge-small-en-v1.5 Embedding"):::process
    end

    %% Storage
    subgraph "4. Storage"
        D1[("Qdrant Vector DB")]:::db
    end

    %% Retrieval & Generation
    subgraph "5. Runtime (User Query)"
        E1("User Query"):::source
        E2("Query Embedding"):::process
        E3("Cosine Similarity Search"):::db
        E4("Context Assembly"):::process
        E5("Groq (Llama-3.1-8b)"):::llm
    end

    %% Output
    F1("Explainable Answer with Confidence Scores"):::output

    %% Flow
    A1 --> B1
    A2 --> B1
    A3 --> B1
    B1 --> B2
    B2 --> B3
    B3 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> D1

    E1 --> E2
    E2 --> E3
    E3 -- "Fetch Top 5 Chunks" --> D1
    D1 -- "Return Chunks & Metadata" --> E4
    E4 --> E5
    E5 --> F1
```

# SIF Copilot — API Reference

## Base URL
`http://localhost:8000`

---

## 1. POST `/query`
Submit a financial research query to the RAG pipeline.

**Request Body:**
```json
{
  "query": "What is the maximum unhedged short exposure for a SIF?"
}
```

**Response (200 OK):**
```json
{
  "answer": "The maximum unhedged short exposure for a Specialized Investment Fund (SIF) is capped at 25% of the Net Asset Value (NAV)...",
  "citations": [
    {
      "chunk_id": "a1b2c3d4-...",
      "document_id": "SEBI-SIF-Framework-2023",
      "document_type": "SEBI Circular",
      "organization": "SEBI",
      "priority_tier": 1
    }
  ]
}
```

---

## 2. GET `/sources/{source_id}`
Retrieve the exact indexed chunk and metadata for a given citation ID. Used by the frontend Evidence Explorer.

**Path Parameters:**
- `source_id` (string): The Qdrant point UUID.

**Response (200 OK):**
```json
{
  "id": "a1b2c3d4-...",
  "text": "...maximum unhedged short exposure for a Specialized Investment Fund shall not exceed 25%...",
  "document_title": "SEBI-SIF-Framework-2023",
  "document_type": "SEBI Circular",
  "organization": "SEBI",
  "page_number": 42,
  "priority_tier": 1
}
```

---

## 3. GET `/metrics`
Fetch real-time health and scale metrics from the backend (Qdrant).

**Response (200 OK):**
```json
{
  "chunk_count": 2001,
  "vector_health": "green",
  "indexed_documents": 2001,
  "last_refresh_timestamp": 1698765432.1
}
```

---

## 4. GET `/health`
Basic system heartbeat.

**Response (200 OK):**
```json
{
  "status": "ok",
  "timestamp": 1698765432.1
}
```

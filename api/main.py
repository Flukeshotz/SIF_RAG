from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import time
import json
from datetime import datetime, timezone

from retrieval.engine import answer_query_structured
from db.qdrant_connection import get_client

app = FastAPI(title="SIF Copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class CitationModel(BaseModel):
    chunk_id: str
    document_title: str
    document_type: str
    organization: str
    page_number: Optional[int] = None
    confidence: float
    text: Optional[str] = None
    
    model_config = {"extra": "allow"}

class RetrievalMetrics(BaseModel):
    chunks_retrieved: int
    search_time_ms: int
    embedding_model: str
    llm: str

class QueryResponse(BaseModel):
    answer: str
    citations: List[CitationModel]
    retrieval: RetrievalMetrics

ANALYTICS_FILE = "data/analytics.jsonl"

def log_analytics(query: str, latency: int, sources_count: int):
    os.makedirs("data", exist_ok=True)
    with open(ANALYTICS_FILE, "a") as f:
        log_entry = {
            "query": query,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "latency": latency,
            "sources_used": sources_count
        }
        f.write(json.dumps(log_entry) + "\n")

@app.post("/query", response_model=QueryResponse)
def query_endpoint(req: QueryRequest):
    try:
        result = answer_query_structured(req.query)
        
        # Log analytics
        log_analytics(
            query=req.query,
            latency=result.get("retrieval", {}).get("search_time_ms", 0),
            sources_count=result.get("retrieval", {}).get("chunks_retrieved", 0)
        )
        
        return result
    except Exception as e:
        print(f"Error querying: {e}")
        raise HTTPException(status_code=500, detail="Failed to process query.")

@app.get("/health")
def health_endpoint():
    return {"status": "ok", "timestamp": time.time()}

@app.get("/metrics")
def metrics_endpoint():
    try:
        client = get_client()
        collection_info = client.get_collection(collection_name="sif_documents")
        
        return {
            "chunk_count": collection_info.points_count,
            "vector_health": collection_info.status.value if hasattr(collection_info, 'status') else "green",
            "indexed_documents": collection_info.points_count,
            "last_refresh_timestamp": time.time()
        }
    except Exception as e:
        print(f"Metrics error: {e}")
        return {
            "chunk_count": "Unknown",
            "vector_health": "red",
            "indexed_documents": "Unknown",
            "last_refresh_timestamp": "Unknown"
        }

@app.get("/scheduler/status")
def scheduler_status_endpoint():
    # Mocking actual scheduler values since we don't have Airflow/Cron hooked up
    return {
        "last_refresh": "2026-06-04T02:00:00Z",
        "next_refresh": "2026-06-05T02:00:00Z",
        "status": "healthy",
        "documents_processed": 14,
        "chunks_generated": 2001
    }

@app.get("/analytics")
def analytics_endpoint():
    if not os.path.exists(ANALYTICS_FILE):
        return {"total_queries": 0, "average_latency": 0, "recent_queries": []}
    
    total_latency = 0
    total_queries = 0
    queries = []
    
    with open(ANALYTICS_FILE, "r") as f:
        for line in f:
            if line.strip():
                try:
                    entry = json.loads(line)
                    queries.append(entry)
                    total_latency += entry.get("latency", 0)
                    total_queries += 1
                except:
                    pass
                    
    avg_latency = total_latency / total_queries if total_queries > 0 else 0
    
    # Sort and get top queries by recency or frequency
    # For MVP, just return the raw stats and last 10 queries
    return {
        "total_queries": total_queries,
        "average_latency": round(avg_latency, 2),
        "recent_queries": list(reversed(queries))[-10:] # Last 10
    }

@app.get("/sources/{source_id}")
def get_source_endpoint(source_id: str):
    try:
        client = get_client()
        result = client.retrieve(collection_name="sif_documents", ids=[source_id])
        if not result:
            raise HTTPException(status_code=404, detail="Source not found")
        
        point = result[0]
        payload = point.payload or {}
        
        return {
            "id": source_id,
            "text": payload.get("text", "No content available"),
            "document_title": payload.get("document_id", "Unknown Document"),
            "document_type": payload.get("document_type", "Unknown Type"),
            "organization": payload.get("organization", "Unknown AMC"),
            "page_number": payload.get("page_number", "N/A"),
            "priority_tier": payload.get("priority_tier", "Unknown")
        }
    except Exception as e:
        print(f"Source fetch error: {e}")
        raise HTTPException(status_code=500, detail="Error fetching source")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)

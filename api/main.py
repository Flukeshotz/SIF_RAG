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
from core.config import settings
from jobs.scheduler import start_scheduler, get_scheduler_status

# Explicit startup validation logs
print(f"Starting SIF Copilot API in {settings.ENVIRONMENT} mode...")
if not settings.GROQ_API_KEY or len(settings.GROQ_API_KEY) < 10:
    print("CRITICAL ERROR: GROQ_API_KEY is missing or invalid.")
    raise ValueError("GROQ_API_KEY environment variable is required.")
print("Configuration validated successfully.")

app = FastAPI(title="SIF Copilot API")

@app.on_event("startup")
def startup_event():
    # Generate initial NAV data for the demo ticker
    from jobs.nav_updater import update_navs
    update_navs()
    
    start_scheduler()
    # Auto-ingest if Qdrant collection is empty (first boot on fresh disk)
    try:
        from db.qdrant_connection import get_client
        from scripts.ingest_qdrant import ingest_vectors
        client = get_client()
        if not client.collection_exists("sif_documents"):
            print("Qdrant collection not found — running initial ingestion from pre-computed embeddings...")
            ingest_vectors()
            print("Initial ingestion complete.")
        else:
            print("Qdrant collection exists, skipping ingestion.")
    except Exception as e:
        print(f"Startup ingestion error (non-fatal): {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.ALLOWED_ORIGINS == "*" else [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")],
    allow_credentials=False,
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
    query_type: Optional[str] = None
    structured_data: Optional[Any] = None

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

@app.get("/admin/ingest")
def admin_ingest_endpoint():
    """Manually trigger Qdrant ingestion from pre-computed embeddings."""
    import traceback
    logs = []
    try:
        from db.qdrant_connection import get_client, init_collection
        from pathlib import Path
        import json, uuid
        from qdrant_client.models import PointStruct

        logs.append("Initializing Qdrant client...")
        client = get_client()
        logs.append(f"Client initialized. QDRANT_PATH={settings.QDRANT_PATH}")

        collection_exists = client.collection_exists("sif_documents")
        logs.append(f"Collection exists: {collection_exists}")

        logs.append("Running init_collection...")
        init_collection(client, "sif_documents")
        logs.append("Collection initialized.")

        embeddings_dir = Path("data/processed/embeddings")
        files = list(embeddings_dir.glob("*.json"))
        logs.append(f"Found {len(files)} embedding files: {[f.name for f in files]}")

        total_uploaded = 0
        failures = 0

        for fp in files:
            with open(fp, "r") as f:
                chunks = json.load(f)
            logs.append(f"Processing {fp.name}: {len(chunks)} chunks")

            points = []
            for c in chunks:
                try:
                    meta = c.get("metadata", {})
                    payload = {
                        "chunk_id": c.get("chunk_id"),
                        "document_id": c.get("document_id"),
                        "document_type": c.get("document_type"),
                        "organization": c.get("organization"),
                        "fund_name": c.get("fund_name") or meta.get("fund_name"),
                        "strategy_type": c.get("strategy_type") or meta.get("strategy"),
                        "priority_tier": c.get("priority_tier") or meta.get("priority_tier"),
                        "chunk_type": c.get("chunk_type"),
                        "page_number": c.get("page_number"),
                        "text": c.get("text")
                    }
                    point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, payload["chunk_id"]))
                    points.append(PointStruct(id=point_id, vector=c["vector"], payload=payload))
                except Exception as e:
                    failures += 1
                    logs.append(f"Point error: {e}")

            if points:
                client.upload_points(collection_name="sif_documents", points=points, batch_size=100)
                total_uploaded += len(points)
                logs.append(f"Uploaded {len(points)} points from {fp.name}")

        logs.append(f"Ingestion complete. Total uploaded: {total_uploaded}, Failures: {failures}")
        return {"status": "success", "total_uploaded": total_uploaded, "failures": failures, "logs": logs}

    except Exception as e:
        logs.append(f"FATAL ERROR: {e}")
        logs.append(traceback.format_exc())
        return {"status": "error", "error": str(e), "logs": logs}

@app.get("/admin/system")
def admin_system_endpoint():
    try:
        registry_data = get_registry_data()
        registry_size = len(registry_data)
        
        metrics = metrics_endpoint()
        scheduler_status = get_scheduler_status()
        
        return {
            "registry_size": registry_size,
            "chunk_count": metrics.get("chunk_count", "Unknown"),
            "vector_count": metrics.get("chunk_count", "Unknown"), # Usually 1 vector per chunk
            "scheduler_status": scheduler_status.get("status", "Unknown"),
            "last_refresh_time": scheduler_status.get("last_run", "Unknown"),
            "api_latency_ms": 12 # Mocked average for demo
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/scheduler/status")
def scheduler_status_endpoint():
    return get_scheduler_status()

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

# --- MARKET ANALYTICS API ---

from pydantic import BaseModel

class ViewFundRequest(BaseModel):
    fund_id: str
    amc: str
    strategy: str

def load_market_analytics():
    if os.path.exists("data/market_analytics.json"):
        with open("data/market_analytics.json", "r") as f:
            try:
                return json.load(f)
            except:
                pass
    return {"funds": {}, "amcs": {}, "strategies": {}}

def save_market_analytics(data):
    os.makedirs("data", exist_ok=True)
    with open("data/market_analytics.json", "w") as f:
        json.dump(data, f, indent=2)

@app.post("/analytics/view_fund")
def record_fund_view(req: ViewFundRequest):
    data = load_market_analytics()
    
    data["funds"][req.fund_id] = data["funds"].get(req.fund_id, 0) + 1
    data["amcs"][req.amc] = data["amcs"].get(req.amc, 0) + 1
    data["strategies"][req.strategy] = data["strategies"].get(req.strategy, 0) + 1
    
    save_market_analytics(data)
    return {"status": "success"}

@app.get("/analytics/market")
def get_market_analytics():
    data = load_market_analytics()
    
    # Sort and return top 5
    top_funds = sorted(data["funds"].items(), key=lambda x: x[1], reverse=True)[:5]
    top_amcs = sorted(data["amcs"].items(), key=lambda x: x[1], reverse=True)[:5]
    top_strategies = sorted(data["strategies"].items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "most_viewed_funds": [{"id": k, "views": v} for k, v in top_funds],
        "most_viewed_amcs": [{"amc": k, "views": v} for k, v in top_amcs],
        "most_viewed_strategies": [{"strategy": k, "views": v} for k, v in top_strategies]
    }

# ------------------------------
def get_registry_data():
    if os.path.exists("data/sif_registry.json"):
        with open("data/sif_registry.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

@app.get("/funds")
def get_all_funds():
    return get_registry_data()

@app.get("/funds/count")
def get_funds_count():
    funds = get_registry_data()
    return {"count": len(funds)}

@app.get("/funds/strategies")
def get_funds_strategies():
    funds = get_registry_data()
    strategies = {}
    for f in funds:
        st = f.get("strategy", "Unknown")
        strategies[st] = strategies.get(st, 0) + 1
    return strategies

@app.get("/funds/categories")
def get_funds_categories():
    funds = get_registry_data()
    categories = {}
    for f in funds:
        cat = f.get("category", "Unknown")
        categories[cat] = categories.get(cat, 0) + 1
    return categories

@app.get("/funds/navs")
def get_funds_navs():
    if os.path.exists("data/nav_data.json"):
        with open("data/nav_data.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

@app.get("/funds/{amc}")
def get_funds_by_amc(amc: str):
    funds = get_registry_data()
    # Case insensitive
    filtered = [f for f in funds if f.get("amc", "").lower() == amc.lower()]
    return filtered
# ------------------------------

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

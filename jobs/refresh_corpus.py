import asyncio
import time
import json
import os
from datetime import datetime, timezone
from ingestion.run import run_ingestion
from chunking.run import run_chunking
from embeddings.generator import generate_embeddings
from scripts.ingest_qdrant import ingest_vectors
from db.qdrant_connection import get_client

PIPELINE_VERSION = "v2.0"
HISTORY_FILE = "data/history/pipeline_history.jsonl"
STATUS_FILE = "data/pipeline_status.json"
LOCK_FILE = "data/pipeline.lock"
MAX_HISTORY_RUNS = 1000

def trigger_refresh():
    """Synchronous wrapper to trigger the async pipeline orchestrator."""
    if os.path.exists(LOCK_FILE):
        print("Pipeline is already running. Skipping trigger.")
        return {"status": "already_running"}
        
    try:
        # Create an empty lock file
        open(LOCK_FILE, 'w').close()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(orchestrate_pipeline())
        loop.close()
        return result
    except Exception as e:
        print(f"Error during corpus refresh trigger: {e}")
        return {"status": "error", "error": str(e)}
    finally:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)

def update_live_status(run_id, state, current_stage=None, start_time=None, prev_docs=0, prev_chunks=0):
    """Updates the status file in real-time while pipeline runs."""
    elapsed = round(time.time() - start_time, 2) if start_time else 0
    status_doc = {
        "pipeline_version": PIPELINE_VERSION,
        "run_id": run_id,
        "state": state,
        "current_stage": current_stage,
        "elapsed_seconds": elapsed,
        "corpus_growth": {
            "total_documents": prev_docs,
            "previous_documents": prev_docs,
            "growth_documents": 0,
            "total_chunks": prev_chunks,
            "growth_chunks": 0
        }
    }
    with open(STATUS_FILE, "w") as f:
        json.dump(status_doc, f, indent=2)

async def orchestrate_pipeline():
    run_id = datetime.now(timezone.utc).isoformat()
    t_start = time.time()
    print(f"--- Starting Pipeline Run {run_id} (Version {PIPELINE_VERSION}) ---")
    
    os.makedirs("data/history", exist_ok=True)
    
    prev_docs = 0
    prev_chunks = 0
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r") as f:
                prev_status = json.load(f)
                prev_docs = prev_status.get("corpus_growth", {}).get("total_documents", 0)
                prev_chunks = prev_status.get("corpus_growth", {}).get("total_chunks", 0)
        except:
            pass

    state = "RUNNING"
    consistency_error = None
    retrieval_health = True
    stages = {}
    total_docs_processed = 0
    new_docs = []
    failed_urls = []
    chunks_generated = 0
    embeddings_created = 0
    vectors_uploaded = 0

    try:
        # 1. Ingestion
        update_live_status(run_id, "RUNNING", "Ingestion", t_start, prev_docs, prev_chunks)
        t0 = time.time()
        docs_processed = await run_ingestion()
        stages["ingestion"] = {"duration_seconds": round(time.time() - t0, 2)}
        
        with open("data/raw/ingestion_report.json", "r") as f:
            ingest_rep = json.load(f)
            total_docs_processed = ingest_rep.get("total_processed", docs_processed)
            new_docs = ingest_rep.get("new_documents", [])
            failed_urls = ingest_rep.get("error_details", [])
            
        # 2. Chunking
        update_live_status(run_id, "RUNNING", "Chunking", t_start, prev_docs, prev_chunks)
        t0 = time.time()
        if new_docs:
            chunks_generated = run_chunking(new_documents=new_docs)
        stages["chunking"] = {"duration_seconds": round(time.time() - t0, 2)}
        
        # 3. Embedding
        update_live_status(run_id, "RUNNING", "Embedding", t_start, prev_docs, prev_chunks)
        t0 = time.time()
        if new_docs:
            embeddings_created = generate_embeddings(new_documents=new_docs)
        stages["embedding"] = {"duration_seconds": round(time.time() - t0, 2)}
        
        # 4. Qdrant Ingestion
        update_live_status(run_id, "RUNNING", "Qdrant Ingestion", t_start, prev_docs, prev_chunks)
        t0 = time.time()
        if new_docs:
            vectors_uploaded = ingest_vectors()
        stages["qdrant"] = {"duration_seconds": round(time.time() - t0, 2)}
        
        state = "SUCCESS"

        # 5. Consistency Validation
        update_live_status(run_id, "RUNNING", "Validation", t_start, prev_docs, prev_chunks)
        try:
            client = get_client()
            collection_info = client.get_collection("sif_documents")
            actual_qdrant_vectors = collection_info.points_count
            expected_vectors = prev_chunks + chunks_generated
            
            if actual_qdrant_vectors < expected_vectors:
                retrieval_health = False
                consistency_error = f"Chunk mismatch. Expected >= {expected_vectors}, found {actual_qdrant_vectors}"
                state = "PARTIAL_SUCCESS"
        except Exception as e:
            retrieval_health = False
            consistency_error = f"Qdrant query failed: {e}"
            state = "PARTIAL_SUCCESS"
            actual_qdrant_vectors = prev_chunks

    except Exception as e:
        state = "FAILED"
        consistency_error = f"Pipeline crashed: {str(e)}"
        actual_qdrant_vectors = prev_chunks

    current_total_docs = prev_docs + len(new_docs)
    current_total_chunks = prev_chunks + chunks_generated
    
    report = {
        "pipeline_version": PIPELINE_VERSION,
        "run_id": run_id,
        "state": state,
        "total_duration_seconds": round(time.time() - t_start, 2),
        "stages": stages,
        "corpus_growth": {
            "total_documents": current_total_docs,
            "previous_documents": prev_docs,
            "growth_documents": len(new_docs),
            "total_chunks": current_total_chunks,
            "growth_chunks": chunks_generated
        },
        "qdrant_validation": {
            "retrieval_health": retrieval_health,
            "expected_vectors": current_total_chunks,
            "actual_qdrant_vectors": actual_qdrant_vectors,
            "consistency_error": consistency_error
        },
        "failed_urls": failed_urls
    }
    
    with open(STATUS_FILE, "w") as f:
        json.dump(report, f, indent=2)
        
    with open(HISTORY_FILE, "a") as f:
        f.write(json.dumps(report) + "\n")
        
    with open(HISTORY_FILE, "r") as f:
        lines = f.readlines()
    if len(lines) > MAX_HISTORY_RUNS:
        with open(HISTORY_FILE, "w") as f:
            f.writelines(lines[-MAX_HISTORY_RUNS:])
            
    print(f"--- Pipeline {run_id} completed: {state} ---")
    return report

if __name__ == "__main__":
    trigger_refresh()

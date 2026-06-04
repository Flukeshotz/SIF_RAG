import asyncio
import logging
import json
from . import registry
from . import downloader
from . import hashing
from . import storage
from . import versioning

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def process_source(source: dict) -> dict:
    """Processes a single source: download, hash, save, version."""
    source_id = source["source_id"]
    url = source.get("pdf_url") or source.get("landing_url")
    
    if not url:
        return {"source_id": source_id, "status": "error", "error": "No URL provided"}
        
    try:
        content, content_type = await downloader.download_file(url)
        content_hash = hashing.generate_hash(content)
        
        is_pdf = "pdf" in content_type.lower() or url.lower().endswith(".pdf")
        
        filepath = storage.save_document(source_id, content, is_pdf, content_hash)
        is_new, metadata = versioning.update_version(source_id, content_hash, filepath)
        
        return {
            "source_id": source_id, 
            "status": "success", 
            "is_new_version": is_new,
            "hash": content_hash
        }
        
    except Exception as e:
        logger.error(f"Failed to process {source_id}: {str(e)}")
        return {"source_id": source_id, "status": "error", "error": str(e)}

async def run_ingestion():
    """Runs the ingestion pipeline for all active sources."""
    sources = registry.get_active_sources()
    logger.info(f"Starting ingestion for {len(sources)} active sources.")
    
    results = []
    # Process sequentially for simplicity and avoiding immediate rate limits
    for source in sources:
        logger.info(f"Processing {source['source_id']}...")
        result = await process_source(source)
        results.append(result)
        
    # Generate summary
    success = [r for r in results if r["status"] == "success"]
    new_versions = [r for r in success if r["is_new_version"]]
    errors = [r for r in results if r["status"] == "error"]
    
    summary = {
        "total_processed": len(results),
        "success": len(success),
        "new_versions": len(new_versions),
        "errors": len(errors),
        "error_details": errors
    }
    
    with open("data/raw/ingestion_report.json", "w") as f:
        json.dump(summary, f, indent=2)
        
    logger.info(f"Ingestion complete. Success: {len(success)}, New Versions: {len(new_versions)}, Errors: {len(errors)}")

if __name__ == "__main__":
    asyncio.run(run_ingestion())

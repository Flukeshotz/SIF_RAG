import json
import os
from pathlib import Path
from typing import List, Dict, Any

from chunking.schema import Chunk
from chunking.regulatory_chunker import RegulatoryChunker
from chunking.isid_chunker import ISIDChunker
from chunking.kim_chunker import KIMChunker
from chunking.factsheet_chunker import FactsheetChunker
from chunking.validator import ChunkValidator

def run_chunking():
    input_dir = Path("data/processed/sanitized")
    output_dir = Path("data/processed/chunks")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not input_dir.exists():
        print(f"Directory {input_dir} does not exist.")
        return

    # Initialize Chunkers
    chunkers = {
        "regulatory": RegulatoryChunker(),
        "isid": ISIDChunker(),
        "kim": KIMChunker(),
        "factsheet": FactsheetChunker()
    }
    
    validator = ChunkValidator()
    
    total_chunks_processed = 0
    all_chunks: List[Chunk] = []

    for file_path in input_dir.glob("*.json"):
        with open(file_path, "r") as f:
            data = json.load(f)
            
        doc_type = data.get("document_type", "Unknown").lower()
        doc_name = data.get("document_id", "").lower()
        
        # Determine chunker
        chunker = None
        if "sebi" in doc_name or "amfi" in doc_name or "circular" in doc_type:
            chunker = chunkers["regulatory"]
        elif "isid" in doc_type or "isid" in doc_name:
            chunker = chunkers["isid"]
        elif "kim" in doc_type or "kim" in doc_name:
            chunker = chunkers["kim"]
        elif "factsheet" in doc_type or "factsheet" in doc_name:
            chunker = chunkers["factsheet"]
        else:
            # Fallback
            chunker = chunkers["isid"]
            
        print(f"Chunking {doc_name} with {chunker.__class__.__name__}...")
        doc_chunks = chunker.chunk(data)
        
        # Save document specific chunks
        chunk_dicts = [c.model_dump() for c in doc_chunks]
        out_path = output_dir / f"{doc_name}_chunks.json"
        
        with open(out_path, "w") as f:
            json.dump(chunk_dicts, f, indent=2)
            
        all_chunks.extend(doc_chunks)
        total_chunks_processed += len(doc_chunks)

    print(f"\nTotal chunks generated: {total_chunks_processed}")
    
    # Run Validator
    print("\nRunning Validator...")
    report = validator.validate(all_chunks)
    
    if report["is_valid"]:
        print("✅ Validation Passed!")
    else:
        print("❌ Validation Failed!")
        for err in report["errors"][:10]:
            print(f"  - {err}")
        if len(report["errors"]) > 10:
            print(f"  ... and {len(report['errors']) - 10} more errors.")
            
    print(f"Metrics: Empty: {report['empty_chunks']}, Oversized: {report['oversized_chunks']}, Duplicate: {report['duplicate_chunks']}, Missing Meta: {report['missing_metadata']}")

if __name__ == "__main__":
    run_chunking()

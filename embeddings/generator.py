import json
from pathlib import Path
from embeddings.model import EmbeddingModel
import numpy as np

from typing import List

def generate_embeddings(new_documents: List[str] = None):
    input_dir = Path("data/processed/chunks")
    output_dir = Path("data/processed/embeddings")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not input_dir.exists():
        print(f"Directory {input_dir} does not exist.")
        return 0

    model = EmbeddingModel()
    
    # We will process document by document
    total_processed = 0
    
    for file_path in input_dir.glob("*_chunks.json"):
        # Extact doc name from filename (e.g. 'doc1_chunks.json' -> 'doc1')
        doc_name = file_path.name.replace('_chunks.json', '').lower()
        
        # Idempotency check
        if new_documents is not None and doc_name not in [d.lower() for d in new_documents]:
            continue
            
        with open(file_path, "r") as f:
            chunks = json.load(f)
            
        if not chunks:
            continue
            
        print(f"Generating embeddings for {file_path.name} ({len(chunks)} chunks)...")
        
        texts = [c["text"] for c in chunks]
        
        # Generate embeddings
        vectors = model.encode_documents(texts)
        
        # Inject vectors back into chunk payloads
        # We convert numpy arrays to lists of floats for JSON serialization
        for i, chunk in enumerate(chunks):
            chunk["vector"] = vectors[i].tolist()
            
        # Save enriched chunks
        out_path = output_dir / file_path.name
        with open(out_path, "w") as f:
            json.dump(chunks, f) # No indent to save space
            
        total_processed += len(chunks)
        
    print(f"\nSuccessfully generated {total_processed} embeddings and saved to {output_dir}")
    return total_processed

if __name__ == "__main__":
    generate_embeddings()

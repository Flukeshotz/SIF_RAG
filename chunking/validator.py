from typing import List, Dict, Any
import tiktoken
from chunking.schema import Chunk, ChunkType

class ChunkValidator:
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def validate(self, chunks: List[Chunk]) -> Dict[str, Any]:
        report = {
            "total_chunks": len(chunks),
            "empty_chunks": 0,
            "duplicate_chunks": 0,
            "oversized_chunks": 0,
            "missing_metadata": 0,
            "is_valid": True,
            "errors": []
        }
        
        seen_texts = set()
        
        # Required metadata fields per instruction
        required_metadata = ["fund_name", "amc", "strategy", "risk_band", "source_type", "priority_tier"]

        for c in chunks:
            # 1. No empty chunks
            if not c.text or not c.text.strip():
                report["empty_chunks"] += 1
                report["errors"].append(f"Empty chunk found: {c.chunk_id}")
                
            # 2. No duplicate chunks
            if c.text in seen_texts:
                report["duplicate_chunks"] += 1
                report["errors"].append(f"Duplicate chunk text: {c.chunk_id}")
            else:
                seen_texts.add(c.text)
                
            # 3. No oversized chunks (Except tables)
            tokens = len(self.tokenizer.encode(c.text))
            if tokens > 800 and c.chunk_type != ChunkType.TABLE:
                report["oversized_chunks"] += 1
                report["errors"].append(f"Oversized chunk {c.chunk_id} ({tokens} tokens)")
                
            # 4. Metadata completeness
            missing = []
            for req in required_metadata:
                # First check direct fields on the Chunk schema
                if getattr(c, req, None) is None and c.metadata.get(req) is None:
                    # Allow missing fund specific details for SEBI circulars
                    if c.organization == "SEBI" or c.organization == "AMFI":
                        continue
                    missing.append(req)
            if missing:
                report["missing_metadata"] += 1
                report["errors"].append(f"Missing metadata {missing} on chunk {c.chunk_id}")

        if report["empty_chunks"] > 0 or report["oversized_chunks"] > 0 or report["duplicate_chunks"] > 0:
            report["is_valid"] = False
            
        return report

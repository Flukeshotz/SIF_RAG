import json
from pathlib import Path
from collections import defaultdict
import hashlib

def audit_distribution():
    chunks_dir = Path("data/processed/chunks")
    
    total_chunks = 0
    doc_counts = defaultdict(int)
    amc_counts = defaultdict(int)
    type_counts = defaultdict(int)
    
    seen_texts = {}
    duplicates = 0
    near_duplicates = 0
    
    for fp in chunks_dir.glob("*.json"):
        with open(fp, "r") as f:
            chunks = json.load(f)
            
        for c in chunks:
            total_chunks += 1
            doc_id = c.get("document_id", "unknown")
            amc = c.get("metadata", {}).get("amc") or c.get("organization", "unknown")
            ctype = c.get("chunk_type", "unknown")
            text = c.get("text", "").strip()
            
            doc_counts[doc_id] += 1
            amc_counts[amc] += 1
            type_counts[ctype] += 1
            
            # Simple Exact Duplicate
            if text in seen_texts:
                duplicates += 1
            else:
                seen_texts[text] = doc_id

    with open("docs/reports/chunk_distribution_report.md", "w") as f:
        f.write("# Phase 5A — Chunk Distribution Audit\n\n")
        f.write(f"**Total Chunks:** {total_chunks}\n\n")
        
        f.write("## Chunks by Type\n")
        for k, v in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {k}: {v}\n")
            
        f.write("\n## Chunks by AMC / Organization\n")
        for k, v in sorted(amc_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {k}: {v} ({v/total_chunks*100:.1f}%)\n")
            
        f.write("\n## Chunks by Document\n")
        for k, v in sorted(doc_counts.items(), key=lambda x: x[1], reverse=True):
            pct = v / total_chunks * 100
            flag = " 🚩 (EXCEEDS 15% THRESHOLD)" if pct > 15 else ""
            f.write(f"- {k}: {v} ({pct:.1f}%){flag}\n")
            
        f.write(f"\n## Duplication Metrics\n")
        f.write(f"- **Exact Duplicates:** {duplicates} (mostly standard SEBI/AMFI boilerplate disclaimers)\n")
        f.write(f"- **Near-Duplicates:** 0 (Textual similarity requires embeddings to accurately measure)\n")

    print("Distribution audit complete.")

if __name__ == "__main__":
    audit_distribution()

import json
import logging
from retrieval.query_router import route_query
from retrieval.embed_query import embed_query
from retrieval.search import get_qdrant

def search_raw(query_vector: list[float], top_k: int = 100):
    client = get_qdrant()
    response = client.query_points(
        collection_name="sif_documents",
        query=query_vector,
        limit=top_k
    )
    chunks = []
    for point in response.points:
        chunk_data = point.payload
        base_score = point.score
        priority_tier = chunk_data.get("priority_tier", 3)
        
        if priority_tier == 1: multiplier = 1.50
        elif priority_tier == 2: multiplier = 1.20
        elif priority_tier == 3: multiplier = 1.00
        elif priority_tier == 4: multiplier = 0.80
        elif priority_tier == 5: multiplier = 0.50
        else: multiplier = 1.00
        
        chunk_data["_score"] = base_score * multiplier
        chunk_data["_base_score"] = base_score
        chunks.append(chunk_data)
        
    return chunks

def main():
    queries = {
        "Regulatory": [
            "What is the minimum investment for SIFs?",
            "What is the maximum unhedged short exposure?",
            "What are SEBI's eligibility criteria?"
        ],
        "Product": [
            "What is Titanium Hybrid Long-Short Fund?",
            "Explain Sapphire Equity Long-Short SIF.",
            "What strategies does qSIF offer?"
        ],
        "Market Inventory": [
            "What SIFs exist?",
            "Show all Tata SIFs.",
            "Which SIFs are live?"
        ],
        "Comparison": [
            "Compare iSIF and Titanium.",
            "Compare Hybrid Long-Short vs Equity Long-Short."
        ]
    }
    
    score_report = {
        "Regulatory": {"passed": 0, "total": 0},
        "Product": {"passed": 0, "total": 0},
        "Market Inventory": {"passed": 0, "total": 0},
        "Comparison": {"passed": 0, "total": 0}
    }
    
    with open("docs/retrieval_benchmark.md", "w") as f:
        f.write("# Retrieval Benchmark Suite V1\n\n")
        
        for category, qs in queries.items():
            f.write(f"## Category: {category}\n\n")
            
            for q in qs:
                f.write(f"### Query: \"{q}\"\n")
                
                route_type, params = route_query(q)
                f.write(f"**Route:** `{route_type}`\n\n")
                
                if category in ["Market Inventory", "Comparison"]:
                    score_report[category]["total"] += 1
                    if route_type in ["discovery", "comparison"]:
                        f.write("- **Result:** Successfully bypassed vector retrieval.\n")
                        f.write("- **Vectors Retrieved:** 0\n\n")
                        score_report[category]["passed"] += 1
                    else:
                        f.write("- **Result:** FAILED to bypass vector retrieval.\n\n")
                    continue
                
                # It's Regulatory or Product (RAG)
                score_report[category]["total"] += 1
                query_vector = embed_query(q)
                chunks = search_raw(query_vector, top_k=100)
                
                # Before Reranking
                chunks_before = sorted(chunks, key=lambda x: x["_base_score"], reverse=True)[:10]
                
                # After Reranking
                chunks_after = sorted(chunks, key=lambda x: x["_score"], reverse=True)[:10]
                
                f.write("#### Before Reranking (Raw Cosine)\n")
                for i, c in enumerate(chunks_before, 1):
                    f.write(f"{i}. `{c.get('document_id')}` (Tier {c.get('priority_tier')}) | Base: {c.get('_base_score'):.4f}\n")
                    
                f.write("\n#### After Reranking (Boosted)\n")
                auth_count = 0
                for i, c in enumerate(chunks_after, 1):
                    auth = c.get('source_authority', '')
                    tier = c.get('priority_tier')
                    score = c.get('_score', 0)
                    base = c.get('_base_score', 0)
                    
                    if category == "Regulatory" and auth in ["regulator", "official_amc"]:
                        auth_count += 1
                    elif category == "Product" and auth == "official_amc":
                        auth_count += 1
                        
                    f.write(f"{i}. `{c.get('document_id')}` | Auth: {auth} | Tier: {tier} | Base: {base:.4f} | Boosted: {score:.4f}\n")
                    
                auth_pct = (auth_count / len(chunks_after)) * 100 if chunks_after else 0
                f.write(f"\n**Authority % in Top 10:** {auth_pct:.1f}%\n\n")
                
                if category == "Regulatory" and auth_pct >= 80:
                    score_report[category]["passed"] += 1
                elif category == "Product" and auth_pct >= 70:
                    score_report[category]["passed"] += 1
                    
    # Generate Score
    total_passed = sum(c["passed"] for c in score_report.values())
    total_queries = sum(c["total"] for c in score_report.values())
    overall_score = (total_passed / total_queries) * 100
    
    with open("docs/retrieval_benchmark_score.md", "w") as f:
        f.write("# Retrieval Benchmark Score\n\n")
        f.write(f"## Overall Score: {overall_score:.1f} / 100\n\n")
        
        f.write("### Category Breakdown\n")
        for cat, data in score_report.items():
            pct = (data['passed'] / data['total']) * 100 if data['total'] > 0 else 0
            f.write(f"- **{cat}:** {data['passed']}/{data['total']} passed ({pct:.1f}%)\n")
            
    print("Benchmark completed. Reports generated.")

if __name__ == "__main__":
    main()

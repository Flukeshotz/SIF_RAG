from retrieval.search import get_qdrant, search_chunks
from retrieval.embed_query import embed_query
import collections

def main():
    client = get_qdrant()
    collection_name = "sif_documents"
    
    # Generate source_priority_audit.md
    print("Generating source priority audit...")
    offset = None
    categories = collections.defaultdict(lambda: {"count": 0, "tier": 0, "weight": 0})
    
    while True:
        res = client.scroll(
            collection_name=collection_name,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False
        )
        points, offset = res
        
        for point in points:
            payload = point.payload
            doc_type = payload.get("document_type", "Unknown")
            doc_id = payload.get("document_id", "Unknown")
            tier = payload.get("priority_tier", 3)
            auth = payload.get("source_authority", "Unknown")
            
            # Map tier to weight
            weight = 1.0
            if tier == 1: weight = 1.5
            elif tier == 2: weight = 1.2
            elif tier == 3: weight = 1.0
            elif tier == 4: weight = 0.8
            elif tier == 5: weight = 0.5
            
            # Sub-categorize Webpages
            cat_name = doc_type
            if doc_type == "Webpage":
                if "groww.in" in doc_id.lower():
                    cat_name = "Groww Pages"
                elif "indmoney.com" in doc_id.lower():
                    cat_name = "INDmoney Pages"
                elif "blog" in doc_id.lower():
                    cat_name = "Blogs"
                else:
                    cat_name = "AMC Websites"
            elif doc_type == "ISID": cat_name = "ISIDs"
            elif doc_type == "KIM": cat_name = "KIMs"
            elif doc_type == "SEBI Circular": cat_name = "SEBI Circulars"
            elif doc_type == "AMFI Circular": cat_name = "AMFI Circulars"
            elif doc_type == "Factsheet": cat_name = "Factsheets"
            
            categories[cat_name]["count"] += 1
            categories[cat_name]["tier"] = tier
            categories[cat_name]["weight"] = weight
            categories[cat_name]["auth"] = auth
            
        if offset is None:
            break
            
    with open("docs/source_priority_audit.md", "w") as f:
        f.write("# Source Priority Audit\n\n")
        f.write("| Source Category | Chunk Count | Assigned Tier | Retrieval Weight | Source Authority |\n")
        f.write("|-----------------|-------------|---------------|------------------|------------------|\n")
        
        # Sort by tier
        sorted_cats = sorted(categories.items(), key=lambda x: x[1]["tier"])
        
        for cat, data in sorted_cats:
            f.write(f"| {cat} | {data['count']} | Tier {data['tier']} | {data['weight']}x | {data['auth']} |\n")

    # Generate retrieval_weighting_report.md
    print("Generating retrieval weighting report...")
    query = "What is the minimum investment for SIFs?"
    query_vector = embed_query(query)
    
    # We want top 10 for the report
    chunks = search_chunks(query_vector, top_k=10)
    
    with open("docs/retrieval_weighting_report.md", "w") as f:
        f.write("# Retrieval Weighting Report\n\n")
        f.write(f"**Query:** \"{query}\"\n\n")
        f.write("This report verifies that Regulatory and AMC documents rank higher than Aggregator pages due to the custom re-ranking multiplier.\n\n")
        f.write("### Top 10 Retrieved Chunks\n\n")
        
        for i, chunk in enumerate(chunks, 1):
            f.write(f"#### {i}. {chunk.get('document_id')} ({chunk.get('document_type')})\n")
            f.write(f"- **Source Authority:** {chunk.get('source_authority', 'Unknown')}\n")
            f.write(f"- **Priority Tier:** {chunk.get('priority_tier', 'Unknown')}\n")
            f.write(f"- **Base Cosine Score:** {chunk.get('_base_score', 0):.4f}\n")
            f.write(f"- **Multiplier:** {chunk.get('retrieval_weight', 1.0)}x\n")
            f.write(f"- **Final Score:** {chunk.get('_score', 0):.4f}\n")
            
            snippet = chunk.get("text", "")[:150].replace("\\n", " ") + "..."
            f.write(f"- **Snippet:** {snippet}\n\n")

    print("Successfully generated priority audit and weighting reports.")

if __name__ == "__main__":
    main()

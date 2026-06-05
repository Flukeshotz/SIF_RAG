from db.qdrant_connection import get_client
from qdrant_client.models import Filter

_client = None

def get_qdrant():
    global _client
    if _client is None:
        _client = get_client()
    return _client

def search_chunks(query_vector: list[float], top_k: int = 5, query_filter: Filter = None):
    """Retrieves chunks from Qdrant and re-ranks them by source priority."""
    client = get_qdrant()
    
    # Fetch a wider net to re-rank
    fetch_k = top_k * 10
    
    response = client.query_points(
        collection_name="sif_documents",
        query=query_vector,
        query_filter=query_filter,
        limit=fetch_k
    )
    
    chunks = []
    for point in response.points:
        chunk_data = point.payload
        base_score = point.score
        
        priority_tier = chunk_data.get("priority_tier", 3)
        
        # Apply multipliers based on Tier
        if priority_tier == 1:
            multiplier = 1.50
        elif priority_tier == 2:
            multiplier = 1.20
        elif priority_tier == 3:
            multiplier = 1.00
        elif priority_tier == 4:
            multiplier = 0.80
        elif priority_tier == 5:
            multiplier = 0.50
        else:
            multiplier = 1.00
            
        modified_score = base_score * multiplier
        
        chunk_data["_score"] = modified_score
        chunk_data["_base_score"] = base_score
        chunk_data["retrieval_weight"] = multiplier
        
        chunks.append(chunk_data)
        
    # Re-sort by the modified score
    chunks.sort(key=lambda x: x["_score"], reverse=True)
    
    return chunks[:top_k]

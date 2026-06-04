from db.qdrant_connection import get_client
from qdrant_client.models import Filter

_client = None

def get_qdrant():
    global _client
    if _client is None:
        _client = get_client()
    return _client

def search_chunks(query_vector: list[float], top_k: int = 5, query_filter: Filter = None):
    """Retrieves top_k chunks from Qdrant using the query vector."""
    client = get_qdrant()
    
    response = client.query_points(
        collection_name="sif_documents",
        query=query_vector,
        query_filter=query_filter,
        limit=top_k
    )
    
    # Return payloads with their ids
    chunks = []
    for point in response.points:
        chunk_data = point.payload
        chunk_data["_score"] = point.score
        chunks.append(chunk_data)
        
    return chunks

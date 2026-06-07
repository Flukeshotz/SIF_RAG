from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from pathlib import Path
from core.config import settings

_client = None

def get_client() -> QdrantClient:
    """Returns a local Qdrant Client."""
    global _client
    if _client is None:
        db_path = Path(settings.QDRANT_PATH)
        db_path.mkdir(parents=True, exist_ok=True)
        _client = QdrantClient(path=str(db_path))
    return _client

def init_collection(client: QdrantClient, collection_name: str = "sif_documents", recreate: bool = False):
    """Recreates the collection with proper vector schema if needed."""
    if client.collection_exists(collection_name):
        if recreate:
            client.delete_collection(collection_name)
        else:
            return
            
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    print(f"Collection '{collection_name}' initialized successfully.")

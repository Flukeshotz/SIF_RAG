from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from pathlib import Path
from core.config import settings

def get_client() -> QdrantClient:
    """Returns a local Qdrant Client."""
    db_path = Path(settings.QDRANT_PATH)
    db_path.mkdir(parents=True, exist_ok=True)
    return QdrantClient(path=str(db_path))

def init_collection(client: QdrantClient, collection_name: str = "sif_documents"):
    """Recreates the collection with proper vector schema."""
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
        
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    print(f"Collection '{collection_name}' initialized successfully.")

from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        # BGE embeddings expect a query instruction for retrieval tasks.
        # But for document encoding, they do not need the instruction.
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        
    def encode_documents(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Encode document chunks without prefix."""
        return self.model.encode(texts, batch_size=batch_size, show_progress_bar=True, normalize_embeddings=True)
        
    def encode_queries(self, queries: List[str]) -> np.ndarray:
        """Encode search queries using the BGE specific instruction prefix."""
        instruction = "Represent this sentence for searching relevant passages: "
        prefixed_queries = [instruction + q for q in queries]
        return self.model.encode(prefixed_queries, normalize_embeddings=True)

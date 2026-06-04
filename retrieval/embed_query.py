from embeddings.model import EmbeddingModel

_model = None

def get_embedding_model():
    global _model
    if _model is None:
        _model = EmbeddingModel()
    return _model

def embed_query(query: str) -> list[float]:
    """Generates a 384-dimensional vector for a user query."""
    model = get_embedding_model()
    # model.encode_queries returns a 2D numpy array, we want the first element as a list
    vector = model.encode_queries([query])[0]
    return vector.tolist()

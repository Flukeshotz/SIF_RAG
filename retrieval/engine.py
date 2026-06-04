from retrieval.embed_query import embed_query
from retrieval.search import search_chunks
from retrieval.context_builder import build_context
from retrieval.citations import generate_citations
from generation.llm import generate_response
import time

def answer_query(query: str) -> str:
    """
    The master entrypoint for the SIF Copilot MVP RAG pipeline.
    """
    # 1. Embed Query
    query_vector = embed_query(query)
    
    # 2. Retrieve Top 5 chunks from Qdrant
    chunks = search_chunks(query_vector, top_k=5)
    
    if not chunks:
        return "I could not find this information in the available official documents."
        
    # 3. Assemble Deterministic Context (max 6000 tokens)
    context_str, included_chunks = build_context(chunks, max_tokens=6000)
    
    # 4. Generate LLM Response with strict constraints
    response_text = generate_response(context_str, query)
    
    # 5. Append citations footer
    citations_text = generate_citations(included_chunks)
    
    final_response = f"{response_text}{citations_text}"
    return final_response

def answer_query_structured(query: str) -> dict:
    """
    Structured entrypoint for the API, returning separate answer, citations, and retrieval metrics.
    """
    start_time = time.perf_counter()
    query_vector = embed_query(query)
    chunks = search_chunks(query_vector, top_k=5)
    search_time_ms = int((time.perf_counter() - start_time) * 1000)
    
    if not chunks:
        return {
            "answer": "I could not find this information in the available official documents.",
            "citations": [],
            "retrieval": {
                "chunks_retrieved": 0,
                "search_time_ms": search_time_ms,
                "embedding_model": "bge-small-en-v1.5",
                "llm": "llama-3.1-8b-instant"
            }
        }
        
    context_str, included_chunks = build_context(chunks, max_tokens=6000)
    
    # Normalize included_chunks to ensure confidence is mapped
    for chunk in included_chunks:
        chunk["confidence"] = round(chunk.get("_score", 0.0), 2)
        chunk["document_title"] = chunk.get("document_id", "Unknown Document")
        
    response_text = generate_response(context_str, query)
    
    return {
        "answer": response_text,
        "citations": included_chunks,
        "retrieval": {
            "chunks_retrieved": len(included_chunks),
            "search_time_ms": search_time_ms,
            "embedding_model": "bge-small-en-v1.5",
            "llm": "llama-3.1-8b-instant"
        }
    }

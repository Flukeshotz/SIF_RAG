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
    
    # --- PHASE 7.6: QUERY ROUTING ---
    from retrieval.query_router import route_query
    from registry.service import get_all_funds, get_funds_by_amc, get_funds_by_strategy, get_live_funds, get_nfo_funds, compare_funds
    
    route_type, params = route_query(query)
    
    if route_type in ("inventory", "discovery", "market_discovery"):
        if "amc" in params and params["amc"]:
            funds = get_funds_by_amc(params["amc"][0])
        elif "strategy" in params and params["strategy"]:
            funds = get_funds_by_strategy(params["strategy"][0])
        elif "filter_status" in params:
            if params["filter_status"] == "Live":
                funds = get_live_funds()
            else:
                funds = get_nfo_funds()
        else:
            funds = get_all_funds()
            
        search_time_ms = int((time.perf_counter() - start_time) * 1000)
        return {
            "answer": f"We currently have structured information for {len(funds)} funds matching your criteria.",
            "query_type": "inventory",
            "structured_data": funds,
            "citations": [],
            "retrieval": {
                "chunks_retrieved": len(funds),
                "search_time_ms": search_time_ms,
                "embedding_model": "registry_lookup",
                "llm": "none"
            }
        }
        
    if route_type == "comparison":
        funds = compare_funds(params.get("funds", []))
        search_time_ms = int((time.perf_counter() - start_time) * 1000)
        return {
            "answer": f"Here is the comparison between the requested funds.",
            "query_type": "comparison",
            "structured_data": funds,
            "citations": [],
            "retrieval": {
                "chunks_retrieved": len(funds),
                "search_time_ms": search_time_ms,
                "embedding_model": "registry_lookup",
                "llm": "none"
            }
        }
        
    if route_type == "amc_comparison":
        amcs = params.get("amcs", [])
        funds_by_amc = {}
        for amc in amcs:
            funds_by_amc[amc] = get_funds_by_amc(amc)
            
        answer_lines = ["I found multiple SIFs under these AMCs.\n"]
        for amc in amcs:
            pretty_amc = amc.title()
            if funds_by_amc[amc]:
                pretty_amc = funds_by_amc[amc][0].get("amc", pretty_amc)
                
            answer_lines.append(f"**{pretty_amc}**")
            for f in funds_by_amc[amc]:
                answer_lines.append(f"• {f.get('fund_name')}")
            answer_lines.append("")
            
        answer_lines.append("Which specific funds would you like me to compare?")
        
        search_time_ms = int((time.perf_counter() - start_time) * 1000)
        return {
            "answer": "\n".join(answer_lines),
            "query_type": "amc_comparison",
            "structured_data": funds_by_amc,
            "citations": [],
            "retrieval": {
                "chunks_retrieved": sum(len(f) for f in funds_by_amc.values()),
                "search_time_ms": search_time_ms,
                "embedding_model": "registry_lookup",
                "llm": "none"
            }
        }
    
    # --- DEFAULT: RAG PIPELINE ---
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
    
    # Post-process answer to reduce cognitive load
    from retrieval.answer_cleaner import clean_answer
    cleaned_response = clean_answer(response_text)
    
    return {
        "answer": cleaned_response,
        "query_type": "rag",
        "citations": included_chunks,
        "retrieval": {
            "chunks_retrieved": len(included_chunks),
            "search_time_ms": search_time_ms,
            "embedding_model": "bge-small-en-v1.5",
            "llm": "llama-3.1-8b-instant"
        }
    }

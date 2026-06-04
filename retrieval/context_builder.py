import tiktoken

def get_tokenizer():
    # cl100k_base is the standard tokenizer used for modern LLMs (including Llama/GPT)
    return tiktoken.get_encoding("cl100k_base")

def build_context(chunks: list[dict], max_tokens: int = 6000) -> tuple[str, list[dict]]:
    """
    Builds the context string for the prompt.
    Returns the assembled string and the list of chunks actually included.
    """
    tokenizer = get_tokenizer()
    context_str = "=== RETRIEVED CONTEXT ===\n\n"
    
    included_chunks = []
    current_tokens = len(tokenizer.encode(context_str + "\n=== END OF CONTEXT ==="))
    
    for i, chunk in enumerate(chunks, 1):
        source_idx = i
        
        doc_title = chunk.get("document_id", "Unknown Document")
        doc_type = chunk.get("document_type", "Unknown Type")
        amc = chunk.get("organization", "Unknown AMC")
        fund = chunk.get("fund_name", "Unknown Fund")
        text = chunk.get("text", "")
        
        # publication_date is missing from schema, use "Current"
        chunk_str = (
            f"[Source {source_idx}]\n"
            f"Document: {doc_title}\n"
            f"Type: {doc_type} | AMC: {amc} | Fund: {fund} | Date: Current\n"
            f"Content:\n{text}\n\n---\n\n"
        )
        
        chunk_tokens = len(tokenizer.encode(chunk_str))
        
        if current_tokens + chunk_tokens > max_tokens:
            break
            
        context_str += chunk_str
        current_tokens += chunk_tokens
        included_chunks.append(chunk)
        
    context_str += "=== END OF CONTEXT ==="
    
    return context_str, included_chunks

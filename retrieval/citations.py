def generate_citations(included_chunks: list[dict]) -> str:
    """
    Generates the citations footer mapping [Source N] to actual document metadata.
    """
    if not included_chunks:
        return ""
        
    citations = "\n\n**Sources:**\n"
    for i, chunk in enumerate(included_chunks, 1):
        doc_title = chunk.get("document_id", "Unknown Document")
        doc_type = chunk.get("document_type", "Unknown Type")
        amc = chunk.get("organization", "Unknown AMC")
        
        # We don't have exact publication_date, so we'll omit or use "Current"
        citations += f"- [Source {i}]: {doc_title} — {amc}, {doc_type}\n"
        
    return citations

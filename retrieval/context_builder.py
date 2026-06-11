import re
import tiktoken

def get_tokenizer():
    return tiktoken.get_encoding("cl100k_base")


def _count_real_cols(row: str) -> int:
    """Count columns with actual non-whitespace content."""
    inner = row.strip().strip('|')
    return len([c for c in inner.split('|') if c.strip()])


def _is_separator_row(row: str) -> bool:
    inner = row.strip().strip('|')
    cells = [c.strip() for c in inner.split('|') if c.strip()]
    return bool(cells) and all(re.match(r'^:?-+:?$', c) for c in cells)


def sanitize_chunk_text(text: str) -> str:
    """
    Clean a raw chunk before it reaches the LLM.

    Problems handled:
    A) Mid-sentence start — chunk begins lowercase/punctuation (PDF shredding).
       Strategy: find the first real sentence boundary. If none exists, the
       chunk is pure table-fragment garbage → return "" so it gets skipped.
    B) Single-column pipe lines — broken table rows from multi-column PDF
       tables that were chunked across rows. Strip the pipes, emit as text,
       or drop if empty.
    C) Table rows where ALL columns beyond the first are empty — artifact of
       colspan cells in PDFs. Drop those rows entirely.
    """
    if not text:
        return ""

    # ── A. Trim mid-sentence starts ──────────────────────────────────────────
    first_real = text.lstrip()
    first_char = first_real[0] if first_real else ''
    starts_broken = first_char and (first_char.islower() or first_char in ':-.;,')

    if starts_broken:
        # Look for the first real sentence start: capital letter that follows
        # a newline, a period+space, or appears after a | boundary.
        match = re.search(r'(?:(?<=\n)|(?<=\.\s)|(?<=\|\s))\s*([A-Z][a-zA-Z])', text)
        if match:
            text = text[match.start():]
        else:
            # No clean sentence start anywhere — entire chunk is a fragment
            return ""

    # ── B & C. Process pipe lines ─────────────────────────────────────────────
    cleaned = []
    for line in text.split('\n'):
        ls = line.strip()
        if ls.startswith('|'):
            if not ls.endswith('|'):
                # Continuation row from a word-wrapped table cell — strip the
                # leading pipe and emit as plain text (or drop if only whitespace)
                plain = ls.lstrip('|').strip()
                if plain:
                    cleaned.append(plain)
                continue
            if _is_separator_row(ls):
                cleaned.append(line)          # keep valid separator rows
                continue
            real_cols = _count_real_cols(ls)
            if real_cols == 0:
                continue                       # empty row — drop
            if real_cols == 1:
                # Single content cell — emit as plain text
                plain = ls.strip('|').strip()
                if plain:
                    cleaned.append(plain)
            else:
                cleaned.append(line)          # real multi-column row — keep
        else:
            cleaned.append(line)

    result = '\n'.join(cleaned).strip()
    return result


def build_context(chunks: list[dict], max_tokens: int = 6000) -> tuple[str, list[dict]]:
    """
    Builds the context string for the LLM prompt.
    Returns the assembled string and the list of chunks actually included.
    """
    tokenizer = get_tokenizer()
    context_str = "=== RETRIEVED CONTEXT ===\n\n"

    included_chunks = []
    current_tokens = len(tokenizer.encode(context_str + "\n=== END OF CONTEXT ==="))

    for i, chunk in enumerate(chunks, 1):
        doc_title = chunk.get("document_id", "Unknown Document")
        doc_type  = chunk.get("document_type", "Unknown Type")
        amc       = chunk.get("organization", "Unknown AMC")
        fund      = chunk.get("fund_name", "Unknown Fund")
        raw_text  = chunk.get("text", "")

        text = sanitize_chunk_text(raw_text)
        if not text:
            continue   # drop broken/empty chunks entirely

        chunk_str = (
            f"[Source {i}]\n"
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

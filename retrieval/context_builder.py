import re
import tiktoken

def get_tokenizer():
    # cl100k_base is the standard tokenizer used for modern LLMs (including Llama/GPT)
    return tiktoken.get_encoding("cl100k_base")


def sanitize_chunk_text(text: str) -> str:
    """
    Clean up a chunk of text before it is fed to the LLM.
    Handles two common PDF-extraction artefacts:

    1. Mid-sentence starts: if the text begins with a lowercase letter or
       certain punctuation (e.g. '-ting', ':-ting'), the PDF chunker caught
       the tail of a previous sentence. We trim to the first real sentence
       boundary (capital letter after newline/period) so the LLM sees
       complete, parseable text.

    2. Single-column pipe lines: lines like '| some text |' with only one
       cell are broken PDF table rows that confuse the markdown renderer.
       Strip the pipes and emit the content as plain text instead.
    """
    if not text:
        return text

    # ── 1. Trim mid-sentence starts ─────────────────────────────────────────
    stripped_start = text.lstrip()
    first_char = stripped_start[0] if stripped_start else ''
    if first_char and (first_char.islower() or first_char in ':-,;.'):
        # Seek the first real sentence start (capital after newline or ". ")
        match = re.search(r'(?:(?<=\n)|(?<=\.\s))\s*([A-Z])', text)
        if match:
            text = text[match.start():]

    # ── 2. Strip single-column pipe lines ───────────────────────────────────
    cleaned_lines = []
    for line in text.split('\n'):
        ls = line.strip()
        if ls.startswith('|') and ls.endswith('|'):
            inner = ls.strip('|')
            cells = [c for c in inner.split('|') if c.strip()]
            is_sep = cells and all(re.match(r'^:?-+:?$', c.strip()) for c in cells)
            if is_sep or len(cells) >= 2:
                cleaned_lines.append(line)   # real table row — keep as-is
            else:
                plain = inner.strip()        # single-column fragment — plain text
                if plain:
                    cleaned_lines.append(plain)
        else:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines).strip()


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
        doc_title = chunk.get("document_id", "Unknown Document")
        doc_type = chunk.get("document_type", "Unknown Type")
        amc = chunk.get("organization", "Unknown AMC")
        fund = chunk.get("fund_name", "Unknown Fund")
        raw_text = chunk.get("text", "")

        # Sanitise before feeding to LLM — this is the root-cause fix
        text = sanitize_chunk_text(raw_text)
        if not text:
            continue   # skip empty/useless chunks after sanitisation

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

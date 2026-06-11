import re
from difflib import SequenceMatcher

def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def _count_real_columns(row: str) -> int:
    """Count real content columns in a pipe-delimited row."""
    # Strip outer pipes then split
    inner = row.strip().strip('|')
    return len([c for c in inner.split('|') if c.strip()])


def _is_separator_row(row: str) -> bool:
    """Return True if this is a markdown table separator like |---|---|."""
    inner = row.strip().strip('|')
    return all(
        re.match(r'^:?-+:?$', cell.strip())
        for cell in inner.split('|')
        if cell.strip()
    )


def strip_broken_pipe_lines(text: str) -> str:
    """
    Remove lines that contain a pipe character but are clearly NOT real markdown
    table rows — e.g. single-column PDF fragments like "| some text |".
    A real table row must have ≥2 columns.
    """
    cleaned = []
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            if _is_separator_row(stripped):
                # Keep separator rows only if preceded by a real header
                cleaned.append(line)
            elif _count_real_columns(stripped) >= 2:
                # Real multi-column table row — keep
                cleaned.append(line)
            else:
                # Single-column pipe fragment from a broken PDF table — strip pipes,
                # emit as plain text
                plain = stripped.strip('|').strip()
                if plain:
                    cleaned.append(plain)
        else:
            cleaned.append(line)
    return '\n'.join(cleaned)


def repair_markdown_tables(text: str) -> str:
    """
    Detects malformed markdown tables (missing the separator row) and repairs them.
    Only operates on REAL multi-column tables (≥2 columns). Single-column pipe
    lines should have been stripped by strip_broken_pipe_lines already.
    """
    lines = text.split('\n')
    repaired_lines = []

    in_table = False
    header_processed = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        is_pipe_row = stripped.startswith('|') and stripped.endswith('|')
        is_real_row = is_pipe_row and (
            _is_separator_row(stripped) or _count_real_columns(stripped) >= 2
        )

        if is_real_row:
            if not in_table:
                in_table = True
                header_processed = False

            repaired_lines.append(line)

            if in_table and not header_processed and not _is_separator_row(stripped):
                next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                if not _is_separator_row(next_line):
                    cols = _count_real_columns(stripped)
                    if cols > 0:
                        separator = "|" + "|".join(["---"] * cols) + "|"
                        repaired_lines.append(separator)
                header_processed = True
        else:
            if in_table:
                in_table = False
                repaired_lines.append("")
            repaired_lines.append(line)

    return '\n'.join(repaired_lines)


def deduplicate_sections(text: str) -> str:
    """
    Parses markdown text by bold headings (**Heading** or ### Heading)
    and deduplicates repeated headings by merging content or discarding
    highly similar redundant content.
    """
    pattern = re.compile(r'^(?:\*\*|###\s+)(.+?)(?:\*\*)?\s*$', re.MULTILINE)
    parts = pattern.split(text)

    if len(parts) <= 1:
        return text

    cleaned_text = parts[0].strip() + "\n\n" if parts[0].strip() else ""
    seen_sections: dict = {}

    for i in range(1, len(parts), 2):
        raw_heading = parts[i].strip()
        norm_heading = raw_heading.lower()
        if norm_heading == "portfolio composition":
            norm_heading = "asset allocation"
            raw_heading = "Asset Allocation"

        content = parts[i + 1].strip() if i + 1 < len(parts) else ""

        if norm_heading not in seen_sections:
            seen_sections[norm_heading] = [content]
        else:
            is_duplicate = any(
                similar(content, existing) > 0.7
                for existing in seen_sections[norm_heading]
            )
            if not is_duplicate and content:
                seen_sections[norm_heading].append(content)

    for heading, contents in seen_sections.items():
        display_heading = heading.title()
        if display_heading.lower() == "asset allocation":
            display_heading = "Asset Allocation"
        cleaned_text += f"**{display_heading}**\n"
        for c in contents:
            cleaned_text += f"{c}\n\n"

    return cleaned_text.strip()


def strip_broken_answer_start(text: str) -> str:
    """
    If the LLM response starts mid-sentence, trim to the first real prose sentence.
    Skips metadata-looking lines like 'Document:', '[Source N]', 'Type:' etc.
    """
    stripped = text.lstrip()
    if not stripped:
        return text
    first_char = stripped[0]
    if first_char == '|' or first_char.islower() or first_char in ':-.;,':
        # Find first line that looks like real prose:
        # - starts with a capital letter
        # - is NOT a metadata key (Document:, Type:, Content:, AMC:)
        # - is NOT a source marker ([Source N])
        # - has meaningful length
        meta_pattern = re.compile(
            r'^(?:\[Source|Document:|Type:|Content:|AMC:|Fund:|Date:)', re.IGNORECASE
        )
        for line in text.split('\n'):
            l = line.strip()
            if not l:
                continue
            if l[0].isupper() and not meta_pattern.match(l) and len(l) > 20:
                idx = text.find(line)
                if idx != -1:
                    return text[idx:].lstrip()
    return text


def strip_source_blocks(text: str) -> str:
    """
    Remove any [Source N]\nDocument: ... blocks that the LLM mistakenly
    echoes verbatim from the context into its answer.
    """
    return re.sub(
        r'\[Source \d+\]\nDocument:.*?(?=\n\[Source \d+\]|\Z)',
        '',
        text,
        flags=re.DOTALL
    ).strip()


def clean_answer(text: str) -> str:
    """
    Master post-processor for LLM output.
    Order matters:
      1. Strip echoed source-block metadata ([Source N]\nDocument:...)
      2. Trim broken answer starts (LLM started mid-sentence or with a table)
      3. Strip broken single-column pipe lines (PDF table fragments)
      4. Repair any real but malformed markdown tables
      5. Deduplicate repeated sections
    """
    text = strip_source_blocks(text)
    text = strip_broken_answer_start(text)
    text = strip_broken_pipe_lines(text)
    text = repair_markdown_tables(text)
    text = deduplicate_sections(text)
    return text

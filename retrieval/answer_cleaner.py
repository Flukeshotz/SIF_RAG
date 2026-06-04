import re
from difflib import SequenceMatcher

def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def repair_markdown_tables(text: str) -> str:
    """
    Detects malformed markdown tables (missing the separator row) and repairs them.
    Also ensures they are separated by newlines so they render correctly.
    """
    lines = text.split('\n')
    repaired_lines = []
    
    in_table = False
    header_processed = False
    
    for i, line in enumerate(lines):
        # A simple heuristic for a table row: starts with | and ends with |
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            if not in_table:
                # Start of a new table
                in_table = True
                header_processed = False
                
            repaired_lines.append(line)
            
            # If we just added the header, check if the NEXT line is a separator
            if in_table and not header_processed:
                next_line = lines[i+1].strip() if i + 1 < len(lines) else ""
                if not (next_line.startswith('|') and '-' in next_line):
                    # Missing separator! Let's inject one based on the number of columns
                    cols = len([c for c in stripped.split('|') if c.strip() or c == '']) - 2
                    if cols > 0:
                        separator = "|" + "|".join(["---"] * cols) + "|"
                        repaired_lines.append(separator)
                header_processed = True
        else:
            if in_table:
                in_table = False
                # Add an extra newline after table just in case
                repaired_lines.append("")
            repaired_lines.append(line)
            
    return '\n'.join(repaired_lines)


def deduplicate_sections(text: str) -> str:
    """
    Parses markdown text by bold headings (**Heading** or ### Heading)
    and deduplicates repeated headings by merging content or discarding
    highly similar redundant content.
    """
    # Regex to find headings like **Heading** or ### Heading
    # We split the document into segments: (heading, content)
    
    # Pattern explanation:
    # ^(?:\*\*|### )([^\n*]+)(?:\*\*)?$ matches a heading line
    pattern = re.compile(r'^(?:\*\*|###\s+)(.+?)(?:\*\*)?\s*$', re.MULTILINE)
    
    parts = pattern.split(text)
    
    if len(parts) <= 1:
        # No headings found, just return text
        return text
    
    # parts[0] is intro text before first heading
    cleaned_text = parts[0].strip() + "\n\n" if parts[0].strip() else ""
    
    seen_sections = {}
    
    # parts[1] is heading1, parts[2] is content1, etc.
    for i in range(1, len(parts), 2):
        raw_heading = parts[i].strip()
        
        # Normalize heading to detect duplicates (e.g. "Asset Allocation" == "Portfolio Composition")
        norm_heading = raw_heading.lower()
        if norm_heading == "portfolio composition":
            norm_heading = "asset allocation"
            raw_heading = "Asset Allocation"
            
        content = parts[i+1].strip() if i+1 < len(parts) else ""
        
        if norm_heading not in seen_sections:
            seen_sections[norm_heading] = [content]
        else:
            # Check if content is a duplicate of existing content
            is_duplicate = False
            for existing_content in seen_sections[norm_heading]:
                if similar(content, existing_content) > 0.7:
                    is_duplicate = True
                    break
            
            if not is_duplicate and content:
                seen_sections[norm_heading].append(content)
                
    # Reassemble
    for heading, contents in seen_sections.items():
        # Capitalize heading properly
        display_heading = heading.title()
        if display_heading.lower() == "asset allocation":
            display_heading = "Asset Allocation"
            
        # Or just use the original casing (we'll use title case for uniformity)
        cleaned_text += f"**{display_heading}**\n"
        for c in contents:
            cleaned_text += f"{c}\n\n"
            
    return cleaned_text.strip()


def clean_answer(text: str) -> str:
    """
    Master post-processor for LLM output.
    """
    # 1. Deduplicate
    text = deduplicate_sections(text)
    
    # 2. Repair tables
    text = repair_markdown_tables(text)
    
    return text

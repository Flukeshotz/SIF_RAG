import fitz
from typing import List, Tuple
from processing.document_model import Section, Table
from processing.table_extractor import extract_tables_from_page

def extract_text_and_tables(pdf_path: str) -> Tuple[List[Section], List[Table]]:
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening {pdf_path}: {e}")
        return [], []

    sections = []
    all_tables = []
    
    current_section = Section(title="Document Start", level=1, page=1)
    sections.append(current_section)
    
    # We will use a simple heuristic based on font size to detect headers
    # A more robust implementation would gather all font sizes, find the median (body text),
    # and treat sizes significantly larger as headers.
    
    font_sizes = []
    for page in doc:
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_IMAGES).get("blocks", [])
        for b in blocks:
            if b.get("type") == 0:  # Text block
                for l in b.get("lines", []):
                    for s in l.get("spans", []):
                        if s.get("text").strip():
                            font_sizes.append(s.get("size"))
                            
    if not font_sizes:
        # Scanned PDF or empty
        doc.close()
        return sections, all_tables
        
    # Sort and find approximate body text size (most common)
    from collections import Counter
    size_counts = Counter([round(sz, 1) for sz in font_sizes])
    body_size = size_counts.most_common(1)[0][0] if size_counts else 10.0
    
    import pdfplumber
    try:
        doc_plumber = pdfplumber.open(pdf_path)
    except:
        doc_plumber = None
        
    for page_num, page in enumerate(doc, 1):
        # Extract tables
        if doc_plumber and page_num - 1 < len(doc_plumber.pages):
            page_tables = extract_tables_from_page(doc_plumber.pages[page_num - 1], page_num)
            all_tables.extend(page_tables)
        
        # Extract text blocks
        blocks = page.get_text("dict").get("blocks", [])
        for b in blocks:
            if b.get("type") == 0:  # Text
                block_text = ""
                max_size = 0
                is_bold = False
                
                for l in b.get("lines", []):
                    for s in l.get("spans", []):
                        text = s.get("text", "").strip()
                        if text:
                            block_text += text + " "
                            if s.get("size", 0) > max_size:
                                max_size = s.get("size", 0)
                            if "bold" in s.get("font", "").lower() or "heavy" in s.get("font", "").lower():
                                is_bold = True
                
                block_text = block_text.strip()
                if not block_text:
                    continue
                    
                # Heuristic for Headings
                if max_size >= body_size + 2.0 or (max_size >= body_size + 0.5 and is_bold):
                    # It's a heading
                    level = 1 if max_size >= body_size + 4.0 else 2
                    
                    new_section = Section(title=block_text, level=level, page=page_num)
                    
                    if level == 1:
                        sections.append(new_section)
                        current_section = new_section
                    else:
                        # Append as subsection to the last level 1
                        sections[-1].subsections.append(new_section)
                        current_section = new_section
                else:
                    # Body text
                    current_section.content += block_text + "\n\n"
                    
    doc.close()
    if doc_plumber: doc_plumber.close()
    return sections, all_tables

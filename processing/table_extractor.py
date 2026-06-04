import pdfplumber
import pandas as pd
from typing import List
from processing.document_model import Table

def extract_tables_from_page(page: pdfplumber.page.Page, page_num: int) -> List[Table]:
    tables = []
    try:
        extracted_tables = page.extract_tables()
        
        for i, tab in enumerate(extracted_tables):
            if tab:
                # Clean up None values
                clean_tab = [[str(cell).strip() if cell is not None else "" for cell in row] for row in tab]
                # Use first row as header if it exists
                if len(clean_tab) > 1:
                    df = pd.DataFrame(clean_tab[1:], columns=clean_tab[0])
                else:
                    df = pd.DataFrame(clean_tab)
                
                markdown_table = df.to_markdown(index=False)
                
                title = f"Table {i+1} on Page {page_num}"
                
                tables.append(Table(
                    title=title,
                    markdown=markdown_table,
                    page=page_num
                ))
    except Exception as e:
        print(f"Error extracting tables on page {page_num}: {e}")
        
    return tables

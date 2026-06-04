import json
from pathlib import Path

def sanitize_factsheets():
    input_dir = Path("data/processed/documents")
    output_dir = Path("data/processed/sanitized")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Denylist for massive tables and historical factsheet data
    section_denylist = ["Performance", "Historical NAV", "Portfolio Holdings", "Top 100", "Top 10", "Dividend History", "Returns since inception"]
    
    count = 0
    for file_path in input_dir.glob("*.json"):
        with open(file_path, "r") as f:
            data = json.load(f)
            
        if data.get("document_type") == "Factsheet" or "factsheet" in data.get("document_id", "").lower():
            # Sanitize sections
            sanitized_sections = []
            for sec in data.get("sections", []):
                keep = True
                title = sec.get("title", "")
                
                for bad in section_denylist:
                    if bad.lower() in title.lower():
                        keep = False
                        break
                        
                if keep:
                    # check content length just in case it's a massive portfolio dump without a clear header
                    if len(sec.get("content", "").split()) < 2000:
                        sanitized_sections.append(sec)
                        
            data["sections"] = sanitized_sections
            
            # Sanitize tables (Factsheet tables are mostly performance/holdings)
            # We'll drastically reduce factsheet tables unless they mention Asset Allocation or Risk
            sanitized_tables = []
            for tab in data.get("tables", []):
                md = tab.get("markdown", "").lower()
                if "asset allocation" in md or "risk" in md or "exit load" in md:
                    sanitized_tables.append(tab)
                    
            data["tables"] = sanitized_tables
            
        with open(output_dir / file_path.name, "w") as f:
            json.dump(data, f, indent=2)
            count += 1
            
    # Generate Factsheet Sanitization Report
    report_path = Path("docs/factsheet_sanitization_report.md")
    with open(report_path, "w") as f:
        f.write("# Phase 3.6 — Factsheet Sanitization Report\n\n")
        f.write(f"Successfully sanitized {count} documents (factsheets filtered, ISID/KIM passed through).\n\n")
        f.write("## Rules Applied to Factsheets\n")
        f.write("- Dropped sections containing: Performance, Historical NAV, Portfolio Holdings, Dividend History.\n")
        f.write("- Dropped tables unless they contained: Asset Allocation, Risk, or Exit Load keywords.\n")
        
    print(f"Sanitization complete. Clean JSONs saved to {output_dir}")

if __name__ == "__main__":
    sanitize_factsheets()

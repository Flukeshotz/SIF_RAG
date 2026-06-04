from processing.document_model import Document
from typing import List, Dict

def validate_document(doc: Document) -> Dict[str, any]:
    errors = []
    warnings = []
    
    # 1. Required Metadata Fields
    if not doc.metadata.fund_name and doc.document_type != "SEBI Circular" and doc.document_type != "AMFI Circular":
        warnings.append("Missing fund_name for non-circular document")
        
    if doc.document_type in ["ISID", "KIM"]:
        if not doc.metadata.minimum_investment:
            warnings.append("Missing minimum_investment")
        elif doc.metadata.minimum_investment < 1000000:
            errors.append(f"Minimum investment must be >= 10L. Found: {doc.metadata.minimum_investment}")
            
        if not doc.metadata.risk_band:
            warnings.append("Missing risk_band")
            
        if doc.metadata.risk_band and not (1 <= doc.metadata.risk_band <= 5):
            errors.append(f"Invalid risk_band: {doc.metadata.risk_band}")
            
    # 2. Document Integrity
    if not doc.sections:
        errors.append("Document has 0 sections extracted (Parsing Failure)")
        
    # SEBI Circulars should have sections but no tables typically (unless formatting allows)
    # ISIDs should definitely have tables
    if doc.document_type == "ISID" and not doc.tables:
        warnings.append("ISID has 0 tables extracted")
        
    is_valid = len(errors) == 0
    
    return {
        "document_id": doc.document_id,
        "is_valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "section_count": len(doc.sections),
        "table_count": len(doc.tables)
    }

def generate_validation_report(results: List[Dict[str, any]], output_path: str):
    total = len(results)
    passed = sum(1 for r in results if r["is_valid"])
    failed = total - passed
    
    with open(output_path, "w") as f:
        f.write("# Phase 3 — Processing Validation Report\n\n")
        f.write("## Summary Metrics\n")
        f.write(f"- **Total Documents Processed:** {total}\n")
        f.write(f"- **Validation Passed:** {passed}\n")
        f.write(f"- **Validation Failed:** {failed}\n\n")
        
        f.write("## Detailed Report\n")
        f.write("| Document ID | Valid | Sections | Tables | Errors | Warnings |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        for r in results:
            valid_mark = "✅" if r["is_valid"] else "❌"
            errs = "<br>".join(r["errors"]) if r["errors"] else "None"
            warns = "<br>".join(r["warnings"]) if r["warnings"] else "None"
            f.write(f"| {r['document_id']} | {valid_mark} | {r['section_count']} | {r['table_count']} | {errs} | {warns} |\n")

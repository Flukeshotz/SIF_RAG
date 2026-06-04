import json
import os
from pathlib import Path
from processing.pdf_quality import main as quality_check
from processing.pdf_parser import extract_text_and_tables
from processing.metadata_extractor import extract_metadata
from processing.validator import validate_document, generate_validation_report
from processing.document_model import Document

def run_pipeline():
    print("Starting Phase 3: Document Processing Pipeline")
    
    # Ensure output dir exists
    output_dir = Path("data/processed/documents")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Quality Check
    print("\n--- Running PDF Quality Assessment ---")
    quality_check()
    
    pdf_dir = Path("data/raw/pdf")
    meta_dir = Path("data/raw/metadata")
    
    validation_results = []
    
    print("\n--- Running Parsers and Extractors ---")
    
    for pdf_path in pdf_dir.glob("*.pdf"):
        source_id = pdf_path.stem
        print(f"Processing {source_id}...")
        
        # Load source metadata
        meta_path = meta_dir / f"{source_id}.json"
        source_metadata = {}
        if meta_path.exists():
            source_metadata = json.loads(meta_path.read_text())
            
        # Parse PDF
        sections, tables = extract_text_and_tables(str(pdf_path))
        
        # Combine text for metadata extraction
        full_text = ""
        for s in sections:
            full_text += s.title + "\n" + s.content + "\n"
            for sub in s.subsections:
                full_text += sub.title + "\n" + sub.content + "\n"
                
        # Extract metadata
        extracted_meta = extract_metadata(full_text, source_metadata, tables)
        
        # Construct Document
        doc = Document(
            document_id=source_id,
            document_type=extracted_meta.document_type or "Unknown",
            organization=source_metadata.get("organization", "Unknown"),
            source_url=source_metadata.get("source_url", ""),
            effective_date=extracted_meta.effective_date or "",
            sections=sections,
            tables=tables,
            metadata=extracted_meta
        )
        
        # Validate
        val_result = validate_document(doc)
        validation_results.append(val_result)
        
        # Save JSON
        out_path = output_dir / f"{source_id}.json"
        out_path.write_text(doc.model_dump_json(indent=2))
        
    # Generate Validation Report
    report_path = "docs/processing_validation_report.md"
    generate_validation_report(validation_results, report_path)
    print(f"\nProcessing complete! Validation report saved to {report_path}")
    print(f"Processed documents saved to {output_dir}")

if __name__ == "__main__":
    run_pipeline()

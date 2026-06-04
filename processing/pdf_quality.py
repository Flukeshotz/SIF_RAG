import fitz  # PyMuPDF
import os
from pathlib import Path

def assess_pdf_quality(pdf_path: str):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        return {"error": str(e)}

    page_count = len(doc)
    extractable_text_count = 0
    image_count = 0

    for page in doc:
        text = page.get_text()
        if len(text.strip()) > 50:  # Arbitrary threshold to ensure it's not just a single character
            extractable_text_count += 1
            
        images = page.get_images(full=True)
        image_count += len(images)

    doc.close()

    # Classification logic
    is_digital = extractable_text_count >= (page_count * 0.8)  # 80% of pages have text
    is_scanned = extractable_text_count == 0 and image_count > 0
    
    if is_scanned:
        pdf_type = "Scanned"
    elif is_digital:
        pdf_type = "Digital"
    else:
        pdf_type = "Mixed"

    return {
        "file_name": os.path.basename(pdf_path),
        "page_count": page_count,
        "extractable_text_count": extractable_text_count,
        "image_count": image_count,
        "type": pdf_type,
        "ocr_required": pdf_type in ["Scanned", "Mixed"]
    }

def main():
    pdf_dir = Path("data/raw/pdf")
    results = []
    
    if not pdf_dir.exists():
        print(f"Directory {pdf_dir} does not exist.")
        return

    for file_path in pdf_dir.glob("*.pdf"):
        res = assess_pdf_quality(str(file_path))
        if "error" not in res:
            results.append(res)
            
    # Generate Markdown Report
    report_path = Path("docs/pdf_quality_assessment.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    total_pdfs = len(results)
    digital = sum(1 for r in results if r["type"] == "Digital")
    scanned = sum(1 for r in results if r["type"] == "Scanned")
    mixed = sum(1 for r in results if r["type"] == "Mixed")
    ocr_recommended = sum(1 for r in results if r["ocr_required"])
    
    with open(report_path, "w") as f:
        f.write("# Phase 3 — PDF Quality Assessment\n\n")
        f.write("## Summary\n")
        f.write(f"- **Total PDFs:** {total_pdfs}\n")
        f.write(f"- **Digital PDFs:** {digital}\n")
        f.write(f"- **Scanned PDFs:** {scanned}\n")
        f.write(f"- **Mixed PDFs:** {mixed}\n")
        f.write(f"- **OCR Required (Recommendation):** {ocr_recommended} documents need OCR\n\n")
        
        f.write("## Document Assessment\n")
        f.write("| Document | Pages | Digital | Scanned | Mixed | OCR Required |\n")
        f.write("|---|---|---|---|---|---|\n")
        for r in results:
            is_dig = "✅" if r["type"] == "Digital" else ""
            is_scan = "✅" if r["type"] == "Scanned" else ""
            is_mix = "✅" if r["type"] == "Mixed" else ""
            req_ocr = "Yes" if r["ocr_required"] else "No"
            f.write(f"| {r['file_name']} | {r['page_count']} | {is_dig} | {is_scan} | {is_mix} | {req_ocr} |\n")

    print(f"Assessment complete. Results saved to {report_path}")

if __name__ == "__main__":
    main()

# Phase 3.6 — OCR Recovery Evaluation

**Target Document:** `amfi-amfi-circular.pdf`

## OCRmyPDF Extraction (First 500 chars)
```text
ASSOCIATION OF MUTUAL FUNDS IN INDIA
CIR/ ARN-29/ 2025-26 
July 30, 2025
To:
All AMFI Members
Mutual Fund RTAs and
Mutual Fund Distributors (MFDs)
Dear Sir/Madam,
Re : Registration of MEDs for distribution of Specialized Investment Funds (SIFs)
In terms of SEBI Circular No. SEBI/HO/IMD/IMD-PoD-1/P/CIR/2025/26 dated February 27, 2025, “An entity
engaged in the sale and/or distribution of Mutual Fund products shall also be eligible to offer products under
the Strategic Investment Fund (SIF), subje
```

## Verdict
`OCRmyPDF` successfully reconstructs the text layer of scanned PDFs, allowing us to pipe the output directly into our existing `PyMuPDF` parser without rewriting the parsing engine. The scanned AMFI circulars will be pre-processed with OCRmyPDF.

# Phase 3.7 — Table Recovery Report

| Document ID | Old Tables | New Tables | Headers Preserved | Columns Preserved | Rows Preserved |
|---|---|---|---|---|---|
| external--uncategorized-isid.json | 64 | 64 | High | High | High |
| icici-prudential-amc-kim.json | 77 | 77 | High | High | High |
| franklin-templeton-kim.json | 40 | 40 | High | High | High |
| quant-mutual-fund-isid.json | 64 | 64 | High | High | High |
| external--uncategorized-isid-1.json | 66 | 66 | High | High | High |

## Before/After Examples
`pdfplumber` effectively recovered horizontal columns for Exit Loads and Asset Allocation that were previously merged by `PyMuPDF`.

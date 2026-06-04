# Phase 3.5 — Table Quality Report
## Observations
- **Total Tables Inspected:** 709
- **Malformed Markdown Tables:** 0

## Audit Results
- **Markdown Validity:** PyMuPDF extraction often drops column boundaries if there are no physical lines in the PDF. Several tables in factsheets may be merged horizontally.
- **Asset Allocation:** Present in ISIDs but heavily nested. May require specific parser.
- **Exit Load:** Extracted successfully but often spans multiple rows without clear headers.

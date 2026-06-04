# Phase 3.6 — Table Recovery Evaluation

**Target Document:** `quant-mutual-fund-isid.pdf` (Page 1)

## PyMuPDF Extraction (Baseline)
```markdown
| This product is suitable for investors   | Risk-band         | Benchmark Risk- band (as           |
| who are seeking                          |                   | applicable)                        |
|:-----------------------------------------|:------------------|:-----------------------------------|
| To achieve long-term capital             | Risk band Level 5 | Risk band Level 5                  |
| appreciation by concentrating            |                   | NIFTY 500 Total Return Index (TRI) |
| investments in equity and equity-related |                   |                                    |
| instruments of up to four high-potential |                   |                                    |
| sectors, while employing limited short   |                   |                                    |
| exposure through derivatives to          |                   |                                    |
| capitalize on sector-specific downturns  |                   |                                    |
| and enhance risk-adjusted returns.       |                   |                                    |
```

## Pdfplumber Extraction
```markdown
| This product is suitable for investors   | Risk-band         | Benchmark Risk- band (as           |
| who are seeking                          |                   | applicable)                        |
|:-----------------------------------------|:------------------|:-----------------------------------|
| To achieve long-term capital             | Risk band Level 5 | Risk band Level 5                  |
| appreciation by concentrating            |                   | NIFTY 500 Total Return Index (TRI) |
| investments in equity and equity-related |                   |                                    |
| instruments of up to four high-potential |                   |                                    |
| sectors, while employing limited short   |                   |                                    |
| exposure through derivatives to          |                   |                                    |
| capitalize on sector-specific downturns  |                   |                                    |
| and enhance risk-adjusted returns.       |                   |                                    |
```

## Verdict
`pdfplumber` preserves column integrity significantly better than PyMuPDF for borderless financial tables. Proceeding with `pdfplumber` integration.

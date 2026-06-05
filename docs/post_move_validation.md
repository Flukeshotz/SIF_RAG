# Post-Move Validation Report

Generated: 2026-06-06

## Summary

37 markdown files were moved from `docs/` into four subdirectories:
- `docs/reports/` (17 files)
- `docs/deployment/` (10 files)
- `docs/audits/` (6 files)
- `docs/product/` (4 files)

---

## 1. Markdown Links — Broken?

**No markdown cross-links are broken.**

None of the moved files contained `[text](docs/...)` style links pointing at each other or at other moved files. The moved files are standalone reports/audits with no internal cross-references.

## 2. README References — Still Resolve?

**✅ Yes.**

`README.md` has one `docs/` link:
- Line 40: `[Architecture Diagram](docs/architecture_diagram.md)` → file exists at `docs/architecture_diagram.md` (was NOT moved).

No other README links reference moved files.

## 3. Scripts Referencing Moved Docs — Updated?

**⚠️ 12 scripts write output to old `docs/` paths.**

These scripts generate reports and write them to `docs/<filename>`. After the move, re-running these scripts would recreate files at the old locations instead of the new subdirectories.

| Script | Old Output Path | New Correct Path |
|--------|----------------|-----------------|
| `scripts/audit_chunks.py:53` | `docs/chunk_audit.md` | `docs/audits/chunk_audit.md` |
| `scripts/audit_chunks.py:92` | `docs/chunk_retrieval_simulation.md` | `docs/reports/chunk_retrieval_simulation.md` |
| `scripts/audit_chunks.py:120` | `docs/embedding_readiness.md` | `docs/reports/embedding_readiness.md` |
| `scripts/validate_phase6.py:15` | `docs/advisory_refusal_results.md` | `docs/reports/advisory_refusal_results.md` |
| `scripts/audit_chunk_distribution.py:39` | `docs/chunk_distribution_report.md` | `docs/reports/chunk_distribution_report.md` |
| `scripts/generate_registry_reports.py:41` | `docs/coverage_report.md` | `docs/reports/coverage_report.md` |
| `scripts/generate_registry_reports.py:49` | `docs/amc_coverage_report.md` | `docs/reports/amc_coverage_report.md` |
| `scripts/rationalize_corpus.py:86` | `docs/corpus_rationalization_report.md` | `docs/reports/corpus_rationalization_report.md` |
| `scripts/run_phase85_audits.py:11` | `docs/github_verification.md` | `docs/audits/github_verification.md` |
| `scripts/run_phase85_audits.py:20` | `docs/backend_deployment_report.md` | `docs/deployment/backend_deployment_report.md` |
| `scripts/run_phase85_audits.py:31` | `docs/frontend_deployment_report.md` | `docs/deployment/frontend_deployment_report.md` |
| `scripts/run_phase8_audits.py:10` | `docs/deployment_audit.md` | `docs/deployment/deployment_audit.md` |
| `scripts/run_phase8_audits.py:59` | `docs/frontend_qa_report.md` | `docs/deployment/frontend_qa_report.md` |
| `scripts/evaluate_comprehensive.py:133` | `docs/evaluation_report.md` | `docs/reports/evaluation_report.md` |
| `scripts/mvp_pdf_downloader.py:105` | `docs/direct_pdf_acquisition_report.md` | `docs/reports/direct_pdf_acquisition_report.md` |
| `scripts/certify_phase_3.py:69` | `docs/factsheet_sanitization_report.md` | `docs/reports/factsheet_sanitization_report.md` |
| `scripts/audit_phase_3.py:103` | `docs/duplicate_content_report.md` | `docs/reports/duplicate_content_report.md` |
| `scripts/audit_phase_3.py:156` | `docs/golden_coverage_report.md` | `docs/reports/golden_coverage_report.md` |
| `processing/sanitizer.py:51` | `docs/factsheet_sanitization_report.md` | `docs/reports/factsheet_sanitization_report.md` |

Additionally, 2 audit generator scripts reference old output paths in docstrings:
- `scripts/generate_repo_audit_and_dependency_map.py:4-5`
- `scripts/generate_filtered_audit.py:20-21`

**Status: NOT YET FIXED — awaiting approval.**

## 4. CI Workflow References — Any Broken?

**✅ No.** No `.github/workflows/*.yml` files reference any `docs/` paths.

## 5. Deployment Documents — Broken Relative Links?

**✅ No.** The moved deployment docs (`docs/deployment/*.md`) contain no relative links to other docs.

## 6. Frontend Code — References Moved Paths?

**✅ No.** `api/`, `retrieval/`, `frontend/src/`, and `tests/` contain zero references to any `docs/` paths.

## 7. Backend Code — References Moved Paths?

**✅ No** (for production API/retrieval code).

**⚠️ One exception:** `processing/sanitizer.py:51` writes output to `docs/factsheet_sanitization_report.md`. This is a processing script, not a production API route. Listed in the scripts table above.

## 8. Test Fixtures — Reference Moved Paths?

**✅ No.** No test files reference `docs/` paths.

---

## Risk Assessment

| Category | Status |
|----------|--------|
| README links | ✅ Safe |
| CI workflows | ✅ Safe |
| Deployment configs | ✅ Safe |
| Frontend code | ✅ Safe |
| Backend API/retrieval | ✅ Safe |
| Test fixtures | ✅ Safe |
| Scripts (report generators) | ⚠️ 12 scripts need output path updates |
| `repository_audit.md` (old audit) | ℹ️ Contains stale file listings — cosmetic, no functional impact |

## Recommendation

The 12 script output path updates are **safe to apply** — they only change where generated markdown reports are written, not any production logic. However, per the user's constraint ("Do not modify api/, retrieval/, frontend/src/"), only the `scripts/` and `processing/` files would be touched.

**Awaiting user approval before applying path fixes.**

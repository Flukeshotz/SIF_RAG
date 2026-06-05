# Report Path Fix Report

Generated: 2026-06-06

## Summary

Updated 19 output path references across 12 scripts and 1 processing module. All changes are output-destination-only — no logic, content, API, retrieval, frontend, or deployment config was modified.

---

## Changes Applied

| # | File Modified | Old Output Path | New Output Path |
|---|---------------|-----------------|-----------------|
| 1 | `scripts/audit_chunks.py:53` | `docs/chunk_audit.md` | `docs/audits/chunk_audit.md` |
| 2 | `scripts/audit_chunks.py:92` | `docs/chunk_retrieval_simulation.md` | `docs/reports/chunk_retrieval_simulation.md` |
| 3 | `scripts/audit_chunks.py:120` | `docs/embedding_readiness.md` | `docs/reports/embedding_readiness.md` |
| 4 | `scripts/validate_phase6.py:15` | `docs/advisory_refusal_results.md` | `docs/reports/advisory_refusal_results.md` |
| 5 | `scripts/audit_chunk_distribution.py:39` | `docs/chunk_distribution_report.md` | `docs/reports/chunk_distribution_report.md` |
| 6 | `scripts/generate_registry_reports.py:41` | `docs/coverage_report.md` | `docs/reports/coverage_report.md` |
| 7 | `scripts/generate_registry_reports.py:49` | `docs/amc_coverage_report.md` | `docs/reports/amc_coverage_report.md` |
| 8 | `scripts/rationalize_corpus.py:86` | `docs/corpus_rationalization_report.md` | `docs/reports/corpus_rationalization_report.md` |
| 9 | `scripts/run_phase85_audits.py:11` | `docs/github_verification.md` | `docs/audits/github_verification.md` |
| 10 | `scripts/run_phase85_audits.py:20` | `docs/backend_deployment_report.md` | `docs/deployment/backend_deployment_report.md` |
| 11 | `scripts/run_phase85_audits.py:31` | `docs/frontend_deployment_report.md` | `docs/deployment/frontend_deployment_report.md` |
| 12 | `scripts/run_phase8_audits.py:10` | `docs/deployment_audit.md` | `docs/deployment/deployment_audit.md` |
| 13 | `scripts/run_phase8_audits.py:59` | `docs/frontend_qa_report.md` | `docs/deployment/frontend_qa_report.md` |
| 14 | `scripts/evaluate_comprehensive.py:133` | `docs/evaluation_report.md` | `docs/reports/evaluation_report.md` |
| 15 | `scripts/mvp_pdf_downloader.py:105` | `docs/direct_pdf_acquisition_report.md` | `docs/reports/direct_pdf_acquisition_report.md` |
| 16 | `scripts/certify_phase_3.py:69` | `docs/factsheet_sanitization_report.md` | `docs/reports/factsheet_sanitization_report.md` |
| 17 | `scripts/audit_phase_3.py:103` | `docs/duplicate_content_report.md` | `docs/reports/duplicate_content_report.md` |
| 18 | `scripts/audit_phase_3.py:156` | `docs/golden_coverage_report.md` | `docs/reports/golden_coverage_report.md` |
| 19 | `processing/sanitizer.py:51` | `docs/factsheet_sanitization_report.md` | `docs/reports/factsheet_sanitization_report.md` |

## Docstring Updates (cosmetic)

| File Modified | Old Docstring Path | New Docstring Path |
|---------------|--------------------|--------------------|
| `scripts/generate_repo_audit_and_dependency_map.py:4-5` | `docs/repository_audit.md`, `docs/dependency_map.md` | `docs/audits/repository_audit.md`, `docs/audits/dependency_map.md` |
| `scripts/generate_filtered_audit.py:20-21` | `docs/repository_audit_filtered.md`, `docs/dependency_map_filtered.md` | `docs/audits/repository_audit_filtered.md`, `docs/audits/dependency_map_filtered.md` |

## Output Path Updates in Audit Generators

| File Modified | Old Output Path | New Output Path |
|---------------|-----------------|-----------------|
| `scripts/generate_repo_audit_and_dependency_map.py:150` | `os.path.join(DOCS_DIR, "repository_audit.md")` | `os.path.join(DOCS_DIR, "audits", "repository_audit.md")` |
| `scripts/generate_repo_audit_and_dependency_map.py:186` | `os.path.join(DOCS_DIR, "dependency_map.md")` | `os.path.join(DOCS_DIR, "audits", "dependency_map.md")` |
| `scripts/generate_filtered_audit.py:147` | `os.path.join(DOCS_DIR, "repository_audit_filtered.md")` | `os.path.join(DOCS_DIR, "audits", "repository_audit_filtered.md")` |
| `scripts/generate_filtered_audit.py:174` | `os.path.join(DOCS_DIR, "dependency_map_filtered.md")` | `os.path.join(DOCS_DIR, "audits", "dependency_map_filtered.md")` |

---

## Files NOT Modified (confirmed out of scope)

- `api/` — untouched
- `retrieval/` — untouched
- `frontend/src/` — untouched
- `tests/` — untouched
- `.github/` — untouched
- `render.yaml` — untouched
- `vercel.json` — untouched
- `docker-compose.yml` — untouched
- `Dockerfile` — untouched
- `requirements.txt` — untouched
- `README.md` — untouched

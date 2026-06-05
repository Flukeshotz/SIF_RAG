# Broken References Report

Generated: 2026-06-06

This report lists every file in the repository that references a moved doc path using the old location.

---

## Scripts with Broken Output Paths

### `docs/chunk_audit.md`
→ referenced by: `scripts/audit_chunks.py:53`
→ new location: `docs/audits/chunk_audit.md`

### `docs/chunk_retrieval_simulation.md`
→ referenced by: `scripts/audit_chunks.py:92`
→ new location: `docs/reports/chunk_retrieval_simulation.md`

### `docs/embedding_readiness.md`
→ referenced by: `scripts/audit_chunks.py:120`
→ new location: `docs/reports/embedding_readiness.md`

### `docs/advisory_refusal_results.md`
→ referenced by: `scripts/validate_phase6.py:15`
→ new location: `docs/reports/advisory_refusal_results.md`

### `docs/chunk_distribution_report.md`
→ referenced by: `scripts/audit_chunk_distribution.py:39`
→ new location: `docs/reports/chunk_distribution_report.md`

### `docs/coverage_report.md`
→ referenced by: `scripts/generate_registry_reports.py:41`
→ new location: `docs/reports/coverage_report.md`

### `docs/amc_coverage_report.md`
→ referenced by: `scripts/generate_registry_reports.py:49`
→ new location: `docs/reports/amc_coverage_report.md`

### `docs/corpus_rationalization_report.md`
→ referenced by: `scripts/rationalize_corpus.py:86`
→ new location: `docs/reports/corpus_rationalization_report.md`

### `docs/github_verification.md`
→ referenced by: `scripts/run_phase85_audits.py:11`
→ new location: `docs/audits/github_verification.md`

### `docs/backend_deployment_report.md`
→ referenced by: `scripts/run_phase85_audits.py:20`
→ new location: `docs/deployment/backend_deployment_report.md`

### `docs/frontend_deployment_report.md`
→ referenced by: `scripts/run_phase85_audits.py:31`
→ new location: `docs/deployment/frontend_deployment_report.md`

### `docs/deployment_audit.md`
→ referenced by: `scripts/run_phase8_audits.py:10`
→ new location: `docs/deployment/deployment_audit.md`

### `docs/frontend_qa_report.md`
→ referenced by: `scripts/run_phase8_audits.py:59`
→ new location: `docs/deployment/frontend_qa_report.md`

### `docs/evaluation_report.md`
→ referenced by: `scripts/evaluate_comprehensive.py:133`
→ new location: `docs/reports/evaluation_report.md`

### `docs/direct_pdf_acquisition_report.md`
→ referenced by: `scripts/mvp_pdf_downloader.py:105`
→ new location: `docs/reports/direct_pdf_acquisition_report.md`

### `docs/factsheet_sanitization_report.md`
→ referenced by: `scripts/certify_phase_3.py:69`, `processing/sanitizer.py:51`
→ new location: `docs/reports/factsheet_sanitization_report.md`

### `docs/duplicate_content_report.md`
→ referenced by: `scripts/audit_phase_3.py:103`
→ new location: `docs/reports/duplicate_content_report.md`

### `docs/golden_coverage_report.md`
→ referenced by: `scripts/audit_phase_3.py:156`
→ new location: `docs/reports/golden_coverage_report.md`

---

## Audit Generator Docstrings (cosmetic only)

### `docs/repository_audit.md` / `docs/dependency_map.md`
→ referenced by: `scripts/generate_repo_audit_and_dependency_map.py:4-5` (docstring)
→ new locations: `docs/audits/repository_audit.md`, `docs/audits/dependency_map.md`

### `docs/repository_audit_filtered.md` / `docs/dependency_map_filtered.md`
→ referenced by: `scripts/generate_filtered_audit.py:20-21` (docstring)
→ new locations: `docs/audits/repository_audit_filtered.md`, `docs/audits/dependency_map_filtered.md`

---

## Stale Listings in Old Audit

`docs/audits/repository_audit.md` (the unfiltered audit) contains ~20 lines listing old `docs/<filename>` paths in its "Generated Artifacts" section. This is **cosmetic** — the audit file itself is a snapshot and does not drive any automation.

---

## Files with ZERO Broken References

The following moved files had no references anywhere in the codebase:

- `docs/accessibility_report.md`
- `docs/acquisition_hardening_report.md`
- `docs/amc_coverage_report.md` (only in old audit listing)
- `docs/backend_deployment_report.md` (only in old audit listing)
- `docs/corpus_expansion_report.md`
- `docs/corpus_coverage_audit.md`
- `docs/critical_issues.md` (only in old audit listing)
- `docs/deployment_blockers.md`
- `docs/deployment_checklist.md`
- `docs/deployment_fix_report.md` (only in old audit listing)
- `docs/deployment_readiness_report.md` (only in old audit listing)
- `docs/deployment_reality_audit.md` (only in old audit listing)
- `docs/deployment_verification.md`
- `docs/implementation_plan.md`
- `docs/research_findings.md`
- `docs/stitch_ui_prompt.md`
- `docs/dependency_map.md` (only in audit generator docstring)
- `docs/dependency_map_filtered.md` (only in audit generator docstring)
- `docs/repository_audit.md` (only in audit generator docstring)
- `docs/repository_audit_filtered.md` (only in audit generator docstring)

---

## Status

- **Functional broken references:** 19 (all in `scripts/` and `processing/sanitizer.py`)
- **Cosmetic broken references:** 4 (docstrings in audit generators) + ~20 (stale listings in old audit)
- **Production code broken references:** 0
- **CI broken references:** 0
- **Frontend broken references:** 0
- **Test broken references:** 0

**No fixes have been applied. Awaiting user approval.**

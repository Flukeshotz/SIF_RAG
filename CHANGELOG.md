# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-04

### Added
- **Core RAG Engine:** Initial implementation of the Hybrid Imperative Retrieval pipeline.
- **Data Ingestion:** Support for SEBI Master Circulars, ISIDs, and Factsheets.
- **Frontend Workspace:** React SPA with Evidence Explorer and dynamic citation hover previews.
- **Presentation Modes:** "Demo Mode" and "Presentation Mode" toggles for recruiter showcasing.
- **Analytics:** Basic JSONL query telemetry and Insights Dashboard.
- **Containerization:** Docker support for seamless local deployment.

### Security
- Replaced all hardcoded localhost URLs with environment variables.
- Added strict Pydantic validation for `GROQ_API_KEY` on startup.

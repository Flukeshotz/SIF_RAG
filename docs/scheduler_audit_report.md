# SIF Copilot — Scheduler Audit & Implementation Report

## 1. Initial Audit

### Verify Scheduler Implementation
1. **Is APScheduler, Celery, or cron implemented?** No. The codebase lacked any asynchronous job queue or cron scheduler.
2. **Does a daily refresh job exist?** No.
3. **What file runs the refresh?** None. `ingestion/run.py` existed but was entirely manual.
4. **What documents are refreshed?** The entire active source registry.
5. **What happens on failure?** Errors were logged to `ingestion_report.json`, but no retry mechanism existed.
6. **Is the scheduler running locally or production?** Neither. The `GET /scheduler/status` endpoint in `api/main.py` was returning hardcoded mock data.

---

## 2. Implementation

To resolve the missing functionality, a production-safe APScheduler has been integrated.

### Files Created:
1. **`jobs/refresh_corpus.py`**: A synchronous wrapper to trigger the asyncio `run_ingestion` pipeline.
2. **`jobs/scheduler.py`**: Initializes an `APScheduler.BackgroundScheduler` that schedules the refresh job daily at 02:00 AM UTC.

### API Integration
- Hooked `start_scheduler()` into the FastAPI startup lifespan in `api/main.py`.
- Replaced the mock `GET /scheduler/status` endpoint with real data querying the APScheduler job store.

### Conclusion
The application now autonomously syncs SEBI and AMC documents nightly, closing the loop on the "always-up-to-date" product requirement without requiring an external Airflow cluster.

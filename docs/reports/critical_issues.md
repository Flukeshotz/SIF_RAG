# SIF Copilot — Critical Issues Log

*The following items scored below 90 in the Launch Readiness Audit and must be documented for future remediation.*

### 1. Missing Global Legal Disclaimer (Compliance Issue)
**Severity: High**
- **Issue:** While the backend LLM is prompted to refuse advisory queries, the frontend UI lacks a persistent, explicitly visible disclaimer stating that the tool is for research purposes only and does not constitute financial advice.
- **Remediation:** Add a permanent, low-profile banner to the bottom of the `SideNavBar` or `ChatArea` empty state.

### 2. Ephemeral Analytics Storage (Architecture Issue)
**Severity: Medium**
- **Issue:** Query telemetry is currently appended to `data/analytics.jsonl`. In a containerized production environment (like Docker on Render or AWS ECS), this file will be wiped every time the container restarts unless a persistent volume is attached.
- **Remediation:** Migrate analytics logging to a lightweight relational database (SQLite/PostgreSQL) or a managed logging service.

### 3. Hardcoded API URLs (Deployment Issue)
**Severity: Medium**
- **Issue:** The frontend `api.ts` hardcodes the backend URL to `http://localhost:8000`. This will break when deployed to Vercel.
- **Remediation:** Replace with an environment variable (`import.meta.env.VITE_API_URL`) before running the final production build.

### 4. Rate Limit Graceful Degradation (UX Issue)
**Severity: Low**
- **Issue:** If Groq API rate limits are hit, the frontend simply displays a generic "Error connecting to the AI Research Engine" message.
- **Remediation:** Add specific error catching for 429 status codes to inform the user to try again in a few seconds.

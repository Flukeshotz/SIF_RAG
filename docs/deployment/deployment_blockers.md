# Deployment Blockers

| ID | Issue | Severity | Root Cause | Fix | Estimated Effort |
|---|---|---|---|---|---|
| 1 | Overly Permissive CORS | High | `api/main.py` currently allows `origins=["*"]` from the MVP phase. | Restrict `allow_origins` to the specific Vercel production domain using an environment variable (e.g., `FRONTEND_URL`). | 5 mins |
| 2 | Unauthenticated Git Push | High | The local git repository lacks GitHub credentials (PAT or SSH key). | Authenticate the terminal with a Personal Access Token or SSH key to complete the push to `Flukeshotz/SIF_RAG`. | 5 mins |
| 3 | Missing Render Secrets | High | The `GROQ_API_KEY` is not checked into git (intentionally). | Before triggering the Render deployment, navigate to the Render dashboard and manually inject the `GROQ_API_KEY` secret. | 5 mins |

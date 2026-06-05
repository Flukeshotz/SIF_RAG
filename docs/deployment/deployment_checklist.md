# SIF Copilot — Deployment Checklist

Before executing Phase 8 (Deployment), verify the following checks have passed.

## Backend (FastAPI / Qdrant)
- [x] Python dependencies frozen in `requirements.txt`.
- [x] CORS middleware is configured appropriately (currently `["*"]` for dev, must tighten for production).
- [ ] `GROQ_API_KEY` is securely injected via platform secrets (e.g., Render Environment Variables, AWS Secrets Manager).
- [ ] Qdrant is configured to persist data to disk in the production container (or migrated to Qdrant Cloud).
- [x] Basic error handling is in place for LLM timeouts.
- [ ] File I/O paths (e.g., `data/analytics.jsonl`) are pointing to persistent volumes, not ephemeral container storage.

## Frontend (React / Vite)
- [x] `npm run build` completes successfully with zero TypeScript errors.
- [x] Bundle size is optimized via `React.lazy()`.
- [x] `API_BASE_URL` in `src/api.ts` is parameterized to switch between `localhost:8000` and the production backend URL (e.g., `import.meta.env.VITE_API_URL`).
- [x] Accessibility sweeps (contrast, focus-rings) pass.

## Content & Compliance
- [x] Demo mode payloads are thoroughly verified for accuracy.
- [ ] UI-level "Not Financial Advice" disclaimer is visible on the main page.

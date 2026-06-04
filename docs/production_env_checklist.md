# SIF Copilot — Production Environment Checklist

Before triggering the deployment pipelines, verify the following secrets and environment variables are injected into your respective hosting dashboards.

## 1. Vercel (Frontend)
Navigate to the Vercel Dashboard -> Project Settings -> Environment Variables.

| Variable | Required | Production Example Value |
|---|---|---|
| `VITE_API_URL` | Yes | `https://sif-backend.onrender.com` |

## 2. Render (Backend)
Navigate to the Render Dashboard -> Web Service Settings -> Environment.

| Variable | Required | Production Example Value |
|---|---|---|
| `ENVIRONMENT` | Yes | `production` |
| `GROQ_API_KEY` | Yes | `gsk_abc123...` (Keep Secret!) |
| `ALLOWED_ORIGINS` | Yes | `https://sif-frontend.vercel.app` |
| `QDRANT_PATH` | Yes | `/app/data/qdrant` |
| `QDRANT_URL` | No | *(Leave blank if using local disk)* |

## 3. Security Checks
- [ ] Ensure `GROQ_API_KEY` is NOT hardcoded anywhere in the codebase.
- [ ] Ensure `.env` is NOT committed to Git.
- [ ] Verify `ALLOWED_ORIGINS` exactly matches your Vercel URL (do not include trailing slashes).

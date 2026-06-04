# SIF Copilot — Deployment Guide

## Prerequisites
- Node.js (v18+)
- Python (3.10+)
- A valid Groq API Key (`GROQ_API_KEY`)

## Local Development Deployment

### 1. Start the FastAPI Backend
The backend serves the core RAG engine, vector database connections, and LLM synthesis.

```bash
# From the root directory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start the API server
python -m api.main
```
The API will be available at `http://localhost:8000`.

### 2. Start the React Frontend
The frontend provides the conversational workspace and Evidence Explorer.

```bash
# In a new terminal window
cd frontend
npm install
npm run dev
```
The UI will be available at `http://localhost:5173`.

---

## Production Deployment Architecture (Future)
When migrating from MVP to Production:

1. **Frontend:** Deploy the Vite built static assets (`npm run build`) via Vercel, AWS S3+CloudFront, or Nginx.
2. **Backend:** Deploy the FastAPI application using Docker to AWS ECS or Render. Run behind a load balancer (e.g., ALB) with multiple workers via `gunicorn -k uvicorn.workers.UvicornWorker`.
3. **Database:** Migrate Qdrant from local file mode to a dedicated Qdrant Cloud cluster.
4. **Environment Variables:** Ensure `GROQ_API_KEY` is securely injected via AWS Secrets Manager or equivalent.

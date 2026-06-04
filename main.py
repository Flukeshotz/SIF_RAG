from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from core.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Application startup and shutdown lifecycle."""
    logger.info(f"Starting SIF Copilot API in {settings.ENVIRONMENT} mode")
    yield
    logger.info("Shutting down SIF Copilot API")


app = FastAPI(
    title="SIF Copilot API",
    description="Backend API for the SIF Copilot Wealth Research Assistant",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    """Health check endpoint. Returns 200 with environment info."""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

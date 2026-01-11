import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .logging_config import setup_logging
from .routers import predictions

settings = get_settings()

# Initialize logging before anything else
setup_logging(
    log_dir=Path(settings.log_dir),
    log_level=getattr(logging, settings.log_level.upper(), logging.INFO),
)

logger = logging.getLogger("varinaut.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s", settings.app_name)
    # Database schema is managed by Alembic migrations
    yield
    # Shutdown: cleanup if needed
    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predictions.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

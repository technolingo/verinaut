from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import predictions

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Database schema is managed by Alembic migrations
    yield
    # Shutdown: cleanup if needed


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

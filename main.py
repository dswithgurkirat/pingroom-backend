"""
PingRoom - Real-time Chat SaaS Backend
Entry point for the FastAPI application.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.routes import auth, rooms, messages, stickers, payments, webhooks

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("🚀 PingRoom API starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    yield
    logger.info("👋 PingRoom API shutting down...")


app = FastAPI(
    title="PingRoom API",
    description="Production-ready real-time chat SaaS backend with Supabase & Stripe",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router,      prefix="/api/v1/auth",     tags=["Auth"])
app.include_router(rooms.router,     prefix="/api/v1/rooms",    tags=["Rooms"])
app.include_router(messages.router,  prefix="/api/v1/messages", tags=["Messages"])
app.include_router(stickers.router,  prefix="/api/v1/stickers", tags=["Stickers"])
app.include_router(payments.router,  prefix="/api/v1/payments", tags=["Payments"])
app.include_router(webhooks.router,  prefix="/api/v1/webhooks", tags=["Webhooks"])


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "service": "PingRoom API", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

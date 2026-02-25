"""
MyTake - FastAPI Application Entry Point
A personal content digestion tool that turns links into understanding and re-expression.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.api import process, health, analytics
from app.storage.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    await init_db()
    yield


app = FastAPI(
    title="MyTake",
    description="A personal content digestion tool that turns links into understanding and re-expression — in your voice.",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(process.router, prefix="/api", tags=["process"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "MyTake",
        "description": "A personal content digestion tool",
        "version": "0.1.0",
        "status": "running"
    }

"""
Health check endpoints.
"""

from fastapi import APIRouter
from app.ai.claude import claude_client

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "service": "MyTake API"
    }


@router.get("/health/ai")
async def ai_health_check():
    """Check if Claude AI is accessible."""
    try:
        is_ready = claude_client.test_connection()
        return {
            "status": "healthy" if is_ready else "unhealthy",
            "service": "Claude AI",
            "ready": is_ready
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "Claude AI",
            "error": str(e)
        }

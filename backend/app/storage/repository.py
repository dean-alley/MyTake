"""
Repository layer for database operations.
"""

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.storage.models import Content, VoiceFeedback
from typing import List, Optional


class ContentRepository:
    """Repository for Content operations."""

    @staticmethod
    async def create(session: AsyncSession, content_data: dict) -> Content:
        """Create new content entry."""
        content = Content(**content_data)
        session.add(content)
        await session.flush()
        await session.refresh(content)
        return content

    @staticmethod
    async def get_by_id(session: AsyncSession, content_id: int) -> Optional[Content]:
        """Get content by ID."""
        result = await session.execute(
            select(Content).where(Content.id == content_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(session: AsyncSession, limit: int = 100) -> List[Content]:
        """Get all content entries."""
        result = await session.execute(
            select(Content).order_by(desc(Content.created_at)).limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def update(session: AsyncSession, content_id: int, updates: dict) -> Optional[Content]:
        """Update content entry."""
        content = await ContentRepository.get_by_id(session, content_id)
        if content:
            for key, value in updates.items():
                setattr(content, key, value)
            await session.flush()
            await session.refresh(content)
        return content


class VoiceFeedbackRepository:
    """Repository for VoiceFeedback operations."""

    @staticmethod
    async def create(session: AsyncSession, feedback_data: dict) -> VoiceFeedback:
        """Create new feedback entry."""
        feedback = VoiceFeedback(**feedback_data)
        session.add(feedback)
        await session.flush()
        await session.refresh(feedback)
        return feedback

    @staticmethod
    async def get_by_content_id(session: AsyncSession, content_id: int) -> List[VoiceFeedback]:
        """Get all feedback for a content item."""
        result = await session.execute(
            select(VoiceFeedback).where(VoiceFeedback.content_id == content_id)
        )
        return result.scalars().all()

    @staticmethod
    async def get_positive_feedback(session: AsyncSession, limit: int = 50) -> List[VoiceFeedback]:
        """Get positive feedback for voice profile learning."""
        result = await session.execute(
            select(VoiceFeedback)
            .where(VoiceFeedback.sounds_like_me == 1)
            .order_by(desc(VoiceFeedback.created_at))
            .limit(limit)
        )
        return result.scalars().all()

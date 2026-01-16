"""
SQLAlchemy models for MyTake.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Content(Base):
    """Content model for storing processed content."""

    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=True, index=True)
    source_type = Column(String, nullable=False)  # youtube, tiktok, text
    title = Column(String, nullable=True)
    original_text = Column(Text, nullable=False)

    # Generated outputs (4-part schema)
    what_they_said_deep = Column(Text)
    what_they_said_simple = Column(Text)
    what_i_say_simple = Column(Text)
    what_i_say_deep = Column(Text)

    # Metadata
    markdown_path = Column(String)
    google_doc_url = Column(String, nullable=True)
    voice_profile_version = Column(String)
    processing_time_seconds = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "url": self.url,
            "source_type": self.source_type,
            "title": self.title,
            "original_text": self.original_text,
            "what_they_said_deep": self.what_they_said_deep,
            "what_they_said_simple": self.what_they_said_simple,
            "what_i_say_simple": self.what_i_say_simple,
            "what_i_say_deep": self.what_i_say_deep,
            "markdown_path": self.markdown_path,
            "google_doc_url": self.google_doc_url,
            "voice_profile_version": self.voice_profile_version,
            "processing_time_seconds": self.processing_time_seconds,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class VoiceFeedback(Base):
    """Store user feedback on voice accuracy."""

    __tablename__ = "voice_feedback"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, index=True)
    section = Column(String)  # which section: what_i_say_simple or what_i_say_deep
    sounds_like_me = Column(Integer)  # 1 for yes, 0 for no
    feedback_text = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "content_id": self.content_id,
            "section": self.section,
            "sounds_like_me": self.sounds_like_me,
            "feedback_text": self.feedback_text,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

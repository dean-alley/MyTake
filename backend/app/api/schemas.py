"""
Pydantic schemas for API requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProcessRequest(BaseModel):
    """Request to process content."""
    input_data: str = Field(..., description="URL or text content to process")
    source_type: str = Field(default="auto", description="Source type: auto, youtube, tiktok, or text")


class ProcessResponse(BaseModel):
    """Response from content processing."""
    id: int
    title: str
    url: Optional[str]
    source_type: str
    what_they_said_deep: str
    what_they_said_simple: str
    what_i_say_simple: str
    what_i_say_deep: str
    markdown_path: str
    processing_time_seconds: float
    created_at: datetime


class ContentResponse(BaseModel):
    """Response for content retrieval."""
    id: int
    title: str
    url: Optional[str]
    source_type: str
    what_they_said_deep: str
    what_they_said_simple: str
    what_i_say_simple: str
    what_i_say_deep: str
    markdown_path: Optional[str]
    google_doc_url: Optional[str]
    processing_time_seconds: Optional[float]
    created_at: datetime
    updated_at: datetime


class FeedbackRequest(BaseModel):
    """Request to submit voice feedback."""
    content_id: int
    section: str = Field(..., description="Section name: what_i_say_simple or what_i_say_deep")
    sounds_like_me: bool = Field(..., description="True if it sounds like the user")
    feedback_text: Optional[str] = Field(None, description="Optional text feedback")


class FeedbackResponse(BaseModel):
    """Response after submitting feedback."""
    id: int
    content_id: int
    section: str
    sounds_like_me: bool
    feedback_text: Optional[str]
    created_at: datetime

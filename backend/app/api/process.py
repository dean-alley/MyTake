"""
Content processing API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.schemas import (
    ProcessRequest, ProcessResponse,
    ContentResponse, FeedbackRequest, FeedbackResponse
)
from app.storage.database import get_db
from app.storage.repository import ContentRepository, VoiceFeedbackRepository
from app.storage.markdown import MarkdownGenerator
from app.extractors.content import ContentExtractor
from app.ai.claude import claude_client
from app.voice.profile import voice_profile

router = APIRouter()


@router.post("/process", response_model=ProcessResponse)
async def process_content(
    request: ProcessRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Process content (URL or text) and generate MyTake analysis.

    This is the core endpoint that:
    1. Extracts content from URL or accepts text
    2. Generates 4-part analysis with Claude
    3. Saves to database
    4. Creates markdown file
    """
    try:
        # Step 1: Extract content
        extractor = ContentExtractor()
        extracted = extractor.extract(request.input_data, request.source_type)

        # Step 2: Generate analysis with Claude
        analysis = claude_client.generate_four_part_analysis(
            content_text=extracted["text"],
            title=extracted.get("title", "Untitled"),
            source_type=extracted["source_type"]
        )

        # Step 3: Save to database
        content_data = {
            "url": extracted.get("url"),
            "source_type": extracted["source_type"],
            "title": extracted.get("title", "Untitled"),
            "original_text": extracted["text"],
            "what_they_said_deep": analysis["what_they_said_deep"],
            "what_they_said_simple": analysis["what_they_said_simple"],
            "what_i_say_simple": analysis["what_i_say_simple"],
            "what_i_say_deep": analysis["what_i_say_deep"],
            "voice_profile_version": analysis["voice_profile_version"],
            "processing_time_seconds": analysis["processing_time_seconds"],
        }

        content = await ContentRepository.create(db, content_data)
        await db.commit()
        await db.refresh(content)

        # Step 4: Generate and save markdown
        markdown_path = MarkdownGenerator.create_and_save({
            **content.to_dict()
        })

        # Update content with markdown path
        await ContentRepository.update(db, content.id, {"markdown_path": markdown_path})
        await db.commit()
        await db.refresh(content)

        return ProcessResponse(
            id=content.id,
            title=content.title,
            url=content.url,
            source_type=content.source_type,
            what_they_said_deep=content.what_they_said_deep,
            what_they_said_simple=content.what_they_said_simple,
            what_i_say_simple=content.what_i_say_simple,
            what_i_say_deep=content.what_i_say_deep,
            markdown_path=content.markdown_path,
            processing_time_seconds=content.processing_time_seconds,
            created_at=content.created_at
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.get("/content", response_model=List[ContentResponse])
async def get_all_content(
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all processed content."""
    content_list = await ContentRepository.get_all(db, limit=limit)
    return [ContentResponse(**content.to_dict()) for content in content_list]


@router.get("/content/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get specific content by ID."""
    content = await ContentRepository.get_by_id(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return ContentResponse(**content.to_dict())


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    request: FeedbackRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit feedback on voice accuracy.

    This helps the voice profile learn and improve over time.
    """
    # Verify content exists
    content = await ContentRepository.get_by_id(db, request.content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Validate section
    valid_sections = ["what_i_say_simple", "what_i_say_deep"]
    if request.section not in valid_sections:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid section. Must be one of: {valid_sections}"
        )

    # Save feedback
    feedback_data = {
        "content_id": request.content_id,
        "section": request.section,
        "sounds_like_me": 1 if request.sounds_like_me else 0,
        "feedback_text": request.feedback_text
    }

    feedback = await VoiceFeedbackRepository.create(db, feedback_data)
    await db.commit()

    # Update voice profile
    voice_profile.update_from_feedback({
        "content_id": request.content_id,
        "section": request.section,
        "sounds_like_me": request.sounds_like_me,
        "feedback_text": request.feedback_text
    })

    return FeedbackResponse(
        id=feedback.id,
        content_id=feedback.content_id,
        section=feedback.section,
        sounds_like_me=bool(feedback.sounds_like_me),
        feedback_text=feedback.feedback_text,
        created_at=feedback.created_at
    )

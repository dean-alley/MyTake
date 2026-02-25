"""
Analytics API endpoints for MyTake.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List

from app.storage.database import get_db
from app.storage.repository import ContentRepository, VoiceFeedbackRepository

router = APIRouter()


@router.get("/analytics/overview")
async def get_analytics_overview(db: AsyncSession = Depends(get_db)) -> Dict:
    """Overview stats: totals, processing times, type distribution, feedback."""
    all_content = await ContentRepository.get_all(db, limit=10000)

    if not all_content:
        return {"total_items": 0, "message": "No content processed yet"}

    processing_times = [
        c.processing_time_seconds for c in all_content
        if c.processing_time_seconds is not None
    ]
    avg_time = sum(processing_times) / len(processing_times) if processing_times else 0

    type_distribution: Dict[str, int] = {}
    for c in all_content:
        type_distribution[c.source_type] = type_distribution.get(c.source_type, 0) + 1

    all_feedback = []
    for c in all_content:
        all_feedback.extend(await VoiceFeedbackRepository.get_by_content_id(db, c.id))

    positive = sum(1 for f in all_feedback if f.sounds_like_me == 1)

    recent_items = [
        {
            "id": c.id,
            "title": c.title[:60] + "..." if len(c.title) > 60 else c.title,
            "source_type": c.source_type,
            "created_at": c.created_at.isoformat(),
            "processing_time_seconds": round(c.processing_time_seconds or 0, 2),
        }
        for c in sorted(all_content, key=lambda x: x.created_at, reverse=True)[:5]
    ]

    return {
        "total_items": len(all_content),
        "processing_stats": {
            "average_time_seconds": round(avg_time, 2),
            "min_time_seconds": round(min(processing_times, default=0), 2),
            "max_time_seconds": round(max(processing_times, default=0), 2),
        },
        "content_type_distribution": type_distribution,
        "voice_feedback": {
            "total": len(all_feedback),
            "positive": positive,
            "negative": len(all_feedback) - positive,
            "accuracy_percentage": round(positive / len(all_feedback) * 100, 1) if all_feedback else None,
        },
        "recent_items": recent_items,
    }


@router.get("/analytics/timeline")
async def get_timeline(days: int = 30, db: AsyncSession = Depends(get_db)) -> List[Dict]:
    """Content processed per day over the last N days."""
    all_content = await ContentRepository.get_all(db, limit=10000)

    daily: Dict[str, Dict] = {}
    for c in all_content:
        key = c.created_at.date().isoformat()
        if key not in daily:
            daily[key] = {"date": key, "items_processed": 0, "by_type": {}}
        daily[key]["items_processed"] += 1
        daily[key]["by_type"][c.source_type] = daily[key]["by_type"].get(c.source_type, 0) + 1

    return sorted(daily.values(), key=lambda x: x["date"], reverse=True)[:days]


@router.get("/analytics/voice-performance")
async def get_voice_performance(db: AsyncSession = Depends(get_db)) -> Dict:
    """Accuracy of voice generation broken down by section."""
    all_content = await ContentRepository.get_all(db, limit=10000)

    all_feedback = []
    for c in all_content:
        all_feedback.extend(await VoiceFeedbackRepository.get_by_content_id(db, c.id))

    if not all_feedback:
        return {"message": "No voice feedback yet", "feedback_count": 0}

    section_stats: Dict[str, Dict] = {}
    for f in all_feedback:
        s = f.section
        if s not in section_stats:
            section_stats[s] = {"total": 0, "positive": 0}
        section_stats[s]["total"] += 1
        if f.sounds_like_me == 1:
            section_stats[s]["positive"] += 1

    for s, stats in section_stats.items():
        stats["accuracy_percentage"] = round(stats["positive"] / stats["total"] * 100, 1)

    positive = sum(1 for f in all_feedback if f.sounds_like_me == 1)

    return {
        "total_feedback": len(all_feedback),
        "overall_accuracy_percentage": round(positive / len(all_feedback) * 100, 1),
        "section_performance": section_stats,
    }


@router.get("/analytics/content-insights")
async def get_content_insights(db: AsyncSession = Depends(get_db)) -> Dict:
    """Word counts and output length distributions."""
    all_content = await ContentRepository.get_all(db, limit=10000)

    if not all_content:
        return {"message": "No content processed yet"}

    input_words = [len(c.original_text.split()) for c in all_content]

    output_words = {
        "what_they_said_deep": [len(c.what_they_said_deep.split()) for c in all_content],
        "what_they_said_simple": [len(c.what_they_said_simple.split()) for c in all_content],
        "what_i_say_simple": [len(c.what_i_say_simple.split()) for c in all_content],
        "what_i_say_deep": [len(c.what_i_say_deep.split()) for c in all_content],
    }

    def avg(lst):
        return round(sum(lst) / len(lst), 1) if lst else 0

    # Simple keyword frequency (exclude stopwords)
    stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
                 "for", "of", "with", "it", "is", "that", "this", "was", "has"}
    all_words = " ".join(c.title for c in all_content).lower().split()
    freq: Dict[str, int] = {}
    for w in all_words:
        if w not in stopwords and len(w) > 3:
            freq[w] = freq.get(w, 0) + 1
    top_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "total_items": len(all_content),
        "input_word_stats": {
            "average": avg(input_words),
            "min": min(input_words),
            "max": max(input_words),
        },
        "average_output_words": {k: avg(v) for k, v in output_words.items()},
        "top_keywords": [{"word": w, "count": c} for w, c in top_keywords],
    }


@router.get("/analytics/search")
async def search_content(
    q: str,
    db: AsyncSession = Depends(get_db)
) -> List[Dict]:
    """Simple full-text search across titles and outputs."""
    all_content = await ContentRepository.get_all(db, limit=10000)
    query = q.lower()

    results = []
    for c in all_content:
        searchable = " ".join([
            c.title or "",
            c.original_text or "",
            c.what_they_said_simple or "",
            c.what_i_say_simple or "",
        ]).lower()

        if query in searchable:
            results.append({
                "id": c.id,
                "title": c.title[:80] + "..." if len(c.title) > 80 else c.title,
                "source_type": c.source_type,
                "created_at": c.created_at.isoformat(),
                "snippet": _extract_snippet(c.what_i_say_simple or "", query),
            })

    return results


def _extract_snippet(text: str, query: str, window: int = 120) -> str:
    """Extract a snippet of text around the first match."""
    idx = text.lower().find(query)
    if idx == -1:
        return text[:window] + "..."
    start = max(0, idx - 40)
    end = min(len(text), start + window)
    snippet = text[start:end]
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    return snippet

"""
Unified content extractor for all source types.
"""

from typing import Dict
from app.extractors.youtube import YouTubeExtractor
from app.extractors.tiktok import TikTokExtractor


class ContentExtractor:
    """Unified interface for extracting content from various sources."""

    def __init__(self):
        self.youtube = YouTubeExtractor()
        self.tiktok = TikTokExtractor()

    def extract(self, input_data: str, source_type: str = "auto") -> Dict:
        """
        Extract content from URL or text.

        Args:
            input_data: URL or raw text
            source_type: "auto", "youtube", "tiktok", or "text"

        Returns:
            Dict with extracted content
        """
        # Auto-detect source type if not specified
        if source_type == "auto":
            source_type = self._detect_source_type(input_data)

        if source_type == "youtube":
            return self.youtube.get_transcript(input_data)
        elif source_type == "tiktok":
            return self.tiktok.get_content(input_data)
        elif source_type == "text":
            return {
                "text": input_data,
                "title": input_data[:100] + "..." if len(input_data) > 100 else input_data,
                "url": None,
                "source_type": "text"
            }
        else:
            raise ValueError(f"Unknown source type: {source_type}")

    def _detect_source_type(self, input_data: str) -> str:
        """Detect source type from input."""
        # Check if it's a URL
        if input_data.startswith(('http://', 'https://')):
            if self.youtube.is_youtube_url(input_data):
                return "youtube"
            elif self.tiktok.is_tiktok_url(input_data):
                return "tiktok"
            else:
                raise ValueError(f"Unsupported URL type: {input_data}")
        else:
            # Treat as raw text
            return "text"

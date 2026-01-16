"""
YouTube transcript extractor.
"""

from youtube_transcript_api import YouTubeTranscriptApi
from typing import Dict, Optional
import re


class YouTubeExtractor:
    """Extract transcripts from YouTube videos."""

    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats."""
        patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&]+)',
            r'(?:https?://)?(?:www\.)?youtu\.be/([^?]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([^?]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/v/([^?]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    @staticmethod
    def get_transcript(url: str) -> Dict:
        """
        Get transcript from YouTube URL.

        Returns:
            Dict with 'text', 'title', and 'video_id'
        """
        video_id = YouTubeExtractor.extract_video_id(url)

        if not video_id:
            raise ValueError(f"Could not extract video ID from URL: {url}")

        try:
            # Get transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

            # Combine all text segments
            full_text = " ".join([entry['text'] for entry in transcript_list])

            # Try to get video title (basic approach)
            title = f"YouTube Video {video_id}"

            return {
                "text": full_text,
                "title": title,
                "video_id": video_id,
                "url": url,
                "source_type": "youtube"
            }

        except Exception as e:
            raise ValueError(f"Failed to get transcript for video {video_id}: {str(e)}")

    @staticmethod
    def is_youtube_url(url: str) -> bool:
        """Check if URL is a YouTube URL."""
        youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'www.youtu.be']
        return any(domain in url.lower() for domain in youtube_domains)

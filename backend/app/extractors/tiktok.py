"""
TikTok content extractor using Apify.
"""

from apify_client import ApifyClient
from typing import Dict, Optional
import re
from app.config import settings


class TikTokExtractor:
    """Extract content from TikTok videos using Apify."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.apify_api_key
        if self.api_key:
            self.client = ApifyClient(self.api_key)
        else:
            self.client = None

    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Extract video ID from TikTok URL."""
        patterns = [
            r'(?:https?://)?(?:www\.)?tiktok\.com/@[^/]+/video/(\d+)',
            r'(?:https?://)?(?:vm\.tiktok\.com|vt\.tiktok\.com)/([A-Za-z0-9]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    def get_content(self, url: str) -> Dict:
        """
        Get content from TikTok URL using Apify.

        Returns:
            Dict with 'text', 'title', and other metadata
        """
        if not self.client:
            raise ValueError("Apify API key not configured. Please set APIFY_API_KEY in .env")

        video_id = self.extract_video_id(url)

        try:
            # Run the Apify TikTok scraper actor
            # Note: You may need to adjust the actor ID based on the specific Apify actor you're using
            run_input = {
                "postURLs": [url],
                "resultsPerPage": 1,
            }

            # This is a placeholder actor ID - replace with actual TikTok scraper actor
            # Common options: "clockworks/tiktok-scraper" or similar
            actor_id = "clockworks/free-tiktok-scraper"

            run = self.client.actor(actor_id).call(run_input=run_input)

            # Fetch results from dataset
            items = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())

            if not items:
                raise ValueError(f"No content found for TikTok URL: {url}")

            item = items[0]

            # Extract text from description and combine with any available transcript
            text = item.get('text', '') or item.get('description', '')
            title = text[:100] if text else f"TikTok Video {video_id}"

            return {
                "text": text,
                "title": title,
                "video_id": video_id or "unknown",
                "url": url,
                "source_type": "tiktok",
                "metadata": {
                    "author": item.get('authorMeta', {}).get('name'),
                    "likes": item.get('diggCount'),
                    "shares": item.get('shareCount'),
                    "comments": item.get('commentCount'),
                }
            }

        except Exception as e:
            raise ValueError(f"Failed to get TikTok content: {str(e)}")

    @staticmethod
    def is_tiktok_url(url: str) -> bool:
        """Check if URL is a TikTok URL."""
        tiktok_domains = ['tiktok.com', 'www.tiktok.com', 'vm.tiktok.com', 'vt.tiktok.com']
        return any(domain in url.lower() for domain in tiktok_domains)

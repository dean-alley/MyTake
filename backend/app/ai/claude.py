"""
Claude AI client for content generation.
"""

from anthropic import Anthropic
from typing import Dict
import time
from app.config import settings
from app.ai.prompts import create_system_prompt, create_user_prompt, parse_claude_response
from app.voice.profile import voice_profile


class ClaudeClient:
    """Client for interacting with Claude AI."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.anthropic_api_key

        if not self.api_key:
            raise ValueError("Anthropic API key not configured. Please set ANTHROPIC_API_KEY in .env")
        self.client = Anthropic(api_key=self.api_key)
        self.model = settings.claude_model
        self.max_tokens = settings.claude_max_tokens

    def generate_four_part_analysis(
        self,
        content_text: str,
        title: str = "Untitled",
        source_type: str = "content"
    ) -> Dict[str, str]:
        """
        Generate the 4-part MyTake analysis.

        Args:
            content_text: The content to analyze
            title: Title of the content
            source_type: Source type (youtube, tiktok, text)

        Returns:
            Dict with the 4 sections and metadata
        """
        start_time = time.time()

        # Get voice profile context
        voice_context = voice_profile.get_prompt_context()

        # Create prompts
        system_prompt = create_system_prompt(voice_context)
        user_prompt = create_user_prompt(content_text, title, source_type)

        # Call Claude
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )

            response_text = message.content[0].text

            # Parse response into sections
            sections = parse_claude_response(response_text)

            # Calculate processing time
            processing_time = time.time() - start_time

            return {
                **sections,
                "processing_time_seconds": processing_time,
                "voice_profile_version": voice_profile.get_version(),
                "model_used": self.model
            }

        except Exception as e:
            raise RuntimeError(f"Failed to generate content with Claude: {str(e)}")

    def test_connection(self) -> bool:
        """Test if Claude API is accessible."""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                messages=[
                    {
                        "role": "user",
                        "content": "Say 'MyTake is ready' if you can read this."
                    }
                ]
            )
            return "mytake" in message.content[0].text.lower()
        except Exception:
            return False


# Global Claude client — instantiated lazily so import works without an API key
_claude_client: "ClaudeClient | None" = None

def get_claude_client() -> "ClaudeClient":
    global _claude_client
    if _claude_client is None:
        _claude_client = ClaudeClient()
    return _claude_client

# Legacy alias used throughout the codebase
class _LazyClient:
    """Proxy that defers ClaudeClient creation until first use."""
    def __getattr__(self, name):
        return getattr(get_claude_client(), name)

claude_client = _LazyClient()

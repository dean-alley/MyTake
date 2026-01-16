"""
Prompt templates for Claude AI generation.
"""

from typing import Dict


def create_system_prompt(voice_context: str) -> str:
    """Create system prompt with voice profile context."""
    return f"""You are MyTake, a content digestion assistant that helps users understand and re-express content in their own voice.

Your task is to generate exactly 4 sections for any given content:

1. **What they said — deep**: A comprehensive, nuanced analysis of the original content. Capture key arguments, evidence, context, implications, and any underlying assumptions.

2. **What they said — simple**: A clear, accessible summary of the original content. Strip away jargon and complexity while preserving accuracy.

3. **What I'd say — simple**: Rewrite the content in the USER'S voice (not yours), keeping it accessible and conversational. This should sound like the user explaining it to a friend.

4. **What I'd say — deep**: Rewrite the content in the USER'S voice with full depth and nuance. This is how the user would explain it when they have time to think deeply.

{voice_context}

CRITICAL INSTRUCTIONS:
- Sections 1 & 2 should be objective summaries of the ORIGINAL content
- Sections 3 & 4 should be re-expressions in the USER'S voice, as if they absorbed the content and are now explaining it
- Keep the same core information across all sections, just vary depth and voice
- Use markdown formatting for structure
- Be honest about limitations or uncertainties in the original content
"""


def create_user_prompt(content_text: str, title: str, source_type: str) -> str:
    """Create user prompt with the content to process."""
    return f"""Process this {source_type} content:

**Title/Source**: {title}

**Content**:
{content_text}

---

Generate all 4 sections following the system instructions. Format your response EXACTLY as follows:

## What they said — deep

[Your comprehensive analysis here]

## What they said — simple

[Your simple summary here]

## What I'd say — simple

[User's voice, simple version here]

## What I'd say — deep

[User's voice, comprehensive version here]
"""


def parse_claude_response(response_text: str) -> Dict[str, str]:
    """
    Parse Claude's response into the 4 sections.

    Returns:
        Dict with keys: what_they_said_deep, what_they_said_simple,
                       what_i_say_simple, what_i_say_deep
    """
    sections = {
        "what_they_said_deep": "",
        "what_they_said_simple": "",
        "what_i_say_simple": "",
        "what_i_say_deep": ""
    }

    # Split by section headers
    parts = response_text.split("## ")

    for part in parts:
        if not part.strip():
            continue

        # Extract section name and content
        lines = part.strip().split("\n", 1)
        if len(lines) < 2:
            continue

        header = lines[0].strip().lower()
        content = lines[1].strip()

        # Map headers to keys
        if "what they said" in header and "deep" in header:
            sections["what_they_said_deep"] = content
        elif "what they said" in header and "simple" in header:
            sections["what_they_said_simple"] = content
        elif "what i'd say" in header and "simple" in header:
            sections["what_i_say_simple"] = content
        elif "what i'd say" in header and "deep" in header:
            sections["what_i_say_deep"] = content

    return sections

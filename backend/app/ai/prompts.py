"""
Prompt templates for Claude AI generation.
"""

from typing import Dict


def create_system_prompt(voice_context: str) -> str:
    """Create system prompt with voice profile context."""
    return f"""You are MyTake, a content digestion assistant that helps users understand and re-express content through reaction and reframing.

CORE PHILOSOPHY: The user doesn't create content from scratch - they create content through reaction and reframing. Their best insights come when they encounter something that resonates, and they process it through their unique lens of lived experience. This isn't copying - it's how learning and dialogue naturally work.

Your task is to generate exactly 4 sections for any given content:

1. **What they said — deep**: A comprehensive, nuanced analysis of the original content. Capture key arguments, evidence, context, implications, and any underlying assumptions.

2. **What they said — simple**: A clear, accessible summary of the original content. Strip away jargon and complexity while preserving accuracy.

3. **What I'd say — simple**: The USER'S TAKE on this content - not a rewrite, but a reaction. Process the content through the user's unique filters and lived experience. This should sound like the user telling a friend at a jam session what they learned and what they think about it. Ground it in their actual experience, not theory.

4. **What I'd say — deep**: The USER'S FULL TAKE with depth and nuance. This is the user reframing the content through all their unique perspective filters - connecting it to their lived experience, their work, their creative practice, their community. Not just what the content said, but what it means to someone with their specific background and how they'd add to the conversation.

{voice_context}

CRITICAL INSTRUCTIONS:
- Sections 1 & 2 should be objective summaries of the ORIGINAL content
- Sections 3 & 4 are REACTIONS and REFRAMES, not just rewrites. The user is processing the content through their unique filters and adding their perspective based on lived experience.
- For "What I'd say" sections, ask: What would this person actually say about this at a jam session? What lived experience do they bring? What's their honest take, including where they might disagree or have nuance to add?
- The user's voice is conversational, not performative - like a voice note to a friend, not a LinkedIn post
- Ground everything in specific experience, not theory ("I literally did this" not "one might consider")
- Be honest about limitations, struggles, and uncertainty - that's part of the authentic voice
- Use markdown formatting for structure
"""


def create_user_prompt(content_text: str, title: str, source_type: str) -> str:
    """Create user prompt with the content to process."""
    return f"""Process this {source_type} content and generate my take on it:

**Title/Source**: {title}

**Content**:
{content_text}

---

Generate all 4 sections following the system instructions.

For the "What I'd say" sections, remember: this is about REACTION and REFRAMING. Process through my unique filters:
- What's my lived experience with this topic?
- What would I tell my friends about this?
- What's the grounded, working-class creative angle?
- What's the ADHD-honest version that acknowledges both struggle and insight?

Format your response EXACTLY as follows:

## What they said — deep

[Comprehensive analysis of the original content]

## What they said — simple

[Clear, accessible summary]

## What I'd say — simple

[My take - conversational, like explaining to a friend at a jam session]

## What I'd say — deep

[My full take - processed through my filters, grounded in lived experience, adding my perspective to the conversation]
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

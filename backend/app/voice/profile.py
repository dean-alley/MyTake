"""
Voice profile system for personalizing content generation.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from app.config import settings


class VoiceProfile:
    """Manages user's voice profile for content generation."""

    def __init__(self, profile_path: Optional[Path] = None):
        self.profile_path = profile_path or settings.voice_profile_path
        self.profile = self._load_or_create_default()

    def _load_or_create_default(self) -> Dict:
        """Load existing profile or create default one."""
        if self.profile_path.exists():
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        else:
            return self._create_default_profile()

    def _create_default_profile(self) -> Dict:
        """Create default voice profile."""
        default_profile = {
            "version": "1.0.0",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "style_rules": {
                "tone": "conversational yet thoughtful",
                "formality": "casual but not sloppy",
                "sentence_structure": "mix of short punchy sentences and longer explanatory ones",
                "vocabulary": "accessible language with occasional precise technical terms when needed",
                "perspective": "first-person when expressing opinions, clear attribution otherwise"
            },
            "preferences": {
                "avoid": [
                    "corporate jargon",
                    "excessive hedging (e.g., 'it seems like', 'perhaps maybe')",
                    "clickbait phrases",
                    "unnecessary superlatives"
                ],
                "embrace": [
                    "direct statements",
                    "concrete examples",
                    "clear reasoning",
                    "honest uncertainty when appropriate"
                ],
                "structural": {
                    "use_bullet_points": True,
                    "use_subheadings": True,
                    "paragraph_length": "medium - 3-5 sentences typically"
                }
            },
            "personality_traits": [
                "curious and questioning",
                "pragmatic over theoretical",
                "values clarity over cleverness",
                "skeptical but open-minded"
            ],
            "example_phrases": [
                "Here's what matters:",
                "The key insight is...",
                "This breaks down to...",
                "Worth noting:"
            ],
            "learning": {
                "positive_examples": [],
                "feedback_incorporated": []
            }
        }

        self._save_profile(default_profile)
        return default_profile

    def _save_profile(self, profile: Dict):
        """Save profile to disk."""
        profile["updated_at"] = datetime.utcnow().isoformat()
        with open(self.profile_path, 'w') as f:
            json.dump(profile, f, indent=2)

    def get_prompt_context(self) -> str:
        """Generate prompt context from voice profile."""
        style = self.profile["style_rules"]
        prefs = self.profile["preferences"]
        traits = self.profile["personality_traits"]
        phrases = self.profile["example_phrases"]

        # Build base context
        context = f"""When writing in my voice, use these guidelines:

TONE & STYLE:
- Tone: {style['tone']}
- Formality: {style['formality']}
- Sentence structure: {style['sentence_structure']}
- Vocabulary: {style['vocabulary']}
- Perspective: {style['perspective']}

PREFERENCES:
Avoid:
{chr(10).join(f'- {item}' for item in prefs['avoid'])}

Embrace:
{chr(10).join(f'- {item}' for item in prefs['embrace'])}

PERSONALITY:
{chr(10).join(f'- {trait}' for trait in traits)}

TYPICAL PHRASES I USE:
{chr(10).join(f'- "{phrase}"' for phrase in phrases)}

STRUCTURAL PREFERENCES:
- Use bullet points: {prefs['structural']['use_bullet_points']}
- Use subheadings: {prefs['structural']['use_subheadings']}
- Paragraph length: {prefs['structural']['paragraph_length']}
"""

        # Add core philosophy if present (v2.0+ profiles)
        if "core_philosophy" in self.profile:
            philosophy = self.profile["core_philosophy"]
            context += f"""
CORE PHILOSOPHY:
{philosophy.get('insight', '')}
"""

        # Add unique filters if present (v2.0+ profiles)
        if "unique_filters" in self.profile:
            filters = self.profile["unique_filters"]
            context += "\nUNIQUE PERSPECTIVE FILTERS (process content through these lenses):\n"
            for key, filter_data in filters.items():
                context += f"- {filter_data['name']}: {filter_data['description']}\n"

        # Add processing questions if present (v2.0+ profiles)
        if "processing_questions" in self.profile:
            questions = self.profile["processing_questions"]
            context += f"""
QUESTIONS TO ASK WHEN CREATING 'MY TAKE':
{chr(10).join(f'- {q}' for q in questions)}
"""

        # Add content sweet spots if present (v2.0+ profiles)
        if "content_sweet_spots" in self.profile:
            sweet_spots = self.profile["content_sweet_spots"]
            context += f"""
CONTENT SWEET SPOTS (topics where this voice shines):
{chr(10).join(f'- {spot}' for spot in sweet_spots)}
"""

        # Add voice markers if present (v2.0+ profiles)
        if "voice_markers" in self.profile:
            markers = self.profile["voice_markers"]
            if "authentic_expressions" in markers:
                context += f"""
AUTHENTIC EXPRESSIONS:
{chr(10).join(f'- "{expr}"' for expr in markers['authentic_expressions'])}
"""

        # Add background context if present (v2.0+ profiles)
        if "background_context" in self.profile:
            bg = self.profile["background_context"]
            context += "\nBACKGROUND CONTEXT (for grounding responses in lived experience):\n"
            for key, value in bg.items():
                context += f"- {key.replace('_', ' ').title()}: {value}\n"

        return context

    def update_from_feedback(self, feedback: Dict):
        """Update profile based on user feedback."""
        if feedback.get("sounds_like_me"):
            self.profile["learning"]["positive_examples"].append({
                "content_id": feedback.get("content_id"),
                "section": feedback.get("section"),
                "timestamp": datetime.utcnow().isoformat()
            })

        if feedback.get("feedback_text"):
            self.profile["learning"]["feedback_incorporated"].append({
                "content_id": feedback.get("content_id"),
                "feedback": feedback["feedback_text"],
                "timestamp": datetime.utcnow().isoformat()
            })

        self._save_profile(self.profile)

    def get_version(self) -> str:
        """Get current profile version."""
        return self.profile["version"]

    def export_profile(self) -> Dict:
        """Export complete profile."""
        return self.profile.copy()

    def update_profile(self, updates: Dict):
        """Update profile with new values."""
        self.profile.update(updates)
        self._save_profile(self.profile)


# Global voice profile instance
voice_profile = VoiceProfile()

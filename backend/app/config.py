"""
Application configuration using Pydantic settings.
"""

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings."""

    # API Keys
    anthropic_api_key: str = ""
    apify_api_key: str = ""

    # Paths
    data_dir: Path = Path(__file__).parent.parent.parent / "data"
    docs_dir: Path = data_dir / "docs"
    db_path: Path = data_dir / "db.sqlite"
    voice_profile_path: Path = data_dir / "voice_profile.json"

    # AI Settings
    claude_model: str = "claude-3-5-sonnet-20241022"
    claude_max_tokens: int = 4096

    # Application Settings
    app_name: str = "MyTake"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()

# Ensure directories exist
settings.data_dir.mkdir(parents=True, exist_ok=True)
settings.docs_dir.mkdir(parents=True, exist_ok=True)

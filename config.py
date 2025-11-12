"""
Configuration management for the meeting recorder application.
"""
import os
from dotenv import load_dotenv


class Config:
    """Application configuration."""

    def __init__(self, env_file=".env"):
        """
        Load configuration from environment file.

        Args:
            env_file: Path to the .env file
        """
        # Load environment variables from .env file
        load_dotenv(env_file)

        # API Configuration
        self.ai_provider = os.getenv("AI_PROVIDER", "claude").lower()
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Recording Settings
        self.sample_rate = int(os.getenv("SAMPLE_RATE", "44100"))
        self.channels = int(os.getenv("CHANNELS", "2"))

        # Directory Settings
        self.recordings_dir = "recordings"
        self.transcripts_dir = "transcripts"

        # Validate configuration
        self._validate()

    def _validate(self):
        """Validate that required configuration is present."""
        if self.ai_provider not in ["claude", "chatgpt"]:
            raise ValueError(f"Invalid AI_PROVIDER: {self.ai_provider}. Must be 'claude' or 'chatgpt'")

        if self.ai_provider == "claude" and not self.anthropic_api_key:
            print("WARNING: ANTHROPIC_API_KEY not set. Claude will not work.")

        if self.ai_provider == "chatgpt" and not self.openai_api_key:
            print("WARNING: OPENAI_API_KEY not set. ChatGPT will not work.")

        if not self.openai_api_key:
            print("WARNING: OPENAI_API_KEY not set. Transcription will not work.")

    def print_config(self):
        """Print current configuration (hiding API keys)."""
        print("\nCurrent Configuration:")
        print("=" * 60)
        print(f"AI Provider: {self.ai_provider}")
        print(f"Anthropic API Key: {'*' * 20 if self.anthropic_api_key else 'Not Set'}")
        print(f"OpenAI API Key: {'*' * 20 if self.openai_api_key else 'Not Set'}")
        print(f"Sample Rate: {self.sample_rate} Hz")
        print(f"Channels: {self.channels}")
        print(f"Recordings Directory: {self.recordings_dir}")
        print(f"Transcripts Directory: {self.transcripts_dir}")
        print("=" * 60 + "\n")

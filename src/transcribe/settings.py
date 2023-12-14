from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """Configuration settings for the transcription application."""

    data_dir: Path = Path(__file__).absolute().parent.parent.parent / "data"
    audio_file: str = str(data_dir / "recording0.wav")
    transcript_file: str = str(data_dir / "transcript.txt")

    model_config = SettingsConfigDict(
        env_nested_delimiter="__", env_file=".env", extra="ignore"
    )


settings = Settings()

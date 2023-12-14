from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    data_dir: Path = Path(__file__).absolute().parent.parent.parent / "data"
    audio_file: Path = data_dir / "recording0.wav"
    transcript_file: Path = data_dir / "transcript.txt"

    model_config = SettingsConfigDict(
        env_nested_delimiter="__", env_file=".env", extra="ignore"
    )


settings = Settings()

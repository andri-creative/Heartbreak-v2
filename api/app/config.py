"""
Konfigurasi Aplikasi Heartbreak AI V3
"""

import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)
else:
    load_dotenv(find_dotenv(), override=True)

class Settings(BaseSettings):
    PROJECT_NAME: str = "❤️‍🩹 Heartbreak AI V3 API"
    VERSION: str = "3.0.0"
    API_PREFIX: str = "/api"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    # Path Model Bundle V3
    MODEL_BUNDLE_PATH: str = "heartbreak_demographic_bundle_v3.pkl"
    
    # OpenRouter API Key (OpenAI GPT)
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    AI_GATEWAY_API_KEY: str = os.getenv("AI_GATEWAY_API_KEY", "")
    
    # Thresholds Klinis Severity (3-Tier)
    THRESHOLD_BERAT: float = 70.0
    THRESHOLD_SEDANG: float = 35.0

    model_config = SettingsConfigDict(
        env_file=dotenv_path,
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

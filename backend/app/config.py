from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str | None = None
    MODEL_NAME: str = "gpt-4o-mini"
    DB_URL: str = "sqlite+aiosqlite:///./symptoms.db"

    class Config:
        env_file = ".env"

settings = Settings()

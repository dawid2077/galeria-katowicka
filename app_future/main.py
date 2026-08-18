from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENROUTER_API_KEY: str
    VENUE_NAME: str = "Galeria Katowicka"

    model_config = SettingsConfigDict(
        # Szuka .env, ale jeśli go nie ma (np. na K8s), ignoruje go i czyta czyste os.environ
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()   
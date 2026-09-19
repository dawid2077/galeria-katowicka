from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    # These will automatically read from environment variables 
    # whether they come from a local .env file OR from Kubernetes!
    CLERK_PUBLIC_KEY: str
    CLERK_SECRET_KEY: str
    DATABASE_URL: str
    OPENROUTER_API_KEY: str
    VENUE_NAME: str = "Galeria Katowicka"
    MODEL: str = "openai/gpt-4o-mini"
    model_config = SettingsConfigDict(
        env_file="../configs/.env", 
        env_file_encoding="utf-8"
    )

settings = Settings()
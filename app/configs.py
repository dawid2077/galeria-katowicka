from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    # These will automatically read from environment variables 
    # whether they come from a local .env file OR from Kubernetes!
    DATABASE_URL: str
    OPENROUTER_API_KEY: str
    VENUE_NAME: str = "Galeria Katowicka"

    # Updated to Pydantic V2 SettingsConfigDict syntax
    model_config = SettingsConfigDict(
        env_file="../configs/.env", 
        env_file_encoding="utf-8"
    )

settings =Settings()
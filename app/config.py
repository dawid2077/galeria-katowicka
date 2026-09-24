from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    CLERK_PUBLIC_KEY: str = Field(...)
    CLERK_SECRET_KEY: str = Field(...)
    DATABASE_URL: str = Field(...)
    OPENROUTER_API_KEY: str = Field(...)
    AUTHORIZED_PARTIES: list[str] = Field(...)
    #in future i can add if its possible to check if these are actual urls in whole settings
    LLM_URL: str = Field(...)
    LLM_MODEL: str = Field(...)

    model_config = SettingsConfigDict(
        env_file="configs/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings() # pyright: ignore[reportCallIssue]

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "..."
    OPENAI_API_KEY: str = "..."
    SECRET_KEY: str = "..."
    
    # This tells Pydantic: "If you see extra stuff, just ignore it."
    model_config = SettingsConfigDict(extra='ignore', env_file=".env")

settings = Settings()
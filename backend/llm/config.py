from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    gemini_api_key: str
    model_config = {
            "env_file": ".env",
            "extra": "ignore"
        }    

settings = Settings()
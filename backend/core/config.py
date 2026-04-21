from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/dbname"
    OPENAI_API_KEY: str = "123123jbaskjdbkj"
    SECRET_KEY: str = "super_secret"
    
    class Config:
        env_file = ".env"

settings = Settings()
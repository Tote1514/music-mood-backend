from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "dev"
    DATABASE_URL: str
    REDIRECT_URI: str

    FRONTEND_URL: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_SCOPES: str

    class Config:
        env_file = ".env"

settings = Settings()

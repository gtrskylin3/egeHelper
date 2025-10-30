from pydantic_settings import BaseSettings
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
CERT_DIR = APP_DIR / 'cert'

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

class JWTSettings(BaseSettings):
    EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30 
    PRIVATE_KEY: Path = CERT_DIR / 'private_key.pem'
    PUBLIC_KEY: Path = CERT_DIR / 'public_key.pem'
    ALGORITHM: str = 'RS256'

settings = Settings()
jwt_settings = JWTSettings()
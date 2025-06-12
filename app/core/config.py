from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

class AutoJWT(BaseSettings):
    algorithm: str = 'RS256'
    private_key_path: Path = BASE_DIR / 'core' / 'cert' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'core' / 'cert' / 'jwt-public.pem'
    access_token_expire_minutes: int = 15

class Settings(BaseSettings):
    auth_jwt: AutoJWT = AutoJWT()

settings = Settings()

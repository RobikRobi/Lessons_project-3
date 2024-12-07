from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

class Config(BaseSettings):
    database:str
    user: str
    password: str
    host: str
    class Config:
        env_file = ".env"

config = Config()
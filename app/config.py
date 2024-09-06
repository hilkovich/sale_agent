import os
import sys
from dotenv import load_dotenv

env_path = os.path.join(sys.path[0], ".env")
load_dotenv(env_path)


class DB_Settings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:{POSTGRES_PORT}/postgres"


class TG_Settings:
    TG_BOT_TOKEN: str = os.getenv("TG_BOT_TOKEN")

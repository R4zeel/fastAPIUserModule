import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "BotFarm"
    PROJECT_VERSION: str = "1.0.0"
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "localhost")
    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DATABASE_URL: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
    )


settings = Settings()

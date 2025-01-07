import os

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine, AsyncSession)
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra="allow")
    DEBUG: bool = True

    DB_USER: str = 'sqlite'
    DB_PASSWORD: str = "sqlite"
    DB_NAME: str = "db_santar4_base"

    GOOGLE_CLIENT_ID: str = "..."
    GOOGLE_CLIENT_SECRET: str = "...."
    GOOGLE_REDIRECT_URI: str = "..."

    SECRET_KEY: str = os.urandom(24)

    def pg_dsn(self, engine_="asyncpg") -> PostgresDsn:
        return (
            f"postgresql+{engine_}://"
            f"{self.DB_USER}:{self.DB_PASSWORD}@"
            f"localhost:5432/{self.DB_NAME}")

    def sqlite_dsn(self) -> str:
        return f"sqlite+aiosqlite:///./{self.DB_NAME}.db"


settings_app = Settings()

DATABASE_URL = settings_app.sqlite_dsn()
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_session() -> AsyncSession:
    async with async_session() as sess:
        yield sess
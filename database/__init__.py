import asyncio
import socket
from contextlib import closing

from logger import logger
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import os
from dotenv import load_dotenv

load_dotenv()


class AsyncDatabaseSession:
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "dev_db")
    DB_PORT = os.getenv("DB_PORT", 5432)

    def __init__(self):
        self.session_factory = None
        self._engine = None
        self._db_config = self.get_db_connection_string()
        self.init()

    async def __aenter__(self):
        if self.session_factory is None:
            self.init()
        return self.session_factory

    def init(self) -> None:
        self._engine = create_async_engine(
            self._db_config,
            future=True,
            echo=True,
        )
        self.session_factory = async_sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )

    def get_db_connection_string(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session

    @staticmethod
    async def check_database_available(retries=5, delay=5):
        for attempt in range(retries):
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                if sock.connect_ex((os.getenv('DATABASE_HOST'), int(os.getenv('DATABASE_PORT')))) == 0:
                    return True
                else:
                    logger.warning(f"Попытка {attempt + 1} не удалась")
                    await asyncio.sleep(delay)
        return False

    async def init_tables(self):
        if await self.check_database_available():
            async with self._engine.begin() as conn:
                result = await conn.execute(
                    text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"))
                tables = result.fetchall()

                if not tables:
                    from .models import Base
                    await conn.run_sync(Base.metadata.create_all)
                    logger.info("Таблицы созданы")
                else:
                    logger.info("Таблицы уже существуют")
        else:
            print("Не удалось подключиться к базе данных")


db = AsyncDatabaseSession()

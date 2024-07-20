from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class AsyncDatabaseSession:
    def __init__(self):
        self.session_factory = None
        self._engine = None
        self._db_config = DATABASE_URL
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

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session


db = AsyncDatabaseSession()


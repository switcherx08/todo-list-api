from sqlalchemy import select, Column, Integer, String, DateTime

from . import Base


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(String(255), nullable=False, default='PENDING')
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    @classmethod
    async def get_all_tasks(cls, session):
        query = select(cls)
        tasks = await session.execute(query)
        return tasks.scalars().all()

    @classmethod
    async def get_by_id(cls, session, id):
        query = select(cls).where(cls.id == id)
        tasks = await session.execute(query)
        return tasks.unique().scalar()

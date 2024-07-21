from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.access_utils import get_task_from_db_by_id
from database import db
from database.models import Task as MTask
from schemas.task import TaskBase, TaskView

ns = APIRouter()


@ns.get('/', response_model=list[TaskView])
async def get_task_list(session: AsyncSession = Depends(db.session_dependency)):
    tasks = await MTask.get_all_tasks(session)
    return tasks


@ns.get('/{task_id}', response_model=TaskView)
async def get_task(task_id: int, session: AsyncSession = Depends(db.session_dependency)):
    return await get_task_from_db_by_id(session, task_id)


@ns.post('/', response_model=TaskView)
async def create_task(data: TaskBase, session: AsyncSession = Depends(db.session_dependency),
                      ):
    task = MTask(**data.model_dump())
    task.created_at, task.updated_at = datetime.now(), datetime.now()
    session.add(task)

    await session.commit()
    return task


@ns.put('/{task_id}', response_model=TaskView)
async def update_task(task_id: int, data: TaskBase, session: AsyncSession = Depends(db.session_dependency),
                      ):
    task = await get_task_from_db_by_id(session, task_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(task, key):
            setattr(task, key, value)

    task.updated_at = datetime.now()
    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


@ns.delete('/{task_id}', status_code=204)
async def delete_task(task_id: int, session: AsyncSession = Depends(db.session_dependency),
                      ):
    task = await get_task_from_db_by_id(session, task_id)
    await session.delete(task)
    await session.commit()

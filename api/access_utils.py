from fastapi import HTTPException
from database.models import Task as MTask


async def get_task_from_db_by_id(session, task_id):
    task = await MTask.get_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    return task

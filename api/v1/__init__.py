from fastapi import APIRouter
from .task import ns as task_ns

api_v1_router = APIRouter()

api_v1_router.include_router(task_ns, prefix="/task", tags=["task"])



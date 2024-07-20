from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    name: str
    description: str
    status: Literal['PENDING', 'IN_PROGRESS', 'COMPLETED'] = None


class TaskView(TaskBase):
    created_at: datetime
    updated_at: datetime
    id: int




from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    parent_task_id: Optional[int] = None
    title: str
    description: str
    deadline: datetime
    status: str
    executor_id: int = None


class TaskRead(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass

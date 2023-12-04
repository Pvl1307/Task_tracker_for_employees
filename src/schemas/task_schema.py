from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    id: int
    parent_task_id: Optional[int]
    title: str
    description: str
    created_at: datetime
    deadline: datetime
    status: str
    executor_id: int = None


class TaskRead(TaskBase):
    pass

    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass

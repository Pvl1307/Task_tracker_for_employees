from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.models.task_model import TaskStatus


class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    deadline: datetime
    status: TaskStatus
    executor_id: Optional[int] = None

    class Config:
        from_attributes = True


class ImportantTask(BaseModel):
    title: str
    deadline: datetime
    executor_name: Optional[str] = None


class TaskCreate(BaseModel):
    parent_task_id: Optional[int] = None
    title: str
    description: str
    deadline: datetime = datetime.utcnow()
    status: TaskStatus
    executor_id: Optional[int] = None


class TaskUpdate(BaseModel):
    parent_task_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    executor_id: Optional[int] = None

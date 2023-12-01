from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str
    deadline: datetime
    status: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    parent_task_id: int
    executor_id: int

    class Config:
        orm_mode = True

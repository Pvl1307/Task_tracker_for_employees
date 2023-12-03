from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    parent_task_id: int = None
    title: str
    description: str
    deadline: datetime
    status: str
    executor_id: int = None


class TaskRead(TaskBase):
    pass

    class Config:
        orm_mode = True


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass

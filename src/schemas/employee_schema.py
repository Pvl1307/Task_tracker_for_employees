from typing import Optional, List

from pydantic import BaseModel

from src.schemas.task_schema import TaskRead


class EmployeeRead(BaseModel):
    id: int
    fullname: str
    position: str
    is_busy: Optional[bool] = False
    tasks: Optional[List[TaskRead]] = None

    class Config:
        from_attributes = True


class EmployeeCreate(BaseModel):
    fullname: str
    position: str
    is_busy: Optional[bool] = False
    tasks: Optional[list[str]] = None


class EmployeeUpdate(BaseModel):
    fullname: str
    position: Optional[str] = None
    is_busy: Optional[bool] = False

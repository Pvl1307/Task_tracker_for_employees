from typing import Optional

from pydantic import BaseModel


class EmployeeBase(BaseModel):
    fullname: str
    position: str
    is_busy: Optional[bool] = False


class EmployeeRead(EmployeeBase):
    id: int

    class Config:
        from_attributes = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    position: Optional[str] = None

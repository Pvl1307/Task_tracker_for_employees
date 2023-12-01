from pydantic import BaseModel


class EmployeeBase(BaseModel):
    fullname: str
    position: str


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True

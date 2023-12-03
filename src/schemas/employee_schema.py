from pydantic import BaseModel


class EmployeeBase(BaseModel):
    fullname: str
    position: str
    is_busy: bool = False


class EmployeeRead(EmployeeBase):
    pass

    class Config:
        orm_mode = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass



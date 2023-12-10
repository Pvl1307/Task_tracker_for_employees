from typing import Union, List, Type

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from src.models import Employee, Task
from src.schemas.employee_schema import EmployeeCreate, EmployeeUpdate


class EmployeeCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_employee(self, employee_id: int) -> Union[Employee, None]:
        """Вывод сотрудника по id (GET)"""
        return self.db.query(Employee).filter_by(id=employee_id).first()

    def get_all_employees(self, skip: int = 0, limit: int = 100) -> List[Type[Employee]]:
        """Вывод всех сотрудников с возможностью пагинации (GET)
        skip - количество, которое нужно в начале пропустить
        limit - лимит сотрудников на вывод"""
        return self.db.query(Employee).offset(skip).limit(limit).all()

    def get_busy_employees(self) -> List[Employee]:
        """Запрос сотрудников и их задач, отсортированных по количеству активных задач."""
        query = (
            self.db.query(Employee)
            .outerjoin(Task, Employee.id == Task.executor_id)
            .group_by(Employee.id)
            .order_by(func.count(Task.id).desc())
            .options(joinedload(Employee.tasks))
            .all())

        return query

    def create_employee(self, employee_schema: EmployeeCreate) -> Employee:
        """Создание сотрудника (CREATE)"""
        is_busy_value = employee_schema.is_busy if employee_schema.is_busy is not None else False

        db_employee = Employee(fullname=employee_schema.fullname,
                               position=employee_schema.position,
                               is_busy=is_busy_value)
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def patch_employee(self, employee_schema: EmployeeUpdate, employee_id: int) -> Union[Employee, None]:
        """Обновление сотрудника (PATCH)"""
        db_employee = self.db.query(Employee).filter_by(id=employee_id).first()

        if db_employee:
            for field, value in employee_schema.model_dump(exclude_unset=True).items():
                setattr(db_employee, field, value)
            self.db.commit()
            self.db.refresh(db_employee)

        return db_employee

    def delete_employee(self, employee_id: int) -> Union[Employee, None]:
        """Удаление сотрудника (DELETE)"""
        db_employee = self.db.query(Employee).filter_by(id=employee_id).first()
        if db_employee:
            self.db.delete(db_employee)
            self.db.commit()

        return db_employee

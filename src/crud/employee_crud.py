from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models import Employee, Task
from src.schemas.employee_schema import EmployeeCreate, EmployeeUpdate


def get_employee(db: Session, employee_id: int):
    """Вывод сотрудника по id (GET)"""
    return db.query(Employee).filter_by(id=employee_id).first()


def get_busy_employee(db: Session):
    """Вывод списка сотрудников и их задачи, отсортированный по количеству активных задач (GET)"""
    return (db.query(Employee, func.count(Task.id).label('task_count'))
            .join(Task, Employee.id == Task.executor_id)
            .filter_by(Employee.is_busy)
            .group_by(Employee.id)
            .order_by(func.count(Task.id).desc())
            .all()
            )


def get_available_employees(db: Session):
    """Вывод сотрудникам, которые могут взять такие задачи
    (наименее загруженный сотрудник или сотрудник выполняющий родительскую задачу,
    если ему назначено максимум на 2 задачи больше,
    чем у наименее загруженного сотрудника)"""
    employees_with_tasks_count = (
        db.query(Employee, func.count(Task.id).label('task_count')
                 .join(Task, Employee.id == Task.executor_id)
                 .filter(Employee.is_busy is True)
                 .groupby(Employee.id)
                 .all()
                 )
    )

    sorted_employees = sorted(employees_with_tasks_count, key=lambda x: x.task_count)

    available_employees = sorted_employees[:2]

    important_tasks = []
    for employee, task_count in available_employees:
        tasks = (
            db.query(Task)
            .filter(Task.executor_id == employee.id)
            .filter(Task.status != 'Completed')  # Выбрать невыполненные задачи
            .order_by(Task.deadline)
            .all()
        )

        for task in tasks:
            important_tasks.append({
                'Важная задача': task.title,
                'Срок': task.deadline,
                'ФИО сотрудника': employee.fullname
            })

    return important_tasks


def get_all_employees(db: Session, skip: int = 0, limit: int = 100):
    """Вывод всех сотрудников с возможностью пагинации (GET)
    skip - количество, которое нужно в начале пропустить
    limit - лимит сотрудников на вывод"""
    return db.query(Employee).offset(skip).limit(limit).all()


def create_employee(db: Session, employee: EmployeeCreate):
    """Создание сотрудника (CREATE)"""
    is_busy_value = employee.is_busy if employee.is_busy is not None else False

    db_employee = Employee(fullname=employee.fullname,
                           position=employee.position,
                           is_busy=is_busy_value)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, employee_id: int, employee_data: EmployeeUpdate):
    """Обновление сотрудника (PUT, PATCH)"""
    db_employee = db.query(Employee).filter_by(id=employee_id).first()

    if db_employee:
        for field, value in employee_data.model_dump(exclude_unset=True).items():
            setattr(db_employee, field, value)
        db.commit()
        db.refresh(db_employee)

    return db_employee


def delete_employee(db: Session, employee_id: int):
    """Удаление сотрудника (DELETE)"""
    db_employee = db.query(Employee).filter_by(id=employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
        db.refresh(db_employee)

    return db_employee

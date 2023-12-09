from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud.employee_crud import EmployeeCRUD
from src.db.database import get_db
from src.schemas.employee_schema import EmployeeRead, EmployeeCreate, EmployeeUpdate

router = APIRouter(
    prefix='/employees',
    tags=['employees']
)


@router.get('/{employee_id}', response_model=EmployeeRead)
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    """Вывод сотрудника по id (GET)"""
    try:
        employee_crud = EmployeeCRUD(db=db)
        employee = employee_crud.get_employee(employee_id=employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail='Employee was not founded')
        return employee
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/', response_model=List[EmployeeRead])
def get_employees(db: Session = Depends(get_db)):
    """Вывод всех сотрудников (GET)"""
    try:
        employee_crud = EmployeeCRUD(db=db)
        employees = employee_crud.get_all_employees()
        if employees is None:
            raise HTTPException(status_code=404, detail='Employees were not founded')
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/busy_employees/', response_model=List[EmployeeRead])
def get_busy_employees(db: Session = Depends(get_db)):
    """Запрашивает из БД список всех сотрудников и их задач, отсортированный по количеству активных задач."""
    try:
        employee_crud = EmployeeCRUD(db=db)
        busy_employees = employee_crud.get_busy_employees()

        if not busy_employees:
            raise HTTPException(status_code=404, detail='No busy employees found')

        return busy_employees

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/', summary='title func', tags=['post'], description='test description', response_model=EmployeeRead)
def create_emp(employee_schema: EmployeeCreate, db: Session = Depends(get_db)):
    """Создание сотрудника (CREATE)"""
    try:
        employee_crud = EmployeeCRUD(db=db)
        created_employee = employee_crud.create_employee(employee_schema=employee_schema)
        return created_employee
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch('/{employee_id}', summary='title func', tags=['post'], response_model=EmployeeRead)
def patch_emp(employee: EmployeeUpdate, employee_id: int, db: Session = Depends(get_db)):
    """Обновление сотрудника (PATCH)"""
    try:
        employee_crud = EmployeeCRUD(db=db)
        employee = employee_crud.patch_employee(employee_id=employee_id, employee_schema=employee)
        return employee
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/{employee_id}')
def delete_emp(employee_id: int, db: Session = Depends(get_db)):
    """Удаление сотрудника (DELETE)"""
    try:
        employee_crud = EmployeeCRUD(db=db)
        employee = employee_crud.delete_employee(employee_id=employee_id)
        return employee
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from typing import List, Type

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud.task_crud import TaskCRUD
from src.db.database import get_db
from src.schemas.task_schema import TaskRead, TaskCreate, TaskUpdate, ImportantTask

router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)


@router.get('/{task_id}', response_model=TaskRead)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)) -> TaskRead:
    """Вывод задания по id (GET)"""
    try:
        task_crud = TaskCRUD(db=db)
        task = task_crud.get_task(task_id=task_id)
        if task is None:
            raise HTTPException(status_code=404, detail='Task was not found')
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/', response_model=List[TaskRead])
def get_tasks(db: Session = Depends(get_db)) -> List[Type[TaskRead]]:
    """Вывод всех заданий (GET)"""
    try:
        task_crud = TaskCRUD(db=db)
        tasks = task_crud.get_all_tasks()
        if tasks is None:
            raise HTTPException(status_code=404, detail='Tasks were not founded')
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/important_tasks/', response_model=List[ImportantTask])
def get_important_tasks(db: Session = Depends(get_db)) -> List[ImportantTask]:
    """Вывод задач, не взятых в работу, и сотрудников, способных взять их (GET)"""
    try:
        task_crud = TaskCRUD(db=db)
        important_tasks = task_crud.get_important_tasks()
        if not important_tasks:
            raise HTTPException(status_code=404, detail='No important tasks founded')
        return important_tasks
    except HTTPException as e:
        print(f"Exception details: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected exception: {str(e)}")
        raise HTTPException(status_code=500, detail='Internal Server Error')


@router.post('/', response_model=TaskRead)
def create_tsk(task_schema: TaskCreate, db: Session = Depends(get_db)) -> TaskRead:
    """Создание задания (POST)"""
    try:
        task_crud = TaskCRUD(db=db)
        created_task = task_crud.create_task(task_schema=task_schema)
        return created_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch('/{task_id}/', response_model=TaskRead)
def patch_tsk(task_schema: TaskUpdate, task_id: int, db: Session = Depends(get_db)) -> TaskRead:
    """Обновление задания (PATCH)"""
    try:
        task_crud = TaskCRUD(db=db)
        task = task_crud.patch_task(task_id=task_id, task_schema=task_schema)
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/{task_id}/')
def delete_tsk(task_id: int, db: Session = Depends(get_db)) -> TaskRead:
    """Удаление задания (DELETE)"""
    try:
        task_crud = TaskCRUD(db=db)
        task = task_crud.delete_task(task_id=task_id)
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from sqlalchemy.orm import Session

from src.models import Task
from src.schemas.task_schema import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int):
    """Вывод задания по id (GET)"""
    return db.query(Task).filter_by(id=task_id).first()


def get_all_tasks(db: Session, skip: int = 0, limit: int = 100):
    """Вывод всех заданий с возможностью пагинации (GET)
    skip - количество, которое нужно в начале пропустить
    limit - лимит заданий на вывод"""
    return db.query(Task).offset(skip).limit(limit).all()


def get_important_tasks(db: Session):
    """Возврашает задачи, не взятые в работу,
    и от которых зависят другие задачи, взятые в работу (GET)"""
    return (db.query(Task)
            .join(Task, Task.id == Task.parent_task_id, isouter=True)
            .filter(Task.status != 'Started')
            .filter(Task.parent_task_id is not None)
            .filter(Task.parent_task.has(status='Started'))
            .all()
            )


def create_task(db: Session, task: TaskCreate):
    """Создание задания (CREATE)"""
    db_task = Task(parent_task_id=task.parent_task_id,
                   title=task.title,
                   description=task.description,
                   deadline=task.deadline,
                   status=task.status,
                   executor_id=task.executor_id
                   )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    """Обновление задания (PUT, PATCH)"""
    db_task = db.query(Task).filter_by(id=task_id).first()

    if db_task:
        for field, value in task_data.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)
        db.commit()
        db.refresh(db_task)

    return db_task


def delete_task(db: Session, task_id: int):
    """Удаление задания (DELETE)"""
    db_task = db.query(Task).filter_by(id=task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()

    return db_task

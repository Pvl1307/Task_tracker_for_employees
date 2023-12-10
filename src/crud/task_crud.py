from datetime import datetime
from typing import Optional, List, Type

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session, joinedload

from src.models import Task, Employee
from src.models.task_model import TaskStatus
from src.schemas.task_schema import TaskCreate, TaskUpdate, ImportantTask


class TaskCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_task(self, task_id: int) -> Optional[Task]:
        """Вывод задания по id (GET)"""
        return self.db.query(Task).filter_by(id=task_id).first()

    def get_all_tasks(self, skip: int = 0, limit: int = 100) -> List[Type[Task]]:
        """Вывод всех заданий с возможностью пагинации (GET)
        skip - количество, которое нужно в начале пропустить
        limit - лимит заданий на вывод"""
        return self.db.query(Task).offset(skip).limit(limit).all()

    def create_task(self, task_schema: TaskCreate) -> Task:
        """Создание задания (CREATE)"""
        db_task = Task(parent_task_id=task_schema.parent_task_id,
                       title=task_schema.title,
                       description=task_schema.description,
                       deadline=task_schema.deadline,
                       status=task_schema.status,
                       executor_id=task_schema.executor_id,
                       created_at=datetime.utcnow()
                       )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)

        return db_task

    def patch_task(self, task_id: int, task_schema: TaskUpdate) -> Optional[Task]:
        """Обновление задания (PATCH)"""
        db_task = self.db.query(Task).filter_by(id=task_id).first()

        if db_task:
            for field, value in task_schema.model_dump(exclude_unset=True).items():
                setattr(db_task, field, value)
            self.db.commit()
            self.db.refresh(db_task)

        return db_task

    def delete_task(self, task_id: int) -> Optional[Task]:
        """Удаление задания (DELETE)"""
        db_task = self.db.query(Task).filter_by(id=task_id).first()
        if db_task:
            self.db.delete(db_task)
            self.db.commit()

        return db_task

    def get_important_tasks(self) -> List[ImportantTask]:
        """Вывод задач, не взятых в работу, и сотрудников, способных взять их (GET)"""
        important_tasks = (self.db.query(Task)
                           .filter(and_(Task.status == TaskStatus.NOT_STARTED,
                                        Task.subtasks.any(Task.status == TaskStatus.STARTED)))
                           .options(joinedload(Task.executor))
                           .all()
                           )

        important_tasks_list = []

        for task in important_tasks:
            suitable_employee = (self.db.query(Employee)
                                 .outerjoin(Task, Employee.id == Task.executor_id)
                                 .group_by(Employee.id)
                                 .having(or_(Employee.id == task.executor_id, func.count(Task.id) <= 2))
                                 .order_by(func.count(Task.id))
                                 .first()
                                 )

            important_task = ImportantTask(
                title=task.title,
                deadline=task.deadline,
                executor_name=suitable_employee.fullname if suitable_employee else None
            )
            important_tasks_list.append(important_task)

        return important_tasks_list

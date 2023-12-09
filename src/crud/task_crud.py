from datetime import datetime

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session, joinedload

from src.models import Task, Employee
from src.models.task_model import TaskStatus
from src.schemas.task_schema import TaskCreate, TaskUpdate, ImportantTask


class TaskCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_task(self, task_id: int):
        """Вывод задания по id (GET)"""
        return self.db.query(Task).filter_by(id=task_id).first()

    def get_all_tasks(self, skip: int = 0, limit: int = 100):
        """Вывод всех заданий с возможностью пагинации (GET)
        skip - количество, которое нужно в начале пропустить
        limit - лимит заданий на вывод"""
        return self.db.query(Task).offset(skip).limit(limit).all()

    def create_task(self, task_schema: TaskCreate):
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

    def patch_task(self, task_id: int, task_schema: TaskUpdate):
        """Обновление задания (PATCH)"""
        db_task = self.db.query(Task).filter_by(id=task_id).first()

        if db_task:
            for field, value in task_schema.model_dump(exclude_unset=True).items():
                setattr(db_task, field, value)
            self.db.commit()
            self.db.refresh(db_task)

        return db_task

    def delete_task(self, task_id: int):
        """Удаление задания (DELETE)"""
        db_task = self.db.query(Task).filter_by(id=task_id).first()
        if db_task:
            self.db.delete(db_task)
            self.db.commit()

        return db_task

    def get_important_tasks(self):
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







        # important_tasks = (
        #     self.db.query(Task)
        #     .filter(
        #         and_(
        #             Task.status == TaskStatus.NOT_STARTED,
        #             Task.parent_task.has(Task.status == TaskStatus.STARTED))
        #     )
        #     .options(joinedload(Task.executor))
        #     .all()
        # )
        #
        # results = []
        # for important_task in important_tasks:
        #     if important_task not in results:
        #         executors = []
        #
        #         if important_task.executor_id:
        #
        #             parent_task_executor = important_task.parent_task.executor
        #             if parent_task_executor and (
        #                     parent_task_executor.tasks.count() <= 2
        #             ):
        #                 executors.append(parent_task_executor.fullname)
        #
        #             if not executors:
        #                 least_busy_executor = (
        #                     self.db.query(Employee)
        #                     .select_from(Employee)
        #                     .outerjoin(Task, Employee.id == Task.executor_id)
        #                     .group_by(Employee.id)
        #                     .having(
        #                         min(func.count(Task.id)) <= 2
        #                     )
        #                     .subquery()
        #                 )
        #
        #                 if least_busy_executor:
        #                     executors.append(least_busy_executor.first().fullname)
        #
        #         important_task.executor_names = executors
        #         results.append(important_task)
        #
        # return results

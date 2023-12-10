from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Enum as EnumType, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.models import Base


class TaskStatus(str, Enum):
    NOT_STARTED = 'Not started'
    STARTED = 'Started'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, index=True)
    parent_task_id = Column(Integer, ForeignKey('task.id'), nullable=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    deadline = Column(DateTime, nullable=False)

    status = Column(EnumType(TaskStatus, native_enum=False), default=TaskStatus.NOT_STARTED)
    executor_id = Column(Integer, ForeignKey('employee.id'))

    # Relationships
    parent_task = relationship('Task', remote_side='Task.id', backref='subtasks')
    executor = relationship('Employee', back_populates='tasks')

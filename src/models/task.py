from datetime import datetime

from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from src.db.database import Base


class Task(Base):
    STATUSES = [
        'Not started',
        'Started',
        'Completed',
        'Cancelled'
    ]

    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, index=True)
    parent_task_id = Column(Integer, ForeignKey('task.id'))

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    deadline = Column(DateTime, nullable=False)

    status = Column(ChoiceType(STATUSES), default='Not started')
    executor_id = Column(Integer, ForeignKey('employees.id'))

    # Relationships
    parent_task = relationship('Task', remote_side='Task.id', backref='subtasks')
    executor = relationship('Employee', back_populates='tasks')

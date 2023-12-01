from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from src.models import Base


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True, nullable=False)
    position = Column(String, nullable=False)
    is_busy = Column(Boolean, default=False)

    # Relationships
    tasks = relationship('Task', back_populates='executor')

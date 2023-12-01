from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

from src.db.database import Base


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True, nullable=False)
    position = Column(String, nullable=False)

    # Relationships
    tasks = relationship('Task', back_populates='executor')

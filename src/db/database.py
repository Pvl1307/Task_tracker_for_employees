from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import DATABASE_URL

SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

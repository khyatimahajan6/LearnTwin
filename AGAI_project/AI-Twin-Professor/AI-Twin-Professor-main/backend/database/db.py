"""
database/db.py

Sets up the SQLAlchemy engine, session factory, and declarative Base
class used by every ORM model in this project.

Why SQLite?
    - No separate database server needs to be installed/run.
    - The entire database lives in a single file: `learntwin.db`.
    - Perfect for a Final Year Project / prototype.

If the team later wants to move to PostgreSQL/MySQL for production,
only the `DATABASE_URL` in config.py needs to change — nothing else in
the codebase depends on SQLite specifically.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import DATABASE_URL


# `connect_args={"check_same_thread": False}` is required ONLY for
# SQLite. FastAPI can handle a single request across multiple threads,
# and SQLite normally forbids sharing a connection across threads —
# this flag disables that restriction safely for our use case.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SessionLocal is a *factory* — calling SessionLocal() creates a new
# database session. Each incoming HTTP request gets its own session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All ORM models (Student, Lecture, ...) inherit from this Base class.
# SQLAlchemy uses it to keep track of every table that needs to be created.
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a database session and guarantees
    it is closed afterwards, even if the request raises an exception.

    Usage in a route:
        def my_route(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Creates all database tables from the ORM models.
    """
    from models.student import Student
    from models.lecture import Lecture

    Base.metadata.create_all(bind=engine)
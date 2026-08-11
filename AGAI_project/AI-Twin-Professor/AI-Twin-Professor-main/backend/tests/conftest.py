import os
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure the test database is isolated from the main backend DB.
TEST_DB_PATH = Path(__file__).parent / "test_learntwin.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH.resolve()}"

from database.db import Base, engine, SessionLocal
from main import app
from models.student import Student
from services.auth_service import create_access_token, hash_password


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
    Base.metadata.create_all(bind=engine)
    yield
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def verified_student(db_session):
    student = Student(
        full_name="Test Student",
        email=f"student+{uuid.uuid4().hex}@example.com",
        hashed_password=hash_password("password123"),
        email_verified=True,
    )
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    return student


@pytest.fixture()
def auth_header(verified_student):
    token = create_access_token({"sub": verified_student.student_id})
    return {"Authorization": f"Bearer {token}"}

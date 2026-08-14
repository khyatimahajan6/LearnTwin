"""
models/student.py

Defines the `Student` table — a registered user of LearnTwin AI Professor.
Students log in to upload lecture files and view their upload history.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from database.db import Base


class Student(Base):
    """
    ORM model mapped to the "students" table.

    Columns:
        id (int):              Internal auto-increment primary key.
        student_id (str):      Public UUID used in API responses/tokens
                                (kept separate from `id` so we never leak
                                sequential database IDs to clients).
        full_name (str):       Student's display name.
        email (str):           Unique email address, used as the login
                                username.
        hashed_password (str): Bcrypt hash of the password. The plain
                                password is NEVER stored.
        created_at (datetime): Account creation timestamp (UTC).
    """

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(
        String, unique=True, index=True, default=lambda: str(uuid.uuid4())
    )
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    email_verified = Column(Boolean, default=False, nullable=False)
    otp_code = Column(String, nullable=True)
    otp_expires_at = Column(DateTime, nullable=True)

    # A student can have many uploaded lectures.
    # `back_populates` keeps both sides of the relationship in sync.
    lectures = relationship("Lecture", back_populates="student")
    test_results = relationship(
    "TestResult",
    back_populates="student",
    cascade="all, delete-orphan"
)

"""
models/test_result.py

Stores the result of every test/quiz attempted by a student.

The Adaptive Engine uses these results to:
- calculate recent performance
- detect repeated low scores
- detect diagram-based weaknesses
- select an appropriate teaching strategy
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Boolean,
)

from sqlalchemy.orm import relationship

from database.db import Base


class TestResult(Base):
    """
    ORM model mapped to the "test_results" table.
    """

    __tablename__ = "test_results"

    # --------------------------------------------------------
    # PRIMARY KEY
    # --------------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Public unique ID for this test result
    test_id = Column(
        String,
        unique=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )

    # --------------------------------------------------------
    # STUDENT RELATIONSHIP
    # --------------------------------------------------------

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
        index=True
    )

    student = relationship(
        "Student",
        back_populates="test_results"
    )

    # --------------------------------------------------------
    # TEST INFORMATION
    # --------------------------------------------------------

    topic = Column(
        String,
        nullable=True,
        index=True
    )

    test_name = Column(
        String,
        nullable=True
    )

    # --------------------------------------------------------
    # SCORE INFORMATION
    # --------------------------------------------------------

    score = Column(
        Float,
        nullable=False
    )

    total_marks = Column(
        Float,
        nullable=False
    )

    percentage = Column(
        Float,
        nullable=False
    )

    # --------------------------------------------------------
    # DIAGRAM-BASED PERFORMANCE
    # --------------------------------------------------------

    diagram_questions = Column(
        Integer,
        default=0,
        nullable=False
    )

    diagram_correct = Column(
        Integer,
        default=0,
        nullable=False
    )

    # --------------------------------------------------------
    # PERFORMANCE FLAGS
    # --------------------------------------------------------

    passed = Column(
        Boolean,
        default=False,
        nullable=False
    )

    # --------------------------------------------------------
    # TIMESTAMP
    # --------------------------------------------------------

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
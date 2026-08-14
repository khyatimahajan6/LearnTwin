"""
models/lecture.py

Defines the `Lecture` table — one row per uploaded file. Stores both
the file's metadata (size, page count, timestamps) and its processing
status, so the frontend can poll / display upload history.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON

from sqlalchemy.orm import relationship

from database.db import Base
from config import STATUS_UPLOADING


class Lecture(Base):
    """
    ORM model mapped to the "lectures" table.

    Columns:
        id (int):                   Internal auto-increment primary key.
        lecture_id (str):           Public UUID identifying this upload.
        student_id (str):           FK -> students.student_id (owner).
        filename (str):              Original filename as uploaded.
        file_type (str):            Detected type: "pdf" | "docx" | "pptx".
        file_size_kb (int):         Size of the uploaded file, in KB.
        page_count (int | None):    Number of pages/slides (None when the
                                     file type has no meaningful page count,
                                     e.g. some DOCX files).
        upload_time (datetime):     When the file was uploaded (UTC).
        processing_status (str):    One of Uploading / Extracting /
                                     Completed / Failed.
        extracted_text_path (str):  Path to the saved .txt file containing
                                     the merged extracted text.
        error_message (str | None): Populated only if processing failed —
                                     helps with debugging corrupted files.
    """

    __tablename__ = "lectures"

    id = Column(Integer, primary_key=True, index=True)
    lecture_id = Column(
        String, unique=True, index=True, default=lambda: str(uuid.uuid4())
    )
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)

    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size_kb = Column(Integer, nullable=True)
    page_count = Column(Integer, nullable=True)

    upload_time = Column(DateTime, default=datetime.utcnow)
    processing_status = Column(String, default=STATUS_UPLOADING)
    extracted_text_path = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
        # ============================================================
    # NLP METADATA
    # ============================================================

    topic = Column(String, nullable=True)

    subtopics = Column(JSON, nullable=True)

    keywords = Column(JSON, nullable=True)

    difficulty = Column(String, nullable=True)

    learning_objectives = Column(JSON, nullable=True)

    prerequisites = Column(JSON, nullable=True)

    summary = Column(Text, nullable=True)
    # Many lectures belong to a single student.
    student = relationship("Student", back_populates="lectures")

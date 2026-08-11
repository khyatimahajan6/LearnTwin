"""
schemas/lecture_schema.py

Pydantic models describing the JSON shape of upload / history responses.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UploadResponse(BaseModel):
    """
    Shape of the JSON returned by POST /upload — exactly matches the
    spec required by the project:
        {
          "lecture_id": "...",
          "filename": "...",
          "file_type": "...",
          "raw_text": "...",
          "clean_text": "...",
          "status": "Processed"
        }
    """
    lecture_id: str
    filename: str
    file_type: str
    raw_text: str
    clean_text: Optional[str] = None
    status: str


class LectureHistoryItem(BaseModel):
    """A single row returned by GET /history."""
    lecture_id: str
    student_id: str
    filename: str
    file_type: str
    file_size_kb: Optional[int] = None
    page_count: Optional[int] = None
    upload_time: datetime
    processing_status: str
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Standard error payload shape used across the API."""
    detail: str

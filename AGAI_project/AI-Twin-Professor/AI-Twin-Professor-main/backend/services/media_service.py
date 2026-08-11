import os
from typing import Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException

from config import STATUS_COMPLETED, STATUS_EXTRACTING, STATUS_FAILED
from database.db import get_db
from models.lecture import Lecture
from services.file_service import save_uploaded_file, get_file_size_kb
from audio_processing.pipeline import process_lecture
from services.auth_service import get_current_student
from utils.validators import FileValidationError, validate_media_upload, validate_youtube_url
from utils.logger import get_logger

logger = get_logger(__name__)


class MediaProcessingError(Exception):
    pass


def _load_existing_document_text(lecture: Lecture) -> Optional[str]:
    if lecture.extracted_text_path and os.path.exists(lecture.extracted_text_path):
        with open(lecture.extracted_text_path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def _create_lecture_record(db: Session, student_id: str, filename: str, file_size_kb: int, file_type: str) -> Lecture:
    lecture = Lecture(
        student_id=student_id,
        filename=filename,
        file_type=file_type,
        file_size_kb=file_size_kb,
        processing_status=STATUS_EXTRACTING,
    )
    db.add(lecture)
    db.commit()
    db.refresh(lecture)
    return lecture


def _update_failure(db: Session, lecture: Lecture, message: str) -> None:
    lecture.processing_status = STATUS_FAILED
    lecture.error_message = message
    db.commit()


def _update_success(db: Session, lecture: Lecture) -> None:
    lecture.processing_status = STATUS_COMPLETED
    db.commit()


def process_media_upload(
    db: Session,
    student_id: str,
    filename: Optional[str] = None,
    file_bytes: Optional[bytes] = None,
    youtube_url: Optional[str] = None,
    lecture_id: Optional[str] = None,
):
    existing_lecture = None
    document_text = None
    try:
        if youtube_url:
            validate_youtube_url(youtube_url)

        if file_bytes and filename:
            validate_media_upload(filename, file_bytes)

        if lecture_id:
            existing_lecture = db.query(Lecture).filter_by(lecture_id=lecture_id, student_id=student_id).first()
            if not existing_lecture:
                raise HTTPException(status_code=404, detail="Lecture ID not found.")
            document_text = _load_existing_document_text(existing_lecture)
        if youtube_url:
            if existing_lecture:
                lecture = existing_lecture
                lecture.processing_status = STATUS_EXTRACTING
                db.commit()
            else:
                lecture = _create_lecture_record(db, student_id, "youtube_url", 0, "youtube")

            result = process_lecture(
                source_type="youtube",
                input_data=youtube_url,
                lecture_id=lecture.lecture_id,
                document_data={
                    "lecture_id": lecture.lecture_id,
                    "source": "youtube",
                    "text": document_text,
                }
                if document_text
                else None,
            )
        else:
            upload_path = save_uploaded_file(filename, file_bytes)
            file_type = os.path.splitext(filename)[1].lower().lstrip(".")
            if existing_lecture:
                lecture = existing_lecture
                lecture.filename = filename
                lecture.file_type = file_type
                lecture.file_size_kb = get_file_size_kb(file_bytes)
                lecture.processing_status = STATUS_EXTRACTING
                db.commit()
            else:
                lecture = _create_lecture_record(
                    db,
                    student_id,
                    filename,
                    get_file_size_kb(file_bytes),
                    file_type,
                )

            source_type = "audio" if file_type in {"mp3", "wav", "m4a"} else "video"
            result = process_lecture(
                source_type=source_type,
                input_data=upload_path,
                lecture_id=lecture.lecture_id,
                document_data={
                    "lecture_id": lecture.lecture_id,
                    "source": source_type,
                    "text": document_text,
                }
                if document_text
                else None,
            )

        _update_success(db, lecture)
    except HTTPException:
        raise
    except FileValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.message)
    except Exception as exc:
        error_message = str(exc)
        if existing_lecture:
            _update_failure(db, existing_lecture, error_message)
        elif 'lecture' in locals():
            _update_failure(db, lecture, error_message)
        logger.error("Media processing failed: %s", error_message)
        raise HTTPException(status_code=422, detail=f"Media processing failed: {error_message}")

    return {
        "lecture_id": result.lecture_id,
        "source": result.source,
        "document_text": result.document_text,
        "transcript": result.transcript,
        "timestamps": [segment.model_dump() for segment in result.timestamps],
        "combined_text": result.combined_text,
    }

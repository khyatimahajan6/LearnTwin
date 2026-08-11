"""
routes/upload_routes.py

The core endpoint of the whole project: POST /upload

Accepts a PDF, DOCX, or PPTX file, validates it, extracts its text,
stores everything, and returns the extracted text as JSON.
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.student import Student
from schemas.lecture_schema import UploadResponse
from services.auth_service import get_current_student
from services.lecture_service import process_uploaded_file
from utils.validators import FileValidationError
from services.extraction_service import ExtractionError
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["Upload"])


@router.post(
    "/upload",
    response_model=UploadResponse,
    summary="Upload a lecture file (PDF, DOCX, or PPTX) and extract its text",
)
async def upload_file(
    file: UploadFile = File(..., description="The lecture file to upload (.pdf, .docx, .pptx)"),
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student),
):
    """
    Full upload pipeline:
        1. Read file bytes.
        2. Validate (type / size / not empty).
        3. Save raw file to /uploads.
        4. Detect file type and extract text (pdf/docx/pptx).
        5. Merge extracted text and save it to /extracted_text/{lecture_id}.txt.
        6. Persist a Lecture row (status: Uploading -> Extracting -> Completed/Failed).
        7. Return the JSON response required by the project spec.

    Requires a valid JWT (student must be logged in) — see /auth/login.
    """
    # Read the raw bytes ONCE. UploadFile is a stream, so we cannot
    # read it twice without seeking back to the start.
    file_bytes = await file.read()

    try:
        lecture = process_uploaded_file(
            db=db,
            student_id=current_student.student_id,
            filename=file.filename,
            file_bytes=file_bytes,
        )
    except FileValidationError as exc:
        # Bad request — the client sent something we can't accept.
        logger.warning("Upload rejected for student %s: %s", current_student.student_id, exc.message)
        raise HTTPException(status_code=400, detail=exc.message)
    except ExtractionError as exc:
        # The file was valid (right type/size) but its CONTENT is
        # corrupted/unreadable. We return 422 Unprocessable Entity.
        logger.error("Extraction failed for student %s: %s", current_student.student_id, exc.message)
        raise HTTPException(status_code=422, detail=f"Failed to process file: {exc.message}")
    except Exception as exc:
        # Catch-all safety net for any unexpected error, so the API
        # never leaks a raw stack trace to the client.
        logger.exception("Unexpected error while processing upload: %s", exc)
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")

    return UploadResponse(
        lecture_id=lecture.lecture_id,
        filename=lecture.filename,
        file_type=lecture.file_type,
        raw_text=lecture.raw_text,
        status="Processed",
    )

"""
services/lecture_service.py

The "orchestrator" for the upload pipeline. This is the module that
routes/upload_routes.py calls — it ties together validation, file
storage, text extraction, and database record-keeping into one clean
function: `process_uploaded_file()`.

Pipeline steps (each one updates `processing_status` in the DB):
    1. Uploading  -> create Lecture row, save raw file to /uploads
    2. Extracting -> run the appropriate extractor (pdf/docx/pptx)
    3. Completed  -> save extracted text to /extracted_text, update row
       (or)
    3. Failed     -> store the error message, keep the row for history
"""

from sqlalchemy.orm import Session

from config import STATUS_UPLOADING, STATUS_EXTRACTING, STATUS_COMPLETED, STATUS_FAILED
from models.lecture import Lecture
from services.file_service import save_uploaded_file, save_extracted_text, get_file_size_kb
from services.extraction_service import ExtractionError
from preprocessing.main import process_lecture_file
from utils.validators import detect_file_type, validate_upload, FileValidationError
from utils.logger import get_logger

logger = get_logger(__name__)


def process_uploaded_file(db: Session, student_id: str, filename: str, file_bytes: bytes) -> Lecture:
    """
    Runs the full upload -> extract -> save pipeline for one file and
    returns the final Lecture database record.

    Args:
        db: Active SQLAlchemy session.
        student_id: The UUID of the student who is uploading.
        filename: Original filename from the client.
        file_bytes: Raw bytes of the uploaded file.

    Raises:
        FileValidationError: if the file fails validation (bad type,
            empty, or too large). Raised BEFORE any DB row is created,
            so no "junk" history entries are left behind for rejected
            uploads.
        ExtractionError: if the file passes validation but its content
            cannot be parsed (e.g. corrupted). In this case a Lecture
            row IS created and marked "Failed" so it still shows up in
            history for transparency/debugging.
    """
    # ------------------------------------------------------------------
    # STEP 0: Validate the file BEFORE touching the database or disk.
    # ------------------------------------------------------------------
    validate_upload(filename, file_bytes)
    file_type = detect_file_type(filename)

    # ------------------------------------------------------------------
    # STEP 1: status = Uploading — create the Lecture row and save the
    # raw file to disk.
    # ------------------------------------------------------------------
    lecture = Lecture(
        student_id=student_id,
        filename=filename,
        file_type=file_type,
        file_size_kb=get_file_size_kb(file_bytes),
        processing_status=STATUS_UPLOADING,
    )
    db.add(lecture)
    db.commit()
    db.refresh(lecture)
    logger.info("Lecture %s created for student %s, status=Uploading", lecture.lecture_id, student_id)

    saved_path = save_uploaded_file(filename, file_bytes)

    # ------------------------------------------------------------------
    # STEP 2: status = Extracting — attempt to pull text out of the file.
    # ------------------------------------------------------------------
    lecture.processing_status = STATUS_EXTRACTING
    db.commit()
    logger.info("Lecture %s status=Extracting", lecture.lecture_id)

    try:
        from services.extraction_service import extract_text
        from utils.text_cleaner import clean_text as new_clean_text

        raw_text, page_count = extract_text(saved_path, file_type)
        clean_text = new_clean_text(raw_text)

        if not clean_text.strip():
            raise ExtractionError("No extractable text found.")

    except ExtractionError as exc:
        lecture.processing_status = STATUS_FAILED
        lecture.error_message = exc.message
        db.commit()
        logger.error(
            "Lecture %s extraction failed: %s",
            lecture.lecture_id,
            exc.message,
        )
        raise

    except Exception as exc:
        lecture.processing_status = STATUS_FAILED
        lecture.error_message = str(exc)
        db.commit()
        logger.error(
            "Lecture %s extraction failed: %s",
            lecture.lecture_id,
            exc,
        )
        raise ExtractionError(str(exc))

    # ------------------------------------------------------------------
    # STEP 3 (success path): status = Completed — save extracted text
    # and update remaining metadata.
    # ------------------------------------------------------------------
    text_path = save_extracted_text(lecture.lecture_id, clean_text)

    lecture.page_count = page_count
    lecture.extracted_text_path = text_path
    lecture.processing_status = STATUS_COMPLETED
    db.commit()
    db.refresh(lecture)
    logger.info("Lecture %s status=Completed (page_count=%s)", lecture.lecture_id, page_count)

    # Stash both raw and clean text on the object temporarily so the route can
    # return them in the JSON response without re-reading the file from disk.
    lecture.raw_text = raw_text
    lecture.clean_text = clean_text
    return lecture

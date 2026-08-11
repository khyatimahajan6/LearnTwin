
"""
routes/upload_routes.py

Core endpoints of the LearnTwin AI Professor project.

Endpoints:

    POST /upload
        Upload PDF, DOCX, PPTX, audio, or video files.

    POST /upload-youtube
        Download audio from a YouTube URL and process it
        through the existing audio/Whisper pipeline.

Supported files:

Documents:
    PDF
    DOCX
    PPTX

Audio:
    MP3
    WAV
    M4A
    AAC
    FLAC
    OGG

Video:
    MP4
    WEBM
    MKV
    AVI
    MOV
"""

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
)

from pydantic import BaseModel

from sqlalchemy.orm import Session

from database.db import get_db
from models.student import Student

from schemas.lecture_schema import UploadResponse

from services.auth_service import get_current_student
from services.lecture_service import process_uploaded_file
from services.extraction_service import ExtractionError
from services.youtube_service import download_youtube_audio

from utils.validators import FileValidationError
from utils.logger import get_logger


# ============================================================
# LOGGER
# ============================================================

logger = get_logger(__name__)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    tags=["Upload"]
)


# ============================================================
# YOUTUBE REQUEST MODEL
# ============================================================

class YouTubeUploadRequest(BaseModel):
    """
    Request body for YouTube lecture upload.
    """

    url: str


# ============================================================
# HELPER — BUILD UPLOAD RESPONSE
# ============================================================

def build_upload_response(lecture) -> UploadResponse:
    """
    Convert the processed Lecture object into the API response.

    The lecture_service attaches the complete preprocessing result
    to the Lecture object.

    For documents:

        clean_text / raw_text
            ↓
        combined_text

    For audio/video:

        transcript
        timestamps
        combined_text

    This helper keeps the response format identical for:

        POST /upload
        POST /upload-youtube
    """

    return UploadResponse(

        lecture_id=str(
            lecture.lecture_id
        ),

        filename=lecture.filename,

        file_type=lecture.file_type,

        source=getattr(
            lecture,
            "source",
            None,
        ),

        document_text=getattr(
            lecture,
            "document_text",
            None,
        ),

        transcript=getattr(
            lecture,
            "transcript",
            None,
        ),

        timestamps=getattr(
            lecture,
            "timestamps",
            None,
        ),

        combined_text=getattr(
            lecture,
            "combined_text",
            None,
        ),

        status="Processed",
    )


# ============================================================
# FILE UPLOAD ENDPOINT
# ============================================================

@router.post(
    "/upload",

    response_model=UploadResponse,

    summary="Upload and process a lecture",

    description="""
Upload a lecture file and automatically process it.

### Supported document files

- PDF
- DOCX
- PPTX

### Supported audio files

- MP3
- WAV
- M4A
- AAC
- FLAC
- OGG

### Supported video files

- MP4
- WEBM
- MKV
- AVI
- MOV

### Processing pipeline

**Documents**

File → Text Extraction → Text Cleaning → Completed

**Audio**

Audio → Faster-Whisper → Timestamped Transcript → Text Cleaning → Completed

**Video**

Video → Audio Extraction → Faster-Whisper → Timestamped Transcript → Text Cleaning → Completed

The final processed text is saved in the `extracted_text` directory.

Authentication is required.
Student must be logged in and provide a valid JWT.
""",
)
async def upload_file(

    file: UploadFile = File(
        ...,

        description=(
            "Upload a lecture file: "
            "PDF, DOCX, PPTX, MP3, WAV, M4A, AAC, "
            "FLAC, OGG, MP4, WEBM, MKV, AVI, or MOV"
        ),
    ),

    db: Session = Depends(
        get_db
    ),

    current_student: Student = Depends(
        get_current_student
    ),
):
    """
    Complete lecture upload pipeline.

    Steps:

        1. Read uploaded file
        2. Validate file type
        3. Validate file size
        4. Create Lecture database record
        5. Save original uploaded file
        6. Detect file type
        7. Process document/audio/video
        8. Generate or extract text
        9. Generate timestamps for media
        10. Clean the text
        11. Save extracted text
        12. Update Lecture status
        13. Return complete processed lecture
    """

    # ============================================================
    # STEP 1 — CHECK FILENAME
    # ============================================================

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    logger.info(
        "Upload received: %s",
        file.filename,
    )

    # ============================================================
    # STEP 2 — READ FILE
    # ============================================================

    try:

        file_bytes = await file.read()

    except Exception as exc:

        logger.exception(
            "Failed to read uploaded file: %s",
            exc,
        )

        raise HTTPException(
            status_code=400,
            detail="Unable to read uploaded file.",
        )

    # ============================================================
    # STEP 3 — PROCESS COMPLETE LECTURE
    # ============================================================

    try:

        lecture = process_uploaded_file(

            db=db,

            student_id=current_student.student_id,

            filename=file.filename,

            file_bytes=file_bytes,
        )

    # ============================================================
    # STEP 4 — VALIDATION ERROR
    # ============================================================

    except FileValidationError as exc:

        logger.warning(

            "Upload rejected for student %s: %s",

            current_student.student_id,

            exc.message,
        )

        raise HTTPException(

            status_code=400,

            detail=exc.message,
        )

    # ============================================================
    # STEP 5 — PROCESSING / EXTRACTION ERROR
    # ============================================================

    except ExtractionError as exc:

        logger.error(

            "Lecture processing failed for student %s: %s",

            current_student.student_id,

            exc.message,
        )

        raise HTTPException(

            status_code=422,

            detail=(
                f"Failed to process lecture: "
                f"{exc.message}"
            ),
        )

    # ============================================================
    # STEP 6 — UNEXPECTED ERROR
    # ============================================================

    except Exception as exc:

        logger.exception(

            "Unexpected error while processing upload: %s",

            exc,
        )

        raise HTTPException(

            status_code=500,

            detail=(
                "An unexpected server error occurred."
            ),
        )

    # ============================================================
    # STEP 7 — RETURN COMPLETE RESPONSE
    # ============================================================

    return build_upload_response(
        lecture
    )


# ============================================================
# YOUTUBE UPLOAD ENDPOINT
# ============================================================

@router.post(
    "/upload-youtube",

    response_model=UploadResponse,

    summary="Upload a lecture from YouTube",

    description="""
Download audio from a YouTube video and process it
through the existing lecture audio pipeline.

### Processing pipeline

YouTube URL
→ yt-dlp
→ MP3
→ Existing lecture pipeline
→ Faster-Whisper
→ Timestamped Transcript
→ Transcript Cleaning
→ Save extracted text
→ Completed

Authentication is required.
Student must be logged in and provide a valid JWT.
""",
)
async def upload_youtube(

    request: YouTubeUploadRequest,

    db: Session = Depends(
        get_db
    ),

    current_student: Student = Depends(
        get_current_student
    ),
):
    """
    Process a lecture directly from a YouTube URL.

    Steps:

        1. Validate YouTube URL
        2. Download audio using yt-dlp
        3. Convert audio to MP3 using FFmpeg
        4. Pass MP3 bytes to existing lecture pipeline
        5. Run Whisper transcription
        6. Generate timestamped segments
        7. Clean transcript
        8. Save extracted text
        9. Update Lecture status
        10. Return complete processed lecture
    """

    # ============================================================
    # STEP 1 — CHECK URL
    # ============================================================

    youtube_url = request.url.strip()

    if not youtube_url:

        raise HTTPException(
            status_code=400,
            detail="YouTube URL is required.",
        )

    logger.info(
        "YouTube URL received from student %s: %s",

        current_student.student_id,

        youtube_url,
    )

    # ============================================================
    # STEP 2 — DOWNLOAD YOUTUBE AUDIO
    # ============================================================

    try:

        filename, file_bytes = download_youtube_audio(
            youtube_url
        )

    except Exception as exc:

        logger.exception(
            "Failed to download YouTube audio: %s",
            exc,
        )

        raise HTTPException(

            status_code=422,

            detail=(
                f"Failed to download YouTube audio: "
                f"{str(exc)}"
            ),
        )

    # ============================================================
    # STEP 3 — CHECK DOWNLOADED FILE
    # ============================================================

    if not file_bytes:

        logger.error(
            "YouTube download returned empty file."
        )

        raise HTTPException(

            status_code=422,

            detail=(
                "YouTube audio download returned "
                "an empty file."
            ),
        )

    logger.info(
        "YouTube audio downloaded successfully: "
        "filename=%s, size=%s bytes",

        filename,

        len(file_bytes),
    )

    # ============================================================
    # STEP 4 — PROCESS USING EXISTING PIPELINE
    # ============================================================

    try:

        lecture = process_uploaded_file(

            db=db,

            student_id=current_student.student_id,

            filename=filename,

            file_bytes=file_bytes,
        )

    # ============================================================
    # STEP 5 — VALIDATION ERROR
    # ============================================================

    except FileValidationError as exc:

        logger.warning(

            "YouTube file validation failed "
            "for student %s: %s",

            current_student.student_id,

            exc.message,
        )

        raise HTTPException(

            status_code=400,

            detail=exc.message,
        )

    # ============================================================
    # STEP 6 — PROCESSING / EXTRACTION ERROR
    # ============================================================

    except ExtractionError as exc:

        logger.error(

            "YouTube lecture processing failed "
            "for student %s: %s",

            current_student.student_id,

            exc.message,
        )

        raise HTTPException(

            status_code=422,

            detail=(
                f"Failed to process YouTube lecture: "
                f"{exc.message}"
            ),
        )

    # ============================================================
    # STEP 7 — UNEXPECTED ERROR
    # ============================================================

    except Exception as exc:

        logger.exception(

            "Unexpected YouTube processing error: %s",

            exc,
        )

        raise HTTPException(

            status_code=500,

            detail=(
                "An unexpected server error occurred "
                "while processing the YouTube lecture."
            ),
        )

    # ============================================================
    # STEP 8 — RETURN COMPLETE RESPONSE
    # ============================================================

    return build_upload_response(
        lecture
    )

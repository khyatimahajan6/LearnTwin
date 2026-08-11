from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.student import Student
from schemas.media_schema import MediaUploadResponse
from services.auth_service import get_current_student
from services.media_service import process_media_upload
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["Media Upload"])


@router.post(
    "/upload/media",
    response_model=MediaUploadResponse,
    summary="Upload an audio/video file or a YouTube URL for transcription",
)
async def upload_media(
    media_file: UploadFile | None = File(
        None,
        description="The audio or video file to upload (mp3, wav, m4a, mp4, mkv)",
    ),
    youtube_url: str | None = Form(
        None,
        description="The YouTube URL to transcribe if no file is uploaded.",
    ),
    lecture_id: str | None = Form(
        None,
        description="Optional existing lecture_id to attach this media to.",
    ),
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student),
):
    if not media_file and not youtube_url:
        raise HTTPException(status_code=400, detail="Either media_file or youtube_url must be provided.")

    if media_file and youtube_url:
        raise HTTPException(status_code=400, detail="Provide either media_file or youtube_url, not both.")

    file_bytes = await media_file.read() if media_file else None
    filename = media_file.filename if media_file else None

    try:
        result = process_media_upload(
            db=db,
            student_id=current_student.student_id,
            filename=filename,
            file_bytes=file_bytes,
            youtube_url=youtube_url,
            lecture_id=lecture_id,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected media upload error: %s", exc)
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")

    return result

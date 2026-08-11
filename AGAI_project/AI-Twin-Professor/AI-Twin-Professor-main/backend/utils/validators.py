"""
utils/validators.py

Reusable validation helpers and custom exception classes for file
uploads. Keeping validation logic here (instead of inline in the
route) keeps `routes/upload_routes.py` short and readable.
"""

import os
from urllib.parse import urlparse

from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_BYTES, EXTENSION_TO_TYPE
from audio_processing.config import SUPPORTED_AUDIO_EXTENSIONS, SUPPORTED_VIDEO_EXTENSIONS, SUPPORTED_SOURCE_TYPES


class FileValidationError(Exception):
    """
    Raised whenever an uploaded file fails validation
    (wrong extension, too large, or empty).

    We use a custom exception (rather than raising HTTPException
    directly inside a service) so that the *service layer* stays
    framework-agnostic — only the *route layer* knows about FastAPI's
    HTTPException. This is a clean-architecture best practice.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def get_file_extension(filename: str) -> str:
    """Returns the lowercase file extension including the dot, e.g. '.pdf'."""
    return os.path.splitext(filename)[1].lower()


def detect_file_type(filename: str) -> str:
    """
    Maps a filename's extension to a friendly type string used
    throughout the API ("pdf", "docx", "pptx").

    Raises:
        FileValidationError: if the extension is not supported.
    """
    ext = get_file_extension(filename)
    if ext not in EXTENSION_TO_TYPE:
        raise FileValidationError(
            f"Unsupported file type '{ext}'. Allowed types: "
            f"{', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )
    return EXTENSION_TO_TYPE[ext]


def validate_upload(filename: str, file_bytes: bytes) -> None:
    """
    Runs all validation checks required BEFORE we attempt to save or
    process an uploaded file:
        1. Extension must be one of .pdf / .docx / .pptx
        2. File must not be empty (0 bytes)
        3. File must not exceed the 20 MB size limit

    Raises:
        FileValidationError: with a human-readable message describing
        exactly what went wrong, so the API can return a clear 400
        error to the frontend.
    """
    # --- 1. Extension check -------------------------------------------------
    ext = get_file_extension(filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise FileValidationError(
            f"File type '{ext or 'unknown'}' is not supported. "
            f"Only PDF, DOCX, and PPTX files are allowed."
        )

    # --- 2. Empty file check -------------------------------------------------
    if len(file_bytes) == 0:
        raise FileValidationError("The uploaded file is empty.")

    # --- 3. Max size check -----------------------------------------------
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        size_mb = len(file_bytes) / (1024 * 1024)
        raise FileValidationError(
            f"File is too large ({size_mb:.2f} MB). "
            f"Maximum allowed size is 20 MB."
        )


def validate_media_upload(filename: str, file_bytes: bytes) -> None:
    ext = get_file_extension(filename)
    if ext not in {f".{x}" for x in SUPPORTED_AUDIO_EXTENSIONS | SUPPORTED_VIDEO_EXTENSIONS}:
        allowed = ", ".join(sorted(f".{x}" for x in SUPPORTED_AUDIO_EXTENSIONS | SUPPORTED_VIDEO_EXTENSIONS))
        raise FileValidationError(
            f"Media type '{ext or 'unknown'}' is not supported. "
            f"Only audio/video files are allowed: {allowed}."
        )

    if len(file_bytes) == 0:
        raise FileValidationError("The uploaded file is empty.")

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        size_mb = len(file_bytes) / (1024 * 1024)
        raise FileValidationError(
            f"File is too large ({size_mb:.2f} MB). "
            f"Maximum allowed size is 20 MB."
        )


def validate_youtube_url(url: str) -> None:
    if not url:
        raise FileValidationError("YouTube URL must not be empty.")

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise FileValidationError("Invalid YouTube URL.")

    hostname = parsed.netloc.lower()
    youtube_domains = {
        "youtube.com",
        "youtu.be",
    }

    def _matches_domain(hostname: str, domain: str) -> bool:
        return hostname == domain or hostname.endswith(f".{domain}")

    if not any(_matches_domain(hostname, domain) for domain in youtube_domains):
        raise FileValidationError("Invalid YouTube URL.")

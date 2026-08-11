"""
main.py

Entry point of the LearnTwin AI Professor backend.

Run from the backend directory:

    python -m uvicorn main:app --reload

Then open:

    http://127.0.0.1:8000/
    http://127.0.0.1:8000/docs
    http://127.0.0.1:8000/redoc
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.db import init_db
from routes import (
    auth_routes,
    upload_routes,
    history_routes,
)

from utils.logger import get_logger


# ============================================================
# LOGGER
# ============================================================

logger = get_logger(__name__)


# ============================================================
# APPLICATION LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.

    Startup:
        - Initialize database
        - Log backend startup

    Shutdown:
        - Log backend shutdown
    """

    # --------------------------------------------------------
    # STARTUP
    # --------------------------------------------------------

    try:

        init_db()

        logger.info(
            "Database initialized successfully."
        )

        logger.info(
            "LearnTwin AI Professor backend "
            "started successfully."
        )

    except Exception as exc:

        logger.exception(
            "Database initialization failed: %s",
            exc,
        )

        raise

    # --------------------------------------------------------
    # APPLICATION RUNNING
    # --------------------------------------------------------

    yield

    # --------------------------------------------------------
    # SHUTDOWN
    # --------------------------------------------------------

    logger.info(
        "LearnTwin AI Professor backend "
        "is shutting down."
    )


# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(

    title=(
        "LearnTwin AI Professor — "
        "Input Processing API"
    ),

    description="""
Backend service for the LearnTwin AI Professor project.

The API handles:

- Student authentication
- Lecture uploads
- PDF extraction
- DOCX extraction
- PPTX extraction
- Audio transcription
- Video audio extraction
- Whisper transcription
- Timestamp generation
- Transcript cleaning
- Combined lecture text generation
- Lecture upload history

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

### YouTube

The backend can also download lecture audio from
a YouTube URL and send it through the same
audio-processing pipeline.
""",

    version="1.0.0",

    lifespan=lifespan,

    swagger_ui_parameters={
        "persistAuthorization": True
    },
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "*"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],
)


# ============================================================
# GLOBAL EXCEPTION HANDLER
# ============================================================

@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Catch unexpected exceptions that are not handled
    by individual routes.

    The complete exception is logged on the backend,
    while the client receives a safe generic message.
    """

    logger.exception(

        "Unhandled exception on %s %s: %s",

        request.method,

        request.url.path,

        exc,
    )

    return JSONResponse(

        status_code=500,

        content={
            "detail": (
                "An unexpected internal server error "
                "occurred."
            )
        },
    )


# ============================================================
# ROUTERS
# ============================================================

# ------------------------------------------------------------
# Authentication
# ------------------------------------------------------------

app.include_router(
    auth_routes.router
)


# ------------------------------------------------------------
# Upload
# ------------------------------------------------------------

app.include_router(
    upload_routes.router
)


# ------------------------------------------------------------
# History
# ------------------------------------------------------------

app.include_router(
    history_routes.router
)


# ============================================================
# ROOT / HEALTH CHECK
# ============================================================

@app.get(

    "/",

    tags=[
        "Health"
    ],

    summary="Health check",

)
def root():
    """
    Simple endpoint to verify that the backend is running.
    """

    return {

        "status": "ok",

        "service": (
            "LearnTwin AI Professor - "
            "Input Processing API"
        ),

        "version": "1.0.0",

        "docs": "/docs",

        "redoc": "/redoc",
    }


# ============================================================
# DETAILED HEALTH CHECK
# ============================================================

@app.get(

    "/health",

    tags=[
        "Health"
    ],

    summary="Detailed health check",

)
def health_check():
    """
    Detailed health-check endpoint.
    """

    return {

        "status": "healthy",

        "service": (
            "LearnTwin AI Professor"
        ),

        "backend": "running",

    }
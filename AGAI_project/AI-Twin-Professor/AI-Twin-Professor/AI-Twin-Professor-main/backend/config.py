"""
config.py

Central configuration file for the LearnTwin AI Professor backend.

Keeping all constants (file paths, size limits, security keys, allowed
file types) in ONE place makes the project easy to maintain — if you
need to change the max upload size or secret key, you only change it
here instead of hunting through the codebase.
"""

import os

# --------------------------------------------------------------------
# BASE DIRECTORY
# --------------------------------------------------------------------
# Absolute path to the "backend" folder (where this file lives).
# Using an absolute path avoids "file not found" bugs that happen when
# the app is started from a different working directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------
# FOLDER PATHS
# --------------------------------------------------------------------
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
EXTRACTED_TEXT_DIR = os.path.join(BASE_DIR, "extracted_text")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Make sure these folders exist as soon as the app starts.
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACTED_TEXT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------------------------
# FILE VALIDATION RULES
# --------------------------------------------------------------------
# Only these file extensions are accepted by the upload endpoint.
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".pptx"}

# Maps an extension to a friendly "file_type" string returned in the API.
EXTENSION_TO_TYPE = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".pptx": "pptx",
}

# Maximum allowed upload size: 20 MB (expressed in bytes for comparison).
MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024  # 20 MB

# --------------------------------------------------------------------
# PROCESSING STATUS CONSTANTS
# --------------------------------------------------------------------
# Using constants (instead of hardcoded strings scattered everywhere)
# prevents typos like "Completed" vs "completed" from causing bugs.
STATUS_UPLOADING = "Uploading"
STATUS_EXTRACTING = "Extracting"
STATUS_COMPLETED = "Completed"
STATUS_FAILED = "Failed"

# --------------------------------------------------------------------
# SECURITY / AUTH SETTINGS
# --------------------------------------------------------------------
# NOTE: In a real production system, SECRET_KEY must be loaded from an
# environment variable (never hardcoded / committed to source control).
# It is hardcoded here only because this is an academic project.
SECRET_KEY = os.getenv("LEARNTWIN_SECRET_KEY", "learntwin-super-secret-key-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # Tokens are valid for 24 hours

# --------------------------------------------------------------------
# DATABASE
# --------------------------------------------------------------------
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'learntwin.db')}"

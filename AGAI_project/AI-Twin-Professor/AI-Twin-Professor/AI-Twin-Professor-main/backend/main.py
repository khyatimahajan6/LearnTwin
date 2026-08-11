"""
main.py

Entry point of the LearnTwin AI Professor backend (Member 1: Input
Processing & File Handling).

Run this app with:
    uvicorn main:app --reload

Then open:
    http://127.0.0.1:8000/docs   -> interactive Swagger UI
    http://127.0.0.1:8000/redoc  -> ReDoc API documentation
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.db import init_db
from routes import auth_routes, upload_routes, history_routes
from utils.logger import get_logger

logger = get_logger(__name__)

# --------------------------------------------------------------------
# CREATE THE FASTAPI APP
# --------------------------------------------------------------------
app = FastAPI(
    title="LearnTwin AI Professor — Input Processing API",
    description=(
        "Backend service responsible for student authentication, file "
        "upload (PDF/DOCX/PPTX), text extraction, and upload history . "
        
    ),
    version="1.0.0",
    swagger_ui_parmeters={
        "persistAuthorization": True
    }
)

# --------------------------------------------------------------------
# CORS
# --------------------------------------------------------------------
# Allows the frontend (running on a different origin, e.g.
# http://localhost:3000 for React) to call this API from the browser.
# In production, replace "*" with the actual frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------------------------
# STARTUP EVENT — create database tables
# --------------------------------------------------------------------
@app.on_event("startup")
def on_startup():
    """Runs once when the server starts. Creates all DB tables if missing."""
    init_db()
    logger.info("Database initialized. LearnTwin AI Professor backend is starting up...")


# --------------------------------------------------------------------
# GLOBAL EXCEPTION HANDLER
# --------------------------------------------------------------------
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Catches any exception that isn't already handled inside a route,
    logs it, and returns a clean JSON error instead of crashing the
    server or leaking a stack trace to the client.
    """
    logger.exception("Unhandled exception on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected internal server error occurred."},
    )


# --------------------------------------------------------------------
# ROUTERS
# --------------------------------------------------------------------
app.include_router(auth_routes.router)
app.include_router(upload_routes.router)
app.include_router(history_routes.router)


# --------------------------------------------------------------------
# ROOT / HEALTH-CHECK ENDPOINT
# --------------------------------------------------------------------
@app.get("/", tags=["Health"], summary="Health check")
def root():
    """Simple health-check endpoint to confirm the API is running."""
    return {
        "status": "ok",
        "service": "LearnTwin AI Professor - Input Processing API",
        "docs": "/docs",
    }

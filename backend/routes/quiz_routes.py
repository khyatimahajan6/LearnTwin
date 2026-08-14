from __future__ import annotations

from functools import lru_cache

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db

from models.student import Student

from schemas.quiz_schema import (
    QuizGenerateRequest,
    QuizResponse,
    QuizSubmitRequest,
    QuizSubmitResponse,
)

from services.auth_service import get_current_student
from services.quiz_service import QuizService

from rag.services.embedding_service import EmbeddingService
from rag.services.chroma_service import ChromaService
from rag.services.retrieval_service import RetrievalService
from rag.services.context_service import ContextService
from rag.services.llm_service import GeminiService


router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"],
)


# ============================================================
# QUIZ SERVICE FACTORY
# ============================================================

@lru_cache(maxsize=1)
def get_quiz_service() -> QuizService:
    """
    Create and cache the quiz generation service.

    Pipeline:

        Question
            ↓
        Embedding
            ↓
        ChromaDB
            ↓
        Retrieval
            ↓
        Context
            ↓
        Gemini
            ↓
        Quiz
    """

    embedding_service = EmbeddingService()

    vector_store = ChromaService()

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    context_service = ContextService()

    llm_service = GeminiService()

    return QuizService(
        retrieval_service=retrieval_service,
        context_service=context_service,
        llm_service=llm_service,
    )


# ============================================================
# GENERATE QUIZ
# ============================================================

@router.post(
    "/generate",
    response_model=QuizResponse,
)
def generate_quiz(
    request: QuizGenerateRequest,
    current_student: Student = Depends(
        get_current_student
    ),
    db: Session = Depends(get_db),
):
    """
    Generate a quiz from an uploaded lecture.
    """

    quiz_service = get_quiz_service()

    return quiz_service.generate_quiz(
        db=db,
        student=current_student,
        lecture_id=request.lecture_id,
        topic=request.topic,
        number_of_questions=request.number_of_questions,
    )


# ============================================================
# SUBMIT QUIZ
# ============================================================

@router.post(
    "/submit",
    response_model=QuizSubmitResponse,
)
def submit_quiz(
    request: QuizSubmitRequest,
    current_student: Student = Depends(
        get_current_student
    ),
    db: Session = Depends(get_db),
):
    """
    Submit quiz answers.

    The service:
        1. Evaluates answers
        2. Calculates score
        3. Saves TestResult
        4. Returns feedback
    """

    quiz_service = get_quiz_service()

    return quiz_service.submit_quiz(
        db=db,
        student=current_student,
        quiz_id=request.quiz_id,
        answers=request.answers,
    )
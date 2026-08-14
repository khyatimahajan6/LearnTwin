from functools import lru_cache

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from database.db import get_db

from models.student import Student

from services.auth_service import get_current_student
from services.decision_service import DecisionService

from rag.models.rag import (
    RAGQuery,
    RAGResponse,
)

from rag.services.rag_service import RAGService
from rag.services.chroma_service import ChromaService
from rag.services.embedding_service import EmbeddingService
from rag.services.retrieval_service import RetrievalService
from rag.services.context_service import ContextService
from rag.services.prompt_service import PromptService
from rag.services.llm_service import GeminiService

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


# ============================================================
# RAG SERVICE FACTORY
# ============================================================

@lru_cache(maxsize=1)
def get_rag_service() -> RAGService:
    """
    Create and cache the complete RAG pipeline.

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
        Prompt
            ↓
        Gemini
            ↓
        Answer
    """

    embedding_service = EmbeddingService()

    vector_store = ChromaService()

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    context_service = ContextService()

    prompt_service = PromptService()

    llm_service = GeminiService()

    rag_service = RAGService(
        retrieval_service=retrieval_service,
        context_service=context_service,
        prompt_service=prompt_service,
        llm_service=llm_service,
    )

    return rag_service


# ============================================================
# ASK LECTURE
# ============================================================

@router.post(
    "/ask",
    response_model=RAGResponse,
)
def ask_lecture(
    query: RAGQuery,
    current_student: Student = Depends(
        get_current_student
    ),
    db: Session = Depends(get_db),
):
    """
    Ask a question about indexed lecture content.

    Teaching strategy is automatically selected by
    the Adaptive Decision Engine unless the request
    explicitly provides a strategy.
    """

    try:

        # ------------------------------------------
        # STEP 1 — Get RAG service
        # ------------------------------------------

        rag_service = get_rag_service()

        # ------------------------------------------
        # STEP 2 — Select teaching strategy
        # ------------------------------------------

        decision = DecisionService.select_strategy(
            db=db,
            student_db_id=current_student.id,
        )

        selected_strategy = decision["strategy"]

        # ------------------------------------------
        # STEP 3 — Optional manual override
        # ------------------------------------------

        # if query.teaching_strategy:
        #     selected_strategy = (
        #         query.teaching_strategy.strip().lower()
        #     )

        # ------------------------------------------
        # STEP 4 — Generate grounded answer
        # ------------------------------------------

        response = rag_service.answer(
            query=query,
            teaching_strategy=selected_strategy,
        )

        # ------------------------------------------
        # STEP 5 — Return response
        # ------------------------------------------

        return response

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Unable to generate "
                f"RAG response: {exc}"
            ),
        )
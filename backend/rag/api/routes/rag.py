from fastapi import APIRouter

from rag.core.container import ServiceContainer

from rag.models.rag import (
    RAGQuery,
    RAGResponse,
)


router = APIRouter(
    prefix="/api/v1/rag",
    tags=["RAG"]
)


@router.post(
    "/query",
    response_model=RAGResponse
)
def query_rag(
    query: RAGQuery
) -> RAGResponse:

    """
    Ask the AI Professor a question.

    Pipeline:

        Question
            ↓
        Retrieval
            ↓
        Context
            ↓
        LLM
            ↓
        Answer
    """

    container = ServiceContainer()

    response = (
        container.rag_service
        .answer(
            query=query
        )
    )

    return response


@router.get("/health")
def rag_health():

    """
    Check RAG/vector database health.
    """

    container = ServiceContainer()

    return (
        container.vector_store
        .health_check()
    )
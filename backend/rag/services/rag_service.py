from __future__ import annotations

from typing import Any

from rag.core.exceptions import RetrievalException
from rag.core.logger import logger

from rag.models.rag import (
    RAGQuery,
    RAGResponse,
    SourceReference,
)

from rag.services.context_service import (
    ContextService,
)

from rag.services.prompt_service import (
    PromptService,
)

from rag.services.retrieval_service import (
    RetrievalService,
)

from rag.interfaces.llm import LLMService


class RAGService:
    """
    Orchestrates the complete Retrieval-Augmented
    Generation pipeline.

    Flow:

        Question
            ↓
        Retrieval
            ↓
        Context
            ↓
        Prompt
            ↓
        LLM
            ↓
        Grounded Response
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
        context_service: ContextService,
        prompt_service: PromptService,
        llm_service: LLMService,
    ) -> None:

        self._retrieval_service = (
            retrieval_service
        )

        self._context_service = (
            context_service
        )

        self._prompt_service = (
            prompt_service
        )

        self._llm_service = llm_service

        logger.info(
            "RAGService initialized."
        )

    # ========================================================
    # ANSWER
    # ========================================================

    def answer(
        self,
        query: RAGQuery,
        teaching_strategy: str | None = None,
    ) -> RAGResponse:
        """
        Generate a grounded answer for a student.

        The teaching strategy is selected by the
        Adaptive Decision Engine and passed to the
        PromptService.
        """

        try:

            # ------------------------------------------------
            # STEP 1 — BUILD METADATA FILTER
            # ------------------------------------------------

            metadata_filter = (
                self._build_metadata_filter(query)
            )

            logger.info(
                "RAG metadata filter: %s",
                metadata_filter,
            )

            # ------------------------------------------------
            # STEP 2 — RETRIEVE CONTEXT
            # ------------------------------------------------

            retrieval_result = (
                self._retrieval_service.retrieve(
                    query=query.question,
                    top_k=query.top_k,
                    metadata_filter=metadata_filter,
                )
            )

            chunks = retrieval_result.chunks

            logger.info(
                "Retrieved %d chunks.",
                len(chunks),
            )

            # ------------------------------------------------
            # STEP 3 — NO RELEVANT CONTEXT
            # ------------------------------------------------

            if not chunks:

                logger.warning(
                    "No relevant context found."
                )

                return RAGResponse(
                    answer=(
                        "I couldn't find enough "
                        "information about this topic "
                        "in the uploaded lecture."
                    ),
                    sources=[],
                    retrieved_chunks=0,
                    grounded=False,
                )

            # ------------------------------------------------
            # STEP 4 — BUILD CONTEXT
            # ------------------------------------------------

            context = (
                self._context_service.build_context(
                    chunks
                )
            )

            if not context.strip():

                logger.warning(
                    "Retrieved context is empty."
                )

                return RAGResponse(
                    answer=(
                        "I couldn't extract enough "
                        "usable information from the "
                        "uploaded lecture."
                    ),
                    sources=[],
                    retrieved_chunks=0,
                    grounded=False,
                )

            # ------------------------------------------------
            # STEP 5 — BUILD ADAPTIVE PROMPT
            # ------------------------------------------------

            logger.info(
                "Teaching strategy selected: %s",
                teaching_strategy,
            )

            prompt = (
                self._prompt_service.build_prompt(
                    question=query.question,
                    context=context,
                    teaching_strategy=(
                        teaching_strategy
                    ),
                )
            )

            # ------------------------------------------------
            # STEP 6 — CALL LLM
            # ------------------------------------------------

            answer = self._llm_service.generate(
                prompt
            )

            # ------------------------------------------------
            # STEP 7 — BUILD SOURCE REFERENCES
            # ------------------------------------------------

            sources = self._build_sources(
                chunks
            )

            # ------------------------------------------------
            # STEP 8 — RETURN RESPONSE
            # ------------------------------------------------

            return RAGResponse(
                answer=answer,
                sources=sources,
                retrieved_chunks=len(chunks),
                grounded=True,
            )

        except Exception as exc:

            logger.exception(
                "RAG pipeline failed."
            )

            raise RetrievalException(
                "Unable to generate RAG response."
            ) from exc

    # ========================================================
    # METADATA FILTER
    # ========================================================

    @staticmethod
    def _build_metadata_filter(
        query: RAGQuery,
    ) -> dict[str, Any] | None:
        """
        Build metadata filter for retrieval.

        lecture_id is used as a HARD FILTER.

        topic is not used as an exact Chroma metadata
        filter because indexed topic names may differ
        from the student's query.
        """

        if not query.lecture_id:
            return None

        return {
            "lecture_id": str(
                query.lecture_id
            )
        }

    # ========================================================
    # SOURCES
    # ========================================================

    @staticmethod
    def _build_sources(
        chunks,
    ) -> list[SourceReference]:
        """
        Convert retrieved chunks into source references.
        """

        sources = []

        for chunk in chunks:

            metadata = chunk.metadata

            sources.append(
                SourceReference(
                    chunk_id=chunk.id,

                    lecture_id=str(
                        metadata.get(
                            "lecture_id",
                            "",
                        )
                    ),

                    lecture_title=str(
                        metadata.get(
                            "lecture_title",
                            "Unknown",
                        )
                    ),

                    source_file=str(
                        metadata.get(
                            "source_file",
                            "Unknown",
                        )
                    ),

                    chunk_number=metadata.get(
                        "chunk_number"
                    ),
                )
            )

        return sources
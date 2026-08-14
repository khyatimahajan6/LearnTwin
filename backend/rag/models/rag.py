from pydantic import BaseModel, Field


class RAGQuery(BaseModel):

    question: str = Field(
        min_length=1,
        max_length=2000,
    )

    lecture_id: str

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )

    teaching_strategy: str | None = None


class SourceReference(BaseModel):

    chunk_id: str

    lecture_id: str

    lecture_title: str

    source_file: str

    chunk_number: int


class RAGResponse(BaseModel):

    answer: str

    sources: list[SourceReference] = []

    retrieved_chunks: int = 0

    grounded: bool = False
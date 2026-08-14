from __future__ import annotations

from pydantic import BaseModel, Field


class QuizQuestion(BaseModel):
    """
    A single multiple-choice question.
    """

    question_id: int

    question: str

    options: list[str] = Field(
        ...,
        min_length=4,
        max_length=4,
    )

    explanation: str

    difficulty: str = "medium"


class QuizGenerateRequest(BaseModel):
    """
    Request sent by the frontend to generate a quiz.
    """

    lecture_id: str

    topic: str | None = None

    number_of_questions: int = Field(
        default=10,
        ge=5,
        le=20,
    )


class QuizResponse(BaseModel):
    """
    Quiz returned to the frontend.

    Notice:
    correct answers are NOT included.
    """

    quiz_id: str

    lecture_id: str

    topic: str | None

    questions: list[QuizQuestion]


class QuizAnswer(BaseModel):
    """
    One answer submitted by the student.
    """

    question_id: int

    selected_answer: str


class QuizSubmitRequest(BaseModel):
    """
    Complete quiz submission.
    """

    quiz_id: str

    answers: list[QuizAnswer]



class QuizAnswerResult(BaseModel):
    """
    Feedback for one submitted question.
    """

    question_id: int

    selected_answer: str

    correct_answer: str

    is_correct: bool

    explanation: str


class QuizSubmitResponse(BaseModel):
    """
    Complete result returned after quiz submission.
    """

    quiz_id: str

    score: float

    total_marks: float

    percentage: float

    passed: bool

    test_id: str

    results: list[QuizAnswerResult]
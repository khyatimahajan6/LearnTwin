from __future__ import annotations

import json
import uuid
from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.lecture import Lecture
from models.student import Student
from models.test_result import TestResult

from rag.services.retrieval_service import RetrievalService
from rag.services.context_service import ContextService
from rag.services.llm_service import GeminiService

from schemas.quiz_schema import (
    QuizAnswer,
    QuizAnswerResult,
    QuizQuestion,
)


class QuizService:
    """
    Handles quiz generation and quiz evaluation.

    Responsibilities:
        1. Verify lecture ownership
        2. Retrieve lecture context
        3. Generate quiz using Gemini
        4. Store correct answers temporarily
        5. Evaluate student answers
        6. Save TestResult
    """

    # --------------------------------------------------------
    # Temporary in-memory quiz storage
    # --------------------------------------------------------

    _quiz_store: dict[str, dict[str, Any]] = {}

    def __init__(
        self,
        retrieval_service: RetrievalService,
        context_service: ContextService,
        llm_service: GeminiService,
    ) -> None:

        self._retrieval_service = retrieval_service
        self._context_service = context_service
        self._llm_service = llm_service

    # ========================================================
    # GENERATE QUIZ
    # ========================================================

    def generate_quiz(
        self,
        db: Session,
        student: Student,
        lecture_id: str,
        topic: str | None,
        number_of_questions: int,
    ) -> dict[str, Any]:
        """
        Generate a quiz from a student's lecture.
        """

        # ----------------------------------------------------
        # 1. Find lecture
        # ----------------------------------------------------

        lecture = (
            db.query(Lecture)
            .filter(
                Lecture.lecture_id == lecture_id
            )
            .first()
        )

        if lecture is None:
            raise HTTPException(
                status_code=404,
                detail="Lecture not found.",
            )

        # ----------------------------------------------------
        # 2. Verify lecture ownership
        # ----------------------------------------------------

        if lecture.student_id != student.student_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have access to this lecture.",
            )

        # ----------------------------------------------------
        # 3. Build retrieval query
        # ----------------------------------------------------

        if topic:
            retrieval_query = (
                f"Generate quiz questions about "
                f"{topic} from this lecture."
            )
        else:
            retrieval_query = (
                "Generate quiz questions covering "
                "the important concepts in this lecture."
            )

        # ----------------------------------------------------
        # 4. Retrieve lecture context
        # ----------------------------------------------------

        retrieval_result = (
            self._retrieval_service.retrieve(
                query=retrieval_query,
                top_k=8,
                metadata_filter={
                    "lecture_id": lecture_id
                },
            )
        )

        chunks = retrieval_result.chunks

        if not chunks:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No relevant lecture content was found "
                    "for quiz generation."
                ),
            )

        # ----------------------------------------------------
        # 5. Build context
        # ----------------------------------------------------

        context = (
            self._context_service.build_context(
                chunks
            )
        )

        if not context.strip():
            raise HTTPException(
                status_code=404,
                detail="Lecture context is empty.",
            )

        # ----------------------------------------------------
        # 6. Build quiz prompt
        # ----------------------------------------------------

        prompt = self._build_quiz_prompt(
            context=context,
            topic=topic,
            number_of_questions=number_of_questions,
        )

        # ----------------------------------------------------
        # 7. Generate using Gemini
        # ----------------------------------------------------

        raw_response = (
            self._llm_service.generate(prompt)
        )

        # ----------------------------------------------------
        # 8. Parse Gemini response
        # ----------------------------------------------------

        questions = self._parse_questions(
            raw_response
        )

        if not questions:
            raise HTTPException(
                status_code=500,
                detail="Gemini did not return valid quiz questions.",
            )

        # ----------------------------------------------------
        # 9. Create quiz ID
        # ----------------------------------------------------

        quiz_id = str(uuid.uuid4())

        # ----------------------------------------------------
        # 10. Store correct answers server-side
        # ----------------------------------------------------

        self._quiz_store[quiz_id] = {
            "student_id": student.student_id,
            "lecture_id": lecture_id,
            "topic": topic or lecture.topic,
            "questions": questions,
        }

        # ----------------------------------------------------
        # 11. Remove correct answers before frontend response
        # ----------------------------------------------------

        public_questions = []

        for question in questions:

            public_questions.append(
                QuizQuestion(
                    question_id=question["question_id"],
                    question=question["question"],
                    options=question["options"],
                    explanation="",
                    difficulty=question.get(
                        "difficulty",
                        "medium",
                    ),
                )
            )

        return {
            "quiz_id": quiz_id,
            "lecture_id": lecture_id,
            "topic": topic or lecture.topic,
            "questions": public_questions,
        }

    # ========================================================
    # QUIZ PROMPT
    # ========================================================

    @staticmethod
    def _build_quiz_prompt(
        context: str,
        topic: str | None,
        number_of_questions: int,
    ) -> str:
        """
        Build a grounded quiz-generation prompt.
        """

        topic_instruction = (
            f"Focus specifically on the topic: {topic}."
            if topic
            else
            "Cover the most important concepts from the lecture."
        )

        return f"""
You are an educational quiz generator.

Generate exactly {number_of_questions}
multiple-choice questions using ONLY the
provided lecture context.

{topic_instruction}

IMPORTANT RULES:

1. Do not use information outside the lecture context.
2. Each question must have exactly 4 options.
3. Only one option must be correct.
4. Questions should test understanding, not only memorization.
5. Mix easy, medium, and hard questions when possible.
6. Provide a short explanation for every correct answer.
7. Do not mention that you are an AI.
8. Do not add markdown.
9. Return ONLY valid JSON.

Return exactly this structure:

{{
  "questions": [
    {{
      "question_id": 1,
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correct_answer": "Option B",
      "explanation": "Why Option B is correct.",
      "difficulty": "medium"
    }}
  ]
}}

LECTURE CONTEXT:

{context}
"""

    # ========================================================
    # PARSE QUESTIONS
    # ========================================================

    @staticmethod
    def _parse_questions(
        raw_response: str,
    ) -> list[dict[str, Any]]:
        """
        Parse Gemini's JSON response.
        """

        try:

            cleaned = raw_response.strip()

            # Remove accidental markdown fences.
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]

            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]

            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            cleaned = cleaned.strip()

            data = json.loads(cleaned)

            questions = data.get("questions")

            if not isinstance(
                questions,
                list,
            ):
                raise ValueError(
                    "questions must be a list."
                )

            validated_questions = []

            for index, question in enumerate(
                questions,
                start=1,
            ):

                if not isinstance(
                    question,
                    dict,
                ):
                    continue

                question_text = question.get(
                    "question"
                )

                options = question.get(
                    "options"
                )

                correct_answer = question.get(
                    "correct_answer"
                )

                explanation = question.get(
                    "explanation"
                )

                difficulty = question.get(
                    "difficulty",
                    "medium",
                )

                if not question_text:
                    continue

                if not isinstance(
                    options,
                    list,
                ):
                    continue

                if len(options) != 4:
                    continue

                if correct_answer not in options:
                    continue

                if not explanation:
                    continue

                validated_questions.append(
                    {
                        "question_id": index,
                        "question": str(
                            question_text
                        ),
                        "options": [
                            str(option)
                            for option in options
                        ],
                        "correct_answer": str(
                            correct_answer
                        ),
                        "explanation": str(
                            explanation
                        ),
                        "difficulty": str(
                            difficulty
                        ),
                    }
                )

            return validated_questions

        except Exception:
            return []

    # ========================================================
    # SUBMIT QUIZ
    # ========================================================

    def submit_quiz(
        self,
        db: Session,
        student: Student,
        quiz_id: str,
        answers: list[QuizAnswer],
    ) -> dict[str, Any]:
        """
        Evaluate a quiz and save the result.
        """

        # ----------------------------------------------------
        # 1. Find quiz
        # ----------------------------------------------------

        quiz = self._quiz_store.get(
            quiz_id
        )

        if quiz is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Quiz not found or has expired."
                ),
            )

        # ----------------------------------------------------
        # 2. Verify student
        # ----------------------------------------------------

        if quiz["student_id"] != student.student_id:
            raise HTTPException(
                status_code=403,
                detail="You cannot submit this quiz.",
            )

        questions = quiz["questions"]

        # ----------------------------------------------------
        # 3. Create answer lookup
        # ----------------------------------------------------

        submitted_answers = {
            answer.question_id: answer.selected_answer
            for answer in answers
        }

        # ----------------------------------------------------
        # 4. Evaluate
        # ----------------------------------------------------

        score = 0

        results = []

        for question in questions:

            question_id = question["question_id"]

            selected_answer = submitted_answers.get(
                question_id,
                "",
            )

            correct_answer = question[
                "correct_answer"
            ]

            is_correct = (
                selected_answer.strip()
                == correct_answer.strip()
            )

            if is_correct:
                score += 1

            results.append(
                {
                    "question_id": question_id,
                    "selected_answer": selected_answer,
                    "correct_answer": correct_answer,
                    "is_correct": is_correct,
                    "explanation": question[
                        "explanation"
                    ],
                }
            )

        # ----------------------------------------------------
        # 5. Calculate score
        # ----------------------------------------------------

        total_marks = len(questions)

        percentage = (
            score / total_marks
        ) * 100

        passed = percentage >= 40

        # ----------------------------------------------------
        # 6. Save TestResult
        # ----------------------------------------------------

        test_result = TestResult(
            student_id=student.id,
            topic=quiz.get("topic"),
            test_name="Lecture Quiz",
            score=float(score),
            total_marks=float(total_marks),
            percentage=float(percentage),
            diagram_questions=0,
            diagram_correct=0,
            passed=passed,
        )

        db.add(test_result)

        db.commit()

        db.refresh(test_result)

        # ----------------------------------------------------
        # 7. Remove completed quiz from memory
        # ----------------------------------------------------

        del self._quiz_store[quiz_id]

        # ----------------------------------------------------
        # 8. Return result
        # ----------------------------------------------------

        return {
            "quiz_id": quiz_id,
            "score": float(score),
            "total_marks": float(total_marks),
            "percentage": float(
                round(percentage, 2)
            ),
            "passed": passed,
            "test_id": test_result.test_id,
            "results": results,
        }
from __future__ import annotations

from google import genai

from rag.core.config import settings
from rag.core.exceptions import RAGException
from rag.core.logger import logger


class GeminiService:
    """
    LLM implementation using Google's Gemini API.
    """

    def __init__(self) -> None:

        if not settings.GEMINI_API_KEY:

            raise RAGException(
                "GEMINI_API_KEY is not configured."
            )

        self._client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self._model = settings.GEMINI_MODEL

        logger.info(
            "GeminiService initialized."
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        if not prompt.strip():

            raise RAGException(
                "LLM prompt cannot be empty."
            )

        try:

            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt
            )

            answer = response.text

            if not answer:

                raise RAGException(
                    "LLM returned an empty response."
                )

            return answer.strip()

        except RAGException:

            raise

        except Exception as exc:

            logger.exception(
                "Gemini generation failed."
            )

            raise RAGException(
                "Unable to generate AI response."
            ) from exc
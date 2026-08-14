import json
import os
import time

from dotenv import load_dotenv
from google import genai

from schemas.nlp_schema import LectureMetadata
from utils.logger import get_logger


load_dotenv()

logger = get_logger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


PROMPT_TEMPLATE = """
You are an expert educational content analyzer.

Analyze the following lecture text and extract educational metadata.

Extract:

1. Topic
2. Subtopics
3. Keywords
4. Difficulty
5. Learning Objectives
6. Prerequisites
7. Summary

Rules:

- Return ONLY valid JSON.
- Do NOT explain anything.
- Do NOT use markdown.
- Do NOT wrap the response in ```json.
- Every field must exist.
- If information is missing, return an empty list or empty string.
- Difficulty must be one of:
  Easy
  Medium
  Hard

Return exactly:
{{
"topic": "...",
"subtopics": [],
"keywords": [],
"difficulty": "...",
"learning_objectives": [],
"prerequisites": [],
"summary": "..."
}}

Lecture:
{lecture_text}
"""


def extract_metadata(
    lecture_text: str
) -> LectureMetadata:

    if not lecture_text.strip():
        raise ValueError(
            "Lecture text cannot be empty."
        )

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Please add GEMINI_API_KEY to backend/.env."
        )

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    prompt = PROMPT_TEMPLATE.format(
        lecture_text=lecture_text
    )

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        try:

            logger.info(
                "Calling Gemini for NLP metadata "
                "(attempt %s/%s)",
                attempt,
                max_attempts
            )

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            if not response.text:
                raise ValueError(
                    "Gemini returned an empty response."
                )

            break

        except Exception as exc:

            error_text = str(exc)

            # Retry temporary Gemini 503 errors.
            if "503" in error_text and attempt < max_attempts:

                wait_time = 2 ** (attempt - 1)

                logger.warning(
                    "Gemini returned 503. "
                    "Retrying in %s seconds...",
                    wait_time
                )

                time.sleep(wait_time)

            else:

                logger.error(
                    "Gemini request failed: %s",
                    exc,
                    exc_info=True
                )

                raise

    try:

        metadata_dict = json.loads(
            response.text
        )

    except json.JSONDecodeError as exc:

        logger.error(
            "Gemini returned invalid JSON: %s",
            response.text
        )

        raise ValueError(
            "Gemini returned invalid JSON."
        ) from exc

    return LectureMetadata(
        **metadata_dict
    )
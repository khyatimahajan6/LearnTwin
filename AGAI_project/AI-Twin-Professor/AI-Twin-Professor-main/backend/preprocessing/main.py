"""
Main lecture preprocessing pipeline.

Flow:

Raw Lecture File
    ↓
File Validation
    ↓
File Type Detection
    ↓
Document Extraction
    ↓
Text Cleaning
    ↓
No-text Detection
    ↓
Standardized Output
"""

from pathlib import Path

from preprocessing.file_validator import (
    FileValidationError,
    validate_file,
    detect_file_type,
)

from preprocessing.pdf_processor import (
    process_pdf,
    PDFProcessingError,
)

from preprocessing.ppt_processor import (
    process_pptx,
    process_ppt,
    PPTProcessingError,
)

from preprocessing.docx_processor import (
    process_docx,
    DOCXProcessingError,
)

from preprocessing.text_cleaner import (
    clean_text,
    count_characters,
    remove_repeated_lines,	
)


def process_lecture_file(file_path: str | Path) -> dict:
    """
    Process a supported lecture document.

    Supported:
        PDF
        PPTX
        DOCX

    Legacy PPT:
        Detected but requires a separate conversion method.

    Returns:
        Standardized dictionary containing:
            file_name
            file_type
            status
            pages_or_slides
            clean_text
            character_count

        For warnings/errors, a message is also included.
    """

    path = Path(file_path)

    # ---------------------------------------------------------
    # STEP 1 — VALIDATION
    # ---------------------------------------------------------

    try:
        validated_path = validate_file(path)
    except FileValidationError as exc:
        return {
            "file_name": path.name,
            "file_type": path.suffix.lower().lstrip("."),
            "status": "error",
            "pages_or_slides": 0,
            "clean_text": "",
            "character_count": 0,
            "message": str(exc),
        }

    # ---------------------------------------------------------
    # STEP 2 — FILE TYPE DETECTION
    # ---------------------------------------------------------

    try:
        file_type = detect_file_type(validated_path)
    except FileValidationError as exc:
        return {
            "file_name": path.name,
            "file_type": path.suffix.lower().lstrip("."),
            "status": "error",
            "pages_or_slides": 0,
            "clean_text": "",
            "character_count": 0,
            "message": str(exc),
        }

    # ---------------------------------------------------------
    # STEP 3 — EXTRACTION
    # ---------------------------------------------------------

    try:

        if file_type == "pdf":
            result = process_pdf(validated_path)

        elif file_type == "pptx":
            result = process_pptx(validated_path)

        elif file_type == "ppt":
            return {
                "file_name": validated_path.name,
                "file_type": file_type,
                "status": "warning",
                "pages_or_slides": 0,
                "clean_text": "",
                "character_count": 0,
                "message": (
                    "Legacy .ppt files require conversion to .pptx "
                    "before text extraction."
                ),
            }

        elif file_type == "docx":
            result = process_docx(validated_path)

        else:
            return {
                "file_name": validated_path.name,
                "file_type": file_type,
                "status": "error",
                "pages_or_slides": 0,
                "clean_text": "",
                "character_count": 0,
                "message": "Unsupported document type.",
            }

    except (
        PDFProcessingError,
        PPTProcessingError,
        DOCXProcessingError,
    ) as exc:

        return {
            "file_name": validated_path.name,
            "file_type": file_type,
            "status": "error",
            "pages_or_slides": 0,
            "clean_text": "",
            "character_count": 0,
            "message": str(exc),
        }

    # ---------------------------------------------------------
    # STEP 4 — TEXT CLEANING
    # ---------------------------------------------------------

    raw_text = result.get("text", "")

    clean_lecture_text = clean_text(raw_text)
    # Remove obvious repeated headers/footers while preserving
    # meaningful lecture content and structural markers.
    clean_lecture_text = remove_repeated_lines(clean_lecture_text)
 
    # Clean once more after duplicate removal.
    clean_lecture_text = clean_text(clean_lecture_text)

    # ---------------------------------------------------------
    # STEP 5 — NO EXTRACTABLE TEXT
    # ---------------------------------------------------------

    # Structural markers such as [Page 1] and [Slide 1]
    # are not actual lecture content.
    import re

    meaningful_text = re.sub(
    	r"\[(?:Page|Slide)\s+\d+\]",
    	"",
    	clean_lecture_text,
    	flags=re.IGNORECASE,
    )

    meaningful_text = re.sub(
    	r"\[(?:Heading|Bullet|Paragraph)\]",
    	"",
    	meaningful_text,
    	flags=re.IGNORECASE,
    )

    meaningful_text = meaningful_text.strip()
    if not meaningful_text:

        return {
            "file_name": validated_path.name,
            "file_type": file_type,
            "status": "warning",
            "pages_or_slides": result.get(
                "pages_or_slides",
                0,
            ),
            "clean_text": "",
            "character_count": 0,
            "message": (
                "No extractable text found. "
                "This file may contain scanned images."
            ),
        }
    # ---------------------------------------------------------
    # STEP 6 — STANDARD OUTPUT
    # ---------------------------------------------------------

    return {
        "file_name": validated_path.name,
        "file_type": file_type,
        "status": "success",
        "pages_or_slides": result.get(
            "pages_or_slides",
            0,
        ),
        "raw_text": result.get("text", ""),
        "clean_text": clean_lecture_text,
        "character_count": count_characters(
            clean_lecture_text
        ),
    }
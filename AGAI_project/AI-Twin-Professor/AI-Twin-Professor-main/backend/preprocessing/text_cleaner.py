"""
preprocessing/text_cleaner.py

Cleans extracted lecture text while preserving:
    - headings
    - bullets
    - punctuation
    - technical terms
    - programming syntax
    - mathematical symbols
    - page/slide structure
"""

import re


def clean_line(line: str) -> str:
    """
    Clean one line without destroying meaningful content.
    """

    # Normalize non-breaking spaces.
    line = line.replace("\u00a0", " ")

    # Remove zero-width characters that sometimes appear
    # during document extraction.
    line = line.replace("\u200b", "")
    line = line.replace("\ufeff", "")

    # Remove trailing/leading whitespace.
    line = line.strip()

    # Collapse repeated normal spaces.
    # This intentionally does NOT alter punctuation or symbols.
    line = re.sub(r"[ \t]+", " ", line)

    return line


def clean_text(text: str) -> str:
    """
    Clean extracted lecture text while preserving its structure.

    Cleaning performed:
        - normalizes line endings
        - removes unnecessary whitespace
        - removes excessive blank lines
        - preserves headings
        - preserves bullets
        - preserves punctuation
        - preserves page/slide markers
        - preserves technical terminology

    No:
        - stopword removal
        - stemming
        - lemmatization
        - aggressive NLP processing
    """

    if not text:
        return ""

    # Normalize Windows / old Mac line endings.
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    lines = text.split("\n")

    cleaned_lines = []

    for line in lines:
        cleaned = clean_line(line)

        if cleaned:
            cleaned_lines.append(cleaned)
        else:
            # Keep blank lines temporarily.
            cleaned_lines.append("")

    # Remove excessive consecutive blank lines.
    final_lines = []
    previous_blank = False

    for line in cleaned_lines:

        is_blank = line == ""

        if is_blank:
            if previous_blank:
                continue

            previous_blank = True
            final_lines.append("")
        else:
            previous_blank = False
            final_lines.append(line)

    # Remove blank lines at the beginning/end.
    while final_lines and final_lines[0] == "":
        final_lines.pop(0)

    while final_lines and final_lines[-1] == "":
        final_lines.pop()

    return "\n".join(final_lines)

def remove_repeated_lines(text: str, min_repetitions: int = 3) -> str:
    """
    Remove obvious repeated headers/footers while preserving
    meaningful lecture content.

    A line is removed only when it appears repeatedly across
    multiple sections.
    """

    lines = text.splitlines()

    # Count non-empty lines
    counts = {}

    for line in lines:
        cleaned = line.strip()

        if cleaned:
            counts[cleaned] = counts.get(cleaned, 0) + 1

    repeated = {
        line
        for line, count in counts.items()
        if count >= min_repetitions
    }

    # Avoid deleting structural markers
    repeated = {
        line for line in repeated
        if not re.match(r"^\[(Page|Slide)\s+\d+\]$", line, re.IGNORECASE)
    }

    cleaned_lines = []

    for line in lines:
        if line.strip() in repeated:
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def count_characters(text: str) -> int:
    """Return the number of characters in cleaned text."""
    return len(text)

def remove_repeated_lines(text: str, minimum_repetitions: int = 3) -> str:
    """
    Remove obvious repeated headers/footers.

    A line is considered removable only when:
        - it is repeated multiple times
        - it is relatively short
        - it is not a structural marker
        - it is not a bullet

    This avoids deleting meaningful repeated lecture concepts.
    """

    if not text:
        return ""

    lines = text.split("\n")

    from collections import Counter

    normalized = []

    for line in lines:
        value = line.strip()

        if not value:
            continue

        if value.startswith("[Page ") or value.startswith("[Slide "):
            continue

        if value.startswith("[Heading]") or value.startswith("[Bullet]"):
            continue

        normalized.append(value)

    counts = Counter(normalized)

    repeated = {
        line
        for line, count in counts.items()
        if count >= minimum_repetitions
        and len(line) <= 150
    }

    cleaned = []

    for line in lines:
        stripped = line.strip()

        if stripped in repeated:
            continue

        cleaned.append(line)

    return "\n".join(cleaned)
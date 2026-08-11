import re

def clean_text(text: str) -> str:
    """
    Cleans raw extracted text according to the following rules:
    1. Removes page/slide markers like '[Page X]', '--- Page X ---', etc.
    2. Removes standalone page numbers on a single line.
    3. Collapses excessive consecutive blank lines into single blank lines.
    4. Replaces multiple spaces/tabs with a single space.
    5. Joins unnecessary line breaks inside sentences/paragraphs.
    6. Preserves headings, paragraph breaks, numbered lists, and bullet points.
    7. Preserves punctuation, numbers, formulas, code, URLs, and technical content.
    8. Converts unusual bullet characters (like ●, ○, ■, •, *) to '-'.
    """
    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove page/slide markers like --- Page 1 --- or [Page 1] or --- Slide 1 ---
    text = re.sub(r"(?i)---?\s*(Page|Slide)\s*\d+\s*---?", "", text)
    text = re.sub(r"(?i)\[\s*(Page|Slide)\s*\d+\s*\]", "", text)

    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            cleaned_lines.append("")
            continue

        # Remove standalone page numbers
        if re.match(r"^\d+$", stripped_line):
            cleaned_lines.append("")
            continue

        # Replace multiple spaces/tabs with a single space
        line_val = re.sub(r"[ \t]+", " ", line).strip()

        # Convert unusual bullet characters to "-"
        line_val = re.sub(r"^[●○■•*]\s*", "- ", line_val)

        cleaned_lines.append(line_val)

    reconstructed_lines = []
    current_paragraph = []

    for line in cleaned_lines:
        if line == "":
            if current_paragraph:
                reconstructed_lines.append(" ".join(current_paragraph))
                current_paragraph = []
            reconstructed_lines.append("")
            continue

        # A line starts a new block if it is a list item or a new paragraph start
        is_new_block = (
            line.startswith("- ") or
            bool(re.match(r"^\d+[\.\)]\s+", line)) or
            (current_paragraph == [])
        )

        if is_new_block:
            if current_paragraph:
                reconstructed_lines.append(" ".join(current_paragraph))
                current_paragraph = []
            current_paragraph.append(line)
        else:
            current_paragraph.append(line)

    if current_paragraph:
        reconstructed_lines.append(" ".join(current_paragraph))

    # Collapse consecutive blank lines
    final_lines = []
    for line in reconstructed_lines:
        if line == "":
            if final_lines and final_lines[-1] == "":
                continue
            final_lines.append("")
        else:
            final_lines.append(line)

    # Trim leading/trailing blank lines
    while final_lines and final_lines[0] == "":
        final_lines.pop(0)
    while final_lines and final_lines[-1] == "":
        final_lines.pop()

    return "\n".join(final_lines)

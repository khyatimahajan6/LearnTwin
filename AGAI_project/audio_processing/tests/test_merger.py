from audio_processing.schemas import MemberDocument, TranscriptSegment
from audio_processing.transcript_merger import merge_document_with_transcript


def test_merge_document_with_transcript():
    document = MemberDocument(
        lecture_id="L001",
        source="slides",
        text="Extracted lecture text."
    )
    segments = [TranscriptSegment(start=0.0, end=1.0, text="Hello world."), TranscriptSegment(start=1.0, end=2.0, text="This is a lecture.")]
    result = merge_document_with_transcript(
        lecture_id="L001",
        source="slides",
        cleaned_segments=segments,
        document_data=document,
    )

    assert result.lecture_id == "L001"
    assert result.source == "slides"
    assert "Extracted lecture text" in result.combined_text
    assert "Hello world" in result.transcript
    assert len(result.timestamps) == 2

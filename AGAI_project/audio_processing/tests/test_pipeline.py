import pytest

from audio_processing.pipeline import PipelineError, generate_output_filename, process_lecture
from audio_processing.transcript_cleaner import TranscriptCleaningError


def test_process_lecture_invalid_source_type():
    with pytest.raises(PipelineError):
        process_lecture(source_type="invalid", input_data="dummy", lecture_id="L001")


def test_process_lecture_missing_document_id_mismatch():
    with pytest.raises(PipelineError):
        process_lecture(
            source_type="audio",
            input_data="dummy",
            lecture_id="L001",
            document_data={"lecture_id": "L002", "source": "slides", "text": "text"},
        )


def test_generate_output_filename_uses_lecture_id_and_title(tmp_path):
    output_path = generate_output_filename("L001", "Binary Search", output_dir=tmp_path)
    assert output_path == tmp_path / "L001_binary_search.json"


def test_generate_output_filename_avoids_overwrite(tmp_path):
    first_path = generate_output_filename("L001", "Binary Search", output_dir=tmp_path)
    first_path.write_text("{}", encoding="utf-8")

    second_path = generate_output_filename("L001", "Binary Search", output_dir=tmp_path)
    assert second_path == tmp_path / "L001_binary_search_1.json"


def test_process_lecture_handles_empty_transcript_segments(monkeypatch):
    monkeypatch.setattr("audio_processing.pipeline.transcribe_audio", lambda _: [])

    def raise_empty(_segments):
        raise TranscriptCleaningError("No transcript segments provided.")

    monkeypatch.setattr("audio_processing.pipeline.clean_transcript_segments", raise_empty)

    with pytest.raises(PipelineError, match="No transcript segments provided"):
        process_lecture("audio", "dummy.mp3", "L001")

import os
import types
import wave
from pathlib import Path
import json

import pytest
from fastapi.testclient import TestClient

from audio_processing.config import SUPPORTED_AUDIO_EXTENSIONS, SUPPORTED_VIDEO_EXTENSIONS
from utils.validators import FileValidationError, validate_youtube_url

TEST_DATA = Path(__file__).parent / "test_data"


def write_dummy_audio(path: Path):
    with path.open("wb") as f:
        with wave.open(f, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(b"\x00\x00" * 16000)


def write_dummy_video(path: Path):
    path.write_bytes(b"\x00\x00\x00\x18ftypmp42")


@pytest.fixture(scope="session", autouse=True)
def create_test_media_files():
    TEST_DATA.mkdir(exist_ok=True)
    audio_path = TEST_DATA / "sample.wav"
    video_path = TEST_DATA / "sample.mp4"
    if not audio_path.exists():
        write_dummy_audio(audio_path)
    if not video_path.exists():
        write_dummy_video(video_path)
    yield


def test_invalid_media_type(client: TestClient, auth_header):
    response = client.post(
        "/upload/media",
        headers=auth_header,
        files={"media_file": ("sample.txt", b"hello world", "text/plain")},
    )
    assert response.status_code == 400
    assert "Media type" in response.json()["detail"]


def test_invalid_youtube_url(client: TestClient, auth_header):
    response = client.post(
        "/upload/media",
        headers=auth_header,
        data={"youtube_url": "https://notyoutube.com/watch?v=abc"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid YouTube URL."


def test_validate_youtube_url_accepts_known_domains():
    for url in [
        "https://youtube.com/watch?v=abc",
        "https://www.youtube.com/watch?v=abc",
        "https://m.youtube.com/watch?v=abc",
        "https://youtu.be/abc",
    ]:
        validate_youtube_url(url)


def test_validate_youtube_url_rejects_invalid_domain():
    with pytest.raises(FileValidationError, match="Invalid YouTube URL."):
        validate_youtube_url("https://notyoutube.com/watch?v=abc")


def test_validate_youtube_url_rejects_empty_url():
    with pytest.raises(FileValidationError, match="YouTube URL must not be empty."):
        validate_youtube_url("")


@pytest.mark.skip("Runtime/integration test: requires actual Whisper and YouTube network access")
def test_valid_youtube_upload(client: TestClient, auth_header):
    response = client.post(
        "/upload/media",
        headers=auth_header,
        data={"youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
    )
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {
        "lecture_id",
        "source",
        "document_text",
        "transcript",
        "timestamps",
        "combined_text",
    }
    assert body["source"] == "youtube"
    assert body["document_text"] is None
    assert isinstance(body["timestamps"], list)
    assert isinstance(body["transcript"], str)
    assert isinstance(body["combined_text"], str)


def test_valid_audio_upload_structure(client: TestClient, auth_header, monkeypatch):
    audio_path = TEST_DATA / "sample.wav"
    fake_result = types.SimpleNamespace(
        lecture_id="fake-lecture-id",
        source="audio",
        document_text=None,
        transcript="dummy transcript",
        timestamps=[],
        combined_text="dummy transcript",
    )

    def fake_process_lecture(source_type, input_data, lecture_id, document_data=None):
        return fake_result

    monkeypatch.setattr("services.media_service.process_lecture", fake_process_lecture)

    response = client.post(
        "/upload/media",
        headers=auth_header,
        files={"media_file": (audio_path.name, audio_path.read_bytes(), "audio/wav")},
    )
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {
        "lecture_id",
        "source",
        "document_text",
        "transcript",
        "timestamps",
        "combined_text",
    }
    assert body["source"] == "audio"
    assert body["document_text"] is None
    assert isinstance(body["timestamps"], list)
    assert isinstance(body["transcript"], str)
    assert isinstance(body["combined_text"], str)


@pytest.mark.skip("Requires actual Whisper model runtime")
def test_valid_video_upload_structure(client: TestClient, auth_header):
    video_path = TEST_DATA / "sample.mp4"
    response = client.post(
        "/upload/media",
        headers=auth_header,
        files={"media_file": (video_path.name, video_path.read_bytes(), "video/mp4")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "video"
    assert body["document_text"] is None
    assert set(body.keys()) == {
        "lecture_id",
        "source",
        "document_text",
        "transcript",
        "timestamps",
        "combined_text",
    }


@pytest.mark.skip("Requires Member 1 document upload support and real file flow")
def test_existing_lecture_id_with_document_text(client: TestClient, auth_header):
    response = client.post(
        "/upload/media",
        headers=auth_header,
        data={"lecture_id": "existing-id"},
    )
    assert response.status_code in {200, 404}

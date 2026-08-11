import pytest

from audio_processing.youtube_processor import (
    YouTubeProcessingError,
    _looks_like_vtt,
    fetch_youtube_captions,
    process_youtube_source,
)


def test_looks_like_vtt_rejects_html_content():
    html = "<!DOCTYPE html><html><body><p>Not a VTT file.</p></body></html>"
    assert not _looks_like_vtt(html)


def test_fetch_youtube_captions_returns_none_for_html_response(monkeypatch):
    class DummyResponse:
        def read(self):
            return b"<!DOCTYPE html><html><head></head><body>Redirect or error</body></html>"

    class DummyYDL:
        def __init__(self, opts):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

        def extract_info(self, url, download=False):
            return {
                "subtitles": {"en": [{"url": "https://example.com/captions.vtt"}]},
                "automatic_captions": {},
            }

        def urlopen(self, url):
            return DummyResponse()

    monkeypatch.setattr("audio_processing.youtube_processor.yt_dlp.YoutubeDL", DummyYDL)

    assert fetch_youtube_captions("https://www.youtube.com/watch?v=abc123") is None


def test_process_youtube_source_falls_back_to_audio_when_captions_missing():
    captions, audio_file = process_youtube_source(
        "https://www.youtube.com/watch?v=abc123",
        caption_retriever=lambda _: None,
        audio_downloader=lambda _, output_dir=None: "downloaded_audio.mp3",
        output_dir=".",
    )

    assert captions is None
    assert audio_file == "downloaded_audio.mp3"

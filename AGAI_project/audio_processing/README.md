# Audio Processing Module

This module handles lecture audio/video ingestion, transcription, timestamped transcript cleaning, and merging with document text from Member 1.

## Architecture

- `config.py`: configuration values and environment loading.
- `schemas.py`: typed data models for transcript segments and final lecture outputs.
- `audio_extractor.py`: extract audio from local video files using FFmpeg.
- `youtube_processor.py`: pluggable YouTube processing and fallback.
- `whisper_processor.py`: speech-to-text with faster-whisper.
- `transcript_cleaner.py`: conservative lecture transcript cleanup.
- `transcript_merger.py`: merge cleaned transcript with Member 1 document text.
- `pipeline.py`: main public entrypoint for the module.

## Installation

1. Create a Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install FFmpeg and ensure it is on your PATH.

## Usage

### Process a local audio file

```python
from audio_processing.pipeline import process_lecture

result = process_lecture(
    source_type="audio",
    input_data="path/to/file.mp3",
    lecture_id="L001",
    document_data={
        "lecture_id": "L001",
        "source": "slides",
        "text": "Extracted lecture text..."
    }
)
```

### Process a local video file

```python
result = process_lecture(
    source_type="video",
    input_data="path/to/file.mp4",
    lecture_id="L001"
)
```

### Process a YouTube URL

```python
result = process_lecture(
    source_type="youtube",
    input_data="https://www.youtube.com/watch?v=...",
    lecture_id="L001"
)
```

## Expected output

The returned structure includes:

- `lecture_id`
- `source`
- `document_text`
- `transcript` (cleaned text)
- `timestamps` (list of `{start, end, text}` segments)
- `combined_text`

## Member 1 integration

Pass Member 1 output as `document_data` to the public function. The module preserves the document source and merges it with the cleaned transcript.

## Member 3 consumption

Member 3 should use `combined_text` for chunking, embeddings, and ChromaDB ingestion.

## Known limitations

- This module does not implement embedding storage, vector DB, RAG, or teaching agent logic.
- YouTube transcript recovery depends on available captions and may fall back to audio transcription.
- The cleaner is intentionally conservative and does not aggressively rewrite technical content.

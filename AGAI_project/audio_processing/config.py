import os
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv()

SUPPORTED_AUDIO_EXTENSIONS = {"mp3", "wav", "m4a"}
SUPPORTED_VIDEO_EXTENSIONS = {"mp4", "mkv"}
SUPPORTED_SOURCE_TYPES = {"audio", "video", "youtube"}

MODEL_NAME = os.getenv("AUDIO_PROCESSING_MODEL", "base")
MODEL_LANGUAGE = os.getenv("AUDIO_PROCESSING_LANGUAGE", "en")
MODEL_DEVICE = os.getenv("AUDIO_PROCESSING_DEVICE", "cpu")
MODEL_COMPUTE_TYPE = os.getenv("AUDIO_PROCESSING_COMPUTE_TYPE", "int8")

YOUTUBE_TRANSCRIPT_PROVIDERS = ["youtube_api", "yt_dlp"]

FILLER_WORDS = set(
    term.strip()
    for term in os.getenv(
        "AUDIO_PROCESSING_FILLER_WORDS",
        "um,uh,uhm,like,so,actually,basically,right,okay,ok,hmm,ah,oh,er,eh",
    ).split(",")
    if term.strip()
)

TECHNICAL_TERMS = [
    term.strip()
    for term in os.getenv(
        "AUDIO_PROCESSING_TECHNICAL_TERMS",
        "CNN,RNN,LSTM,Transformer,API,SQL,Python,recursion,backpropagation,gradient descent,ChromaDB,embeddings,attention",
    ).split(",")
    if term.strip()
]

MAX_TRANSCRIPT_SEGMENT_SECONDS = float(os.getenv("AUDIO_PROCESSING_MAX_SEGMENT_SECONDS", "30"))

_default_output_dir = os.getenv("AUDIO_PROCESSING_OUTPUT_DIR", "outputs")
if os.path.isabs(_default_output_dir):
    DEFAULT_OUTPUT_DIR = _default_output_dir
else:
    DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), _default_output_dir)

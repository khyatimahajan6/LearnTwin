"""
services/youtube_service.py

Download audio from YouTube videos.

Supports:
    - YouTube video URLs
    - YouTube Music URLs
    - YouTube Shorts URLs

The downloaded media is converted to MP3 using FFmpeg.

Returns:
    tuple[str, bytes]:
        (filename, audio_bytes)
"""

import os
import shutil
import tempfile

import yt_dlp

from utils.logger import get_logger


logger = get_logger(__name__)


# ================================================================
# NODE.JS CONFIGURATION
# ================================================================
#
# Automatically find Node.js from the system PATH.
#
# This is better than hardcoding:
#
# C:\Program Files\nodejs\node.exe
#
# because the project can run on another Windows computer
# or another operating system.
#

NODE_PATH = shutil.which("node")


if not NODE_PATH:
    raise RuntimeError(
        "Node.js was not found in PATH. "
        "Please install Node.js and restart your terminal."
    )


logger.info(
    "Node.js found at: %s",
    NODE_PATH,
)


# ================================================================
# MAIN FUNCTION
# ================================================================

def download_youtube_audio(url: str):
    """
    Download audio from a YouTube URL and convert it to MP3.

    Parameters
    ----------
    url : str
        YouTube video, YouTube Music, or YouTube Shorts URL.

    Returns
    -------
    tuple[str, bytes]
        Example:
            ("u8Xam9EsqXQ.mp3", b"...audio bytes...")

    Raises
    ------
    RuntimeError
        If the YouTube media cannot be downloaded or converted.
    """

    # ============================================================
    # VALIDATE URL
    # ============================================================

    if not url or not url.strip():
        raise RuntimeError(
            "YouTube URL cannot be empty."
        )

    url = url.strip()

    # ============================================================
    # CREATE TEMPORARY DIRECTORY
    # ============================================================

    temp_dir = tempfile.mkdtemp(
        prefix="youtube_audio_"
    )

    logger.info(
        "YouTube temporary directory: %s",
        temp_dir,
    )

    # ============================================================
    # OUTPUT TEMPLATE
    # ============================================================
    #
    # yt-dlp first downloads the original audio format.
    #
    # Example:
    #
    #     u8Xam9EsqXQ.webm
    #
    # or:
    #
    #     u8Xam9EsqXQ.m4a
    #
    # FFmpeg then converts it to:
    #
    #     u8Xam9EsqXQ.mp3
    #

    output_template = os.path.join(
        temp_dir,
        "%(id)s.%(ext)s",
    )

    # ============================================================
    # YT-DLP OPTIONS
    # ============================================================

    ydl_opts = {

        # --------------------------------------------------------
        # AUDIO FORMAT
        # --------------------------------------------------------
        #
        # Do NOT force format 140.
        #
        # Your successful test downloaded format 251.
        #
        # bestaudio/best lets yt-dlp select the best available
        # audio format.
        #

        "format": "bestaudio/best",

        # --------------------------------------------------------
        # OUTPUT
        # --------------------------------------------------------

        "outtmpl": output_template,

        # Never download playlists.
        "noplaylist": True,

        # --------------------------------------------------------
        # JAVASCRIPT RUNTIME
        # --------------------------------------------------------
        #
        # Automatically discovered Node.js executable.
        #
        # This avoids hardcoding:
        #
        # C:\Program Files\nodejs\node.exe
        #

        "js_runtimes": {
            "node": {
                "path": NODE_PATH
            }
        },

        # --------------------------------------------------------
        # NETWORK
        # --------------------------------------------------------

        "socket_timeout": 60,

        # Retry complete downloads.
        "retries": 3,

        # Retry individual fragments.
        "fragment_retries": 3,

        # Retry extraction.
        "extractor_retries": 3,

        # Skip unavailable fragments where possible.
        "skip_unavailable_fragments": True,

        # Force IPv4.
        #
        # This can avoid IPv6 routing problems on some networks.
        #

        "force_ipv4": True,

        # --------------------------------------------------------
        # HTTP HEADERS
        # --------------------------------------------------------

        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0.0.0 "
                "Safari/537.36"
            ),

            "Accept-Language": (
                "en-US,en;q=0.9"
            ),
        },

        # --------------------------------------------------------
        # DOWNLOAD SETTINGS
        # --------------------------------------------------------

        "continuedl": True,

        "overwrites": True,

        # --------------------------------------------------------
        # FFMPEG POST PROCESSING
        # --------------------------------------------------------
        #
        # Convert WebM/M4A/etc. to MP3.
        #

        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],

        # --------------------------------------------------------
        # LOGGING
        # --------------------------------------------------------

        "quiet": False,

        "no_warnings": False,
    }

    # ================================================================
    # DOWNLOAD
    # ================================================================

    try:

        logger.info(
            "Starting YouTube audio download: %s",
            url,
        )

        # --------------------------------------------------------
        # CREATE YT-DLP INSTANCE
        # --------------------------------------------------------

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            # ----------------------------------------------------
            # DOWNLOAD
            # ----------------------------------------------------

            info = ydl.extract_info(
                url,
                download=True,
            )

            # ----------------------------------------------------
            # VALIDATE INFO
            # ----------------------------------------------------

            if not info:

                raise RuntimeError(
                    "yt-dlp returned no video information."
                )

            video_id = info.get("id")

            if not video_id:

                raise RuntimeError(
                    "Could not determine YouTube video ID."
                )

            logger.info(
                "YouTube video ID: %s",
                video_id,
            )

        # ========================================================
        # FIND CONVERTED MP3
        # ========================================================

        audio_path = None

        # --------------------------------------------------------
        # First check expected filename.
        # --------------------------------------------------------

        expected_mp3 = os.path.join(
            temp_dir,
            f"{video_id}.mp3",
        )

        if os.path.isfile(expected_mp3):

            audio_path = expected_mp3

        # --------------------------------------------------------
        # If expected filename isn't found, scan directory.
        # --------------------------------------------------------

        if audio_path is None:

            for file_name in os.listdir(temp_dir):

                file_path = os.path.join(
                    temp_dir,
                    file_name,
                )

                if not os.path.isfile(file_path):
                    continue

                if file_name.lower().endswith(".mp3"):

                    audio_path = file_path

                    break

        # ========================================================
        # MP3 NOT FOUND
        # ========================================================

        if audio_path is None:

            try:

                files_found = os.listdir(
                    temp_dir
                )

            except Exception:

                files_found = []

            logger.error(
                "MP3 file was not found."
            )

            logger.error(
                "Files in temporary directory: %s",
                files_found,
            )

            raise RuntimeError(
                "YouTube audio was downloaded, "
                "but FFmpeg did not produce an MP3 file."
            )

        logger.info(
            "MP3 file found: %s",
            audio_path,
        )

        # ========================================================
        # READ MP3
        # ========================================================

        try:

            with open(
                audio_path,
                "rb",
            ) as audio_file:

                audio_bytes = audio_file.read()

        except OSError as exc:

            raise RuntimeError(
                f"Could not read downloaded MP3: {exc}"
            ) from exc

        # ========================================================
        # VALIDATE AUDIO
        # ========================================================

        if not audio_bytes:

            raise RuntimeError(
                "Downloaded audio file is empty."
            )

        logger.info(
            "Downloaded audio size: %d bytes",
            len(audio_bytes),
        )

        # ========================================================
        # CREATE FILENAME
        # ========================================================

        filename = f"{video_id}.mp3"

        logger.info(
            "YouTube audio downloaded successfully: %s",
            filename,
        )

        # ========================================================
        # RETURN
        # ========================================================

        return filename, audio_bytes

    # ================================================================
    # YT-DLP DOWNLOAD ERROR
    # ================================================================

    except yt_dlp.utils.DownloadError as exc:

        logger.exception(
            "yt-dlp download failed: %s",
            exc,
        )

        error_message = str(exc)

        error_lower = error_message.lower()

        # --------------------------------------------------------
        # TIMEOUT
        # --------------------------------------------------------

        if (
            "timed out" in error_lower
            or "winerror 10060" in error_lower
            or "connection timed out" in error_lower
        ):

            message = (
                "YouTube audio download timed out. "
                "The YouTube media server connection was "
                "not reachable. Please try again."
            )

        # --------------------------------------------------------
        # HTTP 403
        # --------------------------------------------------------

        elif "403" in error_lower:

            message = (
                "YouTube rejected the media request "
                "(HTTP 403). "
                "Please update yt-dlp and try again."
            )

        # --------------------------------------------------------
        # AUTHENTICATION
        # --------------------------------------------------------

        elif (
            "sign in" in error_lower
            or "authentication" in error_lower
        ):

            message = (
                "YouTube requires authentication for this video. "
                "The video may be private, age-restricted, "
                "or otherwise protected."
            )

        # --------------------------------------------------------
        # PRIVATE VIDEO
        # --------------------------------------------------------

        elif "private video" in error_lower:

            message = (
                "This YouTube video is private "
                "and cannot be downloaded."
            )

        # --------------------------------------------------------
        # VIDEO UNAVAILABLE
        # --------------------------------------------------------

        elif (
            "video unavailable" in error_lower
            or "is unavailable" in error_lower
        ):

            message = (
                "This YouTube video is unavailable "
                "and cannot be downloaded."
            )

        # --------------------------------------------------------
        # GENERIC YT-DLP ERROR
        # --------------------------------------------------------

        else:

            message = (
                f"YouTube download failed: "
                f"{error_message}"
            )

        raise RuntimeError(
            message
        ) from exc

    # ================================================================
    # OUR OWN RUNTIME ERROR
    # ================================================================

    except RuntimeError:

        # Preserve the useful RuntimeError message we created.
        raise

    # ================================================================
    # OTHER ERRORS
    # ================================================================

    except Exception as exc:

        logger.exception(
            "Unexpected YouTube processing error: %s",
            exc,
        )

        raise RuntimeError(
            f"Failed to download YouTube audio: {exc}"
        ) from exc

    # ================================================================
    # CLEANUP
    # ================================================================

    finally:

        try:

            if os.path.exists(temp_dir):

                shutil.rmtree(
                    temp_dir,
                    ignore_errors=True,
                )

                logger.info(
                    "Removed YouTube temporary directory: %s",
                    temp_dir,
                )

        except Exception as cleanup_error:

            logger.warning(
                "Could not completely remove temporary "
                "directory %s: %s",
                temp_dir,
                cleanup_error,
            )
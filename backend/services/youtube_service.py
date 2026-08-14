"""
services/youtube_service.py

Download audio from YouTube videos.

Supports:
    - YouTube video URLs
    - YouTube audio/music URLs
    - YouTube Shorts URLs

Pipeline:

    YouTube URL
        ↓
    yt-dlp
        ↓
    Audio stream
        ↓
    FFmpeg
        ↓
    MP3 bytes
        ↓
    Existing lecture pipeline
"""

import os
import shutil
import tempfile

import yt_dlp

from utils.logger import get_logger


logger = get_logger(__name__)


def download_youtube_audio(url: str):
    """
    Download audio from a YouTube URL.

    The URL may point to:
        - normal YouTube video
        - YouTube music/audio video
        - YouTube Short

    Returns:
        tuple[str, bytes]:
            (filename, audio_bytes)

    Raises:
        RuntimeError:
            If the YouTube media cannot be downloaded.
    """

    # ================================================================
    # STEP 1 — VALIDATE URL
    # ================================================================

    if not url or not url.strip():

        raise RuntimeError(
            "YouTube URL cannot be empty."
        )

    url = url.strip()

    # ================================================================
    # STEP 2 — TEMPORARY DIRECTORY
    # ================================================================

    temp_dir = tempfile.mkdtemp(
        prefix="youtube_audio_"
    )

    output_template = os.path.join(
        temp_dir,
        "%(id)s.%(ext)s",
    )

    logger.info(
        "Temporary YouTube directory created: %s",
        temp_dir,
    )

    # ================================================================
    # STEP 3 — YT-DLP OPTIONS
    # ================================================================

    ydl_opts = {

        # ------------------------------------------------------------
        # AUDIO FORMAT
        # ------------------------------------------------------------
        #
        # Prefer M4A.
        # If unavailable, use WebM audio.
        # Finally fall back to best available audio.
        #
        "format": (
            "bestaudio[ext=m4a]/"
            "bestaudio[ext=webm]/"
            "bestaudio/best"
        ),

        # ------------------------------------------------------------
        # OUTPUT
        # ------------------------------------------------------------

        "outtmpl": output_template,
        "ffmpeg_location": r"C:\Users\hp\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0-full_build\bin",
        # Never download playlists.
        "noplaylist": True,

        # ------------------------------------------------------------
        # NETWORK SETTINGS
        # ------------------------------------------------------------

        # Increase connection timeout.
        "socket_timeout": 120,

        # Retry complete downloads.
        "retries": 10,

        # Retry individual fragments.
        "fragment_retries": 10,

        # Retry extraction.
        "extractor_retries": 5,

        # ------------------------------------------------------------
        # DOWNLOAD IN SMALLER HTTP CHUNKS
        # ------------------------------------------------------------
        #
        # This can help when a large continuous connection to
        # Google's video server is timing out.
        #
        "http_chunk_size": 10 * 1024 * 1024,

        # ------------------------------------------------------------
        # DOWNLOAD ONE FRAGMENT AT A TIME
        # ------------------------------------------------------------
        #
        # Reduces simultaneous connections.
        #
        "concurrent_fragment_downloads": 1,

        # ------------------------------------------------------------
        # CONTINUE / FRAGMENT SETTINGS
        # ------------------------------------------------------------

        "continuedl": True,

        "skip_unavailable_fragments": True,

        "overwrites": True,

        # ------------------------------------------------------------
        # FORCE IPV4
        # ------------------------------------------------------------
        #
        # Your previous error was a connection timeout.
        # IPv4 avoids some IPv6 routing problems.
        #
        "force_ipv4": True,

        # ------------------------------------------------------------
        # GEO
        # ------------------------------------------------------------

        "geo_bypass": True,

        # ------------------------------------------------------------
        # HTTP HEADERS
        # ------------------------------------------------------------

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

        # ------------------------------------------------------------
        # LOGGING
        # ------------------------------------------------------------

        "quiet": False,

        "no_warnings": False,

        # ------------------------------------------------------------
        # FFMPEG POST PROCESSING
        # ------------------------------------------------------------
        #
        # Downloaded audio:
        #
        # M4A/WebM
        #       ↓
        #     FFmpeg
        #       ↓
        #      MP3
        #
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    # ================================================================
    # STEP 4 — DOWNLOAD
    # ================================================================

    try:

        logger.info(
            "Starting YouTube audio download: %s",
            url,
        )

        with yt_dlp.YoutubeDL(
            ydl_opts
        ) as ydl:

            info = ydl.extract_info(
                url,
                download=True,
            )

            if not info:

                raise RuntimeError(
                    "yt-dlp returned no video information."
                )

            video_id = info.get(
                "id"
            )

            if not video_id:

                raise RuntimeError(
                    "Could not determine YouTube video ID."
                )

            logger.info(
                "YouTube video identified: %s",
                video_id,
            )

        # ============================================================
        # STEP 5 — FIND MP3
        # ============================================================

        audio_path = os.path.join(
            temp_dir,
            f"{video_id}.mp3",
        )

        # ------------------------------------------------------------
        # Expected MP3 path
        # ------------------------------------------------------------

        if not os.path.exists(
            audio_path
        ):

            logger.warning(
                "Expected MP3 was not found: %s",
                audio_path,
            )

            # --------------------------------------------------------
            # Search temporary directory
            # --------------------------------------------------------

            possible_files = []

            for file_name in os.listdir(
                temp_dir
            ):

                file_path = os.path.join(
                    temp_dir,
                    file_name,
                )

                if (
                    os.path.isfile(file_path)
                    and file_name.lower().endswith(
                        ".mp3"
                    )
                ):

                    possible_files.append(
                        file_path
                    )

            # --------------------------------------------------------
            # Use discovered MP3
            # --------------------------------------------------------

            if possible_files:

                audio_path = possible_files[0]

                logger.info(
                    "Found converted MP3: %s",
                    audio_path,
                )

            else:

                # ----------------------------------------------------
                # Show what yt-dlp actually produced.
                # This makes debugging much easier.
                # ----------------------------------------------------

                generated_files = []

                for file_name in os.listdir(
                    temp_dir
                ):

                    generated_files.append(
                        file_name
                    )

                logger.error(
                    "No MP3 found. Files in temp directory: %s",
                    generated_files,
                )

                raise RuntimeError(
                    "YouTube audio was downloaded, "
                    "but FFmpeg did not produce an MP3 file."
                )

        # ============================================================
        # STEP 6 — READ MP3
        # ============================================================

        with open(
            audio_path,
            "rb",
        ) as audio_file:

            audio_bytes = audio_file.read()

        if not audio_bytes:

            raise RuntimeError(
                "Downloaded audio file is empty."
            )

        # ============================================================
        # STEP 7 — FINAL FILENAME
        # ============================================================

        filename = f"{video_id}.mp3"

        logger.info(
            "YouTube audio downloaded successfully."
        )

        logger.info(
            "Filename: %s",
            filename,
        )

        logger.info(
            "Audio size: %d bytes",
            len(audio_bytes),
        )

        # ============================================================
        # STEP 8 — RETURN TO LECTURE SERVICE
        # ============================================================

        return (
            filename,
            audio_bytes,
        )

    # ================================================================
    # STEP 9 — YT-DLP DOWNLOAD ERROR
    # ================================================================

    except yt_dlp.utils.DownloadError as exc:

        logger.exception(
            "yt-dlp download failed: %s",
            exc,
        )

        error_message = str(
            exc
        )

        lower_error = (
            error_message.lower()
        )

        # ------------------------------------------------------------
        # TIMEOUT
        # ------------------------------------------------------------

        if (
            "timed out" in lower_error
            or "winerror 10060" in lower_error
        ):

            message = (
                "YouTube audio download timed out. "
                "The YouTube media server could not be "
                "reached from this computer. "
                "Please check your network connection, "
                "VPN, firewall, or proxy."
            )

        # ------------------------------------------------------------
        # HTTP 403
        # ------------------------------------------------------------

        elif "403" in lower_error:

            message = (
                "YouTube rejected the media request "
                "(HTTP 403). Please try another video "
                "or update yt-dlp."
            )

        # ------------------------------------------------------------
        # SIGN IN
        # ------------------------------------------------------------

        elif "sign in" in lower_error:

            message = (
                "YouTube requires authentication for this "
                "video. The video may be private, "
                "age-restricted, or otherwise protected."
            )

        # ------------------------------------------------------------
        # PRIVATE VIDEO
        # ------------------------------------------------------------

        elif "private video" in lower_error:

            message = (
                "This YouTube video is private "
                "and cannot be downloaded."
            )

        # ------------------------------------------------------------
        # VIDEO UNAVAILABLE
        # ------------------------------------------------------------

        elif (
            "video unavailable" in lower_error
            or "unavailable" in lower_error
        ):

            message = (
                "This YouTube video is unavailable "
                "or cannot be accessed."
            )

        # ------------------------------------------------------------
        # GENERIC YT-DLP ERROR
        # ------------------------------------------------------------

        else:

            message = (
                f"YouTube download failed: "
                f"{error_message}"
            )

        raise RuntimeError(
            message
        ) from exc

    # ================================================================
    # STEP 10 — OTHER ERROR
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
    # STEP 11 — CLEANUP
    # ================================================================

    finally:

        try:

            if os.path.exists(
                temp_dir
            ):

                shutil.rmtree(
                    temp_dir,
                    ignore_errors=True,
                )

                logger.info(
                    "Temporary YouTube directory cleaned: %s",
                    temp_dir,
                )

        except Exception:

            pass
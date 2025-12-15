import yt_dlp
from pathlib import Path
import sys
import os
import threading


class DownloadCancelled(Exception):
    pass


def get_ffmpeg_path():
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "ffmpeg")
    return r"C:\ffmpeg-2025-12-14-git-3332b2db84-essentials_build\bin"


def download_mp3(
    url,
    output_dir,
    quality="320",
    single=False,
    progress_callback=None,
    cancel_event: threading.Event = None,
):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    def hook(d):
        if cancel_event and cancel_event.is_set():
            raise DownloadCancelled("Download cancelled by user")

        if progress_callback:
            progress_callback(d)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(
            output_dir / "%(track_number)02d - %(title)s.%(ext)s"
        ),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": quality,
            },
            {"key": "EmbedThumbnail"},
            {"key": "FFmpegMetadata"},
        ],
        "writethumbnail": True,
        "ignoreerrors": True,
        "continuedl": True,
        "noplaylist": single,
        "progress_hooks": [hook],
        "quiet": True,

        # Stability
        "retries": 10,
        "fragment_retries": 10,
        "socket_timeout": 30,
        "extractor_retries": 5,

        "ffmpeg_location": get_ffmpeg_path(),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

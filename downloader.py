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
    summary_callback=None,
    cancel_event: threading.Event = None,
):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    stats = {
        "total": None,
        "downloaded": 0,
        "skipped": 0,
    }

    def hook(d):
        if cancel_event and cancel_event.is_set():
            raise DownloadCancelled("Download cancelled by user")

        # Capture total track count once
        if d.get("status") == "downloading":
            if d.get("playlist_count") and stats["total"] is None:
                stats["total"] = d.get("playlist_count")

        if d.get("status") == "finished":
            stats["downloaded"] += 1

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

        # 🔥 FULL PLAYLIST SUPPORT
        "playliststart": 1,
        "playlistend": None,
        "noplaylist": single,

        "extractor_args": {
            "youtube": {
                "player_client": ["android_music"],
                "skip": ["dash", "hls"],
            }
        },

        # Stability for huge albums
        "retries": 20,
        "fragment_retries": 20,
        "extractor_retries": 10,
        "socket_timeout": 60,

        "writethumbnail": True,
        "ignoreerrors": True,
        "continuedl": True,
        "progress_hooks": [hook],
        "quiet": True,

        "ffmpeg_location": get_ffmpeg_path(),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    finally:
        if stats["total"] is not None:
            stats["skipped"] = max(0, stats["total"] - stats["downloaded"])

        if summary_callback:
            summary_callback(stats)

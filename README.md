YouTube Music MP3 Downloader
============================

A desktop application to download YouTube Music albums, playlists, or single songs
in high-quality MP3 format, with a modern GUI, live progress tracking, cancel support,
and a professional Windows installer.

------------------------------------------------------------------

FEATURES
--------

- Download entire albums or playlists
- Download single songs only (no extra tracks)
- MP3-only output (128 kbps / 320 kbps)
- Choose custom output folder
- Live download progress and current track display
- Cancel download anytime
- Downloaded files log inside the app
- Modern CustomTkinter-based GUI
- Standalone Windows installer (no Python required)
- FFmpeg bundled internally

------------------------------------------------------------------

TECH STACK
----------

Language: Python  
GUI: CustomTkinter  
Downloader: yt-dlp  
Audio Processing: FFmpeg  
Packaging: PyInstaller  
Installer: Inno Setup  

------------------------------------------------------------------

PROJECT STRUCTURE
-----------------

yt-music-mp3-downloader/

app.py              - GUI application  
downloader.py       - yt-dlp + FFmpeg logic  
ffmpeg/             - ffmpeg.exe & ffprobe.exe  
downloads/          - Output directory (created at runtime)  
requirements.txt  
README.txt  

------------------------------------------------------------------

INSTALLATION (WINDOWS)
----------------------

Option 1: Installer (Recommended)

1. Download YT_Music_MP3_Downloader_Setup.exe
2. Double-click the installer
3. Click "More info" → "Run anyway" (first time only)
4. Launch from Desktop or Start Menu

No Python installation required.

---------------------------------------------------------------

Option 2: Run from Source (Developers)

pip install -r requirements.txt
python app.py

FFmpeg must be available or bundled in the ffmpeg folder.

------------------------------------------------------------------

HOW TO USE
----------

1. Open the application
2. Paste a YouTube Music album, playlist, or song URL
3. Select MP3 quality (128 kbps or 320 kbps)
4. Choose download mode:
   - Album / Playlist
   - Single Song
5. Select output folder
6. Click "Download"
7. Track progress in real time
8. Cancel download anytime if needed

------------------------------------------------------------------

NOTES & LIMITATIONS
-------------------

- Windows-only application
- Requires an active internet connection
- YouTube changes may affect downloads (handled by yt-dlp updates)

------------------------------------------------------------------

DISCLAIMER
----------

This project is intended for educational and personal use only.
Downloading copyrighted content without permission may violate
YouTube’s Terms of Service or local laws.

Use responsibly.

------------------------------------------------------------------

LEARNING OUTCOMES
-----------------

- Python desktop GUI development
- Multithreading and background tasks
- Media downloading automation
- FFmpeg audio conversion
- Error handling and cancellation logic
- Packaging and installer creation

------------------------------------------------------------------

FUTURE ENHANCEMENTS
-------------------

- Auto-update yt-dlp
- Track counter (e.g., 3 / 12)
- Remember last used output folder
- macOS and Linux builds
- Mobile backend version

------------------------------------------------------------------

AUTHOR
------

Shubham Sharma  
B.Tech CSE Student  

Built as a real-world automation and desktop application project.

------------------------------------------------------------------

SUPPORT
-------

If you find this project useful:
- Star the repository
- Report issues
- Suggest improvements

------------------------------------------------------------------
"# yt-music-mp3-downloader" 

# YouTube Downloader (YouTube links only)

A simple desktop app (Python + Tkinter) built on yt-dlp.

## Requirements
- Python 3.9+
- ffmpeg installed and on your PATH
  - Windows: `winget install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`

## Run from source
```
pip install yt-dlp
python yt_downloader.py
```

## Build a standalone app
- Windows: double-click `build.bat`  ->  `dist\YouTubeDownloader.exe`
- macOS/Linux: `chmod +x build.sh && ./build.sh`  ->  `dist/YouTubeDownloader`

## Keep it working
YouTube changes often. If downloads fail, update yt-dlp:
```
pip install -U yt-dlp
```
and rebuild.

## Legal
Only download videos you own, that are Creative Commons licensed, or that
you have permission to download. Respect YouTube's Terms of Service.

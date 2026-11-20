#!/usr/bin/env bash
set -e
python3 -m pip install -r requirements.txt
python3 -m PyInstaller --onefile --windowed --name YouTubeDownloader --collect-all yt_dlp yt_downloader.py
echo
echo "Done. Your app is in the dist/ folder."
echo "Note: ffmpeg must be installed on the computer that runs it."

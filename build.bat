@echo off
python -m pip install -r requirements.txt
python -m PyInstaller --onefile --windowed --name YouTubeDownloader --collect-all yt_dlp yt_downloader.py
echo.
echo Done. Your app is in the "dist" folder: dist\YouTubeDownloader.exe
echo Note: ffmpeg must be installed on the computer that runs it.
pause

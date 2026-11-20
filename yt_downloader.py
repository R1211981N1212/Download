"""
YouTube Video Downloader (YouTube links only)

Setup:
    pip install yt-dlp
    Install ffmpeg (needed to merge video+audio and for MP3):
      - Windows: winget install ffmpeg
      - macOS:   brew install ffmpeg
      - Linux:   sudo apt install ffmpeg

Run:
    python yt_downloader.py

Only download videos you own, that are Creative Commons licensed,
or that you have permission to download. Respect YouTube's Terms of Service.
"""

import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from urllib.parse import urlparse

try:
    import yt_dlp
except ImportError:
    raise SystemExit("yt-dlp is not installed. Run: pip install yt-dlp")

YT_HOSTS = {
    "youtube.com", "www.youtube.com", "m.youtube.com",
    "music.youtube.com", "youtu.be", "www.youtu.be",
}

QUALITIES = {
    "Best available": "bv*+ba/b",
    "1080p": "bv*[height<=1080]+ba/b[height<=1080]",
    "720p": "bv*[height<=720]+ba/b[height<=720]",
    "480p": "bv*[height<=480]+ba/b[height<=480]",
    "360p": "bv*[height<=360]+ba/b[height<=360]",
    "Audio only (MP3)": "bestaudio/best",
}


def is_youtube_url(url: str) -> bool:
    try:
        return urlparse(url.strip()).netloc.lower() in YT_HOSTS
    except Exception:
        return False


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("560x300")
        self.resizable(False, False)

        self.url = tk.StringVar()
        self.quality = tk.StringVar(value="Best available")
        self.folder = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self.status = tk.StringVar(value="Paste a YouTube link to begin.")

        pad = {"padx": 14, "pady": 6}
        ttk.Label(self, text="YouTube URL").pack(anchor="w", **pad)
        ttk.Entry(self, textvariable=self.url).pack(fill="x", padx=14)

        row = ttk.Frame(self)
        row.pack(fill="x", **pad)
        ttk.Label(row, text="Quality").pack(side="left")
        ttk.Combobox(row, textvariable=self.quality, values=list(QUALITIES),
                     state="readonly", width=20).pack(side="left", padx=10)

        row2 = ttk.Frame(self)
        row2.pack(fill="x", **pad)
        ttk.Entry(row2, textvariable=self.folder).pack(side="left", fill="x", expand=True)
        ttk.Button(row2, text="Browse", command=self.pick_folder).pack(side="left", padx=6)

        self.btn = ttk.Button(self, text="Download", command=self.start)
        self.btn.pack(**pad)

        self.bar = ttk.Progressbar(self, maximum=100)
        self.bar.pack(fill="x", padx=14)
        ttk.Label(self, textvariable=self.status, wraplength=520).pack(anchor="w", **pad)

    def pick_folder(self):
        d = filedialog.askdirectory(initialdir=self.folder.get())
        if d:
            self.folder.set(d)

    def start(self):
        url = self.url.get().strip()
        if not is_youtube_url(url):
            messagebox.showerror("Invalid link", "Please enter a valid YouTube URL.")
            return
        self.btn.config(state="disabled")
        self.bar["value"] = 0
        threading.Thread(target=self.download, args=(url,), daemon=True).start()

    def hook(self, d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            if total:
                pct = d["downloaded_bytes"] / total * 100
                self.after(0, lambda: self.bar.configure(value=pct))
                speed = d.get("_speed_str", "").strip()
                eta = d.get("_eta_str", "").strip()
                self.after(0, lambda: self.status.set(f"Downloading {pct:.1f}%  {speed}  ETA {eta}"))
        elif d["status"] == "finished":
            self.after(0, lambda: self.status.set("Processing..."))

    def download(self, url):
        q = self.quality.get()
        opts = {
            "format": QUALITIES[q],
            "outtmpl": os.path.join(self.folder.get(), "%(title)s.%(ext)s"),
            "progress_hooks": [self.hook],
            "noplaylist": True,
            "quiet": True,
        }
        if q.startswith("Audio"):
            opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        else:
            opts["merge_output_format"] = "mp4"
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            self.after(0, lambda: (self.bar.configure(value=100),
                                   self.status.set("Done! Saved to " + self.folder.get())))
        except Exception as e:
            self.after(0, lambda: (self.status.set("Error: " + str(e)[:200]),
                                   messagebox.showerror("Download failed", str(e)[:400])))
        finally:
            self.after(0, lambda: self.btn.config(state="normal"))


if __name__ == "__main__":
    App().mainloop()

# YouTube Video Downloader

A lightweight and user-friendly desktop GUI application built with Python and Tkinter for downloading YouTube videos and playlists using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).

## Features

- **Graphical User Interface:** Clean and intuitive desktop interface powered by Tkinter.
- **Best Quality Default:** One-click download for best available video and audio quality.
- **Quality & Format Selection:** Option to browse and choose specific video resolutions and formats before downloading.
- **Playlist Support:** Toggle playlist downloads on or off with a simple checkbox.
- **Custom Download Location:** Easily browse and choose the destination folder for saved videos.
- **Real-time Progress:** Displays live download percentage and progress bar.
- **Responsive Multithreading:** Downloads run on a background thread to prevent the UI from freezing.
- **Error Logging:** Automatically records any errors to `error_log.txt` for easy troubleshooting.

---

## Prerequisites

- **Python 3.8+**
- **FFmpeg** (Recommended): `yt-dlp` uses FFmpeg to merge high-resolution video streams with audio (e.g., 1080p, 2K, 4K).
  - **Windows:** Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or install via winget:
    ```bash
    winget install Gyan.FFmpeg
    ```
  - **macOS:** `brew install ffmpeg`
  - **Linux:** `sudo apt install ffmpeg`

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LoNE-W0LvES/youtube-downloader.git
   cd youtube-downloader
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   - **Windows:**
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. **How to download:**
   - Paste the YouTube video or playlist link into the **YouTube URL** field.
   - Click **Browse** to select your target download directory.
   - (Optional) Uncheck **Best Quality** if you want to pick a specific resolution/format from a list.
   - (Optional) Check **Download Playlist** if your link is a playlist and you want to download all videos.
   - Click **Download** to begin.

---

## Building Executable (.exe)

You can package the application into a standalone Windows `.exe` using PyInstaller:

```bash
pip install pyinstaller
pyinstaller main.spec
```

The compiled binary will be located in the `dist/` directory.

---

## License

This project is open source and available under the [MIT License](LICENSE).

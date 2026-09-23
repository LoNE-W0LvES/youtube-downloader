# Media & Video Downloader Suite

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/GUI-PySide6%20%28Qt6%29-green.svg?logo=qt&logoColor=white)](https://pyside.org/)
[![yt-dlp](https://img.shields.io/badge/Core-yt--dlp-red.svg?logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![Chrome Extension](https://img.shields.io/badge/Extension-Manifest%20v3-yellow.svg?logo=googlechrome&logoColor=white)](https://developer.chrome.com/docs/extensions/mv3/)
[![FFmpeg](https://img.shields.io/badge/Muxing-FFmpeg-blueviolet.svg?logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)

**A modern, multi-threaded desktop video downloader with seamless Chrome Extension integration, Facebook fallback scraping, and YouTube bot-detection bypass (POT Provider).**

</div>

---

## 🚀 Key Features

- **Multi-Download Queue Management**: Download multiple videos concurrently with individual real-time progress bars, download speeds, and ETAs.
- **YouTube Full Quality Support**: Download in 4K, 1440p, 1080p, 720p, 480p, or extract high-quality audio directly to MP3/M4A.
- **Dual-Method Facebook Downloader**: Integrated fallback parser to handle private, restricted, or complex Facebook video URLs when standard extractors fail.
- **Chrome Browser Extension (Manifest v3)**: Send video URLs and session cookies directly from your active browser tab to the desktop application with a single click.
- **Anti-Bot Bypass (POT Provider)**: Integrates `bgutil-ytdlp-pot-provider` (Proof of Origin Token) to prevent "Sign in to confirm you're not a bot" and HTTP 403 Forbidden errors.
- **Local Communication Server**: Background threaded HTTP server (`server.py`) enables secure two-way communication between the browser extension and the Qt application.
- **Automatic FFmpeg Muxing**: Automatically combines separate video and audio streams into standard MP4/MKV files.

---

## 📁 Project Architecture

```
├── gui.py                      # Main PySide6 desktop GUI application
├── downloader.py               # Core download logic with yt-dlp & Facebook fallback
├── server.py                   # Local HTTP server listening for extension events
├── kill_chrome.bat             # Helper script to release locked browser cookies
├── requirements.txt            # Python dependencies
├── chrome_extension/           # Chrome Extension (Manifest v3)
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   ├── popup.html
│   └── popup.js
├── bgutil-ytdlp-pot-provider/  # YouTube POT token generation plugin
└── ffmpeg/                     # Directory for ffmpeg.exe and ffprobe.exe
```

---

## 🛠️ Installation & Setup

### 1. Clone & Set Up Python Environment

```bash
# Clone the repository
git clone https://github.com/LoNE-W0LvES/youtube-downloader.git
cd youtube-downloader

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### 2. FFmpeg Setup

FFmpeg is required to mux high-definition video and audio streams:
1. Download a portable FFmpeg release for Windows from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or [ffmpeg.org](https://ffmpeg.org/download.html).
2. Extract `ffmpeg.exe` and `ffprobe.exe` into the `ffmpeg/` folder inside this project, or ensure `ffmpeg` is available in your system's `PATH`.

### 3. Chrome Extension Installation (Optional)

1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** in the top-right corner.
3. Click **Load unpacked** and select the `chrome_extension/` folder in this repository.
4. When on any video page (YouTube, Facebook, etc.), click the extension icon to send the URL straight to your desktop downloader queue.

---

## 💻 Usage

Run the GUI application:
```bash
python gui.py
```

### Desktop Interface Controls:
- **Add URL**: Paste any YouTube or Facebook URL and click **Add to Queue** (or send directly from the Chrome extension).
- **Format Selection**: Choose between Best Available, 1080p, 720p, 480p, or Audio Only (MP3).
- **Batch Controls**: **Start All**, **Pause All**, or **Clear Finished** tasks.
- **Custom Output**: Choose your desired target download folder via the browse button.

---

## 🛡️ Anti-Bot & Cookie Authentication

If downloading age-restricted videos or if YouTube triggers bot verification:
- Export your browser cookies using a standard extension (e.g., *Get cookies.txt LOCALLY*) and save them as `cookies.txt` in the root directory.
- The integrated `bgutil-ytdlp-pot-provider` handles automatic token generation when querying YouTube endpoints.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

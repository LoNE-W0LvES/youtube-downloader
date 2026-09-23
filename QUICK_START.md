# YouTube Downloader - Quick Start Guide

## What You Have

A complete YouTube video downloader system with:
- 🖥️ Desktop GUI application (PySide6)
- 🌐 Chrome extension for automatic URL capture
- 📦 Support for multiple resolutions and audio-only downloads
- 📑 Playlist download capability
- 🔗 Automatic organization (videos/audio in separate folders)
- 💻 Can be built as standalone .exe

## Project Structure

```
DOWNLOADER/
├── youtube_downloader.py                    # CLI version (simple)
├── youtube_downloader_gui.py                # GUI version (basic)
├── youtube_downloader_gui_with_extension.py # GUI with extension support ⭐ USE THIS
├── chrome_extension/                         # Chrome extension files
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   ├── background.js
│   ├── content.js
│   ├── icons/                               # Add your icon files here
│   └── README.md
├── requirements.txt                          # Python dependencies
├── build_exe.bat                            # One-click .exe builder
├── BUILD_EXE.md                             # Detailed build instructions
├── CHROME_EXTENSION_SETUP.md                # Extension setup guide
└── README.md                                # Main documentation
```

## Quick Setup (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python youtube_downloader_gui_with_extension.py
```

### Step 3: Install Chrome Extension
1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" → Select `chrome_extension` folder
4. Done!

## How to Use

### Option A: Use Desktop App Only
1. Run `youtube_downloader_gui_with_extension.py`
2. Paste YouTube URL
3. Select quality
4. Check "Download entire playlist" if needed
5. Click Download

### Option B: Use Chrome Extension (Recommended)
1. Run the desktop app first
2. Browse YouTube normally
3. Click the extension icon when you see a video you want
4. Click "Download" in the popup
5. Video automatically downloads!

### Option C: Auto-Download Mode (Like IDM)
1. Run the desktop app
2. Click the extension icon
3. Enable:
   - ✅ Auto-capture YouTube URLs
   - ✅ Auto-download on capture
4. Just visit any YouTube video - it downloads automatically!

## Features

### Resolutions
- Best Quality
- 1080p (Full HD)
- 720p (HD)
- 480p (SD)
- 360p

### Formats
- Video (MP4)
- Audio Only (MP3)

### Special Features
- ✅ Playlist download (checkbox)
- ✅ Auto-capture URLs from Chrome
- ✅ Auto-download mode
- ✅ Organized folders (`downloads/yt_downloader/video` or `/audio`)
- ✅ Real-time progress tracking
- ✅ Download speed and ETA display

## Building .EXE

### Easy Way
Just double-click:
```
build_exe.bat
```

### Manual Way
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="YouTubeDownloader" youtube_downloader_gui_with_extension.py
```

Your .exe will be in: `dist/YouTubeDownloader.exe`

## File Locations

### Downloaded Videos
```
downloads/yt_downloader/video/
```

### Downloaded Audio
```
downloads/yt_downloader/audio/
```

### Playlists
When downloading a playlist, creates a subfolder with the playlist name:
```
downloads/yt_downloader/video/[Playlist Name]/
```

## Which File Should I Use?

| File | When to Use |
|------|-------------|
| `youtube_downloader.py` | Simple CLI, no GUI needed |
| `youtube_downloader_gui.py` | Basic GUI, no extension support |
| `youtube_downloader_gui_with_extension.py` | **⭐ RECOMMENDED** - Full featured with extension support |

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Extension not working
1. Make sure desktop app is running first
2. Check you see "Listening on port 8765" in the app
3. Reload the extension in Chrome

### Downloads failing
1. Check internet connection
2. Verify YouTube URL is valid
3. Try a different quality option
4. For audio: Install FFmpeg

### FFmpeg for Audio Conversion
Audio downloads require FFmpeg:
- **Windows**: Download from https://ffmpeg.org/download.html
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## Common Questions

**Q: Can I distribute the .exe to others?**
A: Yes! The .exe is standalone and includes everything needed.

**Q: Will the Chrome extension work with the .exe?**
A: Yes! Just run the .exe instead of the Python script.

**Q: Can I download entire playlists?**
A: Yes! Check the "Download entire playlist" checkbox.

**Q: How do I change the download folder?**
A: Click "Browse..." in the app or edit the folder path.

**Q: Is this legal?**
A: Only download content you have permission to download. Respect YouTube's ToS and copyright laws.

## Need More Help?

- **Extension Setup**: Read `CHROME_EXTENSION_SETUP.md`
- **Building EXE**: Read `BUILD_EXE.md`
- **General Info**: Read `README.md`

## Tips & Tricks

1. **Keep app running in background** for auto-downloads
2. **Pin extension** to Chrome toolbar for quick access
3. **Set default quality** in extension for faster downloads
4. **Use auto-download** for binge-downloading
5. **Check playlist checkbox** before pasting playlist URLs

## Version Information

- **Python**: 3.7+
- **PySide6**: 6.6.0+
- **yt-dlp**: 2024.0.0+
- **PyInstaller**: 6.0.0+ (for .exe)

## What's Next?

1. ✅ Run the app
2. ✅ Install the extension
3. ✅ Download some videos!
4. ⭐ Build the .exe for easy sharing
5. 🎉 Enjoy your downloader!

---

Made with ❤️ for easy YouTube downloading!

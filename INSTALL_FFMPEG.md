# Installing FFmpeg for Audio Conversion

FFmpeg is required to convert downloaded audio to MP3 format. Without it, audio downloads will remain as `.webm` files.

## Windows Installation (Easy Method)

### Option 1: Using Chocolatey (Recommended)

If you have Chocolatey package manager:
```bash
choco install ffmpeg
```

### Option 2: Manual Installation

1. **Download FFmpeg**
   - Go to: https://www.gyan.dev/ffmpeg/builds/
   - Download: `ffmpeg-release-essentials.zip`

2. **Extract the Files**
   - Extract the ZIP file
   - You'll see a folder like `ffmpeg-7.0-essentials_build`

3. **Add to System PATH**

   **Method A: Quick (Current Session Only)**
   ```bash
   set PATH=%PATH%;C:\path\to\ffmpeg\bin
   ```
   Replace `C:\path\to\ffmpeg\bin` with your actual path

   **Method B: Permanent (Recommended)**
   - Right-click "This PC" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find "Path"
   - Click "Edit"
   - Click "New"
   - Add: `C:\path\to\ffmpeg\bin` (your actual path)
   - Click OK on all dialogs
   - **Restart your terminal/command prompt**

4. **Verify Installation**
   ```bash
   ffmpeg -version
   ```
   You should see version information.

### Option 3: Bundle FFmpeg with Your App (For Distribution)

If you want to distribute your .exe with FFmpeg included:

1. Download `ffmpeg.exe` from the link above
2. Place it in your project folder
3. When building with PyInstaller, use:
   ```bash
   pyinstaller --onefile --windowed --add-binary="ffmpeg.exe;." --name="YouTubeDownloader" youtube_downloader_gui_with_extension.py
   ```

## macOS Installation

### Using Homebrew:
```bash
brew install ffmpeg
```

### Using MacPorts:
```bash
sudo port install ffmpeg
```

## Linux Installation

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

### Fedora:
```bash
sudo dnf install ffmpeg
```

### Arch Linux:
```bash
sudo pacman -S ffmpeg
```

## Verify FFmpeg is Working

After installation:

1. Open a **new** terminal/command prompt
2. Run:
   ```bash
   ffmpeg -version
   ```
3. You should see FFmpeg version information

## Test with Your App

1. **Restart your YouTube Downloader app** (important - it needs to detect FFmpeg)
2. Try downloading audio again
3. It should now convert to MP3 successfully!

## What If I Don't Install FFmpeg?

- **Video downloads**: Work fine without FFmpeg (downloads as MP4)
- **Audio downloads**: Download as `.webm` instead of `.mp3`
  - WebM files work in most media players
  - You can manually convert them later if needed

## Troubleshooting

### "ffmpeg not found" after installation
- Make sure you added FFmpeg to your PATH
- **Restart your terminal/command prompt**
- **Restart the Python app**
- Try running `ffmpeg -version` in terminal

### FFmpeg installed but still not working
1. Check PATH is correct: `echo %PATH%` (Windows) or `echo $PATH` (Mac/Linux)
2. Make sure `ffmpeg.exe` is in a `bin` folder in your PATH
3. Restart your computer (to ensure PATH updates are loaded)

### Permission errors
- On Linux/Mac, you might need to make ffmpeg executable:
  ```bash
  chmod +x /path/to/ffmpeg
  ```

## Quick Test

After installing FFmpeg, test it:
```bash
# This should show FFmpeg is working
ffmpeg -version

# This tests a simple conversion
ffmpeg -f lavfi -i sine=frequency=1000:duration=1 -t 1 test.mp3
```

If `test.mp3` is created, FFmpeg is working correctly!

---

**Note**: Your YouTube Downloader will work without FFmpeg, but audio files will be downloaded as WebM instead of MP3.

# Building YouTube Downloader as .EXE

This guide will help you create a standalone `.exe` file for the YouTube Downloader application.

## Prerequisites

1. Python 3.7 or higher installed
2. All dependencies installed (run `pip install -r requirements.txt`)
3. PyInstaller installed

## Step 1: Install PyInstaller

If not already installed:
```bash
pip install pyinstaller
```

## Step 2: Build the EXE

### Option A: Simple One-File Build (Recommended for Distribution)

Run this command in the project directory:

```bash
pyinstaller --onefile --windowed --name="YouTubeDownloader" --icon=chrome_extension/icons/icon128.png youtube_downloader_gui_with_extension.py
```

**Parameters explained:**
- `--onefile`: Creates a single executable file
- `--windowed`: No console window (GUI only)
- `--name`: Name of the executable
- `--icon`: Application icon (optional, you need to create this)

### Option B: Directory Build (Faster startup)

```bash
pyinstaller --windowed --name="YouTubeDownloader" --icon=chrome_extension/icons/icon128.png youtube_downloader_gui_with_extension.py
```

This creates a folder with the .exe and dependencies.

### Option C: Advanced Build with Custom Spec File

For more control, create a custom spec file:

```bash
pyinstaller --name="YouTubeDownloader" --windowed youtube_downloader_gui_with_extension.py
```

This creates `YouTubeDownloader.spec`. Edit it if needed, then build:

```bash
pyinstaller YouTubeDownloader.spec
```

## Step 3: Find Your EXE

After building, find your executable in:
- **One-file build**: `dist/YouTubeDownloader.exe`
- **Directory build**: `dist/YouTubeDownloader/YouTubeDownloader.exe`

## Step 4: Test the EXE

1. Navigate to the `dist` folder
2. Double-click `YouTubeDownloader.exe`
3. The application should start without needing Python installed

## Step 5: Distribute

You can now distribute the `.exe` file or the entire `dist/YouTubeDownloader` folder.

### For One-File Build:
- Just share the single `.exe` file
- Users can run it directly without installation

### For Directory Build:
- Share the entire `dist/YouTubeDownloader` folder
- All files in that folder are needed

## Creating an Icon (Optional)

If you want a custom icon:

1. Create or download a `.ico` file (Windows icon format)
2. Place it in the project directory
3. Use `--icon=your_icon.ico` in the PyInstaller command

You can convert PNG to ICO using online tools like:
- https://convertio.co/png-ico/
- https://www.icoconverter.com/

## Troubleshooting

### "Failed to execute script" Error

Add this to your PyInstaller command:
```bash
pyinstaller --onefile --windowed --debug=all --name="YouTubeDownloader" youtube_downloader_gui_with_extension.py
```

### Missing Dependencies

If the .exe crashes, some dependencies might be missing. Try:

```bash
pyinstaller --onefile --windowed --hidden-import=yt_dlp --hidden-import=PySide6 --name="YouTubeDownloader" youtube_downloader_gui_with_extension.py
```

### Large File Size

The .exe will be large (100-200 MB) because it includes Python and all dependencies. This is normal.

To reduce size:
- Use directory build instead of one-file
- Remove unused dependencies
- Use UPX compression (add `--upx-dir=path/to/upx`)

### Antivirus False Positives

Some antivirus software may flag the .exe as suspicious. This is common with PyInstaller executables. You can:
- Add an exception in your antivirus
- Sign the executable with a code signing certificate (for professional distribution)

## Complete Build Script

Create a file called `build.bat` (Windows) or `build.sh` (Mac/Linux):

**build.bat:**
```batch
@echo off
echo Building YouTube Downloader...
pyinstaller --onefile --windowed --name="YouTubeDownloader" youtube_downloader_gui_with_extension.py
echo.
echo Build complete! Find your .exe in the dist folder.
pause
```

**build.sh:**
```bash
#!/bin/bash
echo "Building YouTube Downloader..."
pyinstaller --onefile --windowed --name="YouTubeDownloader" youtube_downloader_gui_with_extension.py
echo ""
echo "Build complete! Find your executable in the dist folder."
```

Make it executable (Mac/Linux):
```bash
chmod +x build.sh
./build.sh
```

Run it (Windows):
```bash
build.bat
```

## Notes

- The first build will take several minutes
- Subsequent builds are faster
- The `build` and `dist` folders are created during the build process
- You can delete the `build` folder after building (the `dist` folder contains your .exe)
- The Chrome extension will still work with the .exe version!

## FFmpeg Requirement

For audio conversion (MP3), users will need FFmpeg installed on their system. You have two options:

### Option 1: User installs FFmpeg
Provide instructions for users to install FFmpeg separately.

### Option 2: Bundle FFmpeg (Recommended)
1. Download FFmpeg: https://ffmpeg.org/download.html
2. Extract `ffmpeg.exe`
3. Add to PyInstaller command:
```bash
pyinstaller --onefile --windowed --add-binary="ffmpeg.exe;." --name="YouTubeDownloader" youtube_downloader_gui_with_extension.py
```

## Final Checklist

- [ ] Install PyInstaller
- [ ] Run build command
- [ ] Test the .exe
- [ ] Test downloading a video
- [ ] Test Chrome extension integration
- [ ] Create installer (optional - use Inno Setup or NSIS)

Congratulations! You now have a standalone YouTube Downloader application!

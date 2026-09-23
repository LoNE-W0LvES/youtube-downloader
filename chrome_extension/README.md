# YouTube Downloader Chrome Extension

This Chrome extension automatically captures YouTube URLs and sends them to the YouTube Downloader desktop application.

## Features

- Automatically detect YouTube videos
- Capture URLs with one click
- Select video quality before downloading
- Auto-capture and auto-download options
- Download button integrated into YouTube player
- Desktop app integration

## Installation

### Step 1: Add Icons

You need to add icon images to the `icons` folder:
- `icon16.png` (16x16 pixels)
- `icon48.png` (48x48 pixels)
- `icon128.png` (128x128 pixels)

You can create simple icons or download YouTube-related icons from icon websites.

### Step 2: Load Extension in Chrome

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome_extension` folder
5. The extension should now appear in your extensions list

### Step 3: Pin the Extension

- Click the puzzle icon in Chrome toolbar
- Find "YouTube Downloader Extension"
- Click the pin icon to keep it visible

## Usage

1. **Make sure the desktop app is running** (youtube_downloader_gui.exe)
2. Navigate to any YouTube video
3. Click the extension icon in the toolbar
4. The URL will be automatically captured
5. Select your preferred quality
6. Click "Download" button

### Auto-Capture Mode

Enable "Auto-capture YouTube URLs" in the extension popup to automatically detect videos as you browse YouTube.

### Auto-Download Mode

Enable both auto-capture and "Auto-download on capture" to automatically start downloads when you visit a YouTube video.

## Desktop App Connection

The extension connects to the desktop app via:
1. **Native Messaging** (preferred) - Direct communication
2. **HTTP Fallback** (port 8765) - If native messaging fails

Make sure the desktop app is running before using the extension!

## Troubleshooting

### Extension shows "App Not Connected"
- Make sure the desktop application is running
- Check that native messaging host is installed correctly
- Try restarting Chrome

### Download button doesn't work
- Verify you're on a YouTube video page
- Check that the URL is captured (shown in the extension popup)
- Ensure the desktop app is running

### Icons not showing
- Add icon PNG files to the `icons` folder
- Reload the extension in `chrome://extensions/`

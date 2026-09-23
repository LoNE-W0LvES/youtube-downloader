# Chrome Extension Setup Guide

This guide explains how to install and use the YouTube Downloader Chrome Extension with the desktop application.

## Features

- Automatically captures YouTube video URLs
- One-click download from Chrome
- Auto-capture and auto-download modes
- Download button integrated into YouTube player
- Quality selection from extension popup
- Real-time connection status with desktop app

## Installation

### Step 1: Load the Extension in Chrome

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable **Developer mode** (toggle in the top right corner)
3. Click **"Load unpacked"**
4. Navigate to and select the `chrome_extension` folder in this project
5. The extension should now appear in your extensions list

### Step 2: Add Extension Icons (Optional but Recommended)

The extension needs icon files to display properly:

1. Go to `chrome_extension/icons/` folder
2. Add three icon files:
   - `icon16.png` (16x16 pixels)
   - `icon48.png` (48x48 pixels)
   - `icon128.png` (128x128 pixels)

You can:
- Create simple icons with any image editor
- Download free YouTube/download icons from icon websites
- Use colored squares as placeholders for testing

### Step 3: Pin the Extension

1. Click the **puzzle icon** in Chrome toolbar (Extensions)
2. Find "YouTube Downloader Extension"
3. Click the **pin icon** to keep it visible in your toolbar

### Step 4: Start the Desktop Application

**IMPORTANT:** The extension needs the desktop app running to work!

Run the desktop application:
```bash
python youtube_downloader_gui_with_extension.py
```

Or if you built the .exe:
```bash
YouTubeDownloader.exe
```

You should see:
- "HTTP server started on port 8765" in the app logs
- "Chrome Extension: Listening on port 8765" in the app window

## How to Use

### Method 1: Manual Capture

1. Go to any YouTube video page
2. Click the extension icon in your toolbar
3. The URL will be automatically captured
4. Select your preferred quality from the dropdown
5. Click **"Download"** button

### Method 2: Auto-Capture Mode

1. Click the extension icon
2. Enable **"Auto-capture YouTube URLs"**
3. Browse YouTube normally
4. The extension will automatically detect and capture video URLs
5. Click the extension icon and press Download when ready

### Method 3: Auto-Download Mode (Fully Automatic)

1. Click the extension icon
2. Enable both:
   - ✅ **"Auto-capture YouTube URLs"**
   - ✅ **"Auto-download on capture"**
3. Select your preferred default quality
4. Simply visit any YouTube video - it will automatically start downloading!

### Method 4: In-Page Download Button

The extension adds a download button directly on the YouTube player:
1. Look for the **⬇️** button in the YouTube video player controls
2. Click it to instantly start downloading with default settings (720p)

## Extension Settings

### Quality/Format Options
- Best Quality
- 1080p (Full HD)
- 720p (HD) - Default
- 480p (SD)
- 360p
- Audio Only (MP3)

### Auto-Capture
When enabled, the extension automatically detects when you visit a YouTube video and captures the URL.

### Auto-Download
When enabled with auto-capture, downloads start immediately when you visit a video. Make sure the desktop app is running!

## Connection Status

The extension popup shows the connection status:

- 🟢 **"App Connected"** - Desktop app is running and ready
- 🔴 **"App Not Connected"** - Desktop app is not running or can't be reached

If you see "App Not Connected":
1. Make sure the desktop application is running
2. Check that port 8765 is not blocked by firewall
3. Try restarting the desktop app
4. Try restarting Chrome

## How It Works

The extension communicates with the desktop app in two ways:

### 1. HTTP Communication (Default)
- Extension sends download requests to `http://localhost:8765`
- Simple and reliable
- Works immediately

### 2. Native Messaging (Advanced)
- Direct communication between Chrome and desktop app
- Requires additional setup (manifest installation)
- More secure and efficient

Currently, the HTTP method works out of the box!

## Troubleshooting

### Extension not capturing URLs
- Make sure you're on a YouTube video page (not homepage)
- Check that the URL contains `/watch?v=`
- Reload the page and try again

### Download button does nothing
- Verify the desktop app is running
- Check the extension popup for "App Connected" status
- Look at the desktop app logs for error messages

### Auto-download not working
- Make sure both checkboxes are enabled
- Verify the desktop app is running BEFORE you visit YouTube
- Check that you have write permissions to the download folder

### Icons not showing
- Add the icon PNG files to `chrome_extension/icons/` folder
- Reload the extension in `chrome://extensions/`
- Click the refresh icon next to the extension

### Permission errors
- The extension needs permissions for YouTube domains
- Check that permissions are granted in `chrome://extensions/`
- You may need to reload the extension after changing permissions

## Uninstalling

To remove the extension:
1. Go to `chrome://extensions/`
2. Find "YouTube Downloader Extension"
3. Click **"Remove"**
4. Confirm the removal

## Privacy & Security

- The extension only runs on YouTube pages
- No data is sent to external servers
- All communication is local (between Chrome and desktop app)
- No tracking or analytics
- Your download history stays on your computer

## Tips

- Set your most-used quality as default in the extension
- Keep the desktop app minimized in the background
- Use auto-download for binge-watching/downloading sessions
- The in-page download button is great for quick downloads
- Disable auto-download when just browsing to avoid unwanted downloads

## Updates

After updating the extension files:
1. Go to `chrome://extensions/`
2. Find the extension
3. Click the **refresh/reload icon**
4. Extension is now updated!

## Support

If you encounter issues:
1. Check the desktop app logs
2. Open Chrome DevTools (F12) on YouTube
3. Check the Console tab for errors
4. Ensure both app and extension are up to date

Happy downloading! 🎥📥

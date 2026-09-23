# Fix YouTube Signature Errors - Install Node.js

If you're getting errors like:
- "Signature solving failed"
- "n challenge solving failed"
- "Only images are available"

You need to install **Node.js** for yt-dlp to decrypt YouTube URLs.

## Quick Install (5 minutes)

### Windows

**Option 1: Official Installer (Recommended)**
1. Go to: https://nodejs.org/
2. Download the **LTS version** (Long Term Support)
3. Run the installer
4. Click "Next" through all steps (default options are fine)
5. **Restart your computer** (important!)
6. Verify installation:
   ```bash
   node --version
   ```

**Option 2: Chocolatey**
```bash
choco install nodejs
```

### macOS

**Homebrew:**
```bash
brew install node
```

### Linux

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install nodejs npm
```

**Fedora:**
```bash
sudo dnf install nodejs
```

## Verify Installation

Open a **new** terminal and run:
```bash
node --version
npm --version
```

You should see version numbers (e.g., v20.x.x).

## Test the Downloader

After installing Node.js:

1. **Restart your computer** (ensures PATH is updated)
2. **Restart the downloader app**
3. **Try downloading again**

The "signature solving" errors should be gone!

## Why This Helps

YouTube encrypts video URLs with JavaScript. yt-dlp needs Node.js to run that JavaScript and decrypt the URLs. Without it, yt-dlp can only get thumbnails/images.

## Alternative: Use Pytube Fallback

If you don't want to install Node.js, the app now has a **pytube fallback**:

```bash
pip install pytubefix
```

The app will automatically try pytube if yt-dlp fails!

## Troubleshooting

### "node: command not found" after installation
- **Restart your terminal/command prompt**
- **Restart your computer**
- Check PATH environment variable includes Node.js

### Still getting errors after installing Node.js
- Make sure you restarted the app
- Try updating yt-dlp: `pip install --upgrade yt-dlp`
- Check Node.js is in PATH: `where node` (Windows) or `which node` (Mac/Linux)

### Don't want to install Node.js?
The app will automatically fall back to pytube (simpler but fewer features)

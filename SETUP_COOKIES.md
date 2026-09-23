# Setting Up Cookies to Bypass YouTube Bot Detection

YouTube has strict bot detection. Using your browser cookies makes downloads work reliably.

## Quick Setup (3 Minutes)

### Step 1: Install Browser Extension

**For Chrome:**
1. Go to Chrome Web Store
2. Search for: **"Get cookies.txt LOCALLY"**
3. Install the extension
4. Link: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc

**For Firefox:**
1. Go to Firefox Add-ons
2. Search for: **"cookies.txt"**
3. Install: "cookies.txt" extension

### Step 2: Export YouTube Cookies

1. **Go to YouTube.com** in your browser
2. **Make sure you're logged in** to your YouTube/Google account
3. **Click the extension icon** (cookie icon in toolbar)
4. Click **"Export"** or **"Current Site"**
5. A `cookies.txt` file will be downloaded

### Step 3: Place Cookies File

1. Find the downloaded `cookies.txt` file (usually in Downloads folder)
2. **Move it to your project folder**:
   ```
   DOWNLOADER/
   ├── cookies.txt          ← Place it here!
   ├── youtube_downloader_gui_with_extension.py
   └── ...
   ```

### Step 4: Restart App

```bash
python youtube_downloader_gui_with_extension.py
```

You should see:
```
[INFO] Using cookies from: C:\...\DOWNLOADER\cookies.txt
```

### Step 5: Test Download

Try downloading again - it should work perfectly now!

## Why This Works

✅ **Reliable**: Uses your actual browser session
✅ **No Chrome locking**: Works even with Chrome open
✅ **Easy to update**: Just re-export when cookies expire
✅ **Portable**: Copy cookies.txt to any device

## When to Re-Export Cookies

Export fresh cookies if:
- Downloads start failing with "Sign in" or "bot" errors
- You logged out/in to YouTube
- After ~30 days (cookies expire)

Just repeat Step 2-3 above!

## Alternative: Close Chrome Method

If you don't want to use a cookies file:

1. **Close Chrome completely** (all windows, check taskbar)
2. **Run the app**
3. The app will try to extract cookies from closed Chrome
4. **Keep Chrome closed** while downloading

But the cookies.txt method is easier!

## For Distribution (.exe)

When building your .exe:
- **Don't include your personal cookies.txt** in distribution!
- Users should export their own cookies
- Include this guide (SETUP_COOKIES.md) with your .exe

## Troubleshooting

### "Still getting bot detection"
- Make sure cookies.txt is in the right folder (same folder as the .py file)
- Check you're logged into YouTube when exporting
- Try re-exporting fresh cookies
- Make sure the file is named exactly `cookies.txt`

### "Extension not working"
- Try a different cookie extension
- Some extensions: "Get cookies.txt LOCALLY", "cookies.txt", "EditThisCookie"
- Export format must be "Netscape" format

### "Cookies expired"
- YouTube cookies expire after ~30 days
- Just export fresh cookies again
- App will automatically use the new file

## Privacy Note

**Your cookies.txt file contains your login session!**
- Don't share it with others
- Don't commit it to Git
- Keep it private
- It's in .gitignore by default

## Video Tutorial

Not working? Here's what to do:

1. Install "Get cookies.txt LOCALLY" from Chrome Web Store
2. Go to YouTube.com (make sure you're logged in)
3. Click the extension icon
4. Click "Export" → "Current Site"
5. Move cookies.txt to project folder
6. Restart the app
7. Download should work!

That's it! This is the most reliable method for bypassing YouTube's bot detection. 🎉

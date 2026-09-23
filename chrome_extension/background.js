// Background script for YouTube & Facebook Downloader Extension

let appConnected = false;

// No native messaging - we use HTTP only for simplicity

// Listen for messages from popup and content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('[Background] Received message:', request.action);

    if (request.action === 'download') {
        console.log('[Background] Download request received');
        console.log('[Background]   URL:', request.url);
        console.log('[Background]   Quality:', request.quality);
        console.log('[Background]   Download Playlist:', request.downloadPlaylist);
        handleDownload(request.url, request.quality, request.downloadPlaylist, sendResponse);
        return true; // Keep channel open for async response
    } else if (request.action === 'checkConnection') {
        console.log('[Background] Connection check requested');
        checkHTTPConnection(sendResponse);
        return true; // Keep channel open for async response
    }
});

// Check HTTP connection to desktop app
function checkHTTPConnection(callback) {
    console.log('[Background] Checking connection to http://localhost:8765/health');
    fetch('http://localhost:8765/health', {
        method: 'GET',
        signal: AbortSignal.timeout(2000) // 2 second timeout
    })
    .then(response => {
        console.log('[Background] Health check response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('[Background] Health check data:', data);
        if (data.status === 'ok') {
            appConnected = true;
            console.log('[Background] App is connected!');
            callback({ connected: true });
        } else {
            appConnected = false;
            console.log('[Background] App returned non-ok status');
            callback({ connected: false });
        }
    })
    .catch(error => {
        console.error('[Background] Health check failed:', error);
        appConnected = false;
        callback({ connected: false });
    });
}

// Handle download request
function handleDownload(url, quality, downloadPlaylist, callback) {
    // Always use HTTP (simpler than native messaging)
    sendViaHTTP(url, quality, downloadPlaylist, callback);
}

// Detect platform from URL
function detectPlatform(url) {
    const urlLower = url.toLowerCase();
    if (urlLower.includes('youtube.com') || urlLower.includes('youtu.be')) {
        return 'youtube';
    } else if (urlLower.includes('facebook.com') || urlLower.includes('fb.watch')) {
        return 'facebook';
    } else if (urlLower.includes('tiktok.com')) {
        return 'tiktok';
    } else if (urlLower.includes('instagram.com')) {
        return 'instagram';
    }
    return 'unknown';
}

// Get cookies from browser for the appropriate platform
async function getPlatformCookies(url) {
    try {
        const platform = detectPlatform(url);
        let domain = '';

        if (platform === 'youtube') {
            domain = '.youtube.com';
        } else if (platform === 'facebook') {
            domain = '.facebook.com';
        } else if (platform === 'tiktok') {
            domain = '.tiktok.com';
        } else if (platform === 'instagram') {
            // Instagram often uses multiple subdomains, so using the base domain might be more reliable.
            // Or we could gather cookies for multiple domains if needed, but for now, let's try the base.
            domain = '.instagram.com';
        } else {
            return '';
        }

        const cookies = await chrome.cookies.getAll({ domain: domain });

        // Convert to cookie string format
        let cookieString = '';
        cookies.forEach(cookie => {
            cookieString += `${cookie.name}=${cookie.value}; `;
        });

        console.log(`[Extension] Extracted ${platform} cookies`);
        return cookieString;
    } catch (error) {
        console.error('[Extension] Failed to get cookies:', error);
        return '';
    }
}

// Send via HTTP to localhost
async function sendViaHTTP(url, quality, downloadPlaylist, callback) {
    const platform = detectPlatform(url);
    console.log(`[Extension] Sending ${platform} download request to http://localhost:8765/download`);
    console.log('[Extension] URL:', url);
    console.log('[Extension] Quality:', quality);
    console.log('[Extension] Download Playlist:', downloadPlaylist);

    // Get cookies from browser for the appropriate platform
    const cookies = await getPlatformCookies(url);

    fetch('http://localhost:8765/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            url: url,
            quality: quality,
            downloadPlaylist: downloadPlaylist !== false,  // Default to true
            cookies: cookies,
            platform: platform
        })
    })
    .then(response => {
        console.log('[Extension] Got response:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('[Extension] Download started via HTTP:', data);
        callback({ success: true });
    })
    .catch(error => {
        console.error('[Extension] Failed to send via HTTP:', error);
        callback({ success: false, error: error.message });
    });
}

// Monitor YouTube and Facebook tabs
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        const platform = detectPlatform(tab.url);

        if ((platform === 'youtube' && tab.url.includes('youtube.com/watch')) ||
            (platform === 'facebook' && (tab.url.includes('facebook.com/') || tab.url.includes('fb.watch/')))) {

            // Check if auto-download is enabled
            chrome.storage.sync.get(['autoCapture', 'autoDownload', 'defaultQuality', 'downloadPlaylist'], (data) => {
                if (data.autoCapture) {
                    // Notify content script
                    chrome.tabs.sendMessage(tabId, { action: 'captureUrl' });

                    if (data.autoDownload) {
                        const quality = data.defaultQuality || '720p';
                        const downloadPlaylist = data.downloadPlaylist !== false; // Default to true

                        handleDownload(tab.url, quality, downloadPlaylist, () => {});
                    }
                }
            });
        }
    }
});

// Helper function to strip playlist parameters
function stripPlaylistParams(url) {
    try {
        const urlObj = new URL(url);
        // Remove playlist-related parameters
        urlObj.searchParams.delete('list');
        urlObj.searchParams.delete('index');
        return urlObj.toString();
    } catch (e) {
        // If URL parsing fails, return original
        return url;
    }
}

// Log startup
console.log('[Extension] YouTube & Facebook Downloader background script loaded');

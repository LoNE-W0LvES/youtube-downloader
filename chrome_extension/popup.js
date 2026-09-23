// Popup script for Video Downloader Extension

let currentUrl = '';
let appConnected = false;

// Load saved settings
chrome.storage.sync.get(['autoCapture', 'autoDownload', 'defaultQuality', 'downloadPlaylist'], (data) => {
    document.getElementById('autoCapture').checked = data.autoCapture || false;
    document.getElementById('autoDownload').checked = data.autoDownload || false;
    document.getElementById('downloadPlaylist').checked = data.downloadPlaylist || false;
    if (data.defaultQuality) {
        document.getElementById('qualitySelect').value = data.defaultQuality;
    }
});

// Check if app is running
checkAppConnection();

// Check connection periodically (every 3 seconds)
setInterval(checkAppConnection, 3000);

// Manual refresh button
document.getElementById('refreshConnectionBtn').addEventListener('click', () => {
    console.log('[Popup] Manual connection check requested');
    updateConnectionStatus(false); // Show checking state
    checkAppConnection();
});

// Get current tab URL and update UI
function updateCurrentUrlFromContentScript() {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0] && tabs[0].id) {
            chrome.tabs.sendMessage(tabs[0].id, { action: 'captureUrl' }, (response) => {
                if (chrome.runtime.lastError) {
                    console.error('[Popup] Error sending message to content script:', chrome.runtime.lastError.message);
                    displayUrl('Could not retrieve URL from current tab.', true);
                    document.getElementById('downloadBtn').disabled = true;
                } else if (response && response.url) {
                    currentUrl = response.url;
                    displayUrl(currentUrl);
                    document.getElementById('downloadBtn').disabled = false;
                    // Auto-download if enabled and app is connected
                    chrome.storage.sync.get(['autoDownload'], (data) => {
                        if (data.autoDownload && appConnected) {
                            const quality = document.getElementById('qualitySelect').value;
                            sendToApp(currentUrl, quality);
                        }
                    });
                } else {
                    displayUrl('No video URL detected on this page.', true);
                    document.getElementById('downloadBtn').disabled = true;
                }
            });
        }
    });
}

// Initial URL capture on popup open
updateCurrentUrlFromContentScript();


// Capture URL button
document.getElementById('captureBtn').addEventListener('click', () => {
    updateCurrentUrlFromContentScript();
    showNotification('URL capture requested. Checking page...', 'info');
});

// Download button
document.getElementById('downloadBtn').addEventListener('click', () => {
    console.log('[Popup] Download button clicked!');
    console.log('[Popup] Current URL:', currentUrl);
    if (currentUrl) {
        const quality = document.getElementById('qualitySelect').value;
        sendToApp(currentUrl, quality);
    } else {
        showNotification('No URL captured! Click "Capture URL" first.', 'error');
    }
});

// Auto-capture checkbox
document.getElementById('autoCapture').addEventListener('change', (e) => {
    chrome.storage.sync.set({ autoCapture: e.target.checked });
    if (e.target.checked) {
        showNotification('Auto-capture enabled', 'success');
    }
});

// Auto-download checkbox
document.getElementById('autoDownload').addEventListener('change', (e) => {
    chrome.storage.sync.set({ autoDownload: e.target.checked });
});

// Download playlist checkbox
document.getElementById('downloadPlaylist').addEventListener('change', (e) => {
    chrome.storage.sync.set({ downloadPlaylist: e.target.checked });
    if (e.target.checked) {
        showNotification('Will download entire playlist (if available)', 'success');
    } else {
        showNotification('Will download single video only', 'success');
    }
});

// Quality select
document.getElementById('qualitySelect').addEventListener('change', (e) => {
    chrome.storage.sync.set({ defaultQuality: e.target.value });
});

// Helper functions
function displayUrl(url, isEmpty = false) {
    const urlDisplay = document.getElementById('currentUrl');
    urlDisplay.textContent = url;
    if (isEmpty) {
        urlDisplay.classList.add('empty');
    } else {
        urlDisplay.classList.remove('empty');
    }
}

function sendToApp(url, quality) {
    console.log('[Popup] sendToApp() called');
    console.log('[Popup]   Original URL:', url);
    console.log('[Popup]   Quality:', quality);

    chrome.storage.sync.get(['downloadPlaylist'], (data) => {
        const downloadPlaylist = data.downloadPlaylist || false;

        chrome.runtime.sendMessage({
            action: 'download',
            url: url,
            quality: quality,
            downloadPlaylist: downloadPlaylist
        }, (response) => {
            if (response && response.success) {
                showNotification('Download started!', 'success');
            } else {
                showNotification('Failed to start download. Is the app running?', 'error');
            }
        });
    });
}

function checkAppConnection() {
    chrome.runtime.sendMessage({ action: 'checkConnection' }, (response) => {
        if (chrome.runtime.lastError) {
            console.error('[Popup] Runtime error during connection check:', chrome.runtime.lastError.message);
            appConnected = false;
            updateConnectionStatus(false);
        } else if (response && response.connected) {
            appConnected = true;
            updateConnectionStatus(true);
        } else {
            appConnected = false;
            updateConnectionStatus(false);
        }
    });
}

function updateConnectionStatus(connected) {
    const statusDiv = document.getElementById('status');
    const refreshBtn = document.getElementById('refreshConnectionBtn');
    if (connected) {
        statusDiv.innerHTML = '🟢 App Connected';
        statusDiv.className = 'status connected';
        statusDiv.appendChild(refreshBtn);
    } else {
        statusDiv.innerHTML = '🔴 App Not Connected';
        statusDiv.className = 'status disconnected';
        statusDiv.appendChild(refreshBtn);
    }
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        padding: 10px 15px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        ${type === 'success' ? 'background-color: #4CAF50;' : (type === 'error' ? 'background-color: #f44336;' : 'background-color: #2196F3;')}
    `;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Listen for URL updates from content script (for SPAs)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'urlChanged' && request.url) {
        currentUrl = request.url;
        displayUrl(currentUrl);
        document.getElementById('downloadBtn').disabled = false;
    }
});

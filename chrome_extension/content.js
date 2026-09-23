function detectPlatform() {
    try {
        const url = window.location.href.toLowerCase();
        if (url.includes('youtube.com')) {
            return 'youtube';
        } else if (url.includes('facebook.com') || url.includes('fb.watch')) {
            return 'facebook';
        } else if (url.includes('tiktok.com')) {
            return 'tiktok';
        } else if (url.includes('instagram.com')) {
            return 'instagram';
        }
        return '';
    } catch (error) {
        console.error('[Extension] Error in detectPlatform:', error);
        return '';
    }
}

// Function to check if the current page is a YouTube video page
function checkYouTubeVideo() {
    const url = window.location.href;
    return url.includes('youtube.com/watch') || url.includes('youtube.com/shorts');
}

// Function to extract the canonical URL for YouTube videos
function extractCanonicalUrl() {
    const url = window.location.href;
    try {
        const urlObj = new URL(url);
        // Remove playlist and other non-essential parameters for a cleaner URL
        urlObj.searchParams.delete('list');
        urlObj.searchParams.delete('index');
        urlObj.searchParams.delete('t'); // Remove start time parameter
        urlObj.searchParams.delete('feature');
        return urlObj.toString();
    } catch (e) {
        console.error('[Extension] Error parsing URL for canonical extraction:', e);
        return url; // Return original URL if parsing fails
    }
}

function addFacebookWatchButton(rootElement = document) {
    try {
        const buttonArea = rootElement.querySelector('div[class*="x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1n2onr6 x16tdsg8 x1ja2u2z x1y1aw1k x1sxyh0 x1k90msu xh8yej3"]');
        if (!buttonArea || buttonArea.querySelector('.fb-downloader-btn')) {
            return;
        }

        console.log('[Facebook Watch] Button area found. Adding download button.');

        const downloadBtn = document.createElement('div');
        downloadBtn.className = 'fb-downloader-btn';
        downloadBtn.innerHTML = `
            <div style="display: flex; align-items: center; cursor: pointer; color: white; padding: 8px 12px; background-color: rgba(255, 255, 255, 0.1); border-radius: 6px;">
                <svg viewBox="0 0 24 24" style="width: 20px; height: 20px; fill: currentColor; margin-right: 8px;"><path d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z"></path></svg>
                <span>Download</span>
            </div>
        `;

        downloadBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const videoUrl = window.location.href;
            console.log('[Facebook Watch] Sending download request for URL:', videoUrl);
            chrome.storage.sync.get(['defaultQuality'], (data) => {
                const quality = data.defaultQuality || 'best';
                chrome.runtime.sendMessage({
                    action: 'download',
                    url: videoUrl,
                    quality: quality,
                    downloadPlaylist: false
                });
            });
        });

        buttonArea.prepend(downloadBtn);
        console.log('[Facebook Watch] Download button added successfully.');

    } catch (error) {
        console.error('[Facebook Watch] Error adding download button:', error);
    }
}
function addFacebookReelsButton(rootElement = document) {
    try {
        const reels = rootElement.querySelectorAll('div[aria-label*="Reel"], div.x1ed109x.x18wzrn2.x1n2onr6.x1h4ww2i');
        if (reels.length === 0) return;

        console.log(`[Facebook Reels] Found ${reels.length} reel(s).`);

        reels.forEach((reel, index) => {
            if (reel.querySelector('.fb-reel-downloader-btn')) return;

            const actionBar = reel.querySelector('div[class*="x6s0dn4 x78zum5 x1n2onr6 xh8yej3"]');
            if (!actionBar) return;

            console.log(`[Facebook Reels] Action bar found for reel ${index + 1}. Adding button.`);

            const downloadBtn = document.createElement('div');
            downloadBtn.className = 'fb-reel-downloader-btn';
            downloadBtn.innerHTML = `
                <div style="display: flex; flex-direction: column; align-items: center; cursor: pointer; color: white; margin-top: 15px;">
                    <svg viewBox="0 0 24 24" style="width: 28px; height: 28px; fill: currentColor;"><path d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z"></path></svg>
                    <span style="font-size: 13px; margin-top: 5px;">Download</span>
                </div>
            `;

            downloadBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                let videoUrl = window.location.href;
                // Try to find a more specific URL if possible
                const reelLink = reel.querySelector('a[href*="/reel/"]');
                if (reelLink) {
                    videoUrl = reelLink.href;
                }
                console.log('[Facebook Reels] Sending download request for URL:', videoUrl);
                chrome.storage.sync.get(['defaultQuality'], (data) => {
                    const quality = data.defaultQuality || 'best';
                    chrome.runtime.sendMessage({
                        action: 'download',
                        url: videoUrl,
                        quality: quality,
                        downloadPlaylist: false
                    });
                });
            });

            actionBar.appendChild(downloadBtn);
            console.log(`[Facebook Reels] Button added to reel ${index + 1}.`);
        });

    } catch (error) {
        console.error('[Facebook Reels] Error adding buttons:', error);
    }
}

// ==================== FACEBOOK ====================

function addFacebookDownloadButtonToVideo(video, index) {
    try {
        const container = video.closest('div[class*="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z"]');
        if (!container || container.querySelector('.fb-downloader-btn')) return;

        const downloadBtn = document.createElement('div');
        downloadBtn.className = 'fb-downloader-btn';
        downloadBtn.innerHTML = `<div style="position: absolute; top: 10px; right: 10px; z-index: 100; cursor: pointer; background-color: rgba(0,0,0,0.7); border-radius: 50%; padding: 8px;">
            <svg viewBox="0 0 24 24" style="width: 20px; height: 20px; fill: white;"><path d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z"></path></svg>
        </div>`;

        downloadBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const videoUrl = window.location.href;
            console.log('[Facebook] Sending download request for URL:', videoUrl);
            chrome.storage.sync.get(['defaultQuality'], (data) => {
                const quality = data.defaultQuality || 'best';
                chrome.runtime.sendMessage({
                    action: 'download',
                    url: videoUrl,
                    quality: quality,
                    downloadPlaylist: false
                });
            });
        });

        container.style.position = 'relative';
        container.appendChild(downloadBtn);
        console.log(`[Facebook] Button added to video ${index + 1}.`);
        return true;

    } catch (error) {
        console.error(`[Facebook] Error adding button to video ${index + 1}:`, error);
        return false;
    }
}

// Function to add a download button to YouTube videos
function addYouTubeDownloadButton(rootElement = document) {
    try {
        const controls = rootElement.querySelector('#movie_player .ytp-right-controls');

        // If controls are not in the current node, just exit. This is expected for most mutations.
        if (!controls) {
            return;
        }

        // If we are here, we found player controls. Now check for existing button.
        if (controls.querySelector('#yt-downloader-btn')) {
            // Button already exists, no need to do anything.
            return;
        }

        console.log('[YouTube] Player controls found. Adding download button...');
        
        // If we reach here, 'controls' is found and button does not exist.
        // Proceed with button creation and injection.
        const downloadBtn = document.createElement('button');
        downloadBtn.id = 'yt-downloader-btn';
        downloadBtn.className = 'ytp-button';
        downloadBtn.innerHTML = `
            <svg viewBox="0 0 24 24" style="width: 24px; height: 24px; fill: white;">
                <path d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z" />
            </svg>
        `;
        downloadBtn.title = 'Download with Video Downloader';
        

                    downloadBtn.addEventListener('click', (e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        const url = extractCanonicalUrl(); // Use robust canonical URL
                        console.log('[YouTube] Sending download request for URL:', url); // ADDED LOG
                        chrome.runtime.sendMessage({
                            action: 'download',
                            url: url,
                            quality: 'best' // Default quality
                        });
                    });
        controls.insertBefore(downloadBtn, controls.firstChild);
        console.log('[YouTube] Download button added successfully to player controls.');

    } catch (error) {
        console.error('[YouTube] Error adding regular video button:', error);
    }
}

function addYouTubeShortsButtons(rootElement = document) {
    try {
        if (!window.location.href.includes('youtube.com/shorts')) {
            return;
        }

        const buttonBars = rootElement.querySelectorAll('#actions #menu, #actions.ytd-reel-player-overlay-renderer');
        
        if (buttonBars.length > 0) {
            console.log(`[YouTube Shorts] Found ${buttonBars.length} button bar(s).`);
        }

        let addedCount = 0;
        buttonBars.forEach((buttonBar, index) => {

            if (buttonBar.querySelector('.yt-shorts-downloader-btn')) {
                // Button already exists, do nothing.
                return;
            }

            console.log(`[YouTube Shorts] Adding download button to button bar ${index + 1}`);

            const downloadBtn = document.createElement('button');
            downloadBtn.className = 'yt-shorts-downloader-btn';
            downloadBtn.innerHTML = `
                <svg viewBox="0 0 24 24" style="width: 36px; height: 36px; fill: white;">
                    <path d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z" />
                </svg>
                <span style="color: white; font-size: 12px;">Download</span>
            `;
            downloadBtn.style.cssText = `
                background: none !important;
                border: none !important;
                cursor: pointer;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 10px 5px;
            `;


            downloadBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();

                const url = extractCanonicalUrl(); // Use robust canonical URL
                console.log('[YouTube Shorts] Sending download request for URL:', url); // ADDED LOG

                chrome.storage.sync.get(['defaultQuality'], (data) => {
                    const quality = data.defaultQuality || 'best';
                    chrome.runtime.sendMessage({
                        action: 'download',
                        url: url,
                        quality: quality,
                        downloadPlaylist: false
                    });
                });
            });

            buttonBar.prepend(downloadBtn);


            console.log(`[YouTube Shorts] Button added successfully to button bar ${index + 1}`);
            addedCount++;
        });

        if (addedCount > 0) {
            console.log(`[YouTube Shorts] Added ${addedCount} download button(s)`);
        }
    } catch (error) {
        console.error('[YouTube Shorts] Error adding buttons:', error);
    }
}

function findFacebookVideosAndAddButtons(rootElement = document) {
    if (platform !== 'facebook') return;

    const url = window.location.href;
    const isReelPage = url.includes('/reel/');

    if (isReelPage) {
        addFacebookReelsButton(rootElement); // Call my robust Reels logic, passing rootElement
        return; // If it's a reel page, we handle it with addFacebookReelsButton and return.
    }
    
    // For generic videos (non-reel pages or if the reel logic didn't catch it perfectly)
    const videos = rootElement.querySelectorAll('video');
    console.log(`[Facebook] Found ${videos.length} video element(s) for generic video button adding.`);

    videos.forEach((video, index) => {
        addFacebookDownloadButtonToVideo(video, index);
    });

    // The logic below was moved from original to ensure generic video buttons are only added where appropriate.
    // If the page contains a video that is not a reel, add the generic download button.
    let addedCount = 0;
    videos.forEach((video, index) => {
        if (addFacebookDownloadButtonToVideo(video, index)) {
            addedCount++;
        }
    });

    if (addedCount > 0) {
        console.log(`[Facebook] Added ${addedCount} generic download button(s)`);
    }
}

// ==================== TIKTOK ====================
function addTikTokDownloadButton() {
    try {
        const actionBars = document.querySelectorAll('section[class*="SectionActionBarContainer"]');

        if (actionBars.length === 0) {
            return;
        }

        actionBars.forEach((actionBar) => {
            if (actionBar.querySelector('[data-downloader-btn="true"]')) {
                return; // Button already exists in this action bar, skip.
            }

            console.log('[TikTok] Found new action bar. Adding button.');

            const downloadBtnContainer = document.createElement('div');
            downloadBtnContainer.className = 'css-8cdu41-5e6d46e3--ButtonActionItem efpxn6t0 tiktok-downloader-btn';
            downloadBtnContainer.setAttribute('data-downloader-btn', 'true');
            downloadBtnContainer.setAttribute('role', 'button');
            downloadBtnContainer.setAttribute('tabindex', '0');
            downloadBtnContainer.setAttribute('aria-label', 'Download video');

            downloadBtnContainer.innerHTML = `
                <span data-e2e="download-icon" class="css-15zhuju-5e6d46e3--SpanIconWrapper efpxn6t1" style="color: rgba(255, 255, 255, 0.9);">
                    <svg viewBox="0 0 24 24" style="width: 24px; height: 24px; fill: currentColor;">
                        <path d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z" />
                    </svg>
                </span>
                <strong data-e2e="download-count" class="css-p4azz9-5e6d46e3--StrongText efpxn6t2">Download</strong>
            `;

            downloadBtnContainer.style.cssText = `
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin-top: 12px;
                cursor: pointer;
                padding: 0 10px;
                color: rgba(255, 255, 255, 0.9);
                width: auto;
                height: auto;
                min-height: 48px;
            `;

            downloadBtnContainer.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const videoUrl = window.location.href;
                console.log('[TikTok] Sending download request for URL:', videoUrl);
                chrome.storage.sync.get(['defaultQuality'], (data) => {
                    const quality = data.defaultQuality || 'best';
                    chrome.runtime.sendMessage({
                        action: 'download',
                        url: videoUrl,
                        quality: quality,
                        downloadPlaylist: false
                    });
                });
            });

            const shareButton = actionBar.querySelector('button[aria-label*="Share video"]');
            if (shareButton) {
                actionBar.insertBefore(downloadBtnContainer, shareButton);
            } else {
                actionBar.appendChild(downloadBtnContainer);
            }
            
            console.log('[TikTok] Download button added successfully.');
        });

    } catch (error) {
        console.error('[TikTok] Error adding download button:', error);
    }
}

// ==================== INSTAGRAM ====================
function addInstagramDownloadButton(rootElement = document) {
    console.log('[Instagram] Instagram download button functionality not yet implemented for rootElement:', rootElement);
}

// ==================== INITIALIZATION and LISTENERS ====================

let platform;

function initializePlatformSpecificLogic(rootElement = document) {
    platform = detectPlatform();
    if (platform === 'youtube') {
        if (window.location.href.includes('youtube.com/watch')) {
            addYouTubeDownloadButton(rootElement);
        } else if (window.location.href.includes('youtube.com/shorts')) {
            addYouTubeShortsButtons(rootElement);
        }
    } else if (platform === 'facebook') {
        findFacebookVideosAndAddButtons(rootElement);
    } else if (platform === 'tiktok') {
        addTikTokDownloadButton(); // No rootElement needed for the brute-force document scan
    } else if (platform === 'instagram') {
        addInstagramDownloadButton(rootElement);
    }
}

const observer = new MutationObserver(mutations => {
    const currentPlatform = detectPlatform();
    if (currentPlatform !== platform) {
        console.log('[Extension] Platform changed to:', currentPlatform, ' - Re-initializing all logic.');
        platform = currentPlatform;
        initializePlatformSpecificLogic();
        return;
    }

    if (platform === 'tiktok') {
        // For TikTok, always re-scan the whole document on any mutation due to its complex DOM replacement.
        initializePlatformSpecificLogic();
    } else {
        // For other platforms, we can be more efficient and check only new nodes.
        for (const mutation of mutations) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                for (const node of mutation.addedNodes) {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        initializePlatformSpecificLogic(node);
                    }
                }
            }
        }
    }
});

// Run the script after the page has fully loaded to avoid race conditions.
window.addEventListener('load', () => {
    console.log('[Extension] Page fully loaded. Starting main logic.');
    
    // Initial scan of the page
    initializePlatformSpecificLogic();

    // Start observing for future changes
    observer.observe(document.body, { childList: true, subtree: true });
    console.log('[Extension] MutationObserver active.');
});

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'captureUrl') {
        const url = extractCanonicalUrl(); 
        sendResponse({
            url: url,
            platform: platform
        });
        console.log('[Extension] Sent captured URL to background:', url);
        return true;
    }
});

console.log('[Extension] Content script initialized, waiting for page load event.');
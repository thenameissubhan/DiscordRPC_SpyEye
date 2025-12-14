// SpyEye_Extension/background.js - Service Worker for real-time tracking

const HISTORY_KEY = 'domainHistory';
const MAX_HISTORY = 50; 
const PYTHON_SERVER_URL = 'http://127.0.0.1:12345'; 

// VARIABLE to hold the ID in memory
let cachedInstanceId = null;

// Helper to get or create a persistent ID
function getInstanceId(callback) {
    if (cachedInstanceId) {
        callback(cachedInstanceId);
        return;
    }
    // Try to get from storage (persists across Service Worker sleeps)
    chrome.storage.local.get(['spyeye_instance_id'], (result) => {
        if (result.spyeye_instance_id) {
            cachedInstanceId = result.spyeye_instance_id;
            callback(cachedInstanceId);
        } else {
            // Create new ID and save it
            cachedInstanceId = self.crypto.randomUUID();
            chrome.storage.local.set({ 'spyeye_instance_id': cachedInstanceId }, () => {
                callback(cachedInstanceId);
            });
        }
    });
}

/**
 * Extracts the domain name from the URL, removes TLD, and capitalizes it.
 */
function extractDomainName(url) {
    if (!url) return 'N/A';
    
    // Handle system pages (New Tab, Settings, etc.)
    if (url.startsWith('chrome://') || url.startsWith('edge://') || url.startsWith('about:') || url.startsWith('file://')) {
        return 'N/A';
    }

    try {
        const urlObject = new URL(url);
        let hostname = urlObject.hostname;

        if (hostname.startsWith('www.')) {
            hostname = hostname.substring(4);
        }
        hostname = hostname.split(':')[0];
        
        const parts = hostname.split('.');
        
        if (parts.length > 1) {
            let domainWithoutTld = parts.slice(0, -1).join('.');
            if (domainWithoutTld.length > 0) {
                return domainWithoutTld.charAt(0).toUpperCase() + domainWithoutTld.slice(1);
            }
        }
        
        if (hostname.length > 0) {
             return hostname.charAt(0).toUpperCase() + hostname.slice(1);
        }

        return 'N/A';
    } catch (e) {
        return 'N/A';
    }
}

/**
 * Sends the current domain, incognito status, ID, URL AND FAVICON to the Python application.
 */
function sendToPython(domain, isIncognito, title, url, favIconUrl) {
    // SECURITY FIX: If Incognito, NEVER send the actual domain or URL to Python.
    const safeDomain = isIncognito ? "N/A" : domain;
    const safeUrl = isIncognito ? "N/A" : url;
    // Only send favicon if not incognito and it exists
    const safeFavicon = isIncognito ? "N/A" : (favIconUrl || "N/A");

    // Get the persistent ID before sending
    getInstanceId((id) => {
        fetch(PYTHON_SERVER_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                id: id,             // Uses the persistent ID now
                title: title,       // Current Tab Title (for matching)
                domain: safeDomain,
                incognito: isIncognito,
                url: safeUrl,       // Sends the URL for the button
                favicon: safeFavicon // Sends the dynamic favicon
            })
        }).catch(error => {
            // Silently fail if Python app isn't running
        });
    });
}

/**
 * Updates the history in Chrome's internal storage and sends data to Python.
 */
function updateHistory(tab) {
    if (!tab) return;

    // --- NOISE FILTER ---
    // If the tab is just "loading" and the URL hasn't changed (it's empty or same),
    // DO NOT send an update. This prevents sending "N/A" favicons during refresh.
    if (tab.status === 'loading' && !tab.url) return;

    const url = tab.url || '';
    const title = tab.title || '';
    const favIconUrl = tab.favIconUrl || ''; // Extract favicon
    const domain = extractDomainName(url);
    const isIncognito = tab.incognito; 
    
    // Send to Python immediately with the unique ID, URL, and Favicon
    sendToPython(domain, isIncognito, title, url, favIconUrl);

    // Don't save history if it's 'N/A' or Incognito (Privacy!)
    if (domain === 'N/A' || isIncognito) return; 

    chrome.storage.local.get([HISTORY_KEY], (result) => {
        let history = result[HISTORY_KEY] || [];
        
        const newLog = {
            domain: domain,
            url: url,
            timestamp: new Date().toISOString()
        };

        if (history.length > 0 && history[0].domain === domain) {
            return; 
        }

        history.unshift(newLog);
        if (history.length > MAX_HISTORY) {
            history = history.slice(0, MAX_HISTORY);
        }

        chrome.storage.local.set({ [HISTORY_KEY]: history });
    });
}

/**
 * Main listener function to handle tab activation and updates.
 */
function handleTabChange(tab) {
    if (tab) {
        updateHistory(tab);
    }
}

// Listener 1: Fired when the active tab changes (Swapping tabs)
chrome.tabs.onActivated.addListener((activeInfo) => {
    chrome.tabs.get(activeInfo.tabId, (tab) => {
        if (chrome.runtime.lastError) return;
        handleTabChange(tab);
        
        // FIX: Retry getting tab info shortly after switch. 
        // Chrome sometimes reports missing favicon immediately upon switch.
        setTimeout(() => {
            chrome.tabs.get(activeInfo.tabId, (retryTab) => {
                if (chrome.runtime.lastError) return;
                if (retryTab.active) handleTabChange(retryTab);
            });
        }, 500);
    });
});

// Listener 2: Fired when a tab is updated (Navigating within a tab, Title changes, Loading finishes)
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    // Listen for 'title', 'url', OR 'favIconUrl' changes specifically. 
    // This fixes the issue where the icon doesn't update until tab switch.
    
    // OPTIMIZATION: If status is loading, and we don't have a URL, ignore it.
    // This reduces the 'blink' effect where icon disappears.
    if (changeInfo.status === 'loading' && !changeInfo.url) {
        return;
    }

    if (tab.active && (changeInfo.url || changeInfo.status === 'complete' || changeInfo.title || changeInfo.favIconUrl)) {
        handleTabChange(tab);
    }

    // FIX: Some sites load favicons late via JS (SPAs) or after the 'complete' event.
    // We schedule delayed checks to ensure we catch the icon even if it loads late.
    if (tab.active && changeInfo.status === 'complete') {
        // First check after 1.5 seconds
        setTimeout(() => {
            chrome.tabs.get(tabId, (updatedTab) => {
                if (chrome.runtime.lastError) return;
                // Only send if it's still the active tab to prevent flickering/noise
                if (updatedTab.active) {
                    handleTabChange(updatedTab);
                }
            });
        }, 1500);

        // Second check after 3 seconds (for slower sites)
        setTimeout(() => {
            chrome.tabs.get(tabId, (updatedTab) => {
                if (chrome.runtime.lastError) return;
                if (updatedTab.active) {
                    handleTabChange(updatedTab);
                }
            });
        }, 3000);
    }
});

// Listener 3: Fired when the WINDOW gains focus
chrome.windows.onFocusChanged.addListener((windowId) => {
    if (windowId !== chrome.windows.WINDOW_ID_NONE) {
        // Immediate check
        chrome.tabs.query({ active: true, windowId: windowId }, (tabs) => {
            if (chrome.runtime.lastError) return;
            if (tabs && tabs.length > 0) {
                handleTabChange(tabs[0]);
            }
        });
        
        // Retry logic for robustness
        setTimeout(() => {
            chrome.tabs.query({ active: true, windowId: windowId }, (tabs) => {
                if (chrome.runtime.lastError) return;
                if (tabs && tabs.length > 0) {
                    handleTabChange(tabs[0]);
                }
            });
        }, 500);
    }
});
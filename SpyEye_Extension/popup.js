// Function to extract the domain name and capitalize it (Kept for display purposes)
function extractDomainName(url) {
    if (!url) {
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


document.addEventListener('DOMContentLoaded', function() {
    // Use chrome.tabs.query to get information about the active tab in the current window
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        // Check if any tabs were found
        if (tabs.length > 0) {
            const tab = tabs[0]; // Get the first (and only) active tab
            
            const currentDomain = extractDomainName(tab.url || '');

            // Populate the fields
            document.getElementById('favicon').src = tab.favIconUrl || 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAM1BMVEX////r6+uysrLq6urk5OTn5+fMzMzn5+fr6+uqqqrj4+Ps7OzLy8vAwMDf39/k5OTl5eXAwMCtIq/oAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAHklEQVR4nGJgYGDgZGJhZWEBjIAhDC8D+v8AAIwzAAz3M3+lAAAAAElRU5ErQmCC'; 
            document.getElementById('title').innerHTML = tab.title || 'N/A';
            document.getElementById('url').innerHTML = tab.url || 'N/A';
            document.getElementById('domain').innerHTML = currentDomain;
            document.getElementById('incognito').innerHTML = tab.incognito ? 'Yes' : 'No';
            document.getElementById('tab_num').innerHTML = (tab.index + 1).toString();
            document.getElementById('loading').innerHTML = tab.status || 'N/A';
        } else {
            // Handle case where no tab info is available
            document.getElementById('favicon').src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAM1BMVEX////r6+uysrLq6urk5OTn5+fMzMzn5+fr6+uqqqrj4+Ps7OzLy8vAwMDf39/k5OTl5eXAwMCtIq/oAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAHklEQVR4nGJgYGDgZGJhZWEBjIAhDC8D+v8AAIwzAAz3M3+lAAAAAElRU5ErQmCC';
            document.getElementById('title').innerHTML = 'No tab information available';
            document.getElementById('url').innerHTML = 'N/A';
            document.getElementById('domain').innerHTML = 'N/A'; 
            document.getElementById('incognito').innerHTML = 'N/A';
            document.getElementById('tab_num').innerHTML = 'N/A';
            document.getElementById('loading').innerHTML = 'N/A';
        }
    });
}, false);
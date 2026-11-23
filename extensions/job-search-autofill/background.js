// Extension Background Service Worker
// Acts as a CORS-free, Mixed-Content-free proxy between content scripts and the local Antigravity Bridge (:8765)

const BRIDGE_BASE = "http://127.0.0.1:8765";

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "bridge_request") {
    const targetUrl = `${BRIDGE_BASE}${request.path}`;
    const options = {
      method: request.method || "GET",
      headers: {
        "Content-Type": "application/json"
      }
    };

    if (request.data && (request.method === "POST" || request.method === "PUT")) {
      options.body = JSON.stringify(request.data);
    }

    fetch(targetUrl, options)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`Bridge returned HTTP ${response.status}`);
        }
        const json = await response.json();
        sendResponse({ success: true, data: json });
      })
      .catch((error) => {
        console.warn("[Background Proxy] Bridge request error:", error.message);
        sendResponse({ success: false, error: error.message });
      });

    return true; // Keep message channel open for asynchronous response
  }
});

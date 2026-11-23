document.addEventListener("DOMContentLoaded", async () => {
  const BRIDGE_URL = "http://127.0.0.1:8765";
  const badge = document.getElementById("bridge-badge");
  const bridgeLabel = document.getElementById("bridge-label");
  const status = document.getElementById("status-text");

  // Check bridge status
  async function checkBridge() {
    try {
      const resp = await fetch(`${BRIDGE_URL}/api/status`);
      if (resp.ok) {
        if (bridgeLabel) bridgeLabel.innerText = "Online (:8765)";
        if (badge) badge.classList.add("online");
      } else {
        throw new Error();
      }
    } catch (e) {
      if (bridgeLabel) bridgeLabel.innerText = "Offline";
      if (badge) badge.classList.remove("online");
    }
  }
  checkBridge();

  async function sendTabMessage(action, onSuccessText) {
    status.innerText = "Working...";
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (tab && tab.id) {
        chrome.tabs.sendMessage(tab.id, { action: action }, (response) => {
          if (chrome.runtime.lastError) {
            status.innerText = "Open an ATS form";
          } else {
            status.innerText = onSuccessText || "✓ Done";
            setTimeout(() => { window.close(); }, 1200);
          }
        });
      } else {
        status.innerText = "No active tab";
      }
    } catch (err) {
      status.innerText = "Action sent";
    }
  }

  // 1-Click Standard Fill
  document.getElementById("autofill-btn").addEventListener("click", () => {
    sendTabMessage("autofill", "✓ Standard Filled!");
  });

  // Auto M2: Export -> Analyze -> Inject
  const autoM2Btn = document.getElementById("auto-m2-btn");
  if (autoM2Btn) {
    autoM2Btn.addEventListener("click", () => {
      sendTabMessage("auto_m2", "✨ Auto M2 Completed!");
    });
  }

  // Method 2: Export
  document.getElementById("m2-export-btn").addEventListener("click", () => {
    sendTabMessage("method2_export", "📤 M2 Exported!");
  });

  // Method 2: Inject
  document.getElementById("m2-inject-btn").addEventListener("click", () => {
    sendTabMessage("method2_inject", "📥 M2 Injected!");
  });

  // Method 3: Copy
  document.getElementById("m3-copy-btn").addEventListener("click", () => {
    sendTabMessage("method3_copy", "📋 M3 Copied!");
  });

  // Method 3: Paste
  document.getElementById("m3-paste-btn").addEventListener("click", () => {
    sendTabMessage("method3_paste", "✨ M3 Injected!");
  });

  // Copy Profile Links
  const copyBtn = document.getElementById("copy-portfolio-btn");
  if (copyBtn) {
    copyBtn.addEventListener("click", () => {
      const links = "Full Name: Himanshu Dahiya\nEmail: dahiyahimanshu80@gmail.com\nPhone: +91 7015708154\nCollege: DCRUST Murthal, Sonipat (B.Tech ECE, 2024-2028)\nExperience: Software Engineer Intern @ Softech Media\nGitHub: https://github.com/Bored008\nLinkedIn: https://www.linkedin.com/in/himanshuakabored/\nPortfolio: https://himanshudahiya.vercel.app/";
      navigator.clipboard.writeText(links);
      copyBtn.innerText = "✓ Copied to Clipboard!";
      setTimeout(() => { copyBtn.innerText = "🔗 Copy Links & Profile"; }, 2000);
    });
  }

  // Open Queue Dashboard
  const queueLink = document.getElementById("open-queue-link");
  if (queueLink) {
    queueLink.addEventListener("click", (e) => {
      e.preventDefault();
      chrome.tabs.create({ url: "file:///C:/Project/ai-job-search/tools/application_queue_launcher.html" });
    });
  }
});

document.getElementById("autofill-btn").addEventListener("click", async () => {
  const status = document.getElementById("status-text");
  status.innerText = "Filling...";
  
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab && tab.id) {
    chrome.tabs.sendMessage(tab.id, { action: "autofill" }, (response) => {
      if (chrome.runtime.lastError) {
        status.innerText = "Please open an ATS form";
      } else {
        status.innerText = "✓ Form Filled!";
        setTimeout(() => { window.close(); }, 800);
      }
    });
  }
});

document.getElementById("copy-portfolio-btn").addEventListener("click", () => {
  const links = "GitHub: https://github.com/Bored008\nLinkedIn: https://www.linkedin.com/in/himanshuakabored/\nPortfolio: https://github.com/Bored008\nLive Demo: https://aihealth.Bored008.is-a.dev";
  navigator.clipboard.writeText(links);
  const btn = document.getElementById("copy-portfolio-btn");
  btn.innerText = "✓ Links Copied!";
  setTimeout(() => { btn.innerText = "🔗 Copy Portfolio Links"; }, 2000);
});

document.getElementById("copy-tracex-btn").addEventListener("click", () => {
  const text = "In TraceX (https://github.com/Bored008/tracex), I engineered an interactive microservices causal dependency graph and telemetry visualization engine. In distributed systems, rendering hundreds of service nodes with dynamic latency, error rate metrics, and anomaly propagation paths can easily lock the UI thread. To ensure a fluid 60fps experience, I implemented selective rendering & memoization across DAG node components, decoupled PageRank graph layout computations from the main thread, and implemented DOM virtualization for dense trace lists and log tables, maintaining a sub-15ms frame budget.";
  navigator.clipboard.writeText(text);
  const btn = document.getElementById("copy-tracex-btn");
  btn.innerText = "✓ Essay Copied!";
  setTimeout(() => { btn.innerText = "📋 Copy TraceX Initiative Essay"; }, 2000);
});

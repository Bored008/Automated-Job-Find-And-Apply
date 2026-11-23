// AI Job Search: Lifecycle Entry Point & Listener Registration
(function () {
  const root = (window.AIJobAutofill = window.AIJobAutofill || {});

  window.aiJobAutoM2 = root.autoM2Pipeline;
  window.aiJobAutofill = root.autofillATSForm;

  window.addEventListener("message", (event) => {
    if (event.data && event.data.type === "AI_JOB_AUTO_M2" && root.autoM2Pipeline) {
      root.autoM2Pipeline();
    }
  });

  document.addEventListener("AI_JOB_AUTO_M2", () => {
    if (root.autoM2Pipeline) root.autoM2Pipeline();
  });

  if (typeof chrome !== "undefined" && chrome.runtime && chrome.runtime.onMessage) {
    chrome.runtime.onMessage.addListener((req, sender, sendResponse) => {
      if (req.action === "autofill") {
        const c = root.autofillATSForm ? root.autofillATSForm() : 0;
        sendResponse({ success: true, count: c });
      } else if (req.action === "auto_m2") {
        if (root.autoM2Pipeline) {
          root.autoM2Pipeline().then((r) => sendResponse({ success: true, result: r }));
          return true;
        }
      } else if (req.action === "method2_export") {
        if (root.exportPendingToProject) {
          root.exportPendingToProject().then(() => sendResponse({ success: true }));
          return true;
        }
      } else if (req.action === "method2_inject") {
        if (root.injectReadyAnswers) {
          root.injectReadyAnswers().then(() => sendResponse({ success: true }));
          return true;
        }
      } else if (req.action === "method3_copy") {
        if (root.copyFormForChat) root.copyFormForChat();
        sendResponse({ success: true });
      } else if (req.action === "method3_paste") {
        if (root.pasteAndInjectAnswers) root.pasteAndInjectAnswers();
        sendResponse({ success: true });
      }
    });
  }

  window.addEventListener("load", () => {
    setTimeout(() => {
      if (root.injectFloatingHUD) root.injectFloatingHUD();
    }, 1000);
  });
})();

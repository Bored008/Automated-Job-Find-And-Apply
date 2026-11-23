// AI Job Search: Local Bridge Client & Automated M2 Pipeline
(function () {
  const root = (window.AIJobAutofill = window.AIJobAutofill || {});
  const { BRIDGE_URL, PROFILE, setNativeValue, triggerComboboxSelect, detectJobContext, autofillATSForm, autofillOptionGroups } = root;

  function callBridge(path, method = "GET", data = null) {
    return new Promise((resolve, reject) => {
      if (typeof chrome !== "undefined" && chrome.runtime && chrome.runtime.sendMessage) {
        chrome.runtime.sendMessage(
          { action: "bridge_request", path: path, method: method, data: data },
          (response) => {
            if (chrome.runtime.lastError || !response || !response.success) {
              directFetch(path, method, data).then(resolve).catch(reject);
            } else {
              resolve(response.data);
            }
          }
        );
      } else {
        directFetch(path, method, data).then(resolve).catch(reject);
      }
    });
  }

  async function directFetch(path, method = "GET", data = null) {
    const url = `${BRIDGE_URL}${path}`;
    const opts = {
      method: method,
      headers: { "Content-Type": "application/json" }
    };
    if (data && (method === "POST" || method === "PUT")) {
      opts.body = JSON.stringify(data);
    }
    const resp = await fetch(url, opts);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    return await resp.json();
  }

  async function checkBridgeHealth() {
    try {
      const res = await callBridge("/api/status", "GET");
      const isOnline = res && res.status === "online";
      const badge = document.getElementById("ai-job-bridge-badge");
      if (badge) {
        badge.innerText = isOnline ? "Online (:8765)" : "Offline";
        badge.style.color = isOnline ? "#10b981" : "#94a3b8";
      }
      return isOnline;
    } catch (e) {
      const badge = document.getElementById("ai-job-bridge-badge");
      if (badge) {
        badge.innerText = "Offline";
        badge.style.color = "#94a3b8";
      }
      return false;
    }
  }

  async function exportPendingToProject() {
    const unfilled = root.getUnfilledFields ? root.getUnfilledFields() : [];
    if (unfilled.length === 0) {
      if (root.showToast) root.showToast("No screening fields found on page.");
      return;
    }

    const { company, roleTitle, url } = detectJobContext();
    const payload = {
      url: url,
      company: company,
      role_title: roleTitle,
      fields: unfilled.map(f => ({ id: f.id, label: f.label, placeholder: f.placeholder, type: f.type }))
    };

    try {
      const data = await callBridge("/api/export-pending", "POST", payload);
      if (data && data.success) {
        if (root.showToast) root.showToast(`Exported ${unfilled.length} fields to pending_form.json.`);
      }
    } catch (e) {
      if (root.showToast) root.showToast("Bridge offline: start python tools/bridge/server.py");
    }
  }

  async function injectReadyAnswers() {
    try {
      const data = await callBridge("/api/ready-answers", "GET");
      if (!data || !data.answers || Object.keys(data.answers).length === 0) {
        if (root.showToast) root.showToast("No ready answers found in ready_answers.json yet.");
        return;
      }

      const candidateFields = Array.from(document.querySelectorAll("input:not([type='hidden']):not([type='checkbox']):not([type='radio']):not([type='file']):not([type='submit']):not([type='button']), textarea"));
      let count = 0;

      candidateFields.forEach(f => {
        const bridgeId = f.getAttribute("data-bridge-id") || "";
        const label = root.extractFieldLabel ? root.extractFieldLabel(f).toLowerCase().trim() : "";
        const cleanLabel = label.replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
        const id = (f.id || "").toLowerCase();
        const name = (f.name || "").toLowerCase();

        let ans = (bridgeId && data.answers[bridgeId]) || (id && data.answers[id]);
        if (!ans && name && !name.startsWith("text_") && data.answers[name]) {
          ans = data.answers[name];
        }
        if (!ans && cleanLabel) {
          for (const [k, v] of Object.entries(data.answers)) {
            const keyClean = k.toLowerCase().replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
            if (keyClean && (cleanLabel.includes(keyClean) || keyClean.includes(cleanLabel))) {
              ans = v;
              break;
            }
          }
        }

        if (ans) {
          setNativeValue(f, ans);
          f.style.outline = "2px solid #8b5cf6";
          f.style.backgroundColor = "rgba(139, 92, 246, 0.08)";
          count++;
          if (label.includes("country") || label.includes("location")) {
            triggerComboboxSelect(f, ans);
          }
        }
      });

      autofillOptionGroups();
      if (root.updateHUDCount) root.updateHUDCount();
      if (root.showToast) root.showToast(`Injected ${count} answers from ready_answers.json.`);
    } catch (e) {
      if (root.showToast) root.showToast("Bridge offline: start python tools/bridge/server.py");
    }
  }

  async function autoM2Pipeline() {
    if (root.showToast) root.showToast("Step 1/3: Populating standard profile fields...");
    const standardCount = autofillATSForm();

    const unfilled = root.getUnfilledFields ? root.getUnfilledFields() : [];
    if (unfilled.length === 0) {
      const optCount = autofillOptionGroups();
      if (root.updateHUDCount) root.updateHUDCount();
      if (root.showToast) root.showToast(`Form complete: ${standardCount} fields and ${optCount} options.`);
      return { success: true, standardCount, optCount, total: standardCount + optCount };
    }

    if (root.showToast) root.showToast(`Step 2/3: Analyzing ${unfilled.length} screening questions...`);
    const { company, roleTitle, url } = detectJobContext();
    const payload = {
      url: url,
      company: company,
      role_title: roleTitle,
      auto_synthesize: true,
      fields: unfilled.map(f => ({ id: f.id, label: f.label, placeholder: f.placeholder, type: f.type }))
    };

    try {
      const data = await callBridge("/api/export-pending", "POST", payload);
      let answers = (data && data.answers) || {};
      if (!answers || Object.keys(answers).length === 0) {
        const readyData = await callBridge("/api/ready-answers", "GET");
        answers = (readyData && readyData.answers) || {};
      }

      let injectedCount = 0;
      unfilled.forEach(f => {
        let ans = answers[f.id];
        if (!ans) {
          const cleanLabel = f.label.toLowerCase().replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
          for (const [k, v] of Object.entries(answers)) {
            const keyClean = k.toLowerCase().replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
            if (keyClean && (cleanLabel.includes(keyClean) || keyClean.includes(cleanLabel))) {
              ans = v;
              break;
            }
          }
        }

        if (ans) {
          setNativeValue(f.element, ans);
          f.element.style.outline = "2px solid #10b981";
          f.element.style.backgroundColor = "rgba(16, 185, 129, 0.08)";
          injectedCount++;
          if (f.label.toLowerCase().includes("country") || f.label.toLowerCase().includes("location")) {
            triggerComboboxSelect(f.element, ans);
          }
        }
      });

      const optCount = autofillOptionGroups();
      if (root.updateHUDCount) root.updateHUDCount();
      const total = standardCount + injectedCount + optCount;
      if (root.showToast) root.showToast(`Success: ${total} fields and options populated.`);
      return { success: true, standardCount, injectedCount, optCount, total };
    } catch (e) {
      console.warn("[AI Job Autofill] Bridge request error:", e);
      if (root.showToast) root.showToast("Bridge connection failed. Check server status.");
    }
  }

  root.callBridge = callBridge;
  root.checkBridgeHealth = checkBridgeHealth;
  root.exportPendingToProject = exportPendingToProject;
  root.injectReadyAnswers = injectReadyAnswers;
  root.autoM2Pipeline = autoM2Pipeline;
})();

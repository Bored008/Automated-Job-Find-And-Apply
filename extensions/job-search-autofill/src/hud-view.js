// AI Job Search: Floating HUD View & Candidate Snippets Drawer
(function () {
  const root = (window.AIJobAutofill = window.AIJobAutofill || {});
  const { PROFILE, SNIPPETS, setNativeValue, triggerComboboxSelect, extractFieldLabel, detectJobContext } = root;

  function getUnfilledFields() {
    const candidateFields = Array.from(document.querySelectorAll("input:not([type='hidden']):not([type='checkbox']):not([type='radio']):not([type='file']):not([type='submit']):not([type='button']), textarea"));
    
    return candidateFields.filter((f) => {
      const label = extractFieldLabel(f).toLowerCase();
      const placeholder = (f.placeholder || "").toLowerCase();
      const combined = `${f.id} ${f.name} ${placeholder} ${label}`.toLowerCase();

      if (combined.includes("start typing") || combined.includes("residing") || combined.includes("location") || combined.includes("country")) {
        if (!f.value || f.value.length > 30 || f.value.includes("experience")) {
          setNativeValue(f, PROFILE.country);
          triggerComboboxSelect(f, PROFILE.country);
        }
        return false;
      }
      if (combined.includes("email") || combined.includes("phone") || combined.includes("first name") || combined.includes("last name") || (combined.includes("name") && !combined.includes("company"))) {
        return false;
      }
      if (combined.includes("linkedin") || combined.includes("github") || combined.includes("portfolio") || combined.includes("website")) {
        return false;
      }
      if (f.value && f.value.trim().length > 0 && !f.value.includes("Softech") && !f.value.includes("experience developing web applications")) {
        return false;
      }

      const rect = f.getBoundingClientRect();
      return rect.width > 0 && rect.height > 0 && window.getComputedStyle(f).display !== "none";
    }).map((field, index) => {
      let bridgeId = field.getAttribute("data-bridge-id");
      if (!bridgeId) {
        const rawName = (field.id || field.name || "input").replace(/[^a-zA-Z0-9_-]/g, "");
        bridgeId = `field_${index}_${rawName}`;
        field.setAttribute("data-bridge-id", bridgeId);
      }

      let labelText = extractFieldLabel(field).replace(/[\n\r]+/g, " ").replace(/\s{2,}/g, " ").trim();
      return {
        element: field,
        id: bridgeId,
        label: labelText,
        placeholder: field.placeholder || "",
        type: field.tagName.toLowerCase() === "textarea" ? "textarea" : (field.type || "text")
      };
    });
  }

  function getUnfilledCount() {
    return getUnfilledFields().length;
  }

  function updateHUDCount() {
    const count = getUnfilledCount();
    const countBadge = document.getElementById("ai-job-unfilled-count");
    if (countBadge) {
      countBadge.innerText = count > 0 ? `${count} left` : "Done";
      countBadge.style.color = count > 0 ? "#fbbf24" : "#34d399";
    }
    const pillCount = document.getElementById("ai-job-pill-count");
    if (pillCount) {
      pillCount.innerText = count > 0 ? `${count} left` : "Done";
      pillCount.style.color = count > 0 ? "#fbbf24" : "#34d399";
    }
  }

  function injectFloatingHUD() {
    if (document.getElementById("ai-job-autofill-hud")) return;

    if (!document.getElementById("ai-job-hud-styles")) {
      const styleEl = document.createElement("style");
      styleEl.id = "ai-job-hud-styles";
      styleEl.textContent = `
        .ai-hud-btn-hover:hover { transform: translateY(-1px); opacity: 0.95; }
        .ai-hud-btn-hover:active { transform: translateY(0); }
      `;
      document.head.appendChild(styleEl);
    }

    const hud = document.createElement("div");
    hud.id = "ai-job-autofill-hud";
    hud.style.cssText = `
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 999999;
      background: rgba(9, 13, 22, 0.94);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 14px;
      padding: 12px 14px;
      box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.7);
      display: flex;
      flex-direction: column;
      gap: 10px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #f8fafc;
      min-width: 300px;
      transition: all 0.25s ease;
    `;

    hud.innerHTML = `
      <div id="ai-job-hud-minimized" style="display:none; align-items:center; justify-content:space-between; gap:10px; cursor:pointer;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-weight:700; font-size:12px; color:#ffffff;">AutoFill Pro</span>
          <span id="ai-job-pill-count" style="font-size:10.5px; font-weight:700; color:#fbbf24;">${getUnfilledCount()} left</span>
        </div>
        <span style="font-size:11px; color:#38bdf8; font-weight:600;">Expand</span>
      </div>

      <div id="ai-job-hud-expanded" style="display:flex; flex-direction:column; gap:9px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div style="font-weight: 700; font-size: 13px; display: flex; align-items: center; gap: 7px;">
            <span style="color:#ffffff; font-weight:800;">AutoFill Pro</span>
            <span id="ai-job-unfilled-count" style="font-size:10px; background:rgba(245, 158, 11, 0.18); border:1px solid rgba(245, 158, 11, 0.35); color:#fbbf24; font-weight:700; padding:1px 7px; border-radius:999px;">${getUnfilledCount()} left</span>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <span id="ai-job-bridge-badge" style="font-size:10px; color:#94a3b8; font-weight:600;">Checking...</span>
            <button id="ai-job-min-hud" title="Minimize" style="background:rgba(255,255,255,0.06); color:#94a3b8; border:1px solid rgba(255,255,255,0.08); border-radius:5px; width:20px; height:20px; font-size:12px; cursor:pointer;">-</button>
            <button id="ai-job-close-hud" title="Close" style="background:transparent; color:#64748b; border:none; font-size:16px; cursor:pointer;">&times;</button>
          </div>
        </div>

        <div style="display:flex; gap:6px;">
          <button id="ai-job-autofill-btn" class="ai-hud-btn-hover" style="flex:1; background:#0284c7; color:white; border:none; padding:8px; border-radius:8px; font-weight:700; font-size:11px; cursor:pointer;">Standard Fill</button>
          <button id="ai-job-auto-m2-btn" class="ai-hud-btn-hover" style="flex:1.25; background:#8b5cf6; color:white; border:none; padding:8px; border-radius:8px; font-weight:700; font-size:11px; cursor:pointer;">Auto M2</button>
        </div>

        <div style="display:flex; gap:4px;">
          <button id="ai-job-m2-export-btn" class="ai-hud-btn-hover" style="flex:1; background:rgba(30,41,59,0.6); color:#cbd5e1; border:1px solid rgba(255,255,255,0.08); padding:6px 4px; border-radius:7px; font-size:10px; cursor:pointer;">Export</button>
          <button id="ai-job-m2-inject-btn" class="ai-hud-btn-hover" style="flex:1; background:rgba(30,41,59,0.6); color:#cbd5e1; border:1px solid rgba(255,255,255,0.08); padding:6px 4px; border-radius:7px; font-size:10px; cursor:pointer;">Inject</button>
          <button id="ai-job-m3-copy-btn" class="ai-hud-btn-hover" style="flex:1; background:rgba(30,41,59,0.6); color:#cbd5e1; border:1px solid rgba(255,255,255,0.08); padding:6px 4px; border-radius:7px; font-size:10px; cursor:pointer;">Copy</button>
          <button id="ai-job-snippets-btn" class="ai-hud-btn-hover" style="background:rgba(30,41,59,0.6); color:#38bdf8; border:1px solid rgba(56,189,248,0.25); padding:6px 8px; border-radius:7px; font-size:11px; cursor:pointer;">Snippets</button>
        </div>
      </div>
    `;

    document.body.appendChild(hud);

    const minView = document.getElementById("ai-job-hud-minimized");
    const expView = document.getElementById("ai-job-hud-expanded");

    document.getElementById("ai-job-min-hud").onclick = () => {
      expView.style.display = "none";
      minView.style.display = "flex";
      hud.style.minWidth = "auto";
      hud.style.padding = "8px 12px";
      hud.style.borderRadius = "999px";
    };

    minView.onclick = () => {
      minView.style.display = "none";
      expView.style.display = "flex";
      hud.style.minWidth = "300px";
      hud.style.padding = "12px 14px";
      hud.style.borderRadius = "14px";
    };

    document.getElementById("ai-job-autofill-btn").onclick = () => root.autofillATSForm();
    document.getElementById("ai-job-auto-m2-btn").onclick = () => root.autoM2Pipeline();
    document.getElementById("ai-job-m2-export-btn").onclick = () => root.exportPendingToProject();
    document.getElementById("ai-job-m2-inject-btn").onclick = () => root.injectReadyAnswers();
    document.getElementById("ai-job-m3-copy-btn").onclick = () => copyFormForChat();
    document.getElementById("ai-job-snippets-btn").onclick = () => toggleSnippetsDrawer();
    document.getElementById("ai-job-close-hud").onclick = () => hud.remove();

    if (root.checkBridgeHealth) root.checkBridgeHealth();
    setInterval(updateHUDCount, 3000);
    setInterval(root.checkBridgeHealth, 10000);
  }

  function toggleSnippetsDrawer() {
    let drawer = document.getElementById("ai-job-snippets-drawer");
    if (drawer) {
      drawer.style.display = drawer.style.display === "none" ? "block" : "none";
      return;
    }

    drawer = document.createElement("div");
    drawer.id = "ai-job-snippets-drawer";
    drawer.style.cssText = `
      position: fixed;
      bottom: 120px;
      right: 24px;
      width: 380px;
      max-height: 500px;
      overflow-y: auto;
      z-index: 999999;
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #f8fafc;
    `;

    drawer.innerHTML = `
      <div style="font-weight: 700; font-size: 14px; margin-bottom: 12px; display:flex; justify-content:space-between; align-items:center;">
        <span>Verified Screening Snippets</span>
        <span id="ai-close-snippets" style="cursor:pointer; color:#94a3b8; font-size:18px;">&times;</span>
      </div>
      <div style="display:flex; flex-direction:column; gap:10px;">
        <div style="background:#1e293b; padding:10px; border-radius:8px; border:1px solid #334155;">
          <div style="font-size:12px; font-weight:600; color:#10b981; margin-bottom:4px;">AI Agent Pipeline</div>
          <div style="font-size:11px; color:#cbd5e1; max-height:60px; overflow:hidden;">${SNIPPETS.aiAgentBuilt.slice(0, 140)}...</div>
          <button class="ai-copy-snippet" data-key="aiAgentBuilt" style="margin-top:6px; background:#059669; color:white; border:none; padding:4px 8px; border-radius:4px; font-size:11px; cursor:pointer;">Copy</button>
        </div>
        <div style="background:#1e293b; padding:10px; border-radius:8px; border:1px solid #334155;">
          <div style="font-size:12px; font-weight:600; color:#10b981; margin-bottom:4px;">Hardest Problem (Token Optimization)</div>
          <div style="font-size:11px; color:#cbd5e1; max-height:60px; overflow:hidden;">${SNIPPETS.aiAgentHardestProblem.slice(0, 140)}...</div>
          <button class="ai-copy-snippet" data-key="aiAgentHardestProblem" style="margin-top:6px; background:#059669; color:white; border:none; padding:4px 8px; border-radius:4px; font-size:11px; cursor:pointer;">Copy</button>
        </div>
        <div style="background:#1e293b; padding:10px; border-radius:8px; border:1px solid #334155;">
          <div style="font-size:12px; font-weight:600; color:#38bdf8; margin-bottom:4px;">TraceX Observability</div>
          <div style="font-size:11px; color:#cbd5e1; max-height:60px; overflow:hidden;">${SNIPPETS.traceX.slice(0, 140)}...</div>
          <button class="ai-copy-snippet" data-key="traceX" style="margin-top:6px; background:#2563eb; color:white; border:none; padding:4px 8px; border-radius:4px; font-size:11px; cursor:pointer;">Copy</button>
        </div>
      </div>
    `;

    document.body.appendChild(drawer);
    document.getElementById("ai-close-snippets").onclick = () => { drawer.style.display = "none"; };
    drawer.querySelectorAll(".ai-copy-snippet").forEach((btn) => {
      btn.onclick = (e) => {
        const key = e.target.getAttribute("data-key");
        navigator.clipboard.writeText(SNIPPETS[key]);
        e.target.innerText = "Copied";
        setTimeout(() => { e.target.innerText = "Copy"; }, 2000);
      };
    });
  }

  function copyFormForChat() {
    const unfilled = getUnfilledFields();
    if (unfilled.length === 0) {
      if (root.showToast) root.showToast("All fields are already populated.");
      return;
    }
    const { company, roleTitle, url } = detectJobContext();
    let md = `### Job Application Screening Questions\n`;
    md += `Company: ${company || "Not detected"}\nRole: ${roleTitle || "Not detected"}\nURL: ${url}\n\n`;
    md += `Provide JSON answers grounded in Himanshu Dahiya's profile:\n\`\`\`json\n{\n`;
    unfilled.forEach((f, idx) => {
      const comma = idx < unfilled.length - 1 ? "," : "";
      md += `  "${f.id}": "..."${comma} // Q: ${f.label}\n`;
    });
    md += `}\n\`\`\`\n`;
    navigator.clipboard.writeText(md).then(() => {
      if (root.showToast) root.showToast(`Copied ${unfilled.length} questions to clipboard.`);
    });
  }

  function pasteAndInjectAnswers() {
    const jsonStr = prompt("Paste the JSON answers below:");
    if (!jsonStr) return;
    try {
      const cleaned = jsonStr.replace(/```json/g, "").replace(/```/g, "").trim();
      const parsed = JSON.parse(cleaned);
      const unfilled = getUnfilledFields();
      let injected = 0;
      unfilled.forEach(f => {
        const ans = parsed[f.id];
        if (ans) {
          setNativeValue(f.element, ans);
          f.element.style.outline = "2px solid #ec4899";
          injected++;
        }
      });
      updateHUDCount();
      if (root.showToast) root.showToast(`Injected ${injected} answers from clipboard.`);
    } catch (e) {
      alert("Invalid JSON format.");
    }
  }

  function showToast(msg) {
    const toast = document.createElement("div");
    toast.innerText = msg;
    toast.style.cssText = `
      position: fixed;
      top: 24px;
      right: 24px;
      z-index: 1000000;
      background: rgba(9, 13, 22, 0.94);
      color: #ffffff;
      border-left: 4px solid #38bdf8;
      font-weight: 600;
      font-size: 12.5px;
      padding: 10px 16px;
      border-radius: 8px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    `;
    document.body.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transition = "opacity 0.3s ease";
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  root.getUnfilledFields = getUnfilledFields;
  root.getUnfilledCount = getUnfilledCount;
  root.updateHUDCount = updateHUDCount;
  root.injectFloatingHUD = injectFloatingHUD;
  root.toggleSnippetsDrawer = toggleSnippetsDrawer;
  root.copyFormForChat = copyFormForChat;
  root.pasteAndInjectAnswers = pasteAndInjectAnswers;
  root.showToast = showToast;
})();

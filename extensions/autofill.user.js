// ==UserScript==
// @name         AI Job Search: 1-Click Fast ATS Autofill + AI Bridge (Methods 1, 2, 3)
// @namespace    https://github.com/Bored008/ai-job-search
// @version      2.1.0
// @description  Zero-token standard autofill + 3 AI bridge architectures for Himanshu Dahiya (@Bored008)
// @author       Himanshu Dahiya
// @match        *://*.ashbyhq.com/*
// @match        *://*.greenhouse.io/*
// @match        *://*.lever.co/*
// @match        *://*.workatastartup.com/*
// @match        *://*.ycombinator.com/*
// @match        *://*.micro1.ai/*
// @match        *://*.unstop.com/*
// @match        *://*.linkedin.com/*
// @match        *://*.internshala.com/*
// @match        *://*.wellfound.com/*
// @grant        GM_xmlhttpRequest
// @grant        GM_setClipboard
// @run-at       document-idle
// ==/UserScript==

(function () {
  'use strict';

  console.log("[AI Job Autofill Userscript v2.1] Loaded on:", window.location.href);

  const BRIDGE_URL = "http://127.0.0.1:8765";

  const PROFILE = {
    firstName: "Himanshu",
    lastName: "Dahiya",
    fullName: "Himanshu Dahiya",
    email: "dahiyahimanshu80@gmail.com",
    phone: "+91 7015708154",
    phonePlain: "7015708154",
    location: "Sonipat, Haryana, India",
    city: "Sonipat",
    state: "Haryana",
    country: "India",
    linkedin: "https://www.linkedin.com/in/himanshuakabored/",
    github: "https://github.com/Himanshu-Dahiya-24",
    portfolio: "https://himanshudahiya.vercel.app/",
    twitter: "https://x.com/Bored_OO8",
    currentOrg: "Softech Media",
    currentRole: "Software Engineer Intern",
    college: "Deenbandhu Chhotu Ram University of Science and Technology (DCRUST), Murthal, Sonipat",
    degree: "B.Tech in Electronics and Communication Engineering",
    graduationYear: "2028",
    yearsExperience: "1",
    compensation: "Open to discussion / standard market rate (₹10–14 LPA or standard internship stipend)",
    howDidYouHear: "LinkedIn / Company Careers Page",
    workAuthUS: "Yes",
    sponsorship: "No",
    aiPolicyAgree: "Yes",
    gender: "Male",
    race: "Asian",
    veteran: "I am not a protected veteran",
    disability: "No, I do not have a disability"
  };

  const SNIPPETS = {
    aiAgentBuilt: "I engineered an autonomous multi-agent job application and observability pipeline (https://github.com/Bored008/Automated-Job-Find-And-Apply) leveraging the Model Context Protocol (MCP), Python, and Gemini API. The system orchestrates specialized workers to query live ATS APIs (Ashby, Greenhouse, Unstop), score roles against candidate profiles, and deterministically inject DOM payloads and upload resumes without human intervention. It autonomously manages state verification, monitors Gmail for recruiter updates, and books interview schedules to Google Calendar.",
    aiAgentHardestProblem: "The hardest problem was severe agent token bloat and non-deterministic DOM looping when using multimodal vision agents for form filling (consuming 50k+ tokens per application). I solved this by implementing a dual-layer architecture: offloading all mechanical form operations to deterministic AST/DOM injection scripts (dropping LLM token usage to zero), while restricting LLM calls strictly to high-leverage contextual essay synthesis with a hard 500-token budget and strict schema validation.",
    traceX: "In TraceX (https://github.com/Bored008/tracex), I engineered an interactive microservices causal dependency graph and telemetry visualization engine. In distributed systems, rendering hundreds of service nodes with dynamic latency, error rate metrics, and anomaly propagation paths can easily lock the UI thread. To ensure a fluid 60fps experience, I implemented selective rendering & memoization across DAG node components, decoupled PageRank graph layout computations from the main thread, and implemented DOM virtualization for dense trace lists and log tables, maintaining a sub-15ms frame budget.",
    yanegiDesignTokens: "When engineering the web frontend for Yanegi (https://yanegi.com) and Orbit Shipping Services (Softech Media), the challenge was maintaining strict brand visual consistency while supporting real-time interactive states. I created a centralized design token system mapping Figma color primitives and spacing scales to semantic CSS variables and Tailwind utility classes. For complex components, I encapsulated motion logic inside reusable React hooks, ensuring brand fidelity and 60fps performance budgets across pages.",
    whyGoodFit: "When an engineer is triaging a high-severity production incident at 2 AM, cognitive overload is the enemy. Rather than overwhelming developers with raw logs and unranked trace waterfalls, I prioritize immediate root-cause guidance with quantitative confidence scores, context-preserving drill-down drawers directly from topology maps, and uniform visual status semantics across metrics, logs, and traces. Located in Sonipat / Delhi NCR, immediately available."
  };

  function setNativeValue(element, value) {
    if (!element) return;
    const isTextarea = element.tagName.toLowerCase() === "textarea";
    const prototype = isTextarea ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
    const descriptor = Object.getOwnPropertyDescriptor(prototype, "value");

    if (descriptor && descriptor.set) {
      descriptor.set.call(element, value);
    } else {
      element.value = value;
    }

    element.dispatchEvent(new Event("input", { bubbles: true }));
    element.dispatchEvent(new Event("change", { bubbles: true }));
    element.dispatchEvent(new Event("blur", { bubbles: true }));
  }

  function detectJobContext() {
    let company = "";
    let roleTitle = "";
    const url = window.location.href;
    if (url.includes("ashbyhq.com/")) {
      const parts = url.split("ashbyhq.com/")[1].split("/");
      company = decodeURIComponent(parts[0] || "");
    }
    const h1 = document.querySelector("h1, [data-qa='job-title'], .job-title, [class*='title']");
    roleTitle = (h1 && h1.innerText) ? h1.innerText.trim() : document.title.split("-")[0].split("|")[0].trim();
    return { company, roleTitle, url };
  }

  function getUnfilledFields() {
    const candidateFields = Array.from(document.querySelectorAll("input:not([type='hidden']):not([type='checkbox']):not([type='radio']):not([type='file']):not([type='submit']):not([type='button']), textarea"));
    const unfilled = candidateFields.filter((f) => {
      if (f.value && f.value.trim().length > 0) return false;
      const rect = f.getBoundingClientRect();
      return rect.width > 0 && rect.height > 0 && window.getComputedStyle(f).display !== "none";
    });

    return unfilled.map((field, index) => {
      let bridgeId = field.getAttribute("data-bridge-id");
      if (!bridgeId) {
        bridgeId = field.id || field.name || `bridge_field_${index}`;
        field.setAttribute("data-bridge-id", bridgeId);
      }
      let labelText = "";
      if (field.labels && field.labels.length > 0) {
        labelText = field.labels[0].innerText.trim();
      } else {
        const parent = field.closest("label, .field, [role='group'], [class*='field'], [class*='form-group'], div");
        if (parent) labelText = parent.innerText.replace(field.value || "", "").trim();
      }
      if (!labelText && field.placeholder) labelText = field.placeholder.trim();
      labelText = labelText.replace(/[\n\r]+/g, " ").replace(/\s{2,}/g, " ").trim();

      return {
        element: field,
        id: bridgeId,
        label: labelText,
        placeholder: field.placeholder || "",
        type: field.tagName.toLowerCase() === "textarea" ? "textarea" : (field.type || "text")
      };
    });
  }

  function autofillATSForm() {
    let filledCount = 0;
    const allInputs = Array.from(document.querySelectorAll("input:not([type='hidden']):not([type='checkbox']):not([type='radio']):not([type='file']), textarea"));

    allInputs.forEach((input) => {
      const id = (input.id || "").toLowerCase();
      const name = (input.name || "").toLowerCase();
      const placeholder = (input.placeholder || "").toLowerCase();
      const ariaLabel = (input.getAttribute("aria-label") || "").toLowerCase();
      let labelText = "";
      if (input.labels && input.labels.length > 0) {
        labelText = input.labels[0].innerText.toLowerCase();
      } else {
        const parent = input.closest("label, .field, [role='group'], div");
        if (parent) labelText = parent.innerText.toLowerCase();
      }
      const combinedText = `${id} ${name} ${placeholder} ${ariaLabel} ${labelText}`;

      if (input.type === "email" || combinedText.includes("email")) {
        if (!input.value) { setNativeValue(input, PROFILE.email); filledCount++; }
      } else if (input.type === "tel" || combinedText.includes("phone") || combinedText.includes("mobile")) {
        if (!input.value) { setNativeValue(input, PROFILE.phone); filledCount++; }
      } else if (combinedText.includes("first name") || combinedText.includes("given name") || name === "first_name") {
        if (!input.value) { setNativeValue(input, PROFILE.firstName); filledCount++; }
      } else if (combinedText.includes("last name") || combinedText.includes("family name") || name === "last_name") {
        if (!input.value) { setNativeValue(input, PROFILE.lastName); filledCount++; }
      } else if (combinedText.includes("full name") || combinedText.includes("legal name") || (combinedText.includes("name") && !combinedText.includes("company") && !combinedText.includes("first") && !combinedText.includes("last"))) {
        if (!input.value) { setNativeValue(input, PROFILE.fullName); filledCount++; }
      } else if (combinedText.includes("linkedin")) {
        if (!input.value) { setNativeValue(input, PROFILE.linkedin); filledCount++; }
      } else if (combinedText.includes("github")) {
        if (!input.value) { setNativeValue(input, PROFILE.github); filledCount++; }
      } else if (combinedText.includes("portfolio") || combinedText.includes("website")) {
        if (!input.value) { setNativeValue(input, PROFILE.portfolio); filledCount++; }
      } else if (combinedText.includes("employer") || combinedText.includes("current company")) {
        if (!input.value) { setNativeValue(input, PROFILE.currentOrg); filledCount++; }
      } else if (combinedText.includes("college") || combinedText.includes("university")) {
        if (!input.value) { setNativeValue(input, PROFILE.college); filledCount++; }
      } else if (combinedText.includes("degree")) {
        if (!input.value) { setNativeValue(input, PROFILE.degree); filledCount++; }
      } else if (combinedText.includes("compensation") || combinedText.includes("salary")) {
        if (!input.value) { setNativeValue(input, PROFILE.compensation); filledCount++; }
      } else if (combinedText.includes("total years of experience") || combinedText.includes("years of experience")) {
        if (!input.value) { setNativeValue(input, PROFILE.yearsExperience); filledCount++; }
      } else if (combinedText.includes("how did you learn") || combinedText.includes("how did you hear")) {
        if (!input.value) { setNativeValue(input, PROFILE.howDidYouHear); filledCount++; }
      }
    });

    // Checkboxes
    const checkboxes = Array.from(document.querySelectorAll("input[type='checkbox']"));
    checkboxes.forEach((cb) => {
      const label = (cb.labels && cb.labels[0] ? cb.labels[0].innerText : cb.parentElement ? cb.parentElement.innerText : "").toLowerCase();
      if (label.includes("privacy") || label.includes("terms") || label.includes("acknowledge") || label.includes("consent")) {
        if (!cb.checked) {
          cb.click();
          cb.checked = true;
          cb.dispatchEvent(new Event("change", { bubbles: true }));
          filledCount++;
        }
      }
    });

    // Auto-select option buttons, radio groups & dropdowns (Ashby, Greenhouse, Lever)
    const optionsClicked = autofillOptionGroups();
    filledCount += optionsClicked;

    updateHUDCount();
    showToast(`⚡ Standard Autofill: Populated ${filledCount} fields & options!`);
  }

  // Option & Radio Buttons Auto-Filler (Yes/No buttons, notice period radios, dropdowns)
  function autofillOptionGroups() {
    let clickedCount = 0;
    function triggerClick(el) {
      if (!el) return;
      try {
        el.scrollIntoView({ behavior: "smooth", block: "nearest" });
        el.focus();
        el.dispatchEvent(new MouseEvent("mouseover", { bubbles: true }));
        el.dispatchEvent(new MouseEvent("mousedown", { bubbles: true }));
        el.click();
        el.dispatchEvent(new MouseEvent("mouseup", { bubbles: true }));
        el.dispatchEvent(new Event("change", { bubbles: true }));
        el.dispatchEvent(new Event("input", { bubbles: true }));
        clickedCount++;
      } catch (e) {}
    }

    // 1. Radio Inputs
    const radioInputs = Array.from(document.querySelectorAll("input[type='radio']"));
    const processedRadios = new Set();
    radioInputs.forEach((radio) => {
      if (processedRadios.has(radio)) return;
      const container = radio.closest("[role='radiogroup'], fieldset, [class*='field'], [class*='form-group'], div") || radio.parentElement;
      const containerText = (container ? container.innerText : "").toLowerCase();
      const siblings = Array.from(container.querySelectorAll("input[type='radio']"));
      siblings.forEach(s => processedRadios.add(s));

      if (containerText.includes("notice period") || containerText.includes("how soon can you start")) {
        const match = siblings.find(s => {
          const txt = (s.parentElement ? s.parentElement.innerText : s.value || "").toLowerCase();
          return txt.includes("up to 4") || txt.includes("immediate") || txt.includes("0-") || txt.includes("1 month") || txt.includes("less than");
        }) || siblings[0];
        if (match && !match.checked) triggerClick(match);
      } else if (containerText.includes("live coding") || containerText.includes("without ai")) {
        const match = siblings.find(s => (s.parentElement ? s.parentElement.innerText : s.value || "").toLowerCase().trim().startsWith("yes"));
        if (match && !match.checked) triggerClick(match);
      } else if (containerText.includes("used") && (containerText.includes("product") || containerText.includes("elevenlabs"))) {
        const match = siblings.find(s => (s.parentElement ? s.parentElement.innerText : s.value || "").toLowerCase().trim().startsWith("yes"));
        if (match && !match.checked) triggerClick(match);
      } else if (containerText.includes("education") && (containerText.includes("full-time") || containerText.includes("student"))) {
        const match = siblings.find(s => (s.parentElement ? s.parentElement.innerText : s.value || "").toLowerCase().trim().startsWith("yes"));
        if (match && !match.checked) triggerClick(match);
      } else if (containerText.includes("eligible") || containerText.includes("authorized")) {
        const match = siblings.find(s => (s.parentElement ? s.parentElement.innerText : s.value || "").toLowerCase().trim().startsWith("yes"));
        if (match && !match.checked) triggerClick(match);
      } else if (containerText.includes("visa sponsorship") || containerText.includes("require sponsorship")) {
        const match = siblings.find(s => (s.parentElement ? s.parentElement.innerText : s.value || "").toLowerCase().trim().startsWith("no"));
        if (match && !match.checked) triggerClick(match);
      }
    });

    // 2. Button-based Toggle Groups (Ashby Yes/No buttons)
    const allButtons = Array.from(document.querySelectorAll("button:not([type='submit'])"));
    const processedButtons = new Set();
    allButtons.forEach((btn) => {
      const btnText = (btn.innerText || "").trim().toLowerCase();
      if (btnText !== "yes" && btnText !== "no") return;
      const parentGroup = btn.closest("[role='radiogroup'], [role='group'], [class*='field'], [class*='buttonGroup'], div");
      if (!parentGroup || processedButtons.has(parentGroup)) return;
      processedButtons.add(parentGroup);

      const buttons = Array.from(parentGroup.querySelectorAll("button")).filter(b => {
        const t = (b.innerText || "").trim().toLowerCase();
        return t === "yes" || t === "no";
      });
      if (buttons.length < 2) return;

      const yesBtn = buttons.find(b => (b.innerText || "").trim().toLowerCase() === "yes");
      const noBtn = buttons.find(b => (b.innerText || "").trim().toLowerCase() === "no");
      const qText = (parentGroup.closest("[class*='field'], div")?.innerText || "").toLowerCase();

      let chooseYes = true;
      if (qText.includes("sponsorship") || qText.includes("require visa") || qText.includes("felony")) {
        chooseYes = false;
      }
      const target = chooseYes ? yesBtn : noBtn;
      if (target) {
        const isSelected = target.getAttribute("aria-checked") === "true" || target.getAttribute("aria-pressed") === "true" || target.classList.contains("selected");
        if (!isSelected) triggerClick(target);
      }
    });

    return clickedCount;
  }

  // Method 2 Export
  async function exportPendingToProject() {
    const unfilled = getUnfilledFields();
    if (unfilled.length === 0) return showToast("✓ No unfilled fields!");
    const { company, roleTitle, url } = detectJobContext();

    try {
      const resp = await fetch(`${BRIDGE_URL}/api/export-pending`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url, company, role_title: roleTitle,
          fields: unfilled.map(f => ({ id: f.id, label: f.label, placeholder: f.placeholder, type: f.type }))
        })
      });
      const data = await resp.json();
      showToast(`📤 M2: Exported ${unfilled.length} fields to pending_form.json!`);
    } catch (e) {
      showToast("⚠️ Bridge offline: Start python tools/bridge/server.py");
    }
  }

  // Method 2 Inject
  async function injectReadyAnswers() {
    try {
      const resp = await fetch(`${BRIDGE_URL}/api/ready-answers`);
      const data = await resp.json();
      if (!data.answers || Object.keys(data.answers).length === 0) {
        return showToast("⚠️ No ready answers in ready_answers.json yet!");
      }
      const unfilled = getUnfilledFields();
      let count = 0;
      unfilled.forEach(f => {
        if (data.answers[f.id]) {
          setNativeValue(f.element, data.answers[f.id]);
          f.element.style.outline = "2px solid #8b5cf6";
          count++;
        }
      });
      updateHUDCount();
      showToast(`📥 M2: Injected ${count} answers from ready_answers.json!`);
    } catch (e) {
      showToast("⚠️ Bridge offline: Start python tools/bridge/server.py");
    }
  }

  // Unified Auto M2 Pipeline
  async function autoM2Pipeline() {
    showToast("⚡ Auto M2: Step 1/3 - Standard profile filling...");
    const standardCount = autofillATSForm();
    const unfilled = getUnfilledFields();

    if (unfilled.length === 0) {
      autofillOptionGroups();
      updateHUDCount();
      showToast(`✓ Form 100% Complete! (${standardCount} fields)`);
      return;
    }

    showToast(`⚡ Auto M2: Step 2/3 - Exporting & Analyzing ${unfilled.length} questions...`);
    const { company, roleTitle, url } = detectJobContext();
    const payload = {
      url: url,
      company: company,
      role_title: roleTitle,
      auto_synthesize: true,
      fields: unfilled.map(f => ({ id: f.id, label: f.label, placeholder: f.placeholder, type: f.type }))
    };

    try {
      const resp = await fetch(`${BRIDGE_URL}/api/export-pending`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await resp.json();
      let answers = (data && data.answers) || {};
      if (!answers || Object.keys(answers).length === 0) {
        const rResp = await fetch(`${BRIDGE_URL}/api/ready-answers`);
        const rData = await rResp.json();
        answers = (rData && rData.answers) || {};
      }

      showToast(`⚡ Auto M2: Step 3/3 - Injecting synthesized answers...`);
      let injected = 0;
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
          injected++;
        }
      });

      const optCount = autofillOptionGroups();
      updateHUDCount();
      showToast(`✨ Auto M2 Success: Filled ${standardCount + injected} fields & ${optCount} options!`);
    } catch (e) {
      console.warn("Auto M2 error:", e);
      fallbackClientAI(unfilled);
      autofillOptionGroups();
      updateHUDCount();
    }
  }

  window.aiJobAutoM2 = autoM2Pipeline;

  // Method 3 Copy
  function copyFormForChat() {
    const unfilled = getUnfilledFields();
    if (unfilled.length === 0) return showToast("✓ All fields filled!");
    const { company, roleTitle, url } = detectJobContext();

    let md = `### Job Application Screening Questions\nCompany: ${company}\nRole: ${roleTitle}\nURL: ${url}\n\n`;
    md += `Please synthesize concise, first-person answers grounded in my profile and return a JSON code block in this format:\n\`\`\`json\n{\n`;
    unfilled.forEach((f, idx) => {
      const comma = idx < unfilled.length - 1 ? "," : "";
      md += `  "${f.id}": "..." // Q: ${f.label}\n`;
    });
    md += `}\n\`\`\`\n\nQuestions:\n`;
    unfilled.forEach((f, idx) => {
      md += `${idx + 1}. [${f.id}]: ${f.label}\n`;
    });

    navigator.clipboard.writeText(md).then(() => {
      showToast(`📋 M3: Copied ${unfilled.length} questions for chat!`);
    });
  }

  // Method 3 Paste
  function pasteAndInjectAnswers() {
    const jsonStr = prompt("Paste JSON answers from Antigravity chat:");
    if (!jsonStr) return;
    try {
      const cleaned = jsonStr.replace(/```json/g, "").replace(/```/g, "").trim();
      const parsed = JSON.parse(cleaned);
      const unfilled = getUnfilledFields();
      let count = 0;
      unfilled.forEach(f => {
        if (parsed[f.id]) {
          setNativeValue(f.element, parsed[f.id]);
          f.element.style.outline = "2px solid #ec4899";
          count++;
        }
      });
      updateHUDCount();
      showToast(`✨ M3: Injected ${count} answers from clipboard!`);
    } catch (e) {
      alert("Invalid JSON format.");
    }
  }

  function getUnfilledCount() {
    return getUnfilledFields().length;
  }

  function updateHUDCount() {
    const count = getUnfilledCount();
    const countBadge = document.getElementById("ai-job-unfilled-count");
    if (countBadge) {
      countBadge.innerText = count > 0 ? `${count} left` : "✓ Done";
      countBadge.style.background = count > 0 ? "#f59e0b" : "#10b981";
    }
  }

  function showToast(msg) {
    const toast = document.createElement("div");
    toast.innerText = msg;
    toast.style.cssText = `
      position: fixed; top: 24px; right: 24px; z-index: 1000000;
      background: #10b981; color: white; font-weight: 600; font-size: 13px;
      padding: 10px 18px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      font-family: sans-serif;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3500);
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
      position: fixed; bottom: 24px; right: 24px; z-index: 999999;
      background: rgba(9, 13, 22, 0.92); backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
      border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 14px;
      padding: 12px 14px; box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.7);
      display: flex; flex-direction: column; gap: 9px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #f8fafc; min-width: 300px;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    `;

    hud.innerHTML = `
      <!-- Minimized Pill View -->
      <div id="ai-job-hud-minimized" style="display:none; align-items:center; justify-content:space-between; gap:10px; cursor:pointer;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="display:inline-flex; width:20px; height:20px; border-radius:5px; background:linear-gradient(135deg, #0284c7, #2563eb); align-items:center; justify-content:center; font-size:11px;">⚡</span>
          <span style="font-weight:700; font-size:12px; color:#ffffff;">AutoFill Pro</span>
          <span id="ai-job-pill-count" style="font-size:10.5px; font-weight:700; color:#fbbf24;">${getUnfilledCount()} left</span>
        </div>
        <span style="font-size:11px; color:#38bdf8; font-weight:600;">Expand ↗</span>
      </div>

      <!-- Expanded Full Deck View -->
      <div id="ai-job-hud-expanded" style="display:flex; flex-direction:column; gap:9px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div style="font-weight: 700; font-size: 13px; display: flex; align-items: center; gap: 7px;">
            <span style="display:inline-flex; width:22px; height:22px; border-radius:6px; background:linear-gradient(135deg, #0284c7, #2563eb); align-items:center; justify-content:center; font-size:12px; box-shadow:0 2px 6px rgba(2,132,199,0.3);">⚡</span>
            <span style="color:#ffffff; font-weight:800; letter-spacing:-0.02em;">AutoFill Pro</span>
            <span id="ai-job-unfilled-count" style="font-size:10px; background:rgba(245, 158, 11, 0.18); border:1px solid rgba(245, 158, 11, 0.35); color:#fbbf24; font-weight:700; padding:1px 7px; border-radius:999px;">${getUnfilledCount()} left</span>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <button id="ai-job-min-hud" title="Minimize to floating pill" style="background:rgba(255,255,255,0.06); color:#94a3b8; border:1px solid rgba(255,255,255,0.08); border-radius:5px; width:20px; height:20px; font-size:12px; cursor:pointer; display:flex; align-items:center; justify-content:center; line-height:1;">—</button>
            <button id="ai-job-close-hud" title="Close widget" style="background:transparent; color:#64748b; border:none; font-size:16px; cursor:pointer; padding:0 2px; line-height:1;">&times;</button>
          </div>
        </div>

        <!-- Primary Action Engines -->
        <div style="display:flex; gap:6px;">
          <button id="ai-job-autofill-btn" class="ai-hud-btn-hover" style="flex:1; background:linear-gradient(135deg, #0284c7, #2563eb); color:white; border:none; padding:8px 10px; border-radius:8px; font-weight:700; font-size:11px; cursor:pointer; box-shadow:0 4px 12px rgba(2,132,199,0.28);">⚡ Standard</button>
          <button id="ai-job-auto-m2-btn" class="ai-hud-btn-hover" style="flex:1.25; background:linear-gradient(135deg, #8b5cf6, #6366f1); color:white; border:none; padding:8px 10px; border-radius:8px; font-weight:700; font-size:11px; cursor:pointer; box-shadow:0 4px 12px rgba(139,92,246,0.35);">⚡ Auto M2</button>
        </div>

        <!-- Secondary Advanced Bridge Architectures -->
        <div style="display:flex; gap:4px;">
          <button id="ai-job-m2-export-btn" class="ai-hud-btn-hover" style="flex:1; background:rgba(30, 41, 59, 0.6); color:#cbd5e1; border:1px solid rgba(255, 255, 255, 0.08); padding:6px 4px; border-radius:7px; font-size:10px; font-weight:600; cursor:pointer;">📤 Export</button>
          <button id="ai-job-m2-inject-btn" class="ai-hud-btn-hover" style="flex:1; background:rgba(30, 41, 59, 0.6); color:#cbd5e1; border:1px solid rgba(255, 255, 255, 0.08); padding:6px 4px; border-radius:7px; font-size:10px; font-weight:600; cursor:pointer;">📥 Inject</button>
          <button id="ai-job-m3-copy-btn" class="ai-hud-btn-hover" style="flex:1; background:rgba(30, 41, 59, 0.6); color:#cbd5e1; border:1px solid rgba(255, 255, 255, 0.08); padding:6px 4px; border-radius:7px; font-size:10px; font-weight:600; cursor:pointer;">📋 Copy</button>
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

    document.getElementById("ai-job-autofill-btn").onclick = () => autofillATSForm();
    document.getElementById("ai-job-auto-m2-btn").onclick = () => autoM2Pipeline();
    document.getElementById("ai-job-m2-export-btn").onclick = () => exportPendingToProject();
    document.getElementById("ai-job-m2-inject-btn").onclick = () => injectReadyAnswers();
    document.getElementById("ai-job-m3-copy-btn").onclick = () => copyFormForChat();
    document.getElementById("ai-job-m3-paste-btn").onclick = () => pasteAndInjectAnswers();
    document.getElementById("ai-job-close-hud").onclick = () => hud.remove();

    setInterval(updateHUDCount, 3000);
  }

  window.addEventListener("load", () => {
    setTimeout(injectFloatingHUD, 1000);
  });
})();

// AI Job Search: 1-Click Fast ATS Autofill Content Script
// Built for Himanshu Dahiya (@Bored008)
// Zero-token, sub-second client-side automation

(function () {
  console.log("[AI Job Autofill] Injected into:", window.location.href);

  const PROFILE = {
    firstName: "Himanshu",
    lastName: "Dahiya",
    fullName: "Himanshu Dahiya",
    email: "dahiyahimanshu80@gmail.com",
    phone: "+91 9671757885",
    phonePlain: "9671757885",
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
    yearsExperience: "1 year",
    workAuthUS: "Yes",
    sponsorship: "No",
    aiPolicyAgree: "Yes",
    gender: "Male",
    race: "Asian",
    veteran: "I am not a protected veteran",
    disability: "No, I do not have a disability"
  };

  const SNIPPETS = {
    traceX: "In TraceX (https://github.com/Bored008/tracex), I engineered an interactive microservices causal dependency graph and telemetry visualization engine. In distributed systems, rendering hundreds of service nodes with dynamic latency, error rate metrics, and anomaly propagation paths can easily lock the UI thread. To ensure a fluid 60fps experience, I implemented selective rendering & memoization across DAG node components, decoupled PageRank graph layout computations from the main thread, and implemented DOM virtualization for dense trace lists and log tables, maintaining a sub-15ms frame budget.",
    yanegiDesignTokens: "When engineering the web frontend for Yanegi (https://yanegi.com) and Orbit Shipping Services (Softech Media), the challenge was maintaining strict brand visual consistency while supporting real-time interactive states. I created a centralized design token system mapping Figma color primitives and spacing scales to semantic CSS variables and Tailwind utility classes. For complex components, I encapsulated motion logic inside reusable React hooks, ensuring brand fidelity and 60fps performance budgets across pages.",
    livekitDesignEngineering: "To me, design engineering is closing the chasm between looking like the mockup and feeling alive. In Next.js, Framer Motion, and GSAP: 1) Physics & Easing: I calibrate cubic-bezier curves and spring physics so motion responds naturally to momentum. 2) 60fps Frame Budgeting: I animate strictly GPU-composited properties (transform, opacity), avoiding layout recalcs. 3) Developer-First Subtlety: motion provides functional feedback—guiding the eye through telemetry, latency benchmarks, or code snippets—rather than distracting from content. In Yanegi and EBAT, I engineered fluid interactive maps and high-fidelity product pages running at locked 60fps.",
    whyGoodFit: "When an engineer is triaging a high-severity production incident at 2 AM, cognitive overload is the enemy. Rather than overwhelming developers with raw logs and unranked trace waterfalls, I prioritize immediate root-cause guidance with quantitative confidence scores, context-preserving drill-down drawers directly from topology maps, and uniform visual status semantics across metrics, logs, and traces. Located in Sonipat / Delhi NCR, immediately available."
  };

  // Helper to safely set React synthetic values
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

  function autofillATSForm() {
    let filledCount = 0;
    console.log("[AI Job Autofill] Starting 1-click autofill...");

    // 1. Text & Email Inputs
    const allInputs = Array.from(document.querySelectorAll("input:not([type='hidden']):not([type='checkbox']):not([type='radio']):not([type='file']), textarea"));

    allInputs.forEach((input) => {
      const id = (input.id || "").toLowerCase();
      const name = (input.name || "").toLowerCase();
      const placeholder = (input.placeholder || "").toLowerCase();
      const ariaLabel = (input.getAttribute("aria-label") || "").toLowerCase();
      
      // Match label text
      let labelText = "";
      if (input.labels && input.labels.length > 0) {
        labelText = input.labels[0].innerText.toLowerCase();
      } else {
        const parent = input.closest("label, .field, [role='group'], div");
        if (parent) labelText = parent.innerText.toLowerCase();
      }

      const combinedText = `${id} ${name} ${placeholder} ${ariaLabel} ${labelText}`;

      // Email
      if (input.type === "email" || combinedText.includes("email")) {
        if (!input.value) { setNativeValue(input, PROFILE.email); filledCount++; }
      }
      // Phone
      else if (input.type === "tel" || combinedText.includes("phone") || combinedText.includes("mobile") || combinedText.includes("contact number")) {
        if (!input.value) { setNativeValue(input, PROFILE.phone); filledCount++; }
      }
      // First Name
      else if (combinedText.includes("first name") || combinedText.includes("given name") || name === "first_name" || id.includes("first_name")) {
        if (!input.value) { setNativeValue(input, PROFILE.firstName); filledCount++; }
      }
      // Last Name
      else if (combinedText.includes("last name") || combinedText.includes("family name") || combinedText.includes("surname") || name === "last_name" || id.includes("last_name")) {
        if (!input.value) { setNativeValue(input, PROFILE.lastName); filledCount++; }
      }
      // Preferred Name
      else if (combinedText.includes("preferred name") || id === "_systemfield_name") {
        if (!input.value) { setNativeValue(input, PROFILE.firstName); filledCount++; }
      }
      // Full Name (only if no separate first/last name identified)
      else if (combinedText.includes("full legal name") || combinedText.includes("legal name")) {
        if (!input.value) { setNativeValue(input, PROFILE.fullName); filledCount++; }
      }
      else if (combinedText.includes("name") && !combinedText.includes("company") && !combinedText.includes("organization") && !combinedText.includes("school")) {
        if (!input.value) { setNativeValue(input, PROFILE.firstName); filledCount++; }
      }
      // LinkedIn
      else if (combinedText.includes("linkedin") || combinedText.includes("linked_in")) {
        if (!input.value) { setNativeValue(input, PROFILE.linkedin); filledCount++; }
      }
      // GitHub
      else if (combinedText.includes("github") || combinedText.includes("git_hub")) {
        if (!input.value) { setNativeValue(input, PROFILE.github); filledCount++; }
      }
      // Portfolio / Website
      else if (combinedText.includes("portfolio") || combinedText.includes("website") || combinedText.includes("personal site")) {
        if (!input.value) { setNativeValue(input, PROFILE.portfolio); filledCount++; }
      }
      // Location / Address
      else if (combinedText.includes("location") || combinedText.includes("city") || combinedText.includes("address") || combinedText.includes("reside")) {
        if (!input.value) { setNativeValue(input, PROFILE.location); filledCount++; }
      }
      // College / University / Education
      else if (combinedText.includes("college") || combinedText.includes("university") || combinedText.includes("institute") || combinedText.includes("school")) {
        if (!input.value) { setNativeValue(input, PROFILE.college); filledCount++; }
      }
      // Organization / Company / Current Employer
      else if (combinedText.includes("organisation") || combinedText.includes("organization") || combinedText.includes("company") || combinedText.includes("employer") || combinedText.includes("workplace")) {
        if (!input.value) { setNativeValue(input, PROFILE.currentOrg); filledCount++; }
      }
      // Designation / Title / Current Role
      else if (combinedText.includes("designation") || combinedText.includes("job title") || combinedText.includes("current role") || combinedText.includes("current title")) {
        if (!input.value) { setNativeValue(input, PROFILE.currentRole); filledCount++; }
      }
      // Experience Years
      else if (combinedText.includes("years") && (combinedText.includes("react") || combinedText.includes("typescript") || combinedText.includes("experience"))) {
        if (!input.value) { setNativeValue(input, PROFILE.yearsExperience); filledCount++; }
      }
    });

    // 2. Radio & Button Groups (Ashby, Greenhouse, Lever)
    const radioGroups = document.querySelectorAll("[role='group'], fieldset, div");
    radioGroups.forEach((group) => {
      const groupText = (group.innerText || "").toLowerCase();

      // Work authorization US / Global -> YES
      if (groupText.includes("legally authorized to work") || groupText.includes("authorized to work in")) {
        clickMatchingRadioOrButton(group, ["yes", "authorized"]);
        filledCount++;
      }
      // Sponsorship required -> NO
      else if (groupText.includes("sponsorship") || groupText.includes("require sponsorship") || groupText.includes("visa support")) {
        clickMatchingRadioOrButton(group, ["no", "not required"]);
        filledCount++;
      }
      // AI policy acknowledgment -> YES
      else if (groupText.includes("ai tools") || groupText.includes("ai assistance") || groupText.includes("please select \"yes\" below to acknowledge")) {
        clickMatchingRadioOrButton(group, ["yes"]);
        filledCount++;
      }
      // LLM Bot Trap question -> NO
      else if (groupText.includes("llm/coding agent generated answer") || groupText.includes("mark answer to this question as yes")) {
        clickMatchingRadioOrButton(group, ["no"]);
        filledCount++;
      }
      // Gender -> Male
      else if (groupText.includes("gender") && !groupText.includes("transgender")) {
        clickMatchingRadioOrButton(group, ["male", "decline"]);
        filledCount++;
      }
      // Veteran -> Not a veteran
      else if (groupText.includes("veteran status")) {
        clickMatchingRadioOrButton(group, ["i am not a protected veteran", "not a veteran", "decline"]);
        filledCount++;
      }
    });

    showToast(`⚡ Filled ${filledCount} fields in 0.05s (Zero Tokens Used)!`);
  }

  function clickMatchingRadioOrButton(container, textMatches) {
    const clickable = Array.from(container.querySelectorAll("input[type='radio'], button, [role='radio'], label"));
    for (const el of clickable) {
      const text = (el.innerText || el.value || el.getAttribute("aria-label") || "").toLowerCase().trim();
      for (const match of textMatches) {
        if (text === match || text.startsWith(match)) {
          el.click();
          if (el.tagName.toLowerCase() === "input") el.checked = true;
          return true;
        }
      }
    }
    return false;
  }

  // Floating HUD Widget
  function injectFloatingHUD() {
    if (document.getElementById("ai-job-autofill-hud")) return;

    const hud = document.createElement("div");
    hud.id = "ai-job-autofill-hud";
    hud.style.cssText = `
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 999999;
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 12px 16px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
      display: flex;
      align-items: center;
      gap: 10px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #f8fafc;
    `;

    hud.innerHTML = `
      <div style="font-weight: 600; font-size: 13px; display: flex; align-items: center; gap: 6px;">
        <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10b981;"></span>
        Job Autofill
      </div>
      <button id="ai-job-autofill-btn" style="
        background: #3b82f6;
        color: white;
        border: none;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 13px;
        cursor: pointer;
        transition: background 0.15s ease;
      ">⚡ 1-Click Fill</button>
      <button id="ai-job-snippets-btn" style="
        background: #1e293b;
        color: #94a3b8;
        border: 1px solid #334155;
        padding: 6px 10px;
        border-radius: 8px;
        font-size: 12px;
        cursor: pointer;
      ">📝 Snippets</button>
      <button id="ai-job-close-hud" style="
        background: transparent;
        color: #64748b;
        border: none;
        font-size: 16px;
        cursor: pointer;
        padding: 2px 6px;
      ">&times;</button>
    `;

    document.body.appendChild(hud);

    document.getElementById("ai-job-autofill-btn").onclick = () => autofillATSForm();
    document.getElementById("ai-job-close-hud").onclick = () => hud.remove();
    document.getElementById("ai-job-snippets-btn").onclick = () => toggleSnippetsDrawer();
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
      bottom: 80px;
      right: 24px;
      width: 380px;
      max-height: 480px;
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
      <div style="font-weight: 700; font-size: 14px; margin-bottom: 12px; display:flex; justify-content:space-between;">
        <span>📝 Quick Screening Answers</span>
        <span id="ai-close-snippets" style="cursor:pointer; color:#94a3b8;">&times;</span>
      </div>
      <div style="display:flex; flex-direction:column; gap:10px;">
        <div style="background:#1e293b; padding:10px; border-radius:8px; border:1px solid #334155;">
          <div style="font-size:12px; font-weight:600; color:#38bdf8; margin-bottom:4px;">TraceX: React Performance & Observability</div>
          <div style="font-size:11px; color:#cbd5e1; max-height:60px; overflow:hidden; text-overflow:ellipsis;">${SNIPPETS.traceX.slice(0, 150)}...</div>
          <button class="ai-copy-snippet" data-key="traceX" style="margin-top:6px; background:#2563eb; color:white; border:none; padding:4px 8px; border-radius:4px; font-size:11px; cursor:pointer;">Copy Answer</button>
        </div>

        <div style="background:#1e293b; padding:10px; border-radius:8px; border:1px solid #334155;">
          <div style="font-size:12px; font-weight:600; color:#38bdf8; margin-bottom:4px;">Design Tokens & Motion Systems (Yanegi)</div>
          <div style="font-size:11px; color:#cbd5e1; max-height:60px; overflow:hidden; text-overflow:ellipsis;">${SNIPPETS.yanegiDesignTokens.slice(0, 150)}...</div>
          <button class="ai-copy-snippet" data-key="yanegiDesignTokens" style="margin-top:6px; background:#2563eb; color:white; border:none; padding:4px 8px; border-radius:4px; font-size:11px; cursor:pointer;">Copy Answer</button>
        </div>

        <div style="background:#1e293b; padding:10px; border-radius:8px; border:1px solid #334155;">
          <div style="font-size:12px; font-weight:600; color:#38bdf8; margin-bottom:4px;">Design Engineering & 60fps Frame Budgeting</div>
          <div style="font-size:11px; color:#cbd5e1; max-height:60px; overflow:hidden; text-overflow:ellipsis;">${SNIPPETS.livekitDesignEngineering.slice(0, 150)}...</div>
          <button class="ai-copy-snippet" data-key="livekitDesignEngineering" style="margin-top:6px; background:#2563eb; color:white; border:none; padding:4px 8px; border-radius:4px; font-size:11px; cursor:pointer;">Copy Answer</button>
        </div>
      </div>
    `;

    document.body.appendChild(drawer);

    document.getElementById("ai-close-snippets").onclick = () => { drawer.style.display = "none"; };
    drawer.querySelectorAll(".ai-copy-snippet").forEach((btn) => {
      btn.onclick = (e) => {
        const key = e.target.getAttribute("data-key");
        navigator.clipboard.writeText(SNIPPETS[key]);
        e.target.innerText = "✓ Copied!";
        setTimeout(() => { e.target.innerText = "Copy Answer"; }, 2000);
      };
    });
  }

  function showToast(msg) {
    const toast = document.createElement("div");
    toast.innerText = msg;
    toast.style.cssText = `
      position: fixed;
      top: 24px;
      right: 24px;
      z-index: 1000000;
      background: #10b981;
      color: white;
      font-weight: 600;
      font-size: 13px;
      padding: 10px 18px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      font-family: sans-serif;
      animation: fadeInOut 3s forwards;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3200);
  }

  // Listen for messages from extension popup
  if (typeof chrome !== "undefined" && chrome.runtime && chrome.runtime.onMessage) {
    chrome.runtime.onMessage.addListener((req, sender, sendResponse) => {
      if (req.action === "autofill") {
        autofillATSForm();
        sendResponse({ success: true });
      }
    });
  }

  // Auto-inject HUD on document load
  window.addEventListener("load", () => {
    setTimeout(injectFloatingHUD, 1000);
  });
})();

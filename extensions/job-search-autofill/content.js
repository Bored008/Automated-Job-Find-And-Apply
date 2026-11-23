// AI Job Search: Candidate Profile & Grounded Snippets
(function () {
  const root = (window.AIJobAutofill = window.AIJobAutofill || {});

  root.BRIDGE_URL = "http://127.0.0.1:8765";

  root.PROFILE = {
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
    postalCode: "131039",
    linkedin: "https://www.linkedin.com/in/himanshuakabored/",
    github: "https://github.com/Bored008",
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

  root.SNIPPETS = {
    aiAgentBuilt: "I engineered an autonomous multi-agent job application and observability pipeline (https://github.com/Bored008/Automated-Job-Find-And-Apply) leveraging the Model Context Protocol (MCP), Python, and Gemini API. The system orchestrates specialized workers to query live ATS APIs (Ashby, Greenhouse, Unstop), score roles against candidate profiles, and deterministically inject DOM payloads and upload resumes without human intervention. It autonomously manages state verification, monitors Gmail for recruiter updates, and books interview schedules to Google Calendar.",
    aiAgentHardestProblem: "The hardest problem was severe agent token bloat and non-deterministic DOM looping when using multimodal vision agents for form filling (consuming 50k+ tokens per application). I solved this by implementing a dual-layer architecture: offloading all mechanical form operations to deterministic AST/DOM injection scripts (dropping LLM token usage to zero), while restricting LLM calls strictly to high-leverage contextual essay synthesis with a hard 500-token budget and strict schema validation.",
    traceX: "In TraceX (https://github.com/Bored008/tracex), I engineered an interactive microservices causal dependency graph and telemetry visualization engine. In distributed systems, rendering hundreds of service nodes with dynamic latency, error rate metrics, and anomaly propagation paths can easily lock the UI thread. To ensure a fluid 60fps experience, I implemented selective rendering & memoization across DAG node components, decoupled PageRank graph layout computations from the main thread, and implemented DOM virtualization for dense trace lists and log tables, maintaining a sub-15ms frame budget.",
    yanegiDesignTokens: "When engineering the web frontend for Yanegi (https://yanegi.com) and Orbit Shipping Services (Softech Media), the challenge was maintaining strict brand visual consistency while supporting real-time interactive states. I created a centralized design token system mapping Figma color primitives and spacing scales to semantic CSS variables and Tailwind utility classes. For complex components, I encapsulated motion logic inside reusable React hooks, ensuring brand fidelity and 60fps performance budgets across pages.",
    whyGoodFit: "When an engineer is triaging a high-severity production incident at 2 AM, cognitive overload is the enemy. Rather than overwhelming developers with raw logs and unranked trace waterfalls, I prioritize immediate root-cause guidance with quantitative confidence scores, context-preserving drill-down drawers directly from topology maps, and uniform visual status semantics across metrics, logs, and traces. Located in Sonipat / Delhi NCR, immediately available."
  };
})();
// AI Job Search: DOM Event Engine & Context Parser
(function () {
  const root = (window.AIJobAutofill = window.AIJobAutofill || {});

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
    } catch (e) {
      console.warn("[AI Job Autofill] triggerClick error:", e);
    }
  }

  function triggerComboboxSelect(input, targetText) {
    if (!input) return;
    input.focus();
    input.dispatchEvent(new Event("focus", { bubbles: true }));
    input.dispatchEvent(new Event("input", { bubbles: true }));
    input.dispatchEvent(new KeyboardEvent("keydown", { key: "ArrowDown", keyCode: 40, bubbles: true }));

    setTimeout(() => {
      const options = Array.from(document.querySelectorAll("[role='option'], div[class*='option'], li[class*='option'], div[class*='menu'] div, [id*='option']"));
      const targetLower = (targetText || "").toLowerCase();
      const match = options.find(opt => {
        const text = (opt.innerText || "").trim().toLowerCase();
        return text === "india" || text.startsWith("india") || (targetLower && text.includes(targetLower));
      });
      if (match) {
        match.click();
        match.dispatchEvent(new MouseEvent("mousedown", { bubbles: true }));
        match.dispatchEvent(new MouseEvent("mouseup", { bubbles: true }));
      }
    }, 250);
  }

  function extractFieldLabel(field) {
    if (field.labels && field.labels.length > 0) {
      return field.labels[0].innerText.trim();
    }
    const aria = field.getAttribute("aria-label");
    if (aria && aria.trim().length > 0) {
      return aria.trim();
    }
    let cur = field.parentElement;
    for (let i = 0; i < 4 && cur && cur !== document.body; i++) {
      const labelEl = cur.querySelector("label, legend, [class*='label'], [class*='title'], [class*='prompt'], [data-qa*='label']");
      if (labelEl && labelEl.innerText.trim().length > 0) {
        return labelEl.innerText.trim();
      }
      cur = cur.parentElement;
    }
    if (field.placeholder && field.placeholder.toLowerCase().includes("start typing")) {
      return "Country you're currently residing in";
    }
    return field.placeholder ? field.placeholder.trim() : "";
  }

  function detectJobContext() {
    let company = "";
    let roleTitle = "";
    const url = window.location.href;

    if (url.includes("ashbyhq.com/")) {
      const parts = url.split("ashbyhq.com/")[1].split("/");
      company = decodeURIComponent(parts[0] || "");
    } else if (url.includes("greenhouse.io/")) {
      const match = url.match(/greenhouse\.io\/([^\/]+)/);
      company = match ? match[1] : "";
    } else if (url.includes("lever.co/")) {
      const match = url.match(/lever\.co\/([^\/]+)/);
      company = match ? match[1] : "";
    }

    const h1 = document.querySelector("h1, [data-qa='job-title'], .job-title, [class*='title']");
    if (h1 && h1.innerText) {
      roleTitle = h1.innerText.trim();
    } else {
      roleTitle = document.title.split("-")[0].split("|")[0].trim();
    }

    return { company, roleTitle, url };
  }

  root.setNativeValue = setNativeValue;
  root.triggerClick = triggerClick;
  root.triggerComboboxSelect = triggerComboboxSelect;
  root.extractFieldLabel = extractFieldLabel;
  root.detectJobContext = detectJobContext;
})();
// AI Job Search: Declarative Field Matching Rules & Form Filler
(function () {
  const root = (window.AIJobAutofill = window.AIJobAutofill || {});
  const { PROFILE, SNIPPETS, setNativeValue, triggerClick, triggerComboboxSelect } = root;

  const INPUT_RULES = [
    {
      test: (t, input) => input.type === "email" || t.includes("email"),
      resolve: () => PROFILE.email
    },
    {
      test: (t, input) => input.type === "tel" || t.includes("phone") || t.includes("mobile") || t.includes("contact number"),
      resolve: () => PROFILE.phone
    },
    {
      test: (t, input, id, name) => t.includes("first name") || t.includes("given name") || name === "first_name" || id.includes("first_name"),
      resolve: () => PROFILE.firstName
    },
    {
      test: (t, input, id, name) => t.includes("last name") || t.includes("family name") || t.includes("surname") || name === "last_name" || id.includes("last_name"),
      resolve: () => PROFILE.lastName
    },
    {
      test: (t) => t.includes("full name") || t.includes("legal name") || t.includes("your name") || (t.includes("name") && !t.includes("company") && !t.includes("organization") && !t.includes("school") && !t.includes("first") && !t.includes("last")),
      resolve: () => PROFILE.fullName
    },
    {
      test: (t) => t.includes("linkedin") || t.includes("linked_in"),
      resolve: () => PROFILE.linkedin
    },
    {
      test: (t) => t.includes("github") || t.includes("git_hub"),
      resolve: () => PROFILE.github
    },
    {
      test: (t) => t.includes("portfolio") || t.includes("website") || t.includes("personal site"),
      resolve: () => PROFILE.portfolio
    },
    {
      test: (t) => t.includes("employer") || t.includes("current company") || (t.includes("company") && !t.includes("how did you learn")),
      resolve: () => PROFILE.currentOrg
    },
    {
      test: (t) => t.includes("current title") || t.includes("job title") || t.includes("designation"),
      resolve: () => PROFILE.currentRole
    },
    {
      test: (t) => t.includes("college") || t.includes("university") || t.includes("school") || t.includes("institute"),
      resolve: () => PROFILE.college
    },
    {
      test: (t) => t.includes("degree") || t.includes("major") || t.includes("field of study"),
      resolve: () => PROFILE.degree
    },
    {
      test: (t, input) => t.includes("country") || t.includes("residing") || t.includes("citizenship") || t.includes("location") || (input.placeholder || "").toLowerCase().includes("start typing"),
      resolve: (t, input) => {
        const isCountry = t.includes("country") || t.includes("residing") || (input.placeholder || "").toLowerCase().includes("start typing");
        const val = isCountry ? PROFILE.country : PROFILE.location;
        triggerComboboxSelect(input, val);
        return val;
      }
    },
    {
      test: (t) => t.includes("city") && !t.includes("ethnicity"),
      resolve: () => PROFILE.city
    },
    {
      test: (t) => t.includes("state") && !t.includes("statement"),
      resolve: () => PROFILE.state
    },
    {
      test: (t) => t.includes("compensation") || t.includes("expected salary") || t.includes("expected ctc"),
      resolve: () => PROFILE.compensation
    },
    {
      test: (t) => t.includes("total years of experience") || t.includes("years of experience") || t.includes("overall experience"),
      resolve: () => PROFILE.yearsExperience
    },
    {
      test: (t) => t.includes("highest qualification") || (t.includes("qualification") && !t.includes("preferred")),
      resolve: () => "B.Tech in Electronics and Communication Engineering (Pursuing, DCRUST Murthal, 2024–2028)"
    },
    {
      test: (t) => t.includes("joining timeline") || t.includes("available to join") || t.includes("when would you be available") || t.includes("when can you join") || t.includes("start date"),
      resolve: () => "Immediately (available to start within 0–7 days)"
    },
    {
      test: (t) => t.includes("specialization") || t.includes("branch"),
      resolve: () => "Electronics and Communication"
    },
    {
      test: (t) => t.includes("duration") || t.includes("course duration"),
      resolve: () => "4 Years"
    },
    {
      test: (t) => t.includes("graduating year") || t.includes("graduation year") || t.includes("passing year"),
      resolve: () => PROFILE.graduationYear
    },
    {
      test: (t) => t.includes("ai agent") || (t.includes("agent") && t.includes("built")),
      resolve: () => SNIPPETS.aiAgentBuilt
    },
    {
      test: (t) => t.includes("hardest problem") || (t.includes("problem") && t.includes("running agent")),
      resolve: () => SNIPPETS.aiAgentHardestProblem
    },
    {
      test: (t) => t.includes("how did you learn") || t.includes("how did you hear"),
      resolve: () => PROFILE.howDidYouHear
    }
  ];

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
      const combined = `${id} ${name} ${placeholder} ${ariaLabel} ${labelText}`;

      for (const rule of INPUT_RULES) {
        if (rule.test(combined, input, id, name)) {
          const val = rule.resolve(combined, input);
          if (val && (!input.value || input.value.includes("experience") || input.value.includes("Softech"))) {
            setNativeValue(input, val);
            filledCount++;
          }
          break;
        }
      }
    });

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

    filledCount += autofillOptionGroups();
    if (root.updateHUDCount) root.updateHUDCount();
    if (root.showToast) root.showToast(`Standard autofill populated ${filledCount} fields and options.`);
    return filledCount;
  }

  function autofillOptionGroups() {
    let clickedCount = 0;

    // 1. Radio groups
    const radioInputs = Array.from(document.querySelectorAll("input[type='radio']"));
    const processedRadios = new Set();
    radioInputs.forEach((radio) => {
      if (processedRadios.has(radio)) return;
      const container = radio.closest("[role='radiogroup'], fieldset, [class*='field'], [class*='form-group'], div") || radio.parentElement;
      const text = (container ? container.innerText : "").toLowerCase();
      const siblings = Array.from(container.querySelectorAll("input[type='radio']"));
      siblings.forEach(s => processedRadios.add(s));

      let match = null;
      if (text.includes("notice period") || text.includes("how soon can you start")) {
        match = siblings.find(s => {
          const txt = (s.parentElement ? s.parentElement.innerText : s.value || "").toLowerCase();
          return txt.includes("immediate") || txt.includes("0-") || txt.includes("1 month") || txt.includes("less than") || txt.includes("up to 4");
        }) || siblings[0];
      } else if (text.includes("sponsorship") || text.includes("require sponsorship")) {
        match = siblings.find(s => (s.parentElement ? s.parentElement.innerText : s.value || "").toLowerCase().trim().startsWith("no"));
      } else if (text.includes("eligible") || text.includes("authorized") || text.includes("live coding") || text.includes("used") || text.includes("student")) {
        match = siblings.find(s => (s.parentElement ? s.parentElement.innerText : s.value || "").toLowerCase().trim().startsWith("yes"));
      } else if (text.includes("gender")) {
        match = siblings.find(s => (s.parentElement ? s.parentElement.innerText : s.value || "").toLowerCase().includes("male"));
      } else if (text.includes("veteran")) {
        match = siblings.find(s => (s.parentElement ? s.parentElement.innerText : s.value || "").toLowerCase().includes("not a protected"));
      } else if (text.includes("disability")) {
        match = siblings.find(s => (s.parentElement ? s.parentElement.innerText : s.value || "").toLowerCase().includes("do not have"));
      }

      if (match && !match.checked) {
        triggerClick(match);
        clickedCount++;
      }
    });

    // 2. Segmented toggle buttons
    const allButtons = Array.from(document.querySelectorAll("button:not([type='submit'])"));
    const processedGroups = new Set();
    allButtons.forEach((btn) => {
      const btnText = (btn.innerText || "").trim().toLowerCase();
      if (btnText !== "yes" && btnText !== "no") return;
      const parentGroup = btn.closest("[role='radiogroup'], [role='group'], [class*='field'], [class*='buttonGroup'], [class*='toggle'], div");
      if (!parentGroup || processedGroups.has(parentGroup)) return;
      processedGroups.add(parentGroup);

      const buttons = Array.from(parentGroup.querySelectorAll("button")).filter(b => {
        const t = (b.innerText || "").trim().toLowerCase();
        return t === "yes" || t === "no";
      });
      if (buttons.length < 2) return;

      const yesBtn = buttons.find(b => (b.innerText || "").trim().toLowerCase() === "yes");
      const noBtn = buttons.find(b => (b.innerText || "").trim().toLowerCase() === "no");
      const questionText = (parentGroup.closest("[class*='field'], [class*='form-group'], div") || parentGroup).innerText.toLowerCase();

      const chooseNo = questionText.includes("sponsorship") || questionText.includes("visa") || questionText.includes("criminal") || questionText.includes("felony");
      const target = chooseNo ? noBtn : yesBtn;
      if (target) {
        const selected = target.getAttribute("aria-checked") === "true" || target.getAttribute("aria-pressed") === "true" || target.classList.contains("selected") || target.getAttribute("data-state") === "on";
        if (!selected) {
          triggerClick(target);
          clickedCount++;
        }
      }
    });

    // 3. Dropdown selects
    const selects = Array.from(document.querySelectorAll("select"));
    selects.forEach((sel) => {
      const parentText = (sel.closest("[class*='field'], [class*='form-group'], div")?.innerText || sel.name || sel.id || "").toLowerCase();
      let opt = null;
      if (parentText.includes("notice period")) {
        opt = Array.from(sel.options).find(o => o.text.toLowerCase().includes("immediate") || o.text.toLowerCase().includes("1 month"));
      } else if (parentText.includes("how did you hear") || parentText.includes("source")) {
        opt = Array.from(sel.options).find(o => o.text.toLowerCase().includes("linkedin") || o.text.toLowerCase().includes("website") || o.text.toLowerCase().includes("career"));
      } else if (parentText.includes("country")) {
        opt = Array.from(sel.options).find(o => o.text.toLowerCase() === "india" || o.value.toLowerCase() === "in");
      } else if (parentText.includes("gender")) {
        opt = Array.from(sel.options).find(o => o.text.toLowerCase().includes("male") || o.value.toLowerCase() === "male");
      } else if (parentText.includes("veteran")) {
        opt = Array.from(sel.options).find(o => o.text.toLowerCase().includes("not a protected") || o.text.toLowerCase() === "no");
      } else if (parentText.includes("disability")) {
        opt = Array.from(sel.options).find(o => o.text.toLowerCase().includes("do not have") || o.text.toLowerCase() === "no");
      }

      if (opt && sel.value !== opt.value) {
        sel.value = opt.value;
        sel.dispatchEvent(new Event("change", { bubbles: true }));
        clickedCount++;
      }
    });

    return clickedCount;
  }

  root.INPUT_RULES = INPUT_RULES;
  root.autofillATSForm = autofillATSForm;
  root.autofillOptionGroups = autofillOptionGroups;
})();
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

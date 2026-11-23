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

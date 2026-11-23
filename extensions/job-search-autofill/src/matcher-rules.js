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

// Universal High-Speed Zero-Token Form Injector Engine
// Built for Himanshu Dahiya
// Can be evaluated directly in any browser context (Playwright, Puppeteer, Chrome DevTools Console)

(function universalJobAutofill() {
  console.log("[Universal Autofill] Initializing instantaneous form population...");

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
    
    // Explicit Entity Disambiguation:
    // Employer vs Educational Institute
    currentEmployer: "Softech Media",
    currentRole: "Software Engineer Intern",
    experienceYears: "1",
    experienceYearsFormatted: "1 year",
    
    college: "Deenbandhu Chhotu Ram University of Science and Technology (DCRUST), Murthal, Sonipat",
    collegeShort: "DCRUST Murthal",
    degree: "B.Tech in Electronics and Communication Engineering",
    graduationYear: "2028",
    
    linkedin: "https://www.linkedin.com/in/himanshuakabored/",
    github: "https://github.com/Himanshu-Dahiya-24",
    portfolio: "https://himanshudahiya.vercel.app/",
    twitter: "https://x.com/Bored_OO8",
    
    pitchFrontend: "I am a Frontend Developer proficient in React.js, Next.js, TypeScript, and modern responsive UI engineering. Currently pursuing B.Tech in ECE at DCRUST Murthal (2024-2028), I have practical engineering experience developing scalable web interfaces at Softech Media and interactive animated apps with Next.js/Tailwind CSS at Yanegi.",
    pitchDesign: "I am a UI/UX Designer and Frontend Technologist specializing in user-centered design, interactive prototyping, and scalable design systems in Figma. I designed and developed interactive experiences for Yanegi and user-facing portals at Softech Media, ensuring visual clarity, intuitive navigation, and high brand consistency.",
    
    gender: "Male",
    workAuth: "Yes",
    sponsorship: "No",
    veteran: "I am not a protected veteran",
    disability: "No, I do not have a disability"
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

    element.dispatchEvent(new Event("input", { bubbles: true, cancelable: true }));
    element.dispatchEvent(new Event("change", { bubbles: true, cancelable: true }));
    element.dispatchEvent(new Event("blur", { bubbles: true, cancelable: true }));
  }

  function clickOption(container, matchWords) {
    const clickable = Array.from(container.querySelectorAll("input[type='radio'], button, [role='radio'], label, [role='option'], .dropdown-item, li"));
    for (const el of clickable) {
      const text = (el.innerText || el.value || el.getAttribute("aria-label") || "").toLowerCase().trim();
      for (const w of matchWords) {
        if (text === w || text.includes(w)) {
          el.click();
          if (el.tagName.toLowerCase() === "input") el.checked = true;
          return true;
        }
      }
    }
    return false;
  }

  let filledCount = 0;

  // 1. Text Inputs and Textareas across Ashby, Greenhouse, Lever, Unstop, Workday
  const inputs = Array.from(document.querySelectorAll("input, textarea, select"));
  inputs.forEach((input) => {
    const type = (input.type || "").toLowerCase();
    if (["hidden", "submit", "button", "checkbox", "radio", "file"].includes(type)) return;

    const name = (input.name || "").toLowerCase();
    const id = (input.id || "").toLowerCase();
    const placeholder = (input.placeholder || "").toLowerCase();
    const ariaLabel = (input.getAttribute("aria-label") || "").toLowerCase();
    const autocomplete = (input.getAttribute("autocomplete") || "").toLowerCase();
    
    // Nearest label / parent text
    let labelText = "";
    if (input.labels && input.labels.length > 0) {
      labelText = Array.from(input.labels).map(l => l.innerText).join(" ").toLowerCase();
    } else {
      const parent = input.closest(".form-group, .field, [class*='field'], [class*='input'], div, label");
      labelText = parent ? (parent.innerText || "").toLowerCase() : "";
    }

    const fieldTag = `${name} ${id} ${placeholder} ${ariaLabel} ${autocomplete} ${labelText}`;

    // FIRST NAME
    if (fieldTag.includes("first name") || fieldTag.includes("given name") || fieldTag.includes("fname") || name === "first_name") {
      if (!input.value) { setNativeValue(input, PROFILE.firstName); filledCount++; }
    }
    // LAST NAME
    else if (fieldTag.includes("last name") || fieldTag.includes("family name") || fieldTag.includes("lname") || fieldTag.includes("surname") || name === "last_name") {
      if (!input.value) { setNativeValue(input, PROFILE.lastName); filledCount++; }
    }
    // FULL NAME
    else if (fieldTag.includes("full name") || fieldTag.includes("your name") || fieldTag.includes("candidate name") || name === "name") {
      if (!input.value) { setNativeValue(input, PROFILE.fullName); filledCount++; }
    }
    // EMAIL
    else if (type === "email" || fieldTag.includes("email") || autocomplete === "email") {
      if (!input.value) { setNativeValue(input, PROFILE.email); filledCount++; }
    }
    // PHONE
    else if (type === "tel" || fieldTag.includes("phone") || fieldTag.includes("mobile") || fieldTag.includes("contact number") || autocomplete === "tel") {
      if (!input.value) {
        setNativeValue(input, fieldTag.includes("+") || fieldTag.includes("code") ? PROFILE.phone : PROFILE.phonePlain);
        filledCount++;
      }
    }
    // LINKEDIN
    else if (fieldTag.includes("linkedin") || fieldTag.includes("linkedin.com")) {
      if (!input.value) { setNativeValue(input, PROFILE.linkedin); filledCount++; }
    }
    // GITHUB
    else if (fieldTag.includes("github") || fieldTag.includes("github.com")) {
      if (!input.value) { setNativeValue(input, PROFILE.github); filledCount++; }
    }
    // PORTFOLIO / WEBSITE
    else if (fieldTag.includes("portfolio") || fieldTag.includes("website") || fieldTag.includes("personal site") || fieldTag.includes("url")) {
      if (!input.value) { setNativeValue(input, PROFILE.portfolio); filledCount++; }
    }
    // COLLEGE / UNIVERSITY (Education)
    else if (fieldTag.includes("college") || fieldTag.includes("university") || fieldTag.includes("institute") || fieldTag.includes("school")) {
      if (!input.value) { setNativeValue(input, PROFILE.college); filledCount++; }
    }
    // EMPLOYER / ORGANIZATION / COMPANY (Work Experience)
    else if (fieldTag.includes("organisation") || fieldTag.includes("organization") || fieldTag.includes("company") || fieldTag.includes("current employer") || fieldTag.includes("workplace")) {
      if (!input.value) { setNativeValue(input, PROFILE.currentEmployer); filledCount++; }
    }
    // DESIGNATION / TITLE
    else if (fieldTag.includes("designation") || fieldTag.includes("job title") || fieldTag.includes("current role")) {
      if (!input.value) { setNativeValue(input, PROFILE.currentRole); filledCount++; }
    }
    // EXPERIENCE (Years)
    else if (fieldTag.includes("experience") && (fieldTag.includes("years") || fieldTag.includes("total"))) {
      if (!input.value) { setNativeValue(input, PROFILE.experienceYears); filledCount++; }
    }
    // LOCATION / CITY / ADDRESS
    else if (fieldTag.includes("location") || fieldTag.includes("city") || fieldTag.includes("current address") || fieldTag.includes("residence")) {
      if (!input.value) { setNativeValue(input, PROFILE.location); filledCount++; }
    }
    // PITCH / COVER / WHY JOIN
    else if (input.tagName.toLowerCase() === "textarea" && (fieldTag.includes("why") || fieldTag.includes("cover") || fieldTag.includes("pitch") || fieldTag.includes("about you") || fieldTag.includes("introduce"))) {
      if (!input.value) { setNativeValue(input, PROFILE.pitchFrontend); filledCount++; }
    }
  });

  // 2. Radio Groups & Compliance Question Handling
  const groups = document.querySelectorAll("[role='group'], fieldset, div");
  groups.forEach((g) => {
    const text = (g.innerText || "").toLowerCase();
    if (text.includes("authorized to work") || text.includes("legally authorized")) {
      clickOption(g, ["yes", "authorized"]);
    } else if (text.includes("sponsorship") || text.includes("visa")) {
      clickOption(g, ["no", "not required"]);
    } else if (text.includes("gender")) {
      clickOption(g, ["male"]);
    } else if (text.includes("terms") || text.includes("agree") || text.includes("acknowledge")) {
      const chk = g.querySelector("input[type='checkbox']");
      if (chk && !chk.checked) { chk.click(); chk.checked = true; }
    }
  });

  console.log(`[Universal Autofill] Completed instant fill: ${filledCount} fields populated.`);
  return { success: true, fieldsFilled: filledCount };
})();

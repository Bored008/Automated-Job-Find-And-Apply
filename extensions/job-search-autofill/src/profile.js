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

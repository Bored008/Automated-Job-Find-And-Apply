"""
Agent Bridge Engine
===================
Synthesizes grounded screening answers and field values using Himanshu Dahiya's
canonical candidate profile and project evidence. Table-driven intent dispatch
eliminates order-dependent conditional sprawl and redundant blocks.
"""

import json
import os
import ssl
import urllib.request
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

PROFILE = {
    "first_name": "Himanshu",
    "last_name": "Dahiya",
    "full_name": "Himanshu Dahiya",
    "email": "dahiyahimanshu80@gmail.com",
    "phone": "+91 7015708154",
    "phone_plain": "7015708154",
    "location": "Sonipat, Haryana, India",
    "city": "Sonipat",
    "state": "Haryana",
    "country": "India",
    "postal_code": "131039",
    "college": "Deenbandhu Chhotu Ram University of Science and Technology (DCRUST), Murthal, Sonipat",
    "degree": "B.Tech in Electronics and Communication Engineering",
    "qualification": "B.Tech in Electronics and Communication Engineering (Pursuing, DCRUST Murthal, 2024–2028)",
    "graduation_year": "2028",
    "duration": "4 Years",
    "cgpa": "7.5 CGPA",
    "employer": "Softech Media",
    "designation": "Software Engineer Intern",
    "experience_years": "1",
    "joining_timeline": "Immediately (available to start within 0–7 days)",
    "compensation": "Open to discussion / standard market rate (₹10–14 LPA or standard internship stipend)",
    "how_did_you_hear": "LinkedIn / Company Careers Page",
    "skills": "React.js, Next.js, TypeScript, JavaScript, Python, FastAPI, Tailwind CSS, Redux, Node.js, Git",
    "linkedin": "https://www.linkedin.com/in/himanshuakabored/",
    "github": "https://github.com/Bored008",
    "portfolio": "https://himanshudahiya.vercel.app/",
    "resume_path": str(WORKSPACE_ROOT / "cv" / "Himanshu_Dahiya_Resume.pdf")
}

EVIDENCE_SNIPPETS = {
    "ai_agent_built": (
        "I engineered an autonomous multi-agent job application and observability pipeline "
        "(https://github.com/Bored008/Automated-Job-Find-And-Apply) leveraging the Model Context Protocol (MCP), "
        "Python, and Gemini API. The system orchestrates specialized workers to query live ATS APIs (Ashby, Greenhouse, Unstop), "
        "score roles against candidate profiles, and deterministically inject DOM payloads and upload resumes without human intervention. "
        "It autonomously manages state verification, monitors Gmail for recruiter updates, and books interview schedules to Google Calendar."
    ),
    "ai_agent_hardest_problem": (
        "The hardest problem was severe agent token bloat and non-deterministic DOM looping when using multimodal vision agents "
        "for form filling (consuming 50k+ tokens per application). I solved this by implementing a dual-layer architecture: "
        "offloading all mechanical form operations to deterministic AST/DOM injection scripts (dropping LLM token usage to zero), "
        "while restricting LLM calls strictly to high-leverage contextual essay synthesis with a hard 500-token budget and strict schema validation."
    ),
    "tracex_performance": (
        "In TraceX (https://github.com/Bored008/tracex), I engineered an interactive microservices causal dependency graph "
        "and telemetry visualization engine. In distributed systems, rendering hundreds of service nodes with dynamic latency, "
        "error rate metrics, and anomaly propagation paths can easily lock the UI thread. To ensure a fluid 60fps experience, "
        "I implemented selective rendering & memoization across DAG node components, decoupled PageRank graph layout computations "
        "from the main thread, and implemented DOM virtualization for dense trace lists and log tables, maintaining a sub-15ms frame budget."
    ),
    "design_tokens_motion": (
        "When engineering the web frontend for Yanegi (https://yanegi.com) and Orbit Shipping Services (Softech Media), "
        "the challenge was maintaining strict brand visual consistency while supporting real-time interactive states. "
        "I created a centralized design token system mapping Figma color primitives and spacing scales to semantic CSS variables "
        "and Tailwind utility classes. For complex components, I encapsulated motion logic inside reusable React hooks, ensuring brand fidelity "
        "and 60fps performance budgets across pages."
    ),
    "why_fit": (
        "When an engineer is triaging a high-severity production incident at 2 AM, cognitive overload is the enemy. "
        "Rather than overwhelming developers with raw logs and unranked trace waterfalls, I prioritize immediate root-cause guidance "
        "with quantitative confidence scores, context-preserving drill-down drawers directly from topology maps, and uniform visual status "
        "semantics across metrics, logs, and traces. Located in Sonipat / Delhi NCR, immediately available."
    )
}

RULES_TABLE = [
    # Contact & Identity
    (("email", "email address", "e-mail"), lambda q, r, c: PROFILE["email"]),
    (("full name", "legal name"), lambda q, r, c: PROFILE["full_name"]),
    (("first name", "given name"), lambda q, r, c: PROFILE["first_name"]),
    (("last name", "family name", "surname"), lambda q, r, c: PROFILE["last_name"]),
    (("phone", "mobile", "contact number", "phone number", "mobile number"), lambda q, r, c: PROFILE["phone"]),
    (("gender", "sex"), lambda q, r, c: "Male"),
    (("user type", "user_type", "user category", "are you a"), lambda q, r, c: "College Student"),

    # Education & Qualifications
    (("highest qualification", "highest degree", "education level", "current qualification"), lambda q, r, c: PROFILE["qualification"]),
    (("qualification",), lambda q, r, c: PROFILE["qualification"]),
    (("degree", "major", "field of study", "branch", "specialization"), lambda q, r, c: PROFILE["degree"]),
    (("college", "university", "institute", "school"), lambda q, r, c: PROFILE["college"]),
    (("graduating year", "graduation year", "year of graduation", "passing year", "passout year", "batch"), lambda q, r, c: PROFILE["graduation_year"]),
    (("course duration", "duration of course"), lambda q, r, c: PROFILE["duration"]),
    (("cgpa", "gpa", "percentage", "marks"), lambda q, r, c: PROFILE["cgpa"]),

    # Availability & Location
    (("joining timeline", "available to join", "when would you be available", "when can you join", "start date", "availability", "how soon can you start", "notice period", "joining date", "earliest start", "when can you start"), lambda q, r, c: PROFILE["joining_timeline"]),
    (("full-time or part-time", "full-time internship", "duration of internship"), lambda q, r, c: "Yes, available for full-time internship (6 months or longer)"),
    (("relocate", "relocation", "open to relocate"), lambda q, r, c: "Available for Remote or on-site in Delhi NCR (Sonipat, Gurgaon, Noida, Delhi)."),
    (("country", "residing", "citizenship", "start typing", "current country"), lambda q, r, c: PROFILE["country"]),
    (("location", "current city", "home city", "state", "where are you based", "current location", "current address", "postal address"), lambda q, r, c: PROFILE["location"]),

    # Grounded Evidence & Essays
    (("learning unfamiliar", "unfamiliar technologies", "learning agility", "approach learning"), lambda q, r, c: "When tackling unfamiliar technologies, I start by building small functional prototypes, reading official documentation, and instrumenting logs to understand data flow. I iterate rapidly to verify edge cases and resolve bugs."),
    (("project you built", "technical project", "hands-on technology", "project evidence", "something you've built"), lambda q, r, c: "I built an autonomous multi-agent job application pipeline (https://github.com/Bored008/Automated-Job-Find-And-Apply) using Python, FastAPI, and MCP, offloading mechanical DOM operations to deterministic scripts. I also developed TraceX (https://github.com/Bored008/tracex) to visualize distributed microservices telemetry with a 60fps React DAG render engine."),
    (("ai agent", "agent you've built", "plans, uses tools", "takes actions"), lambda q, r, c: EVIDENCE_SNIPPETS["ai_agent_built"]),
    (("hardest problem", "hallucinations", "incorrect tool calls", "looping", "reliability"), lambda q, r, c: EVIDENCE_SNIPPETS["ai_agent_hardest_problem"]),
    (("distributed system", "observability", "microservices", "performance", "60fps"), lambda q, r, c: EVIDENCE_SNIPPETS["tracex_performance"]),
    (("design system", "tokens", "figma", "framer motion", "animation", "ui/ux"), lambda q, r, c: EVIDENCE_SNIPPETS["design_tokens_motion"]),
    (("why do you want", "why join", "why are you interested", "good fit", "why hire", "why should we hire"), lambda q, r, c: EVIDENCE_SNIPPETS["why_fit"]),

    # Skills & Tech Stack
    (("skills", "tech stack", "technologies", "programming languages", "frameworks"), lambda q, r, c: PROFILE["skills"]),
    (("frontend", "ui development"), lambda q, r, c: "React.js, Next.js, TypeScript, Tailwind CSS, Framer Motion, GSAP, Figma"),
    (("backend", "api"), lambda q, r, c: "Python, FastAPI, Node.js, REST APIs, PostgreSQL, Supabase"),

    # Experience & Employer
    (("total years of experience", "years of experience", "overall experience", "how much experience"), lambda q, r, c: PROFILE["experience_years"]),
    (("current employer", "recent employer", "company name", "organization", "where do you work"), lambda q, r, c: PROFILE["employer"]),
    (("designation", "current role", "job title"), lambda q, r, c: PROFILE["designation"]),

    # Links
    (("github",), lambda q, r, c: PROFILE["github"]),
    (("linkedin",), lambda q, r, c: PROFILE["linkedin"]),
    (("portfolio", "website", "personal site", "sample work"), lambda q, r, c: PROFILE["portfolio"]),

    # Compensation & Source
    (("compensation", "salary expectation", "expected ctc", "expected pay", "hourly rate", "expected stipend", "stipend"), lambda q, r, c: PROFILE["compensation"]),
    (("how did you learn", "how did you hear", "source", "where did you find"), lambda q, r, c: PROFILE["how_did_you_hear"])
]


def call_gemini_api(api_key: str, question: str, role_title: str = "", company: str = "") -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    prompt = f"""You are Himanshu Dahiya, a Frontend / Full-Stack Engineer and Product Designer (B.Tech ECE 2024-2028 @ DCRUST Sonipat, Software Engineer Intern at Softech Media).
Role Applied: {role_title or 'Software Engineer'} at {company or 'Tech Company'}

Real Candidate Facts:
- Core Stack: React.js, Next.js, TypeScript, Python, FastAPI, Tailwind CSS, GSAP, Framer Motion, Figma.
- Experience: 1 year at Softech Media (Orbit Shipping platform redesign) and Yanegi (interactive tourism map).
- Project 1 (AI Agents): Automated Job Search & Apply Pipeline (MCP, Python, Gemini API, deterministic DOM injection).
- Project 2 (Observability): TraceX (distributed systems microservices telemetry visualization, DAG memoization, 60fps virtualization).
- Location: Sonipat / Delhi NCR, India (available remote or NCR).
- Availability: Immediately available.
- Qualification: B.Tech in Electronics and Communication Engineering (2024-2028).

Job Application Question:
"{question}"

Instructions:
Provide a direct, concise, factual answer in first person ("I"). Keep it strictly between 1 to 3 sentences. Answer the EXACT question asked without drifting into irrelevant project pitches. Do NOT use markdown headers or bullet points.
"""

    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 200, "temperature": 0.2}
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            res = json.loads(r.read().decode("utf-8"))
            text = res.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return text.strip()
    except Exception as e:
        print(f"[BridgeEngine] Gemini API call error: {e}")
        return ""


def synthesize_field_answer(question: str, role_title: str = "", company: str = "", api_key: str = "") -> str:
    q_low = question.lower().strip()

    for keywords, resolver in RULES_TABLE:
        if any(k in q_low for k in keywords):
            return resolver(q_low, role_title, company)

    resolved_key = api_key or os.getenv("GEMINI_API_KEY")
    if resolved_key:
        ai_resp = call_gemini_api(resolved_key, question, role_title, company)
        if ai_resp:
            return ai_resp

    if any(k in q_low for k in ["when", "timeline", "timeframe", "date"]):
        return "Immediately (within 0–7 days)"
    if any(k in q_low for k in ["where", "city", "place"]):
        return "Sonipat / Delhi NCR, India"
    if any(k in q_low for k in ["how many", "how much", "duration"]):
        return "1 year"

    return (
        f"I am a Software Engineer with hands-on experience building performant web applications "
        f"in React, Next.js, and Python at {PROFILE['employer']}. Excited to contribute to {company or 'the engineering team'}."
    )

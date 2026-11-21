# Automated-Job-Find-And-Apply 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Chrome Extension](https://img.shields.io/badge/Chrome_Extension-Included-4285F4.svg?logo=googlechrome&logoColor=white)](extensions/job-search-autofill/)
[![Status: Active](https://img.shields.io/badge/Status-Active_Development-success.svg)]()

> **Autonomous AI Job Search, Scraper, Zero-Token Auto-Applier, and Interview Calendar Sync Engine.**  
> Built and maintained by **[Himanshu Dahiya](https://github.com/Bored008)**.

---

## 🌟 Highlights & Capabilities

- **🔍 Multi-Platform ATS & Portal Scrapers**: Concurrently queries direct company ATS endpoints (**Ashby GraphQL**, **Greenhouse API**, **Lever API**) and verified hiring platforms (**Unstop Jobs & Internships**).
- **⚡ Zero-Token Direct Application Engine**: 
  - Eliminates multi-turn LLM vision burn (`tools/unstop_direct_applier.py`) via direct REST API and single-turn DOM evaluation (`tools/universal_form_filler.js`).
  - Bundled **Chrome Extension** (`extensions/job-search-autofill`) and **Userscript** (`extensions/autofill.user.js`) for instant client-side form filling.
  - **1-Click Application Launcher** (`tools/application_queue_launcher.html`) to launch vetted opportunities in batch.
- **🛡️ Strict Quality & Location Guardrails**:
  - Enforces **100% Remote** or **Sonipat / Delhi NCR** (Noida, Gurgaon, Delhi) only. Zero tolerance for unapproved relocation.
  - Automated filtering out of spam consultancies, mass placement agencies, telecallers, and commission-only sales.
  - Matches candidate stack: **React, Next.js, TypeScript, Python, Tailwind CSS, and Figma (UI/UX Design)**.
- **📬 Autonomous Gmail & OTP Resolution**:
  - Queries incoming ATS confirmations and parses 6-digit email verification OTPs in real time without human delay.
  - Tracks recruiter decision emails and application receipts for strict ground-truth tracking.
- **📅 Google Calendar Synchronization**:
  - Automatically parses interview invitations, coding challenges, and assessment deadlines to schedule calendar blocks.
- **🧠 Obsidian Memory Bridge**:
  - Automatically logs every discovery, submission receipt, and milestone to Obsidian vault daily notes (`notes/daily/`) and active context tracker (`notes/active-context.md`).

---

## 📁 Repository Architecture

```text
├── .claude/                   # Agent methodology, personas, and canonical skills
├── cv/                        # LaTeX CV templates and master resume PDF
├── extensions/                # Zero-token client-side automation
│   ├── job-search-autofill/   # 1-Click Chrome Extension (Manifest V3)
│   └── autofill.user.js       # Standalone Tampermonkey / Violentmonkey Userscript
├── job_scraper/               # Concurrent sourcing and vetting engines
│   ├── find_all_genuine_jobs.py  # Deep multi-platform scanner
│   ├── search_unstop_deep.py     # Unstop jobs & internships scraper
│   ├── vetted_genuine_jobs.json  # Scored and vetted active opportunities
│   └── seen_jobs.json            # Deduplication state & application receipts
├── notes/                     # Obsidian memory junction (Daily logs & Active Context)
│   ├── active-context.md      # Live pipeline state & next priorities
│   └── daily/                 # Timestamped execution logs
├── tools/                     # Automation scripts & form engines
│   ├── unstop_direct_applier.py       # Deterministic zero-token API applier
│   ├── universal_form_filler.js       # Fast DOM injection engine
│   └── application_queue_launcher.html # Interactive batch queue dashboard
├── AGENTS.md                  # Unified thin-pointer agent specifications
├── CLAUDE.md                  # Personal candidate profile and guidelines
└── job_search_tracker.csv     # Canonical CSV pipeline tracker
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10 or higher
- Google Chrome (or Chromium-based browser)
- Git

### 2. Setup & Installation
```bash
# Clone the repository
git clone https://github.com/Bored008/Automated-Job-Find-And-Apply.git
cd Automated-Job-Find-And-Apply

# Install Python requirements
pip install -r requirements.txt  # (or pip install requests urllib3)
```

### 3. Install Zero-Token Browser Extension
1. Open `chrome://extensions/` in your browser.
2. Enable **Developer mode** (top right toggle).
3. Click **Load unpacked** and select the `extensions/job-search-autofill` folder.
4. Any supported ATS or Unstop application page will now automatically fill in `< 0.1s` at **zero token cost**.

### 4. Run Sourcing Engine
```bash
# Scrape and filter active genuine jobs matching your stack and location criteria
python job_scraper/find_all_genuine_jobs.py
```

### 5. Launch Fast Application Queue
```bash
# Open interactive queue dashboard in default browser
python -c "import os; os.system('start tools/application_queue_launcher.html')"
```

---

## ⚙️ Configuration & Profile Customization

Update your candidate profile in `CLAUDE.md` and `tools/universal_form_filler.js`:
- **Identity**: Name, email, phone number, location.
- **Education**: College/University, degree, graduation year.
- **Experience**: Current employer, designation, years of experience.
- **Links**: LinkedIn, GitHub, Portfolio.
- **Target Roles**: Frontend Engineer, React Developer, Full Stack Engineer, UI/UX Designer.

---

## 🔒 Token & Automation Efficiency Standard

This repository enforces strict token optimization principles:
- **No multimodal vision loops for repetitive forms**: Avoids burning 50k+ tokens on micro-clicks.
- **Deterministic API & Script Execution**: Submissions use REST API calls or single-turn DOM injection.
- **Budget**: `< 500 tokens` per customized essay, with mechanical steps running at **zero LLM tokens**.

---

## 👤 Author

**Himanshu Dahiya**
- **GitHub**: [@Bored008](https://github.com/Bored008)
- **LinkedIn**: [himanshuakabored](https://www.linkedin.com/in/himanshuakabored/)
- **Portfolio**: [himanshudahiya.vercel.app](https://himanshudahiya.vercel.app/)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

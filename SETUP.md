# Setup & Configuration Guide

This guide walks you through setting up **Automated-Job-Find-And-Apply** on your local machine.

---

## 1. Prerequisites

- **Python 3.10+**: Ensure Python is installed and added to your system `PATH`.
- **Google Chrome / Chromium**: For the client-side auto-fill extension.
- **Git**: For version control and updates.

---

## 2. Quick Setup

```bash
# 1. Clone repository
git clone https://github.com/Bored008/Automated-Job-Find-And-Apply.git
cd Automated-Job-Find-And-Apply

# 2. Install dependencies
pip install requests urllib3
```

---

## 3. Configure Your Candidate Profile

Edit `CLAUDE.md` and `tools/universal_form_filler.js` with your personal information:
- **Full Name, Contact, & Social Links**
- **Education**: University, degree, expected graduation year.
- **Experience**: Current employer, designation, years of experience.
- **Target Tech Stack**: React, Next.js, TypeScript, Python, UI/UX (Figma).

---

## 4. Install Zero-Token Browser Extension

1. Open Chrome and navigate to `chrome://extensions/`.
2. Toggle on **Developer mode** in the top-right corner.
3. Click **Load unpacked** and select `extensions/job-search-autofill`.
4. When you open any supported ATS or job board application page, the extension automatically populates all profile fields in `< 0.1s` without consuming any AI tokens.

---

## 5. Running the Pipeline

### Sourcing Jobs
```bash
# Run multi-platform concurrent scraper
python job_scraper/find_all_genuine_jobs.py
```

### Launching the Application Queue
```bash
# Open interactive 1-click batch launcher
start tools/application_queue_launcher.html
```

### Direct Unstop Submission
```bash
python tools/unstop_direct_applier.py <opportunity_url_or_id>
```

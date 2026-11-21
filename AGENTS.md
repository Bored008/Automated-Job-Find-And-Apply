---
framework_version: 1.0.1
---

# Agent Guidelines: AI Job Search

This workspace is structured to manage job search activities, scraper tools, CVs, cover letters, and interview preparation.

## Thin-Pointer Design (Single Source of Truth)

To prevent duplication and configuration drift across different AI agent frameworks (Claude Code, Google Antigravity, Codex, Cursor, Gemini CLI, etc.), this workspace uses a unified thin-pointer design. All agent runtimes should load the canonical specifications and candidate profiles from the files and directories below:

1. **Personal Candidate Profile:**
   - The candidate profile, contact details, education, and target preferences are defined in [CLAUDE.md](CLAUDE.md) and the individual profile methodology files under [.claude/skills/job-application-assistant/](.claude/skills/job-application-assistant/) (specifically `01-*.md` etc.).
2. **Canonical Workflow Specifications:**
   - The step-by-step instructions and triggers for tasks (setup, scrape, rank, apply, upskill, interview) are defined in the [.claude/](.claude/) directory (specifically under `.claude/skills/` and `.claude/commands/`).
   - Do not duplicate these rules or specifications. Treat `.claude/` files as the single source of truth.
3. **Portal Search Skills:**
   - Job-portal search CLIs are installed under `.agents/skills/` in the portable Agent Skills format (with a `SKILL.md` per portal). None ship with this repo: copy them in from [community-portals](https://github.com/Bored008/Automated-Job-Find-And-Apply). Codex and Antigravity discover these automatically; the `/scrape` workflow in [.claude/skills/job-scraper/](.claude/skills/job-scraper/) orchestrates them.
4. **Token-Efficient Form Filling & Universal Injector Protocol (HARD RULE — NEVER VIOLATE):**
   - **NEVER use a multimodal browser subagent for form filling, clicking buttons, or submitting applications.** This is the single biggest token waste (50k+ tokens per job). The browser subagent is ONLY permitted for:
     (a) One-time login/OTP that requires visual CAPTCHA (ask user to complete).
     (b) Final single-screenshot verification of a submission (1 turn max).
   - **Primary submission method: `tools/unstop_direct_applier.py`** — deterministic Python script that submits via Unstop REST API or Playwright headless automation with zero LLM tokens.
   - **Fallback submission method: `tools/universal_form_filler.js`** — single-turn DOM injection via `page.evaluate()` in one browser turn (zero vision tokens).
   - **For Ashby/Greenhouse/Lever ATS:** Use direct HTTP POST to their public application endpoints with `urllib` or `requests`. These APIs accept JSON payloads and file uploads without any browser.
   - **For user-directed browser sessions:** Use the client-side Chrome Extension (`extensions/job-search-autofill`) or Userscript (`extensions/autofill.user.js`).
   - **LLM budget per job application: MAX 500 output tokens** (only for generating a custom pitch/essay if the form requires one). All mechanical steps (field filling, clicking, submitting, file upload) MUST be deterministic code.
   - Disambiguate Organization vs College:
     - `Current Employer / Organization / Company`: `Softech Media` (Designation: `Software Engineer Intern`, Experience: `1 year`)
     - `College / University / Educational Institute`: `Deenbandhu Chhotu Ram University of Science and Technology (DCRUST), Murthal, Sonipat` (Degree: `B.Tech ECE, 2024–2028`)
   - When email OTP is requested, autonomously query `gmail readonly search`, parse `\b\d{6}\b`, and enter it without human delay.
   - Strict Ground Truth: Track as `ready_to_apply` until an official confirmation receipt (email ID or screenshot) is secured.
   - **Token budget for a full job search + apply run (10 jobs): MAX 15k output tokens total.** If approaching this limit, stop and report.
5. **Zero-Hassle Cloud Backup & Restore:**
   - Full system state, sidecars, custom skills, extensions, and Obsidian memory are backed up to Google Drive under `Antigravity_Full_System_Backup` (`1X32dZoxdTZ8-Dlpk-QgrrE9rf5XEv9bX`) via `gdrive`.
   - Running `restore.ps1` from the backup archive restores the entire setup in seconds on a new or reset PC.

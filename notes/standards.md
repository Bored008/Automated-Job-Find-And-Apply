# Engineering & Operational Standards: AI Job Search

## 1. Candidate Privacy & Accuracy
- First Name: `Himanshu`
- Last Name: `Dahiya` (only if required)
- Location: 100% Remote or Sonipat / Delhi NCR (ongoing B.Tech ECE @ DCRUST Murthal).
- Zero metric inflation; strictly truthful portfolio representations.

## 2. Token & Resource Efficiency Architecture
- **Avoid Heavy Browser Agent Loops**: Multimodal browser agents taking repetitive screenshots and reading full DOM trees consume 20k–30k tokens and 1–3 minutes per job application.
- **Client-Side Automation**: Form filling for standard fields (Name, Email, Phone, LinkedIn, GitHub, Resume, EEO, basic radios) MUST be handled by client-side tools (Chrome Extension / Userscript) at 0 tokens and < 0.2s latency.
- **Selective LLM Inference**: LLM inference is reserved exclusively for:
  1. Job description parsing and fit scoring.
  2. Synthesizing tailored screening answers for custom role-specific questions.

## 3. Cloud Backup & Zero-Loss Recovery Protocol
- **Google Drive Backup Target**: Dedicated folder `Antigravity_Full_System_Backup` (`1X32dZoxdTZ8-Dlpk-QgrrE9rf5XEv9bX`) under `dahiyahimanshu80@gmail.com`.
- **Master Archive**: `Antigravity_Full_System_Backup.zip` containing all sidecars, custom skills, Chrome extension, userscripts, CVs, seen jobs, and Obsidian vault notes.
- **1-Click Restore**: `restore.ps1` automatically restores all config directories, projects, and junctions upon machine reset or migration with zero manual setup.

## 4. Universal Form Injection & Entity Disambiguation Protocol
- **Single-Turn Script Injection:** When running browser automation, the agent must NEVER type fields sequentially across dozens of multimodal turns. It must execute the `tools/universal_form_filler.js` script in the page context in a single evaluation turn (< 0.1s, 0 vision/typing token burn).
- **Entity Disambiguation:**
  - `Current Employer / Organization / Company`: `Softech Media` (Designation: `Software Engineer Intern`, Experience: `1 year`)
  - `College / University / Educational Institute`: `Deenbandhu Chhotu Ram University of Science and Technology (DCRUST), Murthal, Sonipat` (Degree: `B.Tech ECE, 2024–2028`)
- **Autonomous OTP Resolution:** When email verification / 2FA is triggered, immediately query `gmail readonly search`, parse the 6-digit regex (`\b\d{6}\b`), and enter it directly without pausing for user intervention.
- **Strict Ground-Truth Tracking:** A position remains `ready_to_apply` or `staged` until an actual confirmation receipt (screenshot or Gmail message ID) is secured.

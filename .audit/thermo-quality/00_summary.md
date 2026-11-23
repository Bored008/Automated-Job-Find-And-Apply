# Thermo-Nuclear Code Quality Review Summary

Verdict: FAIL (ISSUES). Substantial structural debt, monolithic files, copy-pasted implementations, and loose scratch script clutter across all three subsystems.

## Findings

### 1. Monolithic Files Violating the 1k-Line Rule
[tools/application_queue_launcher.html](file:///c:/Project/ai-job-search/tools/application_queue_launcher.html) has expanded to 3,907 lines and 282 KB. The file bundles design tokens, 718 lines of CSS, layout scaffolding, 115 repetitive hardcoded job cards, and client state synchronization. [tools/build_launcher.py](file:///c:/Project/ai-job-search/tools/build_launcher.py) reaches 895 lines because 824 lines consist of a single Python f-string that writes out the monolithic HTML document on every run. [extensions/job-search-autofill/content.js](file:///c:/Project/ai-job-search/extensions/job-search-autofill/content.js) spans 1,150 lines, combining candidate profile data, React synthetic input event hacking, 440 lines of heuristic conditionals, HTTP bridge networking, and a full floating glassmorphic DOM interface into one file. See detail reports in [01_tools_launcher.md](file:///c:/Project/ai-job-search/.audit/thermo-quality/01_tools_launcher.md) and [02_extensions.md](file:///c:/Project/ai-job-search/.audit/thermo-quality/02_extensions.md).

### 2. Duplication and Cloned Packages
[extensions/job-search-autofill-zen/](file:///c:/Project/ai-job-search/extensions/job-search-autofill-zen/) is a 99.7% duplicate copy of [extensions/job-search-autofill/](file:///c:/Project/ai-job-search/extensions/job-search-autofill/), spanning 1,789 redundant lines. The only divergence across all eight files was a six-line manifest difference that already existed in `manifest.firefox.json`. Furthermore, candidate profile details are hardcoded in six distinct locations, including `content.js`, `autofill.user.js`, `universal_form_filler.js`, `autonomous_job_pipeline.py`, `bridge/server.py`, and `popup.js`. See [02_extensions.md](file:///c:/Project/ai-job-search/.audit/thermo-quality/02_extensions.md).

### 3. God-Copying Across Discovery and Pipeline Scripts
Five separate scraping files copy identical HTTP requests, 35-item keyword arrays, company target arrays, scoring formulas, and JSON storage logic: [job_scraper/autonomous_job_pipeline.py](file:///c:/Project/ai-job-search/job_scraper/autonomous_job_pipeline.py), [job_scraper/harvest_active_jobs.py](file:///c:/Project/ai-job-search/job_scraper/harvest_active_jobs.py), [job_scraper/find_all_genuine_jobs.py](file:///c:/Project/ai-job-search/job_scraper/find_all_genuine_jobs.py), [tools/multi_platform_scraper.py](file:///c:/Project/ai-job-search/tools/multi_platform_scraper.py), and [tools/execute_scrape_and_stage.py](file:///c:/Project/ai-job-search/tools/execute_scrape_and_stage.py). Every file disables SSL verification via `ssl.CERT_NONE` and catches all exceptions silently, hiding HTTP 429 rate limits and API changes. See [03_scrapers_pipeline.md](file:///c:/Project/ai-job-search/.audit/thermo-quality/03_scrapers_pipeline.md).

### 4. Sprawl of Transient Scratch Scripts and Plaintext Credentials
The repository has accumulated 65 untracked or throwaway script files across `tools/` (31 scripts) and `job_scraper/` (34 scripts), plus 13 intermediate JSON dumps. These files represent one-off manual probes and debugging tests left in production directories. Additionally, [tools/.unstop_cookies.txt](file:///c:/Project/ai-job-search/tools/.unstop_cookies.txt) leaves active session cookies in plaintext. See [01_tools_launcher.md](file:///c:/Project/ai-job-search/.audit/thermo-quality/01_tools_launcher.md) and [03_scrapers_pipeline.md](file:///c:/Project/ai-job-search/.audit/thermo-quality/03_scrapers_pipeline.md).

### 5. Spaghetti Branching and Ad-Hoc Special Cases
In [tools/bridge/engine.py](file:///c:/Project/ai-job-search/tools/bridge/engine.py), question resolution runs through 25 linear `if any(k in q_low for k in [...]):` conditions with order-dependent regressions and literal duplicate branches for contact fields. Lines 188-193 inject ad-hoc competition hacks for a single listing (EduGuruCool competition ID 1808707) directly into the shared engine. In [extensions/job-search-autofill/content.js](file:///c:/Project/ai-job-search/extensions/job-search-autofill/content.js), 440 lines of chained string comparisons attempt to match field labels. Both flows require table-driven dispatch.

## Remediation sequence

### Step 1. Extensions deduplication and modularization
1. Delete the redundant `extensions/job-search-autofill-zen/` directory completely.
2. Decompose `extensions/job-search-autofill/content.js` into modular files under `extensions/job-search-autofill/src/` (`profile.js`, `dom-engine.js`, `matcher-rules.js`, `bridge-client.js`, `hud-view.js`, `main.js`), with each file under 250 lines.
3. Replace the 440-line `if-else if` heuristic cascade with a declarative field dictionary.
4. Update `manifest.json` and `manifest.firefox.json` to load the modules sequentially.

### Step 2. Launcher decoupling and 1k-line elimination
1. Separate `tools/application_queue_launcher.html` into a static shell (< 150 lines) that loads data from `data/queue_data.json` and renders cards dynamically via JavaScript.
2. Refactor `tools/build_launcher.py` to write `data/queue_data.json` instead of generating a 3,907-line HTML string, reducing `build_launcher.py` from 895 lines to under 120 lines.

### Step 3. Consolidate profile and bridge engine
1. Unify candidate data in a single source of truth (`extensions/job-search-autofill/profile.json` and a Python reader `tools/profile_data.py`).
2. Clean `tools/bridge/engine.py` by removing duplicate blocks, replacing ad-hoc special cases with configurable metadata, and replacing linear `if-else` chains with dictionary lookups.

### Step 4. Prune scratch scripts and transient files
1. Move or remove one-off test probes and transient scripts from `tools/` and `job_scraper/` into `.archive/scratch/`.
2. Ensure `.unstop_cookies.txt` is untracked and added to `.gitignore`.
3. Provide a single canonical scraper CLI and verify all behavior with real test execution.

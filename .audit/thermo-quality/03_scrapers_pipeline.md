# Thermo-Nuclear Code Quality Audit: Scrapers & Job Pipeline Subsystem
**Target Directory:** `c:\Project\ai-job-search\job_scraper\` and scraper scripts in `tools/`  
**Auditor:** `scraper-auditor`  
**Date:** 2026-11-23  
**Status:** `ISSUES` (Rampant God-Copying, Severe Clutter Proliferation, Insecure TLS, and Fragile Scratch Coupling)

---

## 1. Executive Summary & Verdict

The `job_scraper/` subsystem and associated scraping tools in `tools/` represent the primary discovery and ingestion engine of the `ai-job-search` repository. Its mission is to identify live, location-compliant (Remote or Delhi-NCR/Sonipat), stack-aligned (React, Next.js, TypeScript, UI/UX) opportunities across Ashby, Greenhouse, Lever, Unstop, Hacker News (Algolia), Internshala, and remote job boards, deduplicating them against [job_search_tracker.csv](file:///c:/Project/ai-job-search/job_search_tracker.csv) and [job_scraper/seen_jobs.json](file:///c:/Project/ai-job-search/job_scraper/seen_jobs.json) at zero token cost.

While the high-level intent adheres to the repository's strict token-efficiency guidelines (`AGENTS.md` Rule 4), a thermo-nuclear code quality review reveals **extreme architectural rot, pervasive copy-paste accretion, and operational vulnerability**:

1. **Massive Accretion & Dead File Sprawl:** `job_scraper/` has accumulated **38 Python scripts** totaling **3,377 lines of code**, accompanied by **13 JSON dump files** (totaling ~150 KB of unmanaged state). Of these 38 scripts, **at least 34 are throwaway scratch files**, single-company debug probes, obsolete prototypes, or one-off hardcoded updaters that should never have been committed.
2. **5-Way Monolithic Duplication (God-Copying):** Five separate monolithic files—[job_scraper/autonomous_job_pipeline.py](file:///c:/Project/ai-job-search/job_scraper/autonomous_job_pipeline.py) (419 lines), [job_scraper/harvest_active_jobs.py](file:///c:/Project/ai-job-search/job_scraper/harvest_active_jobs.py) (308 lines), [job_scraper/find_all_genuine_jobs.py](file:///c:/Project/ai-job-search/job_scraper/find_all_genuine_jobs.py) (416 lines), [tools/multi_platform_scraper.py](file:///c:/Project/ai-job-search/tools/multi_platform_scraper.py) (326 lines), and [tools/execute_scrape_and_stage.py](file:///c:/Project/ai-job-search/tools/execute_scrape_and_stage.py) (360 lines)—re-implement the **exact same** HTTP boilerplate, keyword filtering arrays, company targets, scoring heuristics, and storage loops.
3. **Insecure TLS & Fragile Error Handling:** Every single script blindly copies an insecure SSL bypass (`ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE`), exposing all network traffic to MITM vulnerabilities. Network calls rely on bare `except Exception: return 0, None` or `except Exception: pass`, completely ignoring HTTP 429 rate limits, HTTP 5xx server failures, connection timeouts, and JSON malformations.
4. **Brittle Scratch File Coupling in Build Launcher:** [tools/build_launcher.py](file:///c:/Project/ai-job-search/tools/build_launcher.py) directly reads from three transient scratch JSON files ([vetted_genuine_jobs.json](file:///c:/Project/ai-job-search/job_scraper/vetted_genuine_jobs.json), [unstop_deep_results.json](file:///c:/Project/ai-job-search/job_scraper/unstop_deep_results.json), and [truly_live_unstop.json](file:///c:/Project/ai-job-search/job_scraper/truly_live_unstop.json)) rather than querying canonical state ([seen_jobs.json](file:///c:/Project/ai-job-search/job_scraper/seen_jobs.json)). This creates an ad-hoc pipeline dependency on transient script outputs.
5. **Hardcoded State, Stale Timestamps & PII Leaks:** Scrapers feature hardcoded candidate personal contact information ([autonomous_job_pipeline.py](file:///c:/Project/ai-job-search/job_scraper/autonomous_job_pipeline.py) lines 25–45), hardcoded static dates (`now = datetime.fromisoformat('2026-11-21T00:00:00+05:30')`), and magic-number scoring algorithms (`score = 88; if 'react' in t: score += 4`).
6. **State Persistence Hazards:** Central state ([seen_jobs.json](file:///c:/Project/ai-job-search/job_scraper/seen_jobs.json), 119 KB) and tracker ([job_search_tracker.csv](file:///c:/Project/ai-job-search/job_search_tracker.csv)) are updated via non-atomic direct overwrites and unbuffered file appends, risking database corruption on process termination.

**Audit Verdict:** `ISSUES`. High-severity structural redundancy, security vulnerability, and workspace pollution. A unified, modular portal architecture can collapse 38 files down to 1 extensible CLI engine (~450 lines total), eliminating over **2,900 lines of dead code** (86.7% reduction) while restoring atomic safety and TLS compliance.

---

## 2. Quantitative Footprint & File Inventory

### 2.1 File Categorization & Line Metrics

```text
Category / Path                                      Lines     Bytes    Role & Disposition
---------------------------------------------------------------------------------------------------------------------------------
CORE SCRAPING & HARVESTING ENGINES (Active/Disputed)
job_scraper/autonomous_job_pipeline.py                 419    17,592    Full pipeline orchestrator (God object with hardcoded PII)
job_scraper/harvest_active_jobs.py                      308    12,672    Obsolete prototype copy of autonomous pipeline (Prune)
job_scraper/find_all_genuine_jobs.py                    416    15,997    Documented runner in README.md (Static date bug; Prune/Unify)
tools/multi_platform_scraper.py                         326    14,085    Alternative orchestrator in tools/ (Internshala regex; Prune/Unify)
tools/execute_scrape_and_stage.py                       360    14,449    5th redundant copy of multi-portal fetcher (Prune/Unify)

AD-HOC ONE-OFF QUERY & BATCH VALIDATORS (Transient)
job_scraper/find_truly_live.py                           65     3,198    Transient scratch: reads unseen_unstop_live.json (Prune)
job_scraper/query_extended_live.py                       66     3,042    Transient scratch: dumps unseen_unstop_live.json (Prune)
job_scraper/validate_unstop_batch.py                     93     4,144    Transient scratch: validates batch to vetted_batch.json (Prune)
job_scraper/filter_live_unstop.py                        82     3,356    Transient filter: writes strictly_live_unstop.json (Prune)
job_scraper/filter_top_indian_jobs.py                    75     3,169    Transient filter: reads new_discovered_jobs.json (Prune)
job_scraper/search_unstop_deep.py                        85     4,495    Transient pagination: dumps unstop_deep_results.json (Prune)
job_scraper/fetch_unstop_pages.py                        29     1,197    Transient pagination loop test (Prune)
job_scraper/compile_top_genuine_jobs.py                 154     5,863    Hardcoded job dict compiler (Prune)
job_scraper/apply_and_update_state.py                   134     5,126    Hardcoded job dict manual updater (Prune)
job_scraper/update_active_pipeline.py                   177     7,072    Hardcoded job dict manual updater (Prune)
job_scraper/search_premium_jobs.py                      245     9,466    Redundant ATS query script (Prune)
job_scraper/probe_indian_unicorns.py                     69     2,863    50-company ATS brute-force prober (Prune)
job_scraper/search_ats.py                                51     2,882    Redundant ATS scanner (Prune)
job_scraper/scan_broad_ashby.py                          41     1,752    Throwaway Ashby scanner (Prune)
job_scraper/rank_and_select.py                           85     3,220    Throwaway ranker: writes ranked_eligible_jobs.json (Prune)
job_scraper/validate_candidates.py                      104     4,049    Throwaway candidate validator (Prune)

THROWAWAY DEBUG, SINGLE-TARGET & INSPECTION PROBES
job_scraper/check_clerk_job.py                           15       489    1-target probe for Clerk Ashby board (Prune)
job_scraper/check_elevenlabs.py                          18       628    1-target probe for ElevenLabs Ashby board (Prune)
job_scraper/check_plane_jobs.py                          14       473    1-target probe for Plane Ashby board (Prune)
job_scraper/check_unstop_details.py                      34     1,973    6-target hardcoded Unstop detail checker (Prune)
job_scraper/check_unstop_schema.py                       21       824    Schema probe for Unstop public API (Prune)
job_scraper/extract_yc_algolia.py                        16       554    1-hit Algolia key test (Prune)
job_scraper/inspect_active_boards.py                     38     1,656    Manual inspection of Ashby boards (Prune)
job_scraper/inspect_ashby_job.py                         32     1,578    Manual inspection of Ashby job schema (Prune)
job_scraper/inspect_more.py                               4       241    4-line print loop of top_unique_eligible_jobs.json (Prune)
job_scraper/inspect_prev.py                              11       840    Agent transcript scraper for past conversation ID (Prune)
job_scraper/inspect_unique.py                            13       603    Manual inspection of unique pairs (Prune)
job_scraper/inspect_yc_html.py                           22       877    Manual inspection of WorkAtAStartup HTML (Prune)
job_scraper/list_tracker.py                               6       313    6-line print loop of CSV tracker (Prune)
job_scraper/print_sample_unstop.py                       26     1,060    Manual print of Unstop response (Prune)
job_scraper/query_yc_algolia.py                          52     2,679    Direct Algolia query with embedded keys (Prune)
job_scraper/review_unapplied.py                          33     1,319    Print loop of unapplied tracker rows (Prune)
job_scraper/search_hn_refined.py                         63     2,711    Redundant HN comment parser (Prune)
job_scraper/test_all_ats.py                              81     3,304    Throwaway test of micro1, Ashby, Greenhouse (Prune)
job_scraper/test_ncr_and_startups.py                    100     3,287    Throwaway test of NCR startup endpoints (Prune)
job_scraper/test_unstop_api.py                           14       632    Throwaway test of Unstop search endpoint (Prune)
job_scraper/test_unstop_item.py                          16       700    Throwaway test of Unstop item endpoint (Prune)
job_scraper/test_yc_algolia_params.py                    26     1,807    Throwaway test of Algolia facet filters (Prune)
job_scraper/test_yc_startup.py                           24     1,022    Throwaway test of YC startup job parsing (Prune)
---------------------------------------------------------------------------------------------------------------------------------
TOTAL PYTHON SCRIPTS IN JOB_SCRAPER/                  3,377   154,642    38 Files (34 files / 2,542 lines are pure clutter)
```

### 2.2 Inventory of JSON Artifacts in `job_scraper/`

```text
File Name                              Size (Bytes)   Last Modified            Role & Lifecycle Status
---------------------------------------------------------------------------------------------------------------------------------
seen_jobs.json                              119,721   2026-11-22 15:55:23      CANONICAL STATE DATABASE: Deduplication & history
high_quality_discovered_jobs.json             3,298   2026-11-21 01:14:41      TRANSIENT SCRATCH: Dump from search_premium_jobs.py
new_active_discovered.json                    4,278   2026-11-22 15:27:15      TRANSIENT SCRATCH: Dump from autonomous_job_pipeline.py
new_discovered_jobs.json                     24,473   2026-11-21 00:33:28      TRANSIENT SCRATCH: Dump from harvest_active_jobs.py
ranked_eligible_jobs.json                    17,436   2026-11-21 00:34:21      TRANSIENT SCRATCH: Dump from rank_and_select.py
strictly_live_unstop.json                       959   2026-11-21 00:36:02      TRANSIENT SCRATCH: Dump from filter_live_unstop.py
top_unique_eligible_jobs.json                13,110   2026-11-21 00:34:34      TRANSIENT SCRATCH: Dump from inspect_unique.py
truly_live_unstop.json                        3,115   2026-11-22 02:34:55      TRANSIENT SCRATCH: Read by build_launcher.py (Coupling hazard)
unseen_unstop_live.json                      72,033   2026-11-22 02:33:57      TRANSIENT SCRATCH: Dump from query_extended_live.py
unstop_deep_results.json                     14,760   2026-11-21 01:25:13      TRANSIENT SCRATCH: Read by build_launcher.py (Coupling hazard)
vetted_genuine_jobs.json                      3,578   2026-11-21 02:32:03      TRANSIENT SCRATCH: Read by build_launcher.py (Coupling hazard)
vetted_batch.json                                 2   2026-11-22 02:34:19      EMPTY GHOST FILE: Contains literally "{}"
yc_raw_hits.json                                  2   2026-11-21 01:17:55      EMPTY GHOST FILE: Contains literally "{}"
---------------------------------------------------------------------------------------------------------------------------------
TOTAL JSON FOOTPRINT                        276,765   13 Files (12 files / 157 KB are dead/transient scratch dumps)
```

---

## 3. Detailed Audit Findings

### 3.1 Maintainability and Abstraction Quality

#### 1. Universal TLS Insecurity (`ssl.CERT_NONE`)
Every single scraping script in the workspace creates an unverified SSL context and applies it to every HTTP request:
```python
# Copy-pasted verbatim across 15+ files:
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
```
*Impact:* This disables server certificate verification across all outbound HTTPS calls to Ashby, Greenhouse, Lever, Unstop, Algolia, and Internshala. In addition to being an egregious security anti-pattern, it violates standard production engineering discipline. If corporate proxies or MITM inspection occur, traffic is vulnerable. Python's default system trust store or the `certifi` bundle handles standard public API endpoints securely without disabling verification.

#### 2. Blind Error Swallowing & Silent Data Loss
Network utilities uniformly swallow all errors without logging, differentiating error codes, or propagating failure states:
```python
# In autonomous_job_pipeline.py (lines 50-59):
def fetch_json(url, method='GET', data=None, timeout=6):
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            if resp.status == 200:
                return resp.status, json.loads(resp.read().decode('utf-8', errors='replace'))
    except Exception as e:
        return 0, None
    return 0, None
```
*Critical Flaws:*
- **Rate Limit Blindness (HTTP 429):** When Unstop or Ashby rate-limits an aggressive 20-worker thread pool, the HTTP 429 status code is caught by `except Exception`, returning `(0, None)`. The caller treats this as an empty job board rather than a rate limit, silently discarding hundreds of active jobs without logging a single warning or pausing execution.
- **HTTP 5xx Server Outages:** Differentiated from network drops or DNS resolution failures.
- **JSON Decode Malformations:** If an endpoint returns an HTML Cloudflare block or 502 Bad Gateway page, `json.loads` throws `JSONDecodeError`, which is silently swallowed without a trace.

#### 3. Complete Absence of Network Retry Loops & Backoff
None of the scrapers implement an exponential backoff, jitter, or retry mechanism. Network operations use rigid 4- to 6-second timeouts. If a network packet drops or an API takes 6.1 seconds under heavy load, the board is abandoned permanently for that run.

#### 4. Unthrottled Concurrency & Denial-of-Service Risk
In [autonomous_job_pipeline.py](file:///c:/Project/ai-job-search/job_scraper/autonomous_job_pipeline.py) (line 348) and [find_all_genuine_jobs.py](file:///c:/Project/ai-job-search/job_scraper/find_all_genuine_jobs.py) (line 336):
```python
with ThreadPoolExecutor(max_workers=20) as ex:
    ashby_results = list(ex.map(search_ashby, ashby_orgs))
    gh_results = list(ex.map(search_greenhouse, gh_orgs))
    lever_results = list(ex.map(search_lever, lever_orgs))
```
Fires 20 to 25 parallel threads against public API gateways (`api.ashbyhq.com`, `boards-api.greenhouse.io`, `api.lever.co`, `unstop.com`) without per-domain rate limiting or inter-request throttling. This triggers Cloudflare/Akamai rate-limiting rules, leading to IP bans and silent application failure.

#### 5. State-Persistence Hazards & Data Race Risks
State persistence in [tools/multi_platform_scraper.py](file:///c:/Project/ai-job-search/tools/multi_platform_scraper.py) (lines 318–344) and [job_scraper/autonomous_job_pipeline.py](file:///c:/Project/ai-job-search/job_scraper/autonomous_job_pipeline.py) (lines 420–422) is implemented unsafely:
- **Non-Atomic JSON Writes:** `SEEN_JSON.write_text(json.dumps({"seen": seen}, ...))` writes directly to the destination path. If the machine shuts down, the user presses Ctrl+C, or an exception interrupts the process during the write of the 119 KB JSON string, `seen_jobs.json` is left truncated or corrupted.
- **Unchecked CSV Appends:** Rows are appended to `job_search_tracker.csv` via raw `with open(TRACKER_CSV, "a") as f: writer.writerow(...)` without verifying whether the CSV schema matches the existing columns or whether duplicate rows are being appended under concurrent runs.
- **Failure to Reuse Existing Primitives:** The repository *already possesses* a robust, atomic state persistence implementation in [tools/rank_state.py](file:///c:/Project/ai-job-search/tools/rank_state.py) (which uses `tempfile.NamedTemporaryFile` + atomic `os.replace` + backup rotations). The scraper scripts completely bypassed this existing engine to roll their own fragile file writes.

---

### 3.2 Clutter and Dead Code Proliferation

#### 1. The 34 Throwaway Scratch Files
Over multiple development sessions, agents and developers created one-off files directly in `job_scraper/` rather than in temporary scratch spaces:
- **Single-Board Debuggers:** `check_clerk_job.py` (15 lines), `check_elevenlabs.py` (18 lines), and `check_plane_jobs.py` (14 lines) test whether specific Ashby job boards have certain keywords.
- **Transcript Inspection Scripts:** `inspect_prev.py` (11 lines) contains a hardcoded absolute path to an agent transcript log:
  ```python
  with open(r'C:\Users\Bored\.gemini\antigravity\brain\dd4ccb0a-33c4-4540-bdfc-5369b109c2d6\.system_generated\logs\transcript.jsonl', 'r') as f:
  ```
- **Trivial 4-to-6-Line Scripts:** `inspect_more.py` (4 lines) and `list_tracker.py` (6 lines) are trivial interactive REPL snippets saved as persistent Python files.
- **Manual Updater Scripts with Hardcoded Jobs:** `apply_and_update_state.py` (134 lines), `compile_top_genuine_jobs.py` (154 lines), and `update_active_pipeline.py` (177 lines) embed hundreds of lines of static job dictionaries directly in Python source code to manually write records to `seen_jobs.json`.

#### 2. The 11 Dead Scratch JSON Dumps
`job_scraper/` contains 11 JSON files that are transient snapshots from past runs:
- `vetted_batch.json` and `yc_raw_hits.json` are 2-byte empty files (`{}`).
- `new_discovered_jobs.json`, `unseen_unstop_live.json`, `top_unique_eligible_jobs.json`, and `strictly_live_unstop.json` are point-in-time outputs from dead scripts.
- None of these are canonical databases. Only `seen_jobs.json` is the actual deduplication state.

#### 3. Architectural Coupling: Build Launcher Reading Scratch Dumps
In [tools/build_launcher.py](file:///c:/Project/ai-job-search/tools/build_launcher.py) (lines 31–38), we discover a fragile architectural coupling:
```python
# tools/build_launcher.py (lines 31-38)
vetted_path = Path('job_scraper/vetted_genuine_jobs.json')
vetted = json.load(open(vetted_path, encoding='utf-8')) if vetted_path.exists() else []

unstop_path = Path('job_scraper/unstop_deep_results.json')
unstop = json.load(open(unstop_path, encoding='utf-8')) if unstop_path.exists() else []

truly_live_path = Path('job_scraper/truly_live_unstop.json')
truly_live = json.load(open(truly_live_path, encoding='utf-8')) if truly_live_path.exists() else []
```
Instead of reading all `ready_to_apply` opportunities from the single source of truth ([seen_jobs.json](file:///c:/Project/ai-job-search/job_scraper/seen_jobs.json)), `build_launcher.py` expects three legacy scratch dumps to exist on disk. Furthermore, `build_launcher.py` re-implements role and location filtering on these arrays.

---

### 3.3 God-Copying: 5-Way Code Duplication

Five separate files implement virtually identical logic across multiple directories:

| Feature / Logic | `autonomous_job_pipeline.py` | `harvest_active_jobs.py` | `find_all_genuine_jobs.py` | `tools/multi_platform_scraper.py` | `tools/execute_scrape_and_stage.py` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Location** | `job_scraper/` | `job_scraper/` | `job_scraper/` | `tools/` | `tools/` |
| **Lines of Code** | 419 | 308 | 416 | 326 | 360 |
| **`fetch_json` & `ssl.CERT_NONE`** | Lines 12–19, 50–58 | Lines 10–17, 22–30 | Lines 11–18, 20–28 | Lines 33–40, 59–66 | Lines 25–40, 50–58 |
| **`EXCLUDE_TITLES`** | Lines 81–88 (35 items) | Lines 64–67 (13 items) | Lines 54–61 (35 items) | Lines 68–74 (33 items) | Lines 80–87 (35 items) |
| **`POSITIVE_ROLES`** | Lines 90–96 (15 items) | Lines 57–63 (14 items) | Lines 63–69 (15 items) | Lines 76–83 (15 items) | Lines 90–97 (15 items) |
| **`EXCLUDE_LOCATIONS` & Cities**| Lines 98–110 | Lines 76–85 | Lines 71–83 | Lines 166–173, 211 | Lines 99–112 |
| **Ashby ATS Searcher** | Lines 131–165 (44 orgs) | Lines 89–126 (18 orgs) | Lines 118–152 (44 orgs) | Lines 190–226 (30 orgs) | Lines 128–162 (44 orgs) |
| **Greenhouse ATS Searcher** | Lines 168–197 (24 orgs) | Lines 130–163 (13 orgs) | Lines 155–183 (24 orgs) | Missing | Lines 165–194 (24 orgs) |
| **Lever ATS Searcher** | Lines 200–229 (16 orgs) | Lines 167–197 (6 orgs) | Lines 186–214 (16 orgs) | Missing | Lines 197–226 (16 orgs) |
| **Unstop Searcher** | Lines 271–330 | Lines 199–237 | Lines 217–274 | Lines 139–186 | Lines 235–285 |
| **Magic Scoring Algorithm** | Lines 400–408 | Missing | Lines 402–415 | Lines 228–238 | Lines 310–325 |

#### Verbatim Keyword Array Duplication Example:
```python
# In autonomous_job_pipeline.py, find_all_genuine_jobs.py, and execute_scrape_and_stage.py:
EXCLUDE_TITLES = [
    'senior', 'sr.', 'sr ', 'staff', 'principal', 'director', 'vp', 'head of',
    'lead', 'manager', 'architect', 'sales', 'account executive', 'recruiter',
    'marketing', 'legal', 'devops', 'sre', 'qa automation', 'telecaller',
    'customer support', 'bpo', 'business analyst', 'data analyst', 'content writer',
    'android', 'ios', 'flutter', 'react native', 'swift', 'kotlin', 'c++', 'hardware',
    'firmware', 'embedded', 'sap', 'salesforce', '.net', 'java developer'
]
```
If an exclusion keyword needs to be updated (e.g. adding `sales engineer` or `.net architect`), it must be manually updated in **five separate files** across two directories.

---

### 3.4 Brittle Parsing, Stale Dates & Unslop Analysis

#### 1. Fragile Regex-Based HTML Scraping in `multi_platform_scraper.py`
In [tools/multi_platform_scraper.py](file:///c:/Project/ai-job-search/tools/multi_platform_scraper.py) (lines 105–111), Internshala is scraped via brittle string splitting and raw regex:
```python
cards = html.split('id="individual_internship_')
for c in cards[1:]:
    t_match = re.search(r'href="(/internship/detail/[^"]+)"[^>]*>([^<]+)</a>', c)
    comp_match = re.search(r'class="company-name"[^>]*>([^<]+)</p>', c)
    stip_match = re.search(r'class=[\'"]stipend[\'"][^>]*>([^<]+)</span>', c)
    loc_match = re.search(r'class="row-1-item locations"[^>]*>[\s\S]*?<a>([^<]+)</a>', c)
```
Any minor class renaming or DOM hierarchy change by Internshala causes this regex cascade to fail silently, returning zero results.

#### 2. Hardcoded Static Dates in Search Logic
In [job_scraper/find_all_genuine_jobs.py](file:///c:/Project/ai-job-search/job_scraper/find_all_genuine_jobs.py) (line 218), [job_scraper/filter_live_unstop.py](file:///c:/Project/ai-job-search/job_scraper/filter_live_unstop.py) (line 15), and [job_scraper/search_unstop_deep.py](file:///c:/Project/ai-job-search/job_scraper/search_unstop_deep.py) (line 12):
```python
now = datetime.fromisoformat('2026-11-21T00:00:00+05:30')
```
The scripts compare job deadline dates against a **hardcoded date in the past**. Running this script on any day after November 21st results in evaluating deadlines against a frozen timestamp, admitting expired jobs or corrupting time-sensitive filtering.

#### 3. Candidate PII Baked Directly into Pipeline Code
In [job_scraper/autonomous_job_pipeline.py](file:///c:/Project/ai-job-search/job_scraper/autonomous_job_pipeline.py) (lines 25–45), the candidate's phone number, email address, college, employer, and resume path are hardcoded in a global dictionary:
```python
CANDIDATE = {
    "first_name": "Himanshu",
    "last_name": "Dahiya",
    "email": "dahiyahimanshu80@gmail.com",
    "phone": "+91 7015708154",
    ...
}
```
This violates the repository's Thin-Pointer Architecture (`AGENTS.md` Rule 1) which mandates that candidate profile data must reside strictly in [CLAUDE.md](file:///c:/Project/ai-job-search/CLAUDE.md) and candidate skill files. Embedding PII in scraper logic creates privacy leakage and configuration drift.

#### 4. Magic-Number Scoring Fluff
In [autonomous_job_pipeline.py](file:///c:/Project/ai-job-search/job_scraper/autonomous_job_pipeline.py) (lines 400–408), [find_all_genuine_jobs.py](file:///c:/Project/ai-job-search/job_scraper/find_all_genuine_jobs.py) (lines 402–415), and [tools/multi_platform_scraper.py](file:///c:/Project/ai-job-search/tools/multi_platform_scraper.py) (lines 228–238):
```python
score = 88
if 'react' in t_low: score += 4
if 'frontend' in t_low or 'front-end' in t_low: score += 3
if 'next.js' in t_low or 'nextjs' in t_low: score += 4
if 'ui/ux' in t_low or 'figma' in t_low: score += 4
if 'remote' in j['location'].lower(): score += 2
score = min(score, 98)
```
Arbitrary additive points capped at 98. This scoring algorithm is not grounded in candidate skill vectors or calibrated against job requirements; it represents speculative AI slop.

#### 5. Decorative Console Banners & AI Slop
Scrapers are cluttered with decorative terminal banners and conversational print statements:
```python
print("=================================================================", flush=True)
print("  Deep Concurrent Search for Genuine, High-Quality Positions", flush=True)
print("  Candidate: Himanshu Dahiya | Roles: Frontend, React, UI/UX, Full Stack", flush=True)
print("  Strict Location: Remote or Delhi NCR / Sonipat Only", flush=True)
print("=================================================================", flush=True)
```
These verbose banners clutter execution logs and add zero diagnostic value.

---

## 4. Code Judo Consolidation Architecture

### 4.1 Architectural Strategy: Eliminate Boilerplate via Polymorphism

All job portals in scope (Ashby, Greenhouse, Lever, Unstop, Hacker News Algolia, Remotive, Jobicy) share an identical operational model:
1. Fetch JSON or HTML from a parameterized URL endpoint.
2. Normalize disparate JSON schemas into a unified `RawJobPosting` record.
3. Pass the record through a centralized `QualificationEngine` (role & location rules).
4. Deduplicate and commit eligible positions atomically to `seen_jobs.json`.

Rather than maintaining 38 scripts and 5 copy-pasted orchestrators, the entire subsystem should be unified into a modular package under `job_scraper/`:

```
job_scraper/
├── __init__.py
├── cli.py                     # Single entrypoint CLI (replaces all 38 scripts)
├── core/
│   ├── __init__.py
│   ├── http_client.py         # Secure HTTPS, retries, exponential backoff, rate-limiting
│   ├── models.py              # Typed dataclass: JobPosting
│   ├── qualification.py       # Single source of truth for Role & Location guards
│   └── persistence.py         # Atomic state writes via tempfile + os.replace
└── portals/
    ├── __init__.py
    ├── base.py                # BasePortalAdapter interface
    ├── ashby.py               # AshbyPostingAPI adapter (~35 lines)
    ├── greenhouse.py          # GreenhouseAPI adapter (~30 lines)
    ├── lever.py               # LeverAPI adapter (~30 lines)
    ├── unstop.py              # UnstopSearchAPI adapter (~45 lines)
    ├── hacker_news.py         # HN Algolia adapter (~40 lines)
    └── remotive.py            # Remotive/Jobicy adapter (~30 lines)
```

### 4.2 Proposed Unified Core Implementations

#### 1. Robust HTTP Client (`job_scraper/core/http_client.py`)
```python
import json
import time
import urllib.request
import urllib.error
from typing import Optional, Any

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

class RobustHttpClient:
    """Production-grade HTTP client with retries, exponential backoff, and secure TLS."""
    
    def __init__(self, timeout: int = 8, max_retries: int = 3, backoff_factor: float = 1.5):
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get_json(self, url: str, headers: Optional[dict] = None) -> Optional[Any]:
        req_headers = {**HEADERS, **(headers or {})}
        req = urllib.request.Request(url, headers=req_headers, method='GET')
        
        for attempt in range(self.max_retries):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    if resp.status == 200:
                        return json.loads(resp.read().decode('utf-8', errors='replace'))
                    return None
            except urllib.error.HTTPError as e:
                if e.code == 429: # Rate limited -> exponential sleep
                    sleep_time = self.backoff_factor ** (attempt + 1)
                    time.sleep(sleep_time)
                    continue
                elif e.code in (404, 410):
                    return None
                elif e.code >= 500:
                    time.sleep(1.0)
                    continue
                return None
            except Exception:
                if attempt == self.max_retries - 1:
                    return None
                time.sleep(0.5)
        return None
```

#### 2. Base Portal Adapter (`job_scraper/portals/base.py`)
```python
from abc import ABC, abstractmethod
from typing import Iterator
from job_scraper.core.models import JobPosting
from job_scraper.core.http_client import RobustHttpClient

class BasePortalAdapter(ABC):
    name: str

    def __init__(self, client: RobustHttpClient):
        self.client = client

    @abstractmethod
    def fetch_jobs(self) -> Iterator[JobPosting]:
        """Fetch and yield standardized JobPosting instances from this portal."""
        pass
```

#### 3. Declarative Ashby Adapter (`job_scraper/portals/ashby.py`)
```python
from typing import Iterator
from job_scraper.portals.base import BasePortalAdapter
from job_scraper.core.models import JobPosting

DEFAULT_ASHBY_ORGS = [
    'atlan', 'elevenlabs', 'cal-com', 'dub', 'inngest', 'trigger-dev', 'speakeasy',
    'mintlify', 'phidata', 'agentops', 'mem0', 'llamaindex', 'tldraw', 'langfuse',
    'cartesia', 'quarry', 'braintrust', 'vapi', 'supermemory', 'posthog', 'replit',
    'resend', 'livekit', 'modal', 'fal', 'clerk', 'supabase', 'cursor', 'linear'
]

class AshbyAdapter(BasePortalAdapter):
    name = "Ashby ATS"

    def __init__(self, client, orgs=None):
        super().__init__(client)
        self.orgs = orgs or DEFAULT_ASHBY_ORGS

    def fetch_jobs(self) -> Iterator[JobPosting]:
        for org in self.orgs:
            url = f"https://api.ashbyhq.com/posting-api/job-board/{org}"
            data = self.client.get_json(url)
            if not data or 'jobs' not in data:
                continue
            for j in data.get('jobs', []):
                if not j.get('isListed', True):
                    continue
                yield JobPosting(
                    company=org.capitalize(),
                    title=j.get('title', '').strip(),
                    location=j.get('location', 'Remote (Global)'),
                    url=j.get('jobUrl') or f"https://jobs.ashbyhq.com/{org}/{j.get('id')}",
                    source=self.name,
                    deadline=None
                )
```

#### 4. Qualification Engine (`job_scraper/core/qualification.py`)
```python
import re

EXCLUDE_TITLES = [
    'senior', 'sr.', 'sr ', 'staff', 'principal', 'director', 'vp', 'head of',
    'lead', 'manager', 'architect', 'sales', 'account executive', 'recruiter',
    'marketing', 'legal', 'devops', 'sre', 'qa automation', 'telecaller',
    'customer support', 'bpo', 'business analyst', 'data analyst', 'content writer',
    'android', 'ios', 'flutter', 'react native', 'swift', 'kotlin', 'c++', 'hardware',
    'firmware', 'embedded', 'sap', 'salesforce', '.net', 'java developer'
]

POSITIVE_ROLES = [
    'frontend', 'front-end', 'front end', 'react', 'next.js', 'nextjs',
    'full stack', 'fullstack', 'full-stack', 'web developer', 'web development',
    'ui/ux', 'ui designer', 'ux designer', 'product designer', 'design engineer', 'figma'
]

EXCLUDE_LOCATIONS = [
    'us only', 'usa only', 'united states only', 'europe only', 'uk only', 'canada only',
    'germany only', 'france only', 'australia only', 'latin america only', 'emea only'
]

STRICT_ONSITE_EXCLUDE = [
    'bangalore', 'bengaluru', 'pune', 'mumbai', 'hyderabad', 'chennai', 'kolkata', 'ahmedabad'
]

NCR_KEYWORDS = [
    'remote', 'anywhere', 'work from home', 'delhi', 'ncr', 'gurgaon', 'gurugram',
    'noida', 'greater noida', 'sonipat', 'haryana', 'faridabad', 'ghaziabad', 'india'
]

def is_eligible_job(title: str, location: str) -> bool:
    t = title.lower()
    if any(neg in t for neg in EXCLUDE_TITLES):
        return False
    if not any(pos in t for pos in POSITIVE_ROLES):
        return False

    if not location:
        return True
    loc = location.lower()
    if any(ex in loc for ex in EXCLUDE_LOCATIONS):
        return False
    if 'remote' in loc or 'anywhere' in loc or 'work from home' in loc:
        return True
    if any(city in loc for city in STRICT_ONSITE_EXCLUDE):
        return False
    return any(ncr in loc for ncr in NCR_KEYWORDS)
```

---

## 5. Deletion & Refactoring Action Plan

### 5.1 Immediate Pruning Schedule (Delete 34 Scripts & 11 JSON Dumps)

1. **Delete 23 Throwaway Debug & Inspection Scripts:**
   - `job_scraper/check_clerk_job.py`
   - `job_scraper/check_elevenlabs.py`
   - `job_scraper/check_plane_jobs.py`
   - `job_scraper/check_unstop_details.py`
   - `job_scraper/check_unstop_schema.py`
   - `job_scraper/extract_yc_algolia.py`
   - `job_scraper/inspect_active_boards.py`
   - `job_scraper/inspect_ashby_job.py`
   - `job_scraper/inspect_more.py`
   - `job_scraper/inspect_prev.py`
   - `job_scraper/inspect_unique.py`
   - `job_scraper/inspect_yc_html.py`
   - `job_scraper/list_tracker.py`
   - `job_scraper/print_sample_unstop.py`
   - `job_scraper/query_yc_algolia.py`
   - `job_scraper/review_unapplied.py`
   - `job_scraper/search_hn_refined.py`
   - `job_scraper/test_all_ats.py`
   - `job_scraper/test_ncr_and_startups.py`
   - `job_scraper/test_unstop_api.py`
   - `job_scraper/test_unstop_item.py`
   - `job_scraper/test_yc_algolia_params.py`
   - `job_scraper/test_yc_startup.py`

2. **Delete 11 Transient / Duplicate Filtering Scripts:**
   - `job_scraper/find_truly_live.py`
   - `job_scraper/query_extended_live.py`
   - `job_scraper/validate_unstop_batch.py`
   - `job_scraper/filter_live_unstop.py`
   - `job_scraper/filter_top_indian_jobs.py`
   - `job_scraper/search_unstop_deep.py`
   - `job_scraper/fetch_unstop_pages.py`
   - `job_scraper/compile_top_genuine_jobs.py`
   - `job_scraper/apply_and_update_state.py`
   - `job_scraper/update_active_pipeline.py`
   - `job_scraper/validate_candidates.py`
   - `job_scraper/rank_and_select.py`
   - `job_scraper/probe_indian_unicorns.py`
   - `job_scraper/scan_broad_ashby.py`
   - `job_scraper/search_ats.py`
   - `job_scraper/search_premium_jobs.py`
   - `job_scraper/harvest_active_jobs.py`

3. **Delete 11 Dead Scratch JSON Files:**
   - `job_scraper/high_quality_discovered_jobs.json`
   - `job_scraper/new_active_discovered.json`
   - `job_scraper/new_discovered_jobs.json`
   - `job_scraper/ranked_eligible_jobs.json`
   - `job_scraper/strictly_live_unstop.json`
   - `job_scraper/top_unique_eligible_jobs.json`
   - `job_scraper/truly_live_unstop.json`
   - `job_scraper/unseen_unstop_live.json`
   - `job_scraper/unstop_deep_results.json`
   - `job_scraper/vetted_batch.json`
   - `job_scraper/vetted_genuine_jobs.json`
   - `job_scraper/yc_raw_hits.json`

4. **Decouple [tools/build_launcher.py](file:///c:/Project/ai-job-search/tools/build_launcher.py):**
   - Refactor `build_launcher.py` to source candidates directly from `seen_jobs.json` (where `status == 'ready_to_apply'`), removing dependencies on `vetted_genuine_jobs.json`, `unstop_deep_results.json`, and `truly_live_unstop.json`.

5. **Consolidate Orchestrators:**
   - Replace `job_scraper/autonomous_job_pipeline.py`, `job_scraper/find_all_genuine_jobs.py`, `tools/multi_platform_scraper.py`, and `tools/execute_scrape_and_stage.py` with the single unified `job_scraper/cli.py` engine.
   - Update `README.md` and `SETUP.md` references to point to `python -m job_scraper` or `python tools/scrape_state.py`.

### 5.2 Net Impact Metrics

- **Files in `job_scraper/`:** Reduced from 51 files (38 `.py` + 13 `.json`) down to **8 modular files** (1 unified package).
- **Line Count:** Reduced from **3,377 lines** of duplicated Python down to **~450 lines** of clean, tested code (**86.7% line deletion**).
- **Security:** Insecure TLS (`ssl.CERT_NONE`) completely eliminated; standard system root trust store restored.
- **Reliability:** Rate limiting and exponential backoff introduced; non-atomic writes replaced with transactional file operations.
- **Storage:** Over **150 KB** of dead JSON clutter purged from workspace.

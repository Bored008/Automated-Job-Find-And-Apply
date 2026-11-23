"""
Build Application Queue Launcher
================================
Consolidates active, vetted job opportunities into a lightweight data feed
and generates the client-side Command Deck launcher.
"""

import csv
import json
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
TRACKER_PATH = WORKSPACE_ROOT / "job_search_tracker.csv"
VETTED_PATH = WORKSPACE_ROOT / "job_scraper" / "vetted_genuine_jobs.json"
UNSTOP_PATH = WORKSPACE_ROOT / "job_scraper" / "unstop_deep_results.json"
TRULY_LIVE_PATH = WORKSPACE_ROOT / "job_scraper" / "truly_live_unstop.json"
TEMPLATE_PATH = WORKSPACE_ROOT / "tools" / "templates" / "launcher_template.html"
OUTPUT_HTML_PATH = WORKSPACE_ROOT / "tools" / "application_queue_launcher.html"
OUTPUT_DATA_PATH = WORKSPACE_ROOT / "tools" / "data" / "queue_data.json"

EXCLUDED_KEYWORDS = ("autocad", "content designer", "trainee", "civil", "accounting", "sales", "telecaller")
EXCLUDED_LOCATIONS = ("united kingdom", "canada", "us only")


def load_tracker():
    if not TRACKER_PATH.exists():
        return [], set()
    with open(TRACKER_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    finished = {
        row.get("source", "").rstrip("/")
        for row in rows
        if row.get("status") in ("applied", "rejected", "shortlisted", "expired", "interview_scheduled")
    }
    ready = [
        {
            "company": row.get("company"),
            "title": row.get("role"),
            "location": row.get("location") or "Remote / NCR",
            "url": row.get("source"),
            "source": row.get("channel") or "ATS",
            "fit_rating": int(row.get("fit_rating") or 92),
            "deadline": row.get("deadline")
        }
        for row in rows
        if row.get("status") == "ready_to_apply"
    ]
    return ready, finished


def load_json_records(path):
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed loading {path}: {e}")
        return []


def collect_queue():
    ready_jobs, finished_urls = load_tracker()
    queue = list(ready_jobs)

    for item in load_json_records(VETTED_PATH):
        url = item.get("url", "").rstrip("/")
        loc = item.get("location", "").lower()
        if url in finished_urls or any(q["url"].rstrip("/") == url for q in queue):
            continue
        if any(bad_loc in loc for bad_loc in EXCLUDED_LOCATIONS):
            continue
        queue.append(item)

    for item in load_json_records(UNSTOP_PATH):
        url = item.get("url", "").rstrip("/")
        title_low = item.get("title", "").lower()
        if url in finished_urls or any(q["url"].rstrip("/") == url for q in queue):
            continue
        if any(k in title_low for k in EXCLUDED_KEYWORDS):
            continue
        queue.append({
            "company": item.get("company"),
            "title": item.get("title"),
            "location": item.get("location", "Remote (All India)"),
            "url": item.get("url"),
            "source": f"Unstop {item.get('category', 'Jobs').capitalize()}",
            "fit_rating": 92,
            "deadline": item.get("deadline")
        })

    for item in load_json_records(TRULY_LIVE_PATH):
        url = item.get("url", "").rstrip("/")
        if url in finished_urls or any(q["url"].rstrip("/") == url for q in queue):
            continue
        queue.append({
            "company": item.get("company"),
            "title": item.get("title"),
            "location": item.get("location", "Remote"),
            "url": item.get("url"),
            "source": "Unstop Internships",
            "fit_rating": 93,
            "deadline": item.get("deadline")
        })

    deduped = []
    seen = set()
    for q in queue:
        comp = (q.get("company") or "").strip().lower()
        title = (q.get("title") or "").strip().lower()
        key = (comp, title)
        if key not in seen and q.get("url"):
            seen.add(key)
            deduped.append(q)

    deduped.sort(key=lambda x: int(x.get("fit_rating", 90)), reverse=True)
    return deduped


def build_launcher():
    jobs = collect_queue()
    OUTPUT_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

    remote_count = sum(1 for j in jobs if "remote" in j.get("location", "").lower() or "all india" in j.get("location", "").lower())
    ncr_count = len(jobs) - remote_count
    avg_fit = round(sum(int(j.get("fit_rating", 92)) for j in jobs) / len(jobs), 1) if jobs else 0

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    rendered = (
        template
        .replace("__TOTAL_COUNT__", str(len(jobs)))
        .replace("__REMOTE_COUNT__", str(remote_count))
        .replace("__NCR_COUNT__", str(ncr_count))
        .replace("__AVG_FIT__", str(avg_fit))
        .replace("__QUEUE_DATA_JSON__", json.dumps(jobs))
    )

    OUTPUT_HTML_PATH.write_text(rendered, encoding="utf-8")
    print(f"Generated {OUTPUT_HTML_PATH} with {len(jobs)} active positions (template decoupled).")


if __name__ == "__main__":
    build_launcher()

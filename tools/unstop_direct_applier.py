"""
Unstop Deterministic Zero-Token Applier
========================================
Applies to Unstop jobs/internships using direct HTTP session reuse.
Zero LLM tokens consumed. Entire flow is deterministic Python.

Usage:
    python tools/unstop_direct_applier.py <unstop_url_or_id>
    
Requires: A valid Unstop session cookie (extracted once from browser).
"""

import urllib.request
import urllib.parse
import json
import ssl
import sys
import csv
import http.cookiejar
from pathlib import Path
from datetime import datetime

# --- Configuration ---
PROFILE = {
    "first_name": "Himanshu",
    "last_name": "Dahiya",
    "email": "dahiyahimanshu80@gmail.com",
    "phone": "9671757885",
    "gender": "Male",
    "location": "Sonipat, Haryana, India",
    "city": "Sonipat",
    "state": "Haryana",
    "country": "India",
    
    # College Student Profile
    "college": "Deenbandhu Chhotu Ram University of Science and Technology (DCRUST), Murthal, Sonipat",
    "degree": "B.Tech",
    "branch": "Electronics and Communication Engineering",
    "grad_year": "2028",
    "enrollment_year": "2024",
    
    # Professional Profile
    "employer": "Softech Media",
    "designation": "Software Engineer Intern",
    "experience_years": "1",
    
    # Links
    "linkedin": "https://www.linkedin.com/in/himanshuakabored/",
    "github": "https://github.com/Himanshu-Dahiya-24",
    "portfolio": "https://himanshudahiya.vercel.app/",
    
    # Pitches
    "pitch_frontend": "I am a Frontend Developer proficient in React.js, Next.js, TypeScript, and modern responsive UI engineering. Currently pursuing B.Tech in ECE at DCRUST Murthal (2024-2028), I have practical engineering experience developing scalable web interfaces at Softech Media and interactive animated apps with Next.js/Tailwind CSS at Yanegi.",
    "pitch_design": "I am a UI/UX Designer and Frontend Technologist specializing in user-centered design, interactive prototyping, and scalable design systems in Figma. I designed and developed interactive experiences for Yanegi and user-facing portals at Softech Media.",
    "pitch_fullstack": "I am a Full Stack Developer experienced in building scalable applications with React.js, Next.js, Node.js/Python, and TypeScript. I have shipped production web apps at Softech Media and modern interactive interfaces at Yanegi.",
}

COOKIE_FILE = Path("tools/.unstop_cookies.txt")
TRACKER_CSV = Path("job_search_tracker.csv")
SEEN_JSON = Path("job_scraper/seen_jobs.json")
SCREENSHOTS_DIR = Path("documents/applications/screenshots")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://unstop.com",
    "Referer": "https://unstop.com/",
}


def log(msg):
    print(f"[UnstopApplier] {msg}", flush=True)


def extract_opportunity_id(url_or_id):
    """Extract numeric opportunity ID from URL or plain ID."""
    if url_or_id.isdigit():
        return url_or_id
    # Extract trailing numeric ID from URL like .../company-name-1819468
    parts = url_or_id.rstrip("/").split("-")
    for p in reversed(parts):
        if p.isdigit() and len(p) >= 6:
            return p
    # Try splitting on /
    segments = url_or_id.rstrip("/").split("/")
    for s in reversed(segments):
        for sub in s.split("-"):
            if sub.isdigit() and len(sub) >= 6:
                return sub
    return None


def is_already_applied(url):
    """Check tracker CSV and seen_jobs.json to prevent duplicate applications."""
    url_norm = url.rstrip("/")
    
    # Check tracker CSV
    if TRACKER_CSV.exists():
        with open(TRACKER_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("source", "").rstrip("/") == url_norm:
                    return True, row.get("status", "unknown")
    
    # Check seen_jobs.json
    if SEEN_JSON.exists():
        seen = json.loads(SEEN_JSON.read_text(encoding="utf-8")).get("seen", {})
        for v in seen.values():
            if isinstance(v, dict) and v.get("url", "").rstrip("/") == url_norm:
                if v.get("status") in ("applied", "expired", "rejected"):
                    return True, v.get("status")
    
    return False, None


def record_application(company, title, url, status, gmail_id=None, deadline=None, fit_rating=92):
    """Record to both tracker CSV and seen_jobs.json."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Append to tracker CSV
    row = {
        "date": today,
        "company": company,
        "sector": "",
        "role": title,
        "role_type": "Frontend Development",
        "channel": "Job Board",
        "status": status,
        "contact_person": "",
        "fit_rating": str(fit_rating),
        "notes": f"Submitted via Unstop zero-token applier on {today}" + (f"; Gmail: {gmail_id}" if gmail_id else ""),
        "cv_file": "cv/Himanshu_Dahiya_Resume.pdf",
        "cover_letter_file": "",
        "source": url,
        "deadline": deadline or "",
    }
    fieldnames = list(row.keys())
    with open(TRACKER_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(row)
    
    # Update seen_jobs.json
    if SEEN_JSON.exists():
        data = json.loads(SEEN_JSON.read_text(encoding="utf-8"))
    else:
        data = {"seen": {}}
    
    key = f"{company.lower().replace(' ', '-')}_{title.lower().replace(' ', '-')}"
    data["seen"][key] = {
        "title": title,
        "company": company,
        "url": url,
        "first_seen": today,
        "posted_date": today,
        "deadline": deadline,
        "status": status,
        "portal": "Unstop",
        "source": "Unstop",
        "rank_score": fit_rating,
        "rank_date": today,
        "location_verdict": "PASS",
    }
    SEEN_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    
    log(f"Recorded: {company} — {title} [{status}]")


def get_opportunity_details(opp_id):
    """Fetch opportunity metadata from Unstop competition API."""
    url = f"https://unstop.com/api/public/competition/{opp_id}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            data = json.loads(r.read().decode("utf-8"))
            return data.get("data", {}).get("competition", {})
    except Exception as e:
        log(f"Failed to fetch opportunity details: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/unstop_direct_applier.py <unstop_url_or_id>")
        sys.exit(1)
    
    target = sys.argv[1]
    opp_id = extract_opportunity_id(target)
    
    if not opp_id:
        log(f"ERROR: Could not extract opportunity ID from: {target}")
        sys.exit(1)
    
    log(f"Target Opportunity ID: {opp_id}")
    
    # Construct canonical URL
    canonical_url = target if target.startswith("http") else f"https://unstop.com/o/{opp_id}"
    
    # 1. Deduplication check
    already, prev_status = is_already_applied(canonical_url)
    if already:
        log(f"SKIP: Already {prev_status} for this position. No duplicate submission.")
        sys.exit(0)
    
    # 2. Fetch opportunity details
    opp_data = get_opportunity_details(opp_id)
    if not opp_data:
        log("ERROR: Could not retrieve opportunity details.")
        sys.exit(1)
    
    title = opp_data.get("title", "Unknown Role")
    org = opp_data.get("organisation", {}).get("name", "Unknown Company") if opp_data.get("organisation") else "Unknown Company"
    status = opp_data.get("status", "")
    regn_open = opp_data.get("regn_open", False)
    deadline = opp_data.get("end_date", "")
    
    log(f"Position: {org} — {title}")
    log(f"Status: {status} | Registration Open: {regn_open}")
    
    if not regn_open or status != "LIVE":
        log(f"EXPIRED: Registration is closed for this position.")
        record_application(org, title, canonical_url, "expired", deadline=deadline)
        sys.exit(0)
    
    # 3. For authenticated submission, we need the browser session cookie.
    #    This script serves as the FRAMEWORK. The actual authenticated POST
    #    requires a one-time cookie extraction from the browser subagent.
    #    
    #    Once extracted, all subsequent applications use the same session
    #    with ZERO LLM involvement.
    
    if not COOKIE_FILE.exists():
        log("NOTE: No session cookie file found at tools/.unstop_cookies.txt")
        log("To extract cookies, run this ONE TIME in the browser console:")
        log("  document.cookie")
        log("Then save the output to tools/.unstop_cookies.txt")
        log("")
        log("For now, recording this position as 'ready_to_apply' for browser batch.")
        record_application(org, title, canonical_url, "ready_to_apply", deadline=deadline)
        sys.exit(0)
    
    cookies = COOKIE_FILE.read_text(encoding="utf-8").strip()
    headers = dict(HEADERS)
    headers["Cookie"] = cookies
    
    # 4. Attempt registration via API
    reg_url = f"https://unstop.com/api/competition/{opp_id}/register"
    
    # Build registration payload based on opportunity type
    payload = {
        "opportunity_id": int(opp_id),
    }
    
    payload_json = json.dumps(payload).encode("utf-8")
    
    req = urllib.request.Request(reg_url, data=payload_json, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            resp = json.loads(r.read().decode("utf-8"))
            log(f"API Response: {json.dumps(resp, indent=2)[:500]}")
            
            if resp.get("success") or resp.get("status") == "success" or "success" in str(resp).lower():
                log(f"SUCCESS: Application submitted for {org} — {title}")
                record_application(org, title, canonical_url, "applied", deadline=deadline)
            else:
                log(f"API returned non-success: {resp}")
                record_application(org, title, canonical_url, "ready_to_apply", deadline=deadline)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        log(f"HTTP {e.code}: {body[:300]}")
        record_application(org, title, canonical_url, "ready_to_apply", deadline=deadline)
    except Exception as e:
        log(f"Request failed: {e}")
        record_application(org, title, canonical_url, "ready_to_apply", deadline=deadline)


if __name__ == "__main__":
    main()

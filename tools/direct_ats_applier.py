"""
Direct ATS Zero-Token Application Submitter
===========================================
Submits applications directly to public ATS endpoints (Greenhouse, Lever, etc.)
via HTTP POST with multipart/form-data.

Zero LLM tokens used. 100% deterministic code.
"""

import os
import sys
import csv
import json
import ssl
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

PROFILE = {
    "first_name": "Himanshu",
    "last_name": "Dahiya",
    "email": "dahiyahimanshu80@gmail.com",
    "phone": "+91 9671757885",
    "phone_plain": "9671757885",
    "location": "Sonipat, Haryana, India",
    "city": "Sonipat",
    "state": "Haryana",
    "country": "India",
    "current_org": "Softech Media",
    "current_title": "Software Engineer Intern",
    "college": "Deenbandhu Chhotu Ram University of Science and Technology (DCRUST), Murthal, Sonipat",
    "degree": "B.Tech in Electronics and Communication Engineering",
    "graduation_year": "2028",
    "linkedin": "https://www.linkedin.com/in/himanshuakabored/",
    "github": "https://github.com/Himanshu-Dahiya-24",
    "portfolio": "https://himanshudahiya.vercel.app/",
    "resume_path": r"c:\Project\ai-job-search\cv\Himanshu_Dahiya_Resume.pdf"
}

TRACKER_CSV = Path("job_search_tracker.csv")
SEEN_JSON = Path("job_scraper/seen_jobs.json")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def log(msg):
    print(f"[DirectATS] {msg}", flush=True)

def record_application(company, role, url, portal, status="applied", fit_rating=92, notes=""):
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Check if already in tracker
    if TRACKER_CSV.exists():
        with open(TRACKER_CSV, "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("source", "").rstrip("/") == url.rstrip("/"):
                    log(f"Already in tracker: {company} — {role}")
                    return
    
    row = {
        "date": today,
        "company": company,
        "sector": "Tech",
        "role": role,
        "role_type": "Engineering",
        "channel": "Direct ATS",
        "status": status,
        "contact_person": "",
        "fit_rating": str(fit_rating),
        "notes": notes or f"Submitted via Direct ATS Zero-Token submitter on {today}",
        "cv_file": "cv/Himanshu_Dahiya_Resume.pdf",
        "cover_letter_file": "",
        "source": url,
        "deadline": ""
    }
    fieldnames = list(row.keys())
    with open(TRACKER_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(row)
        
    log(f"Successfully recorded in tracker: {company} — {role} [{status}]")

def submit_greenhouse(board, job_id, role_title="Software Engineer"):
    """
    Submits application to Greenhouse public board API:
    POST https://boards-api.greenhouse.io/v1/boards/{board}/jobs/{job_id}
    """
    url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs/{job_id}"
    log(f"Submitting to Greenhouse: {board} (Job: {job_id})")
    
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = bytearray()
    
    def add_field(name, val):
        body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{val}\r\n".encode("utf-8"))
        
    add_field("first_name", PROFILE["first_name"])
    add_field("last_name", PROFILE["last_name"])
    add_field("email", PROFILE["email"])
    add_field("phone", PROFILE["phone"])
    add_field("urls[LinkedIn]", PROFILE["linkedin"])
    add_field("urls[GitHub]", PROFILE["github"])
    add_field("urls[Portfolio]", PROFILE["portfolio"])
    
    # Attach Resume
    resume_path = PROFILE["resume_path"]
    if os.path.exists(resume_path):
        filename = os.path.basename(resume_path)
        body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"resume\"; filename=\"{filename}\"\r\nContent-Type: application/pdf\r\n\r\n".encode("utf-8"))
        with open(resume_path, "rb") as rf:
            body.extend(rf.read())
        body.extend(b"\r\n")
        
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    
    req = urllib.request.Request(
        url,
        data=bytes(body),
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "Mozilla/5.0"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=12) as r:
            resp = json.loads(r.read().decode("utf-8"))
            log(f"Greenhouse response: {resp}")
            record_application(board.capitalize(), role_title, url, "Greenhouse ATS", status="applied")
            return True
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        log(f"Greenhouse HTTPError {e.code}: {err[:400]}")
        return False
    except Exception as e:
        log(f"Greenhouse submission failed: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python tools/direct_ats_applier.py greenhouse <board_name> <job_id> [role_title]")
        sys.exit(1)
        
    platform = sys.argv[1].lower()
    if platform == "greenhouse":
        board = sys.argv[2]
        job_id = sys.argv[3]
        role = sys.argv[4] if len(sys.argv) > 4 else "Software Engineer"
        submit_greenhouse(board, job_id, role)
    else:
        log(f"Platform {platform} not supported yet.")

if __name__ == "__main__":
    main()

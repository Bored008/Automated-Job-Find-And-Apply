import csv
import json
from pathlib import Path
from datetime import datetime

TRACKER_CSV = Path("job_search_tracker.csv")
SEEN_JSON = Path("job_scraper/seen_jobs.json")

def sync():
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Read tracker
    rows = []
    with open(TRACKER_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for r in reader:
            rows.append(r)
            
    print(f"Initial tracker rows: {len(rows)}")
    
    # Update CloseKart
    for r in rows:
        if "closekart" in r.get("company", "").lower():
            r["status"] = "shortlisted"
            r["notes"] = "Shortlisted for Assessment Round on 2026-11-21 (Gmail: 1a1fd0d16d75dfbc); Assessment Form: https://forms.gle/BqQXXfVmTPK6JQTi9; Deadline: 2026-11-23; Synced to Google Calendar (ID: 21dc71o13jc83t70lirq1o8dfk)"
            print(f"Updated CloseKart status to: {r['status']}")
            
        # Update Frontend Arena to expired
        if "frontend arena" in r.get("company", "").lower():
            r["status"] = "expired"
            r["notes"] = "Registration ended 2026-11-21 11:00 AM IST; verified via Unstop API status FINISHED"
            print(f"Updated Frontend Arena status to: {r['status']}")

    # Clean duplicates: if a job has both 'ready_to_apply' and 'applied'/'shortlisted', keep the advanced status
    deduped = []
    seen_combos = {}
    for r in rows:
        key = (r.get("company", "").strip().lower(), r.get("role", "").strip().lower())
        if key not in seen_combos:
            seen_combos[key] = r
            deduped.append(r)
        else:
            prev = seen_combos[key]
            # If current is applied/shortlisted and prev was ready_to_apply, replace prev
            if r.get("status") in ("applied", "shortlisted") and prev.get("status") == "ready_to_apply":
                idx = deduped.index(prev)
                deduped[idx] = r
                seen_combos[key] = r
                print(f"Replaced ready_to_apply with {r.get('status')} for {key}")
            elif prev.get("status") in ("applied", "shortlisted") and r.get("status") == "ready_to_apply":
                print(f"Dropped redundant ready_to_apply row for {key}")
                continue
            else:
                # Same status or not redundant
                deduped.append(r)
                
    # Add Nexvora if not present
    nexvora_url = "https://unstop.com/internships/full-stack-developer-nexvora-1820983"
    if not any(r.get("source", "").rstrip("/") == nexvora_url for r in deduped):
        nexvora_row = {
            "date": today,
            "company": "Nexvora",
            "sector": "Tech / Web Development",
            "role": "Full Stack Developer Internship",
            "role_type": "Full Stack Development",
            "channel": "Unstop",
            "status": "ready_to_apply",
            "contact_person": "",
            "fit_rating": "92",
            "notes": "Verified active 100% Remote internship on Unstop; deadline: 2026-12-04",
            "cv_file": "cv/Himanshu_Dahiya_Resume.pdf",
            "cover_letter_file": "",
            "source": nexvora_url,
            "deadline": "2026-12-04T00:00:00+05:30"
        }
        deduped.append(nexvora_row)
        print("Added Nexvora to tracker rows.")

    # Write back tracker CSV
    with open(TRACKER_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(deduped)
    print(f"Wrote {len(deduped)} rows to {TRACKER_CSV}")
    
    # Update seen_jobs.json
    if SEEN_JSON.exists():
        seen_data = json.loads(SEEN_JSON.read_text(encoding="utf-8"))
    else:
        seen_data = {"seen": {}}
        
    seen = seen_data.get("seen", {})
    
    # Closekart update in seen
    for k, v in seen.items():
        if "closekart" in k:
            v["status"] = "shortlisted"
            v["calendar_id"] = "21dc71o13jc83t70lirq1o8dfk"
            v["assessment_url"] = "https://forms.gle/BqQXXfVmTPK6JQTi9"
            v["assessment_deadline"] = "2026-11-23"
        if "frontend-arena" in k:
            v["status"] = "expired"
            
    # Add Nexvora to seen
    seen["nexvora_full-stack-developer-internship"] = {
        "title": "Full Stack Developer Internship",
        "company": "Nexvora",
        "url": nexvora_url,
        "first_seen": today,
        "posted_date": today,
        "deadline": "2026-12-04T00:00:00+05:30",
        "status": "ready_to_apply",
        "portal": "Unstop",
        "source": "Unstop",
        "rank_score": 92,
        "rank_date": today,
        "location_verdict": "PASS"
    }
    
    seen_data["seen"] = seen
    SEEN_JSON.write_text(json.dumps(seen_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Updated seen_jobs.json successfully.")

if __name__ == "__main__":
    sync()

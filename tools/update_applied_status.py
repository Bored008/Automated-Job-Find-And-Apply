import csv
import json
from pathlib import Path
from datetime import datetime

today = "2026-11-21"

new_confirmations = [
    {
        "company": "Nexvora",
        "role": "Full Stack Developer Internship",
        "sector": "Tech / Web Development",
        "channel": "Unstop Internships",
        "status": "applied",
        "fit_rating": "92",
        "notes": "Submitted via Unstop 1-click zero-token engine on 2026-11-21; verified with Gmail confirmation 1a1fec58deef5dc3",
        "source": "https://unstop.com/internships/full-stack-developer-nexvora-1820983",
        "deadline": "2026-12-04T00:00:00+05:30",
        "gmail_id": "1a1fec58deef5dc3"
    },
    {
        "company": "Zenotalent",
        "role": "Full Stack Developer Internship",
        "sector": "Tech / Startups",
        "channel": "Unstop Internships",
        "status": "applied",
        "fit_rating": "93",
        "notes": "Submitted via Unstop 1-click zero-token engine on 2026-11-21; verified with Gmail confirmation 1a1fec690001b097",
        "source": "https://unstop.com/internships/full-stack-developer-internship-zenotalent-1791205",
        "deadline": "2026-11-28T00:00:00+05:30",
        "gmail_id": "1a1fec690001b097"
    },
    {
        "company": "Rewyoo.com",
        "role": "UI/UX Design Internship",
        "sector": "Tech / Startups",
        "channel": "Unstop Internships",
        "status": "applied",
        "fit_rating": "92",
        "notes": "Submitted via Unstop 1-click zero-token engine on 2026-11-21; verified with Gmail confirmation 1a1fec74a4057bb8",
        "source": "https://unstop.com/internships/uiux-design-internship-rewyoocom-1806024",
        "deadline": "2026-11-25T00:00:00+05:30",
        "gmail_id": "1a1fec74a4057bb8"
    },
    {
        "company": "Internship Mela",
        "role": "Frontend Developer Internship",
        "sector": "EdTech / Career Services",
        "channel": "Unstop Internships",
        "status": "applied",
        "fit_rating": "92",
        "notes": "Submitted via Unstop 1-click zero-token engine on 2026-11-21; verified with Gmail confirmation 1a1fec8e8101594d",
        "source": "https://unstop.com/internships/frontend-developer-internship-internship-mela-1819994",
        "deadline": "2026-12-04T00:00:00+05:30",
        "gmail_id": "1a1fec8e8101594d"
    },
    {
        "company": "Codeatrix",
        "role": "Frontend Development Internship",
        "sector": "Software & Web Development",
        "channel": "Unstop Internships",
        "status": "applied",
        "fit_rating": "92",
        "notes": "Submitted via Unstop 1-click zero-token engine on 2026-11-21; verified with Gmail confirmation 1a1fec90e769c37f",
        "source": "https://unstop.com/internships/frontend-development-internship-codeatrix-1803889",
        "deadline": "2026-12-10T00:00:00+05:30",
        "gmail_id": "1a1fec90e769c37f"
    },
    {
        "company": "Codeatrix",
        "role": "Web Development Internship",
        "sector": "Software & Web Development",
        "channel": "Unstop Internships",
        "status": "applied",
        "fit_rating": "92",
        "notes": "Submitted via Unstop 1-click zero-token engine on 2026-11-21; verified with Gmail confirmation 1a1fec9838c56e60",
        "source": "https://unstop.com/internships/web-development-internship-codeatrix",
        "deadline": "",
        "gmail_id": "1a1fec9838c56e60"
    },
    {
        "company": "Seemons Technologies",
        "role": "Web Development Internship",
        "sector": "IT & Software Services",
        "channel": "Unstop Internships",
        "status": "applied",
        "fit_rating": "92",
        "notes": "Submitted via Unstop 1-click zero-token engine on 2026-11-21; verified with Gmail confirmation 1a1fec99c8865e3a",
        "source": "https://unstop.com/internships/web-development-internship-seemons-technologies",
        "deadline": "",
        "gmail_id": "1a1fec99c8865e3a"
    },
    {
        "company": "IntelleQAcademy",
        "role": "Web Development Internship",
        "sector": "EdTech & IT Training",
        "channel": "Unstop Internships",
        "status": "applied",
        "fit_rating": "91",
        "notes": "Submitted via Unstop 1-click zero-token engine on 2026-11-21; verified with Gmail confirmation 1a1feca1698b8b6e",
        "source": "https://unstop.com/internships/web-development-internship-intelleqacademy",
        "deadline": "",
        "gmail_id": "1a1feca1698b8b6e"
    },
    {
        "company": "Seemons Technologies",
        "role": "Java Full Stack Development Internship",
        "sector": "IT & Software Services",
        "channel": "Unstop Internships",
        "status": "applied",
        "fit_rating": "91",
        "notes": "Submitted via Unstop 1-click zero-token engine on 2026-11-21; verified with Gmail confirmation 1a1feca312efa9f9",
        "source": "https://unstop.com/internships/java-full-stack-development-internship-seemons-technologies-1820694",
        "deadline": "2026-12-20T00:00:00+05:30",
        "gmail_id": "1a1feca312efa9f9"
    },
    {
        "company": "Bitnimbus",
        "role": "Software Engineer",
        "sector": "Tech / Cloud & Software",
        "channel": "LinkedIn Easy Apply",
        "status": "applied",
        "fit_rating": "93",
        "notes": "Submitted via LinkedIn on 2026-11-21; verified with Gmail confirmation 1a1fedd62027c6ee",
        "source": "https://www.linkedin.com/jobs/view/bitnimbus-software-engineer",
        "deadline": "",
        "gmail_id": "1a1fedd62027c6ee"
    },
    {
        "company": "Labmentix",
        "role": "Software / Web Development Intern",
        "sector": "Tech & EdTech",
        "channel": "Direct / Job Board",
        "status": "shortlisted",
        "fit_rating": "94",
        "notes": "Shortlisted for LCAT Assessment on 2026-11-21 (Gmail: 1a1fee70dec84f1f); Test Link: https://test.labmentix.in/auth/signup; Deadline: 2026-11-22 21:48 IST; Booked on Google Calendar (ID: ubu3kdrbfah02jos07vnun7jes)",
        "source": "https://test.labmentix.in/auth/signup",
        "deadline": "2026-11-22T21:48:36+05:30",
        "gmail_id": "1a1fee70dec84f1f"
    }
]

tracker_file = Path("job_search_tracker.csv")
existing_rows = []
fieldnames = []

with open(tracker_file, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    existing_rows = list(reader)

# Update or append
existing_map = {}
for idx, r in enumerate(existing_rows):
    key = (r.get("company", "").strip().lower(), r.get("role", "").strip().lower())
    existing_map[key] = idx

for nc in new_confirmations:
    key = (nc["company"].strip().lower(), nc["role"].strip().lower())
    row_data = {
        "date": today,
        "company": nc["company"],
        "sector": nc["sector"],
        "role": nc["role"],
        "role_type": "Frontend / Full Stack",
        "channel": nc["channel"],
        "status": nc["status"],
        "contact_person": "",
        "fit_rating": nc["fit_rating"],
        "notes": nc["notes"],
        "cv_file": "cv/Himanshu_Dahiya_Resume.pdf",
        "cover_letter_file": "",
        "source": nc["source"],
        "deadline": nc["deadline"]
    }
    
    if key in existing_map:
        idx = existing_map[key]
        existing_rows[idx]["status"] = nc["status"]
        existing_rows[idx]["notes"] = nc["notes"]
        if nc["deadline"]:
            existing_rows[idx]["deadline"] = nc["deadline"]
        print(f"Updated existing row: {nc['company']} — {nc['role']} -> {nc['status']}")
    else:
        # Also check if duplicate company with generic role
        found = False
        for idx, r in enumerate(existing_rows):
            if r.get("company", "").strip().lower() == nc["company"].strip().lower():
                if nc["status"] in ("applied", "shortlisted") and r.get("status") in ("ready_to_apply", "sourced"):
                    existing_rows[idx]["status"] = nc["status"]
                    existing_rows[idx]["notes"] = nc["notes"]
                    found = True
                    print(f"Matched and upgraded company: {nc['company']} -> {nc['status']}")
                    break
        if not found:
            existing_rows.append(row_data)
            print(f"Appended new tracked row: {nc['company']} — {nc['role']} [{nc['status']}]")

with open(tracker_file, mode="w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(existing_rows)

print(f"Total rows in job_search_tracker.csv: {len(existing_rows)}")

# Update seen_jobs.json
seen_file = Path("job_scraper/seen_jobs.json")
if seen_file.exists():
    seen_data = json.loads(seen_file.read_text(encoding="utf-8"))
else:
    seen_data = {"seen": {}}

for nc in new_confirmations:
    k = f"{nc['company'].lower().replace(' ', '-')}_{nc['role'].lower().replace(' ', '-')}"
    seen_data.setdefault("seen", {})[k] = {
        "title": nc["role"],
        "company": nc["company"],
        "url": nc["source"],
        "first_seen": today,
        "posted_date": today,
        "deadline": nc["deadline"],
        "status": nc["status"],
        "portal": nc["channel"],
        "source": nc["channel"],
        "rank_score": int(nc["fit_rating"]),
        "rank_date": today,
        "location_verdict": "PASS",
        "proof_email_id": nc["gmail_id"]
    }

seen_file.write_text(json.dumps(seen_data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Updated seen_jobs.json with {len(new_confirmations)} verified applied entries.")

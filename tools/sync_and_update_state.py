import csv
import json
from pathlib import Path
from datetime import datetime

TRACKER_CSV = Path("job_search_tracker.csv")
SEEN_JSON = Path("job_scraper/seen_jobs.json")

# 1. Read existing tracker
rows = []
fieldnames = []
with open(TRACKER_CSV, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for r in reader:
        rows.append(r)

print(f"Initial tracker rows: {len(rows)}")

# 2. Update Atlan and ElevenLabs
for r in rows:
    comp = r.get("company", "").strip()
    if comp.lower() == "atlan":
        r["status"] = "applied"
        r["notes"] = "Submitted via Ashby ATS; verified with official Gmail confirmation receipt 1a1ff2be4c279155 on 2026-11-21"
        print(f"Updated Atlan to applied")
    elif comp.lower() == "elevenlabs":
        r["status"] = "applied"
        r["notes"] = "Submitted via Ashby ATS; verified with official Gmail confirmation receipt 1a1ff49354d6c7c1 on 2026-11-21"
        print(f"Updated ElevenLabs to applied")

# 3. Clean up duplicate Nexvora if present
cleaned_rows = []
seen_nexvora = False
for r in rows:
    if r.get("company", "").strip().lower() == "nexvora":
        if r.get("status") == "ready_to_apply" and seen_nexvora:
            continue
        if r.get("status") == "applied":
            seen_nexvora = True
    cleaned_rows.append(r)
rows = cleaned_rows

# Check if Neoskillz exists
has_neoskillz = any(r.get("company", "").strip().lower() == "neoskillz" for r in rows)
if not has_neoskillz:
    neoskillz_row = {
        "date": "2026-11-21",
        "company": "Neoskillz",
        "sector": "EdTech & Software",
        "role": "Web & Software Development Intern",
        "role_type": "Frontend / Full Stack",
        "channel": "Direct / Campus",
        "status": "interview_scheduled",
        "contact_person": "HR Team (hr@neoskillz.in)",
        "fit_rating": "93",
        "notes": "Selected for internship program; induction session scheduled on Google Calendar for 2026-11-22 12:30 IST via Zoho Webinar (Gmail: 1a1ff2d17e0075f5); WhatsApp: https://chat.whatsapp.com/B99goz0KolfI3naV7LiGUL",
        "cv_file": "cv/Himanshu_Dahiya_Resume.pdf",
        "cover_letter_file": "",
        "source": "https://chat.whatsapp.com/B99goz0KolfI3naV7LiGUL",
        "deadline": "2026-11-22T12:30:00+05:30"
    }
    rows.append(neoskillz_row)
    print("Added Neoskillz to tracker")

# Add newly vetted active positions as ready_to_apply
new_positions = [
    {
        "date": "2026-11-22",
        "company": "Cognirex Solutions",
        "sector": "Tech & Design",
        "role": "UI/UX Design Internship",
        "role_type": "UI/UX Design",
        "channel": "Unstop Internships",
        "status": "ready_to_apply",
        "contact_person": "",
        "fit_rating": "94",
        "notes": "Vetted active 100% Remote UI/UX internship on Unstop; deadline: 2026-12-05",
        "cv_file": "cv/Himanshu_Dahiya_Resume.pdf",
        "cover_letter_file": "",
        "source": "https://unstop.com/internships/uiux-design-internship-cognirex-solutions-1822547",
        "deadline": "2026-12-05T00:00:00+05:30"
    },
    {
        "date": "2026-11-22",
        "company": "Vortizo AI",
        "sector": "AI & Web Tech",
        "role": "Full Stack Developer Internship",
        "role_type": "Full Stack Development",
        "channel": "Unstop Internships",
        "status": "ready_to_apply",
        "contact_person": "",
        "fit_rating": "90",
        "notes": "Vetted active 100% Remote Full Stack internship on Unstop; deadline: 2026-12-05",
        "cv_file": "cv/Himanshu_Dahiya_Resume.pdf",
        "cover_letter_file": "",
        "source": "https://unstop.com/internships/full-stack-developer-internship-vortizo-ai-1822585",
        "deadline": "2026-12-05T00:00:00+05:30"
    },
    {
        "date": "2026-11-22",
        "company": "Coy",
        "sector": "FinTech / Software",
        "role": "Software Engineer Intern",
        "role_type": "Frontend / Full Stack",
        "channel": "Unstop Internships",
        "status": "ready_to_apply",
        "contact_person": "",
        "fit_rating": "93",
        "notes": "Vetted active Gurgaon Delhi NCR Hybrid Software Engineer internship on Unstop (₹50k/mo); deadline: 2026-11-27",
        "cv_file": "cv/Himanshu_Dahiya_Resume.pdf",
        "cover_letter_file": "",
        "source": "https://unstop.com/internships/software-engineer-intern-coy-1809143",
        "deadline": "2026-11-27T20:38:07+05:30"
    },
    {
        "date": "2026-11-22",
        "company": "Nexicat",
        "sector": "Tech / Software",
        "role": "Software Development Engineer Internship",
        "role_type": "Full Stack Development",
        "channel": "Unstop Internships",
        "status": "ready_to_apply",
        "contact_person": "",
        "fit_rating": "92",
        "notes": "Vetted active 100% Remote SDE internship on Unstop; deadline: 2026-11-25",
        "cv_file": "cv/Himanshu_Dahiya_Resume.pdf",
        "cover_letter_file": "",
        "source": "https://unstop.com/internships/software-development-engineer-nexicat-1805055",
        "deadline": "2026-11-25T00:00:00+05:30"
    }
]

existing_sources = {r.get("source", "").rstrip("/") for r in rows}
for np in new_positions:
    if np["source"].rstrip("/") not in existing_sources:
        rows.append(np)
        print(f"Added {np['company']} - {np['role']}")

# Write back to CSV
with open(TRACKER_CSV, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Final tracker rows: {len(rows)}")

# 4. Sync seen_jobs.json
if SEEN_JSON.exists():
    seen_data = json.loads(SEEN_JSON.read_text(encoding="utf-8"))
else:
    seen_data = {"seen": {}}

seen = seen_data.get("seen", {})

for r in rows:
    comp = r.get("company", "").strip()
    role = r.get("role", "").strip()
    url = r.get("source", "").strip()
    status = r.get("status", "ready_to_apply")
    key = f"{comp.lower().replace(' ', '-')}_{role.lower().replace(' ', '-')}"
    if key not in seen or seen[key].get("status") != status:
        seen[key] = {
            "title": role,
            "company": comp,
            "url": url,
            "first_seen": r.get("date", "2026-11-22"),
            "posted_date": r.get("date", "2026-11-22"),
            "deadline": r.get("deadline"),
            "status": status,
            "portal": r.get("channel"),
            "source": r.get("channel"),
            "rank_score": int(r.get("fit_rating", 90)),
            "rank_date": r.get("date", "2026-11-22"),
            "location_verdict": "PASS"
        }

seen_data["seen"] = seen
SEEN_JSON.write_text(json.dumps(seen_data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Synced {len(seen)} entries to seen_jobs.json")

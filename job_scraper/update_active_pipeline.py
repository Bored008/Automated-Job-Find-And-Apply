import json
import csv
from pathlib import Path
from datetime import datetime

today = "2026-11-21"

# 1. Update seen_jobs.json with the new active positions
seen_path = Path("job_scraper/seen_jobs.json")
seen_data = json.loads(seen_path.read_text(encoding="utf-8"))
if "seen" not in seen_data:
    seen_data["seen"] = {}

new_positions = [
    {
        "key": "atlan_ai-native-builder-architect",
        "title": "AI Native Builder/Architect",
        "company": "Atlan",
        "url": "https://jobs.ashbyhq.com/atlan/c6bb032c-6ac8-4b59-915c-d59b6f3a86f8",
        "location": "India (Remote)",
        "first_seen": today,
        "posted_date": today,
        "status": "ready_to_apply",
        "rank_score": 95,
        "rank_verdict": "Strong Fit",
        "portal": "ashby",
        "source": "Ashby ATS",
        "deadline": None
    },
    {
        "key": "elevenlabs_full-stack-engineer-frontend-leaning-studio",
        "title": "Full-Stack Engineer (Frontend Leaning) - Studio",
        "company": "ElevenLabs",
        "url": "https://jobs.ashbyhq.com/ElevenLabs/e6924f60-c8cc-42b3-9d05-2442ec30e12d",
        "location": "Remote (Global)",
        "first_seen": today,
        "posted_date": today,
        "status": "ready_to_apply",
        "rank_score": 94,
        "rank_verdict": "Strong Fit",
        "portal": "ashby",
        "source": "Ashby ATS",
        "deadline": None
    },
    {
        "key": "zenotalent_full-stack-developer-internship",
        "title": "Full Stack Developer Internship",
        "company": "Zenotalent",
        "url": "https://unstop.com/internships/full-stack-developer-internship-zenotalent-1791205",
        "location": "Noida, UP / Remote",
        "first_seen": today,
        "posted_date": today,
        "status": "ready_to_apply",
        "rank_score": 93,
        "rank_verdict": "Strong Fit",
        "portal": "unstop",
        "source": "Unstop Internships",
        "deadline": "2026-11-28T00:00:00+05:30"
    },
    {
        "key": "mystical-views_full-stack-developer-internship",
        "title": "Full Stack Developer Internship",
        "company": "Mystical Views Private Limited",
        "url": "https://unstop.com/internships/full-stack-developer-internship-mystical-views-private-limited-1806812",
        "location": "Gurgaon, HR (NCR)",
        "first_seen": today,
        "posted_date": today,
        "status": "ready_to_apply",
        "rank_score": 93,
        "rank_verdict": "Strong Fit",
        "portal": "unstop",
        "source": "Unstop Internships",
        "deadline": "2026-11-26T00:00:00+05:30"
    },
    {
        "key": "webmobril-technologies_full-stack-developer-internship",
        "title": "Full Stack Developer Internship",
        "company": "Webmobril Technologies",
        "url": "https://unstop.com/internships/full-stack-developer-internship-webmobril-technologies-1818984",
        "location": "Noida, UP (NCR)",
        "first_seen": today,
        "posted_date": today,
        "status": "ready_to_apply",
        "rank_score": 93,
        "rank_verdict": "Strong Fit",
        "portal": "unstop",
        "source": "Unstop Internships",
        "deadline": "2026-12-03T00:00:00+05:30"
    },
    {
        "key": "accesco-living_frontend-and-backend-internship",
        "title": "Frontend and Backend Internship",
        "company": "Accesco Living",
        "url": "https://unstop.com/internships/frontend-and-backend-internship-accesco-living-1804646",
        "location": "Remote (All India)",
        "first_seen": today,
        "posted_date": today,
        "status": "ready_to_apply",
        "rank_score": 92,
        "rank_verdict": "Strong Fit",
        "portal": "unstop",
        "source": "Unstop Internships",
        "deadline": "2026-11-24T00:00:00+05:30"
    },
    {
        "key": "frontend-arena_frontend-developer-internship",
        "title": "Frontend Developer Internship",
        "company": "Frontend Arena",
        "url": "https://unstop.com/internships/frontend-developer-internship-frontend-arena-1803735",
        "location": "Remote (All India)",
        "first_seen": today,
        "posted_date": today,
        "status": "ready_to_apply",
        "rank_score": 92,
        "rank_verdict": "Strong Fit",
        "portal": "unstop",
        "source": "Unstop Internships",
        "deadline": "2026-11-21T11:00:00+05:30"
    },
    {
        "key": "rewyoo-com_ui-ux-design-internship",
        "title": "UI/UX Design Internship",
        "company": "Rewyoo.com",
        "url": "https://unstop.com/internships/uiux-design-internship-rewyoocom-1806024",
        "location": "Remote (All India)",
        "first_seen": today,
        "posted_date": today,
        "status": "ready_to_apply",
        "rank_score": 92,
        "rank_verdict": "Strong Fit",
        "portal": "unstop",
        "source": "Unstop Internships",
        "deadline": "2026-11-25T00:00:00+05:30"
    }
]

added_seen = 0
for pos in new_positions:
    k = pos["key"]
    if k not in seen_data["seen"]:
        entry = dict(pos)
        del entry["key"]
        seen_data["seen"][k] = entry
        added_seen += 1

seen_path.write_text(json.dumps(seen_data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Updated seen_jobs.json with {added_seen} new active entries (total: {len(seen_data['seen'])}).")

# 2. Update job_search_tracker.csv if not already present
tracker_path = Path("job_search_tracker.csv")
existing_urls = set()
with open(tracker_path, "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row.get("source"):
            existing_urls.add(row["source"].rstrip("/"))

added_tracker = 0
with open(tracker_path, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "date", "company", "sector", "role", "role_type", "channel", "status",
        "contact_person", "fit_rating", "notes", "cv_file", "cover_letter_file",
        "source", "deadline"
    ])
    for pos in new_positions:
        if pos["url"].rstrip("/") not in existing_urls:
            writer.writerow({
                "date": today,
                "company": pos["company"],
                "sector": "Tech / Startups",
                "role": pos["title"],
                "role_type": "Frontend / Full Stack" if "full" in pos["title"].lower() or "frontend" in pos["title"].lower() else "UI/UX Design",
                "channel": pos["portal"].capitalize(),
                "status": "ready_to_apply",
                "contact_person": "",
                "fit_rating": str(pos["rank_score"]),
                "notes": f"Vetted active opportunity on {pos['source']}; payload audited and staged for 1-click submission",
                "cv_file": "cv/Himanshu_Dahiya_Resume.pdf",
                "cover_letter_file": "",
                "source": pos["url"],
                "deadline": pos.get("deadline") or ""
            })
            existing_urls.add(pos["url"].rstrip("/"))
            added_tracker += 1

print(f"Updated job_search_tracker.csv with {added_tracker} new tracked rows.")

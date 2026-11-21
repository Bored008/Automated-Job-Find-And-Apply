import json
import csv
from pathlib import Path

# 1. Update seen_jobs.json
seen_path = Path('job_scraper/seen_jobs.json')
seen_data = json.loads(seen_path.read_text(encoding='utf-8'))
if 'seen' not in seen_data:
    seen_data['seen'] = {}

new_apps = [
    {
        "key": "kikbak-financial_frontend-developer-reactjs",
        "title": "Frontend Developer (React.js)",
        "company": "Kikbak Financial",
        "url": "https://unstop.com/jobs/frontend-developer-reactjs-kikbak-financial-1816010",
        "location": "Remote (India)",
        "first_seen": "2026-11-21",
        "posted_date": "2026-11-20",
        "status": "applied",
        "applied_date": "2026-11-21",
        "rank_score": 94,
        "rank_verdict": "Strong Fit",
        "portal": "unstop",
        "source": "unstop",
        "deadline": "2026-12-01T00:00:00+05:30"
    },
    {
        "key": "techspar-solutions_frontend-developer",
        "title": "Frontend Developer",
        "company": "TECHSPAR SOLUTIONS",
        "url": "https://unstop.com/jobs/frontend-developer-techspar-solutions-1817946",
        "location": "New Delhi, Delhi",
        "first_seen": "2026-11-21",
        "posted_date": "2026-11-20",
        "status": "applied",
        "applied_date": "2026-11-21",
        "rank_score": 92,
        "rank_verdict": "Strong Fit",
        "portal": "unstop",
        "source": "unstop",
        "deadline": "2026-12-02T00:00:00+05:30"
    },
    {
        "key": "ohmyfood_ui-ux-graphic-designer",
        "title": "UI/UX & Graphic Designer",
        "company": "OhMyFood",
        "url": "https://unstop.com/jobs/uiux-graphic-designer-ohmyfood-1814681",
        "location": "Remote (India)",
        "first_seen": "2026-11-21",
        "posted_date": "2026-11-20",
        "status": "applied",
        "applied_date": "2026-11-21",
        "rank_score": 91,
        "rank_verdict": "Strong Fit",
        "portal": "unstop",
        "source": "unstop",
        "deadline": "2026-12-01T00:00:00+05:30"
    }
]

for app in new_apps:
    k = app['key']
    entry = dict(app)
    del entry['key']
    seen_data['seen'][k] = entry

seen_path.write_text(json.dumps(seen_data, indent=2), encoding='utf-8')
print(f"Updated seen_jobs.json with {len(new_apps)} new applications.")

# 2. Update job_search_tracker.csv
tracker_path = Path('job_search_tracker.csv')
rows = []
with open(tracker_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for r in reader:
        # Update Clerk status if matching
        if r.get('company') == 'Clerk' and 'Web Designer' in r.get('role', ''):
            r['status'] = 'rejected'
            r['notes'] = 'Decision update received via Gmail (1a1f989794a4ccb1) on 2026-11-20: moved forward with other candidates'
        rows.append(r)

# Add new rows
new_tracker_rows = [
    {
        "date": "2026-11-21",
        "company": "Kikbak Financial",
        "sector": "FinTech / Payments",
        "role": "Frontend Developer (React.js)",
        "role_type": "Frontend Development",
        "channel": "Unstop",
        "status": "applied",
        "contact_person": "",
        "fit_rating": "94",
        "notes": "Submitted application via Unstop portal on 2026-11-21; profile: React, Next.js, TypeScript",
        "cv_file": "cv/Himanshu_Dahiya_Resume.pdf",
        "cover_letter_file": "",
        "source": "https://unstop.com/jobs/frontend-developer-reactjs-kikbak-financial-1816010",
        "deadline": "2026-12-01T00:00:00+05:30"
    },
    {
        "date": "2026-11-21",
        "company": "TECHSPAR SOLUTIONS",
        "sector": "IT Services / Web",
        "role": "Frontend Developer",
        "role_type": "Frontend Development",
        "channel": "Unstop",
        "status": "applied",
        "contact_person": "",
        "fit_rating": "92",
        "notes": "Submitted application via Unstop portal on 2026-11-21; location: New Delhi, Delhi (Delhi NCR)",
        "cv_file": "cv/Himanshu_Dahiya_Resume.pdf",
        "cover_letter_file": "",
        "source": "https://unstop.com/jobs/frontend-developer-techspar-solutions-1817946",
        "deadline": "2026-12-02T00:00:00+05:30"
    },
    {
        "date": "2026-11-21",
        "company": "OhMyFood",
        "sector": "FoodTech / Consumer",
        "role": "UI/UX & Graphic Designer",
        "role_type": "UI/UX Design",
        "channel": "Unstop",
        "status": "applied",
        "contact_person": "",
        "fit_rating": "91",
        "notes": "Submitted application via Unstop portal on 2026-11-21; profile: Figma, UI/UX Design Systems, Prototyping",
        "cv_file": "cv/Himanshu_Dahiya_Resume.pdf",
        "cover_letter_file": "",
        "source": "https://unstop.com/jobs/uiux-graphic-designer-ohmyfood-1814681",
        "deadline": "2026-12-01T00:00:00+05:30"
    }
]

rows.extend(new_tracker_rows)

with open(tracker_path, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated job_search_tracker.csv: total {len(rows)} entries.")

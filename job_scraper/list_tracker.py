import csv

with open('job_search_tracker.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Total rows in job_search_tracker.csv: {len(rows)}")
for i, r in enumerate(rows, 1):
    print(f"{i}. {r.get('company')} — {r.get('role')} [{r.get('status')}] (Fit: {r.get('fit_rating')}%)")

import json
import csv
from pathlib import Path

vetted = json.load(open('job_scraper/vetted_genuine_jobs.json', encoding='utf-8'))
tracker = list(csv.DictReader(open('job_search_tracker.csv', encoding='utf-8')))
tracked_urls = {t['source'].rstrip('/') for t in tracker if t.get('source')}

unapplied = [j for j in vetted if j['url'].rstrip('/') not in tracked_urls]

html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Job Search - Fast Zero-Token Queue</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 30px; }
        .container { max-width: 900px; margin: 0 auto; }
        h1 { font-size: 24px; color: #38bdf8; margin-bottom: 8px; }
        p.subtitle { color: #94a3b8; font-size: 14px; margin-bottom: 24px; }
        .badge { background: #0284c7; color: white; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; }
        .card { background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 18px 22px; margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between; }
        .card:hover { border-color: #38bdf8; }
        .role { font-size: 16px; font-weight: 600; color: #f1f5f9; }
        .meta { font-size: 13px; color: #94a3b8; margin-top: 4px; }
        .btn { background: #2563eb; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 500; display: inline-flex; align-items: center; gap: 6px; }
        .btn:hover { background: #1d4ed8; }
        .btn-launch-all { background: #10b981; color: white; padding: 10px 20px; font-size: 14px; font-weight: 600; cursor: pointer; border: none; border-radius: 6px; margin-bottom: 20px; }
        .btn-launch-all:hover { background: #059669; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚡ Fast Zero-Token Application Queue</h1>
        <p class="subtitle">Positions vetted for Himanshu Dahiya (100% Remote / Delhi NCR | React, Next.js, UI/UX, Full Stack). Opening any link activates your installed Userscript / Extension for instantaneous 0-token autofill.</p>
        
        <button class="btn-launch-all" onclick="openBatch()">🚀 Open Next 5 Positions in New Tabs</button>
        
        <div id="jobList">
"""

for idx, j in enumerate(unapplied, 1):
    html += f"""
        <div class="card">
            <div>
                <span class="badge">{j.get('source', 'ATS')}</span>
                <div class="role" style="margin-top:6px;">{j['company']} — {j['title']}</div>
                <div class="meta">📍 {j['location']} &nbsp;|&nbsp; 🎯 Fit: {j.get('fit_rating', 92)}%</div>
            </div>
            <div>
                <a href="{j['url']}" target="_blank" class="btn">Open & Autofill ↗</a>
            </div>
        </div>
"""

html += """
        </div>
    </div>
    <script>
        const urls = """ + json.dumps([j['url'] for j in unapplied]) + """;
        function openBatch() {
            const nextFive = urls.slice(0, 5);
            nextFive.forEach(u => window.open(u, '_blank'));
        }
    </script>
</body>
</html>
"""

Path('tools/application_queue_launcher.html').write_text(html, encoding='utf-8')
print('Generated application_queue_launcher.html with', len(unapplied), 'positions.')

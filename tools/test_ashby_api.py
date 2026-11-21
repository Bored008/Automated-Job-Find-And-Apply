import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://jobs.ashbyhq.com/api/non-user-graphql?op=JobPosting'
query = """
query JobPosting($organizationHostedJobsPageName: String!, $jobPostingId: String!) {
  jobPosting(organizationHostedJobsPageName: $organizationHostedJobsPageName, jobPostingId: $jobPostingId) {
    id
    title
    applicationForm {
      id
      sections {
        fields {
          id
          title
          isRequired
          type
        }
      }
    }
  }
}
"""
payload = {
    'operationName': 'JobPosting',
    'variables': {
        'organizationHostedJobsPageName': 'atlan',
        'jobPostingId': 'c6bb032c-6ac8-4b59-915c-d59b6f3a86f8'
    },
    'query': query
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
)

try:
    with urllib.request.urlopen(req, context=ctx, timeout=5) as r:
        d = json.loads(r.read().decode('utf-8'))
        jp = d.get('data', {}).get('jobPosting', {})
        print('Job Title:', jp.get('title'))
        app_form = jp.get('applicationForm', {})
        print('Application Form ID:', app_form.get('id'))
        for sec in app_form.get('sections', []):
            for f in sec.get('fields', []):
                print(f"  Field: {f.get('title')} (id: {f.get('id')}, type: {f.get('type')}, required: {f.get('isRequired')})")
except Exception as e:
    print('Error:', e)

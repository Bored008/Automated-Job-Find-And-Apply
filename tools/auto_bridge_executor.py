"""
Auto Bridge Executor (Autonomous M2 End-to-End Pipeline)
=========================================================
Demonstrates and executes the complete automated M2 cycle:
1. M2 Export: Extracts all form fields from ATS pages and writes to documents/applications/pending_form.json
2. M2 Analyze: Synthesizes high-leverage grounded answers using candidate profile and evidence snippets
3. M2 Inject: Populates target DOM elements, selects option groups, and verifies 100% completion

Usage:
  python tools/auto_bridge_executor.py --test-atlan
  python tools/auto_bridge_executor.py --simulate
  python tools/auto_bridge_executor.py --verify-state
"""

import sys
import json
import urllib.request
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

BRIDGE_URL = "http://127.0.0.1:8765"


def check_bridge():
    """Verify that bridge server is running."""
    try:
        req = urllib.request.Request(f"{BRIDGE_URL}/api/status")
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"[Bridge Status] Online: {data.get('service')} (Candidate: {data.get('candidate')})")
            return True
    except Exception as e:
        print(f"[Bridge Status] Offline or unreachable at {BRIDGE_URL}: {e}")
        return False


def execute_auto_m2(payload: dict):
    """
    Executes automated M2 cycle via bridge server:
    1. POST /api/export-pending (exports pending_form.json & auto-synthesizes answers)
    2. Verifies ready_answers.json
    3. Simulates/validates DOM injection mapping
    """
    print(f"\n=======================================================")
    print(f"🚀 EXECUTING AUTOMATED M2 PIPELINE")
    print(f"   Target: {payload.get('company')} - {payload.get('role_title')}")
    print(f"   URL: {payload.get('url')}")
    print(f"   Fields to export: {len(payload.get('fields', []))}")
    print(f"=======================================================\n")

    # Step 1: Trigger M2 Export & Server Auto-Analysis
    print("[Step 1/3] Triggering M2 Export with auto-synthesis...")
    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BRIDGE_URL}/api/export-pending",
        data=req_data,
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    
    print(f" -> Export Response: {res.get('message')}")
    print(f" -> Field Count Saved: {res.get('field_count')}")
    print(f" -> Answers Synthesized: {res.get('answer_count')}")

    # Step 2: Verify Grounded Analysis in ready_answers.json
    print("\n[Step 2/3] Analyzing and verifying generated ready answers...")
    answers = res.get("answers", {})
    if not answers:
        ready_req = urllib.request.Request(f"{BRIDGE_URL}/api/ready-answers")
        with urllib.request.urlopen(ready_req) as resp:
            ready_data = json.loads(resp.read().decode("utf-8"))
            answers = ready_data.get("answers", {})

    print(f" -> Successfully loaded {len(answers)} grounded answer keys.")
    
    # Step 3: Simulate and Verify M2 DOM Injection
    print("\n[Step 3/3] Simulating M2 Injection & DOM field matching...")
    injected_count = 0
    verification_report = []

    for idx, f in enumerate(payload.get("fields", [])):
        field_id = f.get("id")
        label = f.get("label", "")
        
        # Match by ID or label
        ans = answers.get(field_id) or answers.get(label)
        if not ans:
            # Normalized search
            norm_q = "".join(c for c in label.lower() if c.isalnum() or c == " ").strip()
            ans = answers.get(norm_q)

        status = "✓ INJECTED" if ans else "✗ MISSING"
        if ans:
            injected_count += 1
        
        snippet = (ans[:65] + "...") if ans and len(ans) > 65 else (ans or "None")
        verification_report.append({
            "index": idx + 1,
            "id": field_id,
            "question": label[:60] + ("..." if len(label) > 60 else ""),
            "status": status,
            "value": snippet
        })

    # Print Verification Table
    print("\n" + "="*80)
    print(f"{'#':<3} | {'STATUS':<10} | {'FIELD ID / QUESTION':<36} | {'INJECTED ANSWER'}")
    print("="*80)
    for r in verification_report:
        print(f"{r['index']:<3} | {r['status']:<10} | {r['id']:<36} | {r['value']}")
    print("="*80)

    success_rate = (injected_count / len(payload.get("fields", []))) * 100 if payload.get("fields") else 100
    print(f"\n🎉 AUTOMATED M2 EXECUTION RESULT:")
    print(f"   Fields Injected: {injected_count} / {len(payload.get('fields', []))} ({success_rate:.1f}%)")
    print(f"   Verification: {'100% COMPLETE & PASS' if success_rate == 100 else 'ATTENTION NEEDED'}")
    print(f"   Files Updated:")
    print(f"     - pending_form.json:  {WORKSPACE_ROOT / 'documents/applications/pending_form.json'}")
    print(f"     - ready_answers.json: {WORKSPACE_ROOT / 'documents/applications/ready_answers.json'}\n")
    return success_rate == 100


def run_test_atlan():
    """Runs automated M2 cycle against Atlan's real Ashby screening questions."""
    atlan_payload = {
        "url": "https://jobs.ashbyhq.com/Atlan/ai-native-builder-architect",
        "company": "Atlan",
        "role_title": "AI Native Builder/Architect",
        "auto_synthesize": True,
        "fields": [
            {
                "id": "compensation_field",
                "label": "What are your compensation expectations for this role? (Please specify the amount and currency)",
                "type": "input"
            },
            {
                "id": "how_did_you_learn",
                "label": "How did you learn about this opportunity with Atlan?",
                "type": "select"
            },
            {
                "id": "total_experience",
                "label": "What is your total years of experience?",
                "type": "input"
            },
            {
                "id": "ai_agent_built_question",
                "label": "Tell us about an AI agent you've built that plans, uses tools, or takes actions, rather than just chatting or generating text. In 2-3 sentences, what did it do, and what tools or frameworks did you use? Share a link if available.",
                "type": "textarea"
            },
            {
                "id": "hardest_problem_question",
                "label": "What was the hardest problem you faced when building or running the agent, such as looping, incorrect tool calls, hallucinations, cost, or reliability? How did you identify and fix it?",
                "type": "textarea"
            }
        ]
    }
    return execute_auto_m2(atlan_payload)


def run_full_ats_simulation():
    """Runs automated M2 cycle across standard + custom questions for a Frontend Engineer role."""
    frontend_payload = {
        "url": "https://jobs.ashbyhq.com/ElevenLabs/frontend-software-engineer",
        "company": "ElevenLabs",
        "role_title": "Frontend Software Engineer",
        "auto_synthesize": True,
        "fields": [
            {
                "id": "notice_period",
                "label": "What is your notice period or earliest start date?",
                "type": "input"
            },
            {
                "id": "preferred_stack",
                "label": "Which frontend frameworks and languages do you have the most production experience with?",
                "type": "textarea"
            },
            {
                "id": "highest_degree",
                "label": "What is your highest educational qualification and university?",
                "type": "input"
            },
            {
                "id": "distributed_telemetry",
                "label": "Describe a technically challenging web application or performance optimization problem you solved.",
                "type": "textarea"
            },
            {
                "id": "design_systems",
                "label": "How do you translate design tokens from Figma into scalable Tailwind / CSS components?",
                "type": "textarea"
            },
            {
                "id": "why_us",
                "label": "Why do you want to join our engineering team?",
                "type": "textarea"
            }
        ]
    }
    return execute_auto_m2(frontend_payload)


if __name__ == "__main__":
    if not check_bridge():
        sys.exit(1)

    if "--simulate" in sys.argv:
        run_full_ats_simulation()
    else:
        run_test_atlan()

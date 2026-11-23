"""
Agent Bridge Synthesizer (Method 2 CLI / Automation)
===================================================
Reads exported form fields from documents/applications/pending_form.json,
synthesizes grounded screening answers using engine.py and candidate profile,
and writes the ready answers to documents/applications/ready_answers.json.
"""

import sys
import json
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from tools.bridge.engine import synthesize_field_answer, PROFILE
from tools.bridge.state import get_pending_form, save_ready_answers


def synthesize_pending():
    pending = get_pending_form()
    fields = pending.get("fields", [])
    if not fields:
        print("[Bridge Synthesizer] No pending fields found in documents/applications/pending_form.json")
        return False

    company = pending.get("company", "")
    role_title = pending.get("role_title", "")
    print(f"[Bridge Synthesizer] Synthesizing answers for {company} - {role_title} ({len(fields)} fields)...")

    answers = {}
    for idx, f in enumerate(fields):
        field_id = f.get("id") or f.get("name") or f.get("label", "")
        question = f.get("label") or f.get("placeholder") or f.get("name", "")
        if not question:
            continue
        print(f" -> Question: {question[:75]}...")
        answer = synthesize_field_answer(question, role_title=role_title, company=company)
        
        # Prevent key collision if multiple fields share id like text_0
        target_id = field_id
        if target_id in answers:
            target_id = f"{field_id}_{idx}"
        answers[target_id] = answer
        answers[question] = answer
        import re
        norm_q = re.sub(r'[^a-zA-Z0-9 ]', ' ', question.lower()).strip()
        if norm_q:
            answers[norm_q] = answer
        print(f"    Answer: {answer[:80]}...\n")

    saved = save_ready_answers({
        "company": company,
        "role_title": role_title,
        "answers": answers
    })
    print(f"[Bridge Synthesizer] Successfully saved {saved['answer_count']} answers to documents/applications/ready_answers.json")
    print(f"[Bridge Synthesizer] You can now click '📥 Inject Ready Answers' in the browser extension!")
    return True


if __name__ == "__main__":
    synthesize_pending()

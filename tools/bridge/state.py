"""
Agent Bridge State Manager
==========================
Manages persistence for Method 2 (File Bridge) between the Chrome extension
and the Antigravity conversation environment:
- documents/applications/pending_form.json
- documents/applications/ready_answers.json
- documents/applications/bridge_audit.log
"""

import json
import time
from datetime import datetime
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
APPLICATIONS_DIR = WORKSPACE_ROOT / "documents" / "applications"
PENDING_FORM_PATH = APPLICATIONS_DIR / "pending_form.json"
READY_ANSWERS_PATH = APPLICATIONS_DIR / "ready_answers.json"
AUDIT_LOG_PATH = APPLICATIONS_DIR / "bridge_audit.log"

APPLICATIONS_DIR.mkdir(parents=True, exist_ok=True)


def _log_audit(action: str, details: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{action.upper()}] {details}\n"
    try:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        print(f"[BridgeState] Audit log error: {e}")


def save_pending_form(data: dict) -> dict:
    """Save unfilled screening form exported from Chrome extension."""
    payload = {
        "timestamp": datetime.now().isoformat(),
        "status": "pending_synthesis",
        "url": data.get("url", ""),
        "company": data.get("company", ""),
        "role_title": data.get("role_title", ""),
        "field_count": len(data.get("fields", [])),
        "fields": data.get("fields", [])
    }
    with open(PENDING_FORM_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    _log_audit("export_pending", f"Company: {payload['company']}, Role: {payload['role_title']}, Fields: {payload['field_count']}")
    return payload


def get_pending_form() -> dict:
    """Read pending form data."""
    if not PENDING_FORM_PATH.exists():
        return {"status": "none", "fields": []}
    try:
        with open(PENDING_FORM_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"status": "error", "message": str(e), "fields": []}


def save_ready_answers(data: dict) -> dict:
    """Save synthesized answers for injection into form."""
    payload = {
        "timestamp": datetime.now().isoformat(),
        "status": "ready_for_injection",
        "company": data.get("company", ""),
        "role_title": data.get("role_title", ""),
        "answer_count": len(data.get("answers", {})),
        "answers": data.get("answers", {})
    }
    with open(READY_ANSWERS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    _log_audit("save_answers", f"Company: {payload['company']}, Answers: {payload['answer_count']}")
    return payload


def get_ready_answers() -> dict:
    """Read ready answers for injection."""
    if not READY_ANSWERS_PATH.exists():
        return {"status": "none", "answers": {}}
    try:
        with open(READY_ANSWERS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"status": "error", "message": str(e), "answers": {}}


def clear_state():
    """Archive/clear pending form and ready answers upon application submission."""
    if PENDING_FORM_PATH.exists():
        PENDING_FORM_PATH.unlink()
    if READY_ANSWERS_PATH.exists():
        READY_ANSWERS_PATH.unlink()
    _log_audit("clear_state", "Bridge files cleared after submission")

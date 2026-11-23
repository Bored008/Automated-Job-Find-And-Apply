"""
Agent Bridge Server
===================
Lightweight, zero-dependency local HTTP API server running on port 8765.
Connects the Chrome Autofill Extension to Himanshu's Antigravity project workspace:

Endpoints:
- GET  /api/status            : Health check & bridge capabilities
- POST /api/export-pending    : Auto-M2 / File Bridge - Exports form fields, auto-analyzes, and saves ready answers
- GET  /api/pending-form      : Inspects current exported pending form
- POST /api/ready-answers     : Saves synthesized answers to ready_answers.json
- GET  /api/ready-answers     : Returns ready answers for extension DOM injection
- POST /api/clear             : Resets pending form & ready answers
"""

import sys
import re
import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Add project root to sys.path
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from tools.bridge.engine import synthesize_field_answer, PROFILE
from tools.bridge.state import (
    save_pending_form,
    get_pending_form,
    save_ready_answers,
    get_ready_answers,
    clear_state
)

PORT = 8765
HOST = "127.0.0.1"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class BridgeHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With, Access-Control-Request-Private-Network")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def _send_json(self, data: dict, status_code: int = 200):
        body = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        raw = self.rfile.read(content_length).decode("utf-8")
        try:
            return json.loads(raw)
        except Exception as e:
            logging.error(f"JSON parse error: {e}")
            return {}

    def do_GET(self):
        path = self.path.split("?")[0]
        
        if path == "/api/status" or path == "/":
            pending = get_pending_form()
            ready = get_ready_answers()
            self._send_json({
                "status": "online",
                "service": "Antigravity AI Job Search Bridge",
                "candidate": PROFILE["full_name"],
                "port": PORT,
                "supported_methods": [
                    "auto_m2_unified_pipeline",
                    "method_2_file_bridge",
                    "method_3_clipboard_chat"
                ],
                "has_pending_form": len(pending.get("fields", [])) > 0,
                "has_ready_answers": len(ready.get("answers", {})) > 0
            })
            return

        if path == "/api/pending-form":
            self._send_json(get_pending_form())
            return

        if path == "/api/ready-answers":
            self._send_json(get_ready_answers())
            return

        self._send_json({"error": "Not Found", "path": path}, status_code=404)

    def do_POST(self):
        path = self.path.split("?")[0]
        payload = self._read_json_body()

        # Method 2 & Auto-M2: Export Pending Form, Auto-Analyze, and Save Ready Answers
        if path == "/api/export-pending" or path == "/api/auto-m2":
            saved = save_pending_form(payload)
            logging.info(f"[Method 2 Export] Saved pending_form.json with {saved['field_count']} fields")
            
            auto_synthesize = payload.get("auto_synthesize", True)
            answers = {}
            if auto_synthesize:
                company = payload.get("company", "")
                role_title = payload.get("role_title", "")
                api_key = payload.get("api_key", "")
                fields = payload.get("fields", [])
                
                logging.info(f"[Auto M2 Synthesis] Analyzing & synthesizing {len(fields)} fields for {company} - {role_title}...")
                for idx, f in enumerate(fields):
                    field_id = f.get("id") or f.get("name") or f.get("label", "")
                    question = f.get("label") or f.get("placeholder") or f.get("name", "")
                    if not question:
                        continue
                    ans = synthesize_field_answer(question, role_title=role_title, company=company, api_key=api_key)
                    
                    target_id = field_id
                    if target_id in answers:
                        target_id = f"{field_id}_{idx}"
                    answers[target_id] = ans
                    answers[question] = ans
                    norm_q = re.sub(r'[^a-zA-Z0-9 ]', ' ', question.lower()).strip()
                    if norm_q:
                        answers[norm_q] = ans

                # Save synthesized answers to ready_answers.json
                saved_answers = save_ready_answers({
                    "company": company,
                    "role_title": role_title,
                    "answers": answers
                })
                logging.info(f"[Auto M2 Synthesis] Successfully saved {saved_answers['answer_count']} answers to ready_answers.json")

            self._send_json({
                "success": True,
                "method": "method_2_file_bridge",
                "message": "Form exported, analyzed, and ready_answers.json generated." if auto_synthesize else "Form exported to pending_form.json",
                "field_count": saved["field_count"],
                "answer_count": len(answers),
                "answers": answers,
                "data": saved
            })
            return

        # Method 2: Save Ready Answers (written by Antigravity or automation)
        if path == "/api/ready-answers":
            saved = save_ready_answers(payload)
            logging.info(f"[Method 2 Answers Saved] Saved ready_answers.json with {saved['answer_count']} answers")
            self._send_json({
                "success": True,
                "message": "Answers saved to documents/applications/ready_answers.json",
                "answer_count": saved["answer_count"]
            })
            return

        # Clear State
        if path == "/api/clear":
            clear_state()
            self._send_json({"success": True, "message": "State cleared"})
            return

        self._send_json({"error": "Not Found", "path": path}, status_code=404)

    def log_message(self, format, *args):
        # Override standard log message to keep server stdout clean
        logging.info(f"{self.address_string()} - {format % args}")


def run_server():
    server = HTTPServer((HOST, PORT), BridgeHandler)
    logging.info(f"==================================================")
    logging.info(f"🚀 Antigravity Bridge Server listening on http://{HOST}:{PORT}")
    logging.info(f"   Auto M2:  POST http://{HOST}:{PORT}/api/export-pending (or /api/auto-m2)")
    logging.info(f"   File M2:  GET  http://{HOST}:{PORT}/api/ready-answers")
    logging.info(f"   Clip M3:  Native Clipboard Export & Ingestion")
    logging.info(f"==================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down bridge server...")
        server.server_close()


if __name__ == "__main__":
    run_server()

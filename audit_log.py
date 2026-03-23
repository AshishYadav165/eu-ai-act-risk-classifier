import os
import json
import hashlib
from datetime import datetime

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

def log_classification(session_id: str, use_case: str, claude_result: dict, openai_result: dict, agreement: bool):
    entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'session_id': session_id,
        'use_case_hash': hashlib.sha256(use_case.encode()).hexdigest()[:16],
        'claude_risk_tier': claude_result.get('risk_tier', 'Unknown'),
        'openai_risk_tier': openai_result.get('risk_tier', 'Unknown'),
        'models_agree': agreement,
    }
    log_file = os.path.join(LOG_DIR, f'classifications_{datetime.utcnow().strftime("%Y%m%d")}.jsonl')
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')

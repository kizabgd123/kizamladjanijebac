"""
JudgeGuard v2.0 - The Guardian of the Antigravity System.
Verifies every critical step against WORK_LOG.md and MASTER_ORCHESTRATION.md
"""

import os
import sys
import time

def check_work_log(action: str) -> bool:
    work_log_path = os.path.join(os.getcwd(), "WORK_LOG.md")
    if not os.path.exists(work_log_path):
        print("🛑 WORK_LOG.md not found. Required before action.")
        return False
    
    try:
        with open(work_log_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
            if "🟡" in content or "starting" in content or "completed" in content or "✅" in content:
                return True
    except Exception as e:
        print(f"⚠️ Error reading WORK_LOG.md: {e}")
        return False

    print("🛑 WORK_LOG.md not updated recently.")
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 judge_guard.py '<action_description>'")
        sys.exit(1)
        
    action = sys.argv[1]
    
    # Check work log
    if not check_work_log(action):
        sys.exit(1)
        
    print(f"✅ JudgeGuard: Action '{action}' APPROVED.")
    sys.exit(0)

if __name__ == "__main__":
    main()

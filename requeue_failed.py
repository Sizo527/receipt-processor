import json
import shutil
from pathlib import Path
from config import REVIEW_DIR, RAW_DIR, LOGS_DIR

def requeue_failed_receipts():
    log_file = LOGS_DIR / "log.jsonl"
    
    if not log_file.exists():
        print("No log file found.")
        return
        
    # Read logs to find the LAST status of each file
    file_statuses = {}
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                event = json.loads(line)
                filename = event.get("file")
                if filename:
                    file_statuses[filename] = event
            except json.JSONDecodeError:
                continue
                
    # Filter for files currently in needs_review with an API error
    moved_count = 0
    for filename, event in file_statuses.items():
        if event.get("status") == "needs_review":
            reason = event.get("reason", "")
            if reason.startswith("API error:"):
                source_path = REVIEW_DIR / filename
                if source_path.exists():
                    dest_path = RAW_DIR / filename
                    shutil.move(str(source_path), str(dest_path))
                    moved_count += 1
                    print(f"Requeued: {filename}")
                    
    print(f"\nSuccessfully requeued {moved_count} receipts for processing.")

if __name__ == "__main__":
    requeue_failed_receipts()

import json
import shutil
from datetime import datetime
from pathlib import Path
from config import PROCESSED_DIR, REVIEW_DIR, DUPLICATES_DIR, LOGS_DIR, ARCHIVE_DIR

LOG_FILE = LOGS_DIR / "log.jsonl"

def log_event(event_data):
    event_data['time'] = datetime.now().strftime("%H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(event_data) + '\n')

def archive_original(source_path):
    dest_path = ARCHIVE_DIR / source_path.name
    if not dest_path.exists():
        shutil.copy2(source_path, dest_path)
    return dest_path

def move_to_processed(source_path, category, new_filename):
    category_dir = PROCESSED_DIR / sanitize_for_path(category)
    category_dir.mkdir(exist_ok=True)
    
    dest_path = category_dir / new_filename
    shutil.move(str(source_path), str(dest_path))
    return dest_path

def move_to_review(source_path, new_filename=None):
    if not new_filename:
        new_filename = source_path.name
    dest_path = REVIEW_DIR / new_filename
    shutil.move(str(source_path), str(dest_path))
    return dest_path

def move_to_duplicates(source_path, new_filename=None):
    if not new_filename:
        new_filename = source_path.name
    dest_path = DUPLICATES_DIR / new_filename
    shutil.move(str(source_path), str(dest_path))
    return dest_path

def sanitize_for_path(name):
    return "".join(c if c.isalnum() else "_" for c in name)

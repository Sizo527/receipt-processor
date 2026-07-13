import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"
REVIEW_DIR = BASE_DIR / "review"
DUPLICATES_DIR = BASE_DIR / "duplicates"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"
ARCHIVE_DIR = BASE_DIR / "archive"

# List of directories to create
DIRS = [RAW_DIR, PROCESSED_DIR, REVIEW_DIR, DUPLICATES_DIR, REPORTS_DIR, LOGS_DIR, ARCHIVE_DIR]

# Valid Categories
CATEGORIES = [
    "Feed Cost",
    "Veterinary Care",
    "Husbandry Fees",
    "Transportation",
    "Land Rent",
    "Infrastructure",
    "Equipment and Maintenance",
    "Labour Cost",
    "Vehicles",
    "Utilities",
    "Crop & Soil Inputs",
    "Other"
]

# Supported Currencies
CURRENCIES = ["USD", "ZWL", "ZiG"]

# API settings
CONFIDENCE_THRESHOLD = 0.7
DUPLICATE_HASH_THRESHOLD = 5

def init_directories():
    for directory in DIRS:
        directory.mkdir(parents=True, exist_ok=True)

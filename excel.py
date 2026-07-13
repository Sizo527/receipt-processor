import pandas as pd
from pathlib import Path
from config import REPORTS_DIR

EXCEL_FILE = REPORTS_DIR / "Receipts.xlsx"

COLUMNS = [
    "Date", "Retailer", "Category", "Amount", "Currency",
    "Receipt No", "Filename", "Confidence", "Issues", "Flagged"
]

def load_or_create_excel():
    if EXCEL_FILE.exists():
        return pd.read_excel(EXCEL_FILE)
    return pd.DataFrame(columns=COLUMNS)

def append_to_excel(metadata, new_filename, flagged):
    df = load_or_create_excel()
    
    issues_str = ", ".join(metadata.get('issues', [])) if metadata.get('issues') else ""
    
    new_row = {
        "Date": metadata.get('date'),
        "Retailer": metadata.get('retailer'),
        "Category": metadata.get('category'),
        "Amount": metadata.get('amount'),
        "Currency": metadata.get('currency'),
        "Receipt No": metadata.get('receipt_number'),
        "Filename": new_filename,
        "Confidence": metadata.get('confidence'),
        "Issues": issues_str,
        "Flagged": "Yes" if flagged else "No"
    }
    
    new_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_df], ignore_index=True)
    
    # Sort by date
    df = df.sort_values(by="Date", ascending=True)
    
    df.to_excel(EXCEL_FILE, index=False)

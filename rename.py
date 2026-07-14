import re

def sanitize_filename(name):
    if name is None:
        name = "Unknown"
    # Remove unsafe characters
    return re.sub(r'[^\w\s-]', '', str(name)).strip()

def truncate_retailer(retailer, max_len=25):
    sanitized = sanitize_filename(retailer)
    if len(sanitized) <= max_len:
        return sanitized
    
    # Try to truncate at a word boundary
    truncated = sanitized[:max_len]
    last_space = truncated.rfind(' ')
    if last_space > 0:
        truncated = truncated[:last_space]
    return truncated.strip().replace(' ', '')

def generate_filename(metadata, original_extension):
    date_str = metadata.get('date', 'UnknownDate')
    category_raw = metadata.get('category', 'Other')
    retailer_raw = metadata.get('retailer', 'UnknownRetailer')
    receipt_no = metadata.get('receipt_number', 'UnknownNo')
    
    category = sanitize_filename(category_raw).replace(' ', '')
    retailer = truncate_retailer(retailer_raw)
    receipt_no_clean = sanitize_filename(str(receipt_no)).replace(' ', '')
    
    # Format: YYYY-MM-DD_Category_Retailer_ReceiptNo.png
    new_name = f"{date_str}_{category}_{retailer}_{receipt_no_clean}{original_extension}"
    return new_name

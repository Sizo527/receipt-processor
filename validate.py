from dateutil import parser
from config import CATEGORIES, CURRENCIES, CONFIDENCE_THRESHOLD

def parse_date(date_str):
    try:
        # Zimbabwe dates usually use day-first format
        dt = parser.parse(str(date_str), dayfirst=True)
        return dt.strftime('%Y-%m-%d')
    except (ValueError, TypeError, OverflowError):
        return None

def validate_category(category):
    if not category:
        return "Other"
    
    # Case-insensitive match against valid categories
    for valid_cat in CATEGORIES:
        if valid_cat.lower() == category.lower():
            return valid_cat
    
    return "Other"

def validate_receipt_data(data):
    """
    Validates the receipt data. 
    Returns (is_valid, mapped_data, reason)
    """
    mapped_data = dict(data)
    
    # Check Required Fields
    for field in ['date', 'retailer', 'category', 'amount']:
        if mapped_data.get(field) is None:
            return False, mapped_data, f"Missing required field: {field}"
    
    
    # Check Confidence
    confidence = mapped_data.get('confidence', 0.0)
    try:
        confidence = float(confidence)
    except (ValueError, TypeError):
        confidence = 0.0
        
    if confidence < CONFIDENCE_THRESHOLD:
        return False, mapped_data, f"Low confidence: {confidence}"
        
    # Check Issues
    issues = mapped_data.get('issues', [])
    if issues:
        return False, mapped_data, f"Issues reported by AI: {', '.join(issues)}"
        
    # Check Date
    raw_date = mapped_data.get('date')
    parsed_date = parse_date(raw_date)
    if not parsed_date:
        return False, mapped_data, f"Unparseable date: {raw_date}"
    mapped_data['date'] = parsed_date
        
    # Check Amount
    amount = mapped_data.get('amount')
    if amount is None:
        return False, mapped_data, "Amount missing"
    try:
        amount_val = float(amount)
        if amount_val <= 0:
            return False, mapped_data, "Amount is zero or negative"
        mapped_data['amount'] = amount_val
    except (ValueError, TypeError):
        return False, mapped_data, f"Non-numeric amount: {amount}"
        
    # Check Retailer
    retailer = mapped_data.get('retailer')
    if not retailer or not str(retailer).strip():
        return False, mapped_data, "Retailer missing or empty"
        
    # Check Currency
    currency = mapped_data.get('currency')
    if not currency or str(currency).upper() not in CURRENCIES:
        return False, mapped_data, f"Invalid or missing currency: {currency}"
    mapped_data['currency'] = str(currency).upper()
        
    # Remap Category
    mapped_data['category'] = validate_category(mapped_data.get('category'))
    
    return True, mapped_data, ""

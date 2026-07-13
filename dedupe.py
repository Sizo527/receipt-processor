import imagehash
from PIL import Image
from config import DUPLICATE_HASH_THRESHOLD

def calculate_hash(image_path):
    try:
        img = Image.open(image_path)
        return imagehash.phash(img)
    except Exception:
        return None

def is_duplicate(new_image_path, new_metadata, existing_records):
    """
    new_metadata: dict containing receipt data (date, amount, receipt_number)
    existing_records: list of dicts with (hash, date, amount, receipt_number)
    """
    new_hash = calculate_hash(new_image_path)
    if new_hash is None:
        return False, None
        
    for record in existing_records:
        rec_hash = record.get('hash')
        if not rec_hash:
            continue
            
        hash_diff = new_hash - rec_hash
        
        if hash_diff <= DUPLICATE_HASH_THRESHOLD:
            # Hash is close, now check metadata
            if (new_metadata.get('date') == record.get('date') and 
                new_metadata.get('amount') == record.get('amount') and
                new_metadata.get('receipt_number') == record.get('receipt_number')):
                return True, record
                
    return False, new_hash

import sys
from pathlib import Path
from tqdm import tqdm
import base64
import io
from PIL import Image

from config import init_directories, RAW_DIR
from ai import process_receipt_ai
from validate import validate_receipt_data
from rename import generate_filename
from excel import append_to_excel
from dedupe import is_duplicate
from organize import log_event, move_to_processed, move_to_review, move_to_duplicates, archive_original

# Cache for deduplication
processed_records = []

def process_single_receipt(image_path):
    log_event({"file": image_path.name, "status": "started"})
    
    # Secure an untouched copy to the archive first
    archive_original(image_path)
    
    # First pass: AI
    raw_data, error, quota_exhausted = process_receipt_ai(image_path)
    
    if quota_exhausted:
        return {"filename": image_path.name, "status": "quota_exhausted"}
    
    if error:
        log_event({"file": image_path.name, "status": "needs_review", "reason": f"API error: {error}"})
        move_to_review(image_path)
        return {"filename": image_path.name, "status": "needs_review", "category": "Error", "vendor": "-", "amount": "-"}
            
    is_valid, metadata, reason = validate_receipt_data(raw_data)
        
    # Deduplication check
    is_dup, record = is_duplicate(image_path, metadata, processed_records)
    if is_dup:
        log_event({"file": image_path.name, "status": "duplicate", "matched_record": record.get('receipt_number')})
        move_to_duplicates(image_path)
        return {"filename": image_path.name, "status": "duplicate", "category": "Duplicate", "vendor": "-", "amount": "-"}
        
    # Generate filename
    new_filename = generate_filename(metadata, image_path.suffix)
    
    # Organize and Excel
    if is_valid:
        new_path = move_to_processed(image_path, metadata.get('category', 'Other'), new_filename)
        append_to_excel(metadata, new_filename, flagged=False)
        log_event({"file": image_path.name, "status": "processed", "category": metadata.get('category'), "confidence": metadata.get('confidence')})
    else:
        new_path = move_to_review(image_path, new_filename)
        append_to_excel(metadata, new_filename, flagged=True)
        log_event({"file": image_path.name, "status": "needs_review", "reason": reason})
        
    # Update hash records
    _, img_hash = is_duplicate(image_path, metadata, []) # Just getting the hash
    if img_hash is not None:
        processed_records.append({
            'hash': img_hash,
            'date': metadata.get('date'),
            'amount': metadata.get('amount'),
            'receipt_number': metadata.get('receipt_number')
        })
        
    # Generate image preview
    try:
        with Image.open(new_path) as img:
            # Resize if wider than 800px
            if img.width > 800:
                ratio = 800 / img.width
                new_size = (800, int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert to RGB to ensure we can save as JPEG
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=85)
            b64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            image_data = f"data:image/jpeg;base64,{b64_str}"
    except Exception as e:
        image_data = None
        
    return {
        "filename": image_path.name, 
        "status": "processed" if is_valid else "needs_review",
        "category": metadata.get('category', 'Other'),
        "vendor": metadata.get('retailer', '-'),
        "amount": metadata.get('amount', '-'),
        "date": metadata.get('date', '-'),
        "receipt_number": metadata.get('receipt_number', '-'),
        "currency": "USD", # Assuming USD or extract if available
        "confidence": metadata.get('confidence', 0),
        "image_data": image_data
    }

def main(ui_callback=None, source_dir=None):
    from config import RAW_DIR
    print("Initializing directories...")
    init_directories()
    
    target_dir = Path(source_dir) if source_dir else RAW_DIR
    
    images = list(target_dir.glob("*.png")) + list(target_dir.glob("*.jpg")) + list(target_dir.glob("*.jpeg"))
    
    if not images:
        print(f"No images found in {target_dir}")
        return
        
    print(f"Found {len(images)} receipts to process.")
    
    stats = {"processed": 0, "needs_review": 0, "duplicates": 0, "errors": 0}
    
    for idx, image_path in enumerate(tqdm(images, desc="Processing Receipts") if not ui_callback else images):
        try:
            result = process_single_receipt(image_path)
            
            if result.get("status") == "quota_exhausted":
                remaining = len(images) - idx
                log_event({
                    "status": "batch_halted", 
                    "reason": "daily_quota_exhausted", 
                    "processed_today": idx, 
                    "remaining_in_raw": remaining
                })
                print(f"\n[HALTED] Daily quota exhausted.")
                print(f"Processed today: {idx} | Remaining in raw: {remaining}")
                print("The daily quota resets at midnight Pacific time. Run the script again tomorrow to continue processing.")
                return
                
            if ui_callback:
                ui_callback(result)
        except Exception as e:
            print(f"Error processing {image_path.name}: {e}")
            log_event({"file": image_path.name, "status": "error", "reason": str(e)})
            stats["errors"] += 1
            if ui_callback:
                ui_callback({"filename": image_path.name, "status": "needs_review", "category": "Error", "vendor": "-", "amount": "-"})
            
    print("Processing complete.")

if __name__ == "__main__":
    import sys
    source = sys.argv[1] if len(sys.argv) > 1 else None
    main(source_dir=source)

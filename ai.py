import os
import json
import time
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from PIL import Image

def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # Fallback to local .env
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('GEMINI_API_KEY='):
                        api_key = line.split('=', 1)[1].strip().strip('"\'')
                        break
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    genai.configure(api_key=api_key)

# Initialize client on import
try:
    get_gemini_client()
except ValueError:
    pass # Will be handled later or explicitly

PROMPT = """You are reading fiscal receipts for a farming operation in Zimbabwe.

Extract the following fields and return them as a JSON object using exactly these keys:
- "date" (YYYY-MM-DD format if possible)
- "retailer" (name of the store/vendor)
- "category" (must be one of the possible categories below. Note: classify Fuel under "Transportation")
- "amount" (numeric total amount)
- "currency" (USD, ZWL, or ZiG — do not assume USD)
- "receipt_number" (the receipt or invoice number)
- "confidence" (0.0 to 1.0, your own estimate of extraction reliability)
- "issues" (a list of strings detailing any specific problems, e.g., "date partly obscured" — empty list if none)

Possible categories:
Feed Cost, Veterinary Care, Husbandry Fees, Transportation, Land Rent, Infrastructure, Equipment and Maintenance, Labour Cost, Vehicles, Utilities, Crop & Soil Inputs, Other

Return ONLY valid JSON, no other text.
"""

def call_gemini(image_path, model_name="gemini-1.5-flash", retries=3):
    model = genai.GenerativeModel(model_name)
    
    backoffs = [2, 5, 15]
    
    for attempt in range(retries):
        try:
            with Image.open(image_path) as img:
                img.thumbnail((1500, 1500))
                response = model.generate_content(
                    [PROMPT, img],
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="application/json",
                    ),
                    safety_settings={
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    }
                )
            
            raw_text = response.text
            
            try:
                data = json.loads(raw_text)
                return data, None
            except json.JSONDecodeError:
                return None, f"Failed to parse JSON: {raw_text}"
                
        except Exception as e:
            err_msg = str(e)
            
            # Fail fast for auth/API key errors, no point in retrying
            if "API_KEY" in err_msg or "ADC found" in err_msg or "401" in err_msg or "403" in err_msg:
                return None, f"Authentication error: {err_msg}"
                
            if attempt < retries - 1:
                time.sleep(backoffs[attempt])
            else:
                return None, f"API failed after {retries} attempts. Last error: {err_msg}"
                
    return None, "Unknown failure"

def process_receipt_ai(image_path, escalate_to_pro=False):
    """
    Calls Flash first. If escalation is requested, calls Pro.
    """
    if not escalate_to_pro:
        return call_gemini(image_path, model_name="gemini-3.5-flash")
    else:
        return call_gemini(image_path, model_name="gemini-2.5-pro")

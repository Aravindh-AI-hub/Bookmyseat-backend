import re
import html
from typing import Optional
from utils.constants import BUDGET_KEYWORDS

def parse_price(price_str: str) -> float:
    """Convert price string to float (handles ₹, commas, HTML entities)"""
    try:
        price_str = html.unescape(price_str)
        price_str = re.sub(r'[₹,\s]', '', price_str)
        match = re.search(r'\d+\.?\d*', price_str)
        return float(match.group()) if match else 0.0
    except:
        return 0.0

def detect_budget_query(message: str) -> Optional[float]:
    """Check if user is asking for budget tickets"""
    msg_lower = message.lower()
    
    # Check keyword matches
    for keyword, price in BUDGET_KEYWORDS.items():
        if keyword in msg_lower:
            return price
    
    # Check price range patterns
    patterns = [
        r'under\s+(\d+)', r'below\s+(\d+)', r'less\s+than\s+(\d+)',
        r'maximum\s+(\d+)', r'max\s+(\d+)', r'upto\s+(\d+)', r'up\s+to\s+(\d+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, msg_lower)
        if match:
            return float(match.group(1))
    
    return None

def normalize_text(text: str) -> str:
    """Clean and normalize text"""
    return text.strip().lower()

def decode_html_entities(text: str) -> str:
    """Decode HTML entities in text"""
    return html.unescape(text)
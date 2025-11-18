from typing import List
from utils.parsers import detect_budget_query
from utils.constants import SLANG_MAPPING, SEAT_CATEGORIES

class FilterService:
    """Handle user query filtering and detection"""
    
    @staticmethod
    def detect_budget(message: str) -> float | None:
        """Detect if user wants budget tickets"""
        return detect_budget_query(message)
    
    @staticmethod
    def detect_category(message: str) -> List[str]:
        """Detect seat category preferences from user message"""
        msg = message.lower()
        wanted = set()
        
        # Check slang mappings
        for slang, categories in SLANG_MAPPING.items():
            if slang in msg:
                wanted.update(categories)
        
        # Check direct category names
        for cat in SEAT_CATEGORIES:
            if cat and cat.lower() in msg:
                wanted.add(cat)
        
        return list(wanted)
    
    @staticmethod
    def build_filter_dict(budget_price: float | None = None, categories: List[str] | None = None) -> dict:
        """Build filter dictionary from detected values"""
        filters = {"only_available": True}
        
        if budget_price:
            filters["price_max"] = budget_price
        
        if categories:
            filters["category"] = categories
        
        return filters
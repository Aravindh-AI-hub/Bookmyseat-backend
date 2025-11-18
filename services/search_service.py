from typing import List, Dict, Optional, Union
from utils.parsers import parse_price
from database.db_manager import DatabaseManager

class SearchService:
    """Search and filter movie database"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def search(
        self,
        movie_name: Optional[Union[str, List[str]]] = None,
        theater_name: Optional[Union[str, List[str]]] = None,
        filters: Optional[dict] = None
    ) -> List[Dict]:
        """Search database with filters"""
        
        results = []
        only_available = filters.get("only_available", True) if filters else True
        
        # Normalize inputs to lists
        movies = [movie_name] if isinstance(movie_name, str) else (movie_name or [])
        theaters = [theater_name] if isinstance(theater_name, str) else (theater_name or [])
        
        for item in self.db.get_raw_data():
            # Check availability
            print("Iterm:",item)
            if only_available and not item.get("is_available", False):
                continue
            
            # Filter by movie
            if movies:
                print("movies:",movies)
                if not any(m.lower() in item["movie_name"].lower() for m in movies):
                    continue
            
            # Filter by theater
            if theaters:
                if not any(t.lower() in item["theater_name"].lower() for t in theaters):
                    continue
            
            # Filter by price
            if filters and "price_max" in filters:
                if parse_price(item["price"]) > filters["price_max"]:
                    continue
            
            # Filter by category
            if filters and "category" in filters:
                wanted = set(c.upper() for c in filters["category"])
                item_cat = item["category"].strip().upper() or "REGULAR"
                if item_cat not in wanted:
                    continue
            
            # Filter by language
            if filters and "language" in filters:
                if filters["language"].lower() != item["movie_language"].lower():
                    continue
            
            # Filter by format
            if filters and "format" in filters:
                if filters["format"].lower() not in item["movie_format"].lower():
                    continue
            
            results.append(item)
        
        # Sort by price (cheapest first)
        results.sort(key=lambda x: parse_price(x["price"]))


        return results
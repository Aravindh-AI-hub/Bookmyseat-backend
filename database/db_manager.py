import json
import os
from typing import List, Dict, Tuple
from config import DB_PATH

class DatabaseManager:
    """Manage movie database operations"""
    
    def __init__(self):
        self.db_path = DB_PATH
        self.data = []
        self.metadata = {}
        self.load()
    
    def load(self) -> Tuple[List[Dict], Dict]:
        """Load database from JSON file"""
        try:
            if not os.path.exists(self.db_path):
                raise FileNotFoundError(f"Database not found at {self.db_path}")
            
            with open(self.db_path, 'r', encoding='utf-8') as f:
                db = json.load(f)
                self.data = db.get('data', [])
                self.metadata = db.get('scrape_metadata', {})
                print(f"✓ Loaded {len(self.data)} shows from database")
        except Exception as e:
            print(f"✗ Database load error: {e}")
            self.data = []
            self.metadata = {}
        
        return self.data, self.metadata
    
    def get_all_movies(self) -> List[str]:
        """Get unique movie names"""
        return list(set([item['movie_name'] for item in self.data]))
    
    def get_all_theaters(self) -> List[str]:
        """Get unique theater names"""
        return list(set([item['theater_name'] for item in self.data]))
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        available = sum(1 for m in self.data if m.get('is_available', False))
        
        return {
            "total_movies": len(self.get_all_movies()),
            "total_theaters": len(self.get_all_theaters()),
            "total_shows": len(self.data),
            "available_tickets": available,
            "last_updated": self.metadata.get('scrape_start_time', 'Unknown')
        }
    
    def get_raw_data(self) -> List[Dict]:
        """Get all database records"""
        return self.data
    
    def refresh(self) -> None:
        """Reload database from file"""
        self.load()
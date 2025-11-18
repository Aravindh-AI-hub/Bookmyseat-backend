
from typing import Dict, List, Optional
from datetime import datetime
from utils.parsers import parse_price
import html

class FormatterService:
    """Format search results for API responses with static structure"""
    
    # Static response structure template
    RESPONSE_TEMPLATE = {
        "count": 0,
        "date": "",
        "data_updated": "",
        "intent": "",
        "results": [],
        "metadata": {
            "status": "success",
            "message": ""
        }
    }
    
    @staticmethod
    def format_response(intent: str, results: List[Dict], scrape_date: str, user_query: str = "") -> Dict:
        """Format results based on intent type with static structure"""
        current_date = datetime.now().strftime("%d %B %Y")
        
        # Create base response from template
        response = FormatterService.RESPONSE_TEMPLATE.copy()
        response.update({
            "count": len(results),
            "date": current_date,
            "data_updated": scrape_date,
            "intent": intent,
            "metadata": {
                "status": "success" if results else "no_results",
                "message": FormatterService._get_status_message(intent, len(results))
            }
        })
        
        print("intent:",intent)
        # Format results based on intent
        print("formate response result len: ",len(results))
        if intent == "movies_list":
            print("1")
            response["results"] = FormatterService._group_by_movie(results)
        elif intent == "showtimes":
            print("2")
            response["results"] = FormatterService._format_showtimes(results)
        elif intent == "pricing" or intent == "budget_tickets":
            print("3")
            response["results"] = FormatterService._format_tickets(results)
        elif intent == "theater_info":
            print("4")
            response["results"] = FormatterService._group_by_theater(results)
        elif intent == "greeting":
            print("5")
            response["results"] = FormatterService._greeting(results)
        else:
            print("6")
            response["results"] = FormatterService._format_results(results)
        
        return response
    
    @staticmethod
    def _get_status_message(intent: str, count: int) -> str:
        """Generate status message based on intent and result count"""
        if count == 0:
            return f"No {intent.replace('_', ' ')} found"
        return f"Found {count} {intent.replace('_', ' ')}"
    
    @staticmethod
    def _format_showtimes(results: List[Dict]) -> List[Dict]:
        """Format showtime data with consistent structure"""
        seen = set()
        showtimes = []
        
        for r in results:
            key = f"{r['movie_name']}_{r['theater_name']}_{r['showtime']}"
            if key not in seen:
                showtimes.append({
                    "movie_name": r.get("movie_name", "N/A"),
                    "theater_name": r.get("theater_name", "N/A"),
                    "showtime": r.get("showtime", "N/A"),
                    "price": html.unescape(r.get("price", "N/A")),
                    "category": r.get("category", "STANDARD"),
                    "movie_language": r.get("movie_language", "N/A"),
                    "format": r.get("movie_format", "2D"),
                    "screen_type":r.get("screen_type", "N/A"),
                    "is_available":r.get("availability","N/A"),
                    "poster_url":r.get("poster_url")
                })
                seen.add(key)
        
        return showtimes
    
    @staticmethod
    def _format_tickets(results: List[Dict]) -> List[Dict]:
        """Format ticket pricing data with consistent structure"""
        return [
            {
                "movie_name": r.get("movie_name", "N/A"),
                "theater_name": r.get("theater_name", "N/A"),
                "showtime": r.get("show_time", "N/A"),
                "category": r.get("category", "STANDARD"),
                "price": html.unescape(r.get("price", "N/A")),
                "movie_language": r.get("movie_language", "N/A"),
                "format": r.get("movie_format", "2D"),
                "screen_type":r.get("screen_type", "N/A"),
                "is_available":r.get("availability","N/A"),
                "poster_url":r.get("poster_url")

            }
            for r in results
        ]
    
    @staticmethod
    def _group_by_movie(results: List[Dict]) -> List[Dict]:
        """Flatten results by movie with consistent structure - one object per movie-theater-showtime combination"""
        flattened = []
        seen = set()
        
        print("grou by cinema result len: ",len(results))
        for r in results:
            key = f"{r.get('movie_name')}_{r.get('theater_name')}_{r.get('showtime')}"
            if key not in seen:
                flattened.append({
                    "movie_name": r.get("movie_name", "N/A"),
                    "movie_language": r.get("movie_language", "N/A"),
                    "format": r.get("movie_format", "2D"),
                    "rating": r.get("movie_rating", "N/A"),
                    "theater_name": r.get("theater_name", "N/A"),
                    "showtime": r.get("showtime", "N/A"),
                    "price": html.unescape(r.get("price", "N/A")),
                    "category": r.get("category", "STANDARD"),
                    "screen_type":r.get("screen_type", "N/A"),
                    "is_available":r.get("availability","N/A"),
                    "poster_url":r.get("poster_url")

                })
                seen.add(key)
        
        return flattened
    
    @staticmethod
    def _group_by_theater(results: List[Dict]) -> Dict[str, Dict]:
        """Group results by theater with consistent structure"""
        theaters = {}
        for r in results:
            t = r.get("theater_name", "Unknown")
            if t not in theaters:

                theaters[t] = {
                    "theater_name": t,
                    "address": r.get("theater_address", "N/A"),
                    "city": r.get("theater_city", "N/A"),
                    "movies": [],
                    "categories": set()
                }
            
            movie = r.get("movie_name")
            if movie and movie not in theaters[t]["movies"]:
                theaters[t]["movies"].append(movie)
            
            category = r.get("category")
            if category:
                theaters[t]["categories"].add(category)
        
        # Convert sets to lists for JSON serialization
        for t in theaters:
            theaters[t]["categories"] = list(theaters[t]["categories"])
        
        return theaters
    
    @staticmethod
    def _format_results(results: List[Dict]) -> List[Dict]:
        """Generic result formatting with consistent structure"""
        return [
            {
                "movie_name": r.get("movie_name", "N/A"),
                "theater_name": r.get("theater_name", "N/A"),
                "showtime": r.get("showtime", "N/A"),
                "price": html.unescape(r.get("price", "N/A")),
                "category": r.get("category", "STANDARD"),
                "movie_language": r.get("movie_language", "N/A"),
                "format": r.get("movie_format", "2D"),
                "rating": r.get("movie_rating", "N/A"),
                "screen_type":r.get("screen_type", "N/A"),
                "is_available":r.get("availability","N/A"),
                "poster_url":r.get("poster_url")

            }
            for r in results
        ]
    @staticmethod
    def _greeting(results: List[Dict]) -> List[Dict]:
        """Generic result formatting with consistent structure"""
        return [
            {
                "movie_name":None,
                "theater_name":None,
                "showtime":None,
                "price": None,
                "category":None,
                "movie_language":None,
                "format":None,
                "rating":None,
                "screen_type":None,
                "is_available":None,
                "poster_url":None
            }
        ]
    

    
    @staticmethod
    def add_user_response(data: Dict, user_query: str, response_text: str) -> Dict:
        """Add user query and AI response to formatted data"""
        data["user_query"] = user_query
        data["response"] = response_text
        return data
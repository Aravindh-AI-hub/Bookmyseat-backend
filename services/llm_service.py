import json
from groq import Groq
from typing import Dict, List
from config import GROQ_API_KEY, GROQ_MODEL, LLM_TEMPERATURE
from prompts.system_prompts import get_intent_system_prompt, get_response_system_prompt
from database.db_manager import DatabaseManager
from services.filter_service import FilterService
from utils.constants import SEAT_CATEGORIES

class LLMService:
    """Handle LLM interactions for intent understanding and responses"""
    
    def __init__(self, db_manager: DatabaseManager):
        # print("keey:",GROQ_API_KEY)
        self.client = Groq(api_key=GROQ_API_KEY)
        self.db = db_manager
        self.filter_service = FilterService()
    
    def understand_intent(self, user_message: str, scrape_date: str) -> Dict:
        """Parse user message and extract intent + filters"""
        try:
            # Detect budget and category early
            budget_price = self.filter_service.detect_budget(user_message)
            categories = self.filter_service.detect_category(user_message)
            
            # Get system prompt
            movies = self.db.get_all_movies()
            theaters = self.db.get_all_theaters()
            system = get_intent_system_prompt(movies, theaters, SEAT_CATEGORIES, scrape_date)
            
            # Call LLM
            # print("Model: ",GROQ_MODEL)
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_message}
                ],
                model=GROQ_MODEL,
                temperature=LLM_TEMPERATURE,
                response_format={"type": "json_object"}
            )
            
            llm_response = json.loads(response.choices[0].message.content)
            
            # Enrich with detected filters
            filters = llm_response.get("filters", {})
            if budget_price:
                filters["price_max"] = budget_price
            if categories:
                filters["category"] = categories
            filters["only_available"] = True
            
            llm_response["filters"] = filters
            return llm_response
        
        except Exception as e:
            print(f"Intent understanding error: {e}")
            return {
                "intent": "general",
                "movie_name": None,
                "theater_name": None,
                "filters": {"only_available": True}
            }
    
    def generate_response(self, user_message: str, search_results: List[Dict], scrape_date: str, current_date: str) -> str:
        """Generate natural language response from search results"""
        try:
            # Build summary
            summary = []
            for item in search_results[:20]:
                summary.append({
                    "movie": item["movie_name"],
                    "theater": item["theater_name"],
                    "time": item["showtime"],
                    "price": item["price"],
                    "category": item["category"],
                })
            
            system = get_response_system_prompt(scrape_date, current_date)
            # messages=[
            #         {"role": "system", "content": system},
            #         {"role": "user", "content": f"Query: {user_message}\n\nResults: {json.dumps(summary, ensure_ascii=False)}"}
            #     ]
            # # print("\nMessage:",messages,"\n\n---")
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": f"Query: {user_message}\n\nResults: {json.dumps(summary, ensure_ascii=False)}"}
                ],
                model=GROQ_MODEL,
                temperature=0.4,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            print("Model response: ",response)
            return result.get("response", "No shows found matching your criteria.")
        
        except Exception as e:
            print(f"Response generation error: {e}")
            return f"Found {len(search_results)} shows matching your query."
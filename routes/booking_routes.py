from fastapi import APIRouter, HTTPException
from datetime import datetime
from models.requests import UserTextRequest, UserTextResponse, HealthResponse
from database.db_manager import DatabaseManager
from services.llm_service import LLMService
from services.search_service import SearchService
from services.formatter_service import FormatterService

router = APIRouter(prefix="/api", tags=["booking"])

# Initialize services
db_manager = DatabaseManager()
llm_service = LLMService(db_manager)
search_service = SearchService(db_manager)

@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint with stats"""
    stats = db_manager.get_stats()
    return HealthResponse(
        status="healthy",
        message="🎬 Movie Booking Assistant running",
        stats=stats
    )

@router.post("/chat", response_model=UserTextResponse)
def chat(request: UserTextRequest):
    """Main chat endpoint for user queries"""
    try:
        user_message = request.message.strip()
        if not user_message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        scrape_date = db_manager.metadata.get("scrape_start_time", "Unknown")

        # print("scrapedata ",scrape_date)
        # Step 1: Understand intent
        print("User: ",user_message)
        print("scrape data: ",scrape_date)
        intent_data = llm_service.understand_intent(user_message, scrape_date)
        
        # Step 2: Search database

        print("intent data:",intent_data)
        results = search_service.search(
            movie_name=intent_data.get("movie_name"),
            theater_name=intent_data.get("theater_name"),
            filters=intent_data.get("filters", {})
        )

        print("Lenght od result:",len(results))
        
        # Step 3: Generate response
        response_text = llm_service.generate_response(
            user_message,
            results,
            scrape_date,
            datetime.now().strftime("%d %B %Y")
        )
        
        # Step 4: Format data
    
        formatted_data = FormatterService.format_response(
            intent_data.get("intent", "general"),
            results,
            scrape_date
        )
        # print("Formated data: ",formatted_data)
        return UserTextResponse(
            user_query=user_message,
            response=response_text,
            data=formatted_data
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/movies")
def get_movies():
    """Get all available movies"""
    return {
        "movies": db_manager.get_all_movies(),
        "count": len(db_manager.get_all_movies())
    }

@router.get("/theaters")
def get_theaters():
    """Get all theaters"""
    return {
        "theaters": db_manager.get_all_theaters(),
        "count": len(db_manager.get_all_theaters())
    }

@router.post("/refresh-db")
def refresh_database():
    """Manually refresh database from file"""
    db_manager.refresh()
    return {"status": "success", "message": "Database refreshed"}
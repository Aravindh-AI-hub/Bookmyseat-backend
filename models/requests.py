from pydantic import BaseModel
from typing import Optional, Dict, Any

class UserTextRequest(BaseModel):
    """User text query request"""
    message: str

    class Config:
        example = {"message": "Show me premium tickets for Kantara"}

class UserTextResponse(BaseModel):
    """User text response with data"""
    user_query: str
    response: str
    data: Optional[Dict[str, Any]] = None

    class Config:
        example = {
            "user_query": "Premium tickets",
            "response": "Found 5 premium shows...",
            "data": {"count": 5, "results": []}
        }

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    stats: Optional[Dict[str, Any]] = None
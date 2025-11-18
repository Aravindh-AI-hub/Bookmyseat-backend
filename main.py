from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import API_TITLE, API_VERSION, CORS_ORIGINS, CORS_CREDENTIALS, CORS_METHODS, CORS_HEADERS
from routes.booking_routes import router as booking_router
from config import * 
# Initialize FastAPI
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description="AI-powered movie booking assistant with Groq LLM",
    contact={
        "name": "Aravindh - AI Engineer",
        "email": "aravindhvignesh58@gmail.com"
    },
    license_info={
        "name": "Developed by Aravindh (AI Engineer)",
        "url": "https://www.linkedin.com/public-profile/settings?trk=d_flagship3_profile_self_view_public_profile"
    }
)


#api key removed 
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# Include routes
app.include_router(booking_router)

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": f"🎬{API_TITLE}",
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    #Server
    uvicorn.run(app, host="0.0.0.0", port=8000)




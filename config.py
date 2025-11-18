import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_TITLE = "Vikas-X Movie Booking Agent"
API_VERSION = "3.0"
API_HOST = "localhost"
API_PORT = 8000

# LLM Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY") #
GROQ_MODEL = "llama-3.1-8b-instant"#"llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.3
LLM_RESPONSE_FORMAT = {"type": "json_object"}

# Database
DB_PATH = "data\movie.json"

# Budget thresholds
BUDGET_MAX_PRICE = 60
BUDGET_MIN_PRICE = 54

# Search limits
SEARCH_RESULTS_LIMIT = 30
SHOW_SUMMARY_LIMIT = 30

# CORS
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]
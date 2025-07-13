import os

class Config:
    # ... other configurations ...
    
    HF_API_URL = "https://api-inference.huggingface.co/models"
    HF_MODELS = {
        "sentiment": "distilbert-base-uncased-finetuned-sst-2-english",
        "fake-news": "hello-simpleai/roberta-base-fake-news"
    }
    HF_API_TOKEN = ""  # Get from https://huggingface.co/settings/tokens
    # PostgreSQL Configuration
    DB_CONFIG = {
        "host": "localhost",
        "database": "realestate_db",
        "user": "postgres",
        "password": "1122qqww$",  # Change to your PostgreSQL password
        "port": "5432",
        "connect_timeout": 5
    }
    
    # Add other configurations...

    # File paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CSV_FILE = os.path.join(BASE_DIR, "data/property_data.csv")
    IMAGE_FOLDER = os.path.join(BASE_DIR, "data/property_images")
    
    # Flask settings
    SECRET_KEY = "your-secret-key-here"
    TEMPLATES_AUTO_RELOAD = True
    
    
    # Gemini API
    GEMINI_API_KEY = ""
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
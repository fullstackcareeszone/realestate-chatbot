import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # HuggingFace Configuration
    HF_API_URL = "https://api-inference.huggingface.co/models"
    HF_MODELS = {
        "sentiment": "distilbert-base-uncased-finetuned-sst-2-english",
        "fake-news": "hello-simpleai/roberta-base-fake-news"
    }
    HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")  # Empty default for security

    # PostgreSQL Configuration
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "realestate_db"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", ""),  # Empty default
        "port": os.getenv("DB_PORT", "5432"),
        "connect_timeout": 5
    }
    
    # File paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CSV_FILE = os.path.join(BASE_DIR, "data/property_data.csv")
    IMAGE_FOLDER = os.path.join(BASE_DIR, "data/property_images")
    
    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24).hex())  # Random default
    TEMPLATES_AUTO_RELOAD = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    # Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")  # Empty default
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    @staticmethod
    def init_app(app):
        """Initialize configuration with Flask app"""
        pass


class DevelopmentConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    DEBUG = True


class ProductionConfig(Config):
    TEMPLATES_AUTO_RELOAD = False
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///properties.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Scraper configuration
    ZAMEEN_BASE_URL = "https://www.zameen.com/"
    SCRAPE_LIMIT = 50  # Number of properties to scrape
    SCRAPE_INTERVAL = 86400  # 24 hours in seconds
    
    # LLM configuration
    LLM_ENDPOINT = os.getenv('LLM_ENDPOINT', 'http://localhost:8080/vi/completions')
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
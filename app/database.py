from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

db = SQLAlchemy()

def init_db(app):
    """Initialize the database"""
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
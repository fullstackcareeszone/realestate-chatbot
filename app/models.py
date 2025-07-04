from datetime import datetime
from app import db

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    area = db.Column(db.Float)  # in sqft
    description = db.Column(db.Text)
    amenities = db.Column(db.Text)  # JSON string of amenities
    image_url = db.Column(db.String(300))
    url = db.Column(db.String(300), unique=True)
    source = db.Column(db.String(50), default='zameen')
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    scraped_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'location': self.location,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'area': self.area,
            'description': self.description,
            'amenities': self.amenities,
            'image_url': self.image_url,
            'url': self.url,
            'source': self.source
        }

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), nullable=False)
    query = db.Column(db.String(300), nullable=False)
    response_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
from flask import Flask, render_template, request, jsonify,redirect , url_for
import requests
from zameen_scraper import ZameenScraper  
from fake_detection import FakeDetector
from database import Database
import logging as logger
from config import Config
import os
import time

app = Flask(__name__)
app.config.from_object(Config)
scraper = ZameenScraper()
property_data = scraper.scrape_property("https://www.zameen.com/property/example.html")

# Initialize components
db = Database()
detector = FakeDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url')
    if not url or not url.startswith('http'):
        return render_template('index.html', error="Please enter a valid URL starting with http")

    try:
        # Scrape property data
        property_data = scraper.scrape_property(url)
        if not property_data:
            return render_template('index.html', error="Failed to scrape property data")

        # Perform analysis
        analysis = detector.full_analysis(property_data)
        
        # Prepare template data
        template_data = {
            'property': {
                'title': property_data.get('title', 'No title'),
                'price': property_data.get('price', 'Not specified'),
                'location': property_data.get('location', 'Not specified'),
                'description': property_data.get('description', 'No description provided'),
                'image_urls': property_data.get('image_urls', [])[:3]  # First 3 images
            },
            'analysis': analysis,
            'error': None
        }

        # Save to database
        property_data['analysis'] = analysis
        if not db.save_property(property_data):
            logger.warning("Database save completed with possible issues")

        return render_template('output.html', **template_data)

    except Exception as e:
        logger.error(f"Analysis pipeline failed: {str(e)}", exc_info=True)
        return render_template(
            'index.html',
            error="Technical error during analysis. Please try again later."
        )
@app.route('/history')
def history():
    history_data = db.get_history()
    return render_template('history.html', history=history_data)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Process contact form
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Here you would typically send an email
        # For now, just log it
        logger.info(f"Contact form submitted: {name}, {email}, {message}")
        
        return render_template('contact.html', success=True)
    
    return render_template('contact.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        message = request.json.get('message')
        
        # Call Gemini API
        response = requests.post(
            f"{app.config['GEMINI_API_URL']}?key={app.config['GEMINI_API_KEY']}",
            json={
                "contents": [{
                    "parts": [{"text": f"You are a real estate assistant. Respond to this: {message}"}]
                }]
            }
        )
        
        response.raise_for_status()
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            reply = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'reply': reply})
        
        return jsonify({'reply': "I couldn't process that request. Please try again."})
    except Exception as e:
        logger.error(f"Chatbot error: {e}")
        return jsonify({'reply': "Sorry, I'm having trouble responding right now."})

if __name__ == '__main__':
    # Ensure data directories exist
    os.makedirs(app.config['IMAGE_FOLDER'], exist_ok=True)
    os.makedirs(os.path.dirname(app.config['CSV_FILE']), exist_ok=True)
    
    # Create database tables
    db.create_tables()
    
    app.run(debug=True)
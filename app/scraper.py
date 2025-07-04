import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json
from datetime import datetime
from models import Property, db
from config import Config
import time

class ZameenScraper:
    def __init__(self):
        self.base_url = Config.ZAMEEN_BASE_URL
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_properties(self, limit=Config.SCRAPE_LIMIT):
        """Scrape properties from Zameen.com and save to database"""
        try:
            url = urljoin(self.base_url, "Property/dubai/")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            property_cards = soup.select('article[role="article"]')[:limit]
            
            for card in property_cards:
                self.process_property_card(card)
                time.sleep(1)  # Be polite with requests
            
            print(f"Successfully scraped {len(property_cards)} properties")
            
        except Exception as e:
            print(f"Error scraping properties: {str(e)}")
    
    def process_property_card(self, card):
        """Process individual property card and save to database"""
        try:
            # Extract property URL
            link = card.find('a', href=True)
            if not link:
                return
            
            property_url = urljoin(self.base_url, link['href'])
            
            # Check if property already exists in database
            if Property.query.filter_by(url=property_url).first():
                return
            
            # Extract basic info
            title = card.find('h2').get_text(strip=True) if card.find('h2') else "No Title"
            location = card.find('div', {'aria-label': 'Location'}).get_text(strip=True) if card.find('div', {'aria-label': 'Location'}) else "Unknown"
            
            # Extract price
            price_text = card.find('span', {'aria-label': 'Price'}).get_text(strip=True) if card.find('span', {'aria-label': 'Price'}) else "0"
            price = self.parse_price(price_text)
            
            # Extract details
            details = card.find_all('span', {'aria-label': True})
            bedrooms, bathrooms, area = 0, 0, 0
            
            for detail in details:
                if 'Bed' in detail['aria-label']:
                    bedrooms = int(re.search(r'\d+', detail.get_text(strip=True)).group())
                elif 'Bath' in detail['aria-label']:
                    bathrooms = int(re.search(r'\d+', detail.get_text(strip=True)).group())
                elif 'Area' in detail['aria-label']:
                    area_text = detail.get_text(strip=True)
                    area = float(re.search(r'[\d,]+', area_text.replace(',', '')).group())
            
            # Extract image URL
            image = card.find('img')
            image_url = image['src'] if image and 'src' in image.attrs else None
            
            # Now scrape the individual property page for more details
            property_details = self.scrape_property_details(property_url)
            
            # Create and save property
            property = Property(
                title=title,
                price=price,
                location=location,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                area=area,
                description=property_details.get('description', ''),
                amenities=json.dumps(property_details.get('amenities', [])),
                image_url=image_url,
                url=property_url
            )
            
            db.session.add(property)
            db.session.commit()
            
        except Exception as e:
            print(f"Error processing property card: {str(e)}")
            db.session.rollback()
    
    def scrape_property_details(self, url):
        """Scrape additional details from property page"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract description
            description_section = soup.find('div', {'class': 'description'})
            description = description_section.get_text(strip=True) if description_section else ""
            
            # Extract amenities
            amenities = []
            amenities_section = soup.find('div', {'aria-label': 'Amenities'})
            if amenities_section:
                amenities = [item.get_text(strip=True) for item in amenities_section.find_all('li')]
            
            return {
                'description': description,
                'amenities': amenities
            }
            
        except Exception as e:
            print(f"Error scraping property details: {str(e)}")
            return {'description': '', 'amenities': []}
    
    def parse_price(self, price_text):
        """Convert price text to numeric value"""
        try:
            # Remove currency symbols and commas
            clean_text = re.sub(r'[^\d.]', '', price_text)
            return float(clean_text)
        except:
            return 0.0

def run_scraper():
    """Run the scraper and update database"""
    scraper = ZameenScraper()
    scraper.scrape_properties()
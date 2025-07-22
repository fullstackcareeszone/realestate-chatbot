import time
import psycopg2
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import random
import urllib.request
from urllib.parse import urlparse
import warnings
import logging
from PIL import Image
import io
from config import Config
from bs4 import BeautifulSoup
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Suppress warnings
warnings.filterwarnings("ignore")

class ZameenScraper:
    def __init__(self):
        self.config = Config()
        self.csv_file = self.config.CSV_FILE
        self.image_folder = self.config.IMAGE_FOLDER
        os.makedirs(self.image_folder, exist_ok=True)
        
    def setup_driver(self):
        """Configure and return a Chrome WebDriver with anti-bot evasion techniques"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--log-level=3")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), 
            options=options
        )
        
        # Evade bot detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def save_images(self, image_urls, property_id):
        """Download and save images locally with improved error handling"""
        saved_paths = []
        if not image_urls:
            return saved_paths
        
        for i, img_url in enumerate(image_urls[:10]):  # Limit to 10 images
            try:
                if not img_url or not img_url.startswith('http'):
                    continue
                    
                # Generate filename
                parsed = urlparse(img_url)
                ext = os.path.splitext(parsed.path)[1] or '.jpg'
                img_name = f"{property_id}_{i+1}{ext}"
                img_path = os.path.join(self.image_folder, img_name)
                
                # Download with timeout
                headers = {'User-Agent': 'Mozilla/5.0'}
                req = urllib.request.Request(img_url, headers=headers)
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    img_data = response.read()
                    
                    # Verify and save image
                    try:
                        img = Image.open(io.BytesIO(img_data))
                        img.verify()
                        with open(img_path, 'wb') as f:
                            f.write(img_data)
                        saved_paths.append(img_path)
                        logger.info(f"Saved image: {img_path}")
                    except Exception as e:
                        logger.warning(f"Invalid image {img_url}: {e}")
                
            except Exception as e:
                logger.error(f"Error saving image {img_url}: {e}")
        
        return saved_paths

    def scrape_property_details(self, driver, url):
        """Scrape all property details with robust error handling"""
        property_data = {'url': url}
        try:
            # Load page with random delays
            driver.get(url)
            time.sleep(random.uniform(1, 3))
            
            # Use both Selenium and BeautifulSoup for redundancy
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract title
            title = self._extract_with_fallbacks(
                driver,
                soup,
                [
                    ('//h1[@aria-label="Property title"]', 'xpath'),
                    ('h1._64bb5b3b', 'css'),
                    ('h1', 'tag')
                ]
            )
            property_data['title'] = title
            
            # Extract price
            price = self._extract_with_fallbacks(
                driver,
                soup,
                [
                    ('//span[@aria-label="Price"]', 'xpath'),
                    ('span._812aa185', 'css'),
                    ('span[class*="price"]', 'css')
                ]
            )
            property_data['price'] = price
            
            # Extract location
            location = self._extract_with_fallbacks(
                driver,
                soup,
                [
                    ('//div[@aria-label="Property header"]', 'xpath'),
                    ('div._162e6469', 'css'),
                    ('div[class*="location"]', 'css')
                ]
            )
            property_data['location'] = location
            
            # Extract key features
            features = self._extract_features(driver, soup)
            property_data.update(features)
            
            # Extract description
            description = self._extract_description(driver, soup)
            property_data['description'] = description
            
            # Extract images
            property_data['image_urls'] = self._extract_images(driver, soup)
            
            return property_data
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None

    def _extract_with_fallbacks(self, driver, soup, selectors):
        """Try multiple selectors until success"""
        for selector, selector_type in selectors:
            try:
                if selector_type == 'xpath':
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    return element.text.strip()
                elif selector_type == 'css':
                    element = soup.select_one(selector)
                    if element:
                        return element.get_text(strip=True)
                elif selector_type == 'tag':
                    element = soup.find(selector)
                    if element:
                        return element.get_text(strip=True)
            except Exception:
                continue
        return None

    def _extract_features(self, driver, soup):
        """Extract bedrooms, bathrooms, area, etc."""
        features = {
            'bedrooms': None,
            'bathrooms': None,
            'area': None,
            'type': None,
            'purpose': None,
            'added': None
        }
        
        # Try to find feature containers
        containers = [
            ('//div[contains(@class, "property-features")]', 'xpath'),
            ('div._6dfa2a3a', 'css'),  # Zameen's feature container
            ('ul._033281ab', 'css')    # Alternative container
        ]
        
        feature_text = ""
        for selector, selector_type in containers:
            try:
                if selector_type == 'xpath':
                    container = driver.find_element(By.XPATH, selector)
                    feature_text = container.text
                    break
                elif selector_type == 'css':
                    container = soup.select_one(selector)
                    if container:
                        feature_text = container.get_text()
                        break
            except Exception:
                continue
        
        # Extract features using regex
        if feature_text:
            bedroom_match = re.search(r'(\d+)\s*(Bed|Beds|Bedroom)', feature_text, re.I)
            if bedroom_match:
                features['bedrooms'] = bedroom_match.group(1)
                
            bathroom_match = re.search(r'(\d+)\s*(Bath|Baths|Bathroom)', feature_text, re.I)
            if bathroom_match:
                features['bathrooms'] = bathroom_match.group(1)
                
            area_match = re.search(r'(\d+)\s*(Sq\.?|Square|Marla|Kanal)', feature_text, re.I)
            if area_match:
                features['area'] = f"{area_match.group(1)} {area_match.group(2)}"
                
            type_match = re.search(r'Type:\s*([^\n]+)', feature_text, re.I)
            if type_match:
                features['type'] = type_match.group(1).strip()
                
            purpose_match = re.search(r'Purpose:\s*([^\n]+)', feature_text, re.I)
            if purpose_match:
                features['purpose'] = purpose_match.group(1).strip()
                
            added_match = re.search(r'Added:\s*([^\n]+)', feature_text, re.I)
            if added_match:
                features['added'] = added_match.group(1).strip()
        
        return features

    def _extract_description(self, driver, soup):
        """Extract property description with read-more expansion"""
        description = ""
        
        # Try to expand description if "Read More" exists
        try:
            read_more = driver.find_element(By.XPATH, '//button[contains(text(), "Read More")]')
            driver.execute_script("arguments[0].click();", read_more)
            time.sleep(1)
        except Exception:
            pass
        
        # Try multiple description selectors
        selectors = [
            ('//div[@aria-label="Description"]', 'xpath'),
            ('div._812aa185', 'css'),
            ('div[class*="description"]', 'css')
        ]
        
        for selector, selector_type in selectors:
            try:
                if selector_type == 'xpath':
                    element = driver.find_element(By.XPATH, selector)
                    description = element.text.strip()
                    break
                elif selector_type == 'css':
                    element = soup.select_one(selector)
                    if element:
                        description = element.get_text(strip=True)
                        break
            except Exception:
                continue
                
        return description

    def _extract_images(self, driver, soup):
        """Extract property image URLs with multiple approaches"""
        image_urls = []
        
        # Approach 1: Find image gallery
        try:
            gallery = driver.find_element(By.XPATH, '//div[contains(@class, "gallery")]')
            images = gallery.find_elements(By.TAG_NAME, 'img')
            image_urls.extend([img.get_attribute('src') for img in images if img.get_attribute('src')])
        except Exception:
            pass
        
        # Approach 2: Find all images with certain classes
        img_selectors = [
            'img[class*="image"]',
            'img[class*="photo"]',
            'img[loading="lazy"]'
        ]
        
        for selector in img_selectors:
            try:
                images = soup.select(selector)
                for img in images:
                    src = img.get('src')
                    if src and src.startswith('http'):
                        image_urls.append(src)
            except Exception:
                continue
        
        # Deduplicate and filter
        image_urls = list(set(image_urls))
        image_urls = [url for url in image_urls if url and any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp'])]
        
        return image_urls[:20]  # Return max 20 images

    def scrape_property(self, url):
        """Main method to scrape a single property"""
        driver = None
        try:
            driver = self.setup_driver()
            property_data = self.scrape_property_details(driver, url)
            return property_data
        except Exception as e:
            logger.error(f"Error in scrape_property: {e}")
            return None
        finally:
            if driver:
                driver.quit()

if __name__ == "__main__":
    scraper = ZameenScraper()
    test_url = "https://www.zameen.com/property/details-123.html"
    data = scraper.scrape_property(test_url)
    print(data) 
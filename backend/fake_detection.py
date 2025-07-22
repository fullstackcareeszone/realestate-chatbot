import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

class FakeDetector:
    def __init__(self):
        self.config = Config()
        self.timeout = 15

    def analyze_text(self, description, title, price):
        """Analyze property text with multiple checks"""
        analysis = {
            'is_suspicious': False,
            'reasons': [],
            'confidence': 0.5,
            'recommendation': 'Analysis completed',
            'final_verdict': 'Analysis completed with basic checks'
        }

        # Basic price checks
        price_str = str(price or "").lower()
        if not price_str.strip():
            analysis['reasons'].append("Price information missing")
        elif "negotiable" in price_str or "contact" in price_str:
            analysis['reasons'].append("Non-fixed price indication")
            analysis['confidence'] = min(1.0, analysis['confidence'] + 0.2)

        # Only proceed with API if token exists
        if not self.config.HF_API_TOKEN:
            analysis['reasons'].append("Advanced analysis unavailable (no API token)")
            return analysis

        text_to_analyze = f"Title: {title or 'No title'}\nDescription: {description or 'No description'}"

        # Sentiment analysis
        try:
            sentiment_response = requests.post(
                f"{self.config.HF_API_URL}/{self.config.HF_MODELS['sentiment']}",
                headers={"Authorization": f"Bearer {self.config.HF_API_TOKEN}"},
                json={"inputs": text_to_analyze[:512]},
                timeout=self.timeout
            )
            sentiment_response.raise_for_status()
            sentiment = sentiment_response.json()
            if sentiment and isinstance(sentiment, list) and len(sentiment) > 0:
                label = sentiment[0][0]['label']
                score = sentiment[0][0]['score']
                if label == 'POSITIVE' and score > 0.85:
                    analysis['reasons'].append(f"Overly positive language (score: {score:.2f})")
                    analysis['confidence'] = min(1.0, analysis['confidence'] + 0.2)
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")

        # Fake news detection
        try:
            fake_response = requests.post(
                f"{self.config.HF_API_URL}/{self.config.HF_MODELS['fake-news']}",
                headers={"Authorization": f"Bearer {self.config.HF_API_TOKEN}"},
                json={"inputs": text_to_analyze[:512]},
                timeout=self.timeout
            )
            fake_response.raise_for_status()
            fake_result = fake_response.json()
            if fake_result and isinstance(fake_result, list) and len(fake_result) > 0:
                label = fake_result[0][0]['label']
                score = fake_result[0][0]['score']
                if label == 'LABEL_1' and score > 0.7:
                    analysis['reasons'].append(f"Potential fake content (confidence: {score:.2f})")
                    analysis['confidence'] = min(1.0, analysis['confidence'] + 0.3)
        except Exception as e:
            logger.error(f"Fake news detection failed: {str(e)}")

        # Final determination
        if analysis['confidence'] > 0.7:
            analysis['is_suspicious'] = True
            analysis['final_verdict'] = "High probability of being fake"
        elif analysis['confidence'] > 0.5:
            analysis['final_verdict'] = "Some suspicious indicators found"
            
        return analysis

    def full_analysis(self, property_data):
        """Complete analysis method that was missing"""
        if not property_data:
            return {
                'is_suspicious': False,
                'reasons': ['No property data provided'],
                'confidence': 0.0,
                'recommendation': 'Analysis failed',
                'final_verdict': 'Insufficient data for analysis'
            }
            
        return self.analyze_text(
            property_data.get('description'),
            property_data.get('title'),
            property_data.get('price')
        )
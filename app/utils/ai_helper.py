import google.generativeai as genai
from config import Config
import json
import re

genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel(Config.GEMINI_MODEL)

def generate_query_params(user_input):
    try:
        prompt = f"""
        Convert this real estate request into database query parameters in JSON format.
        Available filters: location, min_price, max_price, min_bedrooms, max_bedrooms, 
        min_bathrooms, max_bathrooms, min_area, max_area, type (villa, apartment, etc.)
        
        Rules:
        1. Only return valid JSON, no explanations
        2. Never include price filters unless explicitly mentioned
        3. For bedroom/bathroom/area, use min/max when ranges are mentioned
        4. Location should be a string to search within location field
        5. Type should be standardized (villa, apartment, townhouse, etc.)
        
        Example Input: "Find 2-3 bedroom villas in Dubai Marina under 2 million"
        Example Output:
        {{
            "location": "Dubai Marina",
            "min_bedrooms": 2,
            "max_bedrooms": 3,
            "max_price": 2000000,
            "type": "villa"
        }}
        
        User Input: "{user_input}"
        """
        
        response = model.generate_content(prompt)
        
        json_match = re.search(r'\{[\s\S]*\}', response.text)
        if json_match:
            return json_match.group()
        
        return None
        
    except Exception as e:
        print(f"Error generating query with Gemini: {str(e)}")
        return None

def generate_chat_response(user_input, properties):
    try:
        properties_str = "\n".join([f"{p['title']} - {p['price']} AED" for p in properties])
        
        prompt = f"""
        You are a friendly real estate assistant. The user asked:
        "{user_input}"
        
        You found {len(properties)} properties matching their criteria:
        {properties_str}
        
        Craft a friendly response summarizing what you found and highlighting
        some interesting options. Keep it conversational and helpful.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Error generating chat response: {str(e)}")
        return f"I found {len(properties)} properties matching your criteria."
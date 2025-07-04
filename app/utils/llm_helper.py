import json
import requests
import re

# Configuration
LLM_ENDPOINT = "http://localhost:8080/vi/completions"
DEFAULT_PROMPT_TEMPLATE = """
You are a real estate query to GraphQL converter. Convert the following user request into a valid GraphQL query for Weaviate.

Rules:
1. Only return the GraphQL query, no explanations or additional text
2. The Weaviate class is 'Property'
3. Available fields: title, description, price, location, bedrooms, bathrooms, source, thumbnail
4. Never include price filters unless explicitly mentioned by the user
5. Always include a limit (default to 10 if not specified)

Example Input: "Find 2 bedroom villas in Dubai Marina"
Example Output:
{
  query: `{
    properties: Get {
      Property(
        where: {
          operator: And,
          operands: [
            { path: ["bedrooms"], operator: Equal, valueInt: 2 },
            { path: ["location"], operator: Like, valueString: "%Dubai Marina%" }
          ]
        },
        limit: 10
      ) {
        title
        description
        price
        location
        bedrooms
        bathrooms
        source
        thumbnail
      }
    }
  }`
}

User Input: "{user_input}"
"""

def generate_graphql_query(user_input):
    """Generate a GraphQL query from natural language using LLM"""
    try:
        # Prepare the prompt
        prompt = DEFAULT_PROMPT_TEMPLATE.replace("{user_input}", user_input)
        
        # Call the LLM API
        response = requests.post(
            LLM_ENDPOINT,
            json={
                "prompt": prompt,
                "temperature": 0.2,
                "max_tokens": 2048
            },
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"LLM API error: {response.status_code}")
        
        # Extract the GraphQL query from the response
        result = response.json()
        completion = result.get('choices', [{}])[0].get('text', '').strip()
        
        # Clean up the response to extract just the GraphQL
        graphql_match = re.search(r'`?\s*{\s*query:\s*`([^`]+)`', completion, re.DOTALL)
        if graphql_match:
            return graphql_match.group(1).strip()
        
        # Fallback: try to find just the GraphQL content
        graphql_match = re.search(r'`([^`]+)`', completion, re.DOTALL)
        if graphql_match:
            return graphql_match.group(1).strip()
        
        return completion.strip()
    
    except Exception as e:
        print(f"Error generating GraphQL query: {str(e)}")
        return None

def extract_filters_from_query(query):
    """Helper function to extract filters from a GraphQL query"""
    # This would parse the GraphQL to extract the filter conditions
    # Implementation would depend on your specific needs
    return {}
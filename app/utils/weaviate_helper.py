import requests
import json

# Configuration
WEAVIATE_ENDPOINT = "http://localhost:8081/vi/graphql"

# Sample property structure
SAMPLE_PROPERTIES = [
    {
        "title": "Luxury Villa",
        "price": 700839,
        "location": "Dubai Marina",
        "bedrooms": 2,
        "bathrooms": 4,
        "description": "Exist number feel assume really big. Never bed could relationship college start several.",
        "source": "yalladeals.com",
        "thumbnail": "https://example.com/villa1.jpg"
    },
    # Add more sample properties as needed
]

def execute_graphql_query(query):
    """Execute a GraphQL query against Weaviate and return results"""
    try:
        # In a real implementation, this would call the actual Weaviate endpoint
        # For now, we'll use mock data
        # response = requests.post(
        #     WEAVIATE_ENDPOINT,
        #     json={"query": query},
        #     headers={"Content-Type": "application/json"},
        #     timeout=30
        # )
        
        # if response.status_code != 200:
        #     raise Exception(f"Weaviate API error: {response.status_code}")
        
        # results = response.json().get('data', {}).get('properties', {}).get('Property', [])
        
        # Mock implementation - filter sample properties based on query
        query_lower = query.lower()
        filtered_properties = []
        
        for prop in SAMPLE_PROPERTIES:
            include = True
            
            # Simple mock filtering based on query content
            if "dubai marina" in query_lower and "dubai marina" not in prop["location"].lower():
                include = False
            if "bedroom" in query_lower:
                if "2" in query_lower and prop["bedrooms"] != 2:
                    include = False
                elif "3" in query_lower and prop["bedrooms"] != 3:
                    include = False
            
            if include:
                filtered_properties.append(prop)
        
        return filtered_properties
    
    except Exception as e:
        print(f"Error executing GraphQL query: {str(e)}")
        return None

def validate_graphql_query(query):
    """Basic validation of a GraphQL query"""
    if not query or not query.strip():
        return False
        # Very basic validation - in a real app you'd want more thorough checks
    return "query" in query.lower() and "property" in query.lower()
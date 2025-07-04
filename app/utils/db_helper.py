from app.models import Property
import json

def search_properties(query_params):
    try:
        if isinstance(query_params, str):
            try:
                filters = json.loads(query_params)
            except json.JSONDecodeError:
                return []
        else:
            filters = query_params
        
        query = Property.query
        
        if 'location' in filters:
            query = query.filter(Property.location.ilike(f"%{filters['location']}%"))
        
        if 'min_price' in filters:
            query = query.filter(Property.price >= filters['min_price'])
        
        if 'max_price' in filters:
            query = query.filter(Property.price <= filters['max_price'])
        
        if 'min_bedrooms' in filters:
            query = query.filter(Property.bedrooms >= filters['min_bedrooms'])
        
        if 'max_bedrooms' in filters:
            query = query.filter(Property.bedrooms <= filters['max_bedrooms'])
        
        if 'min_bathrooms' in filters:
            query = query.filter(Property.bathrooms >= filters['min_bathrooms'])
        
        if 'max_bathrooms' in filters:
            query = query.filter(Property.bathrooms <= filters['max_bathrooms'])
        
        if 'min_area' in filters:
            query = query.filter(Property.area >= filters['min_area'])
        
        if 'max_area' in filters:
            query = query.filter(Property.area <= filters['max_area'])
        
        if 'type' in filters:
            query = query.filter(Property.type.ilike(f"%{filters['type']}%"))
        
        return query.order_by(Property.price).limit(20).all()
    
    except Exception as e:
        print(f"Error searching properties: {str(e)}")
        return []
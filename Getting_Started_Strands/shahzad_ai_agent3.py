from strands import Agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import json
import random
from datetime import datetime, timedelta

# Initialize hotel search agent
agent = Agent()
app = BedrockAgentCoreApp()

class HotelSearchAgent:
    def __init__(self):
        self.agent_name = "hotel-search-agent"
        self.agent_type = "hotel_specialist"
        
    def search_hotels(self, query_params):
        """Search for hotels based on user criteria"""
        # Extract parameters from query
        location = query_params.get('location', 'Manhattan')
        checkin_date = query_params.get('checkin_date', '2025-09-15')
        checkout_date = query_params.get('checkout_date', '2025-09-17')
        guests = query_params.get('guests', 2)
        budget = query_params.get('budget', 'any')
        amenities_pref = query_params.get('amenities', [])
        
        # Mock hotel search results
        # In production, this would call actual hotel APIs like Booking.com, Hotels.com, etc.
        mock_hotels = [
            {
                "hotel_id": "HTL001",
                "name": "Grand Plaza Hotel",
                "location": f"{location}, Downtown",
                "rating": "4.5★",
                "price": "$189/night",
                "total_price": "$378 (2 nights)",
                "amenities": ["WiFi", "Pool", "Gym", "Restaurant", "Spa", "Business Center"],
                "description": "Luxury hotel in the heart of downtown with stunning city views",
                "distance_from_center": "0.2 miles",
                "cancellation": "Free cancellation until 24 hours before check-in",
                "breakfast": "Continental breakfast included"
            },
            {
                "hotel_id": "HTL002", 
                "name": "Boutique Inn",
                "location": f"{location}, Arts District",
                "rating": "4.2★",
                "price": "$129/night",
                "total_price": "$258 (2 nights)",
                "amenities": ["WiFi", "Breakfast", "Pet-friendly", "Parking", "24/7 Front Desk"],
                "description": "Charming boutique hotel with personalized service and local charm",
                "distance_from_center": "0.8 miles", 
                "cancellation": "Free cancellation until 48 hours before check-in",
                "breakfast": "Complimentary breakfast buffet"
            },
            {
                "hotel_id": "HTL003",
                "name": "Business Suites",
                "location": f"{location}, Financial District", 
                "rating": "4.0★",
                "price": "$159/night",
                "total_price": "$318 (2 nights)",
                "amenities": ["WiFi", "Business Center", "Gym", "Kitchenette", "Laundry"],
                "description": "Modern business hotel with fully equipped suites",
                "distance_from_center": "0.5 miles",
                "cancellation": "Free cancellation until 12 hours before check-in", 
                "breakfast": "Grab-and-go breakfast available"
            },
            {
                "hotel_id": "HTL004",
                "name": "Luxury Resort & Spa",
                "location": f"{location}, Uptown",
                "rating": "4.8★", 
                "price": "$299/night",
                "total_price": "$598 (2 nights)",
                "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Room Service", "Concierge", "Valet Parking"],
                "description": "Five-star luxury resort with world-class amenities and service",
                "distance_from_center": "1.2 miles",
                "cancellation": "Free cancellation until 72 hours before check-in",
                "breakfast": "Gourmet breakfast available ($25/person)"
            },
            {
                "hotel_id": "HTL005",
                "name": "Budget Stay Inn", 
                "location": f"{location}, Suburbs",
                "rating": "3.7★",
                "price": "$79/night",
                "total_price": "$158 (2 nights)", 
                "amenities": ["WiFi", "Parking", "24/7 Front Desk"],
                "description": "Clean and comfortable budget accommodation",
                "distance_from_center": "2.1 miles",
                "cancellation": "Free cancellation until 6 hours before check-in",
                "breakfast": "Continental breakfast ($8/person)"
            }
        ]
        
        # Filter by budget if specified
        filtered_hotels = mock_hotels
        if budget != 'any':
            try:
                budget_amount = int(budget.replace('$', '').replace(',', ''))
                filtered_hotels = []
                for hotel in mock_hotels:
                    hotel_price = int(hotel['price'].replace('$', '').replace('/night', ''))
                    if hotel_price <= budget_amount:
                        filtered_hotels.append(hotel)
            except:
                pass
        
        # Filter by amenities if specified
        if amenities_pref:
            amenity_filtered = []
            for hotel in filtered_hotels:
                hotel_amenities_lower = [amenity.lower() for amenity in hotel['amenities']]
                if any(pref.lower() in hotel_amenities_lower for pref in amenities_pref):
                    amenity_filtered.append(hotel)
            if amenity_filtered:
                filtered_hotels = amenity_filtered
        
        # Sort by rating (highest first)
        filtered_hotels.sort(key=lambda x: float(x['rating'].replace('★', '')), reverse=True)
        
        return {
            "hotels": filtered_hotels,
            "total_results": len(filtered_hotels),
            "search_params": query_params,
            "agent": self.agent_name
        }
    
    def parse_hotel_request(self, user_message):
        """Parse user message to extract hotel search parameters"""
        message_lower = user_message.lower()
        
        # Extract location
        location = "Manhattan"  # default
        
        # Look for common location patterns
        location_keywords = {
            'manhattan': 'Manhattan',
            'brooklyn': 'Brooklyn', 
            'downtown': 'Downtown',
            'midtown': 'Midtown',
            'times square': 'Times Square',
            'central park': 'Central Park Area',
            'financial district': 'Financial District',
            'soho': 'SoHo',
            'chelsea': 'Chelsea',
            'tribeca': 'TriBeCa',
            'boston': 'Boston',
            'san francisco': 'San Francisco',
            'los angeles': 'Los Angeles',
            'chicago': 'Chicago',
            'miami': 'Miami',
            'seattle': 'Seattle'
        }
        
        for keyword, location_name in location_keywords.items():
            if keyword in message_lower:
                location = location_name
                break
        
        # Extract dates (simple extraction)
        checkin_date = "2025-09-15"  # default
        checkout_date = "2025-09-17"  # default (2 nights)
        
        if "september" in message_lower or "sep" in message_lower:
            checkin_date = "2025-09-15"
            checkout_date = "2025-09-17"
        elif "october" in message_lower or "oct" in message_lower:
            checkin_date = "2025-10-15"
            checkout_date = "2025-10-17"
        elif "november" in message_lower or "nov" in message_lower:
            checkin_date = "2025-11-15"
            checkout_date = "2025-11-17"
        
        # Extract number of guests
        guests = 2  # default
        if "1 guest" in message_lower or "single" in message_lower:
            guests = 1
        elif "3 guests" in message_lower or "family" in message_lower:
            guests = 3
        elif "4 guests" in message_lower or "4 people" in message_lower:
            guests = 4
        
        # Extract budget
        budget = "any"
        if "$" in user_message:
            import re
            amounts = re.findall(r'\$(\d+)', user_message)
            if amounts:
                budget = f"${amounts[0]}"
        
        # Extract amenity preferences
        amenities = []
        amenity_keywords = {
            'pool': 'Pool',
            'gym': 'Gym', 
            'spa': 'Spa',
            'parking': 'Parking',
            'breakfast': 'Breakfast',
            'wifi': 'WiFi',
            'pet': 'Pet-friendly',
            'restaurant': 'Restaurant'
        }
        
        for keyword, amenity in amenity_keywords.items():
            if keyword in message_lower:
                amenities.append(amenity)
        
        return {
            "location": location,
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "guests": guests,
            "budget": budget,
            "amenities": amenities
        }

# Initialize hotel search agent
hotel_agent = HotelSearchAgent()

def invoke(payload):
    """Process hotel search requests and return hotel options"""
    try:
        user_message = payload.get("prompt", "")
        
        # Parse the hotel request
        query_params = hotel_agent.parse_hotel_request(user_message)
        
        # Search for hotels
        hotel_results = hotel_agent.search_hotels(query_params)
        
        # Format response
        response = {
            "text": f"Found {hotel_results['total_results']} hotels in {query_params['location']}",
            "type": "hotel_search",
            "results": hotel_results["hotels"],
            "agent": "hotel-search-agent",
            "search_summary": {
                "location": query_params['location'],
                "checkin": query_params['checkin_date'],
                "checkout": query_params['checkout_date'],
                "guests": query_params['guests'],
                "budget": query_params['budget'],
                "amenities_requested": query_params['amenities'],
                "total_found": hotel_results['total_results']
            }
        }
        
        return json.dumps(response)
        
    except Exception as e:
        error_response = {
            "text": f"Sorry, I encountered an error searching for hotels: {str(e)}",
            "type": "error", 
            "results": [],
            "agent": "hotel-search-agent"
        }
        return json.dumps(error_response)

# Register the entrypoint
app.entrypoint(invoke)

if __name__ == "__main__":
    print("Starting hotel search agent...")
    print(f"Agent: {hotel_agent.agent_name}")
    print(f"Type: {hotel_agent.agent_type}")
    app.run()

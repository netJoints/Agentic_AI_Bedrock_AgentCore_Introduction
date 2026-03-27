# supervisor agent 

from strands import Agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import json
import re
from datetime import datetime

# Initialize supervisor agent
agent = Agent()
app = BedrockAgentCoreApp()

class TravelSupervisorAgent:
    def __init__(self):
        self.agent_name = "travel-supervisor-agent"
        self.agent_type = "supervisor"
        
        # In production, these would be the actual endpoint URLs of your deployed agents
        self.flight_agent_endpoint = "http://shahzad_ai_agent2:8080/api"  # flight agent
        self.hotel_agent_endpoint = "http://shahzad_ai_agent3:8080/api"   # hotel agent
        
    def analyze_request_intent(self, user_message):
        """Analyze user message to determine what services are needed"""
        message_lower = user_message.lower()
        
        needs_flight = any(keyword in message_lower for keyword in [
            'flight', 'fly', 'plane', 'airline', 'airport', 'departure', 'arrival', 'ticket'
        ])
        
        needs_hotel = any(keyword in message_lower for keyword in [
            'hotel', 'stay', 'accommodation', 'room', 'booking', 'lodge', 'resort', 'inn'
        ])
        
        needs_trip_planning = any(keyword in message_lower for keyword in [
            'trip', 'vacation', 'travel', 'plan', 'itinerary', 'visit', 'tour'
        ])
        
        # If it's general trip planning, we need both
        if needs_trip_planning and not (needs_flight or needs_hotel):
            needs_flight = True
            needs_hotel = True
        
        return {
            "needs_flight": needs_flight,
            "needs_hotel": needs_hotel,
            "needs_trip_planning": needs_trip_planning,
            "intent_type": self._determine_intent_type(needs_flight, needs_hotel, needs_trip_planning)
        }
    
    def _determine_intent_type(self, needs_flight, needs_hotel, needs_trip_planning):
        """Determine the primary intent type"""
        if needs_flight and needs_hotel:
            return "full_trip_planning"
        elif needs_flight:
            return "flight_only"
        elif needs_hotel:
            return "hotel_only"
        elif needs_trip_planning:
            return "trip_planning"
        else:
            return "general_inquiry"
    
    def extract_travel_details(self, user_message):
        """Extract travel details from user message"""
        message_lower = user_message.lower()
        
        # Extract origin and destination for flights
        origin = None
        destination = None
        
        # Look for flight routing patterns
        if "from" in message_lower and "to" in message_lower:
            try:
                parts = message_lower.split("from")[1].split("to")
                if len(parts) >= 2:
                    origin = parts[0].strip().title()
                    destination = parts[1].split()[0].strip().title()
            except:
                pass
        elif " to " in message_lower:
            try:
                parts = message_lower.split(" to ")
                if len(parts) >= 2:
                    origin = parts[0].split()[-1].strip().title()
                    destination = parts[1].split()[0].strip().title()
            except:
                pass
        
        # Extract location for hotels (could be destination or specific location)
        hotel_location = destination if destination else self._extract_location(user_message)
        
        # Extract dates
        dates = self._extract_dates(user_message)
        
        # Extract budget
        budget = self._extract_budget(user_message)
        
        # Extract passenger/guest count
        travelers = self._extract_traveler_count(user_message)
        
        return {
            "origin": origin,
            "destination": destination,
            "hotel_location": hotel_location,
            "dates": dates,
            "budget": budget,
            "travelers": travelers
        }
    
    def _extract_location(self, message):
        """Extract location mentions from message"""
        message_lower = message.lower()
        
        # Common cities and locations
        locations = [
            'new york', 'nyc', 'manhattan', 'brooklyn',
            'los angeles', 'la', 'hollywood',
            'san francisco', 'sf', 'bay area',
            'chicago', 'boston', 'miami', 'seattle',
            'las vegas', 'vegas', 'denver', 'atlanta'
        ]
        
        for location in locations:
            if location in message_lower:
                return location.title()
        
        return "New York"  # default
    
    def _extract_dates(self, message):
        """Extract travel dates from message"""
        message_lower = message.lower()
        
        # Simple date extraction
        if "september" in message_lower or "sep" in message_lower:
            return {"departure": "2025-09-15", "return": "2025-09-17"}
        elif "october" in message_lower or "oct" in message_lower:
            return {"departure": "2025-10-15", "return": "2025-10-17"}
        elif "november" in message_lower or "nov" in message_lower:
            return {"departure": "2025-11-15", "return": "2025-11-17"}
        else:
            return {"departure": "2025-09-15", "return": "2025-09-17"}
    
    def _extract_budget(self, message):
        """Extract budget information from message"""
        budget_match = re.search(r'\$(\d+)', message)
        if budget_match:
            return f"${budget_match.group(1)}"
        return "moderate"
    
    def _extract_traveler_count(self, message):
        """Extract number of travelers"""
        message_lower = message.lower()
        
        if "family" in message_lower:
            return 4
        elif "couple" in message_lower or "two" in message_lower:
            return 2
        elif "solo" in message_lower or "alone" in message_lower:
            return 1
        else:
            return 2  # default
    
    def call_flight_agent(self, travel_details, user_message):
        """Simulate calling the flight search agent"""
        # In production, this would make an HTTP request to the flight agent
        # For now, we'll simulate the response based on the flight agent's logic
        
        origin = travel_details.get('origin', 'LAX')
        destination = travel_details.get('destination', 'JFK')
        departure_date = travel_details['dates']['departure']
        
        # Simulate flight search results
        mock_flights = [
            {
                "flight_id": "AA123",
                "airline": "American Airlines",
                "route": f"{origin} → {destination}",
                "departure": f"{departure_date} 08:00",
                "arrival": f"{departure_date} 16:30",
                "price": "$299",
                "duration": "5h 30m",
                "stops": 0
            },
            {
                "flight_id": "DL456",
                "airline": "Delta",
                "route": f"{origin} → {destination}",
                "departure": f"{departure_date} 14:20",
                "arrival": f"{departure_date} 22:45",
                "price": "$345",
                "duration": "5h 25m",
                "stops": 0
            }
        ]
        
        return {
            "success": True,
            "results": mock_flights,
            "agent": "flight-search-agent"
        }
    
    def call_hotel_agent(self, travel_details, user_message):
        """Simulate calling the hotel search agent"""
        # In production, this would make an HTTP request to the hotel agent
        # For now, we'll simulate the response based on the hotel agent's logic
        
        location = travel_details.get('hotel_location', 'Manhattan')
        checkin = travel_details['dates']['departure']
        checkout = travel_details['dates']['return']
        
        # Simulate hotel search results
        mock_hotels = [
            {
                "hotel_id": "HTL001",
                "name": "Grand Plaza Hotel",
                "location": f"{location}, Downtown",
                "rating": "4.5★",
                "price": "$189/night",
                "amenities": ["WiFi", "Pool", "Gym", "Restaurant"],
                "description": "Luxury hotel in the heart of downtown"
            },
            {
                "hotel_id": "HTL002",
                "name": "Boutique Inn",
                "location": f"{location}, Arts District",
                "rating": "4.2★",
                "price": "$129/night",
                "amenities": ["WiFi", "Breakfast", "Pet-friendly"],
                "description": "Charming boutique hotel with personalized service"
            }
        ]
        
        return {
            "success": True,
            "results": mock_hotels,
            "agent": "hotel-search-agent"
        }
    
    def coordinate_travel_search(self, user_message):
        """Main coordination logic"""
        # Analyze what the user needs
        intent = self.analyze_request_intent(user_message)
        
        # Extract travel details
        travel_details = self.extract_travel_details(user_message)
        
        # Initialize results
        flight_results = None
        hotel_results = None
        
        # Call appropriate agents based on intent
        if intent["needs_flight"]:
            flight_response = self.call_flight_agent(travel_details, user_message)
            if flight_response["success"]:
                flight_results = flight_response["results"]
        
        if intent["needs_hotel"]:
            hotel_response = self.call_hotel_agent(travel_details, user_message)
            if hotel_response["success"]:
                hotel_results = hotel_response["results"]
        
        # Generate coordinated response
        return self.generate_coordinated_response(
            intent, travel_details, flight_results, hotel_results, user_message
        )
    
    def generate_coordinated_response(self, intent, travel_details, flight_results, hotel_results, user_message):
        """Generate a coordinated response combining results from multiple agents"""
        
        response_parts = []
        combined_results = {}
        
        # Handle flight results
        if flight_results:
            flight_count = len(flight_results)
            origin = travel_details.get('origin', 'your departure city')
            destination = travel_details.get('destination', 'your destination')
            response_parts.append(f"Found {flight_count} flights from {origin} to {destination}")
            combined_results["flights"] = flight_results
        
        # Handle hotel results
        if hotel_results:
            hotel_count = len(hotel_results)
            location = travel_details.get('hotel_location', 'your destination')
            response_parts.append(f"Found {hotel_count} hotels in {location}")
            combined_results["hotels"] = hotel_results
        
        # Create summary message
        if flight_results and hotel_results:
            summary = f"I've found complete travel options for your trip! {' and '.join(response_parts)}."
            response_type = "full_trip_planning"
        elif flight_results:
            summary = response_parts[0] + "."
            response_type = "flight_search"
        elif hotel_results:
            summary = response_parts[0] + "."
            response_type = "hotel_search"
        else:
            summary = "I can help you find flights and hotels. Please specify your travel needs."
            response_type = "general"
        
        # Add travel recommendations
        if flight_results and hotel_results:
            summary += " I recommend booking both together for potential savings and coordinated timing."
        
        return {
            "text": summary,
            "type": response_type,
            "results": combined_results,
            "agent": "travel-supervisor-agent",
            "coordination_summary": {
                "intent_analysis": intent,
                "travel_details": travel_details,
                "agents_called": {
                    "flight_agent": flight_results is not None,
                    "hotel_agent": hotel_results is not None
                },
                "total_flights": len(flight_results) if flight_results else 0,
                "total_hotels": len(hotel_results) if hotel_results else 0
            }
        }

# Initialize supervisor agent
supervisor_agent = TravelSupervisorAgent()

def invoke(payload):
    """Process travel coordination requests"""
    try:
        user_message = payload.get("prompt", "")
        
        # Coordinate the travel search across multiple agents
        response = supervisor_agent.coordinate_travel_search(user_message)
        
        return json.dumps(response)
        
    except Exception as e:
        error_response = {
            "text": f"Sorry, I encountered an error coordinating your travel search: {str(e)}",
            "type": "error",
            "results": {},
            "agent": "travel-supervisor-agent"
        }
        return json.dumps(error_response)

# Register the entrypoint
app.entrypoint(invoke)

if __name__ == "__main__":
    print("Starting travel supervisor agent...")
    print(f"Agent: {supervisor_agent.agent_name}")
    print(f"Type: {supervisor_agent.agent_type}")
    print("Coordinating flight and hotel search agents...")
    app.run()

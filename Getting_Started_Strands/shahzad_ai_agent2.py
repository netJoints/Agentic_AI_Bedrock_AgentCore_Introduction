# Flight search Agentic AI 

from strands import Agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import json
import random
from datetime import datetime, timedelta

# Initialize flight search agent
agent = Agent()
app = BedrockAgentCoreApp()

class FlightSearchAgent:
    def __init__(self):
        self.agent_name = "flight-search-agent"
        self.agent_type = "flight_specialist"
        
    def search_flights(self, query_params):
        """Search for flights based on user criteria"""
        # Extract parameters from query
        origin = query_params.get('origin', 'LAX')
        destination = query_params.get('destination', 'JFK')
        departure_date = query_params.get('departure_date', '2025-09-15')
        passengers = query_params.get('passengers', 1)
        budget = query_params.get('budget', 'any')
        
        # Mock flight search results
        # In production, this would call actual flight APIs like Amadeus, Skyscanner, etc.
        mock_flights = [
            {
                "flight_id": "AA123",
                "airline": "American Airlines",
                "route": f"{origin} → {destination}",
                "departure": f"{departure_date} 08:00",
                "arrival": f"{departure_date} 16:30",
                "price": "$299",
                "duration": "5h 30m",
                "stops": 0,
                "aircraft": "Boeing 737",
                "class": "Economy"
            },
            {
                "flight_id": "DL456", 
                "airline": "Delta",
                "route": f"{origin} → {destination}",
                "departure": f"{departure_date} 14:20",
                "arrival": f"{departure_date} 22:45", 
                "price": "$345",
                "duration": "5h 25m",
                "stops": 0,
                "aircraft": "Airbus A320",
                "class": "Economy"
            },
            {
                "flight_id": "UA789",
                "airline": "United Airlines", 
                "route": f"{origin} → {destination}",
                "departure": f"{departure_date} 06:15",
                "arrival": f"{departure_date} 14:40",
                "price": "$275",
                "duration": "5h 25m", 
                "stops": 0,
                "aircraft": "Boeing 757",
                "class": "Economy"
            }
        ]
        
        # Filter by budget if specified
        if budget != 'any':
            try:
                budget_amount = int(budget.replace('$', '').replace(',', ''))
                mock_flights = [f for f in mock_flights if int(f['price'].replace('$', '').replace(',', '')) <= budget_amount]
            except:
                pass
        
        return {
            "flights": mock_flights,
            "total_results": len(mock_flights),
            "search_params": query_params,
            "agent": self.agent_name
        }
    
    def parse_flight_request(self, user_message):
        """Parse user message to extract flight search parameters"""
        message_lower = user_message.lower()
        
        # Extract origin and destination
        # Look for common patterns like "from X to Y" or "X to Y"
        origin = "LAX"  # default
        destination = "JFK"  # default
        
        # Simple pattern matching - in production use NLP
        if "from" in message_lower and "to" in message_lower:
            parts = message_lower.split("from")[1].split("to")
            if len(parts) >= 2:
                origin = parts[0].strip().upper()[:3]
                destination = parts[1].strip().upper()[:3]
        elif " to " in message_lower:
            parts = message_lower.split(" to ")
            if len(parts) >= 2:
                origin = parts[0].split()[-1].upper()[:3]
                destination = parts[1].split()[0].upper()[:3]
        
        # Extract date (simple extraction)
        departure_date = "2025-09-15"  # default
        if "september" in message_lower or "sep" in message_lower:
            departure_date = "2025-09-15"
        elif "october" in message_lower or "oct" in message_lower:
            departure_date = "2025-10-15"
        elif "november" in message_lower or "nov" in message_lower:
            departure_date = "2025-11-15"
        
        # Extract budget
        budget = "any"
        if "$" in user_message:
            # Extract dollar amount
            import re
            amounts = re.findall(r'\$(\d+)', user_message)
            if amounts:
                budget = f"${amounts[0]}"
        
        return {
            "origin": origin,
            "destination": destination, 
            "departure_date": departure_date,
            "passengers": 1,
            "budget": budget
        }

# Initialize flight search agent
flight_agent = FlightSearchAgent()

@app.entrypoint
def invoke(payload):
    """Process flight search requests and return flight options"""
    try:
        user_message = payload.get("prompt", "")
        
        # Parse the flight request
        query_params = flight_agent.parse_flight_request(user_message)
        
        # Search for flights
        flight_results = flight_agent.search_flights(query_params)
        
        # Format response
        response = {
            "text": f"Found {flight_results['total_results']} flights from {query_params['origin']} to {query_params['destination']}",
            "type": "flight_search",
            "results": flight_results["flights"],
            "agent": "flight-search-agent",
            "search_summary": {
                "route": f"{query_params['origin']} → {query_params['destination']}", 
                "date": query_params['departure_date'],
                "budget": query_params['budget'],
                "total_found": flight_results['total_results']
            }
        }
        
        return json.dumps(response)
        
    except Exception as e:
        error_response = {
            "text": f"Sorry, I encountered an error searching for flights: {str(e)}",
            "type": "error",
            "results": [],
            "agent": "flight-search-agent"
        }
        return json.dumps(error_response)

if __name__ == "__main__":
    app.run()

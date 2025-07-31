import os
import json
import requests
from typing import TypedDict, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain.tools import tool

# Load environment variables from .env file
load_dotenv()

# Set your Groq API key
# os.environ["GROQ_API_KEY"] = "your-groq-api-key-here"

# Define the state structure
class TravelState(TypedDict):
    destination: str
    budget: str
    duration: str
    interests: List[str]
    itinerary: str
    recommendations: str
    final_plan: str
    weather_info: str  # New field for tool data
    memory: dict       # New field for memory

# API Keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

# Simple memory storage (in production, use proper database)
TRAVEL_MEMORY = {}

# TOOLS: Real API integrations
@tool
def get_real_weather(destination: str) -> str:
    """Get real current weather for a destination using WeatherAPI"""
    try:
        # Step 1: Get coordinates using Geoapify
        geo_url = f"https://api.geoapify.com/v1/geocode/search?text={destination}&apiKey={GEOAPIFY_API_KEY}"
        geo_resp = requests.get(geo_url)
        geo_data = geo_resp.json()
        
        if not geo_data.get('features'):
            return f"Location not found for {destination}"
        
        # Get coordinates
        coords = geo_data['features'][0]['geometry']['coordinates']
        lat, lon = coords[1], coords[0]  # Geoapify returns [lon, lat]
        
        # Step 2: Get weather using coordinates
        weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={lat},{lon}"
        weather_resp = requests.get(weather_url)
        weather_data = weather_resp.json()
        
        current = weather_data['current']
        location = weather_data['location']
        
        return f"{location['name']}: {current['temp_c']}°C, {current['condition']['text']}, Feels like {current['feelslike_c']}°C"
        
    except Exception as e:
        return f"Weather data unavailable: {str(e)}"

@tool
def save_preferences(user_data: dict) -> str:
    """Save user preferences to memory"""
    user_id = f"user_{hash(str(user_data))}"
    TRAVEL_MEMORY[user_id] = user_data
    return f"Preferences saved for {user_id}"

# Tool executor
tools = [get_real_weather, save_preferences]

# Initialize Groq LLM
llm = ChatGroq(
    model="llama3-70b-8192",  # You can also use "llama3-8b-8192" for faster responses
    temperature=0.7
)

def collect_preferences(state: TravelState) -> TravelState:
    """Node to collect user travel preferences with MEMORY"""
    print("🌍 Welcome to Simple Travel Planner!")
    
    # Check memory for previous trips
    if TRAVEL_MEMORY:
        print(f"📚 Found {len(TRAVEL_MEMORY)} previous trips in memory")
    
    destination = input("Where would you like to travel? ")
    budget = input("What's your budget range? (low/medium/high) ")
    duration = input("How many days? ")
    interests_input = input("What are your interests? (separate with commas) ")
    interests = [interest.strip() for interest in interests_input.split(",")]
    
    # MEMORY: Save preferences using tool
    user_data = {
        "destination": destination,
        "budget": budget,
        "duration": duration,
        "interests": interests
    }
    
    # Use tool to save preferences
    save_result = save_preferences.invoke({"user_data": user_data})
    
    state["destination"] = destination
    state["budget"] = budget
    state["duration"] = duration
    state["interests"] = interests
    state["memory"] = user_data
    
    print(f"✅ Collected preferences for {destination}")
    print(f"💾 {save_result}")
    return state

def generate_itinerary(state: TravelState) -> TravelState:
    """Node to generate a basic itinerary with REAL WEATHER"""
    print("📅 Generating itinerary...")
    
    # TOOL: Get real weather information
    weather_info = get_real_weather.invoke({"destination": state["destination"]})
    state["weather_info"] = weather_info
    
    prompt = f"""
    Create a {state['duration']}-day travel itinerary for {state['destination']}.
    Budget: {state['budget']}
    Interests: {', '.join(state['interests'])}
    Current Weather: {weather_info}
    
    Provide a day-by-day breakdown with:
    - Morning, afternoon, and evening activities
    - Estimated costs
    - Travel tips
    - Weather-appropriate recommendations
    
    Keep it concise and practical.
    """
    
    messages = [
        SystemMessage(content="You are a helpful travel planning assistant."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    state["itinerary"] = response.content
    
    print(f"✅ Itinerary generated (Real Weather: {weather_info})")
    return state

def get_recommendations(state: TravelState) -> TravelState:
    """Node to get accommodation and dining recommendations"""
    print("🏨 Getting recommendations...")
    
    prompt = f"""
    For a trip to {state['destination']} with a {state['budget']} budget, recommend:
    
    1. 3 accommodation options (hotels/hostels/Airbnb)
    2. 5 must-try restaurants or food experiences
    3. Transportation tips
    4. Packing essentials
    
    Consider the traveler is interested in: {', '.join(state['interests'])}
    """
    
    messages = [
        SystemMessage(content="You are a travel expert providing practical recommendations."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    state["recommendations"] = response.content
    
    print("✅ Recommendations generated")
    return state

def create_final_plan(state: TravelState) -> TravelState:
    """Node to combine everything into a final travel plan"""
    print("📋 Creating final travel plan...")
    
    prompt = f"""
    Create a comprehensive travel plan summary for {state['destination']} combining:
    
    ITINERARY:
    {state['itinerary']}
    
    RECOMMENDATIONS:
    {state['recommendations']}
    
    Format it as a clean, organized travel guide with:
    - Trip overview
    - Daily schedule
    - Where to stay and eat
    - Budget breakdown
    - Important tips
    
    Make it ready to print or save.
    """
    
    messages = [
        SystemMessage(content="You are creating a final polished travel guide."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    state["final_plan"] = response.content
    
    print("✅ Final plan created")
    return state

def should_continue(state: TravelState) -> str:
    """Conditional edge to decide next step"""
    # Simple logic: if we have basic info, continue to itinerary
    if state.get("destination") and not state.get("itinerary"):
        return "generate_itinerary"
    elif state.get("itinerary") and not state.get("recommendations"):
        return "get_recommendations"
    elif state.get("recommendations") and not state.get("final_plan"):
        return "create_final_plan"
    else:
        return END

# Create the graph
def create_travel_planner():
    """Create and configure the travel planner graph"""
    
    # Initialize the StateGraph
    workflow = StateGraph(TravelState)
    
    # Add nodes
    workflow.add_node("collect_preferences", collect_preferences)
    workflow.add_node("generate_itinerary", generate_itinerary)
    workflow.add_node("get_recommendations", get_recommendations)
    workflow.add_node("create_final_plan", create_final_plan)
    
    # Set entry point
    workflow.set_entry_point("collect_preferences")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "collect_preferences",
        should_continue
    )
    
    workflow.add_conditional_edges(
        "generate_itinerary",
        should_continue
    )
    
    workflow.add_conditional_edges(
        "get_recommendations",
        should_continue
    )
    
    workflow.add_edge("create_final_plan", END)
    
    return workflow.compile()

# Main execution
def main():
    """Run the travel planner"""
    try:
        # Create the compiled graph
        app = create_travel_planner()
        
        # Initialize empty state
        initial_state = {
            "destination": "",
            "budget": "",
            "duration": "",
            "interests": [],
            "itinerary": "",
            "recommendations": "",
            "final_plan": "",
            "weather_info": "",  # New field
            "memory": {}         # New field
        }
        
        # Run the workflow
        print("🚀 Starting Travel Planner...")
        result = app.invoke(initial_state)
        
        # Display results
        print("\n" + "="*50)
        print("🎉 YOUR TRAVEL PLAN IS READY!")
        print("="*50)
        print(result["final_plan"])
        print("="*50)
        
        # Optionally save to file
        save_plan = input("\nWould you like to save this plan to a file? (y/n): ")
        if save_plan.lower() == 'y':
            filename = f"travel_plan_{result['destination'].replace(' ', '_')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result["final_plan"])
            print(f"✅ Plan saved to {filename}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have set your GROQ_API_KEY environment variable")

if __name__ == "__main__":
    main()
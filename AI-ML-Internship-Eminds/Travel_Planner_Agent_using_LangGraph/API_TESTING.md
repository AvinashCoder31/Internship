# 🔧 Backend API Testing Guide

This guide provides curl commands to test the Travel Planner Agent Flask backend API endpoints.

## 🚀 Starting the Backend Server

First, start the Flask backend server:

```bash
cd AI-ML-Internship-Eminds/Travel_Planner_Agent_using_LangGraph
python main.py
```

The server will start on `http://localhost:5000`

## 📡 API Endpoints & Curl Commands

### 1. Health Check
Test if the API is running:

```bash
curl -X GET http://localhost:5000/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Travel Planner API"
}
```

### 2. Home Endpoint
Get API information and available endpoints:

```bash
curl -X GET http://localhost:5000/
```

**Expected Response:**
```json
{
  "message": "Welcome to Travel Planner API",
  "version": "1.0.0",
  "endpoints": {
    "POST /api/plan": "Create a travel plan",
    "POST /api/save": "Save a travel plan to file",
    "POST /api/plan-and-save": "Create and optionally save a travel plan",
    "GET /api/health": "Health check"
  },
  "example_request": {
    "destination": "Paris",
    "budget": "medium",
    "duration": "5",
    "interests": ["museums", "food", "architecture"],
    "save_to_file": true
  }
}
```

### 3. Generate Travel Plan
Create a travel plan without saving:

```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris",
    "budget": "medium",
    "duration": "5",
    "interests": ["museums", "food", "architecture"]
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "plan": "# 5-Day Travel Plan for Paris\n\n## Day 1: Arrival and City Center...",
  "destination": "Paris",
  "weather_info": "Paris: 18°C, Partly cloudy, Feels like 16°C"
}
```

### 4. Save Travel Plan
Save an existing travel plan to file:

```bash
curl -X POST http://localhost:5000/api/save \
  -H "Content-Type: application/json" \
  -d '{
    "plan_content": "# My Travel Plan\n\nThis is my amazing travel plan...",
    "destination": "Tokyo"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "filepath": "output/travel_plan_Tokyo.md",
  "message": "Plan saved to output/travel_plan_Tokyo.md"
}
```

### 5. Generate and Save Travel Plan
Create a travel plan and optionally save it in one request:

```bash
curl -X POST http://localhost:5000/api/plan-and-save \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo",
    "budget": "high",
    "duration": "7",
    "interests": ["technology", "food", "culture", "shopping"],
    "save_to_file": true
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "plan": "# 7-Day Travel Plan for Tokyo\n\n## Day 1: Arrival and Shibuya...",
  "destination": "Tokyo",
  "weather_info": "Tokyo: 22°C, Clear, Feels like 24°C",
  "file_saved": true,
  "filepath": "output/travel_plan_Tokyo.md",
  "save_message": "Plan saved to output/travel_plan_Tokyo.md"
}
```

## 🧪 Test Scenarios

### Basic Test (Quick Check)
```bash
# 1. Check if server is running
curl -X GET http://localhost:5000/api/health

# 2. Generate a simple plan
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "London",
    "budget": "medium",
    "duration": "3",
    "interests": ["museums", "history"]
  }'
```

### Comprehensive Test
```bash
# Test with multiple interests and file saving
curl -X POST http://localhost:5000/api/plan-and-save \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "New York",
    "budget": "high",
    "duration": "6",
    "interests": ["art", "food", "nightlife", "shopping", "architecture"],
    "save_to_file": true
  }'
```

### Error Testing
```bash
# Test missing required fields
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris"
  }'

# Expected error response:
# {"error": "Missing 'budget' in request"}
```

## 📊 Response Formats

### Success Response Structure
```json
{
  "success": true,
  "plan": "Generated travel plan content...",
  "destination": "Destination name",
  "weather_info": "Current weather information"
}
```

### Error Response Structure
```json
{
  "error": "Error message describing what went wrong"
}
```

## 🔍 Testing Different Parameters

### Budget Options
```bash
# Low budget
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"destination": "Bangkok", "budget": "low", "duration": "4", "interests": ["food", "culture"]}'

# Medium budget
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"destination": "Bangkok", "budget": "medium", "duration": "4", "interests": ["food", "culture"]}'

# High budget
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"destination": "Bangkok", "budget": "high", "duration": "4", "interests": ["food", "culture"]}'
```

### Duration Variations
```bash
# Short trip (2 days)
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"destination": "Amsterdam", "budget": "medium", "duration": "2", "interests": ["museums", "canals"]}'

# Long trip (10 days)
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"destination": "India", "budget": "medium", "duration": "10", "interests": ["culture", "food", "history"]}'
```

### Interest Categories
```bash
# Adventure focused
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"destination": "Nepal", "budget": "medium", "duration": "7", "interests": ["adventure", "nature", "hiking"]}'

# Culture focused
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"destination": "Kyoto", "budget": "medium", "duration": "5", "interests": ["culture", "temples", "traditional"]}'

# Food focused
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"destination": "Italy", "budget": "medium", "duration": "6", "interests": ["food", "wine", "cooking"]}'
```

## 🛠️ Troubleshooting

### Common Issues

**1. Connection Refused**
```bash
curl: (7) Failed to connect to localhost port 5000: Connection refused
```
**Solution**: Make sure the Flask server is running with `python main.py`

**2. API Key Errors**
```json
{"error": "Weather data unavailable: API key error"}
```
**Solution**: Check your `.env` file has valid API keys:
- `GROQ_API_KEY`
- `WEATHER_API_KEY`
- `GEOAPIFY_API_KEY`

**3. Missing Fields Error**
```json
{"error": "Missing 'destination' in request"}
```
**Solution**: Ensure all required fields are included in your JSON payload

### Debug Mode
To see detailed error messages, the Flask app runs in debug mode. Check the terminal where you started the server for detailed error logs.

## 📝 Sample Test Script

Create a test script to run multiple tests:

```bash
#!/bin/bash
# test_api.sh

echo "Testing Travel Planner API..."

echo "1. Health Check:"
curl -s -X GET http://localhost:5000/api/health | jq

echo -e "\n2. API Info:"
curl -s -X GET http://localhost:5000/ | jq

echo -e "\n3. Generate Plan:"
curl -s -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris",
    "budget": "medium",
    "duration": "3",
    "interests": ["museums", "food"]
  }' | jq

echo -e "\n4. Generate and Save Plan:"
curl -s -X POST http://localhost:5000/api/plan-and-save \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo",
    "budget": "high",
    "duration": "5",
    "interests": ["technology", "food"],
    "save_to_file": true
  }' | jq

echo "Testing complete!"
```

Make it executable and run:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

**Note**: Make sure you have `jq` installed for pretty JSON formatting, or remove `| jq` from the commands to see raw JSON output.
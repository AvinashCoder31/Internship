from flask import Flask, request, jsonify
from src.routers.router import travel_blueprint

app = Flask(__name__)
app.register_blueprint(travel_blueprint, url_prefix="/api")

@app.route("/", methods=["GET"])
def home():
    """Home endpoint with API information"""
    return jsonify({
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
            "save_to_file": True
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
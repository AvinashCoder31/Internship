from flask import Blueprint, request, jsonify
from src.services.service1 import generate_travel_plan, save_travel_plan

travel_blueprint = Blueprint("travel_blueprint", __name__)

@travel_blueprint.route("/plan", methods=["POST"])
def create_travel_plan():
    """Create a travel plan based on user preferences"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["destination", "budget", "duration", "interests"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing '{field}' in request"}), 400
        
        destination = data.get("destination")
        budget = data.get("budget")
        duration = data.get("duration")
        interests = data.get("interests", [])
        
        # Validate interests is a list
        if not isinstance(interests, list):
            return jsonify({"error": "Interests must be a list"}), 400
        
        # Generate travel plan
        result = generate_travel_plan(destination, budget, duration, interests)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "plan": result["plan"],
                "destination": result["destination"],
                "weather_info": result["weather_info"]
            })
        else:
            return jsonify({"error": result["error"]}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@travel_blueprint.route("/save", methods=["POST"])
def save_plan():
    """Save a travel plan to file"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if "plan_content" not in data or "destination" not in data:
            return jsonify({"error": "Missing 'plan_content' or 'destination' in request"}), 400
        
        plan_content = data.get("plan_content")
        destination = data.get("destination")
        
        # Save the plan
        result = save_travel_plan(plan_content, destination)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "filepath": result["filepath"],
                "message": result["message"]
            })
        else:
            return jsonify({"error": result["error"]}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@travel_blueprint.route("/plan-and-save", methods=["POST"])
def create_and_save_plan():
    """Create and optionally save a travel plan in one request"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["destination", "budget", "duration", "interests"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing '{field}' in request"}), 400
        
        destination = data.get("destination")
        budget = data.get("budget")
        duration = data.get("duration")
        interests = data.get("interests", [])
        save_to_file = data.get("save_to_file", False)
        
        # Validate interests is a list
        if not isinstance(interests, list):
            return jsonify({"error": "Interests must be a list"}), 400
        
        # Generate travel plan
        plan_result = generate_travel_plan(destination, budget, duration, interests)
        
        if not plan_result["success"]:
            return jsonify({"error": plan_result["error"]}), 500
        
        response_data = {
            "success": True,
            "plan": plan_result["plan"],
            "destination": plan_result["destination"],
            "weather_info": plan_result["weather_info"]
        }
        
        # Save to file if requested
        if save_to_file:
            save_result = save_travel_plan(plan_result["plan"], destination)
            if save_result["success"]:
                response_data["file_saved"] = True
                response_data["filepath"] = save_result["filepath"]
                response_data["save_message"] = save_result["message"]
            else:
                response_data["file_saved"] = False
                response_data["save_error"] = save_result["error"]
        
        return jsonify(response_data)
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@travel_blueprint.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Travel Planner API"})
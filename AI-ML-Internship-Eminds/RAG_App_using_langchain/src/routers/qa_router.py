from flask import Blueprint, request, jsonify
from src.services.qa_service import get_response

qa_blueprint = Blueprint("qa_blueprint", __name__)

@qa_blueprint.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"error": "Missing 'question' in request"}), 400

    try:
        response = get_response(question)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
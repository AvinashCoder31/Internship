from flask import Blueprint, request, jsonify
from src.services.rag_service import retrieve_chunks, generate_answer

query_bp = Blueprint('query_bp', __name__)

@query_bp.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query not provided"}), 400

    try:
        chunks = retrieve_chunks(query)
        answer = generate_answer(query, chunks)
        return jsonify({
            "query": query,
            "answer": answer
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

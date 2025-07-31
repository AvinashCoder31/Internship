from flask import Flask, request, jsonify
from src.routers.qa_router import qa_blueprint

app = Flask(__name__)
app.register_blueprint(qa_blueprint, url_prefix="/api")

if __name__ == '__main__':
    app.run(debug=True)
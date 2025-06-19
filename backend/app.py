"""
Project: Contract Proposal Agent
Author: ann.marie783@gmail.com
Date: 2025-06-19
File: app.py
Purpose: Flask app for the contract proposal agent
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/upload', methods=['POST'])
def upload():
    #NEED TO ADD FILE PARSING< CHUNK EMBED ETC
    return jsonify({"message": "File uploaded successfully."}), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    #NEED TO ADD CHAT LOGIC
    user_message = request.json.get("message")
    doc_id = request.json.get("doc_id")
    return jsonify({"response": "LLM will answer here."}), 200


if __name__ == '__main__':
    app.run(debug=True)
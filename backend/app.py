"""
Project: Contract Proposal Agent
Author: ann.marie783@gmail.com
Date: 2025-06-19
File: app.py
Purpose: Flask app for the contract proposal agent
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import logging
from rag_utils import parse_and_index_document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

#Creating storage for the app
STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

#Upload endpoint
@app.route('/api/upload', methods=['POST'])
def upload():
    """
    Receives an uploaded file and saves it to the storage directory with a UUID.
    """
    try:
        if 'file' not in request.files:
            logger.error("No file provided in request")
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            logger.error("No file selected")
            return jsonify({"error": "No file selected"}), 400
        
        filename = file.filename
        logger.info(f"Processing upload for file: {filename}")

        # Generate a UUID for the file
        doc_id = str(uuid.uuid4())
        
        # Create the file path with UUID prefix
        file_path = os.path.join(STORAGE_DIR, f"{doc_id}_{filename}")
        logger.info(f"Saving file to: {file_path}")

        # Save the file to the storage directory
        file.save(file_path)
        logger.info(f"File saved successfully with doc_id: {doc_id}")

        ##call the parsing utility
        num_chunks = parse_and_index_document(file_path, doc_id, STORAGE_DIR)

        return jsonify({
            "message": f"File '{filename}' uploaded successfully with {num_chunks} chunks.",
            "doc_id": doc_id
        }), 200
        
    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}")
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500
    



@app.route('/api/chat', methods=['POST'])
def chat():
    #NEED TO ADD CHAT LOGIC
    user_message = request.json.get("message")
    doc_id = request.json.get("doc_id")
    return jsonify({"response": "LLM will answer here."}), 200

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(port=8000, debug=True)
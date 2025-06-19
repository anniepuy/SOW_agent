"""
Project: Contract Proposal Agent
Author: ann.marie783@gmail.com
Date: 2025-06-19
File: test_app.py
Purpose: Simple health check test for the Flask app.
"""

import unittest
import sys
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_health(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get("status"), "ok")
    
    def test_upload_document(self):
        response = self.client.post('/api/upload_document', data={
            'file': (b'Test file content', 'testfile.txt')
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"RFP uploaded and processed", response.data)

    def test_chat_endpoint(self):
        response = self.client.post('/api/chat', json={
            "message": "What is this RFP about?",
            "rfp_id": "dummy_id"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"LLM will answer here", response.data)

if __name__ == '__main__':
    unittest.main()
            
            
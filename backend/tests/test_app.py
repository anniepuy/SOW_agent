"""
Project: Contract Proposal Agent
Author: ann.marie783@gmail.com
Date: 2025-06-19
File: test_app.py
Purpose: Unit tests for the Flask app. Uses python unittest: https://docs.python.org/3/library/unittest.html and keeps a log file.
"""

import unittest
import sys
import os
import logging
from datetime import datetime

# Configure logging
def setup_logging():
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = os.path.join(log_dir, f'test_app_{timestamp}.log')
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)  # Also print to console
        ]
    )
    return logging.getLogger(__name__)

# Setup logger
logger = setup_logging()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

class FlaskAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up logging for the test class"""
        cls.logger = logging.getLogger(f"{cls.__name__}")
        cls.logger.info("=" * 50)
        cls.logger.info(f"Starting test suite: {cls.__name__}")
        cls.logger.info("=" * 50)
    
    def setUp(self):
        """Set up test environment before each test"""
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{self._testMethodName}")
        self.logger.info(f"Setting up test: {self._testMethodName}")
        
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.logger.info("Flask test client configured")

    def tearDown(self):
        """Clean up after each test"""
        self.logger.info(f"Tearing down test: {self._testMethodName}")
        self.logger.info("-" * 30)

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests in the class"""
        cls.logger.info("=" * 50)
        cls.logger.info(f"Completed test suite: {cls.__name__}")
        cls.logger.info("=" * 50)

    def test_upload_file(self):
        """Test file upload endpoint"""
        self.logger.info("Testing file upload endpoint")
        
        try:
            # Prepare test data
            test_file_content = b'Test file content'
            test_filename = 'test.pdf'
            self.logger.info(f"Preparing test file: {test_filename}")
            
            # Make request
            self.logger.info("Making POST request to /api/upload")
            response = self.client.post('/api/upload', 
                                        data={'file': (test_file_content, test_filename)})
            
            # Log response details
            self.logger.info(f"Response status code: {response.status_code}")
            self.logger.info(f"Response data: {response.data}")
            
            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'File uploaded successfully', response.data)
            
            self.logger.info("✓ File upload test passed")
            
        except Exception as e:
            self.logger.error(f"✗ File upload test failed: {str(e)}")
            raise

    def test_chat(self):
        """Test chat endpoint"""
        self.logger.info("Testing chat endpoint")
        
        try:
            # Prepare test data
            test_message = 'What is this document about?'
            test_doc_id = 'test_doc_id'
            test_payload = {'message': test_message, 'doc_id': test_doc_id}
            
            self.logger.info(f"Test message: {test_message}")
            self.logger.info(f"Test document ID: {test_doc_id}")
            
            # Make request
            self.logger.info("Making POST request to /api/chat")
            response = self.client.post('/api/chat', json=test_payload)
            
            # Log response details
            self.logger.info(f"Response status code: {response.status_code}")
            self.logger.info(f"Response data: {response.data}")
            
            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'LLM will answer here', response.data)
            
            self.logger.info("✓ Chat test passed")
            
        except Exception as e:
            self.logger.error(f"✗ Chat test failed: {str(e)}")
            raise

if __name__ == '__main__':
    # Log test execution start
    logger.info("Starting test execution")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {os.getcwd()}")
    
    # Run tests
    unittest.main(verbosity=2)
    
    # Log test execution completion
    logger.info("Test execution completed")
            
            
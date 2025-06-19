"""
Project: Contract Proposal Agent
Author: ann.marie783@gmail.com
Date: 2025-06-19
File: streamlist_app.py
Purpose: Simple frontend for LLM app
"""

import streamlit as st
import requests
import io

BACKEND_URL = "http://localhost:8000/api"

st.title("Contract Proposal Agent")

#Upload RFP
st.header("Upload a new RFP")
rfp_file = st.file_uploader("Upload a document (PDF, DOCX, etc.)", 
                            type = ["pdf", "docx", "txt"])

if rfp_file and st.button("Submit RFP"):    
    try:
        # Get file content as bytes to avoid encoding issues
        file_content = rfp_file.read()
        # Reset file pointer for potential future reads
        rfp_file.seek(0)
        
        # Create file tuple with proper filename and content type
        files = {
            "file": (
                rfp_file.name,  # Use original filename
                io.BytesIO(file_content),  # Use BytesIO for binary content
                rfp_file.type or "application/octet-stream"  # Fallback content type
            )
        }
        
        response = requests.post(f"{BACKEND_URL}/upload", files=files)
        
        if response.status_code == 200:
            st.success(response.json().get("message"))
        else:
            st.error(f"Upload failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")

# Chat will LLM
st.header("Chat with the LLM")
selected_rfp = st.selectbox("Select an RFP", ["(LOAD FROM BACKEND)"])
user_input = st.text_input("Ask a question:")
if st.button("Send") and user_input:
    try:
        payload = {"message": user_input, "rfp_id": selected_rfp}
        response = requests.post(f"{BACKEND_URL}/chat", json=payload)
        
        if response.status_code == 200:
            st.write("AI Response:", response.json().get("response"))
        else:
            st.error(f"Chat request failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        st.error(f"Error sending message: {str(e)}")

# TODO - add history view, proposal approval, Agent actions, etc
"""
Project: Contract Proposal Agent
Author: ann.marie783@gmail.com
Date: 2025-06-19
File: streamlist_app.py
Purpose: Simple frontend for LLM app
"""

import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/api"

st.title("Contract Proposal Agent")

#Upload RFP
st.header("Upload a new RFP")
rfp_file = st.file_uploader("Upload a document (PDF, DOCX, etc.)", 
                            type = ["pdf", "docx", "txt"])

if rfp_file and st.button("Submit RFP"):    
    files = {"file": (rfp_file.getvalue(), rfp_file.type)}
    response = requests.post(f"{BACKEND_URL}/upload", files=files)
    st.success(response.json().get("message"))

# Chat will LLM
st.header("Chat with the LLM")
selected_rfp = st.selectbox("Select an RFP", ["(LOAD FROM BACKEND)"])
user_input = st.text_input("Ask a question:")
if st.button("Send") and user_input:
    payload = {"message": user_input, "rfp_id": selected_rfp}
    response = requests.post(f"{BACKEND_URL}/chat", json=payload)
    st.write("AI Response:",response.json().get("response"))

# TODO - add history view, proposal approval, Agent actions, etc
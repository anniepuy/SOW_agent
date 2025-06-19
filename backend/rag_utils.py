"""
Project: Contract Proposal Agent
Author: ann.marie783@gmail.com
Date: 2025-06-19
File: rag_utils.py
Purpose: Document parsing, chunking and embedding creation for the RAG pipeline.
"""

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

def get_loader(file_path):
    """
    Get the appropriate loader based on file extension
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return PyPDFLoader(file_path)
    elif file_extension == '.txt':
        return TextLoader(file_path)
    elif file_extension in ['.docx', '.doc']:
        return Docx2txtLoader(file_path)
    else:
        # Default to text loader for unknown file types
        return TextLoader(file_path)

#Parse the document into chunks, embed the chunks, and store into ChromaDB
def parse_and_index_document(doc_path, doc_id, storage_dir):
    """
    Load and parse the document.
    """
    try:
        loader = get_loader(doc_path)
        docs = loader.load()
    except Exception as e:
        print(f"Error loading document: {e}")
        # Return 0 chunks if loading fails
        return 0

    """
    Split the document into chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100,
    )
    all_chunks  = []
    for doc in docs:
        splits = text_splitter.create_documents([doc.page_content])
        all_chunks.extend(splits)

    """
    Create embeddings for the chunks
    """
    try:
        embeddings = OllamaEmbeddings(model="llama3:8b")
    except Exception as e:
        print(f"Error creating embeddings: {e}")
        # Return 0 chunks if embedding creation fails
        return 0

    """
    Store the chunks in ChromaDB
    """
    try:
        vector_dir = os.path.join(storage_dir, doc_id, "chroma_index")
        os.makedirs(vector_dir, exist_ok=True)
        vectordb = Chroma.from_documents(
            documents = all_chunks,
            embedding = embeddings,
            persist_directory = vector_dir,
        )

        # ChromaDB 0.4.x+ automatically persists data, no need for manual persist()
        return len(all_chunks)
    except Exception as e:
        print(f"Error storing in vector database: {e}")
        return 0
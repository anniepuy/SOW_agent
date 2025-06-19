"""
Project: Contract Proposal Agent
Author: ann.marie783@gmail.com
Date: 2025-06-19
File: rag_utils.py
Purpose: Document parsing, chunking and embedding creation for the RAG pipeline.
"""

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

#Parse the document into chunks, embed the chunks, and store into ChromaDB
def parse_and_index_document(doc_path, doc_id, storage_dir):
    """
    Load and parse the document.
    """
    loader = UnstructuredLoader(doc_path)
    docs = loader.load()

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
    embeddings = OllamaEmbeddings(model="llama3")

    """
    Store the chunks in ChromaDB
    """
    vector_dir = os.path.join(storage_dir, doc_id, "chroma_index")
    os.makedirs(vector_dir, exist_ok=True)
    vectordb = Chroma.from_documents(
        documents = all_chunks,
        embedding = embeddings,
        persist_directory = vector_dir,
    )

    """
    Persist the vectorstore
    """
    vectordb.persist()
    return len(all_chunks)
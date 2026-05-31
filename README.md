# LLM-Powered RAG Assistant

## Overview

LLM-Powered RAG Assistant is a Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions based on their content.

The system extracts text from PDFs, converts the text into embeddings using Sentence Transformers, stores embeddings in ChromaDB, retrieves relevant context, and generates answers using the Groq LLM API.

## Features

* Upload multiple PDF files
* Automatic text extraction
* Text chunking using LangChain
* Vector storage using ChromaDB
* Semantic search with embeddings
* Context-aware question answering
* FastAPI backend

## Technologies Used

* Python
* FastAPI
* ChromaDB
* Sentence Transformers
* LangChain
* Groq API
* PyPDF

## Project Workflow

1. Upload PDF documents
2. Extract text from PDFs
3. Split text into chunks
4. Generate embeddings
5. Store embeddings in ChromaDB
6. Retrieve relevant chunks
7. Send context to Groq LLM
8. Generate accurate answers

## Future Enhancements

* User authentication
* Chat history
* Multi-document retrieval
* Web interface using React
* Cloud deployment

## Author

Arthi Reddy
B.Tech Information Technology

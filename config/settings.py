"""
Configuration settings for RAG system
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Paths
PDF_DATA_PATH = "./data/pdf_data"
TEXT_DATA_PATH = "./data/text_data"
NEW_PDF_PATH = "./data/new_pdfs"
NEW_TEXT_PATH = "./data/new_texts"
MODELS_CACHE_PATH = "./models"

# Vector Store Settings
COLLECTION_NAME = "rag_collection"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVAL_K = 3

# Embedding Model Settings
OLLAMA_MODEL = "mxbai-embed-large:latest"
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_NUM_THREADS = 10

HUGGINGFACE_MODEL = "sentence-transformers/all-MiniLM-L12-v2"

# LLM Settings
GROQ_MODEL = "openai/gpt-oss-120b"
GROQ_TEMPERATURE = 0.2
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Web URLs for initial data loading
WEB_URLS = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Machine_learning",
    "https://en.wikipedia.org/wiki/Deep_learning",
    "https://en.wikipedia.org/wiki/Natural_language_processing",
    "https://en.wikipedia.org/wiki/Computer_vision"
]


# AstraDB Settings
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_NAMESPACE = os.getenv("ASTRA_DB_NAMESPACE", "default_keyspace")



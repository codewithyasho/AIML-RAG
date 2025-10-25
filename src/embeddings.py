"""
Embedding model initialization
"""
from langchain_ollama import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import (
    OLLAMA_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_NUM_THREADS,
    HUGGINGFACE_MODEL,
    MODELS_CACHE_PATH
)


def get_ollama_embeddings():
    """Initialize Ollama embeddings"""
    embeddings = OllamaEmbeddings(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        num_thread=OLLAMA_NUM_THREADS
    )
    print("✅ Ollama embeddings initialized")
    return embeddings


def get_huggingface_embeddings():
    """Initialize HuggingFace embeddings"""
    embeddings = HuggingFaceEmbeddings(
        model_name=HUGGINGFACE_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={
            "normalize_embeddings": True,
            "batch_size": 32
        },
        cache_folder=MODELS_CACHE_PATH,
        show_progress=True
    )
    print("✅ HuggingFace embeddings initialized")
    return embeddings

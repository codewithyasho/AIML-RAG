"""
AstraDB vector store operations
"""
import os
from langchain_astradb import AstraDBVectorStore
from config.settings import ASTRA_DB_API_ENDPOINT, ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_NAMESPACE, COLLECTION_NAME


def load_vector_store(embeddings):
    """Load existing vector store from AstraDB"""
    vectorstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_NAMESPACE,
    )

    try:
        print(f"📂 Loaded AstraDB collection '{COLLECTION_NAME}'")
    except Exception as e:
        print(f"📂 Connected to AstraDB vector store (collection: {COLLECTION_NAME})")

    return vectorstore


def create_vector_store(documents, embeddings):
    """Create/add to vector store from documents"""
    vectorstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_NAMESPACE,
    )
    
    # Add documents to the collection
    vectorstore.add_documents(documents)
    
    print(f"💾 Created AstraDB vector store with {len(documents)} documents")

    return vectorstore


def add_new_documents_to_vectorstore(vectorstore, documents):
    """Add new documents to existing vector store"""
    vectorstore.add_documents(documents)
    
    print(f"➕ Added {len(documents)} documents to AstraDB")

    return vectorstore

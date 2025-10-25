"""
Main RAG System - Simple and Clean
"""
from src.utils import suppress_warnings, print_response
from src.embeddings import get_ollama_embeddings
from src.vector_store import load_vector_store
from src.chain import create_rag_chain

# Suppress warnings for clean output
suppress_warnings()


def main():
    """Main RAG application"""
    print("🚀 Starting RAG System...\n")

    # Load embeddings
    embeddings = get_ollama_embeddings()

    # Load vector store
    vectorstore = load_vector_store(embeddings)

    # Create RAG chain
    rag_chain = create_rag_chain(vectorstore)

    # Ask questions
    query = input("Enter your question: ")
    print(f"\n❓ Question: {query}")

    response = rag_chain.invoke({"input": query})
    print_response(response)


if __name__ == "__main__":
    main()
    print("\n🚀 RAG System finished.")

"""
Utility functions
"""
import warnings


def suppress_warnings():
    """Suppress unnecessary warnings"""
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore")


def print_response(response: dict, show_sources: bool = True):
    """Pretty print RAG response"""
    print("\n" + "="*50)
    print("🤖 ANSWER:")
    print("="*50)
    print(response["answer"])

    if show_sources and "context" in response:
        print("\n" + "="*50)
        print("📚 SOURCES:")
        print("="*50)
        for i, doc in enumerate(response["context"][:3], 1):
            source = doc.metadata.get('source', 'Unknown')
            print(f"\n{i}. {source}")
            print(f"   Preview: {doc.page_content[:150]}...")

"""
Add new documents to Pinecone
"""
from src.utils import suppress_warnings
from src.data_loaders import load_pdf_files, load_text_files, chunk_documents
from src.embeddings import get_huggingface_embeddings
from src.vector_store import load_vector_store, add_new_documents_to_vectorstore
from config.settings import NEW_PDF_PATH, NEW_TEXT_PATH

suppress_warnings()

print("📥 Adding new documents to Pinecone...\n")

# Load new files
new_pdfs = load_pdf_files(NEW_PDF_PATH)
new_texts = load_text_files(NEW_TEXT_PATH)

# Combine and chunk
all_new_docs = new_pdfs + new_texts
new_chunks = chunk_documents(all_new_docs)

# Load embeddings and vector store
embeddings = get_huggingface_embeddings()
vectorstore = load_vector_store(embeddings)

# Add new documents to Pinecone
add_new_documents_to_vectorstore(vectorstore, new_chunks)

print("\n✅ New documents added to Pinecone!")

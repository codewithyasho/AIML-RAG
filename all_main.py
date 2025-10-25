"""
RAG System for Document Question Answering
Supports: PDF, Text files, and Web data
Uses: Ollama/HuggingFace embeddings + Groq LLM
"""


from langchain_community.document_loaders import TextLoader, WebBaseLoader, DirectoryLoader, PyPDFDirectoryLoader
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_classic.chains import create_retrieval_chain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore")

load_dotenv()


### DATA INGESTION ###

# loading all text files from a directory
def load_text_files(directory_path):
    text_loader = DirectoryLoader(

        path=directory_path,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True

    )

    text_docs = text_loader.load()

    print(f"Loaded of text documents: {len(text_docs)}")

    return text_docs


# web loader
def load_web_data():
    web_loader = WebBaseLoader(
        [
            "https://en.wikipedia.org/wiki/Artificial_intelligence",
            "https://en.wikipedia.org/wiki/Machine_learning",
            "https://en.wikipedia.org/wiki/Deep_learning",
            "https://en.wikipedia.org/wiki/Natural_language_processing",
            "https://en.wikipedia.org/wiki/Computer_vision"
        ]
    )

    web_data = web_loader.load()

    print(f"Loaded of web data: {len(web_data)}")

    return web_data


# loading all PDF files from a directory
def load_pdf_files(directory_path):

    pdf_loader = PyPDFDirectoryLoader(
        path=directory_path,
        glob="**/[!.]*.pdf",  # Default pattern
        silent_errors=False,
        recursive=False,
        extract_images=True
    )

    pdf_docs = pdf_loader.load()

    print(f"Loaded of PDF documents: {len(pdf_docs)}")

    return pdf_docs


## FUNCTION TO LOAD NEWLY ADDED DOCUMENTS ###

# Load NEW text files
def load_new_text_files(directory_path):
    new_text_loader = DirectoryLoader(
        path=directory_path,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    new_text_docs = new_text_loader.load()

    print(f"📄 Loaded {len(new_text_docs)} new text files")

    return new_text_docs


# Load NEW PDFs
# ============================================
def load_new_pdf_files(directory_path):
    new_pdf_loader = PyPDFDirectoryLoader(
        path=directory_path,
        glob="**/*.pdf"
    )

    new_pdf_docs = new_pdf_loader.load()

    print(f"📑 Loaded {len(new_pdf_docs)} new PDF pages")

    return new_pdf_docs


## SPLITTING DOCUMENTS INTO CHUNKS ###

# chunking the documents
def chunk_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunked_documents = text_splitter.split_documents(documents)

    print(f"Total chunks: {len(chunked_documents)}")

    return chunked_documents


## CREATING VECTOR EMBEDDINGS ###
# ollama embeddings function
def use_ollama_embedding():
    ollama_embeddings = OllamaEmbeddings(

        model="mxbai-embed-large:latest",
        base_url="http://localhost:11434",  # Ollama server URL
        num_thread=10  # Number of threads for processing
    )

    print("Ollama Embeddings initialized.")

    return ollama_embeddings


# huggingface embeddings function
def use_huggingface_embedding():
    huggingface_embeddings = HuggingFaceEmbeddings(

        model_name="sentence-transformers/all-MiniLM-L12-v2",
        model_kwargs={"device": "cpu"},

        encode_kwargs={
            "normalize_embeddings": True,  # ADD THIS - Important for similarity!
            "batch_size": 32  # Optional but recommended
        },

        cache_folder="./models",
        show_progress=True

    )

    print("HuggingFace Embeddings initialized.")

    return huggingface_embeddings


## 1. CREATING VECTOR STORE ###
def create_vector_store(documents, embeddings):
    created_vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="rag_collection",
        persist_directory="./chroma_db"  # Saves to disk

    )

    print("Vector store created and persisted to disk.")
    print(
        f"Total documents in vector store: {created_vectorstore._collection.count()}")

    return created_vectorstore


##  2. Load existing vector store (NO re-embedding needed!) ##
def load_vector_store(embeddings):
    loaded_vectorstore = Chroma(

        collection_name="rag_collection",
        embedding_function=embeddings,
        persist_directory="./chroma_db"  # Points to existing folder

    )

    print("Vector store loaded from disk.")
    print(
        f"Total documents in vector store: {loaded_vectorstore._collection.count()}")

    return loaded_vectorstore


## APPEND NEW DOCUMENTS TO VECTOR STORE ###
def append_new_documents_to_vector_store(new_documents):
    vectorstore.add_documents(new_documents)

    print("New documents appended to vector store.")
    print(
        f"Updated total documents in vector store: {vectorstore._collection.count()}")


if __name__ == "__main__":

    # SIMPLY CALLING THE FUNCTIONS ###
    # text_documents = load_text_files("./data/text_data")
    # web_documents = load_web_data()
    # pdf_documents = load_pdf_files("./data/pdf_data")

    # Combine all documents into one list
    # all_documents = text_documents + pdf_documents + web_documents

    # all_chunked_documents = chunk_documents(all_documents)

    embeddings = use_ollama_embedding()

    vectorstore = load_vector_store(embeddings)

    ## CREATING THE RETRIVER ###
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    ## CREATING THE CHAT MODEL ###
    llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2)

    ## CREATING THE PROMPT ###
    prompt = ChatPromptTemplate.from_template(
        """   
        Answer the following question based only on the provided context. 
        Think step by step before answering. If you don't know the answer, just say that you don't know.

        <context>
        {context}
        </context>

        Question: {input}
        """
    )

    ## BUILDING FINAL RAG CHAIN WITH RETRIEVER & PROMPT ###
    document_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, document_chain)

    ## TESTING THE RAG CHAIN ###
    query = "what is embeddings?"

    response = rag_chain.invoke(
        input={"input": query}
    )

    print("\nRAG Response:")
    print(response["answer"])

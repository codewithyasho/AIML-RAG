"""
Document loading and chunking functions
"""
from langchain_community.document_loaders import (
    TextLoader,
    WebBaseLoader,
    DirectoryLoader,
    PyPDFDirectoryLoader
)
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP


def load_text_files(directory_path: str):
    """Load all text files from a directory"""
    text_loader = DirectoryLoader(
        path=directory_path,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True
    )
    text_docs = text_loader.load()
    print(f"📄 Loaded {len(text_docs)} text documents")
    return text_docs


def load_pdf_files(directory_path: str):
    """Load all PDF files from a directory"""
    pdf_loader = PyPDFDirectoryLoader(
        path=directory_path,
        glob="**/[!.]*.pdf",
        silent_errors=False,
        recursive=False,
        extract_images=True
    )
    pdf_docs = pdf_loader.load()
    print(f"📑 Loaded {len(pdf_docs)} PDF documents")
    return pdf_docs


def load_web_data(urls: list):
    """Load data from web URLs"""
    web_loader = WebBaseLoader(urls)
    web_docs = web_loader.load()
    print(f"🌐 Loaded {len(web_docs)} web pages")
    return web_docs


def chunk_documents(documents: list):
    """Split documents into chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✂️  Created {len(chunks)} chunks")
    return chunks

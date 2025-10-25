# 🤖 RAG Document Q&A System

A comprehensive **Retrieval-Augmented Generation (RAG)** system built with LangChain, **AstraDB**, and Groq LLM for intelligent document question answering. This production-ready system supports multiple data sources and provides both CLI and web interfaces.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [System Components](#system-components)
- [API Reference](#api-reference)
- [Contributing](#contributing)

---

## 🎯 Overview

This RAG system enables users to:
- 📚 **Load documents** from multiple sources (PDFs, text files, web pages)
- 🔍 **Query documents** using natural language
- 💬 **Get AI-powered answers** with source citations
- 🎨 **Interact via multiple interfaces** (CLI, Gradio web UI)
- 📦 **Incrementally add documents** without rebuilding the entire database

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Ingestion Layer                     │
│  (PDFs, Text Files, Web Pages) → Document Loaders           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Processing Layer                           │
│  Text Splitter → Chunks (1000 chars, 200 overlap)          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Embedding Layer                            │
│  Ollama (mxbai-embed-large) / HuggingFace (all-MiniLM)     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                Vector Store (AstraDB)                        │
│  Cloud-native vector database with similarity search        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Retrieval Layer                            │
│  Similarity Search (k=3) → Relevant Context                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Generation Layer                          │
│  Groq LLM (gpt-oss-120b) → Contextual Answers              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  User Interfaces                             │
│  CLI (main.py) | Gradio UI (app.py, app_advanced.py)       │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### Core Features
- ✅ **Multi-Source Document Loading**
  - PDF files (with image extraction)
  - Text files (.txt)
  - Web pages (via URL)
  
- ✅ **Advanced Text Processing**
  - Recursive character splitting
  - Configurable chunk size (1000 chars) and overlap (200 chars)
  - Metadata preservation

- ✅ **Flexible Embedding Options**
  - **Ollama**: Local embeddings (mxbai-embed-large)
  - **HuggingFace**: Sentence transformers (all-MiniLM-L12-v2)

- ✅ **Persistent Vector Storage**
  - AstraDB cloud vector database
  - Fast similarity search with serverless scaling
  - Incremental document addition

- ✅ **Powerful LLM Integration**
  - Groq API (gpt-oss-120b model)
  - Customizable temperature
  - Context-aware responses

- ✅ **Multiple User Interfaces**
  - **CLI**: Simple command-line interface
  - **Gradio Basic**: Clean chat interface with examples
  - **Gradio Advanced**: Enhanced UI with settings, source display, and statistics

- ✅ **Production-Ready Architecture**
  - Modular design with separation of concerns
  - Centralized configuration
  - Warning suppression for clean output
  - Error handling

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | LangChain | Latest |
| **Vector DB** | AstraDB (DataStax) | Latest |
| **LLM** | Groq (gpt-oss-120b) | API |
| **Embeddings** | Ollama / HuggingFace | Local/Cloud |
| **Web UI** | Gradio | Latest |
| **Document Processing** | PyPDF, BeautifulSoup4 | Latest |
| **Environment** | Python | 3.8+ |

---

## 📁 Project Structure

```
project5/
├── 📄 README.md                    # Project documentation
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env                         # Environment variables (GROQ_API_KEY)
│
├── 🎯 Main Entry Points
│   ├── main.py                     # Simple CLI interface
│   ├── app.py                      # Basic Gradio UI
│   ├── app_advanced.py             # Advanced Gradio UI with settings
│   ├── all_main.py                 # Legacy/monolithic implementation
│   └── add_new_docs.py             # Script to add new documents
│
├── 📂 config/                      # Configuration module
│   ├── __init__.py
│   └── settings.py                 # Centralized settings (paths, models, params)
│
├── 📂 src/                         # Core system modules
│   ├── __init__.py
│   ├── data_loaders.py             # Document loading functions
│   ├── embeddings.py               # Embedding model initialization
│   ├── vector_store.py             # Vector store operations
│   ├── chain.py                    # RAG chain construction
│   └── utils.py                    # Utility functions
│
├── 📂 data/                        # Data directories
│   ├── pdf_data/                   # Initial PDF documents
│   ├── text_data/                  # Initial text documents
│   │   ├── ai.txt
│   │   └── ai2.txt
│   ├── new_pdfs/                   # New PDFs to add
│   └── new_texts/                  # New text files to add
│
├── 📂 chroma_db/                   # Persistent vector database
│   ├── chroma.sqlite3              # SQLite database
│   └── 6ecace5f-.../               # Collection data
│
└── 📂 models/                      # Cached embedding models (auto-created)
```

---

## 🚀 Installation

### Prerequisites
- **Python 3.8+**
- **AstraDB Account** - [Sign up free at DataStax](https://astra.datastax.com/)
- **Ollama** (for local embeddings) - [Install Ollama](https://ollama.ai/)
- **Groq API Key** - [Get from Groq Console](https://console.groq.com/)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd project5
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Ollama (for local embeddings)
```bash
# Install and pull the embedding model
ollama pull mxbai-embed-large:latest
```

### Step 5: Set Up AstraDB
Follow the detailed guide in [`ASTRADB_SETUP.md`](ASTRADB_SETUP.md) to:
1. Create an AstraDB database
2. Get your API endpoint and token
3. Configure environment variables

### Step 6: Configure Environment Variables
Create a `.env` file in the project root:
```env
# AstraDB Configuration
ASTRA_DB_API_ENDPOINT=https://your-database-id-your-region.apps.astra.datastax.com
ASTRA_DB_APPLICATION_TOKEN=AstraCS:xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ASTRA_DB_NAMESPACE=default_keyspace

# LLM API Key
GROQ_API_KEY=your_groq_api_key_here
```

### Step 7: Initialize Vector Store (First Time Only)
If starting fresh, run the monolithic script to create initial vector store:
```bash
python all_main.py
```

Or create it programmatically using the modular approach (see Usage section).

---

## ⚙️ Configuration

All settings are centralized in `config/settings.py`:

### Path Settings
```python
PDF_DATA_PATH = "./data/pdf_data"
TEXT_DATA_PATH = "./data/text_data"
NEW_PDF_PATH = "./data/new_pdfs"
NEW_TEXT_PATH = "./data/new_texts"
```

### AstraDB Settings
```python
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_NAMESPACE = os.getenv("ASTRA_DB_NAMESPACE", "default_keyspace")
COLLECTION_NAME = "rag_collection"
```

### Embedding Settings
```python
OLLAMA_MODEL = "mxbai-embed-large:latest"
OLLAMA_BASE_URL = "http://localhost:11434"
HUGGINGFACE_MODEL = "sentence-transformers/all-MiniLM-L12-v2"
```

### Text Processing
```python
CHUNK_SIZE = 1000              # Characters per chunk
CHUNK_OVERLAP = 200            # Overlap between chunks
RETRIEVAL_K = 3                # Number of chunks to retrieve
```

### LLM Settings
```python
GROQ_MODEL = "openai/gpt-oss-120b"
GROQ_TEMPERATURE = 0.2         # Lower = more deterministic
```

---

## 💻 Usage

### 1. CLI Interface (Simple)
```bash
python main.py
```
**Features:**
- Simple command-line interaction
- Enter a question and get an answer
- Shows source documents

### 2. Gradio Web UI (Basic)
```bash
python app.py
```
**Features:**
- Clean chat interface
- Example questions
- Automatic source citations
- Share link generation
- Port: 7860

### 3. Gradio Web UI (Advanced)
```bash
python app_advanced.py
```
**Features:**
- All basic features plus:
- Toggle source display
- Temperature control slider
- System statistics panel
- Document preview in sources
- Enhanced UI/UX
- Port: 7861

### 4. Adding New Documents
```bash
python add_new_docs.py
```
**Process:**
1. Place PDFs in `data/new_pdfs/`
2. Place text files in `data/new_texts/`
3. Run the script
4. Documents are automatically embedded and added to vector store

---

## 🔧 System Components

### 1. Data Loaders (`src/data_loaders.py`)
**Functions:**
- `load_text_files(directory_path)` - Load .txt files
- `load_pdf_files(directory_path)` - Load PDFs with image extraction
- `load_web_data(urls)` - Scrape web pages
- `chunk_documents(documents)` - Split into chunks

**Example:**
```python
from src.data_loaders import load_pdf_files, chunk_documents

docs = load_pdf_files("./data/pdf_data")
chunks = chunk_documents(docs)
```

### 2. Embeddings (`src/embeddings.py`)
**Functions:**
- `get_ollama_embeddings()` - Local Ollama embeddings
- `get_huggingface_embeddings()` - HuggingFace embeddings

**Example:**
```python
from src.embeddings import get_ollama_embeddings

embeddings = get_ollama_embeddings()
```

### 3. Vector Store (`src/vector_store.py`)
**Functions:**
- `create_vector_store(documents, embeddings)` - Create new collection
- `load_vector_store(embeddings)` - Load existing collection
- `add_new_documents_to_vectorstore(vectorstore, documents)` - Add docs

**Example:**
```python
from src.vector_store import load_vector_store

vectorstore = load_vector_store(embeddings)
print(f"Connected to AstraDB collection")
```

### 4. RAG Chain (`src/chain.py`)
**Functions:**
- `get_llm()` - Initialize Groq LLM
- `get_prompt()` - Get prompt template
- `create_rag_chain(vectorstore)` - Build complete RAG pipeline

**Example:**
```python
from src.chain import create_rag_chain

rag_chain = create_rag_chain(vectorstore)
response = rag_chain.invoke({"input": "What is AI?"})
print(response["answer"])
```

### 5. Utils (`src/utils.py`)
**Functions:**
- `suppress_warnings()` - Clean console output
- `print_response(response, show_sources)` - Pretty print results

---

## 📚 API Reference

### RAG Chain Response Structure
```python
response = {
    "input": "What is machine learning?",
    "answer": "Machine learning is...",
    "context": [
        Document(page_content="...", metadata={"source": "file.pdf"}),
        Document(page_content="...", metadata={"source": "web_page.html"}),
        ...
    ]
}
```

### Document Metadata
```python
doc.metadata = {
    "source": "/path/to/file.pdf",    # Source file
    "page": 5,                         # Page number (PDFs only)
}
```

---

## 🎨 Customization Examples

### Change Number of Retrieved Documents
```python
# In config/settings.py
RETRIEVAL_K = 5  # Default is 3
```

### Use HuggingFace Instead of Ollama
```python
# In your script
from src.embeddings import get_huggingface_embeddings

embeddings = get_huggingface_embeddings()
```

### Adjust Chunk Size
```python
# In config/settings.py
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 300
```

### Change LLM Temperature
```python
# In config/settings.py
GROQ_TEMPERATURE = 0.5  # More creative (0.0-1.0)
```

---

## 🐛 Troubleshooting

### Issue: "Ollama connection refused"
**Solution:** Ensure Ollama is running
```bash
ollama serve
```

### Issue: "GROQ_API_KEY not found"
**Solution:** Check your `.env` file exists and contains the key

### Issue: "AstraDB connection failed"
**Solution:** Check your credentials in `.env`
```bash
# Verify your ASTRA_DB_API_ENDPOINT and ASTRA_DB_APPLICATION_TOKEN
# Make sure database status is "Active" in AstraDB dashboard
```

### Issue: "Collection not found"
**Solution:** Initialize the database first (see ASTRADB_SETUP.md)
```bash
python all_main.py  # Create initial collection
```

### Issue: "Import errors"
**Solution:** Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📈 Performance Optimization

1. **Use Ollama for faster embeddings** (local, no API calls)
2. **Adjust `CHUNK_SIZE`** for better context (larger = more context)
3. **Tune `RETRIEVAL_K`** (higher = more sources but slower)
4. **Use HuggingFace embeddings** if Ollama unavailable
5. **AstraDB auto-scales** based on usage (serverless architecture)

---

## 🔐 Security Notes

- ⚠️ **Never commit `.env` file** to version control
- 🔑 **Keep GROQ_API_KEY and ASTRA_DB_APPLICATION_TOKEN secret**
- 📁 **Sanitize uploaded documents** before processing
- 🛡️ **Use environment variables** for all secrets
- 🔒 **AstraDB tokens** have role-based access control

---

## 🚦 Roadmap

- [ ] Add support for more document types (DOCX, CSV, JSON)
- [ ] Implement conversation memory
- [ ] Add user authentication
- [ ] Deploy to cloud (Hugging Face Spaces, Railway)
- [ ] Add document management UI
- [ ] Implement hybrid search (dense + sparse)
- [ ] Add multilingual support

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

Built with ❤️ by **Krish** using LangChain

---

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) - RAG framework
- [AstraDB](https://www.datastax.com/products/datastax-astra) - Vector database
- [Groq](https://groq.com/) - Fast LLM inference
- [Ollama](https://ollama.ai/) - Local LLM & embeddings
- [Gradio](https://gradio.app/) - Web UI framework

---

## 📞 Support

For issues, questions, or suggestions:
- 📧 Email: [your-email@example.com]
- 🐛 Issues: [GitHub Issues](link-to-issues)
- 💬 Discussions: [GitHub Discussions](link-to-discussions)

---

**⭐ If you find this project helpful, please give it a star!**

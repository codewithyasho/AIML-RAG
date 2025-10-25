"""
Streamlit UI for RAG System with AstraDB
"""
import streamlit as st
from src.utils import suppress_warnings
from src.embeddings import get_huggingface_embeddings
from src.vector_store import create_vector_store, load_vector_store
from src.chain import create_rag_chain
from src.data_loaders import load_text_files, load_pdf_files, load_web_data, chunk_documents
from config.settings import *

# Load documents and create vector store if not exists
if 'vectorstore' not in st.session_state:
    with st.spinner("🚀 Loading data and creating vector store..."):
        text_docs = load_text_files(TEXT_DATA_PATH)
        pdf_docs = load_pdf_files(PDF_DATA_PATH)
        web_docs = load_web_data(WEB_URLS)
        all_docs = text_docs + pdf_docs + web_docs
        chunks = chunk_documents(all_docs)
        embeddings = get_huggingface_embeddings()
        st.session_state.vectorstore = create_vector_store(chunks, embeddings)
        st.success("✅ Data loaded and vector store created!")

# Suppress warnings
suppress_warnings()

# Page configuration
st.set_page_config(
    page_title="Ai ML Q&A Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    .source-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        border-left: 4px solid #ff9800;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_rag_system():
    """Initialize RAG system (cached to avoid reloading)"""
    with st.spinner("🚀 Loading RAG system..."):
        embeddings = get_huggingface_embeddings()
        vectorstore = load_vector_store(embeddings)
        rag_chain = create_rag_chain(vectorstore)
    return rag_chain


def display_chat_message(role, content, sources=None):
    """Display a chat message with styling"""
    css_class = "user-message" if role == "user" else "assistant-message"
    icon = "👤" if role == "user" else "🤖"
    
    st.markdown(f"""
        <div class="chat-message {css_class}">
            <strong>{icon} {role.capitalize()}</strong>
            <div style="margin-top: 0.5rem;">{content}</div>
        </div>
    """, unsafe_allow_html=True)
    
    if sources and role == "assistant":
        with st.expander("📚 View Sources", expanded=False):
            for i, doc in enumerate(sources, 1):
                source = doc.metadata.get('source', 'Unknown')
                source_name = source.split('/')[-1].split('\\')[-1]
                content_preview = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                
                st.markdown(f"**{i}. {source_name}**")
                st.text(content_preview)
                st.divider()


def main():
    # Header
    st.title("Ai ML Q&A Assistant")
    st.markdown("Ask me anything about your documents! Powered by **AstraDB** and **LangChain**.")
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ Information")
        st.markdown("""
        ### About
        This RAG system uses:
        - 🗄️ **AstraDB** - Vector database
        - 🧠 **HuggingFace** - Embeddings
        - 🤖 **Groq** - LLM inference
        - 🔗 **LangChain** - Orchestration
        
        ### Features
        - ✅ Multi-source documents (PDFs, Text, Web)
        - ✅ Semantic search
        - ✅ Source citations
        - ✅ Real-time responses
        """)
        
        st.divider()
        
        st.header("💡 Example Questions")
        example_questions = [
            "What is machine learning?",
            "Explain embeddings",
            "What is artificial intelligence?",
            "How does deep learning work?"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"example_{question}", use_container_width=True):
                st.session_state.example_question = question
        
        st.divider()
        
        # Settings
        st.header("⚙️ Settings")
        show_sources = st.checkbox("Show source documents", value=True)
        st.session_state.show_sources = show_sources
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Initialize RAG system
    try:
        rag_chain = initialize_rag_system()
        st.success("✅ RAG system ready!", icon="✅")
    except Exception as e:
        st.error(f"❌ Error initializing RAG system: {str(e)}")
        st.stop()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(
            message["role"], 
            message["content"],
            message.get("sources") if st.session_state.get("show_sources", True) else None
        )
    
    # Handle example question click
    if "example_question" in st.session_state:
        user_input = st.session_state.example_question
        del st.session_state.example_question
    else:
        user_input = None
    
    # Chat input
    prompt = st.chat_input("Ask a question about your documents...")
    
    if prompt or user_input:
        question = prompt if prompt else user_input
        
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": question})
        display_chat_message("user", question)
        
        # Get response from RAG system
        with st.spinner("🤔 Thinking..."):
            try:
                response = rag_chain.invoke({"input": question})
                answer = response["answer"]
                sources = response.get("context", [])[:3]  # Get top 3 sources
                
                # Add assistant message to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
                
                # Display assistant message
                display_chat_message(
                    "assistant", 
                    answer,
                    sources if st.session_state.get("show_sources", True) else None
                )
                
            except Exception as e:
                error_message = f"❌ Error: {str(e)}"
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })
                display_chat_message("assistant", error_message)
        
        st.rerun()
    
    # Footer
    st.divider()
    st.markdown("""
        <div style="text-align: center; color: #666; padding: 1rem;">
            Built with ❤️ using Streamlit, LangChain, and AstraDB
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

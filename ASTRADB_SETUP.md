# AstraDB Setup Guide

This project uses **DataStax AstraDB** as the vector database for storing document embeddings.

## Prerequisites

1. Create a free AstraDB account at [https://astra.datastax.com](https://astra.datastax.com)
2. Python environment with required packages installed

## Step 1: Create an AstraDB Database

1. Go to [AstraDB Console](https://astra.datastax.com)
2. Click **"Create Database"**
3. Choose:
   - **Database name**: `rag_database` (or any name you prefer)
   - **Keyspace name**: `default_keyspace` (or any name you prefer)
   - **Provider**: Choose your preferred cloud provider (AWS, GCP, Azure)
   - **Region**: Select the region closest to you
4. Click **"Create Database"**
5. Wait for the database to become **Active** (usually takes 2-3 minutes)

## Step 2: Get Your Connection Credentials

### API Endpoint
1. In your database dashboard, click **"Connect"**
2. Copy the **API Endpoint** (looks like: `https://XXXX-XXXX.apps.astra.datastax.com`)

### Application Token
1. Go to your AstraDB dashboard
2. Click on your profile icon → **"Organization Settings"**
3. Go to **"Token Management"** tab
4. Click **"Generate Token"**
5. Select role: **"Database Administrator"**
6. Copy the **Token** (starts with `AstraCS:...`)
   - ⚠️ **Important**: Save this token securely! It won't be shown again.

## Step 3: Configure Environment Variables

1. Create a `.env` file in the project root (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your AstraDB credentials:
   ```bash
   # AstraDB Configuration
   ASTRA_DB_API_ENDPOINT=https://your-database-id-your-region.apps.astra.datastax.com
   ASTRA_DB_APPLICATION_TOKEN=AstraCS:xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ASTRA_DB_NAMESPACE=default_keyspace
   
   # LLM API Keys
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Step 4: Install Dependencies

Make sure `langchain-astradb` is installed:

```bash
pip install -r requirements.txt
```

The package `langchain-astradb` is already included in `requirements.txt`.

## Step 5: Initialize Your Vector Store

Run the initialization script to load your documents into AstraDB:

```bash
python all_main.py
```

This will:
- Load documents from your data folders
- Create embeddings
- Store them in AstraDB collection

## Verify Connection

The application will automatically:
1. Connect to AstraDB using your credentials
2. Create a collection named `rag_collection` (defined in `config/settings.py`)
3. Store document embeddings with metadata

## Collection Management

### View Collections
You can view your collections in the AstraDB dashboard:
1. Go to your database
2. Click on **"Data Explorer"** or **"CQL Console"**
3. Select your keyspace
4. You'll see the collection `rag_collection`

### Collection Schema
AstraDB automatically creates the collection with:
- **Vector dimension**: Based on your embedding model (e.g., 384 for `all-MiniLM-L12-v2`)
- **Similarity metric**: Cosine similarity
- **Metadata fields**: Source, content, and custom fields

## Configuration Options

You can customize settings in `config/settings.py`:

```python
# Collection name
COLLECTION_NAME = "rag_collection"

# Chunking settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval settings
RETRIEVAL_K = 3  # Number of documents to retrieve
```

## Benefits of AstraDB

✅ **Serverless**: No infrastructure to manage  
✅ **Scalable**: Auto-scales based on usage  
✅ **Fast**: Low-latency vector search  
✅ **Free Tier**: 25GB storage, 25M reads, 5M writes per month  
✅ **Multi-cloud**: Deploy on AWS, GCP, or Azure  
✅ **Integrated**: Built-in support in LangChain  

## Troubleshooting

### Error: "Could not connect to AstraDB"
- ✔️ Check your API endpoint is correct
- ✔️ Verify your token is valid and hasn't expired
- ✔️ Ensure database status is "Active"

### Error: "Collection not found"
- ✔️ Run the initialization script first
- ✔️ Check the collection name matches in `settings.py`

### Error: "Authentication failed"
- ✔️ Regenerate your application token
- ✔️ Make sure token has "Database Administrator" role
- ✔️ Update token in `.env` file

## Additional Resources

- [AstraDB Documentation](https://docs.datastax.com/en/astra/home/astra.html)
- [LangChain AstraDB Integration](https://python.langchain.com/docs/integrations/vectorstores/astradb)
- [AstraDB Python SDK](https://github.com/datastax/astrapy)

## Support

For issues:
- AstraDB: [DataStax Support](https://support.datastax.com/)
- LangChain: [LangChain Discord](https://discord.gg/langchain)

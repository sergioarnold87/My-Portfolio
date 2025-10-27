# 🏗️ RAG Demo Architecture

## 📐 System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      Streamlit Frontend                         │
│                        (app/main.py)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────┐          ┌────────────────────────┐    │
│  │  Upload Mode      │          │  Pre-loaded Mode       │    │
│  │  📤              │          │  📚                    │    │
│  │                   │          │                        │    │
│  │  • Drag & Drop    │          │  • data/ directory     │    │
│  │  • PDF, CSV, TXT  │          │  • .txt files          │    │
│  │  • MD files       │          │  • Discovery prompts   │    │
│  └────────┬──────────┘          └────────┬───────────────┘    │
│           │                              │                     │
└───────────┼──────────────────────────────┼─────────────────────┘
            │                              │
            ▼                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RAG Engine (rag_engine.py)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐      ┌──────────────────────┐       │
│  │ process_uploaded_    │      │ load_documents()     │       │
│  │ file()               │      │ create_vectorstore() │       │
│  │                      │      │                      │       │
│  │ 1. extract_text()    │      │ 1. Load .txt files   │       │
│  │ 2. chunk_text()      │      │ 2. Chunk documents   │       │
│  │ 3. create_embeddings │      │ 3. Create embeddings │       │
│  │ 4. build_vectorstore │      │ 4. Build vectorstore │       │
│  └──────────┬───────────┘      └──────────┬───────────┘       │
│             │                             │                    │
│             └──────────┬──────────────────┘                    │
│                        │                                       │
│                        ▼                                       │
│             ┌──────────────────────┐                          │
│             │ build_qa_chain()     │                          │
│             │                      │                          │
│             │ • OpenAI LLM         │                          │
│             │ • Retriever (k=3)    │                          │
│             │ • RetrievalQA chain  │                          │
│             └──────────┬───────────┘                          │
└────────────────────────┼────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     External Services                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌─────────────┐     │
│  │ OpenAI API   │    │ ChromaDB     │    │ LangChain   │     │
│  │              │    │              │    │             │     │
│  │ • Embeddings │    │ • Vector     │    │ • Chains    │     │
│  │ • GPT Models │    │   Storage    │    │ • Splitters │     │
│  │ • Completion │    │ • Similarity │    │ • Prompts   │     │
│  └──────────────┘    └──────────────┘    └─────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### Upload Mode Flow

```
User Upload
    │
    ├─ .txt/.md ──→ UTF-8 Decode ──┐
    │                               │
    ├─ .pdf ──→ PyPDF2 Extract ────┤
    │                               │
    └─ .csv ──→ Pandas to_string ──┘
                                    │
                                    ▼
                            Raw Text String
                                    │
                                    ▼
                    RecursiveCharacterTextSplitter
                    (chunk_size=800, overlap=100)
                                    │
                                    ▼
                            Text Chunks []
                                    │
                                    ▼
                        OpenAI Embeddings API
                                    │
                                    ▼
                            Vector Embeddings
                                    │
                                    ▼
                            ChromaDB Store
                                    │
                                    ▼
                                Retriever
                                    │
                                    ▼
                            RetrievalQA Chain
                                    │
                                    ▼
                            Ready for Queries
```

### Query Processing Flow

```
User Query
    │
    ▼
QA Chain
    │
    ├──→ Vectorstore.similarity_search(query, k=3)
    │         │
    │         ▼
    │    Top 3 Relevant Chunks
    │         │
    ├─────────┘
    │
    ▼
Prompt Construction
    │
    ├─ System Context
    ├─ Retrieved Chunks
    └─ User Question
    │
    ▼
OpenAI API Call
    │
    ▼
LLM Response
    │
    ▼
Display to User
```

---

## 🗂️ File Structure

```
rag-demo-data-engineering/
│
├── app/
│   ├── main.py              # Streamlit UI with dual modes
│   ├── rag_engine.py        # Core RAG logic + upload processing
│   └── prompts.py           # Discovery prompt library
│
├── data/                    # Pre-loaded knowledge base
│   ├── *.txt               # Data engineering documents
│   └── ...
│
├── requirements.txt         # Python dependencies
├── .env                     # API keys (not in git)
├── .env.template           # Template for .env
│
├── README.md               # Main documentation
├── UPLOAD_GUIDE.md         # Upload feature guide
├── SETUP_INSTRUCTIONS.md   # Quick setup
├── ARCHITECTURE.md         # This file
├── CHANGELOG.md            # Version history
│
└── test_upload.py          # Test script
```

---

## 🧩 Key Components

### 1. Frontend Layer (`main.py`)

**Responsibilities:**
- User interface and interaction
- Mode selection (upload vs pre-loaded)
- File upload handling
- Session state management
- Error display and user feedback

**Technologies:**
- Streamlit for UI
- Session state for persistence
- File uploader widget

---

### 2. Processing Layer (`rag_engine.py`)

**Responsibilities:**
- Text extraction from multiple formats
- Document chunking
- Embedding generation
- Vector store management
- QA chain construction

**Key Functions:**

#### `extract_text(file)`
- **Input**: Uploaded file object
- **Process**: Format detection and extraction
- **Output**: Raw text string

#### `process_uploaded_file(file)`
- **Input**: Uploaded file object
- **Process**: Complete pipeline (extract → chunk → embed → store)
- **Output**: ChromaDB vectorstore

#### `load_documents(path)`
- **Input**: Directory path
- **Process**: Load all .txt files
- **Output**: List of document strings

#### `create_vectorstore(docs)`
- **Input**: List of documents
- **Process**: Chunk and embed documents
- **Output**: ChromaDB vectorstore

#### `build_qa_chain(vectorstore)`
- **Input**: Vectorstore
- **Process**: Create LLM + retriever chain
- **Output**: RetrievalQA chain

---

### 3. External Services

#### OpenAI API
- **Purpose**: Embeddings and LLM
- **Usage**:
  - `OpenAIEmbeddings()` - Convert text to vectors
  - `OpenAI(temperature=0.3)` - Generate responses

#### ChromaDB
- **Purpose**: Vector database
- **Usage**:
  - Store embeddings
  - Similarity search
  - Document retrieval

#### LangChain
- **Purpose**: Orchestration framework
- **Usage**:
  - Text splitting
  - Chain construction
  - Prompt management

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```bash
# Required
OPENAI_API_KEY=sk-...

# Optional (for local LLM)
OPENAI_API_BASE=http://localhost:11434/v1
```

### RAG Parameters

```python
# Chunking
chunk_size = 800          # Characters per chunk
chunk_overlap = 100       # Overlap between chunks

# Retrieval
k = 3                     # Number of chunks to retrieve

# LLM
temperature = 0.3         # Creativity level (0-1)
```

---

## 🔐 Security Considerations

1. **API Key Management**
   - Store in `.env` file (not in git)
   - Use environment variables
   - Rotate keys regularly

2. **File Upload Safety**
   - Validate file types
   - Limit file sizes
   - Sanitize file names

3. **Data Privacy**
   - Uploaded files processed in memory
   - Vectors stored locally in ChromaDB
   - API calls to OpenAI (review their privacy policy)

---

## 🚀 Performance Optimization

### Current Implementation
- **Upload Processing**: ~5-10 seconds per document
- **First Query**: ~2-3 seconds
- **Subsequent Queries**: ~1-2 seconds

### Optimization Strategies
1. **Caching**: Store vectorstores for reuse
2. **Batch Processing**: Process multiple documents together
3. **Lazy Loading**: Load embeddings on-demand
4. **Local Embeddings**: Use local models to reduce API calls

---

## 🔮 Future Architecture Enhancements

### Phase 1: Performance
- Vector persistence (save/load)
- Response caching
- Async processing

### Phase 2: Features
- Batch upload
- Metadata filtering
- Cross-encoder re-ranking

### Phase 3: Scale
- API endpoints
- Multi-user support
- Production deployment
- Monitoring and analytics

---

## 📊 Technical Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit | Interactive UI |
| **Backend** | Python 3.8+ | Core logic |
| **Text Processing** | PyPDF2, pandas | Multi-format support |
| **Chunking** | LangChain | Text splitting |
| **Embeddings** | OpenAI API | Vector generation |
| **Vector DB** | ChromaDB | Semantic search |
| **LLM** | OpenAI GPT | Answer generation |
| **Orchestration** | LangChain | RAG pipeline |

---

**Architecture Version:** 2.0  
**Last Updated:** October 21, 2025  
**Built in:** Neuquén, Argentina 🇦🇷

<div align="center">

# 🧠 RAG Demo — Data Engineering Discovery Assistant

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-green?logo=chainlink&logoColor=white)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-orange)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Made in Argentina](https://img.shields.io/badge/Made%20in-Neuqu%C3%A9n%2C%20Argentina%20🇦🇷-blue)](https://github.com/sergioarnold87)

**Un sistema RAG avanzado para descubrir insights ocultos en documentación técnica de Data Engineering**

[Demo](#-demo) • [Instalación](#-setup-instructions) • [Uso](#-discovery-modes) • [Documentación](#-knowledge-base-details)

</div>

---

## 📖 Sobre el Proyecto

Este proyecto fue diseñado en **Neuquén, Argentina 🇦🇷** para demostrar cómo los profesionales de Data Engineering pueden usar **Retrieval-Augmented Generation (RAG)** para desbloquear insights de literatura técnica especializada.

## 🎯 Purpose

The goal is to **reason with knowledge**, not just search it.

By loading key open-source Data Engineering texts, this RAG system connects concepts like:
- **Data Fabric** — Unified data management architectures
- **Observability** — Monitoring data systems health
- **Cost Optimization** — Building efficient pipelines
- **Quality Monitoring** — Ensuring data reliability
- **Analytics Engineering** — Transforming data with software practices
- **Design Patterns** — Proven solutions for data systems

## 🧩 How It Works

### Two Operation Modes:

#### 📤 **Upload Mode** (NEW!)
1. **Upload Document:** Drag & drop any TXT, PDF, CSV, or MD file
2. **Auto-Processing:** Automatic text extraction, chunking, and embedding
3. **Query & Analyze:** Ask questions directly about your uploaded document
4. **Instant Insights:** Get AI-powered analysis in seconds

#### 📚 **Pre-loaded Knowledge Base Mode**
1. **Knowledge Base:** All `.txt` materials from `data/` are split into semantic chunks
2. **Vector Indexing:** ChromaDB creates embeddings and indexes the knowledge
3. **Retrieval:** LangChain retrieves relevant context for your questions
4. **Generation:** OpenAI (or local LLM) synthesizes answers from retrieved context
5. **Interaction:** Streamlit UI provides an interactive exploration interface

## 📁 Project Structure

```
rag-demo-data-engineering/
│
├── data/                                                   # Knowledge base
│   ├── konieczny_data_engineering_design_patterns.txt     # Design patterns
│   ├── leonard_cost_effective_pipelines.txt               # Cost optimization
│   ├── mezzetta_data_fabric.txt                          # Data Fabric architecture
│   ├── stanley_data_quality_monitoring.txt               # Quality monitoring
│   ├── pinto_data_observability.txt                      # Observability practices
│   └── de_wilde_analytics_engineering.txt                # Analytics engineering
│
├── app/                                                   # Application code
│   ├── main.py                                           # Streamlit UI
│   ├── rag_engine.py                                     # RAG core logic
│   └── prompts.py                                        # Discovery prompts
│
├── requirements.txt                                       # Python dependencies
├── README.md                                             # This file
├── .env.template                                         # Environment config template
└── .env                                                  # Your API keys (create this)
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+ installed
- Linux Mint, Ubuntu, or similar OS
- OpenAI API key (or local LLM setup)

### Installation

```bash
# Navigate to the project directory
cd /home/sergio/CascadeProjects/rag-demo-data-engineering

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.template .env
# Edit .env and add your OpenAI API key
nano .env
```

### Configuration

Edit `.env` file:
```bash
# For OpenAI (cloud)
OPENAI_API_KEY=sk-your-actual-api-key-here

# OR for local Ollama
# OPENAI_API_BASE=http://localhost:11434/v1
# OPENAI_API_KEY=ollama
```

## 🎮 Running the Application

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run Streamlit app
streamlit run app/main.py
```

The application will open in your browser at `http://localhost:8501`

## 📤 Upload Mode — Automatic Document Processing

The RAG system now supports **automatic document upload and processing**!

### Supported Formats
- **📄 Text Files:** `.txt`, `.md` (UTF-8 encoding)
- **📕 PDF Documents:** `.pdf` (using PyPDF2)
- **📊 CSV Data:** `.csv` (converted to structured text)

### How to Use Upload Mode

1. **Select Upload Mode** in the sidebar: `📤 Upload Document`
2. **Drag & drop** or click to upload your file
3. **Automatic Processing** happens instantly:
   - Text extraction based on file type
   - Intelligent chunking (800 chars, 100 overlap)
   - Embedding generation with OpenAI
   - Vector store creation with ChromaDB
4. **Ask Questions** about your uploaded document
5. **Get Insights** powered by RAG retrieval

### Example Workflow
```bash
# Upload a PDF whitepaper
→ Drop: "machine_learning_guide.pdf"
→ Wait: 5-10 seconds for processing
→ Query: "What are the main ML algorithms discussed?"
→ Result: Contextual answer extracted from your PDF
```

For detailed upload documentation, see **[UPLOAD_GUIDE.md](UPLOAD_GUIDE.md)**

## 🧠 Discovery Modes

The RAG system offers several exploration modes:

| Mode | Purpose | Example Prompt |
|------|---------|---------------|
| **Explore** | List core concepts | "What are the main principles of Data Fabric?" |
| **Combine** | Fuse frameworks | "Combine observability and data quality frameworks" |
| **Architecture** | Design systems | "Design a hybrid cloud data pipeline using these frameworks" |
| **Weakness** | Critique approaches | "What risks exist in this architecture?" |
| **Insight** | Discover connections | "Find relationships between cost optimization and governance" |

## 💡 Example Interactions

### Discovery Example 1: Combining Concepts
```
Mode: combine
Query: "How can I integrate Data Fabric principles with Observability practices?"

Response: The RAG will retrieve relevant sections from both texts and synthesize
a unified approach combining active metadata monitoring with observability patterns.
```

### Discovery Example 2: Architecture Design
```
Mode: architecture
Query: "Design a cost-effective data pipeline for real-time customer analytics"

Response: Combines cost optimization strategies, design patterns, and analytics
engineering best practices to propose a specific architecture.
```

### Discovery Example 3: Critical Analysis
```
Mode: weakness
Query: "What are the hidden risks in Lambda architecture for data quality?"

Response: Analyzes Lambda architecture through the lens of data quality monitoring,
identifying potential failure points and mitigation strategies.
```

## 🔧 Using Local LLMs (Optional)

### Option 1: Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull mistral

# Update app/rag_engine.py
# Replace: llm = OpenAI(temperature=0.3)
# With:
from langchain.llms import Ollama
llm = Ollama(model="mistral")

# Update .env
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_API_KEY=ollama
```

### Option 2: LM Studio

1. Download and install LM Studio
2. Load a model (e.g., Mistral 7B)
3. Start local server (default: `http://localhost:1234`)
4. Update `.env`:
   ```
   OPENAI_API_BASE=http://localhost:1234/v1
   OPENAI_API_KEY=lm-studio
   ```

## 📊 Knowledge Base Details

The demo includes 6 comprehensive technical documents:

1. **Design Patterns** (Konieczny)
   - Lambda/Kappa architectures
   - Medallion pattern
   - CDC and event sourcing
   - Data partitioning strategies

2. **Cost Optimization** (Leonard)
   - Compute right-sizing
   - Storage tiering
   - Query optimization
   - Network cost reduction

3. **Data Fabric** (Mezzetta)
   - Active metadata
   - Knowledge graphs
   - Data virtualization
   - Unified governance

4. **Quality Monitoring** (Stanley)
   - Quality dimensions
   - Monitoring architecture
   - Great Expectations patterns
   - Remediation workflows

5. **Data Observability** (Pinto)
   - Metrics, logs, traces
   - Golden signals
   - Anomaly detection
   - Incident response

6. **Analytics Engineering** (De Wilde)
   - dbt framework
   - Modeling patterns
   - Testing strategies
   - Development workflows

## 🛠️ Customization

### Adding Your Own Documents

```bash
# Simply add .txt files to the data/ directory
cp your_document.txt data/

# Restart the app - it will automatically load the new content
streamlit run app/main.py
```

### Modifying Discovery Prompts

Edit `app/prompts.py`:
```python
PROMPT_LIBRARY = {
    "your_mode": "Your custom prompt here",
    # ... existing prompts
}
```

### Adjusting RAG Parameters

Edit `app/rag_engine.py`:
```python
# Change chunk size
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Adjust chunk size
    chunk_overlap=200  # Adjust overlap
)

# Change retrieval count
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}  # Retrieve more chunks
)

# Change LLM temperature
llm = OpenAI(temperature=0.5)  # More creative responses
```

## 🧪 Testing the RAG System

Quick validation:
```bash
# Activate environment
source venv/bin/activate

# Test document loading
python -c "from app.rag_engine import load_documents; print(f'Loaded {len(load_documents())} documents')"

# Test vector store creation
python -c "from app.rag_engine import load_documents, create_vectorstore; docs = load_documents(); vs = create_vectorstore(docs); print('Vector store created successfully')"
```

## 📈 Performance Tips

1. **First Run:** Initial embedding creation takes 1-2 minutes
2. **Subsequent Runs:** ChromaDB caches embeddings (much faster)
3. **Large Documents:** Increase chunk_overlap for better context
4. **Slow Responses:** Reduce `k` parameter in retriever
5. **Memory Issues:** Reduce chunk_size or process fewer documents

## 🐛 Troubleshooting

### Issue: "No module named 'app'"
```bash
# Run from project root
cd /home/sergio/CascadeProjects/rag-demo-data-engineering
streamlit run app/main.py
```

### Issue: OpenAI API errors
```bash
# Verify API key is set
cat .env | grep OPENAI_API_KEY

# Test API connection
python -c "import openai; print(openai.Model.list())"
```

### Issue: Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: ChromaDB errors
```bash
# Clear ChromaDB cache
rm -rf chroma_db/

# Restart application
streamlit run app/main.py
```

## 🔒 Security Notes

- **Never commit `.env` file** to version control
- Add `.env` to `.gitignore`
- Use environment-specific API keys
- Rotate keys regularly
- Consider using secret management tools for production

## 📚 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [RAG Best Practices](https://www.anthropic.com/index/retrieval-augmented-generation)

## 🚀 Next Steps

Enhance your RAG system:

### Already Implemented ✅
- [x] Multi-format document upload (TXT, PDF, CSV, MD)
- [x] Automatic text extraction and chunking
- [x] Dual mode operation (upload vs pre-loaded)
- [x] Semantic retrieval with ChromaDB
- [x] Interactive Streamlit UI

### Future Enhancements 🔮
1. **Batch Upload:** Process multiple documents simultaneously
2. **Metadata Extraction:** Track author, date, title for advanced filtering
3. **Cross-Encoder Re-Ranking:** Improve answer relevance
4. **Local LLM Support:** Full Ollama/Llama2 integration
5. **Vector Persistence:** Save and load vectorstores for faster reuse
6. **Chat History:** Enable conversational interactions
7. **Response Caching:** Cache common queries for speed
8. **RAG Evaluation:** Implement evaluation metrics (RAGAS, etc.)
9. **Advanced Chunking:** Semantic chunking based on topics
10. **Export Results:** Download insights as PDF/MD
11. **Deploy to Cloud:** Host on Streamlit Cloud, Hugging Face Spaces, or AWS

## 🤝 Contributing

This is a demo project for learning and experimentation. Feel free to:
- Fork and customize for your needs
- Add new discovery modes
- Improve the UI/UX
- Optimize performance
- Share insights and improvements

## 📝 License

This demo is provided as-is for educational purposes. The knowledge base content is synthetic and created for demonstration.

## 🌟 Acknowledgments

Inspired by modern data engineering practices and the RAG revolution in AI-powered knowledge systems.

Built with:
- 🦜 LangChain - Orchestration framework
- 🎨 Streamlit - Interactive UI
- 🗄️ ChromaDB - Vector database
- 🧠 OpenAI - Language models
- 🐍 Python - The glue holding it all together

---

**Built in Neuquén, Argentina 🇦🇷**  
For data engineers who want to **discover**, not just search.

Happy exploring! 🚀

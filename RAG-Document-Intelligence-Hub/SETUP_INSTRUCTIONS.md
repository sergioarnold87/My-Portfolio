# 🚀 Quick Setup Instructions

## 📋 Prerequisites
- Python 3.8+
- OpenAI API Key

## ⚡ Fast Setup (5 minutes)

```bash
# 1. Navigate to project
cd /home/sergio/CascadeProjects/rag-demo-data-engineering

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API key
cp .env.template .env
nano .env  # Add your OPENAI_API_KEY

# 5. Run the app
streamlit run app/main.py
```

## 🎯 First Steps

### Option 1: Upload Your Own Document
1. Open `http://localhost:8501`
2. Select **"📤 Upload Document"** in sidebar
3. Drag & drop a PDF, TXT, CSV, or MD file
4. Wait for automatic processing (~10 seconds)
5. Ask questions about your document

### Option 2: Use Pre-loaded Knowledge Base
1. Open `http://localhost:8501`
2. Select **"📚 Pre-loaded Knowledge Base"** in sidebar
3. Choose a discovery mode from dropdown
4. Click **"🚀 Run Discovery"**

## 🔍 Validation

Quick test to verify everything works:

```bash
# Activate environment
source venv/bin/activate

# Test imports
python -c "from app.rag_engine import process_uploaded_file; print('✅ Imports OK')"

# Check dependencies
pip list | grep -E "(langchain|openai|streamlit|chromadb|PyPDF2|pandas)"
```

## 📦 What's New?

### Recent Updates:
- ✅ **Multi-format upload:** PDF, CSV, TXT, MD support
- ✅ **Automatic processing:** Zero-config text extraction
- ✅ **Dual mode:** Upload or pre-loaded knowledge base
- ✅ **Better UX:** Cleaner interface with status messages
- ✅ **Error handling:** Graceful failures with helpful messages

## 🐛 Common Issues

### Issue: Missing dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Issue: OpenAI API not configured
```bash
# Check .env file exists and has your key
cat .env
# Should show: OPENAI_API_KEY=sk-...
```

### Issue: Port already in use
```bash
# Use a different port
streamlit run app/main.py --server.port 8502
```

## 📚 Documentation

- **[README.md](README.md)** - Complete project documentation
- **[UPLOAD_GUIDE.md](UPLOAD_GUIDE.md)** - Detailed upload instructions
- **[QUICKSTART.md](QUICKSTART.md)** - Original quickstart guide

## 🎉 You're Ready!

The RAG system is now ready to:
- 📄 Process any document format
- 🧬 Generate embeddings automatically
- 🔍 Perform semantic search
- 🤖 Answer questions with LLM-powered insights

**Happy exploring! 🚀**

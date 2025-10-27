# 🎯 Command Cheatsheet — RAG Demo

Quick reference for common commands.

## 🚀 Initial Setup

```bash
# Navigate to project
cd /home/sergio/CascadeProjects/rag-demo-data-engineering

# Automated setup (recommended)
./setup.sh

# Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.template .env
```

## ▶️ Running the Application

```bash
# Activate virtual environment (always do this first!)
source venv/bin/activate

# Run Streamlit app
streamlit run app/main.py

# Run on different port
streamlit run app/main.py --server.port 8502

# Run with auto-reload on code changes
streamlit run app/main.py --server.runOnSave true
```

## 🧪 Testing & Validation

```bash
# Test document loading
python -c "from app.rag_engine import load_documents; docs = load_documents(); print(f'Loaded {len(docs)} documents')"

# Test vector store creation
python -c "from app.rag_engine import load_documents, create_vectorstore; docs = load_documents(); vs = create_vectorstore(docs); print('Vector store OK')"

# Verify data files
ls -lh data/*.txt | wc -l  # Should show 6

# Check environment variables
cat .env | grep OPENAI_API_KEY
```

## 🔧 Maintenance

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Clear ChromaDB cache (if issues occur)
rm -rf chroma_db/

# Check Python version
python3 --version

# List installed packages
pip list

# Check pip version
pip --version
```

## 🐛 Debugging

```bash
# View Streamlit logs
streamlit run app/main.py --logger.level=debug

# Test OpenAI connection
python -c "import openai; import os; openai.api_key = os.getenv('OPENAI_API_KEY'); print(openai.Model.list())"

# Check if port is in use
lsof -i :8501

# Kill process on port 8501
kill -9 $(lsof -t -i:8501)

# View running Python processes
ps aux | grep python
```

## 📦 Virtual Environment

```bash
# Activate
source venv/bin/activate

# Deactivate
deactivate

# Delete and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📝 Adding Content

```bash
# Add a new document
cp your_document.txt data/

# Count total documents
ls data/*.txt | wc -l

# View file sizes
ls -lh data/*.txt
```

## 🔐 Security

```bash
# Verify .env is ignored by git
git check-ignore .env  # Should output: .env

# Add .env to gitignore if missing
echo ".env" >> .gitignore

# Check what files would be committed
git status
```

## 🌐 Browser Control

```bash
# Open specific browser
streamlit run app/main.py --browser.gatherUsageStats false

# Disable browser auto-open
streamlit run app/main.py --server.headless true

# Access from another machine (use with caution)
streamlit run app/main.py --server.address 0.0.0.0
```

## 📊 Monitoring

```bash
# Watch system resources
htop  # or top

# Check disk usage
du -sh .
du -sh data/
du -sh chroma_db/  # if created

# Monitor network
netstat -tuln | grep 8501
```

## 🧹 Cleanup

```bash
# Remove virtual environment
rm -rf venv/

# Remove ChromaDB cache
rm -rf chroma_db/

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Full cleanup (keeps source files)
rm -rf venv/ chroma_db/ .streamlit/
find . -type d -name "__pycache__" -exec rm -r {} +
```

## 🔄 Git Operations

```bash
# Initialize git (if not already)
git init

# Check status
git status

# Add all files (respects .gitignore)
git add .

# Commit changes
git commit -m "Initial RAG demo setup"

# Create GitHub repo and push
git remote add origin https://github.com/yourusername/rag-demo.git
git branch -M main
git push -u origin main
```

## 🚀 Quick Restart

```bash
# One-liner to restart everything
cd /home/sergio/CascadeProjects/rag-demo-data-engineering && source venv/bin/activate && streamlit run app/main.py
```

## 💡 Useful Aliases

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# Navigate to project
alias cdrag='cd /home/sergio/CascadeProjects/rag-demo-data-engineering'

# Activate environment
alias ragenv='cd /home/sergio/CascadeProjects/rag-demo-data-engineering && source venv/bin/activate'

# Run application
alias ragrun='cd /home/sergio/CascadeProjects/rag-demo-data-engineering && source venv/bin/activate && streamlit run app/main.py'
```

Then reload your shell:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

Now you can use:
```bash
cdrag    # Navigate to project
ragenv   # Activate environment  
ragrun   # Run the app
```

## 📞 Getting Help

```bash
# Streamlit help
streamlit --help

# Run-specific help
streamlit run --help

# Python package info
pip show langchain
pip show chromadb
pip show streamlit
```

## ✨ Pro Tips

```bash
# Check what changed in your code
git diff

# View commit history
git log --oneline

# Create a backup
tar -czf rag-demo-backup-$(date +%Y%m%d).tar.gz .

# Find large files
find . -type f -size +1M -exec ls -lh {} \;

# Count lines of code
find app/ -name "*.py" -exec wc -l {} + | tail -1
```

---

**Quick Start:** `./setup.sh && source venv/bin/activate && streamlit run app/main.py`

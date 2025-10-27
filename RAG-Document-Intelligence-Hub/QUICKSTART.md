# 🚀 Quick Start Guide

Get your RAG demo running in 5 minutes!

## Step 1: Navigate to Project
```bash
cd /home/sergio/CascadeProjects/rag-demo-data-engineering
```

## Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 4: Configure API Key
```bash
# Copy template
cp .env.template .env

# Edit and add your OpenAI API key
nano .env
```

Add this line to `.env`:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Save and exit (Ctrl+X, then Y, then Enter)

## Step 5: Run the App
```bash
streamlit run app/main.py
```

## Step 6: Explore!

The app will open in your browser. Try these queries:

1. **Select "explore" mode** → Click "Run discovery"
2. **Select "combine" mode** → Click "Run discovery"
3. **Type your own question** → "How do I optimize data pipeline costs?"

## 🎯 Expected First Run

- ⏱️ **First startup:** 1-2 minutes (creating embeddings)
- ⚡ **Subsequent startups:** <10 seconds (cached)
- 🔍 **Query response time:** 5-15 seconds

## ⚠️ Troubleshooting

**Error: "No OpenAI API key found"**
```bash
cat .env  # Verify key is set
export OPENAI_API_KEY=sk-your-key  # Set temporarily
```

**Error: "Module not found"**
```bash
pip install -r requirements.txt --force-reinstall
```

**Port already in use**
```bash
streamlit run app/main.py --server.port 8502
```

## 🎊 Success!

You should see:
- Streamlit UI with title "RAG Demo — Data Engineering Discovery Assistant"
- Sidebar with mode selection
- Text area for custom questions
- "Run discovery" button

Now start exploring the knowledge base! 🚀

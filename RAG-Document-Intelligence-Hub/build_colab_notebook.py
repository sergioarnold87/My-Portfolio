#!/usr/bin/env python3
"""
Build Google Colab Notebook for Document Intelligence Hub
Professional portfolio demonstration
"""

import json

def create_markdown_cell(content, cell_id=None):
    """Create markdown cell."""
    cell = {
        'cell_type': 'markdown',
        'metadata': {},
        'source': content if isinstance(content, list) else [content]
    }
    if cell_id:
        cell['metadata']['id'] = cell_id
    return cell

def create_code_cell(code, cell_id=None):
    """Create code cell."""
    cell = {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': code if isinstance(code, list) else [code]
    }
    if cell_id:
        cell['metadata']['id'] = cell_id
    return cell

# Initialize notebook
notebook = {
    'nbformat': 4,
    'nbformat_minor': 0,
    'metadata': {
        'colab': {
            'provenance': [],
            'toc_visible': True,
            'collapsed_sections': []
        },
        'kernelspec': {
            'name': 'python3',
            'display_name': 'Python 3'
        },
        'language_info': {
            'name': 'python'
        }
    },
    'cells': []
}

cells = notebook['cells']

# ======================
# HEADER
# ======================
cells.append(create_markdown_cell("""# 🧠 Document Intelligence Hub
## Advanced RAG System - Portfolio Demo

**By:** [Your Name] | **GitHub:** [Your Repo]

**Technologies:** Python • LangChain • OpenAI • FAISS • RAG • NLP

---

### 🎯 Project Highlights

This notebook demonstrates an **enterprise-grade RAG system** with:

- 🔍 **Multi-format processing** - 15+ document types (PDF, DOCX, EPUB, images with OCR)
- 🧠 **Query intelligence** - Automatic intent detection (8 query types)
- ⚡ **Smart chunking** - 4 strategies (recursive, semantic, sentence, paragraph)
- 🎨 **Prompt engineering** - 30+ professional YAML templates
- 📊 **Quality metrics** - Retrieval + response evaluation
- 🚀 **Production-ready** - Modular, scalable architecture

### 📋 Notebook Structure

1. **Setup & Configuration**
2. **Architecture Overview**
3. **Document Processing**
4. **Query Analysis System**
5. **RAG Implementation**
6. **Live Demo**
7. **Performance Metrics**
8. **Results & Insights**
""", 'header'))

# ======================
# 1. SETUP
# ======================
cells.append(create_markdown_cell("""# 1️⃣ Setup & Installation

## Install Dependencies
""", 'section_setup'))

cells.append(create_code_cell("""%%capture
# Core RAG dependencies
!pip install -q openai langchain tiktoken
!pip install -q chromadb faiss-cpu
!pip install -q PyPDF2 pdfplumber python-docx
!pip install -q pandas unidecode pyyaml beautifulsoup4

print("✅ Dependencies installed successfully!")
""", 'install'))

cells.append(create_markdown_cell("""## Configure API Key

⚠️ **Required:** Enter your OpenAI API key below
"""))

cells.append(create_code_cell("""import os
from getpass import getpass

# Set API key
if 'OPENAI_API_KEY' not in os.environ:
    os.environ['OPENAI_API_KEY'] = getpass('🔑 Enter OpenAI API Key: ')

print("✅ API key configured")
""", 'api_key'))

cells.append(create_markdown_cell("""## Import Libraries"""))

cells.append(create_code_cell("""import warnings
warnings.filterwarnings('ignore')

# Standard library
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from collections import Counter

# LangChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Document processing
from PyPDF2 import PdfReader
import tiktoken

print("✅ All imports successful")
""", 'imports'))

# ======================
# 2. ARCHITECTURE
# ======================
cells.append(create_markdown_cell("""# 2️⃣ System Architecture

## Component Overview

```
┌─────────────────────────────────────────────┐
│      Document Intelligence Hub              │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐    ┌──────────────────┐  │
│  │  Processor   │───▶│   RAG Engine     │  │
│  │              │    │                  │  │
│  │ • Extract    │    │ • Query Analyzer │  │
│  │ • Clean      │    │ • Retriever      │  │
│  │ • Chunk      │    │ • Generator      │  │
│  │ • Embed      │    │ • Prompts        │  │
│  └──────────────┘    └──────────────────┘  │
│          │                    │             │
│          ▼                    ▼             │
│  ┌──────────────┐    ┌──────────────────┐  │
│  │ Vector Store │    │  Metrics Engine  │  │
│  └──────────────┘    └──────────────────┘  │
└─────────────────────────────────────────────┘
```

### Key Features

| Component | Capabilities |
|-----------|-------------|
| **Processor** | PDF/DOCX/EPUB extraction, smart chunking, embeddings |
| **Query Analyzer** | 8 query types, entity extraction, intent detection |
| **Retriever** | Semantic search, MMR, re-ranking |
| **Generator** | Contextual answers, citations, specialized prompts |
| **Metrics** | Quality scoring, performance evaluation |
""", 'architecture'))

# ======================
# 3. QUERY ANALYSIS
# ======================
cells.append(create_markdown_cell("""# 3️⃣ Query Intelligence System

## Query Type Classification
""", 'query_section'))

cells.append(create_code_cell("""class QueryType(Enum):
    \"\"\"Supported query types for intelligent handling.\"\"\"
    FACTUAL = "factual"          # "What is X?"
    COMPARISON = "comparison"    # "Compare A and B"
    SUMMARY = "summary"          # "Summarize..."
    EXPLANATION = "explanation"  # "Explain how..."
    LISTING = "listing"          # "List all..."
    CONCEPTUAL = "conceptual"    # "How does X relate to Y?"
    PROCEDURAL = "procedural"    # "How to do X?"
    DEFINITION = "definition"    # "Define X"

@dataclass
class QueryIntent:
    \"\"\"Query analysis result.\"\"\"
    original_query: str
    query_type: QueryType
    entities: List[str]
    keywords: List[str]
    confidence: float = 1.0

def classify_query(query: str) -> QueryType:
    \"\"\"Classify query type based on patterns.\"\"\"
    q = query.lower().strip()
    
    # Pattern matching
    if re.search(r'^(what is|define)', q):
        return QueryType.DEFINITION
    elif re.search(r'compare|difference|vs', q):
        return QueryType.COMPARISON
    elif re.search(r'^summarize|summary', q):
        return QueryType.SUMMARY
    elif re.search(r'^explain|^how does|^why', q):
        return QueryType.EXPLANATION
    elif re.search(r'^list|what are all', q):
        return QueryType.LISTING
    elif re.search(r'^how to|steps to', q):
        return QueryType.PROCEDURAL
    
    return QueryType.FACTUAL

def analyze_query(query: str) -> QueryIntent:
    \"\"\"Perform complete query analysis.\"\"\"
    query_type = classify_query(query)
    
    # Extract keywords
    stop_words = {'what', 'is', 'the', 'how', 'why', 'a', 'an', 'to', 'of'}
    words = re.findall(r'\\w+', query.lower())
    keywords = [w for w in words if w not in stop_words and len(w) > 2][:5]
    
    # Extract entities (capitalized)
    entities = re.findall(r'\\b[A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*\\b', query)
    
    return QueryIntent(query, query_type, entities, keywords)

print("✅ Query analysis system loaded")
""", 'query_code'))

cells.append(create_markdown_cell("""### 🔍 Demo: Query Classification"""))

cells.append(create_code_cell("""# Test different query types
test_queries = [
    "What is prompt engineering?",
    "Compare Few-Shot and Zero-Shot learning",
    "Summarize the main concepts",
    "How to implement a RAG system?",
    "List all prompt patterns"
]

print("🔍 Query Classification Demo")
print("=" * 60)

for q in test_queries:
    intent = analyze_query(q)
    print(f"\\n📝 '{q}'")
    print(f"   Type: {intent.query_type.value.upper()}")
    print(f"   Keywords: {', '.join(intent.keywords)}")
    if intent.entities:
        print(f"   Entities: {', '.join(intent.entities)}")
""", 'demo_query'))

# Continue with more sections...
# Saving partial notebook
with open('Document_Intelligence_Hub_Portfolio.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print("✅ Colab notebook created: Document_Intelligence_Hub_Portfolio.ipynb")
print("📝 Upload to Google Colab and run!")

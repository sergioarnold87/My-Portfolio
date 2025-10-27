import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import pandas as pd

load_dotenv()

def load_documents(path="data/"):
    """Load all .txt files from the data directory."""
    docs = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                docs.append(f.read())
    return docs

def create_vectorstore(docs):
    """Split documents into chunks and create a vector store."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = []
    for doc in docs:
        chunks.extend(splitter.split_text(doc))
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(chunks, embedding=embeddings)
    return vectorstore

def build_qa_chain(vectorstore):
    """Build the QA chain with retriever."""
    llm = OpenAI(temperature=0.3)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever
    )
    return qa_chain


# ========== Automatic File Processing Functions ==========

def extract_text(file):
    """
    Extract text from uploaded file based on extension.
    Supports: .txt, .md, .pdf, .csv
    """
    ext = file.name.split('.')[-1].lower()
    text = ""
    
    if ext in ['txt', 'md']:
        text = file.read().decode('utf-8')
    elif ext == 'pdf':
        reader = PdfReader(file)
        text = "\n".join([
            page.extract_text() for page in reader.pages 
            if page.extract_text()
        ])
    elif ext == 'csv':
        df = pd.read_csv(file)
        # Convert CSV to text representation
        text = df.to_string(index=False)
    
    return text


def process_uploaded_file(file):
    """
    Complete automatic pipeline:
    1. Extract text from file
    2. Chunk text
    3. Create embeddings
    4. Build vectorstore
    Returns vectorstore ready for retrieval
    """
    # 1. Extract text
    text = extract_text(file)
    
    # 2. Chunking (automatic)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, 
        chunk_overlap=100
    )
    chunks = splitter.split_text(text)
    
    # 3. Embeddings & Vectorstore creation (automatic)
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(chunks, embedding=embeddings)
    
    return vectorstore

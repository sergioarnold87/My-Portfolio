"""
RAG Engine V2 - Advanced Architecture
Unified interface integrating all new modules.
"""

import os
from typing import Dict, List, Optional, Union
from pathlib import Path
from dotenv import load_dotenv

# Import new modules
from processor import (
    detect_document_format,
    extract_text_from_document,
    clean_and_normalize_text,
    create_smart_chunks,
    create_vectorstore
)
from rag import (
    analyze_query,
    classify_query_type,
    AdvancedRetriever,
    ContextualGenerator
)
from utils import (
    calculate_retrieval_metrics,
    evaluate_response_quality
)
from prompts import get_system_prompt, get_query_template

load_dotenv()


class DocumentIntelligenceHub:
    """
    Advanced RAG system with full document processing pipeline.
    """
    
    def __init__(
        self,
        embedding_model: str = 'text-embedding-3-small',
        llm_model: str = 'gpt-3.5-turbo',
        chunk_size: int = 800,
        chunk_overlap: int = 100,
        chunking_strategy: str = 'recursive'
    ):
        """
        Initialize Document Intelligence Hub.
        
        Args:
            embedding_model: OpenAI embedding model
            llm_model: OpenAI LLM model
            chunk_size: Target chunk size in characters
            chunk_overlap: Overlap between chunks
            chunking_strategy: 'recursive', 'semantic', 'sentence', 'paragraph'
        """
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.chunking_strategy = chunking_strategy
        
        # Components (initialized on demand)
        self.vectorstore = None
        self.retriever = None
        self.generator = None
        
        # Metadata
        self.document_metadata = {}
        self.processing_stats = {}
    
    def process_document(
        self,
        file_source: Union[str, Path, 'BytesIO'],
        filename: Optional[str] = None,
        clean_text: bool = True,
        use_ocr: bool = False
    ) -> Dict:
        """
        Process document through complete pipeline.
        
        Args:
            file_source: File path or file object
            filename: Original filename (required for file objects)
            clean_text: Apply text cleaning
            use_ocr: Enable OCR for images/scanned PDFs
            
        Returns:
            Dictionary with processing results and stats
        """
        
        print("🔍 Step 1: Detecting format...")
        doc_format = detect_document_format(file_source, filename)
        print(f"   Format: {doc_format.extension} ({doc_format.category})")
        
        print("📄 Step 2: Extracting text...")
        extraction_result = extract_text_from_document(
            file_source,
            filename,
            use_ocr=use_ocr
        )
        print(f"   Extracted: {extraction_result.char_count} chars, {extraction_result.word_count} words")
        
        raw_text = extraction_result.text
        
        if clean_text:
            print("🧹 Step 3: Cleaning text...")
            cleaned_text = clean_and_normalize_text(raw_text)
            print(f"   Cleaned: {len(cleaned_text)} chars")
        else:
            cleaned_text = raw_text
        
        print("✂️ Step 4: Chunking text...")
        chunks = create_smart_chunks(
            cleaned_text,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            strategy=self.chunking_strategy,
            metadata={
                'format': doc_format.extension,
                'source': filename or 'uploaded'
            }
        )
        print(f"   Created: {len(chunks)} chunks")
        
        print("🧬 Step 5: Creating embeddings and vectorstore...")
        self.vectorstore = create_vectorstore(
            chunks,
            backend='chroma',
            model=self.embedding_model
        )
        print(f"   Vectorstore created with {len(chunks)} vectors")
        
        # Initialize retriever and generator
        self.retriever = AdvancedRetriever(
            self.vectorstore,
            default_k=5,
            use_reranking=True
        )
        
        self.generator = ContextualGenerator(
            model_name=self.llm_model,
            temperature=0.3
        )
        
        # Store metadata
        self.document_metadata = {
            'format': doc_format.extension,
            'category': doc_format.category,
            'filename': filename,
            'char_count': extraction_result.char_count,
            'word_count': extraction_result.word_count,
            'chunk_count': len(chunks),
            'extraction_metadata': extraction_result.metadata
        }
        
        self.processing_stats = {
            'chunks_created': len(chunks),
            'avg_chunk_size': sum(len(c.text) for c in chunks) // len(chunks),
            'embedding_model': self.embedding_model
        }
        
        print("✅ Document processing complete!\n")
        
        return {
            'status': 'success',
            'document_metadata': self.document_metadata,
            'processing_stats': self.processing_stats
        }
    
    def query(
        self,
        question: str,
        k: Optional[int] = None,
        analyze_intent: bool = True,
        include_metrics: bool = False
    ) -> Dict:
        """
        Query the document with intelligent retrieval and generation.
        
        Args:
            question: User question
            k: Number of chunks to retrieve (uses default if None)
            analyze_intent: Analyze query intent for better retrieval
            include_metrics: Include quality metrics in response
            
        Returns:
            Dictionary with answer, sources, and optional metrics
        """
        
        if not self.vectorstore or not self.retriever or not self.generator:
            return {
                'error': 'No document processed. Call process_document() first.',
                'answer': None
            }
        
        # Analyze query intent
        query_intent = None
        if analyze_intent:
            query_intent = analyze_query(question, expand=False)
        
        # Retrieve relevant chunks
        retrieved_docs = self.retriever.retrieve(
            question,
            k=k,
            query_intent=query_intent
        )
        
        if not retrieved_docs:
            return {
                'answer': "I couldn't find relevant information to answer your question.",
                'sources': [],
                'confidence': 0.0
            }
        
        # Generate answer
        result = self.generator.generate(
            question,
            retrieved_docs,
            query_intent=query_intent,
            include_citations=True
        )
        
        # Add metrics if requested
        if include_metrics:
            # Retrieval metrics
            retrieval_metrics = calculate_retrieval_metrics(
                [{'score': doc.score} for doc in retrieved_docs]
            )
            
            # Response quality metrics
            context = '\n\n'.join([doc.text for doc in retrieved_docs])
            response_metrics = evaluate_response_quality(
                result['answer'],
                context,
                question
            )
            
            result['metrics'] = {
                'retrieval': retrieval_metrics,
                'response': response_metrics,
                'query_intent': {
                    'type': query_intent.query_type.value if query_intent else 'unknown',
                    'entities': query_intent.entities if query_intent else [],
                    'keywords': query_intent.keywords if query_intent else []
                }
            }
        
        return result
    
    def get_document_info(self) -> Dict:
        """Get information about the processed document."""
        return {
            'metadata': self.document_metadata,
            'stats': self.processing_stats,
            'ready': self.vectorstore is not None
        }


# ========== Backward Compatibility Functions ==========

def process_uploaded_file(uploaded_file) -> 'VectorStore':
    """
    Backward compatible function for existing app.
    Processes uploaded file and returns vectorstore.
    """
    hub = DocumentIntelligenceHub()
    hub.process_document(uploaded_file, filename=uploaded_file.name)
    return hub.vectorstore


def load_documents(path: str = "data/") -> List[str]:
    """
    Load documents from directory (backward compatible).
    """
    docs = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                docs.append(f.read())
    return docs


def create_vectorstore_from_docs(docs: List[str]) -> 'VectorStore':
    """
    Create vectorstore from list of documents (backward compatible).
    """
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import Chroma
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = []
    for doc in docs:
        chunks.extend(splitter.split_text(doc))
    
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts(chunks, embedding=embeddings)
    
    return vectorstore


def build_qa_chain(vectorstore) -> 'RetrievalQA':
    """
    Build QA chain (backward compatible).
    """
    from langchain.llms import OpenAI
    from langchain.chains import RetrievalQA
    
    llm = OpenAI(temperature=0.3)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever
    )
    return qa_chain


# ========== Convenience Function ==========

def quick_process_and_query(file_path: str, question: str) -> Dict:
    """
    Quick function to process a document and ask a question.
    
    Args:
        file_path: Path to document file
        question: Question to ask
        
    Returns:
        Answer dictionary
    """
    hub = DocumentIntelligenceHub()
    hub.process_document(file_path)
    return hub.query(question, include_metrics=True)

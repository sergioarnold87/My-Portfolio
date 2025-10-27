"""
Embeddings and Vector Store Management Module
Advanced embedding generation and vector database operations.
"""

from typing import List, Optional, Dict
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma, FAISS
from .chunker import Chunk
import os


class EmbeddingManager:
    """Manage embeddings generation and vector store operations."""
    
    def __init__(
        self,
        model: str = 'text-embedding-3-small',
        backend: str = 'chroma'
    ):
        """
        Initialize embedding manager.
        
        Args:
            model: OpenAI embedding model name
                  - 'text-embedding-3-small' (1536 dims, fast, cheap)
                  - 'text-embedding-3-large' (3072 dims, better quality)
                  - 'text-embedding-ada-002' (legacy, 1536 dims)
            backend: Vector store backend ('chroma', 'faiss')
        """
        self.model = model
        self.backend = backend
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(model=model)
        
    def embed_chunks(self, chunks: List[Chunk]) -> List[float]:
        """
        Generate embeddings for chunks.
        
        Args:
            chunks: List of Chunk objects
            
        Returns:
            List of embedding vectors
        """
        texts = [chunk.text for chunk in chunks]
        return self.embeddings.embed_documents(texts)
    
    def create_vectorstore(
        self,
        chunks: List[Chunk],
        persist_directory: Optional[str] = None
    ):
        """
        Create vector store from chunks.
        
        Args:
            chunks: List of Chunk objects
            persist_directory: Directory to persist vectorstore (optional)
            
        Returns:
            Vector store instance
        """
        
        # Extract texts and metadata
        texts = [chunk.text for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        
        # Add chunk IDs to metadata
        for i, metadata in enumerate(metadatas):
            metadata['chunk_id'] = chunks[i].chunk_id
            metadata['chunk_size'] = len(chunks[i].text)
            metadata['token_count'] = chunks[i].token_count
        
        if self.backend == 'chroma':
            return self._create_chroma_store(texts, metadatas, persist_directory)
        elif self.backend == 'faiss':
            return self._create_faiss_store(texts, metadatas, persist_directory)
        else:
            raise ValueError(f"Unknown backend: {self.backend}")
    
    def _create_chroma_store(
        self,
        texts: List[str],
        metadatas: List[Dict],
        persist_directory: Optional[str]
    ):
        """Create ChromaDB vector store."""
        
        if persist_directory:
            vectorstore = Chroma.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas,
                persist_directory=persist_directory
            )
            vectorstore.persist()
        else:
            vectorstore = Chroma.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas
            )
        
        return vectorstore
    
    def _create_faiss_store(
        self,
        texts: List[str],
        metadatas: List[Dict],
        persist_directory: Optional[str]
    ):
        """Create FAISS vector store."""
        
        vectorstore = FAISS.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas
        )
        
        if persist_directory:
            os.makedirs(persist_directory, exist_ok=True)
            vectorstore.save_local(persist_directory)
        
        return vectorstore
    
    @staticmethod
    def load_vectorstore(
        persist_directory: str,
        backend: str = 'chroma',
        embeddings = None
    ):
        """
        Load existing vector store from disk.
        
        Args:
            persist_directory: Directory containing saved vectorstore
            backend: Vector store backend ('chroma', 'faiss')
            embeddings: Embeddings instance (required for loading)
            
        Returns:
            Loaded vector store
        """
        
        if embeddings is None:
            embeddings = OpenAIEmbeddings()
        
        if backend == 'chroma':
            return Chroma(
                persist_directory=persist_directory,
                embedding_function=embeddings
            )
        elif backend == 'faiss':
            return FAISS.load_local(
                persist_directory,
                embeddings
            )
        else:
            raise ValueError(f"Unknown backend: {backend}")


# ========== Convenience Functions ==========

def generate_embeddings(
    chunks: List[Chunk],
    model: str = 'text-embedding-3-small'
) -> List[float]:
    """
    Generate embeddings for chunks.
    
    Args:
        chunks: List of Chunk objects
        model: OpenAI embedding model
        
    Returns:
        List of embedding vectors
    """
    manager = EmbeddingManager(model=model)
    return manager.embed_chunks(chunks)


def create_vectorstore(
    chunks: List[Chunk],
    backend: str = 'chroma',
    model: str = 'text-embedding-3-small',
    persist_directory: Optional[str] = None
):
    """
    Create vector store from chunks.
    
    Args:
        chunks: List of Chunk objects
        backend: Vector store backend ('chroma', 'faiss')
        model: OpenAI embedding model
        persist_directory: Directory to persist vectorstore
        
    Returns:
        Vector store instance
    """
    manager = EmbeddingManager(model=model, backend=backend)
    return manager.create_vectorstore(chunks, persist_directory)


def create_vectorstore_from_texts(
    texts: List[str],
    metadatas: Optional[List[Dict]] = None,
    backend: str = 'chroma',
    model: str = 'text-embedding-3-small',
    persist_directory: Optional[str] = None
):
    """
    Create vector store directly from texts (backward compatibility).
    
    Args:
        texts: List of text strings
        metadatas: Optional list of metadata dicts
        backend: Vector store backend
        model: OpenAI embedding model
        persist_directory: Directory to persist vectorstore
        
    Returns:
        Vector store instance
    """
    
    embeddings = OpenAIEmbeddings(model=model)
    
    if backend == 'chroma':
        if persist_directory:
            vectorstore = Chroma.from_texts(
                texts=texts,
                embedding=embeddings,
                metadatas=metadatas,
                persist_directory=persist_directory
            )
            vectorstore.persist()
        else:
            vectorstore = Chroma.from_texts(
                texts=texts,
                embedding=embeddings,
                metadatas=metadatas
            )
    elif backend == 'faiss':
        vectorstore = FAISS.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas
        )
        if persist_directory:
            os.makedirs(persist_directory, exist_ok=True)
            vectorstore.save_local(persist_directory)
    else:
        raise ValueError(f"Unknown backend: {backend}")
    
    return vectorstore


def estimate_embedding_cost(
    total_tokens: int,
    model: str = 'text-embedding-3-small'
) -> float:
    """
    Estimate cost of embedding generation.
    
    Args:
        total_tokens: Total number of tokens to embed
        model: Embedding model name
        
    Returns:
        Estimated cost in USD
    """
    
    # Pricing per 1M tokens (as of 2024)
    pricing = {
        'text-embedding-3-small': 0.02,  # $0.02 / 1M tokens
        'text-embedding-3-large': 0.13,  # $0.13 / 1M tokens
        'text-embedding-ada-002': 0.10   # $0.10 / 1M tokens
    }
    
    price_per_million = pricing.get(model, 0.10)
    cost = (total_tokens / 1_000_000) * price_per_million
    
    return round(cost, 4)

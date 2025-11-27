""
Vector store implementation using ChromaDB for document storage and retrieval.
"""
import os
import uuid
from typing import List, Dict, Any, Optional, Tuple
import chromadb
from chromadb.config import Settings
from chromadb.api.types import EmbeddingFunction
from sentence_transformers import SentenceTransformer
import numpy as np

from .config import settings, logger
from .models import Document, DocumentChunk, SearchResult, SearchQuery, SearchResponse

class LocalEmbeddingFunction(EmbeddingFunction):
    """Local embedding function using SentenceTransformers."""
    
    def __init__(self, model_name: str = settings.EMBEDDING_MODEL):
        self.model = SentenceTransformer(model_name)
        logger.info(f"Initialized embedding model: {model_name}")
    
    def __call__(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        if not texts:
            return []
        return self.model.encode(texts, show_progress_bar=False).tolist()

class VectorStore:
    """Vector store for document storage and retrieval using ChromaDB."""
    
    def __init__(self, collection_name: str = "documents"):
        """Initialize the vector store."""
        self.collection_name = collection_name
        self.embedding_function = LocalEmbeddingFunction()
        self.client = self._get_chroma_client()
        self.collection = self._get_or_create_collection()
    
    def _get_chroma_client(self) -> chromadb.Client:
        """Create and configure the ChromaDB client."""
        client_settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=settings.CHROMA_DB_PATH,
            anonymized_telemetry=False
        )
        return chromadb.Client(client_settings)
    
    def _get_or_create_collection(self):
        """Get an existing collection or create a new one."""
        try:
            # Try to get an existing collection
            collection = self.client.get_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
            logger.info(f"Loaded existing collection: {self.collection_name}")
            return collection
        except ValueError:
            # Create a new collection if it doesn't exist
            collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}  # Optimize for cosine similarity
            )
            logger.info(f"Created new collection: {self.collection_name}")
            return collection
    
    def add_document(self, document: Document) -> str:
        """Add a document to the vector store."""
        if not document.chunks:
            raise ValueError("Document has no chunks to add")
        
        # Prepare data for ChromaDB
        ids = []
        documents = []
        metadatas = []
        
        for chunk in document.chunks:
            chunk_id = str(uuid.uuid4())
            ids.append(chunk_id)
            documents.append(chunk.content)
            
            # Prepare metadata
            metadata = chunk.metadata.copy()
            metadata.update({
                "document_id": document.id,
                "chunk_index": chunk.chunk_index,
                "document_type": document.metadata.document_type.value,
                "source": document.metadata.source,
                "tags": ",".join(document.metadata.tags) if document.metadata.tags else "",
            })
            metadatas.append(metadata)
        
        # Add to ChromaDB
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        
        # Persist changes
        self.client.persist()
        
        logger.info(f"Added document {document.id} with {len(document.chunks)} chunks")
        return document.id
    
    def search(self, query: SearchQuery) -> SearchResponse:
        """Search for documents similar to the query."""
        # Convert filters to ChromaDB format
        where = {}
        if query.filters:
            for key, value in query.filters.items():
                if isinstance(value, list):
                    where[key] = {"$in": value}
                else:
                    where[key] = value
        
        # Execute the query
        results = self.collection.query(
            query_texts=[query.query],
            n_results=query.limit,
            where=where or None,
            include=["documents", "metadatas", "distances"]
        )
        
        # Process results
        search_results = []
        for i in range(len(results["ids"][0])):
            doc_id = results["ids"][0][i]
            content = results["documents"][0][i]
            metadata = results["metadatas"][0][i]
            score = 1.0 - results["distances"][0][i]  # Convert distance to similarity score
            
            if score < query.min_score:
                continue
                
            search_results.append(SearchResult(
                id=doc_id,
                document_id=metadata.get("document_id", ""),
                content=content,
                metadata=metadata,
                score=score,
                chunk_index=metadata.get("chunk_index", 0)
            ))
        
        return SearchResponse(
            results=search_results,
            total=len(search_results),
            query=query.query
        )
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document and all its chunks from the vector store."""
        try:
            # Find all chunks for this document
            results = self.collection.get(where={"document_id": document_id})
            if not results["ids"]:
                return False
                
            # Delete the chunks
            self.collection.delete(ids=results["ids"])
            self.client.persist()
            
            logger.info(f"Deleted document {document_id} with {len(results['ids'])} chunks")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {str(e)}")
            return False
    
    def get_document_chunks(self, document_id: str) -> List[Dict[str, Any]]:
        """Get all chunks for a document."""
        results = self.collection.get(where={"document_id": document_id})
        return [
            {
                "id": doc_id,
                "content": doc,
                "metadata": meta,
                "embedding": emb
            }
            for doc_id, doc, meta, emb in zip(
                results["ids"],
                results["documents"],
                results["metadatas"],
                results["embeddings"]
            )
        ]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "embedding_dimension": len(self.embedding_function(["sample"])[0]) if count > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error getting vector store stats: {str(e)}")
            return {"error": str(e)}

# Global instance
vector_store = VectorStore()

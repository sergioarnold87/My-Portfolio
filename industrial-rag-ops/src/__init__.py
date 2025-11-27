""
Industrial RAG Ops - A system for processing and retrieving industrial documents.
"""
__version__ = "1.0.0"

# Import key components for easier access
from .config import settings, logger
from .models import Document, DocumentType, DocumentStatus, SearchQuery
from .vector_store import vector_store
from .processing import document_processor

__all__ = [
    'settings',
    'logger',
    'Document',
    'DocumentType',
    'DocumentStatus',
    'SearchQuery',
    'vector_store',
    'document_processor'
]

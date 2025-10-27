"""
Document Processing Module
Handles format detection, text extraction, cleaning, chunking, and embeddings.
"""

from .detect_format import detect_document_format
from .extract_text import extract_text_from_document
from .clean_text import clean_and_normalize_text
from .chunker import create_smart_chunks
from .embeddings import generate_embeddings, create_vectorstore

__all__ = [
    'detect_document_format',
    'extract_text_from_document',
    'clean_and_normalize_text',
    'create_smart_chunks',
    'generate_embeddings',
    'create_vectorstore'
]

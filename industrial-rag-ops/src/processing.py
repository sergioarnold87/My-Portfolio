"""Document processing pipeline for PII masking and logical chunking."""
import re
import uuid
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import logging
import spacy
import numpy as np
from pathlib import Path

from .config import settings, logger
from .models import Document, DocumentChunk, DocumentMetadata, DocumentType, DocumentStatus

# Load the Spanish language model for NLP processing
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    logger.warning("Spanish language model not found. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "es_core_news_sm"])
    nlp = spacy.load("es_core_news_sm")

class PIIDetector:
    """Detect and mask Personally Identifiable Information (PII) in text."""
    
    def __init__(self):
        # Regular expressions for common PII patterns
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b(\+\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b',
            'dni': r'\b\d{7,8}\b',  # Argentine DNI
            'cuil': r'\b\d{2}-\d{8}-\d\b',  # Argentine CUIL/CUIT
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        }
        
        # Compile all patterns for faster matching
        self.compiled_patterns = {name: re.compile(pattern) for name, pattern in self.patterns.items()}
    
    def detect_pii(self, text: str) -> List[Dict[str, Any]]:
        """Detect PII in the given text."""
        pii_entities = []
        
        # Check for each PII type
        for pii_type, pattern in self.compiled_patterns.items():
            for match in pattern.finditer(text):
                pii_entities.append({
                    'type': pii_type,
                    'value': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'replacement': self._get_replacement(pii_type, match.group())
                })
        
        # Sort by start position (ascending)
        pii_entities.sort(key=lambda x: x['start'])
        
        return pii_entities
    
    def mask_pii(self, text: str, pii_entities: List[Dict[str, Any]] = None) -> Tuple[str, List[Dict[str, Any]]]:
        """Mask PII in the given text."""
        if pii_entities is None:
            pii_entities = self.detect_pii(text)
        
        # Sort entities by start position in reverse order to avoid offset issues
        pii_entities_sorted = sorted(pii_entities, key=lambda x: x['start'], reverse=True)
        
        masked_text = text
        for entity in pii_entities_sorted:
            masked_text = (
                masked_text[:entity['start']] + 
                entity['replacement'] + 
                masked_text[entity['end']:]
            )
        
        return masked_text, pii_entities
    
    def _get_replacement(self, pii_type: str, value: str) -> str:
        """Get a masked replacement for the PII value."""
        if pii_type == 'email':
            user, domain = value.split('@')
            return f"{user[0]}***@{domain}"
        elif pii_type == 'phone':
            return "[PHONE]"
        elif pii_type == 'dni':
            return "[DNI]"
        elif pii_type == 'cuil':
            return "[CUIL]"
        elif pii_type == 'credit_card':
            return "[CREDIT_CARD]"
        elif pii_type == 'ip_address':
            return "[IP_ADDRESS]"
        return "[PII]"

class DocumentChunker:
    """Chunk documents into logical sections for better retrieval."""
    
    def __init__(self, max_chunk_size: int = 1000, overlap: int = 100):
        """Initialize the chunker.
        
        Args:
            max_chunk_size: Maximum number of characters per chunk
            overlap: Number of characters to overlap between chunks
        """
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
    
    def chunk_document(self, document: Document) -> Document:
        """Chunk a document into logical sections."""
        if not document.content:
            raise ValueError("Document content is empty")
        
        # Process the document with spaCy for better chunking
        doc = nlp(document.content)
        
        # Split into sentences first
        sentences = [sent.text for sent in doc.sents]
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # If adding this sentence would exceed the max chunk size, finalize the current chunk
            if current_length + sentence_length > self.max_chunk_size and current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append(chunk_text)
                
                # Start a new chunk with overlap from the previous one
                overlap_start = max(0, len(chunk_text) - self.overlap)
                current_chunk = [chunk_text[overlap_start:]]
                current_length = len(current_chunk[0])
            
            current_chunk.append(sentence)
            current_length += sentence_length + 1  # +1 for the space
        
        # Add the last chunk if not empty
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        # Create DocumentChunk objects
        document.chunks = [
            DocumentChunk(
                id=str(uuid.uuid4()),
                document_id=document.id,
                content=chunk,
                metadata={
                    "chunk_index": i,
                    "chunk_total": len(chunks),
                    "document_type": document.metadata.document_type.value,
                    "source": document.metadata.source,
                },
                chunk_index=i
            )
            for i, chunk in enumerate(chunks)
        ]
        
        return document

class DocumentProcessor:
    """Process documents through the pipeline: PII masking and chunking."""
    
    def __init__(self):
        self.pii_detector = PIIDetector()
        self.chunker = DocumentChunker()
    
    def process_document(self, document: Document) -> Document:
        """Process a document through the pipeline."""
        try:
            # 1. Mask PII
            masked_content, pii_entities = self.pii_detector.mask_pii(document.content)
            document.content = masked_content
            
            # 2. Chunk the document
            document = self.chunker.chunk_document(document)
            
            # 3. Update status
            document.status = DocumentStatus.PROCESSED
            
            logger.info(f"Processed document {document.id} with {len(document.chunks)} chunks")
            
        except Exception as e:
            document.status = DocumentStatus.ERROR
            document.processing_errors.append(str(e))
            logger.error(f"Error processing document {document.id}: {str(e)}")
        
        return document

# Global instance
document_processor = DocumentProcessor()

"""
Smart Chunking Module
Advanced text chunking strategies with semantic awareness.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter


@dataclass
class Chunk:
    """Container for a text chunk with metadata."""
    text: str
    start_idx: int
    end_idx: int
    chunk_id: int
    metadata: Dict
    token_count: Optional[int] = None
    
    def __post_init__(self):
        if self.token_count is None:
            self.token_count = estimate_tokens(self.text)


class SmartChunker:
    """Advanced chunking with multiple strategies."""
    
    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
        strategy: str = 'recursive',
        model: str = 'gpt-3.5-turbo'
    ):
        """
        Initialize chunker.
        
        Args:
            chunk_size: Target size in characters
            chunk_overlap: Overlap between chunks
            strategy: 'recursive', 'semantic', 'sentence', 'paragraph'
            model: Model name for token counting
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.strategy = strategy
        self.model = model
        
        # Initialize tokenizer
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def chunk(self, text: str, metadata: Optional[Dict] = None) -> List[Chunk]:
        """
        Chunk text using selected strategy.
        
        Args:
            text: Input text to chunk
            metadata: Base metadata to attach to all chunks
            
        Returns:
            List of Chunk objects
        """
        
        if not text or not text.strip():
            return []
        
        metadata = metadata or {}
        
        if self.strategy == 'recursive':
            return self._chunk_recursive(text, metadata)
        elif self.strategy == 'semantic':
            return self._chunk_semantic(text, metadata)
        elif self.strategy == 'sentence':
            return self._chunk_by_sentence(text, metadata)
        elif self.strategy == 'paragraph':
            return self._chunk_by_paragraph(text, metadata)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")
    
    def _chunk_recursive(self, text: str, base_metadata: Dict) -> List[Chunk]:
        """Recursive character-based chunking (LangChain)."""
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        raw_chunks = splitter.split_text(text)
        
        chunks = []
        current_idx = 0
        
        for i, chunk_text in enumerate(raw_chunks):
            start = text.find(chunk_text, current_idx)
            end = start + len(chunk_text)
            
            chunk = Chunk(
                text=chunk_text,
                start_idx=start,
                end_idx=end,
                chunk_id=i,
                metadata={
                    **base_metadata,
                    'chunking_strategy': 'recursive',
                    'total_chunks': len(raw_chunks)
                }
            )
            chunks.append(chunk)
            current_idx = end
        
        return chunks
    
    def _chunk_semantic(self, text: str, base_metadata: Dict) -> List[Chunk]:
        """Semantic chunking based on content structure."""
        
        # Split by double newlines (paragraphs)
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = []
        current_size = 0
        chunk_id = 0
        start_idx = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            para_size = len(para)
            
            # If adding this paragraph exceeds chunk size, save current chunk
            if current_size + para_size > self.chunk_size and current_chunk:
                chunk_text = '\n\n'.join(current_chunk)
                end_idx = start_idx + len(chunk_text)
                
                chunks.append(Chunk(
                    text=chunk_text,
                    start_idx=start_idx,
                    end_idx=end_idx,
                    chunk_id=chunk_id,
                    metadata={
                        **base_metadata,
                        'chunking_strategy': 'semantic',
                        'paragraph_count': len(current_chunk)
                    }
                ))
                
                # Start new chunk with overlap
                if self.chunk_overlap > 0 and current_chunk:
                    # Include last paragraph for context
                    current_chunk = [current_chunk[-1], para]
                    current_size = len(current_chunk[-2]) + para_size
                else:
                    current_chunk = [para]
                    current_size = para_size
                
                start_idx = end_idx - (len(current_chunk[-2]) if len(current_chunk) > 1 else 0)
                chunk_id += 1
            else:
                current_chunk.append(para)
                current_size += para_size
        
        # Save final chunk
        if current_chunk:
            chunk_text = '\n\n'.join(current_chunk)
            end_idx = start_idx + len(chunk_text)
            
            chunks.append(Chunk(
                text=chunk_text,
                start_idx=start_idx,
                end_idx=end_idx,
                chunk_id=chunk_id,
                metadata={
                    **base_metadata,
                    'chunking_strategy': 'semantic',
                    'paragraph_count': len(current_chunk)
                }
            ))
        
        return chunks
    
    def _chunk_by_sentence(self, text: str, base_metadata: Dict) -> List[Chunk]:
        """Chunk by sentences (simple implementation)."""
        
        # Simple sentence splitting (can be improved with NLTK/spaCy)
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        chunk_id = 0
        start_idx = 0
        
        for sent in sentences:
            sent = sent.strip()
            sent_size = len(sent)
            
            if current_size + sent_size > self.chunk_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                end_idx = start_idx + len(chunk_text)
                
                chunks.append(Chunk(
                    text=chunk_text,
                    start_idx=start_idx,
                    end_idx=end_idx,
                    chunk_id=chunk_id,
                    metadata={
                        **base_metadata,
                        'chunking_strategy': 'sentence',
                        'sentence_count': len(current_chunk)
                    }
                ))
                
                current_chunk = [sent]
                current_size = sent_size
                start_idx = end_idx
                chunk_id += 1
            else:
                current_chunk.append(sent)
                current_size += sent_size
        
        # Save final chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append(Chunk(
                text=chunk_text,
                start_idx=start_idx,
                end_idx=start_idx + len(chunk_text),
                chunk_id=chunk_id,
                metadata={
                    **base_metadata,
                    'chunking_strategy': 'sentence',
                    'sentence_count': len(current_chunk)
                }
            ))
        
        return chunks
    
    def _chunk_by_paragraph(self, text: str, base_metadata: Dict) -> List[Chunk]:
        """Chunk by paragraphs (preserve natural boundaries)."""
        
        paragraphs = text.split('\n\n')
        
        chunks = []
        start_idx = 0
        
        for i, para in enumerate(paragraphs):
            para = para.strip()
            if not para:
                continue
            
            chunks.append(Chunk(
                text=para,
                start_idx=start_idx,
                end_idx=start_idx + len(para),
                chunk_id=i,
                metadata={
                    **base_metadata,
                    'chunking_strategy': 'paragraph',
                    'is_single_paragraph': True
                }
            ))
            
            start_idx += len(para) + 2  # Account for \n\n
        
        return chunks


def create_smart_chunks(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 100,
    strategy: str = 'recursive',
    metadata: Optional[Dict] = None
) -> List[Chunk]:
    """
    Create smart chunks from text.
    
    Args:
        text: Input text
        chunk_size: Target chunk size in characters
        chunk_overlap: Overlap between chunks
        strategy: Chunking strategy ('recursive', 'semantic', 'sentence', 'paragraph')
        metadata: Base metadata for chunks
        
    Returns:
        List of Chunk objects
    """
    
    chunker = SmartChunker(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        strategy=strategy
    )
    
    return chunker.chunk(text, metadata)


def estimate_tokens(text: str, model: str = 'gpt-3.5-turbo') -> int:
    """
    Estimate token count for text.
    
    Args:
        text: Input text
        model: Model name for tokenizer
        
    Returns:
        Estimated token count
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))


def optimize_chunk_size(
    text: str,
    target_chunks: int,
    min_overlap: int = 50
) -> tuple:
    """
    Calculate optimal chunk size and overlap for target number of chunks.
    
    Args:
        text: Input text
        target_chunks: Desired number of chunks
        min_overlap: Minimum overlap size
        
    Returns:
        Tuple of (chunk_size, chunk_overlap)
    """
    
    text_length = len(text)
    
    # Calculate chunk size to achieve target chunks
    chunk_size = text_length // target_chunks
    
    # Ensure minimum chunk size
    chunk_size = max(chunk_size, 200)
    
    # Calculate overlap (10-15% of chunk size)
    chunk_overlap = max(min_overlap, int(chunk_size * 0.12))
    
    return chunk_size, chunk_overlap

"""
Intelligent Document Format Detection
Detects document type and provides format-specific metadata
"""

import magic
import os
from pathlib import Path
from typing import Dict, Optional


class DocumentFormat:
    """Document format information"""
    def __init__(self, extension: str, mime_type: str, category: str):
        self.extension = extension
        self.mime_type = mime_type
        self.category = category  # 'text', 'document', 'spreadsheet', 'presentation', 'ebook', 'image'
        
    def __repr__(self):
        return f"DocumentFormat(ext={self.extension}, mime={self.mime_type}, category={self.category})"


# Format mappings
FORMAT_CATEGORIES = {
    'text': ['.txt', '.md', '.markdown', '.rst', '.log', '.json', '.xml', '.yaml', '.yml'],
    'document': ['.pdf', '.doc', '.docx', '.odt', '.rtf'],
    'spreadsheet': ['.csv', '.xls', '.xlsx', '.ods'],
    'presentation': ['.ppt', '.pptx', '.odp'],
    'ebook': ['.epub', '.mobi', '.azw', '.azw3'],
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
}


def detect_document_format(file_path: Optional[str] = None, file_name: Optional[str] = None, 
                          file_content: Optional[bytes] = None) -> DocumentFormat:
    """
    Detect document format from file path, name, or content
    
    Args:
        file_path: Path to the file
        file_name: Name of the file (for uploaded files)
        file_content: Binary content of the file
    
    Returns:
        DocumentFormat object with detected information
    """
    
    # Try to detect from extension first
    if file_path:
        ext = Path(file_path).suffix.lower()
        file_name = os.path.basename(file_path)
    elif file_name:
        ext = Path(file_name).suffix.lower()
    else:
        ext = None
    
    # Determine category from extension
    category = 'unknown'
    if ext:
        for cat, extensions in FORMAT_CATEGORIES.items():
            if ext in extensions:
                category = cat
                break
    
    # Try to detect MIME type from content using python-magic
    mime_type = 'application/octet-stream'
    if file_content:
        try:
            mime_type = magic.from_buffer(file_content, mime=True)
        except:
            pass
    elif file_path and os.path.exists(file_path):
        try:
            mime_type = magic.from_file(file_path, mime=True)
        except:
            pass
    
    return DocumentFormat(
        extension=ext or 'unknown',
        mime_type=mime_type,
        category=category
    )


def is_text_extractable(format_info: DocumentFormat) -> bool:
    """Check if text can be extracted from this format"""
    extractable_categories = ['text', 'document', 'spreadsheet', 'ebook']
    return format_info.category in extractable_categories


def requires_ocr(format_info: DocumentFormat) -> bool:
    """Check if format might require OCR (scanned PDFs, images)"""
    return format_info.category == 'image'


def get_recommended_chunking_strategy(format_info: DocumentFormat) -> str:
    """
    Get recommended chunking strategy based on document format
    
    Returns:
        'semantic', 'fixed', 'paragraph', or 'structural'
    """
    strategy_map = {
        'text': 'paragraph',
        'document': 'semantic',
        'spreadsheet': 'structural',
        'ebook': 'semantic',
        'presentation': 'structural'
    }
    return strategy_map.get(format_info.category, 'fixed')

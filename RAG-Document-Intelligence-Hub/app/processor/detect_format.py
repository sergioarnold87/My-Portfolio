"""
Document Format Detection Module
Intelligent detection of document types and characteristics.
"""

import os
import magic
from typing import Dict, Optional
from pathlib import Path


class DocumentFormat:
    """Document format information container."""
    
    def __init__(self, extension: str, mime_type: str, category: str):
        self.extension = extension.lower()
        self.mime_type = mime_type
        self.category = category  # text, pdf, spreadsheet, presentation, ebook, image
        
    def __repr__(self):
        return f"DocumentFormat(ext={self.extension}, category={self.category})"


# Format mappings
FORMAT_CATEGORIES = {
    # Text formats
    'txt': 'text',
    'md': 'text',
    'markdown': 'text',
    'rst': 'text',
    'log': 'text',
    
    # PDF
    'pdf': 'pdf',
    
    # Spreadsheets
    'csv': 'spreadsheet',
    'xlsx': 'spreadsheet',
    'xls': 'spreadsheet',
    'tsv': 'spreadsheet',
    
    # Documents
    'docx': 'document',
    'doc': 'document',
    'odt': 'document',
    
    # Presentations
    'pptx': 'presentation',
    'ppt': 'presentation',
    
    # Ebooks
    'epub': 'ebook',
    'mobi': 'ebook',
    
    # Images (for OCR)
    'png': 'image',
    'jpg': 'image',
    'jpeg': 'image',
    'tiff': 'image',
    'bmp': 'image'
}


def detect_document_format(file_path_or_obj, filename: Optional[str] = None) -> DocumentFormat:
    """
    Detect document format from file path or file object.
    
    Args:
        file_path_or_obj: File path string or file-like object
        filename: Original filename (required if file_path_or_obj is file object)
        
    Returns:
        DocumentFormat object with detected information
        
    Raises:
        ValueError: If format cannot be detected or is not supported
    """
    
    # Extract extension
    if isinstance(file_path_or_obj, (str, Path)):
        ext = os.path.splitext(str(file_path_or_obj))[1][1:].lower()
        file_path = str(file_path_or_obj)
    elif hasattr(file_path_or_obj, 'name'):
        ext = file_path_or_obj.name.split('.')[-1].lower()
        file_path = None
    elif filename:
        ext = filename.split('.')[-1].lower()
        file_path = None
    else:
        raise ValueError("Cannot determine file extension. Provide filename parameter.")
    
    # Check if extension is supported
    if ext not in FORMAT_CATEGORIES:
        raise ValueError(
            f"Unsupported format: .{ext}. "
            f"Supported formats: {', '.join(sorted(FORMAT_CATEGORIES.keys()))}"
        )
    
    category = FORMAT_CATEGORIES[ext]
    
    # Try to detect MIME type using python-magic (optional)
    mime_type = f"application/{ext}"
    try:
        if file_path and os.path.exists(file_path):
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(file_path)
    except (ImportError, Exception):
        # python-magic not available or failed, use fallback
        pass
    
    return DocumentFormat(
        extension=ext,
        mime_type=mime_type,
        category=category
    )


def get_supported_formats() -> Dict[str, list]:
    """
    Get dictionary of supported formats by category.
    
    Returns:
        Dictionary mapping categories to list of extensions
    """
    result = {}
    for ext, category in FORMAT_CATEGORIES.items():
        if category not in result:
            result[category] = []
        result[category].append(ext)
    return result


def is_format_supported(extension: str) -> bool:
    """
    Check if a file format is supported.
    
    Args:
        extension: File extension (with or without leading dot)
        
    Returns:
        True if supported, False otherwise
    """
    ext = extension.lstrip('.').lower()
    return ext in FORMAT_CATEGORIES


def get_extraction_complexity(doc_format: DocumentFormat) -> str:
    """
    Estimate extraction complexity for a document format.
    
    Args:
        doc_format: DocumentFormat object
        
    Returns:
        Complexity level: 'simple', 'medium', 'complex'
    """
    complexity_map = {
        'text': 'simple',
        'spreadsheet': 'simple',
        'pdf': 'medium',
        'document': 'medium',
        'ebook': 'medium',
        'presentation': 'complex',
        'image': 'complex'  # Requires OCR
    }
    return complexity_map.get(doc_format.category, 'medium')

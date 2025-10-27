"""
Text Cleaning and Normalization Module
Advanced text preprocessing for better RAG performance.
"""

import re
from typing import Optional, List
from unidecode import unidecode


class TextCleaner:
    """Advanced text cleaning with configurable options."""
    
    def __init__(
        self,
        remove_urls: bool = True,
        remove_emails: bool = True,
        remove_phone_numbers: bool = False,
        normalize_whitespace: bool = True,
        remove_special_chars: bool = False,
        preserve_structure: bool = True,
        min_line_length: int = 10
    ):
        self.remove_urls = remove_urls
        self.remove_emails = remove_emails
        self.remove_phone_numbers = remove_phone_numbers
        self.normalize_whitespace = normalize_whitespace
        self.remove_special_chars = remove_special_chars
        self.preserve_structure = preserve_structure
        self.min_line_length = min_line_length
        
    def clean(self, text: str) -> str:
        """Apply all cleaning operations."""
        
        if not text or not text.strip():
            return ""
        
        # Remove common PDF artifacts
        text = self._remove_pdf_artifacts(text)
        
        # Remove headers/footers patterns
        text = self._remove_headers_footers(text)
        
        # Remove URLs
        if self.remove_urls:
            text = self._remove_urls(text)
        
        # Remove emails
        if self.remove_emails:
            text = self._remove_emails(text)
        
        # Remove phone numbers
        if self.remove_phone_numbers:
            text = self._remove_phone_numbers(text)
        
        # Normalize whitespace
        if self.normalize_whitespace:
            text = self._normalize_whitespace(text)
        
        # Remove very short lines (likely artifacts)
        if self.min_line_length > 0:
            text = self._remove_short_lines(text, self.min_line_length)
        
        # Remove special characters (optional)
        if self.remove_special_chars:
            text = self._remove_special_characters(text)
        
        return text.strip()
    
    def _remove_pdf_artifacts(self, text: str) -> str:
        """Remove common PDF extraction artifacts."""
        
        # Remove page numbers (various formats)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
        
        # Remove excessive dots/dashes (table of contents artifacts)
        text = re.sub(r'\.{4,}', ' ', text)
        text = re.sub(r'-{4,}', ' ', text)
        
        # Remove form feed characters
        text = text.replace('\f', '\n')
        
        return text
    
    def _remove_headers_footers(self, text: str) -> str:
        """Remove repetitive headers and footers."""
        
        lines = text.split('\n')
        
        if len(lines) < 10:
            return text
        
        # Find repetitive lines (simple heuristic)
        line_counts = {}
        for line in lines:
            clean_line = line.strip()
            if len(clean_line) > 5:  # Ignore very short lines
                line_counts[clean_line] = line_counts.get(clean_line, 0) + 1
        
        # Remove lines that appear too frequently (likely headers/footers)
        threshold = max(3, len(lines) // 20)  # Adaptive threshold
        frequent_lines = {line for line, count in line_counts.items() if count >= threshold}
        
        filtered_lines = [
            line for line in lines 
            if line.strip() not in frequent_lines or len(line.strip()) > 50
        ]
        
        return '\n'.join(filtered_lines)
    
    def _remove_urls(self, text: str) -> str:
        """Remove URLs from text."""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(url_pattern, '', text)
    
    def _remove_emails(self, text: str) -> str:
        """Remove email addresses."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.sub(email_pattern, '', text)
    
    def _remove_phone_numbers(self, text: str) -> str:
        """Remove phone numbers (various formats)."""
        patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # US format
            r'\b\(\d{3}\)\s*\d{3}[-.]?\d{4}\b',  # (XXX) XXX-XXXX
            r'\+\d{1,3}\s?\d{1,14}\b'  # International
        ]
        for pattern in patterns:
            text = re.sub(pattern, '', text)
        return text
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace while preserving structure."""
        
        if self.preserve_structure:
            # Replace multiple spaces with single space
            text = re.sub(r' +', ' ', text)
            # Replace multiple newlines with max 2 newlines
            text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        else:
            # Aggressive: collapse all whitespace
            text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def _remove_short_lines(self, text: str, min_length: int) -> str:
        """Remove lines shorter than minimum length."""
        
        lines = text.split('\n')
        filtered = [
            line for line in lines 
            if len(line.strip()) >= min_length or line.strip() == ''
        ]
        return '\n'.join(filtered)
    
    def _remove_special_characters(self, text: str) -> str:
        """Remove special characters (keep alphanumeric and basic punctuation)."""
        # Keep: letters, numbers, spaces, basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s.,;:!?\'"\-\(\)\[\]]', '', text)
        return text


def clean_and_normalize_text(
    text: str,
    aggressive: bool = False,
    preserve_structure: bool = True
) -> str:
    """
    Clean and normalize text with sensible defaults.
    
    Args:
        text: Input text to clean
        aggressive: Use aggressive cleaning (removes more)
        preserve_structure: Keep paragraph breaks and structure
        
    Returns:
        Cleaned text string
    """
    
    cleaner = TextCleaner(
        remove_urls=True,
        remove_emails=True,
        remove_phone_numbers=aggressive,
        normalize_whitespace=True,
        remove_special_chars=aggressive,
        preserve_structure=preserve_structure,
        min_line_length=10 if not aggressive else 20
    )
    
    return cleaner.clean(text)


def normalize_unicode(text: str) -> str:
    """
    Normalize unicode characters to ASCII equivalents.
    
    Args:
        text: Input text with unicode characters
        
    Returns:
        ASCII-normalized text
    """
    return unidecode(text)


def extract_sections(text: str) -> List[dict]:
    """
    Extract sections from structured text (chapters, headings, etc.)
    
    Args:
        text: Input text with section markers
        
    Returns:
        List of dictionaries with section info: {'title': str, 'content': str, 'level': int}
    """
    
    sections = []
    lines = text.split('\n')
    
    current_section = None
    current_content = []
    
    # Patterns for common section markers
    heading_patterns = [
        (r'^#+\s+(.+)$', 'markdown'),  # Markdown: ## Heading
        (r'^([A-Z][A-Za-z\s]+)$', 'caps'),  # All caps or title case alone
        (r'^\d+\.\s+(.+)$', 'numbered'),  # 1. Section
        (r'^Chapter\s+\d+[:\s]+(.+)$', 'chapter')  # Chapter 1: Title
    ]
    
    for line in lines:
        is_heading = False
        
        for pattern, htype in heading_patterns:
            match = re.match(pattern, line.strip())
            if match:
                # Save previous section
                if current_section:
                    sections.append({
                        'title': current_section,
                        'content': '\n'.join(current_content).strip(),
                        'type': htype
                    })
                
                # Start new section
                current_section = match.group(1) if match.groups() else line.strip()
                current_content = []
                is_heading = True
                break
        
        if not is_heading and line.strip():
            current_content.append(line)
    
    # Save last section
    if current_section:
        sections.append({
            'title': current_section,
            'content': '\n'.join(current_content).strip(),
            'type': 'final'
        })
    
    return sections

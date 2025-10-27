"""
Language Tools Module
Language detection, text normalization, and NLP utilities.
"""

import re
from typing import List, Optional
from collections import Counter


def detect_language(text: str) -> str:
    """
    Detect language of text (simple heuristic-based).
    
    Args:
        text: Input text
        
    Returns:
        Language code ('en', 'es', 'unknown')
    """
    
    # Simple language detection based on common words
    spanish_indicators = [
        'el', 'la', 'los', 'las', 'un', 'una', 'de', 'del', 'que', 'es',
        'en', 'por', 'para', 'con', 'como', 'pero', 'más', 'también'
    ]
    
    english_indicators = [
        'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'can', 'could', 'should', 'may', 'might', 'must'
    ]
    
    words = text.lower().split()
    word_set = set(words[:100])  # Check first 100 words
    
    spanish_matches = sum(1 for w in spanish_indicators if w in word_set)
    english_matches = sum(1 for w in english_indicators if w in word_set)
    
    if spanish_matches > english_matches:
        return 'es'
    elif english_matches > spanish_matches:
        return 'en'
    else:
        return 'unknown'


def normalize_text(text: str, lowercase: bool = True) -> str:
    """
    Normalize text for comparison and processing.
    
    Args:
        text: Input text
        lowercase: Convert to lowercase
        
    Returns:
        Normalized text
    """
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Lowercase if requested
    if lowercase:
        text = text.lower()
    
    return text


def extract_key_phrases(text: str, top_n: int = 10) -> List[str]:
    """
    Extract key phrases from text (simple frequency-based).
    
    Args:
        text: Input text
        top_n: Number of top phrases to return
        
    Returns:
        List of key phrases
    """
    
    # Extract 2-3 word phrases
    words = text.lower().split()
    
    # Stop words to filter
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this',
        'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
    }
    
    # Extract bigrams and trigrams
    phrases = []
    
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i+1]}"
        if words[i] not in stop_words and words[i+1] not in stop_words:
            phrases.append(bigram)
    
    for i in range(len(words) - 2):
        trigram = f"{words[i]} {words[i+1]} {words[i+2]}"
        if all(w not in stop_words for w in [words[i], words[i+1], words[i+2]]):
            phrases.append(trigram)
    
    # Count and return top phrases
    phrase_counts = Counter(phrases)
    return [phrase for phrase, count in phrase_counts.most_common(top_n)]


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences (simple rule-based).
    
    Args:
        text: Input text
        
    Returns:
        List of sentences
    """
    
    # Simple sentence splitting
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def count_syllables(word: str) -> int:
    """
    Estimate syllable count for readability metrics.
    
    Args:
        word: Input word
        
    Returns:
        Estimated syllable count
    """
    
    word = word.lower()
    vowels = "aeiouy"
    syllable_count = 0
    previous_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllable_count += 1
        previous_was_vowel = is_vowel
    
    # Adjust for silent 'e'
    if word.endswith('e'):
        syllable_count -= 1
    
    # Ensure at least one syllable
    if syllable_count == 0:
        syllable_count = 1
    
    return syllable_count


def calculate_readability(text: str) -> dict:
    """
    Calculate readability metrics (Flesch Reading Ease approximation).
    
    Args:
        text: Input text
        
    Returns:
        Dictionary with readability metrics
    """
    
    sentences = split_into_sentences(text)
    words = text.split()
    
    if not sentences or not words:
        return {
            'flesch_score': 0,
            'grade_level': 'N/A',
            'difficulty': 'N/A'
        }
    
    # Count syllables
    total_syllables = sum(count_syllables(word) for word in words)
    
    # Flesch Reading Ease Score
    # Formula: 206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
    avg_sentence_length = len(words) / len(sentences)
    avg_syllables_per_word = total_syllables / len(words)
    
    flesch_score = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
    flesch_score = max(0, min(100, flesch_score))  # Clamp between 0-100
    
    # Determine difficulty level
    if flesch_score >= 90:
        difficulty = 'Very Easy'
        grade = '5th grade'
    elif flesch_score >= 80:
        difficulty = 'Easy'
        grade = '6th grade'
    elif flesch_score >= 70:
        difficulty = 'Fairly Easy'
        grade = '7th grade'
    elif flesch_score >= 60:
        difficulty = 'Standard'
        grade = '8-9th grade'
    elif flesch_score >= 50:
        difficulty = 'Fairly Difficult'
        grade = '10-12th grade'
    elif flesch_score >= 30:
        difficulty = 'Difficult'
        grade = 'College'
    else:
        difficulty = 'Very Difficult'
        grade = 'College Graduate'
    
    return {
        'flesch_score': round(flesch_score, 1),
        'grade_level': grade,
        'difficulty': difficulty,
        'avg_sentence_length': round(avg_sentence_length, 1),
        'avg_syllables_per_word': round(avg_syllables_per_word, 2)
    }


def highlight_keywords(text: str, keywords: List[str], marker: str = '**') -> str:
    """
    Highlight keywords in text (for Markdown rendering).
    
    Args:
        text: Input text
        keywords: Keywords to highlight
        marker: Markdown marker (default: '**' for bold)
        
    Returns:
        Text with highlighted keywords
    """
    
    highlighted = text
    
    for keyword in keywords:
        # Case-insensitive replacement
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        highlighted = pattern.sub(f'{marker}\\g<0>{marker}', highlighted)
    
    return highlighted


def truncate_text(
    text: str,
    max_length: int = 500,
    ellipsis: str = '...'
) -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Input text
        max_length: Maximum length in characters
        ellipsis: String to append when truncated
        
    Returns:
        Truncated text
    """
    
    if len(text) <= max_length:
        return text
    
    # Try to truncate at sentence boundary
    truncated = text[:max_length]
    last_period = truncated.rfind('.')
    last_space = truncated.rfind(' ')
    
    if last_period > max_length * 0.8:
        return text[:last_period + 1] + ' ' + ellipsis
    elif last_space > max_length * 0.8:
        return text[:last_space] + ellipsis
    else:
        return text[:max_length] + ellipsis


def extract_abbreviations(text: str) -> dict:
    """
    Extract abbreviations and their full forms from text.
    
    Args:
        text: Input text
        
    Returns:
        Dictionary mapping abbreviations to possible full forms
    """
    
    # Pattern: Full Form (Abbreviation)
    pattern = r'([A-Z][a-zA-Z\s]+)\s+\(([A-Z]{2,})\)'
    matches = re.findall(pattern, text)
    
    abbreviations = {}
    for full_form, abbr in matches:
        abbreviations[abbr] = full_form.strip()
    
    return abbreviations


def clean_markdown(text: str) -> str:
    """
    Remove Markdown formatting from text.
    
    Args:
        text: Text with Markdown
        
    Returns:
        Plain text
    """
    
    # Remove headers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    
    # Remove bold/italic
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    
    # Remove links
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    
    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`(.+?)`', r'\1', text)
    
    return text


def estimate_reading_time(text: str, words_per_minute: int = 200) -> dict:
    """
    Estimate reading time for text.
    
    Args:
        text: Input text
        words_per_minute: Average reading speed
        
    Returns:
        Dictionary with time estimates
    """
    
    word_count = len(text.split())
    minutes = word_count / words_per_minute
    
    return {
        'word_count': word_count,
        'estimated_minutes': round(minutes, 1),
        'display_time': f"{int(minutes)} min" if minutes >= 1 else f"{int(minutes * 60)} sec"
    }

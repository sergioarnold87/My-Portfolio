"""
Query Analysis Module
Intelligent query understanding and classification for better retrieval.
"""

import re
from typing import Dict, List, Optional
from enum import Enum


class QueryType(Enum):
    """Types of queries for tailored handling."""
    FACTUAL = "factual"              # "What is X?"
    COMPARISON = "comparison"        # "Compare A and B"
    SUMMARY = "summary"              # "Summarize..."
    EXPLANATION = "explanation"      # "Explain how..."
    LISTING = "listing"              # "List all..."
    CONCEPTUAL = "conceptual"        # "How does X relate to Y?"
    PROCEDURAL = "procedural"        # "How to do X?"
    DEFINITION = "definition"        # "Define X"


class QueryIntent:
    """Container for query analysis results."""
    
    def __init__(
        self,
        original_query: str,
        query_type: QueryType,
        entities: List[str],
        keywords: List[str],
        expanded_query: Optional[str] = None,
        confidence: float = 1.0
    ):
        self.original_query = original_query
        self.query_type = query_type
        self.entities = entities
        self.keywords = keywords
        self.expanded_query = expanded_query or original_query
        self.confidence = confidence
    
    def __repr__(self):
        return f"QueryIntent(type={self.query_type.value}, entities={self.entities})"


def classify_query_type(query: str) -> QueryType:
    """
    Classify the type of query based on patterns.
    
    Args:
        query: User query string
        
    Returns:
        QueryType enum value
    """
    
    query_lower = query.lower().strip()
    
    # Pattern matching for query types
    patterns = {
        QueryType.DEFINITION: [
            r'^what is ',
            r'^what are ',
            r'^define ',
            r'^definition of '
        ],
        QueryType.COMPARISON: [
            r'compare ',
            r'difference between ',
            r'versus',
            r' vs ',
            r'similar to',
            r'contrast '
        ],
        QueryType.SUMMARY: [
            r'^summarize ',
            r'^summary of ',
            r'give me a summary',
            r'overview of '
        ],
        QueryType.EXPLANATION: [
            r'^explain ',
            r'^how does ',
            r'^why does ',
            r'how come',
            r'reasoning behind'
        ],
        QueryType.LISTING: [
            r'^list ',
            r'^enumerate ',
            r'what are all ',
            r'show me all ',
            r'give me all '
        ],
        QueryType.PROCEDURAL: [
            r'^how to ',
            r'^how do i ',
            r'^steps to ',
            r'procedure for ',
            r'process of '
        ],
        QueryType.CONCEPTUAL: [
            r'relationship between',
            r'how .* relate',
            r'connection between',
            r'impact of .* on'
        ]
    }
    
    # Check patterns
    for qtype, pattern_list in patterns.items():
        for pattern in pattern_list:
            if re.search(pattern, query_lower):
                return qtype
    
    # Default: factual query
    return QueryType.FACTUAL


def extract_entities(query: str) -> List[str]:
    """
    Extract potential entities/topics from query.
    
    Args:
        query: User query string
        
    Returns:
        List of extracted entities
    """
    
    entities = []
    
    # Remove common question words
    stop_words = {
        'what', 'is', 'are', 'the', 'how', 'why', 'when', 'where', 'who',
        'does', 'do', 'did', 'can', 'could', 'would', 'should', 'a', 'an',
        'compare', 'explain', 'define', 'summarize', 'list', 'tell', 'me',
        'about', 'between', 'of', 'in', 'on', 'to', 'for', 'with'
    }
    
    # Extract words (simple approach)
    words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b|\b[a-z]+\b', query)
    
    for word in words:
        word_lower = word.lower()
        if word_lower not in stop_words and len(word) > 2:
            entities.append(word)
    
    # Look for quoted phrases
    quoted = re.findall(r'"([^"]+)"', query)
    entities.extend(quoted)
    
    return list(set(entities))  # Remove duplicates


def extract_keywords(query: str) -> List[str]:
    """
    Extract important keywords from query.
    
    Args:
        query: User query string
        
    Returns:
        List of keywords
    """
    
    # Remove punctuation and convert to lowercase
    query_clean = re.sub(r'[^\w\s]', ' ', query.lower())
    
    # Stop words to filter out
    stop_words = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
        'to', 'was', 'will', 'with', 'what', 'when', 'where', 'who', 'why',
        'how', 'can', 'could', 'would', 'should', 'me', 'you', 'this', 'these'
    }
    
    words = query_clean.split()
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    return keywords


def expand_query(query: str, query_type: QueryType) -> str:
    """
    Expand query with additional context for better retrieval.
    
    Args:
        query: Original query
        query_type: Classified query type
        
    Returns:
        Expanded query string
    """
    
    expansions = {
        QueryType.DEFINITION: f"{query} What is the meaning and explanation?",
        QueryType.COMPARISON: f"{query} What are the similarities and differences?",
        QueryType.SUMMARY: f"{query} Provide key points and main concepts.",
        QueryType.EXPLANATION: f"{query} Include details, reasons, and examples.",
        QueryType.LISTING: f"{query} Include all relevant items and categories.",
        QueryType.PROCEDURAL: f"{query} Include steps, methods, and best practices.",
        QueryType.CONCEPTUAL: f"{query} Include relationships, connections, and implications."
    }
    
    return expansions.get(query_type, query)


def analyze_query(query: str, expand: bool = False) -> QueryIntent:
    """
    Perform full query analysis.
    
    Args:
        query: User query string
        expand: Whether to expand the query
        
    Returns:
        QueryIntent object with analysis results
    """
    
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    
    # Classify query type
    query_type = classify_query_type(query)
    
    # Extract entities and keywords
    entities = extract_entities(query)
    keywords = extract_keywords(query)
    
    # Expand query if requested
    expanded = expand_query(query, query_type) if expand else query
    
    # Calculate confidence (simple heuristic)
    confidence = 1.0 if entities or len(keywords) > 2 else 0.7
    
    return QueryIntent(
        original_query=query,
        query_type=query_type,
        entities=entities,
        keywords=keywords,
        expanded_query=expanded,
        confidence=confidence
    )


def suggest_retrieval_strategy(query_intent: QueryIntent) -> Dict:
    """
    Suggest retrieval parameters based on query analysis.
    
    Args:
        query_intent: Analyzed query intent
        
    Returns:
        Dictionary with suggested retrieval parameters
    """
    
    strategies = {
        QueryType.FACTUAL: {
            'k': 3,
            'search_type': 'similarity',
            'score_threshold': 0.7
        },
        QueryType.COMPARISON: {
            'k': 6,  # Need more context for comparison
            'search_type': 'mmr',  # Maximum Marginal Relevance for diversity
            'score_threshold': 0.6
        },
        QueryType.SUMMARY: {
            'k': 8,  # Gather broad context
            'search_type': 'similarity',
            'score_threshold': 0.65
        },
        QueryType.EXPLANATION: {
            'k': 5,
            'search_type': 'similarity',
            'score_threshold': 0.7
        },
        QueryType.LISTING: {
            'k': 10,  # Comprehensive retrieval
            'search_type': 'mmr',
            'score_threshold': 0.5
        },
        QueryType.PROCEDURAL: {
            'k': 5,
            'search_type': 'similarity',
            'score_threshold': 0.75  # Need high relevance for procedures
        },
        QueryType.CONCEPTUAL: {
            'k': 6,
            'search_type': 'mmr',
            'score_threshold': 0.6
        },
        QueryType.DEFINITION: {
            'k': 2,  # Precise definition needed
            'search_type': 'similarity',
            'score_threshold': 0.8
        }
    }
    
    return strategies.get(query_intent.query_type, strategies[QueryType.FACTUAL])

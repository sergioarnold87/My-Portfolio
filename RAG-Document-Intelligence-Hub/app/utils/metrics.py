"""
Metrics and Evaluation Module
Quality metrics for RAG system performance.
"""

from typing import List, Dict, Optional
import re
from collections import Counter


def calculate_retrieval_metrics(
    retrieved_docs: List[Dict],
    min_score_threshold: float = 0.7
) -> Dict:
    """
    Calculate metrics for retrieval quality.
    
    Args:
        retrieved_docs: List of retrieved documents with scores
        min_score_threshold: Minimum acceptable score
        
    Returns:
        Dictionary with retrieval metrics
    """
    
    if not retrieved_docs:
        return {
            'num_results': 0,
            'avg_score': 0.0,
            'min_score': 0.0,
            'max_score': 0.0,
            'above_threshold': 0,
            'quality_grade': 'F'
        }
    
    scores = [doc.get('score', 0.0) for doc in retrieved_docs]
    
    avg_score = sum(scores) / len(scores)
    min_score = min(scores)
    max_score = max(scores)
    above_threshold = sum(1 for s in scores if s >= min_score_threshold)
    
    # Quality grade
    if avg_score >= 0.85:
        grade = 'A'
    elif avg_score >= 0.75:
        grade = 'B'
    elif avg_score >= 0.65:
        grade = 'C'
    elif avg_score >= 0.5:
        grade = 'D'
    else:
        grade = 'F'
    
    return {
        'num_results': len(retrieved_docs),
        'avg_score': round(avg_score, 3),
        'min_score': round(min_score, 3),
        'max_score': round(max_score, 3),
        'above_threshold': above_threshold,
        'quality_grade': grade,
        'score_distribution': {
            'excellent': sum(1 for s in scores if s >= 0.85),
            'good': sum(1 for s in scores if 0.7 <= s < 0.85),
            'fair': sum(1 for s in scores if 0.5 <= s < 0.7),
            'poor': sum(1 for s in scores if s < 0.5)
        }
    }


def evaluate_response_quality(
    answer: str,
    retrieved_context: str,
    query: str
) -> Dict:
    """
    Evaluate quality of generated response.
    
    Args:
        answer: Generated answer
        retrieved_context: Context used for generation
        query: Original query
        
    Returns:
        Dictionary with quality metrics
    """
    
    metrics = {}
    
    # 1. Length metrics
    metrics['answer_length'] = len(answer)
    metrics['word_count'] = len(answer.split())
    metrics['sentence_count'] = len(re.split(r'[.!?]+', answer))
    
    # 2. Completeness (answer length vs context)
    if retrieved_context:
        metrics['context_utilization'] = min(1.0, len(answer) / len(retrieved_context))
    else:
        metrics['context_utilization'] = 0.0
    
    # 3. Relevance to query
    query_terms = set(query.lower().split())
    answer_terms = set(answer.lower().split())
    overlap = len(query_terms & answer_terms)
    metrics['query_term_coverage'] = overlap / len(query_terms) if query_terms else 0.0
    
    # 4. Information density
    unique_words = len(set(answer.lower().split()))
    total_words = len(answer.split())
    metrics['lexical_diversity'] = unique_words / total_words if total_words > 0 else 0.0
    
    # 5. Check for hedging/uncertainty phrases
    uncertainty_phrases = [
        "i don't know", "not sure", "cannot answer", "unclear",
        "no information", "doesn't say", "not mentioned"
    ]
    metrics['has_uncertainty'] = any(phrase in answer.lower() for phrase in uncertainty_phrases)
    
    # 6. Check for citations (if present)
    citation_pattern = r'\[(?:Source|Chunk|Page)\s+\d+\]'
    citations = re.findall(citation_pattern, answer)
    metrics['citation_count'] = len(citations)
    metrics['has_citations'] = len(citations) > 0
    
    # 7. Overall quality score
    quality_score = (
        min(metrics['word_count'] / 50, 1.0) * 0.3 +  # Length appropriateness
        metrics['context_utilization'] * 0.2 +         # Context usage
        metrics['query_term_coverage'] * 0.2 +         # Relevance
        metrics['lexical_diversity'] * 0.2 +           # Information density
        (0 if metrics['has_uncertainty'] else 0.1)     # Confidence
    )
    
    metrics['quality_score'] = round(quality_score, 3)
    
    # Quality grade
    if quality_score >= 0.85:
        metrics['quality_grade'] = 'A'
    elif quality_score >= 0.70:
        metrics['quality_grade'] = 'B'
    elif quality_score >= 0.55:
        metrics['quality_grade'] = 'C'
    elif quality_score >= 0.40:
        metrics['quality_grade'] = 'D'
    else:
        metrics['quality_grade'] = 'F'
    
    return metrics


def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """
    Calculate simple semantic similarity between texts.
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Similarity score (0-1)
    """
    
    # Simple word overlap-based similarity
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1 & words2
    union = words1 | words2
    
    jaccard_similarity = len(intersection) / len(union)
    
    return round(jaccard_similarity, 3)


def analyze_chunk_statistics(chunks: List) -> Dict:
    """
    Analyze statistics of document chunks.
    
    Args:
        chunks: List of Chunk objects
        
    Returns:
        Dictionary with chunk statistics
    """
    
    if not chunks:
        return {
            'total_chunks': 0,
            'avg_chunk_size': 0,
            'min_chunk_size': 0,
            'max_chunk_size': 0,
            'total_characters': 0
        }
    
    sizes = [len(chunk.text) for chunk in chunks]
    
    return {
        'total_chunks': len(chunks),
        'avg_chunk_size': round(sum(sizes) / len(sizes)),
        'min_chunk_size': min(sizes),
        'max_chunk_size': max(sizes),
        'total_characters': sum(sizes),
        'size_distribution': {
            'small': sum(1 for s in sizes if s < 500),
            'medium': sum(1 for s in sizes if 500 <= s < 1000),
            'large': sum(1 for s in sizes if s >= 1000)
        }
    }


def calculate_token_usage(
    prompt_tokens: int,
    completion_tokens: int,
    model: str = "gpt-3.5-turbo"
) -> Dict:
    """
    Calculate cost and usage metrics for LLM calls.
    
    Args:
        prompt_tokens: Number of prompt tokens
        completion_tokens: Number of completion tokens
        model: Model name
        
    Returns:
        Dictionary with usage metrics and costs
    """
    
    # Pricing per 1M tokens (as of 2024)
    pricing = {
        'gpt-3.5-turbo': {'prompt': 0.5, 'completion': 1.5},
        'gpt-4': {'prompt': 30.0, 'completion': 60.0},
        'gpt-4-turbo': {'prompt': 10.0, 'completion': 30.0}
    }
    
    # Get pricing or use default
    model_pricing = pricing.get(model, pricing['gpt-3.5-turbo'])
    
    total_tokens = prompt_tokens + completion_tokens
    
    # Calculate costs (per 1M tokens)
    prompt_cost = (prompt_tokens / 1_000_000) * model_pricing['prompt']
    completion_cost = (completion_tokens / 1_000_000) * model_pricing['completion']
    total_cost = prompt_cost + completion_cost
    
    return {
        'prompt_tokens': prompt_tokens,
        'completion_tokens': completion_tokens,
        'total_tokens': total_tokens,
        'prompt_cost_usd': round(prompt_cost, 6),
        'completion_cost_usd': round(completion_cost, 6),
        'total_cost_usd': round(total_cost, 6),
        'model': model
    }


def benchmark_retrieval_speed(
    retrieval_time_ms: float,
    num_documents: int
) -> Dict:
    """
    Benchmark retrieval performance.
    
    Args:
        retrieval_time_ms: Time taken for retrieval in milliseconds
        num_documents: Number of documents retrieved
        
    Returns:
        Performance metrics
    """
    
    docs_per_second = (num_documents / retrieval_time_ms) * 1000 if retrieval_time_ms > 0 else 0
    
    # Performance grade
    if retrieval_time_ms < 100:
        grade = 'Excellent'
    elif retrieval_time_ms < 500:
        grade = 'Good'
    elif retrieval_time_ms < 1000:
        grade = 'Fair'
    else:
        grade = 'Slow'
    
    return {
        'retrieval_time_ms': round(retrieval_time_ms, 2),
        'num_documents': num_documents,
        'docs_per_second': round(docs_per_second, 2),
        'performance_grade': grade
    }


def create_performance_report(
    retrieval_metrics: Dict,
    response_quality: Dict,
    timing_metrics: Optional[Dict] = None
) -> str:
    """
    Create a formatted performance report.
    
    Args:
        retrieval_metrics: Retrieval quality metrics
        response_quality: Response quality metrics
        timing_metrics: Optional timing metrics
        
    Returns:
        Formatted report string
    """
    
    report = "# RAG Performance Report\n\n"
    
    # Retrieval section
    report += "## Retrieval Quality\n"
    report += f"- **Grade**: {retrieval_metrics.get('quality_grade', 'N/A')}\n"
    report += f"- **Documents Retrieved**: {retrieval_metrics.get('num_results', 0)}\n"
    report += f"- **Average Score**: {retrieval_metrics.get('avg_score', 0.0)}\n"
    report += f"- **Above Threshold**: {retrieval_metrics.get('above_threshold', 0)}\n\n"
    
    # Response quality section
    report += "## Response Quality\n"
    report += f"- **Grade**: {response_quality.get('quality_grade', 'N/A')}\n"
    report += f"- **Quality Score**: {response_quality.get('quality_score', 0.0)}\n"
    report += f"- **Word Count**: {response_quality.get('word_count', 0)}\n"
    report += f"- **Has Citations**: {'Yes' if response_quality.get('has_citations') else 'No'}\n"
    report += f"- **Lexical Diversity**: {response_quality.get('lexical_diversity', 0.0)}\n\n"
    
    # Timing section (if available)
    if timing_metrics:
        report += "## Performance\n"
        report += f"- **Retrieval Time**: {timing_metrics.get('retrieval_time_ms', 0)} ms\n"
        report += f"- **Generation Time**: {timing_metrics.get('generation_time_ms', 0)} ms\n"
        report += f"- **Total Time**: {timing_metrics.get('total_time_ms', 0)} ms\n\n"
    
    return report

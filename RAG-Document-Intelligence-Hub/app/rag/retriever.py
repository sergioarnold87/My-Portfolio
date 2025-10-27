"""
Advanced Retriever Module
Intelligent document retrieval with multiple strategies and re-ranking.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from langchain.vectorstores.base import VectorStore
from .query_analyzer import QueryIntent, suggest_retrieval_strategy


@dataclass
class RetrievalResult:
    """Container for a single retrieval result."""
    text: str
    metadata: Dict
    score: float
    rank: int
    
    def __repr__(self):
        return f"RetrievalResult(rank={self.rank}, score={self.score:.3f})"


class AdvancedRetriever:
    """Advanced retrieval with query understanding and re-ranking."""
    
    def __init__(
        self,
        vectorstore: VectorStore,
        default_k: int = 5,
        use_reranking: bool = True,
        diversity_enabled: bool = False
    ):
        """
        Initialize advanced retriever.
        
        Args:
            vectorstore: Vector store instance
            default_k: Default number of results to retrieve
            use_reranking: Enable re-ranking of results
            diversity_enabled: Promote diversity in results
        """
        self.vectorstore = vectorstore
        self.default_k = default_k
        self.use_reranking = use_reranking
        self.diversity_enabled = diversity_enabled
        
    def retrieve(
        self,
        query: str,
        k: Optional[int] = None,
        query_intent: Optional[QueryIntent] = None,
        filters: Optional[Dict] = None
    ) -> List[RetrievalResult]:
        """
        Retrieve relevant documents for query.
        
        Args:
            query: Search query
            k: Number of results (uses default if None)
            query_intent: Pre-analyzed query intent
            filters: Metadata filters
            
        Returns:
            List of RetrievalResult objects
        """
        
        k = k or self.default_k
        
        # Get retrieval strategy if query intent is provided
        if query_intent:
            strategy = suggest_retrieval_strategy(query_intent)
            k = strategy.get('k', k)
            search_type = strategy.get('search_type', 'similarity')
            score_threshold = strategy.get('score_threshold', 0.0)
        else:
            search_type = 'mmr' if self.diversity_enabled else 'similarity'
            score_threshold = 0.0
        
        # Perform retrieval
        if search_type == 'mmr':
            docs = self._retrieve_mmr(query, k, filters)
        else:
            docs = self._retrieve_similarity(query, k, filters)
        
        # Convert to RetrievalResult objects
        results = []
        for i, (doc, score) in enumerate(docs):
            result = RetrievalResult(
                text=doc.page_content,
                metadata=doc.metadata,
                score=score,
                rank=i + 1
            )
            results.append(result)
        
        # Filter by score threshold
        if score_threshold > 0:
            results = [r for r in results if r.score >= score_threshold]
        
        # Re-rank if enabled
        if self.use_reranking and len(results) > 1:
            results = self._rerank_results(query, results, query_intent)
        
        return results
    
    def _retrieve_similarity(
        self,
        query: str,
        k: int,
        filters: Optional[Dict]
    ) -> List[Tuple]:
        """Retrieve using similarity search."""
        
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k, "filter": filters} if filters else {"k": k}
        )
        
        # Get documents with scores
        docs = self.vectorstore.similarity_search_with_score(query, k=k)
        
        return docs
    
    def _retrieve_mmr(
        self,
        query: str,
        k: int,
        filters: Optional[Dict]
    ) -> List[Tuple]:
        """Retrieve using Maximum Marginal Relevance for diversity."""
        
        # MMR parameters
        fetch_k = k * 3  # Fetch more candidates
        lambda_mult = 0.5  # Balance relevance vs diversity
        
        try:
            docs = self.vectorstore.max_marginal_relevance_search_with_score(
                query,
                k=k,
                fetch_k=fetch_k,
                lambda_mult=lambda_mult
            )
            return docs
        except AttributeError:
            # Fallback to similarity if MMR not supported
            return self._retrieve_similarity(query, k, filters)
    
    def _rerank_results(
        self,
        query: str,
        results: List[RetrievalResult],
        query_intent: Optional[QueryIntent]
    ) -> List[RetrievalResult]:
        """
        Re-rank results using additional heuristics.
        
        Args:
            query: Original query
            results: Initial retrieval results
            query_intent: Query analysis
            
        Returns:
            Re-ranked list of results
        """
        
        # Calculate additional relevance signals
        for result in results:
            relevance_boost = 0.0
            
            # Boost if query keywords appear in text
            if query_intent:
                keyword_matches = sum(
                    1 for kw in query_intent.keywords
                    if kw.lower() in result.text.lower()
                )
                relevance_boost += keyword_matches * 0.05
                
                # Boost if entities appear
                entity_matches = sum(
                    1 for entity in query_intent.entities
                    if entity.lower() in result.text.lower()
                )
                relevance_boost += entity_matches * 0.1
            
            # Boost based on chunk position (earlier chunks often more important)
            chunk_id = result.metadata.get('chunk_id', 999)
            position_boost = max(0, 0.1 - (chunk_id * 0.01))
            relevance_boost += position_boost
            
            # Apply boost
            result.score += relevance_boost
        
        # Re-sort by adjusted score
        results.sort(key=lambda x: x.score, reverse=True)
        
        # Update ranks
        for i, result in enumerate(results):
            result.rank = i + 1
        
        return results
    
    def retrieve_with_context(
        self,
        query: str,
        k: Optional[int] = None,
        context_window: int = 1
    ) -> List[RetrievalResult]:
        """
        Retrieve results with surrounding context chunks.
        
        Args:
            query: Search query
            k: Number of results
            context_window: Number of surrounding chunks to include
            
        Returns:
            List of results with expanded context
        """
        
        # Get initial results
        results = self.retrieve(query, k)
        
        if context_window == 0:
            return results
        
        # Expand with context
        expanded_results = []
        
        for result in results:
            chunk_id = result.metadata.get('chunk_id')
            
            if chunk_id is not None:
                # Try to get surrounding chunks
                context_chunks = self._get_surrounding_chunks(
                    chunk_id,
                    context_window,
                    result.metadata
                )
                
                if context_chunks:
                    # Combine chunks
                    combined_text = '\n\n'.join(context_chunks)
                    result.text = combined_text
                    result.metadata['expanded_context'] = True
            
            expanded_results.append(result)
        
        return expanded_results
    
    def _get_surrounding_chunks(
        self,
        chunk_id: int,
        window: int,
        base_metadata: Dict
    ) -> List[str]:
        """Get surrounding chunks by ID."""
        
        # This is a simplified implementation
        # In production, you'd query the vectorstore with metadata filters
        
        chunks = [base_metadata.get('text', '')]
        
        # TODO: Implement actual surrounding chunk retrieval
        # This would require storing and querying chunks by sequential IDs
        
        return chunks
    
    def hybrid_search(
        self,
        query: str,
        k: int = 5,
        semantic_weight: float = 0.7
    ) -> List[RetrievalResult]:
        """
        Hybrid search combining semantic and keyword-based retrieval.
        
        Args:
            query: Search query
            k: Number of results
            semantic_weight: Weight for semantic search (0-1)
            
        Returns:
            Combined and re-ranked results
        """
        
        keyword_weight = 1.0 - semantic_weight
        
        # Semantic search
        semantic_results = self.retrieve(query, k=k * 2)
        
        # Simple keyword search (simulation)
        # In production, use BM25 or similar
        keyword_results = self._keyword_search(query, k=k * 2)
        
        # Combine scores
        combined_scores = {}
        
        for result in semantic_results:
            key = result.text[:100]  # Use text prefix as key
            combined_scores[key] = result.score * semantic_weight
        
        for result in keyword_results:
            key = result.text[:100]
            if key in combined_scores:
                combined_scores[key] += result.score * keyword_weight
            else:
                combined_scores[key] = result.score * keyword_weight
        
        # Create final results
        final_results = []
        seen = set()
        
        all_results = semantic_results + keyword_results
        for result in all_results:
            key = result.text[:100]
            if key not in seen:
                result.score = combined_scores.get(key, result.score)
                final_results.append(result)
                seen.add(key)
        
        # Sort and limit
        final_results.sort(key=lambda x: x.score, reverse=True)
        final_results = final_results[:k]
        
        # Update ranks
        for i, result in enumerate(final_results):
            result.rank = i + 1
        
        return final_results
    
    def _keyword_search(self, query: str, k: int) -> List[RetrievalResult]:
        """Simple keyword-based search (fallback)."""
        
        # This is a simplified implementation
        # In production, use proper keyword search like BM25
        
        query_terms = query.lower().split()
        
        # For now, just return semantic search results
        # This should be replaced with actual keyword search
        return self.retrieve(query, k=k)

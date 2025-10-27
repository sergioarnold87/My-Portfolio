"""
Contextual Generator Module
LLM-powered answer generation with citation and quality control.
"""

from typing import List, Optional, Dict
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from .retriever import RetrievalResult
from .query_analyzer import QueryIntent, QueryType


class ContextualGenerator:
    """Generate contextual answers with citations."""
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.3,
        max_tokens: int = 500
    ):
        """
        Initialize generator.
        
        Args:
            model_name: OpenAI model name
            temperature: Generation temperature (0-1)
            max_tokens: Maximum tokens in response
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize LLM
        if "gpt-3.5" in model_name or "gpt-4" in model_name:
            self.llm = ChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            self.llm = OpenAI(
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens
            )
    
    def generate(
        self,
        query: str,
        retrieved_docs: List[RetrievalResult],
        query_intent: Optional[QueryIntent] = None,
        include_citations: bool = True
    ) -> Dict:
        """
        Generate answer from retrieved documents.
        
        Args:
            query: User query
            retrieved_docs: Retrieved document chunks
            query_intent: Query analysis results
            include_citations: Whether to include source citations
            
        Returns:
            Dictionary with 'answer', 'sources', 'confidence'
        """
        
        if not retrieved_docs:
            return {
                'answer': "I couldn't find relevant information to answer your question.",
                'sources': [],
                'confidence': 0.0
            }
        
        # Select appropriate prompt based on query type
        prompt_template = self._select_prompt_template(query_intent)
        
        # Format context from retrieved docs
        context = self._format_context(retrieved_docs, include_citations)
        
        # Create prompt
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=prompt_template
        )
        
        # Generate answer
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            answer = chain.run(context=context, question=query)
            
            # Calculate confidence
            confidence = self._calculate_confidence(answer, retrieved_docs)
            
            # Extract sources
            sources = self._extract_sources(retrieved_docs)
            
            return {
                'answer': answer.strip(),
                'sources': sources,
                'confidence': confidence,
                'num_sources': len(retrieved_docs)
            }
            
        except Exception as e:
            return {
                'answer': f"Error generating answer: {str(e)}",
                'sources': [],
                'confidence': 0.0
            }
    
    def _select_prompt_template(self, query_intent: Optional[QueryIntent]) -> str:
        """Select appropriate prompt template based on query type."""
        
        if not query_intent:
            return self._get_default_template()
        
        templates = {
            QueryType.FACTUAL: self._get_factual_template(),
            QueryType.COMPARISON: self._get_comparison_template(),
            QueryType.SUMMARY: self._get_summary_template(),
            QueryType.EXPLANATION: self._get_explanation_template(),
            QueryType.LISTING: self._get_listing_template(),
            QueryType.PROCEDURAL: self._get_procedural_template(),
            QueryType.CONCEPTUAL: self._get_conceptual_template(),
            QueryType.DEFINITION: self._get_definition_template()
        }
        
        return templates.get(query_intent.query_type, self._get_default_template())
    
    def _get_default_template(self) -> str:
        """Default QA template."""
        return """You are a helpful assistant that answers questions based on the provided context.

Context:
{context}

Question: {question}

Instructions:
- Answer the question using ONLY the information from the context above
- Be concise and accurate
- If the context doesn't contain enough information, say so
- Include relevant details and examples when available

Answer:"""
    
    def _get_factual_template(self) -> str:
        """Template for factual queries."""
        return """You are a precise assistant providing factual answers.

Context:
{context}

Question: {question}

Instructions:
- Provide a direct, factual answer
- Use exact information from the context
- Be concise but complete
- Cite specific details when relevant

Answer:"""
    
    def _get_comparison_template(self) -> str:
        """Template for comparison queries."""
        return """You are an analytical assistant comparing concepts.

Context:
{context}

Question: {question}

Instructions:
- Compare the items systematically
- Highlight both similarities and differences
- Use a structured format (bullet points or table)
- Be objective and balanced

Answer:"""
    
    def _get_summary_template(self) -> str:
        """Template for summary queries."""
        return """You are an expert at summarizing information.

Context:
{context}

Question: {question}

Instructions:
- Provide a concise summary covering main points
- Use bullet points or numbered lists for clarity
- Maintain the key information hierarchy
- Keep it comprehensive but brief

Answer:"""
    
    def _get_explanation_template(self) -> str:
        """Template for explanation queries."""
        return """You are a teacher explaining concepts clearly.

Context:
{context}

Question: {question}

Instructions:
- Explain the concept thoroughly
- Include reasoning and mechanisms
- Use examples when available
- Break down complex ideas into understandable parts

Answer:"""
    
    def _get_listing_template(self) -> str:
        """Template for listing queries."""
        return """You are an assistant creating comprehensive lists.

Context:
{context}

Question: {question}

Instructions:
- Create a well-organized list
- Include all relevant items from the context
- Group or categorize if appropriate
- Be complete and systematic

Answer:"""
    
    def _get_procedural_template(self) -> str:
        """Template for procedural queries."""
        return """You are a guide providing step-by-step instructions.

Context:
{context}

Question: {question}

Instructions:
- Provide clear, sequential steps
- Number each step
- Include important details and warnings
- Make it actionable and practical

Answer:"""
    
    def _get_conceptual_template(self) -> str:
        """Template for conceptual queries."""
        return """You are an expert explaining relationships and connections.

Context:
{context}

Question: {question}

Instructions:
- Explain the relationships between concepts
- Show how ideas connect and influence each other
- Provide a holistic understanding
- Use analogies if helpful

Answer:"""
    
    def _get_definition_template(self) -> str:
        """Template for definition queries."""
        return """You are a dictionary providing clear definitions.

Context:
{context}

Question: {question}

Instructions:
- Provide a clear, precise definition
- Include the essential characteristics
- Add context or examples if helpful
- Keep it concise but complete

Answer:"""
    
    def _format_context(
        self,
        docs: List[RetrievalResult],
        include_citations: bool
    ) -> str:
        """Format retrieved documents as context."""
        
        context_parts = []
        
        for i, doc in enumerate(docs, 1):
            if include_citations:
                # Include source reference
                chunk_id = doc.metadata.get('chunk_id', i)
                context_parts.append(f"[Source {i}, Chunk {chunk_id}]\n{doc.text}")
            else:
                context_parts.append(doc.text)
        
        return "\n\n---\n\n".join(context_parts)
    
    def _calculate_confidence(
        self,
        answer: str,
        docs: List[RetrievalResult]
    ) -> float:
        """Calculate confidence score for the answer."""
        
        if not answer or "don't know" in answer.lower() or "cannot answer" in answer.lower():
            return 0.3
        
        # Base confidence on retrieval scores
        if docs:
            avg_score = sum(doc.score for doc in docs) / len(docs)
            confidence = min(0.95, avg_score)
        else:
            confidence = 0.5
        
        # Boost if answer is substantial
        if len(answer.split()) > 30:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _extract_sources(self, docs: List[RetrievalResult]) -> List[Dict]:
        """Extract source information from documents."""
        
        sources = []
        
        for doc in docs:
            source_info = {
                'chunk_id': doc.metadata.get('chunk_id', 'unknown'),
                'score': round(doc.score, 3),
                'preview': doc.text[:200] + '...' if len(doc.text) > 200 else doc.text
            }
            
            # Add any additional metadata
            if 'page' in doc.metadata:
                source_info['page'] = doc.metadata['page']
            if 'section' in doc.metadata:
                source_info['section'] = doc.metadata['section']
            
            sources.append(source_info)
        
        return sources
    
    def generate_with_fallback(
        self,
        query: str,
        retrieved_docs: List[RetrievalResult],
        query_intent: Optional[QueryIntent] = None
    ) -> Dict:
        """Generate answer with fallback to simpler generation if primary fails."""
        
        try:
            return self.generate(query, retrieved_docs, query_intent)
        except Exception as e:
            # Fallback: simple generation without complex prompting
            try:
                context = "\n\n".join([doc.text for doc in retrieved_docs[:3]])
                simple_prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
                
                answer = self.llm.predict(simple_prompt)
                
                return {
                    'answer': answer.strip(),
                    'sources': self._extract_sources(retrieved_docs),
                    'confidence': 0.6,
                    'fallback_used': True
                }
            except Exception as fallback_error:
                return {
                    'answer': f"Unable to generate answer: {str(fallback_error)}",
                    'sources': [],
                    'confidence': 0.0,
                    'error': True
                }

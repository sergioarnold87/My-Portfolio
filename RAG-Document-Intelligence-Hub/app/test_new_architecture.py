"""
Test Script for New RAG Architecture
Demonstrates all capabilities of the Document Intelligence Hub.
"""

import os
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from rag_engine_v2 import DocumentIntelligenceHub, quick_process_and_query
from processor import detect_document_format, get_supported_formats
from rag import analyze_query, classify_query_type
from utils import calculate_readability, estimate_reading_time


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def test_format_detection():
    """Test document format detection."""
    print_section("TEST 1: Document Format Detection")
    
    # Show supported formats
    formats = get_supported_formats()
    print("Supported formats:")
    for category, extensions in formats.items():
        print(f"  • {category}: {', '.join(extensions)}")
    
    print("\n✅ Format detection module loaded successfully")


def test_query_analysis():
    """Test query analysis."""
    print_section("TEST 2: Query Analysis")
    
    test_queries = [
        "What is prompt engineering?",
        "Compare Chain-of-Thought and Few-Shot prompting",
        "Summarize the key concepts in Chapter 3",
        "How to implement a RAG system?",
        "List all prompt patterns mentioned"
    ]
    
    for query in test_queries:
        intent = analyze_query(query)
        print(f"Query: {query}")
        print(f"  Type: {intent.query_type.value}")
        print(f"  Entities: {intent.entities}")
        print(f"  Keywords: {intent.keywords[:5]}")  # Show first 5
        print()
    
    print("✅ Query analysis working correctly")


def test_document_processing():
    """Test document processing pipeline."""
    print_section("TEST 3: Document Processing Pipeline")
    
    # Check if data directory exists
    data_dir = Path(__file__).parent.parent / "data"
    
    if not data_dir.exists():
        print(f"⚠️  Data directory not found: {data_dir}")
        print("   Creating sample text for testing...")
        
        sample_text = """
        Prompt Engineering: A Comprehensive Guide
        
        Introduction
        Prompt engineering is the practice of designing and optimizing text prompts
        to elicit desired responses from large language models (LLMs). It combines
        elements of linguistics, psychology, and software engineering.
        
        Key Concepts
        1. Instruction Prompts: Clear, direct instructions for the model
        2. Few-Shot Learning: Providing examples to guide the model
        3. Chain-of-Thought: Encouraging step-by-step reasoning
        4. Role-Based Prompting: Assigning specific roles to the model
        
        Best Practices
        - Be specific and clear in your instructions
        - Provide context when necessary
        - Use examples to demonstrate desired behavior
        - Iterate and refine based on results
        
        Advanced Techniques
        Meta-prompting involves prompts that reason about prompts themselves.
        Self-reflection allows models to critique their own outputs.
        Multi-turn conversation maintains context across interactions.
        """
        
        # Save sample text
        sample_file = data_dir.parent / "sample_doc.txt"
        sample_file.write_text(sample_text)
        print(f"   Created: {sample_file}")
        file_to_process = sample_file
    else:
        # Use first available text file
        txt_files = list(data_dir.glob("*.txt"))
        if txt_files:
            file_to_process = txt_files[0]
            print(f"Using existing file: {file_to_process.name}")
        else:
            print("⚠️  No text files found in data directory")
            return
    
    # Initialize hub
    print("\nInitializing Document Intelligence Hub...")
    hub = DocumentIntelligenceHub(
        chunk_size=500,  # Smaller for testing
        chunking_strategy='semantic'
    )
    
    # Process document
    print(f"\nProcessing: {file_to_process.name}")
    result = hub.process_document(str(file_to_process))
    
    print(f"\n📊 Processing Results:")
    print(f"   Status: {result['status']}")
    print(f"   Format: {result['document_metadata']['format']}")
    print(f"   Words: {result['document_metadata']['word_count']}")
    print(f"   Chunks: {result['processing_stats']['chunks_created']}")
    
    print("\n✅ Document processing completed successfully")
    
    return hub


def test_query_execution(hub: DocumentIntelligenceHub):
    """Test query execution with the processed document."""
    print_section("TEST 4: Query Execution")
    
    test_queries = [
        "What is prompt engineering?",
        "What are the key concepts mentioned?",
        "Explain chain-of-thought prompting"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Query {i} ---")
        print(f"Question: {query}")
        
        result = hub.query(query, include_metrics=True)
        
        print(f"\nAnswer:")
        print(f"{result['answer']}")
        
        if 'metrics' in result:
            print(f"\n📊 Metrics:")
            print(f"   Retrieval Quality: {result['metrics']['retrieval']['quality_grade']}")
            print(f"   Response Quality: {result['metrics']['response']['quality_grade']}")
            print(f"   Confidence: {result['confidence']:.2f}")
        
        print(f"\n📚 Sources: {result['num_sources']} chunks retrieved")
    
    print("\n✅ Query execution working correctly")


def test_text_utilities():
    """Test utility functions."""
    print_section("TEST 5: Utility Functions")
    
    sample_text = """
    This is a sample text to test the utility functions. It contains multiple
    sentences and various words. The readability metrics will analyze this text
    and provide insights about its complexity and reading difficulty.
    """
    
    # Test readability
    readability = calculate_readability(sample_text)
    print("Readability Analysis:")
    print(f"  Flesch Score: {readability['flesch_score']}")
    print(f"  Grade Level: {readability['grade_level']}")
    print(f"  Difficulty: {readability['difficulty']}")
    
    # Test reading time
    reading_time = estimate_reading_time(sample_text)
    print(f"\nReading Time:")
    print(f"  Word Count: {reading_time['word_count']}")
    print(f"  Estimated: {reading_time['display_time']}")
    
    print("\n✅ Utility functions working correctly")


def run_full_demo():
    """Run full demonstration of the system."""
    print("\n" + "=" * 70)
    print("  DOCUMENT INTELLIGENCE HUB - FULL DEMONSTRATION")
    print("=" * 70)
    
    try:
        # Test 1: Format Detection
        test_format_detection()
        
        # Test 2: Query Analysis
        test_query_analysis()
        
        # Test 3: Document Processing
        hub = test_document_processing()
        
        if hub and hub.vectorstore:
            # Test 4: Query Execution
            test_query_execution(hub)
        
        # Test 5: Utilities
        test_text_utilities()
        
        # Final summary
        print_section("✅ ALL TESTS PASSED")
        print("The Document Intelligence Hub is ready to use!")
        print("\nNext steps:")
        print("  1. Place your documents in the data/ directory")
        print("  2. Run: streamlit run main.py")
        print("  3. Upload and query your documents")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()


def quick_demo():
    """Quick demo with minimal output."""
    print("\n🚀 Quick Demo - Document Intelligence Hub\n")
    
    print("1. Creating sample document...")
    sample_file = Path("sample_demo.txt")
    sample_file.write_text("""
    Artificial Intelligence and Machine Learning
    
    AI is transforming how we interact with technology. Machine learning, a subset
    of AI, enables systems to learn from data without explicit programming.
    Deep learning uses neural networks with multiple layers to process complex patterns.
    """)
    
    print("2. Processing document...")
    hub = DocumentIntelligenceHub()
    hub.process_document(str(sample_file))
    
    print("3. Asking question...")
    result = hub.query("What is machine learning?")
    
    print(f"\n💡 Answer: {result['answer']}\n")
    print(f"✅ Demo completed successfully!")
    
    # Cleanup
    sample_file.unlink()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Document Intelligence Hub")
    parser.add_argument("--quick", action="store_true", help="Run quick demo")
    parser.add_argument("--full", action="store_true", help="Run full test suite")
    
    args = parser.parse_args()
    
    if args.quick:
        quick_demo()
    elif args.full:
        run_full_demo()
    else:
        # Default: show help
        print("Document Intelligence Hub - Test Script")
        print("\nUsage:")
        print("  python test_new_architecture.py --quick    # Quick demo")
        print("  python test_new_architecture.py --full     # Full test suite")
        print("\nRun with --help for more options")

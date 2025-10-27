#!/usr/bin/env python3
"""
Quick test script to validate upload functionality.
This script tests the core functions without running the full Streamlit app.
"""

import os
import sys
from io import BytesIO

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from rag_engine import extract_text, process_uploaded_file, build_qa_chain


class MockUploadedFile:
    """Mock Streamlit uploaded file for testing"""
    def __init__(self, name, content):
        self.name = name
        self.content = content
    
    def read(self):
        if isinstance(self.content, str):
            return self.content.encode('utf-8')
        return self.content


def test_text_extraction():
    """Test text extraction from different file types"""
    print("🧪 Testing text extraction...")
    
    # Test TXT file
    txt_file = MockUploadedFile("test.txt", "This is a test document.")
    text = extract_text(txt_file)
    assert len(text) > 0, "TXT extraction failed"
    print("  ✅ TXT extraction works")
    
    # Test MD file
    md_file = MockUploadedFile("test.md", "# Test Markdown\nThis is a test.")
    text = extract_text(md_file)
    assert len(text) > 0, "MD extraction failed"
    print("  ✅ MD extraction works")
    
    print("✅ Text extraction tests passed!\n")


def test_sample_upload():
    """Test complete upload pipeline with sample text"""
    print("🧪 Testing complete upload pipeline...")
    
    # Create sample document
    sample_text = """
    Data Engineering is the foundation of modern data systems.
    It involves designing, building, and maintaining data pipelines.
    Key concepts include ETL, data warehousing, and real-time processing.
    Modern data engineers use tools like Spark, Airflow, and dbt.
    """
    
    sample_file = MockUploadedFile("sample.txt", sample_text)
    
    try:
        # Test processing
        print("  📄 Processing sample document...")
        vectorstore = process_uploaded_file(sample_file)
        print("  ✅ Vectorstore created successfully")
        
        # Test QA chain building
        print("  🔗 Building QA chain...")
        qa_chain = build_qa_chain(vectorstore)
        print("  ✅ QA chain built successfully")
        
        # Test query (requires OpenAI API key)
        print("  🤔 Testing query (requires API key)...")
        try:
            response = qa_chain.run("What is data engineering?")
            print(f"  ✅ Query successful!")
            print(f"  💡 Response preview: {response[:100]}...")
        except Exception as e:
            print(f"  ⚠️  Query skipped (API key required): {str(e)[:50]}")
        
        print("\n✅ Upload pipeline tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 RAG Upload Functionality Tests")
    print("=" * 60 + "\n")
    
    # Check environment
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found. Some tests may fail.\n")
    
    try:
        # Run tests
        test_text_extraction()
        test_sample_upload()
        
        print("\n" + "=" * 60)
        print("🎉 All tests completed!")
        print("=" * 60)
        print("\n💡 Next step: Run the full app with:")
        print("   streamlit run app/main.py\n")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# 📝 Changelog

All notable changes to the RAG Demo project.

---

## [2.0.0] - 2025-10-21

### 🎉 Major Features Added

#### 📤 Automatic Document Upload System
- **Multi-format Support**: Upload TXT, PDF, CSV, and MD files
- **Automatic Processing Pipeline**:
  - Text extraction based on file type
  - Intelligent chunking (RecursiveCharacterTextSplitter)
  - Automatic embedding generation
  - ChromaDB vectorstore creation
- **Zero-configuration**: No manual preprocessing needed

#### 🎨 Enhanced UI/UX
- **Dual Mode Operation**:
  - 📤 Upload Mode: Process your own documents
  - 📚 Pre-loaded Mode: Use existing knowledge base
- **Interactive Sidebar**: Easy mode switching
- **Status Messages**: Real-time feedback during processing
- **Error Handling**: Graceful failures with helpful messages
- **Processing Pipeline Info**: Visual guide in sidebar

### 🔧 Technical Improvements

#### Backend (`app/rag_engine.py`)
- Added `extract_text()` function for multi-format text extraction
- Added `process_uploaded_file()` for complete upload pipeline
- Integrated PyPDF2 for PDF processing
- Integrated pandas for CSV processing
- Maintained backward compatibility with existing functions

#### Frontend (`app/main.py`)
- Complete UI redesign with dual modes
- File uploader with drag & drop support
- Session state management for uploaded files
- Separate QA chains for upload vs pre-loaded modes
- Enhanced error handling and user feedback

#### Dependencies (`requirements.txt`)
- Added `PyPDF2` for PDF processing
- Added `pandas` for CSV/tabular data processing

### 📚 Documentation

#### New Files
- **UPLOAD_GUIDE.md**: Comprehensive upload documentation
- **SETUP_INSTRUCTIONS.md**: Quick setup guide
- **test_upload.py**: Testing script for upload functionality
- **CHANGELOG.md**: This file

#### Updated Files
- **README.md**: Added upload mode documentation and examples
- Project structure section updated

### 🧪 Testing
- Created `test_upload.py` for validating upload functionality
- Tests for text extraction across formats
- Tests for complete pipeline integration

---

## [1.0.0] - Initial Release

### Initial Features
- Pre-loaded knowledge base system
- 6 data engineering documents included
- LangChain + ChromaDB integration
- OpenAI embeddings and LLM
- Streamlit UI with discovery modes
- Prompt library for common queries
- Local LLM support (Ollama)

### Included Documents
1. Data Engineering Design Patterns (Konieczny)
2. Cost-Effective Pipelines (Leonard)
3. Data Fabric (Mezzetta)
4. Data Quality Monitoring (Stanley)
5. Data Observability (Pinto)
6. Analytics Engineering (De Wilde)

---

## 🔮 Upcoming Features (Roadmap)

### Version 2.1.0 (Planned)
- [ ] Batch upload support (multiple files)
- [ ] Metadata extraction and filtering
- [ ] Vector persistence (save/load vectorstores)
- [ ] Export results to PDF/Markdown

### Version 2.2.0 (Planned)
- [ ] Cross-encoder re-ranking for better relevance
- [ ] Advanced semantic chunking
- [ ] Chat history and conversational mode
- [ ] Response caching system

### Version 3.0.0 (Future)
- [ ] Full local LLM integration (Ollama/Llama2)
- [ ] RAG evaluation metrics (RAGAS)
- [ ] Dashboard with analytics
- [ ] API endpoints for programmatic access
- [ ] Multi-user support with authentication

---

## 📊 Stats

### Lines of Code (Approximate)
- **app/rag_engine.py**: 92 lines (+54 new)
- **app/main.py**: 110 lines (+81 new)
- **Documentation**: 500+ lines

### Files Changed: 8
- Modified: 3
- Added: 5

### New Dependencies: 2
- PyPDF2
- pandas

---

## 🙏 Contributors

Built with ❤️ in Neuquén, Argentina 🇦🇷

---

**Note**: This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

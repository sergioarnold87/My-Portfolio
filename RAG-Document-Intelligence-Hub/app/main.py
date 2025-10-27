import streamlit as st
from rag_engine import (
    load_documents, create_vectorstore, build_qa_chain,
    process_uploaded_file
)
from prompts import PROMPT_LIBRARY

st.set_page_config(page_title="RAG Data Engineering Assistant", layout="wide")

st.title("🧠 RAG Demo — Data Engineering Discovery Assistant")
st.write("Upload your document or use the pre-loaded knowledge base to explore data engineering concepts.")

# ========== Sidebar: Source Selection ==========
st.sidebar.title("📁 Data Source")
source_mode = st.sidebar.radio(
    "Choose your data source:",
    ["📤 Upload Document", "📚 Pre-loaded Knowledge Base"]
)

# ========== Upload Mode ==========
if source_mode == "📤 Upload Document":
    st.subheader("📤 Upload Your Document")
    uploaded_file = st.file_uploader(
        "Drop your document here (.txt, .pdf, .csv, .md)", 
        type=['txt', 'pdf', 'csv', 'md'],
        accept_multiple_files=False
    )
    
    if uploaded_file:
        # Check if this is a new file
        if "uploaded_filename" not in st.session_state or st.session_state.uploaded_filename != uploaded_file.name:
            with st.spinner("🔄 Processing document: extracting, chunking, embedding..."):
                try:
                    vectorstore = process_uploaded_file(uploaded_file)
                    st.session_state.qa = build_qa_chain(vectorstore)
                    st.session_state.uploaded_filename = uploaded_file.name
                    st.success(f"✅ Document '{uploaded_file.name}' processed successfully! Ready to query.")
                except Exception as e:
                    st.error(f"❌ Error processing document: {str(e)}")
                    st.session_state.qa = None
        
        # Query section (only if QA is ready)
        if "qa" in st.session_state and st.session_state.qa:
            st.subheader("💬 Ask Questions")
            query = st.text_area("Type your question about the uploaded document:")
            
            if st.button("🔍 Analyze"):
                if query:
                    with st.spinner("🧠 Analyzing document..."):
                        try:
                            response = st.session_state.qa.run(query)
                            st.subheader("💡 Insight:")
                            st.write(response)
                        except Exception as e:
                            st.error(f"❌ Error during analysis: {str(e)}")
                else:
                    st.warning("⚠️ Please enter a question.")

# ========== Pre-loaded Knowledge Base Mode ==========
else:
    # Load and build only once
    if "preloaded_qa" not in st.session_state:
        with st.spinner("📚 Loading knowledge base from data/ directory..."):
            try:
                docs = load_documents("data/")
                if docs:
                    vectorstore = create_vectorstore(docs)
                    st.session_state.preloaded_qa = build_qa_chain(vectorstore)
                    st.success(f"✅ Loaded {len(docs)} documents from knowledge base.")
                else:
                    st.warning("⚠️ No documents found in data/ directory.")
                    st.session_state.preloaded_qa = None
            except Exception as e:
                st.error(f"❌ Error loading knowledge base: {str(e)}")
                st.session_state.preloaded_qa = None
    
    qa = st.session_state.get("preloaded_qa")
    
    if qa:
        # Select mode from prompt library
        st.subheader("🎯 Discovery Modes")
        mode = st.selectbox("Select a discovery mode:", list(PROMPT_LIBRARY.keys()))
        st.info(f"**Prompt:** {PROMPT_LIBRARY[mode]}")
        
        user_query = st.text_area("Or type your own question:")
        
        if st.button("🚀 Run Discovery"):
            query = user_query if user_query else PROMPT_LIBRARY[mode]
            with st.spinner("🧠 Reasoning through sources..."):
                try:
                    response = qa.run(query)
                    st.subheader("💡 Insight:")
                    st.write(response)
                except Exception as e:
                    st.error(f"❌ Error during discovery: {str(e)}")

# ========== Footer Info ==========
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About")
st.sidebar.info(
    """
    **Automatic Processing Pipeline:**
    1. 📄 Text Extraction
    2. ✂️ Smart Chunking
    3. 🧬 Embedding Generation
    4. 🔍 Semantic Retrieval
    5. 🤖 LLM-powered Insights
    """
)

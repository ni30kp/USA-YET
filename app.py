import streamlit as st
import os
from query_engine import load_query_engine
from ingest import build_index
from document_manager import DocumentManager
from config import OPENAI_API_KEY, LLAMAINDEX_API_KEY, DOCS_PATH
import tempfile
import shutil
from datetime import datetime

# Initialize document manager
@st.cache_resource
def get_document_manager():
    return DocumentManager(DOCS_PATH)

st.set_page_config(
    page_title="Multi-Hop RAG Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.document-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    border-left: 4px solid #1f77b4;
}
.document-header {
    font-weight: bold;
    color: #1f77b4;
}
.document-meta {
    font-size: 0.8rem;
    color: #666;
}
.success-box {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 0.75rem;
    border-radius: 0.25rem;
    margin: 0.5rem 0;
}
.warning-box {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    color: #856404;
    padding: 0.75rem;
    border-radius: 0.25rem;
    margin: 0.5rem 0;
}
.error-box {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
    padding: 0.75rem;
    border-radius: 0.25rem;
    margin: 0.5rem 0;
}

.quick-start-card {
    background-color: #e8f4f8;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    border-left: 4px solid #17a2b8;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding-left: 20px;
    padding-right: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Multi-Hop RAG Assistant")
st.markdown("Ask questions about your documents and get intelligent, context-aware answers.")

# Initialize document manager
doc_manager = get_document_manager()

# Quick Start Guide at the top - more accessible
with st.expander("📋 Quick Start Guide - Click to expand", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="quick-start-card">
        <strong>1. 📤 Upload Documents</strong><br>
        • Use the sidebar file uploader<br>
        • Supports PDF, TXT, DOCX files<br>
        • Automatic duplicate detection
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="quick-start-card">
        <strong>2. 🔄 Build Index</strong><br>
        • Click "Rebuild Index" after uploads<br>
        • Wait for processing to complete<br>
        • Index is saved automatically
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="quick-start-card">
        <strong>3. ❓ Ask Questions</strong><br>
        • Type questions in the main area<br>
        • Enable debug mode to see sources<br>
        • Get detailed, sourced answers
        </div>
        """, unsafe_allow_html=True)

# Main layout with tabs for better organization
tab1, tab2, tab3 = st.tabs(["💬 Chat & Query", "📚 Documents & Transcripts", "🔧 System & Debug"])

with tab1:
    # Query interface - main focus
    st.header("❓ Ask a Question")
    
    # Debug mode toggle at the top
    debug_mode = st.checkbox("🔍 Show Retrieved Chunks", help="Display the exact text chunks used to answer your question")
    
    query = st.text_input("Your question:", placeholder="e.g., What mental health condition does Robert struggle with?")
    
    if query:
        with st.spinner("🔍 Searching through documents..."):
            try:
                query_engine = load_query_engine()
                
                if debug_mode:
                    # Get the retriever to show retrieved chunks
                    retriever = query_engine._retriever
                    retrieved_nodes = retriever.retrieve(query)
                    
                    st.subheader("🔍 Debug Information")
                    st.write(f"**Query:** {query}")
                    st.write(f"**Retrieved {len(retrieved_nodes)} chunks:**")
                    
                    for i, node in enumerate(retrieved_nodes):
                        with st.expander(f"Chunk {i+1} (Score: {node.score:.3f})"):
                            # Show source filename from metadata
                            source = node.metadata.get('source', 'Unknown source')
                            file_name = node.metadata.get('file_name', 'Unknown file')
                            
                            st.write(f"**Source:** {source}")
                            st.write(f"**File:** {file_name}")
                            st.write(f"**Score:** {node.score:.3f}")
                            st.write("**Text:**")
                            st.text(node.text)
                            
                            # Highlight PTSD mentions
                            if "ptsd" in node.text.lower() or "post-traumatic" in node.text.lower():
                                st.success("🎯 **PTSD MENTION FOUND!**")
                    
                    st.divider()
                
                # Get the actual response
                response = query_engine.query(query)
                
                st.subheader("💡 Answer")
                st.write(response.response)
                
                if debug_mode:
                    st.subheader("📊 Response Metadata")
                    if hasattr(response, 'source_nodes'):
                        st.write(f"Used {len(response.source_nodes)} source chunks")
                        for i, node in enumerate(response.source_nodes):
                            source = node.metadata.get('source', 'Unknown')
                            st.write(f"- Chunk {i+1}: {source}")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Make sure you have:")
                st.info("1. Set your OpenAI API key in .env file")
                st.info("2. Uploaded documents and rebuilt the index")
                st.info("3. Installed all requirements")

with tab2:
    # Document library with scrollable container
    st.header("📚 Documents & Transcripts")
    
    # Sync and display storage statistics at the top
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Sync with Files", help="Sync with files already in data/ directory"):
            with st.spinner("Syncing with filesystem..."):
                sync_result = doc_manager.sync_with_filesystem()
                if sync_result['new_files'] > 0:
                    st.success(f"✅ Synced {sync_result['new_files']} new files!")
                    for filename in sync_result['new_file_names']:
                        st.write(f"- {filename}")
                else:
                    st.info("📁 All files already synced")
    
    with col2:
        stats = doc_manager.get_storage_stats()
        if stats['total_files'] > 0:
            st.info(f"""
            📊 **Storage Stats**
            - Documents: {stats['total_files']}
            - Total Size: {stats['total_size_mb']} MB
            - Avg Size: {stats['average_file_size_mb']} MB
            """)
    
    documents = doc_manager.get_all_documents()
    
    if documents:
        st.write(f"**{len(documents)} documents in library**")
        
        # Use native Streamlit container with height limit
        with st.container(height=400):
            for doc in documents:
                # Determine if file was synced or uploaded
                doc_metadata = doc_manager.metadata.get(doc['filename'], {})
                is_synced = doc_metadata.get('synced', False)
                source_icon = "🔄" if is_synced else "📤"
                source_text = "Synced" if is_synced else "Uploaded"
                
                # Create a card-like layout
                with st.container():
                    col1, col2 = st.columns([5, 1])
                    
                    with col1:
                        st.markdown(f"""
                        **{source_icon} {doc['filename']}**  
                        📅 {source_text}: {doc['upload_date'][:10] if doc['upload_date'] else 'Unknown'}  
                        💾 Size: {round(doc['file_size'] / 1024, 1) if doc['file_size'] else 0} KB  
                        {'✅ Active' if doc['exists'] else '❌ Missing'}
                        """)
                    
                    with col2:
                        # Delete button
                        if st.button(f"🗑️", key=f"delete_{doc['filename']}", help=f"Remove {doc['filename']}"):
                            result = doc_manager.remove_document(doc['filename'])
                            if result['success']:
                                st.success(f"✅ {result['message']}")
                                st.session_state.needs_reindex = True
                                st.rerun()
                            else:
                                st.error(f"❌ {result['message']}")
                    
                    st.divider()
        
    else:
        st.info("📁 No documents uploaded yet. Use the uploader in the sidebar to get started!")
        
        # Show sample documents if they exist
        sample_docs = [f for f in os.listdir(DOCS_PATH) if f.endswith(('.pdf', '.txt', '.docx'))]
        if sample_docs:
            st.write("**Sample documents found:**")
            for doc in sample_docs:
                st.write(f"- {doc}")

with tab3:
    # System check and debug info
    st.header("🔧 System Check & Debug")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Integration Test")
        if st.button("🧪 Test Integration"):
            with st.spinner("Testing integration..."):
                try:
                    query_engine = load_query_engine()
                    test_response = query_engine.query("Hello, are you working?")
                    st.session_state.integration_status = "✅ Integration working!"
                    st.session_state.test_response = str(test_response)
                except Exception as e:
                    st.session_state.integration_status = f"❌ Integration failed: {str(e)}"
                    st.session_state.test_response = None
        
        # Show integration status
        if hasattr(st.session_state, 'integration_status'):
            st.write(st.session_state.integration_status)
    
    with col2:
        st.subheader("Index Management")
        needs_reindex = getattr(st.session_state, 'needs_reindex', False)
        button_text = "🔄 Rebuild Index (New Files Added)" if needs_reindex else "🔄 Rebuild Index"
        button_type = "primary" if needs_reindex else "secondary"
        
        if st.button(button_text, type=button_type):
            with st.spinner("Building index... This may take a few minutes."):
                try:
                    build_index()
                    st.success("✅ Index rebuilt successfully!")
                    st.session_state.needs_reindex = False
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error building index: {str(e)}")
    
    # System information
    st.subheader("System Information")
    st.write("**Configuration:**")
    st.write(f"- Documents Path: {DOCS_PATH}")
    st.write(f"- OpenAI API: {'✅ Configured' if OPENAI_API_KEY else '❌ Not configured'}")
    
    if hasattr(st.session_state, 'test_response'):
        st.write("**Last Test Response:**")
        st.write(st.session_state.test_response)

# Sidebar for document management and controls
with st.sidebar:
    st.header("📁 Upload Documents")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        type=['pdf', 'txt', 'docx'],
        accept_multiple_files=True,
        help="Upload PDF, TXT, or DOCX files to add to the knowledge base"
    )
    
    # Process uploaded files
    if uploaded_files:
        st.subheader("📤 Processing Uploads")
        
        # Initialize processed files tracking
        if 'processed_files' not in st.session_state:
            st.session_state.processed_files = set()
        
        for uploaded_file in uploaded_files:
            file_key = f"{uploaded_file.name}_{uploaded_file.size}"
            
            # Skip if already processed in this session
            if file_key in st.session_state.processed_files:
                continue
                
            file_content = uploaded_file.getbuffer()
            
            # Check for duplicates
            duplicate_check = doc_manager.check_duplicate(uploaded_file.name, file_content)
            
            if duplicate_check['is_duplicate']:
                st.warning(f"⚠️ **{uploaded_file.name}** already exists!")
                
                existing_file = duplicate_check['existing_file']
                upload_date = duplicate_check.get('upload_date', 'Unknown')
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"Replace", key=f"replace_{file_key}", help=f"Replace {uploaded_file.name}"):
                        result = doc_manager.add_document(uploaded_file.name, file_content, force_overwrite=True)
                        if result['success']:
                            st.success(f"✅ {result['message']}")
                            st.session_state.needs_reindex = True
                            st.session_state.processed_files.add(file_key)
                            st.rerun()
                        else:
                            st.error(f"❌ {result['message']}")
                
                with col2:
                    if st.button(f"Skip", key=f"skip_{file_key}", help=f"Skip {uploaded_file.name}"):
                        st.info(f"⏭️ Skipped {uploaded_file.name}")
                        st.session_state.processed_files.add(file_key)
                        st.rerun()
            else:
                # Add new document
                result = doc_manager.add_document(uploaded_file.name, file_content)
                if result['success']:
                    st.success(f"✅ {result['message']}")
                    st.session_state.needs_reindex = True
                    st.session_state.processed_files.add(file_key)
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")
        
        # Clear processed files when no files are uploaded (user cleared the uploader)
        if not uploaded_files and 'processed_files' in st.session_state:
            st.session_state.processed_files.clear()
        
        # Add a clear button for users
        if st.button("🗑️ Clear Upload Queue", help="Clear all uploaded files from the queue"):
            st.session_state.processed_files.clear()
            st.rerun()
    
    # Quick stats in sidebar
    stats = doc_manager.get_storage_stats()
    if stats['total_files'] > 0:
        st.markdown("---")
        st.metric("📊 Total Documents", stats['total_files'])
        st.metric("💾 Total Size", f"{stats['total_size_mb']} MB")
    
    # Quick actions
    st.markdown("---")
    st.markdown("**Quick Actions:**")
    if st.button("🔄 Quick Sync", help="Sync with filesystem"):
        sync_result = doc_manager.sync_with_filesystem()
        if sync_result['new_files'] > 0:
            st.success(f"✅ Found {sync_result['new_files']} new files!")
        else:
            st.info("📁 All synced")
    
    if getattr(st.session_state, 'needs_reindex', False):
        st.warning("⚠️ Index needs rebuilding")
        if st.button("🚀 Rebuild Now", type="primary"):
            with st.spinner("Rebuilding..."):
                try:
                    build_index()
                    st.success("✅ Done!")
                    st.session_state.needs_reindex = False
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Document
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from config import VECTOR_DB_PATH, DOCS_PATH
import torch
import faiss
import os
import pickle

def build_index():
    # Clear existing storage
    if os.path.exists(VECTOR_DB_PATH):
        import shutil
        shutil.rmtree(VECTOR_DB_PATH)
    
    # Load documents with metadata
    documents = []
    for filename in os.listdir(DOCS_PATH):
        if filename.endswith(('.pdf', '.txt', '.docx')):
            file_path = os.path.join(DOCS_PATH, filename)
            try:
                reader = SimpleDirectoryReader(input_files=[file_path])
                docs = reader.load_data()
                for doc in docs:
                    # Add source filename to metadata
                    doc.metadata["source"] = filename
                    doc.metadata["file_name"] = filename
                    documents.append(doc)
            except Exception as e:
                print(f"⚠️  Error loading {filename}: {e}")
                continue
    
    if not documents:
        print("⚠️  No documents found in data/ directory")
        return
    
    print(f"📚 Found {len(documents)} documents to process")
    
    # Aggressive chunking strategy for finding specific quotes
    text_splitter = SentenceSplitter(
        chunk_size=256,  # Much smaller chunks to isolate quotes
        chunk_overlap=64,  # Significant overlap to preserve context
        separator=" ",
        paragraph_separator="\n\n",
        secondary_chunking_regex="[.!?]+",
    )
    
    embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5",
        device="cpu"
    )
    
    # Create index with aggressive chunking
    index = VectorStoreIndex.from_documents(
        documents,
        embed_model=embed_model,
        transformations=[text_splitter],  # Use our custom splitter
        show_progress=True
    )
    
    # Save the index using pickle for better compatibility
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    index_path = os.path.join(VECTOR_DB_PATH, "index.pkl")
    
    with open(index_path, 'wb') as f:
        pickle.dump(index, f)
    
    print("✅ Index built and stored successfully!")
    print(f"📁 Index saved to: {index_path}")
    print(f"🔧 Using aggressive chunking: chunk_size=256, overlap=64")
    print(f"🎯 Optimized for finding specific quotes like 'PTSD'")

if __name__ == "__main__":
    build_index()
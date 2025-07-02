import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("⚠️  Warning: OPENAI_API_KEY not found in environment variables")
    print("   Please set your OpenAI API key in a .env file or environment variable")

# LlamaIndex Configuration (optional - for cloud features)
LLAMAINDEX_API_KEY = os.getenv("LLAMAINDEX_API_KEY")

# Model Configuration
EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
LLM_DEFAULT = os.getenv("LLM_DEFAULT", "openai")
LLM_FALLBACK = os.getenv("LLM_FALLBACK", "ollama/mistral")

# Paths
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "storage/faiss_index")
DOCS_PATH = os.getenv("DOCS_PATH", "data/")
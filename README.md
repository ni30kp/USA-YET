# 🧠 Multi-Hop RAG Assistant

A production-ready **Retrieval-Augmented Generation (RAG)** system that enables intelligent question-answering over document collections. Built with LlamaIndex, OpenAI, and Streamlit for a seamless user experience.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)

## 💻 System Requirements

### 🖥️ **Operating System**
- **Windows**: 10/11 (64-bit)
- **macOS**: 10.14+ (Intel/Apple Silicon)
- **Linux**: Ubuntu 18.04+, CentOS 7+, or equivalent

### 🐍 **Python Environment**
- **Python**: 3.8 - 3.12 (3.13 supported but may have compatibility issues)
- **pip**: Latest version (comes with Python)
- **Virtual environment**: Recommended (venv, conda, or virtualenv)

### 💾 **Hardware Requirements**

#### **Minimum Requirements**
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space
- **CPU**: Any modern processor (2+ cores recommended)
- **Internet**: Required for API calls and model downloads

#### **Recommended for Better Performance**
- **RAM**: 8GB+ (for large document collections)
- **Storage**: 5GB+ free space (for embeddings cache)
- **CPU**: 4+ cores (faster document processing)
- **GPU**: Optional (CUDA-compatible for faster embeddings)

### 🔑 **Required Accounts & API Keys**
- **OpenAI API Key**: Required for GPT models
  - Sign up at [platform.openai.com](https://platform.openai.com)
  - Add billing information (pay-per-use)
  - Generate API key from dashboard
- **Git**: For cloning the repository
- **Internet Connection**: For downloading dependencies and API calls

### 📦 **Software Dependencies** (Auto-installed)
- **Core Libraries**: LlamaIndex, OpenAI, Streamlit, FAISS
- **ML Libraries**: Transformers, Torch, Sentence-Transformers
- **Utilities**: Python-dotenv for environment management

### 📁 **File Format Support**
- **Documents**: PDF, TXT, DOCX, DOC
- **Text Encoding**: UTF-8 (recommended), ASCII, Latin-1
- **File Size**: Up to 50MB per document (configurable)

### 🌐 **Network Requirements**
- **Outbound HTTPS**: For OpenAI API calls
- **Port Access**: 8505 (default Streamlit port, configurable)
- **Bandwidth**: Minimal (API calls are small)

## ✨ Features

### 🔍 **Smart Document Processing**
- **Multi-format support**: PDF, TXT, DOCX files
- **Intelligent chunking**: Optimized text segmentation (256 tokens, 64 overlap)
- **Duplicate detection**: Automatic file hash comparison
- **Metadata tracking**: Upload dates, file sizes, and status

### 🧠 **Advanced RAG Pipeline**
- **Vector similarity search**: FAISS-powered fast retrieval
- **Multi-document synthesis**: Combines information across sources
- **Contradiction handling**: Prioritizes recent/specific statements
- **Source attribution**: Shows exact document references

### 🎯 **Production-Ready UI**
- **Tabbed interface**: Organized Chat & Query, Documents & Transcripts, System & Debug
- **Document management**: Upload, view, and remove files with scrollable library
- **Real-time duplicate alerts**: Smart replace/skip options
- **Debug mode**: Inspect retrieved chunks and similarity scores
- **Storage statistics**: Live tracking of usage and performance
- **One-click setup**: Automated environment configuration
- **Session state management**: Persistent upload queue handling

## 📥 Installation Guide

### 🔧 **Pre-Installation Checklist**
- [ ] Python 3.8+ installed ([Download Python](https://python.org/downloads/))
- [ ] Git installed ([Download Git](https://git-scm.com/downloads))
- [ ] OpenAI API key ready ([Get API Key](https://platform.openai.com/api-keys))
- [ ] 4GB+ RAM available
- [ ] 2GB+ free disk space

### 🎯 **Step-by-Step Installation**

#### **1. Clone the Repository**
```bash
git clone https://github.com/ni30kp/USA-YET.git
cd USA-YET
```

#### **2. Verify Python Installation**
```bash
python --version  # Should show 3.8+
pip --version      # Should show pip version
```

#### **3. Choose Installation Method**

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# After cloning the repository above:

# 2. Run the setup script
python setup.py

# 3. Add your OpenAI API key to .env file
# Edit .env and replace: OPENAI_API_KEY=your_actual_api_key_here

# 4. Start the application
python start.py
```

#### **4. First-Time Setup**
After installation, you'll need to:

1. **Add Documents**: Place your PDF/TXT/DOCX files in the `data/` folder
2. **Build Index**: Click "Rebuild Index" in the System & Debug tab
3. **Test System**: Use the "Test Integration" button to verify everything works
4. **Start Asking Questions**: Switch to Chat & Query tab and start chatting!

### Option 2: Manual Setup

<details>
<summary>Click to expand manual setup instructions</summary>

```bash
# 1. Clone and navigate
git clone https://github.com/ni30kp/USA-YET.git
cd USA-YET

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp env.example .env
# Edit .env and add your OpenAI API key

# 5. Create directories
mkdir -p data storage/faiss_index

# 6. Start the application
streamlit run app.py --server.port 8505
```

</details>

## 📱 Usage

### 🎯 **Quick Start Guide** (Built-in)
- Expandable guide at the top of the interface
- Step-by-step instructions for new users
- Always accessible without scrolling

### 💬 **Chat & Query Tab**
1. **❓ Ask Questions**: Type questions in the main input area
2. **🔍 Debug Mode**: Toggle to see retrieved chunks and similarity scores
3. **📊 Response Analysis**: View source attribution and metadata

### 📚 **Documents & Transcripts Tab**
1. **📄 Upload Files**: Drag and drop PDF, TXT, or DOCX files
2. **📋 Document Library**: Scrollable view of all documents (400px height)
3. **🔄 Sync Files**: Automatically detect files in data/ directory
4. **📊 Storage Stats**: Real-time document count and size tracking
5. **🗑️ File Management**: Remove documents with one-click deletion

### 🔧 **System & Debug Tab**
1. **🧪 Integration Test**: Verify system functionality
2. **🔄 Index Management**: Rebuild index with visual indicators
3. **⚙️ System Information**: Configuration and status details

## 🏗️ System Architecture

### Core Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Document Manager** | File handling, duplicate detection | Python, SHA-256 hashing |
| **Text Processing** | Chunking, embedding generation | LlamaIndex, HuggingFace BGE |
| **Vector Store** | Similarity search, indexing | FAISS (Facebook AI Similarity Search) |
| **Query Engine** | Question answering, synthesis | OpenAI GPT, Custom prompts |
| **Web Interface** | User interaction, file management | Streamlit |

## ⚙️ Configuration

### Environment Variables (`.env`)

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# LLM Settings
LLM_DEFAULT=openai
LLM_FALLBACK=ollama/mistral

# System Paths
DOCS_PATH=data
VECTOR_DB_PATH=storage/faiss_index
```

### Advanced Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `chunk_size` | 256 | Tokens per text chunk |
| `chunk_overlap` | 64 | Overlap between chunks |
| `similarity_top_k` | 10 | Retrieved chunks per query |
| `embedding_model` | `BAAI/bge-small-en-v1.5` | HuggingFace embedding model |

## 🎨 User Interface Features

### 📑 **Tabbed Organization**
- **💬 Chat & Query**: Main interaction area for questions and answers
- **📚 Documents & Transcripts**: Complete document management interface
- **🔧 System & Debug**: Technical controls and debugging tools

### 📱 **Responsive Design**
- **Scrollable document library**: Fixed 400px height with smooth scrolling
- **Quick Start Guide**: Expandable section at the top (no more scrolling to find help)
- **Session state management**: Persistent file upload handling
- **Real-time updates**: Immediate UI refresh after actions

### 🎯 **User Experience Improvements**
- **No excessive scrolling**: Everything organized in accessible tabs
- **Visual feedback**: Progress bars, success/error messages, loading spinners
- **Smart file handling**: Prevents duplicate processing with session tracking
- **One-click actions**: Replace, skip, delete, sync operations

## 🎯 Key Features Explained

### 🔍 **Enhanced File Management**
- **Content-based duplicate detection**: SHA-256 hash comparison
- **Smart alerts**: Shows existing file info with upload dates
- **User choice**: Replace or skip duplicates with one-click actions
- **Session state tracking**: Prevents reprocessing of handled files
- **Automatic sync**: Detects existing files in data/ directory
- **Visual indicators**: 🔄 (Synced) vs 📤 (Uploaded) file sources

### 🧠 **Advanced Prompting**
```python
# Handles contradictory statements intelligently
"If a person discusses a topic more than once:
- Always use the most recent or strongest admission
- Prioritize specific self-disclosures over vague statements"
```

### 📊 **Advanced Debug Mode**
- **Retrieved chunks**: See exact text segments with full context
- **Similarity scores**: Understand relevance rankings (0.0-1.0)
- **Source tracking**: Identify contributing documents with filenames
- **Metadata display**: File names, upload dates, sizes, and status
- **PTSD detection**: Automatic highlighting of mental health mentions
- **Expandable chunks**: Detailed view of each retrieved segment
- **Response metadata**: Shows which chunks were used in final answer

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Import errors** | Ensure virtual environment is activated |
| **OpenAI API errors** | Check API key and billing status |
| **Memory issues** | Reduce chunk size or use smaller models |
| **Slow performance** | Enable GPU acceleration for embeddings |

### Debug Steps

1. **Test Integration**: Use the "Test Integration" button in System & Debug tab
2. **Check Logs**: Look for error messages in terminal
3. **Verify Files**: Use "Sync with Files" to detect existing documents
4. **Rebuild Index**: Try rebuilding after document changes (shows progress)
5. **Clear Upload Queue**: Use "Clear Upload Queue" if files are stuck
6. **Debug Mode**: Enable to inspect retrieved chunks and similarity scores

## 📈 Performance Optimization

### For Large Document Collections

```python
# Recommended settings for 1000+ documents
chunk_size = 512          # Larger chunks for better context
similarity_top_k = 5      # Fewer chunks for faster processing
embedding_model = "BAAI/bge-base-en-v1.5"  # Better quality
```

### Memory Management

- **Batch processing**: Process documents in smaller batches
- **Index compression**: Use FAISS compression for large indices
- **Caching**: Enable embedding caching for repeated queries

## 🚀 Deployment Options

### Local Development
```bash
python start.py
```

### Docker Deployment
```bash
docker build -t rag-assistant .
docker run -p 8505:8505 rag-assistant
```

### Cloud Deployment
- **Streamlit Cloud**: Direct GitHub integration
- **Heroku**: Container-based deployment
- **AWS/GCP**: Full infrastructure control

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Fork the repository
git clone https://github.com/your-username/multi-hop-rag-assistant.git
cd multi-hop-rag-assistant

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and test
python setup.py
python start.py

# Submit pull request
```

## 📚 Documentation

- **[Technical Architecture](TECHNICAL_ARCHITECTURE.md)**: Detailed system design
- **[API Reference](docs/api.md)**: Component documentation
- **[Deployment Guide](docs/deployment.md)**: Production setup
- **[FAQ](docs/faq.md)**: Common questions and answers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[LlamaIndex](https://github.com/run-llama/llama_index)**: RAG framework
- **[FAISS](https://github.com/facebookresearch/faiss)**: Vector similarity search
- **[Streamlit](https://streamlit.io)**: Web application framework
- **[OpenAI](https://openai.com)**: Language model API

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/multi-hop-rag-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/multi-hop-rag-assistant/discussions)
- **Email**: support@yourproject.com

---

<div align="center">
  <strong>Made with ❤️ for the AI community</strong>
</div> 
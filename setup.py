#!/usr/bin/env python3
"""
Multi-Hop RAG Assistant - Easy Setup Script
This script handles the complete setup process for the RAG system.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_step(step, text):
    """Print a formatted step"""
    print(f"\n[{step}] {text}")

def run_command(command, description=""):
    """Run a command and handle errors"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error {description}: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print_step("1", "Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    
    print(f"✅ Python version: {sys.version}")
    return True

def setup_virtual_environment():
    """Create and activate virtual environment"""
    print_step("2", "Setting up virtual environment...")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("📁 Virtual environment already exists")
        return True
    
    # Create virtual environment
    if not run_command(f"{sys.executable} -m venv venv", "creating virtual environment"):
        return False
    
    print("✅ Virtual environment created successfully")
    return True

def install_dependencies():
    """Install required dependencies"""
    print_step("3", "Installing dependencies...")
    
    # Determine pip command based on OS
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/MacOS
        pip_cmd = "venv/bin/pip"
    
    # Upgrade pip first
    if not run_command(f"{pip_cmd} install --upgrade pip", "upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{pip_cmd} install -r requirements.txt", "installing requirements"):
        return False
    
    print("✅ Dependencies installed successfully")
    return True

def setup_environment_file():
    """Create .env file from template"""
    print_step("4", "Setting up environment configuration...")
    
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("📁 .env file already exists")
        return True
    
    if not env_example.exists():
        print("⚠️  env.example not found, creating basic .env file")
        with open(env_file, 'w') as f:
            f.write("# OpenAI API Configuration\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n\n")
            f.write("# LLM Configuration\n")
            f.write("LLM_DEFAULT=openai\n")
            f.write("LLM_FALLBACK=ollama/mistral\n\n")
            f.write("# Paths\n")
            f.write("DOCS_PATH=data\n")
            f.write("VECTOR_DB_PATH=storage/faiss_index\n")
    else:
        shutil.copy(env_example, env_file)
    
    print("✅ Environment file created")
    print("⚠️  Please edit .env file and add your OpenAI API key")
    return True

def create_directories():
    """Create necessary directories"""
    print_step("5", "Creating directories...")
    
    directories = ["data", "storage", "storage/faiss_index"]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    print("✅ Directories created successfully")
    return True

def test_installation():
    """Test if the installation works"""
    print_step("6", "Testing installation...")
    
    # Determine python command based on OS
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/MacOS
        python_cmd = "venv/bin/python"
    
    # Test imports
    test_script = """
import sys
try:
    import streamlit
    import llama_index
    import openai
    import faiss
    import transformers
    print("✅ All required packages imported successfully")
    print(f"✅ Streamlit version: {streamlit.__version__}")
    print(f"✅ LlamaIndex version: {llama_index.__version__}")
    print("✅ Installation test passed!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
"""
    
    with open("test_installation.py", "w") as f:
        f.write(test_script)
    
    success = run_command(f"{python_cmd} test_installation.py", "testing installation")
    
    # Clean up test file
    Path("test_installation.py").unlink(missing_ok=True)
    
    return success

def print_next_steps():
    """Print instructions for next steps"""
    print_header("🎉 SETUP COMPLETE!")
    
    print("\n📋 Next Steps:")
    print("1. Edit the .env file and add your OpenAI API key:")
    print("   OPENAI_API_KEY=your_actual_api_key_here")
    
    print("\n2. Start the application:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\python -m streamlit run app.py --server.port 8505")
    else:  # Unix/Linux/MacOS
        print("   source venv/bin/activate")
        print("   streamlit run app.py --server.port 8505")
    
    print("\n3. Open your browser and go to:")
    print("   http://localhost:8505")
    
    print("\n4. Upload documents and start asking questions!")
    
    print("\n🔧 Troubleshooting:")
    print("- If you get OpenAI API errors, check your API key in .env")
    print("- If you get import errors, try reinstalling dependencies")
    print("- Check the README.md for detailed documentation")

def main():
    """Main setup function"""
    print_header("Multi-Hop RAG Assistant Setup")
    print("This script will set up the complete RAG system for you.")
    
    # Check if user wants to continue
    response = input("\nDo you want to continue with the setup? (y/n): ")
    if response.lower() not in ['y', 'yes']:
        print("Setup cancelled.")
        return
    
    # Run setup steps
    steps = [
        check_python_version,
        setup_virtual_environment,
        install_dependencies,
        setup_environment_file,
        create_directories,
        test_installation
    ]
    
    for step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at step: {step_func.__name__}")
            print("Please check the error messages above and try again.")
            return
    
    print_next_steps()

if __name__ == "__main__":
    main() 
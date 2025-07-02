#!/usr/bin/env python3
"""
Quick Start Script for Multi-Hop RAG Assistant
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check if virtual environment exists
    if not Path("venv").exists():
        print("❌ Virtual environment not found!")
        print("💡 Run: python setup.py")
        return False
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("❌ .env file not found!")
        print("💡 Run: python setup.py")
        return False
    
    # Check if data directory exists
    Path("data").mkdir(exist_ok=True)
    Path("storage").mkdir(exist_ok=True)
    
    print("✅ Environment looks good!")
    return True

def start_app():
    """Start the Streamlit application"""
    if not check_environment():
        return
    
    print("🚀 Starting Multi-Hop RAG Assistant...")
    print("📱 Opening in your browser at: http://localhost:8505")
    print("🛑 Press Ctrl+C to stop the application")
    
    # Determine the correct python command
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/MacOS
        python_cmd = "venv/bin/python"
    
    # Start Streamlit
    try:
        subprocess.run([
            python_cmd, "-m", "streamlit", "run", "app.py", 
            "--server.port", "8505",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Thanks for using Multi-Hop RAG Assistant!")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("💡 Try running: python setup.py")

if __name__ == "__main__":
    start_app() 
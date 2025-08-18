#!/usr/bin/env python3
"""
Start script for SmartInvest Bot
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pandas
        import yfinance
        print("✅ Backend dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting SmartInvest Bot Backend...")
    
    # Change to workspace directory
    os.chdir('/workspace')
    
    # Start the backend server
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "backend.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=False)
    except KeyboardInterrupt:
        print("\n👋 Shutting down SmartInvest Bot...")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def main():
    """Main entry point"""
    print("🤖 SmartInvest Bot - Intelligent Investment Management")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path('/workspace/backend/main.py').exists():
        print("❌ Backend files not found. Please run from the correct directory.")
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("\n📊 Starting the application...")
    print("🌐 Backend will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("\n⚡ Press Ctrl+C to stop the server\n")
    
    # Start the backend
    start_backend()

if __name__ == "__main__":
    main()
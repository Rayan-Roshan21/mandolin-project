#!/usr/bin/env python3
"""
Setup script to check and install dependencies for PA Form Automation
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        print(f"❌ Python {required_version[0]}.{required_version[1]}+ required")
        print(f"   Current version: {current_version[0]}.{current_version[1]}")
        return False
    
    print(f"✅ Python {current_version[0]}.{current_version[1]} - Compatible")
    return True

def install_requirements():
    """Install requirements with error handling"""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    print("📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ])
        
        # Install requirements
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        
        print("✅ Dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def verify_installation():
    """Verify that key packages are installed correctly"""
    packages_to_check = [
        "google.generativeai",
        "mistralai", 
        "fitz",  # PyMuPDF
        "dotenv"
    ]
    
    print("\n🔍 Verifying installation...")
    
    for package in packages_to_check:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Failed to import")
            return False
    
    return True

def create_env_file():
    """Create .env template if it doesn't exist"""
    env_file = Path(".env")
    env_template = Path(".env.template")
    
    template_content = """# API Keys for PA Form Automation Pipeline
# Get Google API key from: https://aistudio.google.com/app/apikey  
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Get Mistral API key from: https://console.mistral.ai/
MISTRAL_API_KEY=your_mistral_api_key_here

# Optional configuration
DEBUG=False
MAX_RETRIES=3
TIMEOUT_SECONDS=30
"""
    
    if not env_template.exists():
        with open(env_template, 'w') as f:
            f.write(template_content)
        print("📝 Created .env.template")
    
    if not env_file.exists():
        print("⚠️  Please copy .env.template to .env and add your API keys")
    else:
        print("✅ .env file exists")

def main():
    """Main setup function"""
    print("🚀 PA Form Automation - Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_requirements():
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("⚠️  Some packages failed to install correctly")
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("📋 Next steps:")
    print("   1. Add your API keys to .env file")
    print("   2. Place PDF files in Input Data/ folder")
    print("   3. Run the automation notebook")
    print("=" * 50)

if __name__ == "__main__":
    main()

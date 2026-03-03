"""
Resume Screening System Setup Script

Run this to set up the entire system from scratch.
"""

import subprocess
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def run_command(command, description):
    """Run a command and report status."""
    print(f"\n{'='*60}")
    print(f"⏳ {description}...")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        print(f"✅ {description} completed successfully!\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with error code {e.returncode}\n")
        return False


def main():
    """Main setup function."""
    
    print("\n" + "="*60)
    print("Resume Screening System - Setup Wizard")
    print("="*60)
    
    # Check Python version
    print(f"\n📌 Python Version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        sys.exit(1)
    
    # Step 1: Install dependencies
    if not run_command(
        "pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        print("⚠️  Failed to install dependencies. Please install manually:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Step 2: Download spaCy model
    print("\n" + "="*60)
    print("⏳ Downloading spaCy model...")
    print("="*60)
    try:
        import spacy
        try:
            spacy.load("en_core_web_sm")
            print("✅ spaCy model already installed")
        except OSError:
            result = subprocess.run(
                "python -m spacy download en_core_web_sm",
                shell=True,
                check=True,
                capture_output=False
            )
            print("✅ spaCy model downloaded successfully!")
    except Exception as e:
        print(f"⚠️  Could not download spaCy model: {e}")
        print("Run manually: python -m spacy download en_core_web_sm")
    
    # Step 3: Verify installations
    print("\n" + "="*60)
    print("⏳ Verifying installations...")
    print("="*60)
    
    verification_script = """
import sys
try:
    import spacy
    print(f"✅ spaCy: {spacy.__version__}")
except ImportError:
    print("❌ spaCy not installed")
    sys.exit(1)

try:
    import transformers
    print(f"✅ Transformers: {transformers.__version__}")
except ImportError:
    print("❌ Transformers not installed")
    sys.exit(1)

try:
    import torch
    print(f"✅ PyTorch: {torch.__version__}")
    print(f"   CUDA available: {torch.cuda.is_available()}")
except ImportError:
    print("❌ PyTorch not installed")
    sys.exit(1)

try:
    import streamlit
    print(f"✅ Streamlit: {streamlit.__version__}")
except ImportError:
    print("❌ Streamlit not installed")
    sys.exit(1)

print("\\n✅ All core dependencies verified!")
"""
    
    try:
        subprocess.run([sys.executable, "-c", verification_script], check=True)
    except subprocess.CalledProcessError:
        print("❌ Some dependencies are missing. Please install them manually.")
        sys.exit(1)
    
    # Step 4: Create necessary directories
    print("\n" + "="*60)
    print("⏳ Creating necessary directories...")
    print("="*60)
    
    directories = ["uploads", "output", "config"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directory created/verified: {directory}")
    
    # Step 5: Final instructions
    print("\n" + "="*60)
    print("🎉 Setup Complete!")
    print("="*60)
    
    print("""
    Next Steps:
    
    1. Start the Web Interface:
       streamlit run app.py
       
    2. Or use the Pipeline Programmatically:
       from src.pipeline import ResumeSceningPipeline
       pipeline = ResumeSceningPipeline()
       result = pipeline.process_resume('resume.pdf', 'job description')
    
    3. Check examples:
       python examples.py
    
    4. Read the documentation:
       - README.md for full documentation
       - config/config.yaml to customize settings
    
    For GPU Acceleration:
    - Most operations will automatically use GPU if available
    - Verify with: python -c "import torch; print(torch.cuda.is_available())"
    
    Enjoy Resume Screening! 🚀
    """)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        logging.exception("Setup error:")
        sys.exit(1)

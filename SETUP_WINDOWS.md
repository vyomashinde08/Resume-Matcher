# SETUP GUIDE FOR WINDOWS

## Quick Setup (5-10 minutes)

### 1. Install Python Dependencies

Open PowerShell or Command Prompt in the project folder and run:

```powershell
# Activate virtual environment
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download spaCy Model

```powershell
python -m spacy download en_core_web_sm
```

### 3. Start the Application

```powershell
streamlit run app.py
```

The web interface will open at `http://localhost:8501`

---

## Detailed Windows Setup

### Prerequisites
- Python 3.8+ ([Download](https://www.python.org/downloads/))
- Git (optional, for version control)
- 4GB RAM minimum (8GB recommended)
- ~2GB disk space for dependencies

### Step-by-Step Installation

#### 1. Check Python Installation

Open PowerShell and run:
```powershell
python --version
pip --version
```

Both should show version numbers. If not, install Python from https://www.python.org/

#### 2. Create Virtual Environment

```powershell
# Check if .venv exists
ls -Name .venv

# If it doesn't exist, create it
python -m venv .venv

# Activate it
.\.venv\Scripts\activate

# You should see (.venv) at the start of the command line
```

#### 3. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

#### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- spaCy (NLP)
- Transformers & PyTorch (BERT)
- scikit-learn (similarity)
- Streamlit (web UI)
- pdfplumber & python-docx (file parsing)
- Pandas & NumPy (data handling)

**First time install might take 5-10 minutes**

#### 5. Download spaCy Model

```powershell
python -m spacy download en_core_web_sm
```

#### 6. Verify Installation

```powershell
python -c "import spacy; import torch; import transformers; print('✅ All libraries installed successfully')"
```

---

## Running the Application

### Option 1: Web Interface (Graphical)

```powershell
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

Features:
- Upload resumes visually
- Enter job description
- View results in browser
- Download CSV export

### Option 2: Python Script (Programmatic)

```powershell
python examples.py
```

Or create your own script:

```python
from src.pipeline import ResumeSceningPipeline

pipeline = ResumeSceningPipeline()

result = pipeline.process_resume(
    "resume.pdf",
    "Senior Developer required..."
)

print(f"Match: {result['percentage_match']:.1f}%")
```

### Option 3: Quick Test

```powershell
python quickstart.py
```

This will:
- Create sample files
- Test all components
- Show you how to proceed

---

## GPU Acceleration (Optional)

If you have an NVIDIA GPU and want faster processing:

### 1. Check CUDA Capability

```powershell
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

If it shows `True`, your GPU is ready!

### 2. Install GPU-Optimized PyTorch

```powershell
# Deactivate and remove current pytorch
pip uninstall torch torchvision torchaudio

# Install CUDA-enabled version (for CUDA 11.8)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

---

## Troubleshooting

### Issue: "Python command not found"
**Solution**: Add Python to PATH
- Right-click "This PC" > Properties > Advanced system settings
- Click "Environment Variables"
- Find and edit the `PATH` variable
- Add the Python installation folder path

### Issue: "venv activation doesn't work"
**Solution**: Try different activation script
```powershell
# If .\.venv\Scripts\activate doesn't work, try:
.\.venv\Scripts\Activate.ps1

# If PowerShell shows execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "Module not found" errors
**Solution**: Reinstall dependencies
```powershell
pip install --force-reinstall -r requirements.txt
```

### Issue: "spaCy model download fails"
**Solution**: Manual download
```powershell
python -m spacy download en_core_web_sm --no-cache

# If still fails, use alternative:
pip install spacy-lookups-data
python -m spacy download en_core_web_sm
```

### Issue: "BERT model is too large" (memory error)
**Solution**: Use smaller model
```python
# In app.py or your script, change:
pipeline = ResumeSceningPipeline(
    model_name="sentence-transformers/all-MiniLM-L6-v2"  # Lighter version
)
```

### Issue: Streamlit app runs slow first time
**Normal!** BERT models are large and take time to load on first run.
Subsequent runs will be much faster.

---

## File Structure

```
Resume_Matcher/
├── src/                          # Core modules
│   ├── preprocessing.py         # Text cleaning
│   ├── ner_extraction.py        # Entity extraction
│   ├── embedding_generator.py   # BERT embeddings
│   ├── similarity_calculator.py # Scoring
│   ├── resume_parser.py         # File parsing
│   ├── pipeline.py              # Main orchestration
│   └── utils.py                 # Helpers
├── config/
│   └── config.yaml              # Settings
├── uploads/                     # Upload directory
├── output/                      # Results directory
├── app.py                       # Streamlit app
├── requirements.txt             # Dependencies
├── README.md                    # Full documentation
├── examples.py                  # Usage examples
├── quickstart.py                # Quick start
└── setup_system.py              # Setup script
```

---

## First Time Usage

1. **Start the app**
   ```powershell
   streamlit run app.py
   ```

2. **Provide input**
   - Paste a job description
   - Upload 1-5 sample resumes (PDF/DOCX/TXT)

3. **Review results**
   - See matching scores
   - Check skill analysis
   - Download as CSV

4. **Customize**
   - Adjust weights in sidebar
   - Change number of results
   - Select different BERT model

---

## Performance Tips

### For Large-Scale Screening
- Use GPU acceleration if available
- Process resumes in batches
- Use smaller BERT model for speed

### Batch Processing Example
```python
resume_files = [f"resume_{i}.pdf" for i in range(100)]

results = pipeline.process_multiple_resumes(
    resume_files,
    job_description,
    top_k=10
)
```

### Expected Times (CPU/GPU)
- First run: 10-30 seconds (model loading)
- Single resume: 1-2 seconds
- 10 resumes: 15-30 seconds
- 100 resumes: 3-5 minutes

---

## Next Steps

1. **[Start WebUI]**
   ```powershell
   streamlit run app.py
   ```

2. **[Test System]**
   ```powershell
   python quickstart.py
   ```

3. **[See Examples]**
   ```powershell
   python examples.py
   ```

4. **[Read Full Docs]**
   Open `README.md` in your editor

---

## Support

- Check [README.md](README.md) for detailed documentation
- Review [examples.py](examples.py) for code samples
- Uncomment logging lines for debugging

---

**Created**: 2024-03-03  
**Version**: 1.0.0  
**Status**: Production Ready ✅

# Resume Screening System

## Overview

A **production-ready**, **AI-powered** Resume Screening System built with Python that automatically matches resumes with job descriptions using advanced Natural Language Processing (NLP) and deep learning models.

### Key Features

✅ **Multi-Format Support**: Handles PDF, DOCX, and TXT files  
✅ **NLP Processing**: spaCy for tokenization, lemmatization, and named entity recognition  
✅ **Deep Learning**: BERT embeddings from HuggingFace Transformers for semantic understanding  
✅ **Intelligent Matching**: Combines semantic similarity and skill-based scoring  
✅ **Comprehensive Analytics**: Detailed reports with skill analysis and matching insights  
✅ **Web Interface**: Beautiful Streamlit UI for easy interaction  
✅ **Production Ready**: Clean architecture, modular code, comprehensive logging  

---

## Project Structure

```
Resume_Matcher/
├── src/                          # Source code modules
│   ├── __init__.py
│   ├── preprocessing.py          # Text cleaning and preprocessing
│   ├── ner_extraction.py         # Named Entity Recognition
│   ├── embedding_generator.py    # BERT embedding generation
│   ├── similarity_calculator.py  # Similarity computation
│   ├── resume_parser.py          # Resume file parsing
│   ├── pipeline.py               # Main orchestration pipeline
│   └── utils.py                  # Utility functions
├── config/                       # Configuration files
│   └── config.yaml              # System configuration
├── uploads/                      # Directory for uploaded resumes
├── output/                       # Directory for results and reports
├── app.py                        # Streamlit web application
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup
└── README.md                     # This file
```

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Text Processing** | spaCy 3.7+ |
| **Embeddings** | BERT (HuggingFace Transformers) |
| **Similarity Metrics** | scikit-learn (Cosine Similarity) |
| **File Parsing** | pdfplumber, python-docx |
| **Web Framework** | Streamlit |
| **Data Processing** | Pandas, NumPy |
| **Deep Learning** | PyTorch |
| **Language** | Python 3.8+ |

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or conda package manager
- 4GB RAM minimum (8GB recommended)
- GPU support (optional, for faster embeddings)

### Step-by-Step Setup

1. **Clone or download the project**
   ```bash
   cd Resume_Matcher
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Verify installation**
   ```bash
   python -c "import spacy; import torch; import transformers; print('✅ All dependencies installed successfully!')"
   ```

---

## Usage

### Option 1: Web Interface (Recommended for Users)

Run the Streamlit web application:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

**Steps:**
1. Enter a job description in the text area
2. Upload PDF, DOCX, or TXT resume files
3. (Optional) Adjust similarity weights in the sidebar
4. Click "Screen Resumes" to process
5. View detailed results and export as CSV

### Option 2: Python Script (For Integration)

Use the pipeline programmatically:

```python
from src.pipeline import ResumeSceningPipeline

# Initialize pipeline
pipeline = ResumeSceningPipeline(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Process single resume
report = pipeline.process_resume(
    resume_path="path/to/resume.pdf",
    job_description="Senior Python Developer..."
)

print(f"Match Score: {report['percentage_match']:.1f}%")
print(f"Matched Skills: {report['matched_required_skills']}")

# Process multiple resumes
results = pipeline.process_multiple_resumes(
    resume_paths=["resume1.pdf", "resume2.docx", "resume3.txt"],
    job_description="Job description text here...",
    top_k=10  # Get top 10 candidates
)

# Display ranked results
for idx, candidate in enumerate(results, 1):
    print(f"{idx}. {candidate['candidate_name']}: {candidate['percentage_match']:.1f}%")
```

---

## Configuration

Edit `config/config.yaml` to customize the system:

```yaml
# spaCy Model
spacy:
  model: "en_core_web_sm"
  lowercase: true
  remove_stopwords: true

# BERT Model
bert:
  model_name: "sentence-transformers/all-MiniLM-L6-v2"
  max_length: 512

# Similarity Settings
similarity:
  threshold: 0.3
  top_k: 10

# File Upload
uploads:
  max_size_mb: 25
  allowed_formats:
    - "pdf"
    - "docx"
    - "txt"
```

---

## System Architecture

### Processing Pipeline

```
Resume File
    ↓
[Resume Parser] → Extract Text
    ↓
[Text Preprocessor] → Clean & Normalize
    ↓
[NER Extractor] → Extract Entities & Skills
    ↓
[BERT Embedding] → Generate Embeddings
    ↓
[Similarity Calculator] → Calculate Scores
    ↓
Ranked Results with Detailed Reports
```

### Module Details

#### 1. **TextPreprocessor** (`preprocessing.py`)
- Text cleaning (URLs, emails, special chars)
- Tokenization and lemmatization
- Stopword removal
- Keyword extraction

#### 2. **NERExtractor** (`ner_extraction.py`)
- Organization extraction
- Education & degree recognition
- Skill pattern matching (100+ tech skills)
- Contact information extraction

#### 3. **BERTEmbedding** (`embedding_generator.py`)
- HuggingFace model loading
- Batch processing support
- GPU acceleration
- Normalization and pooling

#### 4. **SimilarityCalculator** (`similarity_calculator.py`)
- Cosine similarity computation
- Skill-based overlap matching
- Combined weighted scoring
- Candidate ranking

#### 5. **ResumeParser** (`resume_parser.py`)
- PDF parsing with pdfplumber
- DOCX parsing with python-docx
- TXT file reading
- Batch processing

#### 6. **ResumeSceningPipeline** (`pipeline.py`)
- Orchestrates all components
- Manages workflow
- Handles error cases
- Provides unified interface

---

## Understanding the Scores

### Match Score Components

**Semantic Similarity (Default: 60%)**
- BERT-based embedding similarity
- Captures meaning and context
- Ranges from 0 to 1
- Example: Similar job titles, descriptions

**Skill Overlap (Default: 40%)**
- Percentage of required skills found
- Exact keyword matching
- Ranges from 0 to 1
- Example: Python, React, AWS, etc.

### Final Score Interpretation

| Score Range | Rating | Recommendation |
|------------|--------|-----------------|
| 🟢 80-100% | Excellent | Strong candidate, recommend for interview |
| 🟡 60-79%  | Good | Good match, consider for next round |
| 🟠 40-59%  | Moderate | Possible fit, review manually |
| 🔴 <40%    | Weak | Limited match, not recommended |

---

## Advanced Usage

### Custom Model Selection

Use different BERT models for different use cases:

```python
# Lightweight, fast
pipeline = ResumeSceningPipeline(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# More accurate but slower
pipeline = ResumeSceningPipeline(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

# Very accurate
pipeline = ResumeSceningPipeline(
    model_name="sentence-transformers/all-roberta-large-v1"
)
```

### Adjusting Weights

Customize scoring weights based on your needs:

```python
# Prioritize semantic meaning
combined_score = similarity_calculator.calculate_combined_score(
    resume_embedding,
    job_embedding,
    resume_skills,
    job_skills,
    semantic_weight=0.8,  # 80%
    skill_weight=0.2      # 20%
)

# Prioritize skills
combined_score = similarity_calculator.calculate_combined_score(
    resume_embedding,
    job_embedding,
    resume_skills,
    job_skills,
    semantic_weight=0.3,  # 30%
    skill_weight=0.7      # 70%
)
```

### Batch Processing

```python
# Process multiple resumes in one go
resume_files = [
    "candidates/john_doe.pdf",
    "candidates/jane_smith.docx",
    "candidates/bob_wilson.txt"
]

results = pipeline.process_multiple_resumes(
    resume_paths=resume_files,
    job_description="Senior Software Engineer position...",
    top_k=5
)

# Save results
for candidate in results:
    print(f"{candidate['candidate_name']}: {candidate['percentage_match']:.1f}%")
```

---

## Performance Optimization

### For Large-Scale Screening

1. **Use Batch Processing**
   ```python
   # Process embeddings in batches
   embeddings = embedding_generator.get_embeddings_batch(
       texts,
       batch_size=32
   )
   ```

2. **GPU Acceleration**
   ```python
   # Automatic GPU detection
   pipeline = ResumeSceningPipeline(
       model_name="sentence-transformers/all-mpnet-base-v2"
   )
   # Uses CUDA if available
   ```

3. **Caching Results**
   - First run: ~10-30 seconds (model loading)
   - Subsequent runs: ~2-5 seconds
   - Use Streamlit caching: `@st.cache_resource`

### Benchmarks (on CPU)

| Operation | Time |
|-----------|------|
| Model Loading | ~5-10 seconds |
| Single Resume Processing | ~1-2 seconds |
| 100 Resumes Screening | ~2-3 minutes |
| Embedding Generation | ~100ms per text |

---

## Logging and Debugging

### View Logs

```python
import logging

# Set logging level
logging.basicConfig(level=logging.DEBUG)

# Run pipeline
pipeline = ResumeSceningPipeline()
results = pipeline.process_multiple_resumes(
    resume_paths=resume_files,
    job_description=job_desc
)
```

Logs are saved to `resume_screening.log`

### Debug Individual Components

```python
from src.preprocessing import TextPreprocessor
from src.ner_extraction import NERExtractor
from src.embedding_generator import BERTEmbedding

# Test preprocessing
preprocessor = TextPreprocessor()
cleaned = preprocessor.preprocess("Raw resume text here...")

# Test NER
ner = NERExtractor()
entities = ner.extract_all_entities("Resume text...")

# Test embeddings
bert = BERTEmbedding()
embedding = bert.get_embedding("Some text")
```

---

## Troubleshooting

### Problem: spaCy model not found
```bash
python -m spacy download en_core_web_sm
```

### Problem: BERT model download slow
```python
# Use smaller, faster model
pipeline = ResumeSceningPipeline(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

### Problem: PDF parsing fails
```bash
pip install --upgrade pdfplumber
```

### Problem: Out of memory
- Use CPU instead of GPU
- Reduce batch size
- Use smaller model

### Problem: Low match scores
- Ensure resumes are well-formatted
- Use clear skill names
- Adjust weights (increase semantic weight)

---

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

CMD ["streamlit", "run", "app.py"]
```

### Heroku Deployment

```bash
heroku create your-app-name
git push heroku main
```

### Cloud Services

- **AWS**: Use Lambda + S3 for serverless processing
- **Google Cloud**: App Engine for web hosting
- **Azure**: Cognitive Services integration available

---

## API Integration Example

```python
from flask import Flask, request, jsonify
from src.pipeline import ResumeSceningPipeline

app = Flask(__name__)
pipeline = ResumeSceningPipeline()

@app.route('/screen', methods=['POST'])
def screen_resume():
    resume_path = request.json['resume_path']
    job_description = request.json['job_description']
    
    result = pipeline.process_resume(resume_path, job_description)
    
    return jsonify({
        'candidate': result['candidate_name'],
        'match_score': result['percentage_match'],
        'skills': result['matched_required_skills']
    })

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Contributing

Contributions are welcome! Areas for improvement:

- [ ] Support for additional languages
- [ ] Real-time candidate comparison
- [ ] Database integration
- [ ] API enhancements
- [ ] Performance optimizations
- [ ] Additional NLP models

---

## License

This project is provided as-is for educational and commercial use.

---

## Support

For issues, questions, or feature requests, please create an issue or contact the development team.

---

## Acknowledgments

- **spaCy**: Industrial-strength NLP
- **HuggingFace Transformers**: BERT models and utilities
- **Streamlit**: Modern web framework for data apps
- **scikit-learn**: Machine learning utilities

---

## Version History

**v1.0** (2024)
- Initial release
- Complete pipeline implementation
- Web interface
- Production-ready code

---

**Last Updated**: 2024-03-03  
**Status**: Production Ready ✅

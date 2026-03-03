# 📑 COMPLETE PROJECT INDEX

## Project Navigation Guide

This file helps you navigate the entire Resume Screening System project.

---

## 🎯 START HERE

### For First-Time Users
1. **[BUILD_SUMMARY.md](BUILD_SUMMARY.md)** - Project overview (5 min read)
2. **[README.md](README.md)** - Complete documentation (30 min read)
3. Run: `streamlit run app.py`

### For Developers
1. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and diagrams
2. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Commands and code snippets
3. Review: `src/pipeline.py` and other modules

### For Deployment
1. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Cloud deployment guide
2. **[SETUP_WINDOWS.md](SETUP_WINDOWS.md)** - Environment setup

---

## 📁 PROJECT STRUCTURE GUIDE

### Core Application (`src/`)

#### [src/preprocessing.py](src/preprocessing.py) (350+ lines)
**Purpose**: Text cleaning and normalization  
**Key Class**: `TextPreprocessor`  
**Functions**:
- `clean_text()` - Remove URLs, emails, special characters
- `tokenize()` - Split text into tokens
- `lemmatize()` - Normalize word forms
- `remove_stopwords()` - Filter common words
- `preprocess()` - Complete pipeline
- `extract_texts_and_keywords()` - Extract important phrases

**When to Edit**:
- Change text cleaning rules
- Adjust tokenization behavior
- Modify stopword filtering

---

#### [src/ner_extraction.py](src/ner_extraction.py) (400+ lines)
**Purpose**: Named Entity Recognition and skill extraction  
**Key Class**: `NERExtractor`  
**Functions**:
- `extract_organizations()` - Find company names
- `extract_skills()` - Extract technical skills (100+ patterns)
- `extract_education()` - Find degrees and institutions
- `extract_names()` - Extract person names
- `extract_emails()` - Find email addresses
- `extract_phone()` - Find phone numbers
- `extract_all_entities()` - Comprehensive extraction

**When to Edit**:
- Add new skill patterns
- Modify education detection
- Change entity extraction logic

**⭐ IMPORTANT**: To add custom skills, edit the `skill_patterns` list around line 40-45

---

#### [src/embedding_generator.py](src/embedding_generator.py) (300+ lines)
**Purpose**: BERT-based semantic embeddings  
**Key Class**: `BERTEmbedding`  
**Functions**:
- `get_embedding()` - Generate embedding for single text
- `get_embeddings_batch()` - Process multiple texts efficiently
- `get_similarity()` - Calculate similarity between texts
- `get_model_info()` - Return model configuration

**When to Edit**:
- Change BERT model
- Modify pooling strategy
- Adjust batch size
- Enable/disable normalization

**Default Model**: `sentence-transformers/all-MiniLM-L6-v2` (fast, lightweight)  
**Alternative Models**:
- `sentence-transformers/all-mpnet-base-v2` (more accurate)
- `sentence-transformers/all-roberta-large-v1` (highest quality)

---

#### [src/similarity_calculator.py](src/similarity_calculator.py) (350+ lines)
**Purpose**: Scoring and ranking system  
**Key Class**: `SimilarityCalculator`  
**Functions**:
- `cosine_similarity_score()` - Compute vector similarity
- `skill_based_similarity()` - Calculate skill overlap %
- `calculate_combined_score()` - Weighted combination (60% semantic + 40% skills)
- `rank_candidates()` - Sort and rank candidates
- `generate_match_report()` - Create detailed report
- `batch_similarity()` - Compare multiple resumes to one job

**When to Edit**:
- Adjust scoring weights
- Change ranking logic
- Modify report format

**Default Weights**: 60% semantic, 40% skill-based (adjustable)

---

#### [src/resume_parser.py](src/resume_parser.py) (300+ lines)
**Purpose**: Parse resume files in multiple formats  
**Key Class**: `ResumeParser`  
**Functions**:
- `parse_pdf()` - Extract text from PDF files
- `parse_docx()` - Extract text from DOCX files
- `parse_txt()` - Read text files
- `parse_file()` - Auto-detect format and parse
- `batch_parse()` - Process multiple files
- `is_supported_format()` - Validate file format

**Supported Formats**: PDF, DOCX, TXT, DOC  
**Dependencies**: pdfplumber (PDF), python-docx (DOCX)

**When to Edit**:
- Add support for new formats
- Modify text extraction logic
- Change encoding handling

---

#### [src/pipeline.py](src/pipeline.py) (300+ lines)
**Purpose**: Main orchestrator that coordinates all components  
**Key Class**: `ResumeSceningPipeline`  
**Functions**:
- `__init__()` - Initialize pipeline with components
- `extract_text_from_resume()` - Get text from resume file
- `process_resume()` - Screen single resume against job
- `process_multiple_resumes()` - Screen batch of resumes
- `get_pipeline_info()` - Return configuration info

**When to Edit**:
- Modify workflow
- Add preprocessing steps
- Change orchestration logic

**This is the main entry point for programmatic use**

---

#### [src/utils.py](src/utils.py) (400+ lines)
**Purpose**: Utility functions and helpers  
**Classes**:
- `ConfigLoader` - Load YAML configuration
- `FileHelper` - File operations (static methods)
- `PercentageFormatter` - Format scores and ratings

**Key Functions**:
- `setup_logging()` - Configure logging
- `format_percentage()` - Convert score to percentage
- `get_color_code()` - Get color for score
- `get_rating()` - Get rating description

**When to Edit**:
- Change configuration structure
- Modify file operations
- Adjust formatting

---

#### [src/__init__.py](src/__init__.py)
**Purpose**: Make src a Python package  
**Content**: Version and author information  
**Do Not Edit**: Unless updating version

---

### Configuration

#### [config/config.yaml](config/config.yaml)
**Purpose**: System-wide configuration  
**Sections**:
- `spacy` - NLP model selection
- `bert` - BERT model and settings
- `similarity` - Scoring configuration
- `uploads` - File upload rules
- `streamlit` - UI settings
- `ner` - Entity extraction settings
- `logging` - Log configuration

**Edit This For**:
- Changing default model
- Adjusting weights
- Setting file size limits
- Configuring logging

---

### Web Application

#### [app.py](app.py) (700+ lines)
**Purpose**: Streamlit web interface  
**Key Functions**:
- `load_pipeline()` - Load/cache pipeline
- `save_uploaded_files()` - Handle file uploads
- `display_match_score()` - Render result card
- `main()` - Main application logic

**Structure**:
- Sidebar (configuration)
- Tab 1: Screening interface
- Tab 2: About page
- Tab 3: Help page

**When to Edit**:
- Modify UI layout
- Change colors/styling
- Add new features
- Customize sections

**To Run**: `streamlit run app.py`

---

### Documentation

#### [README.md](README.md) (500+ lines)
**Purpose**: Complete project documentation  
**Sections**:
1. Overview and features
2. Technology stack
3. Installation guide
4. Usage instructions
5. Configuration guide
6. System architecture
7. Understanding scores
8. Advanced usage
9. Performance optimization
10. Logging and debugging
11. Troubleshooting
12. Deployment guide
13. API integration
14. Contributing guidelines

**Read This For**: Complete understanding of the system

---

#### [BUILD_SUMMARY.md](BUILD_SUMMARY.md) (400+ lines)
**Purpose**: Project completion summary  
**Contents**:
- What's been built
- Feature checklist
- Technology stack
- Get started guide
- Next steps
- Troubleshooting quick reference

**Read This For**: Quick overview of the project

---

#### [ARCHITECTURE.md](ARCHITECTURE.md) (500+ lines)
**Purpose**: System design and architecture  
**Contents**:
- System architecture diagram
- Data flow diagram
- Module dependency graph
- Class structure
- Scoring system architecture
- File I/O operations
- Configuration hierarchy
- Error handling strategy
- Performance optimization
- Security considerations
- Scalability design
- Monitoring and observability

**Read This For**: Understanding how everything works together

---

#### [DEPLOYMENT.md](DEPLOYMENT.md) (600+ lines)
**Purpose**: Cloud deployment guide  
**Covers**:
1. Local deployment
2. Docker deployment
3. Heroku deployment
4. AWS deployment (EC2, Lambda, Elastic Beanstalk)
5. Google Cloud deployment (Cloud Run)
6. Azure deployment (App Service)
7. Railway deployment
8. Render deployment
9. API deployment (Flask)
10. Kubernetes deployment
11. Production checklist
12. Security considerations
13. Cost estimation

**Read This For**: Deploying to production

---

#### [SETUP_WINDOWS.md](SETUP_WINDOWS.md) (400+ lines)
**Purpose**: Windows-specific setup guide  
**Sections**:
- Quick setup (5-10 minutes)
- Detailed installation
- Running the application
- GPU acceleration setup
- Troubleshooting
- File structure guide
- Support

**Read This For**: Setting up on Windows

---

#### [PROJECT_CHECKLIST.md](PROJECT_CHECKLIST.md) (300+ lines)
**Purpose**: Project completion verification  
**Contents**:
- Implementation status
- Features by category
- Code statistics
- Quality assurance checklist
- Technology stack summary
- Performance metrics
- Testing coverage

**Read This For**: Verifying all features are implemented

---

#### [QUICK_REFERENCE.md](QUICK_REFERENCE.md) (400+ lines)
**Purpose**: Quick lookup reference  
**Contents**:
- Most important commands
- Key file locations
- Quick start (3 steps)
- Common customizations
- Troubleshooting
- Function quick reference
- Configuration reference
- Common use cases
- Debugging tips
- Deployment commands

**Read This For**: Quick answers and code snippets

---

#### [INDEX.md](INDEX.md) (This File)
**Purpose**: Navigate the entire project  
**Contents**:
- File descriptions
- When to read each document
- Where to find things
- Navigation guide

**Read This For**: Finding what you need

---

### Utilities and Setup Scripts

#### [setup_system.py](setup_system.py) (250+ lines)
**Purpose**: Automated system setup wizard  
**Features**:
- Check Python version
- Install dependencies
- Download spaCy model
- Verify installations
- Create directories
- Display instructions

**Usage**: `python setup_system.py`

---

#### [quickstart.py](quickstart.py) (300+ lines)
**Purpose**: Quick system test and validation  
**Features**:
- Create sample files
- Run component tests
- Verify all modules work
- Show next steps

**Usage**: `python quickstart.py`

---

#### [examples.py](examples.py) (400+ lines)
**Purpose**: Usage examples and demonstrations  
**Examples**:
1. Single resume screening
2. Multiple resume screening
3. Job description analysis
4. Candidate comparison
5. Results export

**Usage**: `python examples.py`

---

### Configuration and Ignore Files

#### [requirements.txt](requirements.txt)
**Purpose**: Python dependencies list  
**Contents**: All required packages with versions  
**Usage**: `pip install -r requirements.txt`

**Key Dependencies**:
- spacy (NLP)
- transformers (BERT)
- torch (Deep learning)
- scikit-learn (ML)
- streamlit (Web UI)
- pdfplumber (PDF parsing)
- python-docx (DOCX parsing)
- pandas (Data handling)
- numpy (Numerical computing)

---

#### [.gitignore](.gitignore)
**Purpose**: Specify files to ignore in version control  
**Ignores**:
- Virtual environment
- Python cache files
- IDE files
- Logs
- Uploaded files
- Model files
- OS files

---

### Directories

#### [src/](src/)
**Purpose**: Core application code  
**Contains**: All Python modules  
**Size**: ~2500+ lines of code

#### [config/](config/)
**Purpose**: Configuration files  
**Contains**: config.yaml

#### [uploads/](uploads/)
**Purpose**: Store uploaded resume files  
**Note**: Auto-created, use for temporary uploads

#### [output/](output/)
**Purpose**: Store exported results  
**Note**: Auto-created, for CSV/JSON exports

#### [models/](models/)
**Purpose**: Optional for cached models  
**Note**: Auto-created if needed

---

## 🎯 QUICK NAVIGATION BY TASK

### I want to...

#### ...Get started quickly
→ Read [BUILD_SUMMARY.md](BUILD_SUMMARY.md)  
→ Run `streamlit run app.py`

#### ...Understand the system
→ Read [README.md](README.md)  
→ Review [ARCHITECTURE.md](ARCHITECTURE.md)

#### ...Set up on Windows
→ Follow [SETUP_WINDOWS.md](SETUP_WINDOWS.md)

#### ...Deploy to production
→ Follow [DEPLOYMENT.md](DEPLOYMENT.md)

#### ...Find a command quickly
→ Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

#### ...See code examples
→ Review [examples.py](examples.py)

#### ...Add custom skills
→ Edit [src/ner_extraction.py](src/ner_extraction.py) lines 40-45

#### ...Change scoring weights
→ Use web interface sidebar OR  
→ Edit [config/config.yaml](config/config.yaml)

#### ...Use it as a library
→ Review [examples.py](examples.py)  
→ Import from [src/pipeline.py](src/pipeline.py)

#### ...Debug issues
→ Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) troubleshooting  
→ Run `python quickstart.py`

#### ...Understand the architecture
→ Read [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 📊 PROJECT STATISTICS

| Metric | Value |
|--------|-------|
| Total Files | 17 |
| Core Modules | 8 |
| Lines of Code | 3000+ |
| Documentation Files | 7 |
| Setup/Utility Scripts | 3 |
| Total Lines (with docs) | 6000+ |
| Python Classes | 8 |
| Python Functions | 60+ |
| Comments/Docstrings | Comprehensive |

---

## 🎓 LEARNING PATH

### Beginner
1. Run: `streamlit run app.py`
2. Use web interface
3. Read: [BUILD_SUMMARY.md](BUILD_SUMMARY.md)
4. Read: [README.md](README.md)

### Intermediate
1. Run: `python examples.py`
2. Read: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
3. Explore: [src/pipeline.py](src/pipeline.py)
4. Try: Modify config.yaml

### Advanced
1. Read: [ARCHITECTURE.md](ARCHITECTURE.md)
2. Study: All source files
3. Read: [DEPLOYMENT.md](DEPLOYMENT.md)
4. Deploy to cloud

---

## 🔗 DEPENDENCIES & IMPORTS

### External Libraries Used
- **spacy** (3.7+) - NLP processing
- **transformers** (4.35+) - BERT models
- **torch** (2.0+) - Deep learning
- **scikit-learn** (1.3+) - Similarity metrics
- **streamlit** (1.28+) - Web UI
- **pdfplumber** (0.10+) - PDF parsing
- **python-docx** (0.8+) - DOCX parsing
- **pandas** (2.0+) - Data handling
- **numpy** (1.24+) - Numerical computing
- **PyYAML** (6.0+) - Configuration
- **nltk** (3.8+) - NLP utilities

### Internal Module Imports
```python
from src.preprocessing import TextPreprocessor
from src.ner_extraction import NERExtractor
from src.embedding_generator import BERTEmbedding
from src.similarity_calculator import SimilarityCalculator
from src.resume_parser import ResumeParser
from src.pipeline import ResumeSceningPipeline
from src.utils import ConfigLoader, FileHelper, setup_logging
```

---

## ✅ VERIFICATION CHECKLIST

After setup, verify:
- [ ] All files present (run `ls` or `dir`)
- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] `pip install -r requirements.txt` completed
- [ ] `python -m spacy download en_core_web_sm` completed
- [ ] `streamlit run app.py` starts successfully
- [ ] Web interface opens at http://localhost:8501
- [ ] Sample files exist
- [ ] uploads/ directory exists
- [ ] output/ directory exists

---

## 🚀 NEXT STEPS

1. **[Read This First](BUILD_SUMMARY.md)** - 5 min overview
2. **[Run the App](app.py)** - `streamlit run app.py`
3. **[Read Full Docs](README.md)** - Complete guide
4. **[Customize](config/config.yaml)** - Adjust settings
5. **[Deploy](DEPLOYMENT.md)** - Go to production

---

## 📞 FILE QUICK LOOKUP

```
Need...                          Find in...
────────────────────────────────────────────────────────
Complete documentation          README.md
Quick overview                 BUILD_SUMMARY.md
Setup guide (Windows)          SETUP_WINDOWS.md
Cloud deployment               DEPLOYMENT.md
System architecture            ARCHITECTURE.md
Quick answers                  QUICK_REFERENCE.md
Code examples                  examples.py
Quick test                     quickstart.py
Main web interface             app.py
NLP processing                 src/preprocessing.py
Skill extraction              src/ner_extraction.py
BERT embeddings                src/embedding_generator.py
Scoring system                 src/similarity_calculator.py
Resume parsing                 src/resume_parser.py
Orchestration                  src/pipeline.py
Utilities                      src/utils.py
Configuration                  config/config.yaml
```

---

**Version**: 1.0.0  
**Last Updated**: 2024-03-03  
**Status**: Complete ✅  
**Total Documentation**: Comprehensive

---

**You now have a complete map of the Resume Screening System!**

👉 **Start here**: [BUILD_SUMMARY.md](BUILD_SUMMARY.md)  
👉 **Then run**: `streamlit run app.py`  
👉 **Get details**: [README.md](README.md)

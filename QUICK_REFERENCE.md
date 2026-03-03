# QUICK REFERENCE GUIDE

## 🎯 Most Important Commands

```bash
# SETUP (First time only)
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# RUN WEB INTERFACE (Most common)
streamlit run app.py

# RUN EXAMPLES
python examples.py

# QUICK TEST
python quickstart.py

# AUTOMATED SETUP
python setup_system.py
```

---

## 📁 Key File Locations

| File | Purpose | When to Edit |
|------|---------|--------------|
| `app.py` | Web interface | Customize UI |
| `config/config.yaml` | Settings | Adjust weights, models |
| `src/pipeline.py` | Main orchestrator | Workflow changes |
| `src/ner_extraction.py` | Skill patterns | Add new skills |
| `requirements.txt` | Dependencies | Add new libraries |
| `README.md` | Main documentation | Reference guide |

---

## 🚀 Quick Start (3 steps)

```bash
# 1. Activate environment
.\.venv\Scripts\activate    # Windows
source .venv/bin/activate   # macOS/Linux

# 2. Run app
streamlit run app.py

# 3. Open browser
http://localhost:8501
```

---

## 🔧 Common Customizations

### Change BERT Model
```python
# In app.py, line ~variable
pipeline = load_pipeline("sentence-transformers/all-mpnet-base-v2")
```

### Adjust Scoring Weights
```python
# In web interface sidebar
semantic_weight = 0.7    # Increase importance of semantic matching
skill_weight = 0.3       # Decrease importance of skill matching
```

### Add Custom Skills
```python
# In src/ner_extraction.py, line ~120
r'\b(python|java|your_skill)\b',
```

### Configure Batch Size
```python
# In src/embedding_generator.py
embeddings = self.get_embeddings_batch(texts, batch_size=64)  # Increase for speed
```

---

## 🐛 Quick Troubleshooting

| Problem | Fix |
|---------|-----|
| Module not found | `pip install -r requirements.txt` |
| spaCy error | `python -m spacy download en_core_web_sm` |
| Port 8501 in use | `streamlit run app.py --server.port=8502` |
| BERT slow | Use lighter model in config |
| Memory error | Reduce batch size or use smaller model |
| PDF won't parse | `pip install --upgrade pdfplumber` |

---

## 📊 File Structure Quick Map

```
Resume_Matcher/
├── app.py                    ◄── RUN THIS: streamlit run app.py
├── src/
│   ├── pipeline.py          ◄── Main orchestrator
│   ├── preprocessing.py      ◄── Text cleaning
│   ├── ner_extraction.py     ◄── Skill extraction (edit for custom skills)
│   ├── embedding_generator.py ◄── BERT models
│   ├── similarity_calculator.py
│   ├── resume_parser.py
│   └── utils.py
├── config/
│   └── config.yaml          ◄── EDIT FOR SETTINGS
├── uploads/                 ◄── Resume files go here
└── output/                  ◄── Results exported here
```

---

## 📚 Documentation Map

| Document | Content | Read When |
|----------|---------|-----------|
| README.md | Complete guide | First time |
| SETUP_WINDOWS.md | Windows setup | Windows users |
| DEPLOYMENT.md | Cloud deployment | Before production |
| ARCHITECTURE.md | System design | Want to understand flow |
| PROJECT_CHECKLIST.md | Features list | Verify completeness |
| BUILD_SUMMARY.md | Project overview | Quick overview |
| This file | Quick reference | Need quick answer |

---

## 💻 Function Quick Reference

### Text Preprocessing
```python
from src.preprocessing import TextPreprocessor

preprocessor = TextPreprocessor()
cleaned = preprocessor.preprocess("raw text")
```

### Extract Entities
```python
from src.ner_extraction import NERExtractor

ner = NERExtractor()
entities = ner.extract_all_entities("resume text")
skills = entities['skills']
```

### Generate Embeddings
```python
from src.embedding_generator import BERTEmbedding

bert = BERTEmbedding()
embedding = bert.get_embedding("some text")
similarity = bert.get_similarity("text1", "text2")
```

### Calculate Similarity
```python
from src.similarity_calculator import SimilarityCalculator

calculator = SimilarityCalculator(bert)
score = calculator.calculate_combined_score(emb1, emb2, skills1, skills2)
ranked = calculator.rank_candidates(scores, top_k=10)
```

### Parse Resume
```python
from src.resume_parser import ResumeParser

parser = ResumeParser()
text = parser.parse_file("resume.pdf")
```

### Run Pipeline
```python
from src.pipeline import ResumeSceningPipeline

pipeline = ResumeSceningPipeline()
result = pipeline.process_resume("resume.pdf", "job description")
results = pipeline.process_multiple_resumes(
    ["resume1.pdf", "resume2.docx"],
    "job description",
    top_k=5
)
```

---

## ⚙️ Configuration Quick Reference

```yaml
# Model Selection
bert:
  model_name: "sentence-transformers/all-MiniLM-L6-v2"  # Fast
  # OR
  model_name: "sentence-transformers/all-mpnet-base-v2" # Accurate

# Scoring
similarity:
  threshold: 0.3        # Minimum match score
  top_k: 10            # Results to return

# NLP
spacy:
  model: "en_core_web_sm"  # Standard model
  # OR
  model: "en_core_web_md"  # More accurate but larger
```

---

## 🎯 Common Use Cases

### Use Case 1: Screen Single Resume
```python
from src.pipeline import ResumeSceningPipeline

pipeline = ResumeSceningPipeline()
result = pipeline.process_resume("resume.pdf", job_desc)
print(f"Match: {result['percentage_match']:.1f}%")
```

### Use Case 2: Batch Process Many Resumes
```python
files = ["r1.pdf", "r2.pdf", "r3.pdf"]
results = pipeline.process_multiple_resumes(files, job_desc, top_k=3)
for r in results:
    print(f"{r['candidate_name']}: {r['percentage_match']:.1f}%")
```

### Use Case 3: Analyze Job Description
```python
from src.ner_extraction import NERExtractor

ner = NERExtractor()
entities = ner.extract_all_entities(job_description)
required_skills = entities['skills']
print(f"Skills needed: {required_skills}")
```

### Use Case 4: Custom Scoring
```python
from src.similarity_calculator import SimilarityCalculator

calculator = SimilarityCalculator(bert)
# Custom weights (semantic 70%, skills 30%)
score = calculator.calculate_combined_score(
    emb1, emb2, skills1, skills2,
    semantic_weight=0.7, skill_weight=0.3
)
```

---

## 📦 Dependency Management

```bash
# Install all dependencies
pip install -r requirements.txt

# Install single package
pip install transformers

# Update specific package
pip install --upgrade torch

# Check installed packages
pip list

# Freeze current environment
pip freeze > requirements.txt
```

---

## 🔍 Debugging

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Model Loading
```python
from src.embedding_generator import BERTEmbedding
bert = BERTEmbedding()
info = bert.get_model_info()
print(info)
```

### Test Components
```bash
python quickstart.py  # Quick test of all components
python examples.py    # Run example scripts
```

### View Logs
```bash
tail -f resume_screening.log  # Live log viewing
```

---

## 🌐 Deployment Quick Commands

```bash
# Docker
docker build -t resume-screener .
docker run -p 8501:8501 resume-screener

# Heroku
heroku create appname
git push heroku main

# Google Cloud
gcloud run deploy appname --source .

# AWS
zip -r deployment.zip . && aws lambda update-function-code --zip-file fileb://deployment.zip
```

---

## 📊 Performance Tips

```python
# Use GPU if available
pipeline = ResumeSceningPipeline()  # Auto-detects GPU

# Batch processing for speed
embeddings = bert.get_embeddings_batch(
    texts, 
    batch_size=32  # Increase for faster processing
)

# Cache results to avoid recomputation
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_embed(text):
    return bert.get_embedding(text)

# Use smaller model for speed
"sentence-transformers/all-MiniLM-L6-v2"  # Fast & light
```

---

## 🔐 Security Checklist

- [ ] Validate file formats before processing
- [ ] Set file size limits in config
- [ ] Use secure filenames only
- [ ] Run on HTTPS in production
- [ ] Implement rate limiting
- [ ] Log all operations
- [ ] Sanitize error messages
- [ ] Use environment variables for secrets

---

## 📈 Next Steps

### Immediate (Today)
- [ ] Read README.md
- [ ] Run `streamlit run app.py`
- [ ] Test with sample files

### This Week
- [ ] Customize settings in `config/config.yaml`
- [ ] Add custom skill patterns
- [ ] Test with real resumes

### This Month
- [ ] Deploy to cloud (DEPLOYMENT.md)
- [ ] Set up monitoring
- [ ] Fine-tune scoring weights

### Long-term
- [ ] Gather user feedback
- [ ] Add database integration
- [ ] Create API endpoints
- [ ] Integrate with ATS systems

---

## 🆘 Getting Help

1. **Read Documentation**
   - Start with README.md
   - Check ARCHITECTURE.md for design

2. **Check Examples**
   - Run `python examples.py`
   - Review example code

3. **Debug Issues**
   - Check logs: `resume_screening.log`
   - Run `python quickstart.py` for system test

4. **Modify Code**
   - Refer to file descriptions
   - Use type hints for guidance
   - Check docstrings

---

## ⌨️ Command Cheat Sheet

```bash
# Environment
source .venv/bin/activate              # Activate on Mac/Linux
.\.venv\Scripts\activate               # Activate on Windows

# Dependencies
pip install -r requirements.txt        # Install all
pip install transformers               # Install specific

# Running
streamlit run app.py                   # Web UI
python examples.py                     # Examples
python quickstart.py                   # Quick test
python setup_system.py                 # Automated setup

# Debugging
python -c "import spacy; spacy.load('en_core_web_sm')"  # Test spaCy
python -m spacy download en_core_web_sm                 # Download model

# Deployment
docker build -t resume-screener .      # Build Docker
docker run -p 8501:8501 resume-screener  # Run Docker
```

---

## 📞 Version & Support

**Version**: 1.0.0  
**Status**: Production Ready ✅  
**Last Updated**: 2024-03-03  
**Python Version**: 3.8+  
**Dependencies**: See requirements.txt  

---

## 🎊 Success Checklist

- ✅ Environment set up
- ✅ Dependencies installed
- ✅ spaCy model downloaded
- ✅ Application runs
- ✅ Tested with samples
- ✅ Configuration understood
- ✅ Documentation read
- ✅ Ready to deploy

**You're all set! 🚀**

---

**Remember**: 
- Always read the docs first
- Check examples for patterns
- Use logging for debugging
- Test before production
- Have fun! 🎉

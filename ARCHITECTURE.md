# ARCHITECTURE & SYSTEM DESIGN

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                   RESUME SCREENING SYSTEM ARCHITECTURE              │
└─────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────────┐
                              │   WEB INTERFACE      │
                              │   (Streamlit App)    │
                              └──────────┬───────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
            ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
            │ Job Desc.    │    │ Resume Files │    │ Configuration│
            │ Input        │    │ Upload       │    │ Selection    │
            └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
                   │                   │                   │
                   └───────────────────┼───────────────────┘
                                       │
                                       ▼
                    ┌──────────────────────────────────┐
                    │   RESUME SCREENING PIPELINE      │
                    │   (Orchestrator)                 │
                    └──────────────┬───────────────────┘
                                   │
            ┌──────────────────────┼──────────────────────┐
            │                      │                      │
            ▼                      ▼                      ▼
    ┌─────────────────┐   ┌──────────────────┐   ┌──────────────────┐
    │ Resume Parser   │   │ Text Preprocessor│   │ NER Extractor    │
    ├─────────────────┤   ├──────────────────┤   ├──────────────────┤
    │• PDF parsing    │   │• URL removal     │   │• Organization    │
    │• DOCX parsing   │   │• Email removal   │   │• Skills (100+)   │
    │• TXT reading    │   │• Tokenization    │   │• Education       │
    │• Format detect  │   │• Lemmatization   │   │• Contact info    │
    │• Batch support  │   │• Stopword removal│   │• Email/Phone     │
    └────────┬────────┘   └────────┬─────────┘   └────────┬─────────┘
             │                     │                      │
             └─────────────────────┼──────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────────┐
                    │   BERT Embedding Generator       │
                    ├──────────────────────────────────┤
                    │• HuggingFace model loading       │
                    │• Single & batch processing       │
                    │• GPU acceleration               │
                    │• Embedding normalization         │
                    └────────────┬─────────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │                                 │
                ▼                                 ▼
        ┌──────────────────┐          ┌──────────────────┐
        │Resume Embeddings │          │Job Embeddings    │
        └────────┬─────────┘          └────────┬─────────┘
                 │                             │
                 └──────────────┬──────────────┘
                                │
                                ▼
                    ┌──────────────────────────────────┐
                    │  Similarity Calculator           │
                    ├──────────────────────────────────┤
                    │• Semantic similarity (BERT)      │
                    │• Skill overlap calculation       │
                    │• Weighted combination            │
                    │• Candidate ranking               │
                    │• Report generation               │
                    └────────────┬─────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────────────┐
                    │   RESULTS & RANKING              │
                    ├──────────────────────────────────┤
                    │• Match percentages               │
                    │• Score breakdown                 │
                    │• Skill analysis                  │
                    │• Candidate ranking               │
                    │• Detailed reports                │
                    └────────────┬─────────────────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
            ▼                    ▼                    ▼
    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
    │ Web Display  │    │ CSV Export   │    │ JSON Export  │
    │ Leaderboard  │    │ Results file │    │ Results file │
    │ Visualization│    │              │    │              │
    └──────────────┘    └──────────────┘    └──────────────┘
```

---

## Data Flow Diagram

```
Input Layer:
    Job Description (Text)  ──┐
                              ├──► Resume Screening Pipeline
    Resume Files (PDF/DOCX/TXT) ┘
                              │
                              ▼
Processing Layer:
    ┌─────────────────────────────────────┐
    │ 1. Text Extraction                  │
    │    └─ Parse resume files            │
    └─────────────────────────────────────┘
           │
           ▼
    ┌─────────────────────────────────────┐
    │ 2. Text Cleaning                    │
    │    └─ Remove noise, normalize text  │
    └─────────────────────────────────────┘
           │
           ▼
    ┌─────────────────────────────────────┐
    │ 3. Entity Extraction (Parallel)     │
    │    ├─ Extract Skills                │
    │    ├─ Extract Organizations         │
    │    ├─ Extract Education             │
    │    └─ Extract Contact Info          │
    └─────────────────────────────────────┘
           │
           ▼
    ┌─────────────────────────────────────┐
    │ 4. Embedding Generation (Parallel)  │
    │    ├─ Resume Embedding              │
    │    └─ Job Embedding                 │
    └─────────────────────────────────────┘
           │
           ▼
Scoring Layer:
    ┌─────────────────────────────────────┐
    │ 5. Similarity Calculation           │
    │    ├─ Semantic Similarity (BERT)    │
    │    ├─ Skill Overlap                 │
    │    └─ Combined Score                │
    └─────────────────────────────────────┘
           │
           ▼
Output Layer:
    ┌─────────────────────────────────────┐
    │ 6. Ranking & Report Generation      │
    │    ├─ Rank Candidates               │
    │    ├─ Generate Reports              │
    │    └─ Prepare Visualization         │
    └─────────────────────────────────────┘
           │
           ▼
    Results: Ranked Candidates with Scores
```

---

## Module Dependency Graph

```
app.py (Streamlit Web Interface)
    │
    └── pipeline.py (ResumeSceningPipeline)
            │
            ├── preprocessing.py (TextPreprocessor)
            │       └── spacy
            │
            ├── ner_extraction.py (NERExtractor)
            │       └── spacy
            │
            ├── embedding_generator.py (BERTEmbedding)
            │       ├── transformers
            │       └── torch
            │
            ├── similarity_calculator.py (SimilarityCalculator)
            │       └── scikit-learn
            │
            ├── resume_parser.py (ResumeParser)
            │       ├── pdfplumber
            │       ├── python-docx
            │       └── pathlib
            │
            └── utils.py (Utilities)
                    ├── yaml
                    ├── json
                    └── logging
```

---

## Class Structure

```
TextPreprocessor
├── __init__(model_name)
├── clean_text(text)
├── tokenize(text)
├── lemmatize(text)
├── remove_stopwords(tokens)
├── preprocess(text, remove_stops, lowercase)
└── extract_texts_and_keywords(text)

NERExtractor
├── __init__(model_name)
├── extract_organizations(text)
├── extract_skills(text)
├── extract_education(text)
├── extract_names(text)
├── extract_emails(text)
├── extract_phone(text)
└── extract_all_entities(text)

BERTEmbedding
├── __init__(model_name, device)
├── _mean_pooling(model_output, attention_mask)
├── get_embedding(text, normalize)
├── get_embeddings_batch(texts, normalize, batch_size)
├── get_similarity(text1, text2)
└── get_model_info()

SimilarityCalculator
├── __init__(embedding_generator)
├── cosine_similarity_score(embedding1, embedding2)
├── skill_based_similarity(resume_skills, job_skills)
├── calculate_combined_score(resume_emb, job_emb, ...)
├── rank_candidates(similarity_scores, top_k)
├── generate_match_report(resume_name, combined_score, ...)
└── batch_similarity(resume_embeddings, job_embedding)

ResumeParser
├── __init__()
├── is_supported_format(file_path)
├── parse_pdf(file_path)
├── parse_docx(file_path)
├── parse_txt(file_path, encoding)
├── parse_file(file_path)
└── batch_parse(file_paths)

ResumeSceningPipeline
├── __init__(model_name)
├── extract_text_from_resume(file_path)
├── process_resume(resume_path, job_description)
├── process_multiple_resumes(resume_paths, job_desc, top_k)
└── get_pipeline_info()

ConfigLoader
├── __init__(config_path)
├── _load_config()
├── get(key, default)
└── get_section(section)

FileHelper (static methods)
├── create_directory(path)
├── save_json(data, file_path)
├── load_json(file_path)
├── get_file_name(file_path)
└── get_file_extension(file_path)

PercentageFormatter (static methods)
├── format_percentage(score, decimal_places)
├── get_color_code(score)
└── get_rating(score)
```

---

## Scoring System Architecture

```
COMBINED SCORE CALCULATION
─────────────────────────────────────────────────────────────

Input:
    • Resume Embedding (768-dimensional BERT vector)
    • Job Embedding (768-dimensional BERT vector)
    • Resume Skills (extracted from resume)
    • Job Skills (extracted from job description)

Step 1: Calculate Semantic Similarity
    Resume Embedding ──┐
                      ├──► Cosine Similarity ──► Score: 0-1
    Job Embedding ────┘

Step 2: Calculate Skill Overlap
    Resume Skills ──┐
                    ├──► Calculate Intersection ──► Score: 0-1
    Job Skills ─────┘

Step 3: Weighted Combination
    Semantic Score × 0.6 (default) ──┐
                                      ├──► Combined Score: 0-1
    Skill Score × 0.4 (default) ─────┘

Step 4: Convert to Percentage
    Combined Score × 100 ──► Percentage: 0-100%

Output:
    {
        "overall_score": 0.85,
        "percentage_match": 85.0,
        "semantic_similarity": 0.92,
        "skill_overlap": 0.72,
        "matched_skills": [...],
        "missing_skills": [...]
    }
```

---

## File I/O Operations

```
UPLOAD FLOW:
────────────
User Browser
    │
    ├─ Upload Resume (PDF/DOCX/TXT)
    │
    ▼
app.py (Streamlit)
    │
    ├─ Validate file format
    ├─ Save to ~/uploads/
    │
    ▼
pipeline.py
    │
    ├─ resume_parser.py
    │   ├─ Detect format
    │   ├─ Parse content
    │   └─ Extract text
    │
    ▼
Text Content

EXPORT FLOW:
────────────
Results (In Memory)
    │
    ▼
similarity_calculator.py
    │
    ├─ Format results
    ├─ Create DataFrame
    │
    ▼
app.py (Streamlit)
    │
    ├─ CSV: export_results.csv
    ├─ JSON: export_results.json
    │
    ▼
User Browser
    │
    └─ Download file
```

---

## Configuration Hierarchy

```
System Configuration Sources (Priority Order):
──────────────────────────────────────────────

1. YAML Config File          ◄─── Highest Priority
   └─ config/config.yaml
       ├─ NLP settings
       ├─ Model settings
       ├─ Similarity settings
       └─ File upload settings

2. Python Code Defaults
   └─ Hardcoded in each module
       ├─ Model names
       ├─ Batch sizes
       └─ Thresholds

3. Streamlit UI Settings      ◄─── User Selection
   └─ Sidebar configuration
       ├─ Model choice
       ├─ Weight adjustment
       └─ Results count

Runtime Configuration Resolution:
YAML Config → Python Defaults → Streamlit UI
```

---

## Error Handling Strategy

```
Error Handling Flow:
───────────────────

User Input
    │
    ├─► File Upload
    │   ├─ Validate format
    │   ├─ Check size limit
    │   └─ Handle parse errors
    │
    ├─► Job Description
    │   ├─ Check not empty
    │   └─ Validate length
    │
    ▼
Processing
    ├─ Text extraction
    │   └─ Handle malformed files
    │
    ├─ NLP processing
    │   └─ Handle model errors
    │
    ├─ Embedding generation
    │   └─ Handle CUDA errors
    │
    └─ Similarity calculation
        └─ Handle math errors

Error Response:
    Try Block
        │
        ├─ Execute operation
        │
        ▼
    Except Block
        ├─ Log error
        ├─ Display user-friendly message
        ├─ Fallback to safe default
        └─ Continue execution

Result:
    ✓ User sees error message
    ✓ System logs full traceback
    ✓ Application remains stable
```

---

## Performance Optimization

```
OPTIMIZATION STRATEGIES:
──────────────────────

1. Lazy Loading
   First Import ──► Model Loading ──► Cache in Memory
   Subsequent Use ──► No reload (fast)

2. Batch Processing
   Multiple Texts ──► Process in Batches ──► Faster GPU utilization

3. GPU Acceleration
   Device Detection ──► Auto select CUDA/CPU
   BERT Processing ──► GPU compute (10-30x faster)

4. Caching
   Streamlit @st.cache_resource ──► Load model once per session
   Function results ──► Cache embeddings

5. Vectorization
   Loop (slow) ──► NumPy operations (fast)
   Cosine similarity ──► Use sklearn (optimized)

Expected Performance:
────────────────────
First Run:   10-30 seconds (model loading)
Subsequent:   2-5 seconds (cached models)
100 Resumes:  3-5 minutes (CPU), 1-2 minutes (GPU)
```

---

## Security Considerations

```
Security Architecture:
─────────────────────

Input Validation
    ├─ File format checking
    ├─ File size validation
    ├─ Filename sanitization
    └─ Text length checking

File Handling
    ├─ Temporary directory usage
    ├─ File permission restriction
    ├─ Auto-cleanup after processing
    └─ No direct path exposure

Code Security
    ├─ No eval() or exec()
    ├─ No SQL injection (no database)
    ├─ Input sanitization
    └─ Error message filtering

Deployment Security
    ├─ HTTPS on production
    ├─ Rate limiting (if API)
    ├─ Authentication (if needed)
    └─ CORS configuration
```

---

## Scalability Design

```
Current Architecture: Single Instance
──────────────────────────────────────
[Web Service] ──► [Processing] ──► [Results]

Scaling Strategy 1: Horizontal (Multiple Instances)
───────────────────────────────────────────────────
[Load Balancer]
    │
    ├─► [Service 1] ──► [GPU 1]
    ├─► [Service 2] ──► [GPU 2]
    └─► [Service 3] ──► [GPU 3]

Scaling Strategy 2: Microservices
─────────────────────────────────
[Web UI] ──► [Parser] ──► [Embeddings] ──► [Scoring]

Scaling Strategy 3: Queue-based (Batch Processing)
──────────────────────────────────────────────────
[Upload] ──► [Queue] ──► [Workers] ──► [Results Storage]

Scaling Strategy 4: Distributed (Cloud)
───────────────────────────────────────
[Multi-region] ──► [Auto-scaling] ──► [Load balancing]
```

---

## Monitoring & Observability

```
Logging Architecture:
────────────────────

Module Level Logging
    ├─ preprocessing.py ──► Text processing logs
    ├─ ner_extraction.py ──► Entity extraction logs
    ├─ embedding_generator.py ──► Model loading logs
    ├─ similarity_calculator.py ──► Scoring logs
    ├─ resume_parser.py ──► File parsing logs
    └─ pipeline.py ──► Workflow logs

Log Output
    ├─ Console Output (development)
    └─ File: resume_screening.log (production)

Log Levels:
    ├─ DEBUG: Detailed troubleshooting
    ├─ INFO: General information
    ├─ WARNING: Warning messages
    └─ ERROR: Error messages

Metrics to Monitor:
    ├─ Processing time (per resume)
    ├─ Model load time
    ├─ Error rate
    ├─ GPU utilization
    ├─ Memory usage
    └─ Throughput (resumes/minute)
```

---

**Version**: 1.0.0  
**Date**: 2024-03-03  
**Status**: Complete ✅

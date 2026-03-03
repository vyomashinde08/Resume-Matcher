# DEPLOYMENT GUIDE

## Overview

This guide covers deploying the Resume Screening System to various platforms.

---

## 1. LOCAL DEPLOYMENT (Development)

### Quick Start

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run the application
streamlit run app.py
```

Access at: `http://localhost:8501`

### Configuration for Local

Edit `config/config.yaml`:
```yaml
bert:
  model_name: "sentence-transformers/all-MiniLM-L6-v2"  # Lightweight
```

---

## 2. DOCKER DEPLOYMENT

### Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy application
COPY . .

# Create directories
RUN mkdir -p uploads output

# Expose port
EXPOSE 8501

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  resume-screener:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./uploads:/app/uploads
      - ./output:/app/output
      - ./config:/app/config
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

### Build and Run

```bash
# Build image
docker build -t resume-screener:latest .

# Run container
docker run -p 8501:8501 -v $(pwd)/uploads:/app/uploads resume-screener:latest

# Or use Docker Compose
docker-compose up -d
```

---

## 3. HEROKU DEPLOYMENT

### Setup

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

2. Create `Procfile`:
```
web: streamlit run --logger.level=debug --client.logger.level=debug app.py
```

3. Create `.streamlit/config.toml`:
```toml
[server]
headless = true
port = $PORT
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

### Deploy

```bash
# Login
heroku login

# Create app
heroku create your-unique-app-name

# Push code
git push heroku main

# View logs
heroku logs --tail
```

Access at: `https://your-unique-app-name.herokuapp.com`

### Important Notes

- Heroku has file system limitations (read-only)
- Use cloud storage for uploaded files
- Model downloads may exceed Memory
- Use smaller BERT model

Recommended config for Heroku:

```python
# In app.py, use this model for Heroku
pipeline = load_pipeline("sentence-transformers/all-MiniLM-L6-v2")
```

---

## 4. AWS DEPLOYMENT

### Option A: Elastic Beanstalk

1. **Create `.ebextensions/streamlit.config`**:

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: streamlit_app:application
  aws:elasticbeanstalk:application:environment:
    PYTHONUNBUFFERED: 1

commands:
  01_download_spacy:
    command: "python -m spacy download en_core_web_sm"
```

2. **Deploy**:
```bash
pip install awseb-cli

eb create resume-screener
eb deploy
```

### Option B: Lambda (Serverless)

For batch processing without web UI:

```python
# lambda_function.py
from src.pipeline import ResumeSceningPipeline
import json

pipeline = None

def lambda_handler(event, context):
    global pipeline
    
    if pipeline is None:
        pipeline = ResumeSceningPipeline()
    
    resume_path = event['resume_path']
    job_description = event['job_description']
    
    result = pipeline.process_resume(resume_path, job_description)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'candidate': result['candidate_name'],
            'match_score': result['percentage_match'],
            'skills': result['matched_required_skills']
        })
    }
```

Deploy with:
```bash
sam build
sam deploy
```

### Option C: EC2

1. **Launch EC2 instance**
   - Ubuntu 20.04 LTS
   - t3.medium or larger
   - 8GB RAM minimum

2. **SSH and setup**:
```bash
sudo apt update
sudo apt upgrade
sudo apt install python3-pip python3-venv

git clone your-repo
cd Resume_Matcher

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm

streamlit run app.py
```

3. **Setup Nginx reverse proxy**:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
    }
}
```

---

## 5. GOOGLE CLOUD DEPLOYMENT

### Cloud Run

1. **Create `cloudbuild.yaml`**:

```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/resume-screener', '.']
  
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/resume-screener']
  
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args: ['run', '-f', '.', '-i', 'gcr.io/$PROJECT_ID/resume-screener']
```

2. **Deploy**:
```bash
gcloud builds submit

gcloud run deploy resume-screener \
  --image gcr.io/$PROJECT_ID/resume-screener \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 6. MICROSOFT AZURE DEPLOYMENT

### App Service

1. **Create `requirements.txt`** (already done)

2. **Create deployment config**:

```cmd
# Install Azure CLI
az login

# Create resource group
az group create -n resume-screener -l eastus

# Create App Service plan
az appservice plan create -n resume-screener -g resume-screener --sku B2

# Create web app
az webapp create -n resume-screener -g resume-screener -p resume-screener

# Deploy
az webapp up --name resume-screener
```

---

## 7. RAILWAY DEPLOYMENT

Simply connect your GitHub repo:

1. Sign up at railway.app
2. Create new project
3. Connect GitHub repository
4. Select root directory
5. Auto-deploys on push

Access at: `https://resume-screener.railway.app`

---

## 8. RENDER DEPLOYMENT

1. **Sign up at render.com**
2. **New Web Service**
3. **Connect GitHub**
4. **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
5. **Start Command**: `streamlit run app.py`

---

## 9. API DEPLOYMENT (Optional Flask)

Create `api_app.py`:

```python
from flask import Flask, request, jsonify
from src.pipeline import ResumeSceningPipeline

app = Flask(__name__)
pipeline = ResumeSceningPipeline()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/screen', methods=['POST'])
def screen_resume():
    data = request.json
    resume_path = data['resume_path']
    job_description = data['job_description']
    
    try:
        result = pipeline.process_resume(resume_path, job_description)
        return jsonify({
            'success': True,
            'data': {
                'candidate': result['candidate_name'],
                'match_score': result['percentage_match'],
                'skills': result['matched_required_skills'],
                'missing_skills': result['missing_skills']
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

---

## 10. KUBERNETES DEPLOYMENT

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resume-screener
spec:
  replicas: 2
  selector:
    matchLabels:
      app: resume-screener
  template:
    metadata:
      labels:
        app: resume-screener
    spec:
      containers:
      - name: resume-screener
        image: gcr.io/your-project/resume-screener:latest
        ports:
        - containerPort: 8501
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        env:
        - name: PYTHONUNBUFFERED
          value: "1"
---
apiVersion: v1
kind: Service
metadata:
  name: resume-screener-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8501
  selector:
    app: resume-screener
```

Deploy with:
```bash
kubectl apply -f k8s-deployment.yaml
```

---

## 11. PRODUCTION CHECKLIST

- [ ] Environment variables configured
- [ ] Logging configured
- [ ] Error handling covers all cases
- [ ] HTTPS/SSL enabled
- [ ] Database backups (if using)
- [ ] Upload file limits set
- [ ] Rate limiting configured
- [ ] Security headers added
- [ ] CORS properly configured
- [ ] Monitoring and alerts setup
- [ ] Regular updates scheduled
- [ ] Backup and recovery plan

---

## 12. PERFORMANCE OPTIMIZATION

### For Production

1. **Use larger models** (if resources available):
```python
# More accurate but slower
"sentence-transformers/all-mpnet-base-v2"
```

2. **Enable caching**:
```python
# Cache embeddings
@lru_cache(maxsize=1000)
def get_embedding(text):
    return embedding_generator.get_embedding(text)
```

3. **Use GPU** on cloud providers:
   - AWS EC2 with GPU instance
   - Google Cloud with GPU acceleration
   - Azure with GPU compute

4. **Load balancing**:
   - Multiple instances
   - Distribute requests
   - Use containerization

---

## 13. SECURITY CONSIDERATIONS

1. **File Upload Security**:
```python
# Validate file types
def validate_upload(file):
    allowed = {'pdf', 'docx', 'txt'}
    return file.split('.')[-1] in allowed
```

2. **Rate Limiting**:
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/screen')
@limiter.limit("10 per minute")
def screen():
    ...
```

3. **Input Validation**:
```python
from werkzeug.utils import secure_filename
filename = secure_filename(uploaded_file.filename)
```

---

## 14. MONITORING & LOGGING

### Logs Collection

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### Error Tracking (Sentry)

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

---

## 15. COST ESTIMATION

| Platform | Estimated Cost |
|----------|-----------------|
| Heroku | $50-300/month |
| AWS | $20-200/month |
| Google Cloud | $20-150/month |
| Azure | $30-200/month |
| Railway | $5-50/month |
| Render | Free-100/month |

---

## 📞 Troubleshooting Deployment

| Issue | Solution |
|-------|----------|
| Model too large | Use lighter model, increase RAM |
| Slow startup | Cache models, use cloud storage |
| Memory errors | Reduce batch size, use smaller model |
| Timeout errors | Increase timeout, optimize code |
| File upload fails | Check permissions, increase file size limit |

---

**Quick Deploy Commands Summary**

```bash
# Docker
docker-compose up -d

# Heroku
heroku create app-name && git push heroku main

# AWS
eb create app-name && eb deploy

# Google Cloud
gcloud run deploy app-name

# Railway
git push

# Azure
az webapp up --name app-name
```

---

**Version**: 1.0.0  
**Last Updated**: 2024-03-03  
**Status**: Ready for Production ✅

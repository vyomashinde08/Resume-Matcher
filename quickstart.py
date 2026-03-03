"""
Quick Start Guide for Resume Screening System

This script provides a simple, quick way to get started with the system.
"""

import os
import sys
from pathlib import Path


def print_header(text):
    """Print formatted header."""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print('='*70)


def create_sample_files():
    """Create sample resume and job description files for testing."""
    
    print_header("Creating Sample Files")
    
    # Sample Job Description
    job_desc = """
Senior Python Developer

Location: Remote
Experience: 5+ years
Type: Full-time

About the Role:
We're seeking a Senior Python Developer to join our growing engineering team. 
You'll work on building scalable, high-performance applications for our platform.

Key Responsibilities:
- Design and develop scalable Python applications
- Implement REST APIs and microservices
- Work with machine learning pipelines
- Optimize code for performance
- Mentor junior developers
- Collaborate with cross-functional teams

Required Skills:
- 5+ years of Python development experience
- Strong understanding of Django or Flask
- Proficiency with SQL and NoSQL databases
- Experience with AWS or GCP
- Knowledge of Docker and containerization
- Excellent problem-solving skills
- Strong communication abilities

Preferred Qualifications:
- Experience with Kubernetes
- Machine learning knowledge
- Open source contributions
- Experience with microservices architecture
- RESTful API design expertise

What We Offer:
- Competitive salary and benefits
- Remote work opportunity
- Professional development budget
- Collaborative team environment
"""
    
    with open("sample_job_description.txt", "w") as f:
        f.write(job_desc)
    
    print("✅ Created: sample_job_description.txt")
    
    # Sample Resume
    resume = """
John Smith
Email: john.smith@email.com
Phone: (555) 987-6543
LinkedIn: linkedin.com/in/john-smith

PROFESSIONAL SUMMARY
Experienced Senior Python Developer with 6 years of professional experience
in developing scalable web applications. Proven track record of delivering
high-quality software solutions and leading technical teams.

TECHNICAL SKILLS
Languages: Python, JavaScript, SQL, Bash
Frameworks: Django, Flask, FastAPI
Databases: PostgreSQL, MongoDB, Redis, MySQL
Cloud Services: AWS (EC2, S3, RDS, Lambda), GCP (Compute, Storage)
Tools: Docker, Git, Jenkins, Kubernetes
Other: REST APIs, Microservices, System Design, Problem Solving

PROFESSIONAL EXPERIENCE

Senior Python Developer | TechCorp Inc.
March 2021 - Present
- Led development of microservices architecture serving 1M+ users
- Designed and implemented high-performance REST APIs using FastAPI
- Mentored team of 4 junior developers
- Optimized database queries reducing load time by 45%
- Implemented CI/CD pipelines using Jenkins and Docker
- Technologies: Python, FastAPI, PostgreSQL, Docker, AWS

Python Developer | InnovateSoft
June 2019 - February 2021
- Developed Django-based e-commerce platform
- Implemented real-time notification system using WebSockets
- Migrated legacy code to modern Python practices
- Worked on machine learning model integration
- Technologies: Python, Django, PostgreSQL, Redis, AWS

Junior Developer | StartupXYZ
January 2018 - May 2019
- Built RESTful APIs for mobile applications
- Maintained and enhanced Python backend services
- Participated in agile development process
- Technologies: Python, Flask, SQLite

EDUCATION
Bachelor of Science in Computer Science
State University, Graduated May 2017
GPA: 3.8/4.0

CERTIFICATIONS
- AWS Solutions Architect - Associate (2022)
- Python Professional Development Certificate (2020)

NOTABLE PROJECTS
- Built real-time analytics dashboard using Python and D3.js
- Developed machine learning recommendation system
- Created microservices-based order processing system

ADDITIONAL INFORMATION
- Open source contributor to several Python projects
- Published 3 technical blog posts on Python best practices
- Regular speaker at local Python meetups
"""
    
    with open("sample_resume.txt", "w") as f:
        f.write(resume)
    
    print("✅ Created: sample_resume.txt")


def run_quick_test():
    """Run a quick test of the system."""
    
    print_header("Running Quick Test")
    
    try:
        from src.pipeline import ResumeSceningPipeline
        from src.utils import PercentageFormatter
        
        print("📥 Loading pipeline...")
        pipeline = ResumeSceningPipeline()
        
        print("📄 Reading sample files...")
        with open("sample_resume.txt", "r") as f:
            resume_text = f.read()
        
        with open("sample_job_description.txt", "r") as f:
            job_desc = f.read()
        
        print("🔍 Processing resume...")
        # For quick test, we'll just test the components
        from src.preprocessing import TextPreprocessor
        from src.ner_extraction import NERExtractor
        
        preprocessor = TextPreprocessor()
        ner = NERExtractor()
        
        # Test preprocessing
        cleaned = preprocessor.preprocess(resume_text)
        print(f"✅ Preprocessing successful ({len(cleaned)} chars)")
        
        # Test NER
        entities = ner.extract_all_entities(resume_text)
        print(f"✅ NER extraction successful:")
        print(f"   - Skills found: {len(entities['skills'])}")
        print(f"   - Organizations: {len(entities['organizations'])}")
        
        # Test embeddings
        embeddings = pipeline.embedding_generator.get_embedding(cleaned[:100])
        print(f"✅ Embedding generation successful")
        print(f"   - Embedding dimension: {len(embeddings)}")
        
        print("\n✅ All components working correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Make sure spaCy model is downloaded: python -m spacy download en_core_web_sm")
        print("3. Check Python version (3.8+): python --version")
        return False
    
    return True


def show_next_steps():
    """Show next steps to the user."""
    
    print_header("Next Steps")
    
    print("""
📖 OPTION 1: Web Interface (Recommended for Users)
   Run this command to start the web interface:
   
   streamlit run app.py
   
   Then open your browser to http://localhost:8501

🔧 OPTION 2: Command Line (For Integration)
   1. Modify your resume/job description files
   2. Run the pipeline programmatically:
   
   from src.pipeline import ResumeSceningPipeline
   pipeline = ResumeSceningPipeline()
   result = pipeline.process_resume('your_resume.pdf', 'job description')
   print(f"Match: {result['percentage_match']:.1f}%")

📚 OPTION 3: Run Examples
   See more examples of how to use the system:
   
   python examples.py

📖 Full Documentation
   Read the complete README.md for detailed information

⚙️ Configuration
   Edit config/config.yaml to customize scoring weights and settings
    """)


def main():
    """Main quick start function."""
    
    print_header("Resume Screening System - Quick Start")
    
    print("""
Welcome to the Resume Screening System!

This tool will help you get started quickly by:
1. Creating sample files for testing
2. Running a quick system test
3. Showing you how to proceed
    """)
    
    # Create sample files
    create_sample_files()
    
    # Run quick test
    success = run_quick_test()
    
    if success:
        # Show next steps
        show_next_steps()
    
    print("\n" + "="*70)
    print("✨ Ready to screen resumes! Choose an option above.")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

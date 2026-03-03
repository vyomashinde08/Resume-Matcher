"""
Example usage of the Resume Screening Pipeline

This script demonstrates how to use the pipeline programmatically
for resume screening and candidate ranking.
"""

import logging
from src.pipeline import ResumeSceningPipeline
from src.utils import setup_logging, FileHelper, PercentageFormatter
import json

# Setup logging
setup_logging("INFO")
logger = logging.getLogger(__name__)


def example_single_resume():
    """Example: Screen a single resume against a job description."""
    
    print("\n" + "="*80)
    print("EXAMPLE 1: Single Resume Screening")
    print("="*80 + "\n")
    
    # Initialize pipeline
    pipeline = ResumeSceningPipeline()
    
    # Sample job description
    job_description = """
    Senior Python Developer
    
    Responsibilities:
    - Design and develop scalable Python applications
    - Work with machine learning and NLP libraries
    - Collaborate with data scientists and engineers
    - Optimize code for performance
    
    Requirements:
    - 5+ years Python development experience
    - Strong knowledge of Django or Flask
    - Experience with PostgreSQL and MongoDB
    - Familiarity with AWS and Docker
    - Machine Learning experience preferred
    - Strong problem-solving skills
    
    Nice to have:
    - Experience with Kubernetes
    - Contributions to open-source projects
    - Knowledge of PyTorch or TensorFlow
    """
    
    # For this example, we'll create a sample resume
    sample_resume_text = """
    John Doe
    Email: john.doe@email.com
    Phone: (555) 123-4567
    
    SUMMARY
    Experienced Python developer with 6 years of professional experience in building
    scalable web applications and working with machine learning projects.
    
    TECHNICAL SKILLS
    - Programming Languages: Python, JavaScript, SQL
    - Backend Frameworks: Django, Flask
    - Databases: PostgreSQL, MongoDB, Redis
    - Cloud Services: AWS (EC2, S3, Lambda)
    - DevOps: Docker, CI/CD pipelines, Jenkins
    - Machine Learning: PyTorch, scikit-learn, TensorFlow
    - Tools: Git, Jira, VSCode
    
    PROFESSIONAL EXPERIENCE
    
    Senior Developer | Tech Company
    2021 - Present
    - Led development of machine learning pipeline for recommendation system
    - Designed and implemented REST APIs using Flask
    - Optimized database queries reducing load time by 40%
    - Mentored junior developers
    
    Python Developer | StartUp Inc.
    2018 - 2021
    - Developed Django-based web applications
    - Worked with AWS services for cloud deployment
    - Implemented Docker containerization for microservices
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology, 2018
    
    CERTIFICATIONS
    - AWS Solutions Architect Associate
    - Python Professional Development
    """
    
    # Process resume
    print("Processing resume...")
    result = pipeline.process_resume("sample_resume.txt", job_description)
    
    if result:
        print(f"\n✅ Resume Processed Successfully!\n")
        print(f"Candidate: {result['candidate_name']}")
        print(f"Match Score: {PercentageFormatter.format_percentage(result['percentage_match'])}")
        print(f"Rating: {PercentageFormatter.get_rating(result['overall_score'])}")
        print(f"\nDetailed Breakdown:")
        print(f"  • Semantic Similarity: {result['semantic_similarity']:.1%}")
        print(f"  • Skill Overlap: {result['skill_overlap']:.1%}")
        print(f"\nSkills Analysis:")
        print(f"  • Total Skills Found: {len(result['extracted_skills'])}")
        print(f"  • Matched Required Skills: {result['skill_coverage']}")
        
        if result['matched_required_skills']:
            print(f"\n✅ Matched Skills:")
            for skill in result['matched_required_skills']:
                print(f"    • {skill}")
        
        if result['missing_skills']:
            print(f"\n❌ Missing Skills:")
            for skill in result['missing_skills'][:5]:
                print(f"    • {skill}")
    else:
        print("❌ Failed to process resume")


def example_multiple_resumes():
    """Example: Screen multiple resumes and rank them."""
    
    print("\n" + "="*80)
    print("EXAMPLE 2: Multiple Resume Screening and Ranking")
    print("="*80 + "\n")
    
    # Initialize pipeline
    pipeline = ResumeSceningPipeline()
    
    # Job description
    job_description = """
    Data Scientist
    
    We are looking for an experienced Data Scientist to join our analytics team.
    
    Responsibilities:
    - Build and train machine learning models
    - Analyze large datasets and derive insights
    - Create data visualizations and reports
    - Collaborate with engineers on model deployment
    
    Requirements:
    - 4+ years of data science experience
    - Strong Python programming skills
    - Experience with machine learning frameworks (scikit-learn, TensorFlow, PyTorch)
    - Knowledge of deep learning and NLP
    - Experience with SQL and big data tools
    - Strong statistical background
    
    Preferred:
    - Published research papers
    - Kaggle competitions participation
    - Experience with Apache Spark
    """
    
    # Simulated file paths (in real scenario, these would be actual files)
    # For this example, we'll demonstrate the structure
    print("Simulating multiple resume processing...\n")
    print("Resume Files:")
    resume_files = [
        "candidates/alice_data_scientist.pdf",
        "candidates/bob_ml_engineer.pdf",
        "candidates/carol_analyst.pdf",
        "candidates/david_researcher.pdf",
    ]
    
    for file in resume_files:
        print(f"  • {file}")
    
    print("\nNote: In a real scenario, use actual resume files")
    print("pipeline.process_multiple_resumes(resume_files, job_description, top_k=5)")
    
    print("\nExpected Output Structure:")
    sample_output = {
        "rank": 1,
        "candidate_name": "alice_data_scientist",
        "percentage_match": 92.5,
        "overall_score": 0.925,
        "semantic_similarity": 0.95,
        "skill_overlap": 0.89,
        "matched_required_skills": ["python", "machine learning", "tensorflow", "sql"],
        "missing_skills": ["apache spark"],
        "skill_coverage": "4/5"
    }
    
    import json
    print(json.dumps(sample_output, indent=2))


def example_job_analysis():
    """Example: Analyze job description to extract requirements."""
    
    print("\n" + "="*80)
    print("EXAMPLE 3: Job Description Analysis")
    print("="*80 + "\n")
    
    from src.preprocessing import TextPreprocessor
    from src.ner_extraction import NERExtractor
    
    job_description = """
    Senior Full Stack Developer at Google
    
    Join our team to build amazing products using Python and JavaScript.
    We're looking for an experienced developer with expertise in React, Node.js,
    and AWS. You should have strong knowledge of databases like MongoDB and PostgreSQL.
    
    Requirements:
    - 5+ years of software development experience
    - Expert in JavaScript and Python
    - Deep understanding of REST APIs and microservices
    - Experience with AWS, Docker, and Kubernetes
    - Strong problem-solving skills
    - Experience with React or Vue.js
    
    Nice to have:
    - Machine learning experience with TensorFlow or PyTorch
    - Open source contributions
    - Published technical blog posts
    """
    
    # Extract information
    ner = NERExtractor()
    preprocessor = TextPreprocessor()
    
    print("Analyzing Job Description...\n")
    
    # Extract skills
    skills = ner.extract_skills(job_description)
    print(f"Required Skills Identified ({len(skills)}):")
    for skill in sorted(skills):
        print(f"  • {skill}")
    
    # Preprocess and show cleaned text
    cleaned = preprocessor.preprocess(job_description)
    print(f"\nCleaned Job Description Preview:")
    print(f"  {cleaned[:200]}...")
    
    # Extract organizations
    orgs = ner.extract_organizations(job_description)
    if orgs:
        print(f"\nOrganization: {', '.join(orgs)}")


def example_comparison():
    """Example: Compare multiple candidates side by side."""
    
    print("\n" + "="*80)
    print("EXAMPLE 4: Candidate Comparison")
    print("="*80 + "\n")
    
    from src.utils import PercentageFormatter
    import pandas as pd
    
    # Simulated comparison data
    candidates = [
        {
            "name": "Alice Johnson",
            "match_score": 0.92,
            "matched_skills": 8,
            "total_skills": 9,
            "years_experience": 6
        },
        {
            "name": "Bob Smith",
            "match_score": 0.78,
            "matched_skills": 6,
            "total_skills": 9,
            "years_experience": 4
        },
        {
            "name": "Carol White",
            "match_score": 0.65,
            "matched_skills": 5,
            "total_skills": 9,
            "years_experience": 3
        },
    ]
    
    print("Candidate Comparison Table:\n")
    
    # Create comparison table
    comparison_data = []
    for idx, candidate in enumerate(candidates, 1):
        rating = PercentageFormatter.get_rating(candidate['match_score'])
        percentage = PercentageFormatter.format_percentage(candidate['match_score'])
        
        comparison_data.append({
            "Rank": idx,
            "Candidate": candidate['name'],
            "Match Score": percentage,
            "Rating": rating,
            "Skills": f"{candidate['matched_skills']}/{candidate['total_skills']}",
            "Experience": f"{candidate['years_experience']}y"
        })
    
    df = pd.DataFrame(comparison_data)
    print(df.to_string(index=False))
    
    print("\n" + "-"*80)
    print("Summary:")
    print(f"  • Best Candidate: {candidates[0]['name']} ({PercentageFormatter.format_percentage(candidates[0]['match_score'])})")
    print(f"  • Total Candidates: {len(candidates)}")
    print(f"  • Average Match: {PercentageFormatter.format_percentage(sum(c['match_score'] for c in candidates) / len(candidates))}")


def example_export_results():
    """Example: Export screening results to CSV and JSON."""
    
    print("\n" + "="*80)
    print("EXAMPLE 5: Export Results")
    print("="*80 + "\n")
    
    from src.utils import FileHelper
    
    results = [
        {
            "candidate_name": "Alice Johnson",
            "percentage_match": 92.5,
            "overall_score": 0.925,
            "semantic_similarity": 0.95,
            "skill_overlap": 0.89,
            "matched_required_skills": ["python", "machine learning"],
            "missing_skills": ["spark"],
        },
        {
            "candidate_name": "Bob Smith",
            "percentage_match": 78.0,
            "overall_score": 0.78,
            "semantic_similarity": 0.82,
            "skill_overlap": 0.72,
            "matched_required_skills": ["python"],
            "missing_skills": ["machine learning", "spark"],
        },
    ]
    
    print("Exporting results...\n")
    
    # Save as JSON
    json_file = "output/screening_results.json"
    FileHelper.save_json({"results": results}, json_file)
    print(f"✅ JSON exported to: {json_file}")
    
    # Save as CSV
    import pandas as pd
    export_data = []
    for result in results:
        export_data.append({
            "Candidate": result['candidate_name'],
            "Match %": f"{result['percentage_match']:.1f}",
            "Matched Skills": ', '.join(result['matched_required_skills']),
            "Missing Skills": ', '.join(result['missing_skills']),
        })
    
    df = pd.DataFrame(export_data)
    csv_file = "output/screening_results.csv"
    df.to_csv(csv_file, index=False)
    print(f"✅ CSV exported to: {csv_file}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Resume Screening System - Usage Examples")
    print("="*80)
    
    try:
        # Run examples
        example_single_resume()
        example_multiple_resumes()
        example_job_analysis()
        example_comparison()
        example_export_results()
        
        print("\n" + "="*80)
        print("✅ All examples completed successfully!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        logger.error(f"Example error: {e}", exc_info=True)

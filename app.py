"""
Resume Screening System - Streamlit Web Application

A production-ready web interface for matching resumes with job descriptions using NLP.
"""

import streamlit as st
import pandas as pd
import os
import logging
from pathlib import Path
from typing import List, Optional
import tempfile

# Import pipeline components
from src.pipeline import ResumeSceningPipeline
from src.utils import FileHelper, PercentageFormatter, setup_logging, ConfigLoader

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="Resume Screening System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .match-excellent {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .match-good {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .match-moderate {
        background-color: #ffe5cc;
        border-left: 5px solid #fd7e14;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .match-weak {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_pipeline():
    """Load pipeline with caching."""
    try:
        return ResumeSceningPipeline()
    except Exception as e:
        st.error(f"Failed to load pipeline: {e}")
        st.stop()


def save_uploaded_files(uploaded_files) -> List[str]:
    """Save uploaded files to temporary directory."""
    file_paths = []
    
    for uploaded_file in uploaded_files:
        # Create temp directory if it doesn't exist
        temp_dir = Path("./uploads")
        temp_dir.mkdir(exist_ok=True)
        
        # Save file
        file_path = temp_dir / uploaded_file.name
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        file_paths.append(str(file_path))
        logger.info(f"Saved uploaded file: {file_path}")
    
    return file_paths


def display_match_score(score: dict, idx: int):
    """Display a matched resume with detailed metrics."""
    candidate_name = score['candidate_name']
    percentage = score['percentage_match']
    rating = PercentageFormatter.get_rating(score['overall_score'])
    
    # Determine CSS class based on score
    if percentage >= 80:
        css_class = "match-excellent"
    elif percentage >= 60:
        css_class = "match-good"
    elif percentage >= 40:
        css_class = "match-moderate"
    else:
        css_class = "match-weak"
    
    # Display card
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"""
                <div class='{css_class}'>
                <h3>#{idx + 1} {candidate_name}</h3>
                <p><strong>Overall Match:</strong> {PercentageFormatter.format_percentage(percentage)} | {rating}</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric(
                "Match Score",
                f"{percentage:.1f}%",
                delta=None
            )
        
        with col3:
            st.metric(
                "Skill Overlap",
                score['skill_coverage']
            )
    
    # Display detailed metrics
    with st.expander(f"ℹ️ Details for {candidate_name}"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Semantic Similarity", 
                     f"{score['semantic_similarity']:.2%}")
        with col2:
            st.metric("Skill Overlap Score",
                     f"{score['skill_overlap']:.2%}")
        with col3:
            st.metric("Overall Score",
                     f"{score['overall_score']:.2%}")
        
        # Skills section
        st.subheader("Skills Analysis")
        skill_col1, skill_col2 = st.columns(2)
        
        with skill_col1:
            st.write("**Matched Required Skills:**")
            if score['matched_required_skills']:
                for skill in score['matched_required_skills']:
                    st.write(f"✅ {skill}")
            else:
                st.write("No matched skills found")
        
        with skill_col2:
            st.write("**Missing Skills:**")
            if score['missing_skills']:
                for skill in score['missing_skills']:
                    st.write(f"❌ {skill}")
            else:
                st.write("All required skills present!")
        
        # Additional information
        st.subheader("Additional Information")
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.write("**Contact Information:**")
            if score['contact']['emails']:
                st.write(f"📧 Email: {', '.join(score['contact']['emails'])}")
            if score['contact']['phones']:
                st.write(f"📱 Phone: {', '.join(score['contact']['phones'])}")
        
        with info_col2:
            st.write("**Professional Background:**")
            if score['organizations']:
                st.write(f"🏢 Organizations: {', '.join(score['organizations'][:3])}")
            if score['education']['degrees']:
                st.write(f"🎓 Degrees: {', '.join(score['education']['degrees'][:2])}")
        
        # All extracted skills
        st.write("**All Extracted Skills:**")
        if score['extracted_skills']:
            skills_df = pd.DataFrame({
                "Skill": score['extracted_skills']
            })
            st.dataframe(skills_df, use_container_width=True, hide_index=True)


def main():
    """Main application function."""
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        # Model selection
        model_choice = st.selectbox(
            "Select BERT Model",
            [
                "sentence-transformers/all-MiniLM-L6-v2",
                "sentence-transformers/all-mpnet-base-v2",
                "bert-base-uncased"
            ],
            help="Select the embedding model for similarity calculation"
        )
        
        # Similarity weights
        st.subheader("Similarity Weights")
        semantic_weight = st.slider(
            "Semantic Similarity Weight",
            0.0, 1.0, 0.6,
            help="Weight for BERT embedding similarity"
        )
        skill_weight = st.slider(
            "Skill Overlap Weight",
            0.0, 1.0, 0.4,
            help="Weight for skill matching"
        )
        
        # Results configuration
        st.subheader("Results Configuration")
        top_k = st.slider(
            "Number of Top Candidates to Show",
            1, 20, 10,
            help="Number of best matching resumes to display"
        )
        
        # About section
        st.markdown("---")
        st.subheader("ℹ️ About")
        st.markdown("""
        **Resume Screening System v1.0**
        
        An AI-powered resume matching system using:
        - 🔍 spaCy for NLP & NER
        - 🤖 BERT embeddings for semantic similarity
        - 📊 Cosine similarity for ranking
        
        **How it works:**
        1. Upload resume files (PDF, DOCX, TXT)
        2. Enter job description
        3. System extracts and analyzes
        4. Candidates ranked by match score
        """)
    
    # Main content
    st.title("📄 Resume Screening System")
    st.markdown("### Intelligent Resume-to-Job Matching with NLP")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Screening", "About", "Help"])
    
    with tab1:
        st.markdown("<h2 style='color: #F8FAFC; margin-bottom: 30px;'>🎯 Resume Matching Interface</h2>", unsafe_allow_html=True)
        
        # Job Description Input
        st.markdown("<div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(6, 182, 212, 0.05)); padding: 16px; border-radius: 12px; border-left: 4px solid #3B82F6; margin-bottom: 20px;'><h3 style='color: #60A5FA; margin-top: 0;'>Step 1: Enter Job Description</h3></div>", unsafe_allow_html=True)
        job_description = st.text_area(
            "Paste the job description here:",
            height=200,
            placeholder="Enter job title, responsibilities, requirements, skills needed, etc.",
            key="job_desc"
        )
        
        if not job_description.strip():
            st.info("� Please enter a job description to begin")
        
        # File Upload
        st.markdown("<div style='background: linear-gradient(135deg, rgba(20, 184, 166, 0.05), rgba(34, 197, 94, 0.05)); padding: 16px; border-radius: 12px; border-left: 4px solid #14B8A6; margin-bottom: 20px;'><h3 style='color: #2DD4BF; margin-top: 0;'>Step 2: Upload Resumes</h3></div>", unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "Upload resume files (PDF, DOCX, or TXT):",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            key="resume_files"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully")
        else:
            st.info("📂 Upload one or more resume files to proceed")
        
        # Process button
        if st.button("🚀 Screen Resumes", type="primary", use_container_width=True):
            if not job_description.strip():
                st.error("❌ Please enter a job description")
            elif not uploaded_files:
                st.error("❌ Please upload at least one resume")
            else:
                # Show progress
                with st.spinner("⏳ Loading AI model..."):
                    pipeline = load_pipeline()
                
                # Save uploaded files
                with st.spinner("💾 Processing uploaded files..."):
                    file_paths = save_uploaded_files(uploaded_files)
                
                # Screen resumes
                with st.spinner("🔍 Analyzing resumes and calculating similarity scores..."):
                    try:
                        results = pipeline.process_multiple_resumes(
                            file_paths,
                            job_description,
                            top_k=top_k
                        )
                        
                        if results:
                            st.session_state.results = results
                            st.session_state.job_description = job_description
                            st.session_state.processed = True
                        else:
                            st.error("❌ No valid resumes were processed")
                    except Exception as e:
                        st.error(f"❌ Error during screening: {str(e)}")
                        logger.error(f"Processing error: {e}", exc_info=True)
        
        # Display results
        if st.session_state.get('processed', False):
            st.success("✅ Resume screening complete!")
            
            results = st.session_state.results
            
            # Summary statistics
            st.markdown("<h2 style='color: #F8FAFC; margin-top: 30px; margin-bottom: 20px;'>📊 Summary Statistics</h2>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Resumes Processed", len(results))
            with col2:
                avg_score = sum(r['percentage_match'] for r in results) / len(results)
                st.metric("Average Match Score", f"{avg_score:.1f}%")
            with col3:
                best_score = max(r['percentage_match'] for r in results)
                st.metric("Best Match Score", f"{best_score:.1f}%")
            with col4:
                excellent = sum(1 for r in results if r['percentage_match'] >= 80)
                st.metric("Excellent Matches", excellent)
            
            # Leaderboard
            st.markdown("<h2 style='color: #F8FAFC; margin-top: 30px; margin-bottom: 20px;'>🏆 Top Candidates Leaderboard</h2>", unsafe_allow_html=True)
            
            # Create dataframe for display
            leaderboard_data = []
            for idx, result in enumerate(results[:top_k], 1):
                leaderboard_data.append({
                    "Rank": idx,
                    "Candidate": result['candidate_name'],
                    "Match Score": f"{result['percentage_match']:.1f}%",
                    "Semantic": f"{result['semantic_similarity']:.1%}",
                    "Skills": result['skill_coverage'],
                    "Rating": PercentageFormatter.get_rating(result['overall_score'])
                })
            
            leaderboard_df = pd.DataFrame(leaderboard_data)
            st.dataframe(leaderboard_df, use_container_width=True, hide_index=True)
            
            # Detailed results
            st.markdown("<h2 style='color: #F8FAFC; margin-top: 30px; margin-bottom: 20px;'>📋 Detailed Candidate Analysis</h2>", unsafe_allow_html=True)
            
            for idx, result in enumerate(results[:top_k]):
                display_match_score(result, idx)
            
            # Export option
            st.markdown("<h2 style='color: #F8FAFC; margin-top: 30px; margin-bottom: 20px;'>💾 Export Results</h2>", unsafe_allow_html=True)
            if st.button("📥 Export Results as CSV"):
                export_data = []
                for result in results:
                    export_data.append({
                        "Candidate Name": result['candidate_name'],
                        "Match Percentage": f"{result['percentage_match']:.2f}",
                        "Overall Score": f"{result['overall_score']:.4f}",
                        "Semantic Similarity": f"{result['semantic_similarity']:.4f}",
                        "Skill Overlap": f"{result['skill_overlap']:.4f}",
                        "Skill Coverage": result['skill_coverage'],
                        "Extracted Skills": ', '.join(result['extracted_skills']),
                        "Matched Skills": ', '.join(result['matched_required_skills']),
                        "Missing Skills": ', '.join(result['missing_skills']),
                    })
                
                export_df = pd.DataFrame(export_data)
                csv = export_df.to_csv(index=False)
                
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="resume_screening_results.csv",
                    mime="text/csv"
                )
    
    with tab2:
        st.header("About Resume Screening System")
        
        st.markdown("""
        ## Overview
        
        The **Resume Screening System** is an AI-powered application that automatically
        matches resumes with job descriptions using advanced Natural Language Processing
        and Machine Learning techniques.
        
        ## How It Works
        
        ### 1. **Text Processing**
        - Cleans and normalizes resume and job description text
        - Removes special characters, URLs, and extra whitespace
        - Applies tokenization and lemmatization using spaCy
        - Removes stopwords for better focus on meaningful content
        
        ### 2. **Information Extraction**
        - Extracts key entities: names, organizations, education
        - Identifies technical skills using pattern matching
        - Detects contact information (emails, phone numbers)
        - Recognizes degrees and educational institutions
        
        ### 3. **Semantic Embedding**
        - Generates vector embeddings using BERT models
        - Captures semantic meaning of resume and job description
        - Creates dense representations for similarity comparison
        
        ### 4. **Similarity Scoring**
        - Calculates cosine similarity between embeddings
        - Measures skill overlap percentage
        - Combines metrics for comprehensive matching score
        - Ranks candidates by overall match percentage
        
        ## Key Features
        
        ✅ **Multi-Format Support**: PDF, DOCX, and TXT files
        
        ✅ **NLP-Powered**: Uses spaCy for advanced text processing
        
        ✅ **Deep Learning**: BERT embeddings for semantic understanding
        
        ✅ **Comprehensive Matching**: Combines semantic and skill-based scoring
        
        ✅ **Detailed Analytics**: Skill matching, gap analysis, and insights
        
        ✅ **Production Ready**: Clean code, modular architecture, comprehensive logging
        
        ## Technology Stack
        
        | Component | Technology |
        |-----------|-----------|
        | NLP Processing | spaCy |
        | Embeddings | BERT (HuggingFace Transformers) |
        | Similarity | Scikit-learn (Cosine Similarity) |
        | File Parsing | PyPDF2, python-docx |
        | Web Interface | Streamlit |
        | Data Handling | Pandas, NumPy |
        | Deep Learning | PyTorch |
        """)
    
    with tab3:
        st.header("Help & Guide")
        
        st.markdown("""
        ## Getting Started
        
        ### 1. **Prepare Your Job Description**
        - Copy and paste the complete job description
        - Include title, responsibilities, requirements, and desired skills
        - More detailed descriptions lead to better matching
        
        ### 2. **Upload Resumes**
        - Click "Upload resume files"
        - Select multiple files at once
        - Supported formats: PDF, DOCX, TXT
        - Max file size: 25 MB per file
        
        ### 3. **Configure Matching**
        - Adjust semantic similarity weight (affects BERT-based matching)
        - Adjust skill overlap weight (affects exact skill matching)
        - Set number of top candidates to display
        
        ### 4. **Review Results**
        - Check the leaderboard with top candidates
        - Review detailed analysis for each candidate
        - Look for matched vs. missing skills
        - Export results as CSV for further analysis
        
        ## Understanding Scores
        
        ### Match Score Interpretation
        - **80-100%**: Excellent Match ⭐⭐⭐
        - **60-79%**: Good Match ⭐⭐
        - **40-59%**: Moderate Match ⭐
        - **Below 40%**: Weak Match
        
        ### Score Components
        
        **Semantic Similarity**: How well the resume content matches the job description
        - Uses BERT embeddings
        - Captures meaning, not just keywords
        - Flexible to variations and synonyms
        
        **Skill Overlap**: Percentage of required skills present in resume
        - Based on extracted technical skills
        - Exact keyword matching
        - Shows skill coverage ratio
        
        **Overall Score**: Weighted combination of both components
        - Default: 60% semantic + 40% skills
        - Customizable via sidebar settings
        
        ## Tips for Best Results
        
        1. **Job Description**: Be detailed and specific about requirements
        2. **Resume Format**: Use clean, well-structured resumes
        3. **Skills Section**: Include technical skills explicitly
        4. **Keywords**: Use industry-standard terminology
        5. **Weights**: Adjust weights based on your priorities
        
        ## Troubleshooting
        
        **Problem**: Files not uploading
        - **Solution**: Ensure file format is PDF, DOCX, or TXT
        
        **Problem**: Low match scores overall
        - **Solution**: Check if resume format is accessible; ensure clear skill listing
        
        **Problem**: Missing skills not detected
        - **Solution**: Verify skill names match job description exactly
        
        **Problem**: Slow processing
        - **Solution**: BERT model loading takes time on first run
        
        ## Contact & Support
        
        For issues, suggestions, or questions, please contact the development team.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div class='footer'>
            <p><strong>📄 Resume Screening System v1.0</strong></p>
            <p style='font-size: 0.9rem; margin-top: 8px;'>Powered by spaCy, BERT & Streamlit</p>
            <p style='font-size: 0.8rem; color: #64748B; margin-top: 12px;'>© 2024 All rights reserved</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    # Initialize session state
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    
    main()

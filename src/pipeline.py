"""
Resume Screening Pipeline Module

Main pipeline that orchestrates all components for resume screening.
"""

import logging
import os
from typing import List, Dict, Tuple, Optional
from pathlib import Path

from .preprocessing import TextPreprocessor
from .ner_extraction import NERExtractor
from .embedding_generator import BERTEmbedding
from .similarity_calculator import SimilarityCalculator
from .resume_parser import ResumeParser
from .utils import FileHelper, PercentageFormatter

logger = logging.getLogger(__name__)


class ResumeSceningPipeline:
    """
    Main orchestrator for resume screening system.
    
    Handles the complete workflow:
    1. Parse resume files
    2. Preprocess text
    3. Extract entities
    4. Generate embeddings
    5. Calculate similarity
    6. Rank candidates
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize Resume Screening Pipeline.
        
        Args:
            model_name (str): BERT model name from HuggingFace
        """
        logger.info("Initializing Resume Screening Pipeline...")
        
        # Initialize components
        self.preprocessor = TextPreprocessor()
        self.ner_extractor = NERExtractor()
        self.embedding_generator = BERTEmbedding(model_name)
        self.similarity_calculator = SimilarityCalculator(self.embedding_generator)
        self.resume_parser = ResumeParser()
        
        logger.info("Pipeline initialized successfully")
    
    def extract_text_from_resume(self, file_path: str) -> Optional[str]:
        """
        Extract text from resume file.
        
        Args:
            file_path (str): Path to resume file
            
        Returns:
            Optional[str]: Extracted text or None if failed
        """
        try:
            text = self.resume_parser.parse_file(file_path)
            logger.info(f"Extracted {len(text)} characters from {file_path}")
            return text
        except Exception as e:
            logger.error(f"Failed to extract text from {file_path}: {e}")
            return None
    
    def process_resume(self, resume_path: str, 
                      job_description: str) -> Optional[Dict]:
        """
        Process a single resume against job description.
        
        Args:
            resume_path (str): Path to resume file
            job_description (str): Job description text
            
        Returns:
            Optional[Dict]: Processing results or None if failed
        """
        # Extract text from resume
        resume_text = self.extract_text_from_resume(resume_path)
        if not resume_text:
            return None
        
        # Preprocess both texts
        logger.info("Preprocessing resume and job description...")
        cleaned_resume = self.preprocessor.preprocess(resume_text)
        cleaned_job = self.preprocessor.preprocess(job_description)
        
        # Extract entities from resume
        logger.info("Extracting entities from resume...")
        resume_entities = self.ner_extractor.extract_all_entities(resume_text)
        
        # Extract skills from job description
        logger.info("Extracting skills from job description...")
        job_entities = self.ner_extractor.extract_all_entities(job_description)
        job_skills = job_entities.get('skills', [])
        
        # Generate embeddings
        logger.info("Generating embeddings...")
        resume_embedding = self.embedding_generator.get_embedding(cleaned_resume)
        job_embedding = self.embedding_generator.get_embedding(cleaned_job)
        
        # Calculate similarity
        logger.info("Calculating similarity scores...")
        combined_score = self.similarity_calculator.calculate_combined_score(
            resume_embedding,
            job_embedding,
            resume_entities.get('skills', []),
            job_skills
        )
        
        # Generate report
        candidate_name = FileHelper.get_file_name(resume_path)
        report = self.similarity_calculator.generate_match_report(
            candidate_name,
            combined_score,
            resume_entities,
            job_skills
        )
        
        report['resume_path'] = resume_path
        report['combined_score'] = combined_score
        
        return report
    
    def process_multiple_resumes(self, resume_paths: List[str],
                                job_description: str,
                                top_k: int = 10) -> List[Dict]:
        """
        Process multiple resumes against job description and rank them.
        
        Args:
            resume_paths (List[str]): List of resume file paths
            job_description (str): Job description text
            top_k (int): Number of top candidates to return
            
        Returns:
            List[Dict]: Ranked list of candidates with scores
        """
        logger.info(f"Processing {len(resume_paths)} resumes...")
        
        # Process each resume
        results = []
        for idx, resume_path in enumerate(resume_paths, 1):
            logger.info(f"Processing resume {idx}/{len(resume_paths)}: {resume_path}")
            
            try:
                report = self.process_resume(resume_path, job_description)
                if report:
                    results.append(report)
            except Exception as e:
                logger.error(f"Error processing {resume_path}: {e}")
                continue
        
        # Rank candidates
        logger.info(f"Ranking {len(results)} processed resumes...")
        ranked = self.similarity_calculator.rank_candidates(results, top_k=top_k)
        
        logger.info(f"Processing complete. Top {min(top_k, len(ranked))} candidates returned.")
        
        return ranked
    
    def get_pipeline_info(self) -> Dict:
        """
        Get information about the pipeline configuration.
        
        Returns:
            Dict: Pipeline information
        """
        return {
            "embedding_model": self.embedding_generator.get_model_info(),
            "preprocessor": "spaCy with lemmatization and stopword removal",
            "ner_extractor": "spaCy NER with custom skill patterns",
            "similarity_metric": "Cosine similarity with weighted components",
            "supported_resume_formats": ResumeParser.SUPPORTED_FORMATS,
        }

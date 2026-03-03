"""
Similarity Calculation Module

This module computes similarity scores between resumes and job descriptions
using cosine similarity on BERT embeddings.
"""

import numpy as np
import logging
from typing import Dict, List, Tuple
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class SimilarityCalculator:
    """
    Calculate semantic similarity between resumes and job descriptions.
    
    Features:
        - Cosine similarity calculation
        - Weighted similarity considering skills
        - Ranking of candidates
        - Detailed matching reports
    """
    
    def __init__(self, embedding_generator):
        """
        Initialize Similarity Calculator.
        
        Args:
            embedding_generator: BERTEmbedding instance for generating embeddings
        """
        self.embedding_generator = embedding_generator
        logger.info("Similarity Calculator initialized")
    
    def cosine_similarity_score(self, embedding1: np.ndarray, 
                               embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1 (np.ndarray): First embedding vector
            embedding2 (np.ndarray): Second embedding vector
            
        Returns:
            float: Cosine similarity score (0-1)
        """
        # Ensure embeddings are 2D for sklearn
        emb1 = embedding1.reshape(1, -1)
        emb2 = embedding2.reshape(1, -1)
        
        similarity = cosine_similarity(emb1, emb2)[0][0]
        
        return float(similarity)
    
    def skill_based_similarity(self, resume_skills: List[str], 
                              job_skills: List[str]) -> float:
        """
        Calculate similarity based on skill overlap.
        
        Args:
            resume_skills (List[str]): Skills extracted from resume
            job_skills (List[str]): Skills required for job
            
        Returns:
            float: Skill overlap percentage (0-1)
        """
        if not job_skills:
            return 0.0
        
        resume_skills_set = set(skill.lower().strip() for skill in resume_skills)
        job_skills_set = set(skill.lower().strip() for skill in job_skills)
        
        if not job_skills_set:
            return 0.0
        
        intersection = len(resume_skills_set.intersection(job_skills_set))
        union = len(job_skills_set)
        
        similarity = intersection / union
        
        return float(similarity)
    
    def calculate_combined_score(self, resume_embedding: np.ndarray,
                                job_embedding: np.ndarray,
                                resume_skills: List[str],
                                job_skills: List[str],
                                semantic_weight: float = 0.6,
                                skill_weight: float = 0.4) -> Dict:
        """
        Calculate combined similarity score using semantic and skill-based metrics.
        
        Args:
            resume_embedding (np.ndarray): Resume embedding
            job_embedding (np.ndarray): Job description embedding
            resume_skills (List[str]): Skills from resume
            job_skills (List[str]): Skills from job description
            semantic_weight (float): Weight for semantic similarity (0-1)
            skill_weight (float): Weight for skill similarity (0-1)
            
        Returns:
            Dict: Score breakdown with components and final score
        """
        # Calculate semantic similarity
        semantic_score = self.cosine_similarity_score(resume_embedding, job_embedding)
        
        # Calculate skill-based similarity
        skill_score = self.skill_based_similarity(resume_skills, job_skills)
        
        # Normalize weights
        total_weight = semantic_weight + skill_weight
        semantic_weight = semantic_weight / total_weight
        skill_weight = skill_weight / total_weight
        
        # Calculate combined score
        combined_score = (semantic_score * semantic_weight + 
                         skill_score * skill_weight)
        
        return {
            "semantic_score": float(semantic_score),
            "skill_score": float(skill_score),
            "combined_score": float(combined_score),
            "percentage": float(combined_score * 100),
            "semantic_weight": semantic_weight,
            "skill_weight": skill_weight,
        }
    
    def rank_candidates(self, similarity_scores: List[Dict], 
                       top_k: int = None) -> List[Dict]:
        """
        Rank candidates based on similarity scores.
        
        Args:
            similarity_scores (List[Dict]): List of similarity score dictionaries
            top_k (int): Number of top candidates to return (None for all)
            
        Returns:
            List[Dict]: Ranked candidates with their scores
        """
        # Sort by combined score in descending order
        ranked = sorted(similarity_scores, 
                       key=lambda x: x['combined_score'], 
                       reverse=True)
        
        # Add rank
        for idx, candidate in enumerate(ranked, 1):
            candidate['rank'] = idx
        
        # Return top_k if specified
        if top_k is not None:
            ranked = ranked[:top_k]
        
        logger.info(f"Ranked {len(ranked)} candidates")
        
        return ranked
    
    def generate_match_report(self, resume_name: str,
                             combined_score: Dict,
                             extracted_entities: Dict,
                             job_skills: List[str]) -> Dict:
        """
        Generate a detailed matching report for a resume.
        
        Args:
            resume_name (str): Name of the resume/candidate
            combined_score (Dict): Score breakdown
            extracted_entities (Dict): Extracted entities from resume
            job_skills (List[str]): Required skills from job description
            
        Returns:
            Dict: Detailed matching report
        """
        resume_skills = extracted_entities.get('skills', [])
        matched_skills = [skill for skill in resume_skills if skill in job_skills]
        missing_skills = [skill for skill in job_skills if skill not in resume_skills]
        
        report = {
            "candidate_name": resume_name,
            "overall_score": combined_score['combined_score'],
            "percentage_match": combined_score['percentage'],
            "semantic_similarity": combined_score['semantic_score'],
            "skill_overlap": combined_score['skill_score'],
            "extracted_skills": resume_skills,
            "matched_required_skills": matched_skills,
            "missing_skills": missing_skills,
            "organizations": extracted_entities.get('organizations', []),
            "education": extracted_entities.get('education', {}),
            "contact": {
                "emails": extracted_entities.get('emails', []),
                "phones": extracted_entities.get('phones', []),
            },
            "skill_coverage": f"{len(matched_skills)}/{len(job_skills)}" if job_skills else "N/A",
        }
        
        logger.info(f"Generated report for {resume_name}: {combined_score['percentage']:.2f}%")
        
        return report
    
    def batch_similarity(self, resume_embeddings: np.ndarray,
                        job_embedding: np.ndarray) -> np.ndarray:
        """
        Calculate similarity between multiple resumes and a job description.
        
        Args:
            resume_embeddings (np.ndarray): Array of resume embeddings
            job_embedding (np.ndarray): Job description embedding
            
        Returns:
            np.ndarray: Array of similarity scores
        """
        # Reshape job embedding
        job_embedding = job_embedding.reshape(1, -1)
        
        # Calculate similarities
        similarities = cosine_similarity(resume_embeddings, job_embedding).flatten()
        
        return similarities

"""
Named Entity Recognition and Keyword Extraction Module

This module extracts skills, organizations, education, and other relevant entities
from resumes using spaCy NER and custom patterns.
"""

import re
import spacy
import logging
from typing import Dict, List, Set, Optional

logger = logging.getLogger(__name__)


class NERExtractor:
    """
    Extract named entities and keywords from text using spaCy.
    
    Features:
        - Organization extraction
        - Education extraction
        - Skill extraction using patterns
        - Date/Duration extraction
    """
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initialize NER Extractor.
        
        Args:
            model_name (str): spaCy model name
        """
        try:
            self.nlp = spacy.load(model_name)
            logger.info(f"NER Extractor initialized with model: {model_name}")
        except OSError:
            logger.error(f"Model {model_name} not found")
            raise
        
        # Common skill patterns
        self.skill_patterns = [
            r'\b(python|java|javascript|c\+\+|c#|ruby|php|golang|rust|kotlin)\b',
            r'\b(react|vue|angular|django|flask|spring|node\.?js|express)\b',
            r'\b(sql|mongodb|postgresql|mysql|redis|elasticsearch)\b',
            r'\b(aws|azure|gcp|cloud|docker|kubernetes|devops)\b',
            r'\b(machine learning|deep learning|nlp|computer vision|data science)\b',
            r'\b(rest|graphql|microservices|api|agile|scrum)\b',
            r'\b(html|css|webpack|git|ci\/cd|jenkins|gitlab)\b',
        ]
        
        # Common degree patterns
        self.degree_patterns = [
            r"\b(bachelor|b\.?s\.?|bachelor of science)\b",
            r"\b(master|m\.?s\.?|master of science|mba)\b",
            r"\b(phd|doctorate)\b",
            r"\b(associate|diploma|certificate)\b",
        ]
        
        # Education institution patterns
        self.education_patterns = [
            r"\b(university|college|institute|school|academy)\b",
        ]
    
    def extract_organizations(self, text: str) -> List[str]:
        """
        Extract organization names using spaCy NER.
        
        Args:
            text (str): Input text
            
        Returns:
            List[str]: List of organization names
        """
        doc = self.nlp(text)
        organizations = []
        
        for ent in doc.ents:
            if ent.label_ == "ORG":
                org_name = ent.text.strip()
                if org_name and len(org_name) > 1:
                    organizations.append(org_name)
        
        return list(set(organizations))  # Remove duplicates
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract technical skills using pattern matching.
        
        Args:
            text (str): Input text
            
        Returns:
            List[str]: List of extracted skills
        """
        skills: Set[str] = set()
        text_lower = text.lower()
        
        # Match each skill pattern
        for pattern in self.skill_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                skill = match.group(1).lower()
                skills.add(skill)
        
        # Also extract from noun chunks that might be technologies
        doc = self.nlp(text)
        tech_keywords = ['python', 'java', 'javascript', 'react', 'data', 'analysis', 
                        'management', 'development', 'engineering', 'architecture']
        
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower()
            if any(keyword in chunk_text for keyword in tech_keywords):
                if len(chunk_text) > 1:
                    skills.add(chunk_text)
        
        return sorted(list(skills))
    
    def extract_education(self, text: str) -> Dict[str, List[str]]:
        """
        Extract education information including degrees and institutions.
        
        Args:
            text (str): Input text
            
        Returns:
            Dict[str, List[str]]: Dictionary with 'degrees' and 'institutions' keys
        """
        education_info = {
            "degrees": [],
            "institutions": []
        }
        
        text_lower = text.lower()
        
        # Extract degrees
        for pattern in self.degree_patterns:
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                degree = match.group(0)
                education_info["degrees"].append(degree)
        
        # Extract institutions
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "ORG":
                # Check if it might be educational institution
                entity_text = ent.text.lower()
                if any(keyword in entity_text for keyword in 
                      ['university', 'college', 'institute', 'school', 'academy']):
                    education_info["institutions"].append(ent.text)
        
        # Additional pattern matching for institutions
        for pattern in self.education_patterns:
            # Find context around education keywords
            sentences = text.split('.')
            for sentence in sentences:
                if re.search(pattern, sentence, re.IGNORECASE):
                    # Extract proper nouns from this sentence
                    sentence_doc = self.nlp(sentence)
                    for ent in sentence_doc.ents:
                        if ent.label_ == "ORG":
                            education_info["institutions"].append(ent.text)
        
        # Remove duplicates
        education_info["degrees"] = list(set(education_info["degrees"]))
        education_info["institutions"] = list(set(education_info["institutions"]))
        
        return education_info
    
    def extract_names(self, text: str) -> List[str]:
        """
        Extract person names from text.
        
        Args:
            text (str): Input text
            
        Returns:
            List[str]: List of person names
        """
        doc = self.nlp(text)
        names = []
        
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                names.append(ent.text)
        
        return list(set(names))
    
    def extract_emails(self, text: str) -> List[str]:
        """
        Extract email addresses from text.
        
        Args:
            text (str): Input text
            
        Returns:
            List[str]: List of email addresses
        """
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(pattern, text)
        return list(set(emails))
    
    def extract_phone(self, text: str) -> List[str]:
        """
        Extract phone numbers from text.
        
        Args:
            text (str): Input text
            
        Returns:
            List[str]: List of phone numbers
        """
        pattern = r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b'
        phones = re.findall(pattern, text)
        return [''.join(phone) for phone in phones]
    
    def extract_all_entities(self, text: str) -> Dict[str, any]:
        """
        Extract all entities and information from text.
        
        Args:
            text (str): Input text
            
        Returns:
            Dict: Dictionary containing all extracted entities
        """
        entities = {
            "names": self.extract_names(text),
            "emails": self.extract_emails(text),
            "phones": self.extract_phone(text),
            "organizations": self.extract_organizations(text),
            "skills": self.extract_skills(text),
            "education": self.extract_education(text),
        }
        
        logger.info(f"Extracted entities - Skills: {len(entities['skills'])}, "
                   f"Organizations: {len(entities['organizations'])}, "
                   f"Education: {len(entities['education']['degrees'])} degrees")
        
        return entities

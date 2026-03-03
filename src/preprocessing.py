"""
Text Preprocessing Module

This module handles text cleaning, tokenization, lemmatization, and stopword removal
using spaCy for NLP tasks.
"""

import re
import spacy
import logging
from typing import List, Set, Tuple

logger = logging.getLogger(__name__)


class TextPreprocessor:
    """
    A class for preprocessing text data using spaCy.
    
    Features:
        - Text cleaning (special characters, extra whitespace)
        - Tokenization
        - Lemmatization
        - Stopword removal
    """
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initialize the TextPreprocessor with spaCy model.
        
        Args:
            model_name (str): Name of the spaCy model to load
        """
        try:
            self.nlp = spacy.load(model_name)
            logger.info(f"Successfully loaded spaCy model: {model_name}")
        except OSError:
            logger.error(f"Model {model_name} not found. Download it using: python -m spacy download {model_name}")
            raise
    
    def clean_text(self, text: str) -> str:
        """
        Clean text by removing special characters, URLs, and extra whitespace.
        
        Args:
            text (str): Raw text to clean
            
        Returns:
            str: Cleaned text
        """
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep spaces and basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\-\+\(\)]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into individual tokens.
        
        Args:
            text (str): Text to tokenize
            
        Returns:
            List[str]: List of tokens
        """
        doc = self.nlp(text)
        return [token.text for token in doc]
    
    def lemmatize(self, text: str) -> List[str]:
        """
        Lemmatize text tokens.
        
        Args:
            text (str): Text to lemmatize
            
        Returns:
            List[str]: List of lemmatized tokens
        """
        doc = self.nlp(text)
        return [token.lemma_ for token in doc]
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove stopwords from token list.
        
        Args:
            tokens (List[str]): List of tokens
            
        Returns:
            List[str]: Tokens with stopwords removed
        """
        doc = self.nlp(" ".join(tokens))
        return [token.text for token in doc if not token.is_stop and token.is_alpha]
    
    def preprocess(self, text: str, remove_stops: bool = True, 
                   lowercase: bool = True) -> str:
        """
        Complete preprocessing pipeline: cleaning, tokenization, lemmatization.
        
        Args:
            text (str): Raw text to preprocess
            remove_stops (bool): Whether to remove stopwords
            lowercase (bool): Whether to convert to lowercase
            
        Returns:
            str: Preprocessed text
        """
        # Step 1: Clean text
        text = self.clean_text(text)
        
        # Step 2: Convert to lowercase if needed
        if lowercase:
            text = text.lower()
        
        # Step 3: Process with spaCy
        doc = self.nlp(text)
        
        # Step 4: Filter tokens (lemmatize, remove stops if needed)
        tokens = []
        for token in doc:
            # Skip stopwords if requested
            if remove_stops and token.is_stop:
                continue
            
            # Skip pure punctuation
            if not token.is_punct and token.text.strip():
                tokens.append(token.lemma_.lower())
        
        # Step 5: Remove duplicates while preserving order
        seen: Set[str] = set()
        unique_tokens = []
        for token in tokens:
            if token not in seen:
                unique_tokens.append(token)
                seen.add(token)
        
        return " ".join(unique_tokens)
    
    def extract_texts_and_keywords(self, text: str) -> Tuple[str, List[str]]:
        """
        Extract cleaned text and important keywords/phrases.
        
        Args:
            text (str): Raw text
            
        Returns:
            Tuple[str, List[str]]: Cleaned text and list of keywords
        """
        cleaned = self.preprocess(text)
        
        # Extract noun phrases as keywords
        doc = self.nlp(text)
        keywords = []
        
        for chunk in doc.noun_chunks:
            keyword = chunk.text.lower().strip()
            if len(keyword) > 2:  # Skip very short words
                keywords.append(keyword)
        
        return cleaned, list(set(keywords))

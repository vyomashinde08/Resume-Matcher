"""
BERT Embedding Generation Module

This module generates semantic embeddings for texts using pretrained BERT models
from HuggingFace Transformers.
"""

import torch
import logging
import numpy as np
from typing import List, Union, Tuple
from transformers import AutoTokenizer, AutoModel

logger = logging.getLogger(__name__)


class BERTEmbedding:
    """
    Generate embeddings using pretrained BERT models from HuggingFace.
    
    Features:
        - Lazy loading of models
        - GPU support if available
        - Batch processing
        - Dimension flexibility
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 device: str = None):
        """
        Initialize BERT embedding generator.
        
        Args:
            model_name (str): HuggingFace model identifier
            device (str): Device to use ('cuda', 'cpu', or None for auto-detection)
        """
        self.model_name = model_name
        
        # Auto-detect device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        logger.info(f"Using device: {self.device}")
        
        # Initialize tokenizer and model
        try:
            logger.info(f"Loading tokenizer from {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            logger.info(f"Loading model from {model_name}")
            self.model = AutoModel.from_pretrained(model_name).to(self.device)
            self.model.eval()  # Set to evaluation mode
            
            logger.info(f"Model successfully loaded on {self.device}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def _mean_pooling(self, model_output, attention_mask):
        """
        Mean Pooling - Apply mean pooling attention masks.
        
        Args:
            model_output: Model output tensors
            attention_mask: Attention mask tensor
            
        Returns:
            Pooled embeddings
        """
        # Extract token embeddings
        token_embeddings = model_output[0]
        
        # Expand attention mask
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        
        # Perform mean pooling
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        
        return sum_embeddings / sum_mask
    
    def get_embedding(self, text: str, normalize: bool = True) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text (str): Input text
            normalize (bool): Whether to normalize the embedding
            
        Returns:
            np.ndarray: Embedding vector
        """
        # Tokenize
        encoded_input = self.tokenizer(text, padding=True, truncation=True, 
                                      max_length=512, return_tensors='pt').to(self.device)
        
        # Generate embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        
        # Apply mean pooling
        embeddings = self._mean_pooling(model_output, encoded_input['attention_mask'])
        
        # Normalize embeddings if requested
        if normalize:
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
        
        # Convert to numpy
        return embeddings.cpu().detach().numpy()[0]
    
    def get_embeddings_batch(self, texts: List[str], normalize: bool = True, 
                            batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for multiple texts in batches.
        
        Args:
            texts (List[str]): List of input texts
            normalize (bool): Whether to normalize embeddings
            batch_size (int): Batch size for processing
            
        Returns:
            np.ndarray: Array of embeddings (n_texts, embedding_dim)
        """
        all_embeddings = []
        
        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            
            # Tokenize batch
            encoded_input = self.tokenizer(batch_texts, padding=True, truncation=True,
                                          max_length=512, return_tensors='pt').to(self.device)
            
            # Generate embeddings
            with torch.no_grad():
                model_output = self.model(**encoded_input)
            
            # Apply mean pooling
            embeddings = self._mean_pooling(model_output, encoded_input['attention_mask'])
            
            # Normalize if requested
            if normalize:
                embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            
            # Convert to numpy and accumulate
            all_embeddings.append(embeddings.cpu().detach().numpy())
        
        # Concatenate all batches
        return np.vstack(all_embeddings)
    
    def get_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts.
        
        Args:
            text1 (str): First text
            text2 (str): Second text
            
        Returns:
            float: Similarity score between 0 and 1
        """
        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)
        
        # Calculate cosine similarity
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        
        return float(similarity)
    
    def get_model_info(self) -> dict:
        """
        Get information about the loaded model.
        
        Returns:
            dict: Model information
        """
        return {
            "model_name": self.model_name,
            "device": self.device,
            "embedding_dimension": self.model.config.hidden_size if hasattr(self.model, 'config') else "Unknown",
            "vocab_size": self.tokenizer.vocab_size,
        }

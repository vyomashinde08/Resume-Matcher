"""
Utility Functions and Configuration Loader Module

Helper functions and configuration management for the Resume Screening System.
"""

import os
import yaml
import logging
import json
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Load and manage application configuration."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize Config Loader.
        
        Args:
            config_path (str): Path to configuration YAML file
        """
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), '..', 'config', 'config.yaml'
        )
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Returns:
            Dict: Configuration dictionary
        """
        if not os.path.exists(self.config_path):
            logger.warning(f"Config file not found: {self.config_path}")
            return {}
        
        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
            logger.info(f"Configuration loaded from {self.config_path}")
            return config or {}
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key (str): Configuration key (dot-separated for nested keys)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def get_section(self, section: str) -> Dict:
        """
        Get a configuration section.
        
        Args:
            section (str): Section name
            
        Returns:
            Dict: Section configuration
        """
        return self.config.get(section, {})


class FileHelper:
    """File and directory helper functions."""
    
    @staticmethod
    def create_directory(path: str) -> bool:
        """
        Create directory if it doesn't exist.
        
        Args:
            path (str): Directory path
            
        Returns:
            bool: True if created or already exists
        """
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory created/verified: {path}")
            return True
        except Exception as e:
            logger.error(f"Error creating directory {path}: {e}")
            return False
    
    @staticmethod
    def save_json(data: Dict, file_path: str) -> bool:
        """
        Save dictionary to JSON file.
        
        Args:
            data (Dict): Data to save
            file_path (str): Output file path
            
        Returns:
            bool: True if successful
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2)
            logger.info(f"JSON saved to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
            return False
    
    @staticmethod
    def load_json(file_path: str) -> Optional[Dict]:
        """
        Load dictionary from JSON file.
        
        Args:
            file_path (str): Input file path
            
        Returns:
            Optional[Dict]: Loaded data or None if error
        """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            logger.info(f"JSON loaded from {file_path}")
            return data
        except Exception as e:
            logger.error(f"Error loading JSON: {e}")
            return None
    
    @staticmethod
    def get_file_name(file_path: str) -> str:
        """
        Get file name from path.
        
        Args:
            file_path (str): File path
            
        Returns:
            str: File name without extension
        """
        return Path(file_path).stem
    
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """
        Get file extension.
        
        Args:
            file_path (str): File path
            
        Returns:
            str: File extension
        """
        return Path(file_path).suffix.lower()


class PercentageFormatter:
    """Format percentage scores for display."""
    
    @staticmethod
    def format_percentage(score: float, decimal_places: int = 2) -> str:
        """
        Format a score as percentage.
        
        Args:
            score (float): Score between 0 and 1 (or 0-100)
            decimal_places (int): Number of decimal places
            
        Returns:
            str: Formatted percentage string
        """
        if score <= 1:
            score = score * 100
        
        return f"{score:.{decimal_places}f}%"
    
    @staticmethod
    def get_color_code(score: float) -> str:
        """
        Get color code based on score.
        
        Args:
            score (float): Score between 0 and 1
            
        Returns:
            str: Color code (hex)
        """
        if score >= 0.8:
            return "#28a745"  # Green
        elif score >= 0.6:
            return "#ffc107"  # Yellow
        elif score >= 0.4:
            return "#fd7e14"  # Orange
        else:
            return "#dc3545"  # Red
    
    @staticmethod
    def get_rating(score: float) -> str:
        """
        Get rating based on score.
        
        Args:
            score (float): Score between 0 and 1
            
        Returns:
            str: Rating description
        """
        if score >= 0.9:
            return "Excellent Match ⭐⭐⭐"
        elif score >= 0.7:
            return "Good Match ⭐⭐"
        elif score >= 0.5:
            return "Moderate Match ⭐"
        else:
            return "Weak Match"


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Setup logging configuration.
    
    Args:
        log_level (str): Logging level
        
    Returns:
        logging.Logger: Configured logger
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('resume_screening.log')
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging setup completed with level: {log_level}")
    
    return logger

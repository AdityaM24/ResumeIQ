"""
Text Preprocessing Module

This module handles normalization and cleaning of resume text before parsing.
It removes unnecessary whitespace, normalizes line breaks, and prepares text
for pattern matching and information extraction.
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def normalize_text(text: str) -> str:
    """
    Normalize resume text by fixing whitespace and line breaks.
    
    This function:
    - Collapses multiple newlines into single spaces
    - Removes extra whitespace
    - Strips leading/trailing whitespace
    
    Args:
        text (str): Raw text extracted from resume.
        
    Returns:
        str: Normalized text ready for parsing.
        
    Example:
        >>> raw = "John   Smith\\n\\n\\nPython  Expert"
        >>> clean = normalize_text(raw)
        >>> print(clean)
        "John Smith Python Expert"
    """
    if not text:
        logger.warning("Empty text provided to normalize_text")
        return ""
    
    try:
        # Replace multiple newlines with single space
        text = re.sub(r'\n+', ' ', text)
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        # Strip leading/trailing whitespace
        text = text.strip()
        
        logger.debug(f"Normalized text from {len(text)} to {len(text)} characters")
        return text
        
    except Exception as e:
        logger.error(f"Error normalizing text: {str(e)}")
        return text


def clean_text(text: str, remove_special: bool = False) -> str:
    """
    Advanced text cleaning with optional special character removal.
    
    Args:
        text (str): Text to clean.
        remove_special (bool): If True, removes special characters except punctuation.
        
    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""
    
    text = normalize_text(text)
    
    if remove_special:
        # Keep alphanumeric, whitespace, and basic punctuation
        text = re.sub(r'[^\w\s@\.\-\#\(\)]', '', text)
    
    return text


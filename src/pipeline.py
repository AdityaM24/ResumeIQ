"""
Resume Processing Pipeline Module

This module orchestrates the complete resume processing workflow:
1. Extract text from PDF
2. Preprocess and normalize text
3. Parse and extract structured information

It acts as the main entry point for processing individual resumes.
"""

import os
import logging
from typing import Dict, Any, Optional

from src.extract_text import extract_text_from_pdf
from src.preprocess import normalize_text
from src.parser import parse_resume

logger = logging.getLogger(__name__)


def process_resume(pdf_path: str) -> Optional[Dict[str, Any]]:
    """
    Process a single resume PDF and extract structured information.
    
    This function executes the complete pipeline:
    1. Extract raw text from PDF
    2. Normalize and clean text
    3. Parse structured fields (name, email, skills, education)
    4. Add metadata (filename)
    
    Args:
        pdf_path (str): Full path to the resume PDF file.
        
    Returns:
        Optional[Dict[str, Any]]: Dictionary with parsed resume data and metadata.
            Returns None if processing fails.
            
    Raises:
        ValueError: If pdf_path is invalid or empty.
        
    Example:
        >>> result = process_resume("john_resume.pdf")
        >>> print(result['Name'], result['Skills'])
    """
    try:
        if not pdf_path or not pdf_path.strip():
            raise ValueError("PDF path cannot be empty")
        
        logger.info(f"Processing resume: {pdf_path}")
        
        # Step 1: Extract text from PDF
        logger.debug("Extracting text from PDF...")
        raw_text = extract_text_from_pdf(pdf_path)
        
        if not raw_text or not raw_text.strip():
            logger.warning(f"No text extracted from {pdf_path}")
            return None
        
        # Step 2: Preprocess text
        logger.debug("Preprocessing text...")
        clean_text = normalize_text(raw_text)
        
        # Step 3: Parse resume
        logger.debug("Parsing resume information...")
        parsed_data = parse_resume(clean_text)
        
        # Step 4: Add metadata
        parsed_data["File"] = os.path.basename(pdf_path)
        parsed_data["FilePath"] = os.path.abspath(pdf_path)
        
        logger.info(f"Successfully processed: {os.path.basename(pdf_path)}")
        return parsed_data
        
    except Exception as e:
        logger.error(f"Error processing resume {pdf_path}: {str(e)}")
        return None


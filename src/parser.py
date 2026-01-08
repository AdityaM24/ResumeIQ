"""
Resume Information Extraction Module

This module contains functions for extracting specific fields from resume text
using regex patterns and keyword matching. Each extraction function is specialized
for a particular field (name, email, skills, education, etc.).
"""

import re
import logging
from typing import List, Optional, Dict, Any
from config import SKILLS_KEYWORDS, EDUCATION_KEYWORDS, EMAIL_PATTERN, PHONE_PATTERN

logger = logging.getLogger(__name__)


def extract_name(text: str) -> Optional[str]:
    """
    Extract candidate name from resume text.
    
    Uses a heuristic approach: assumes name appears in first line/beginning.
    Returns first two capitalized words as name.
    
    Args:
        text (str): Normalized resume text.
        
    Returns:
        Optional[str]: Extracted name or None if not found.
        
    Note:
        This is a basic heuristic. For production use, consider using NLP models
        like spaCy for better name entity recognition.
    """
    try:
        # Clean the text and split into words
        first_line = text.split('\n')[0] if '\n' in text else text[:100]
        words = [w.strip() for w in first_line.split() if len(w.strip()) > 1]
        
        # Take first two words that look like names (capitalized or all caps)
        name_words = [w for w in words[:5] if w and (w[0].isupper() or w.isupper())]
        
        if name_words:
            name = " ".join(name_words[:2])
            logger.debug(f"Extracted name: {name}")
            return name
        
        logger.warning("Could not extract name from resume")
        return None
        
    except Exception as e:
        logger.error(f"Error extracting name: {str(e)}")
        return None


def extract_email(text: str) -> Optional[str]:
    """
    Extract email address from resume text.
    
    Args:
        text (str): Resume text.
        
    Returns:
        Optional[str]: Email address or None if not found.
    """
    try:
        match = re.search(EMAIL_PATTERN, text, re.IGNORECASE)
        if match:
            email = match.group(0).lower()
            logger.debug(f"Extracted email: {email}")
            return email
        
        logger.debug("No email found in resume")
        return None
        
    except Exception as e:
        logger.error(f"Error extracting email: {str(e)}")
        return None


def extract_phone(text: str) -> Optional[str]:
    """
    Extract phone number from resume text.
    
    Supports multiple formats:
    - 10-digit: 1234567890
    - Formatted: (123) 456-7890
    - International: +1-123-456-7890
    
    Args:
        text (str): Resume text.
        
    Returns:
        Optional[str]: Phone number or None if not found.
    """
    try:
        match = re.search(PHONE_PATTERN, text)
        if match:
            phone = match.group(0)
            logger.debug(f"Extracted phone: {phone}")
            return phone
        
        logger.debug("No phone number found in resume")
        return None
        
    except Exception as e:
        logger.error(f"Error extracting phone: {str(e)}")
        return None


def extract_education(text: str) -> Optional[str]:
    """
    Extract education qualification from resume text.
    
    Searches for common degree keywords like Bachelor, Master, MBA, etc.
    
    Args:
        text (str): Resume text.
        
    Returns:
        Optional[str]: First matched education degree or None.
    """
    try:
        text_lower = text.lower()
        
        for keyword in EDUCATION_KEYWORDS:
            if keyword.lower() in text_lower:
                logger.debug(f"Extracted education: {keyword}")
                return keyword
        
        logger.debug("No education qualifications found in resume")
        return None
        
    except Exception as e:
        logger.error(f"Error extracting education: {str(e)}")
        return None


def extract_skills(text: str) -> List[str]:
    """
    Extract technical and professional skills from resume text.
    
    Performs case-insensitive matching against a predefined skills database.
    
    Args:
        text (str): Resume text.
        
    Returns:
        List[str]: List of found skills (empty list if none found).
    """
    try:
        text_lower = text.lower()
        found_skills = []
        
        for skill in SKILLS_KEYWORDS:
            if skill.lower() in text_lower and skill not in found_skills:
                found_skills.append(skill)
        
        logger.debug(f"Extracted {len(found_skills)} skills")
        return found_skills
        
    except Exception as e:
        logger.error(f"Error extracting skills: {str(e)}")
        return []


def parse_resume(text: str) -> Dict[str, Any]:
    """
    Parse resume text and extract all structured information.
    
    This is the main entry point for resume parsing. It orchestrates
    the extraction of all individual fields and returns a dictionary
    with the complete structured resume data.
    
    Args:
        text (str): Preprocessed resume text.
        
    Returns:
        Dict[str, Any]: Dictionary containing:
            - Name: Candidate's name
            - Email: Email address
            - Phone: Phone number
            - Education: Primary education degree
            - Skills: List of identified skills
    """
    try:
        logger.debug("Starting resume parsing...")
        
        parsed_data = {
            "Name": extract_name(text),
            "Email": extract_email(text),
            "Phone": extract_phone(text),
            "Education": extract_education(text),
            "Skills": extract_skills(text),
        }
        
        logger.info(f"Successfully parsed resume with {len([v for v in parsed_data.values() if v])} fields")
        return parsed_data
        
    except Exception as e:
        logger.error(f"Error parsing resume: {str(e)}")
        return {
            "Name": None,
            "Email": None,
            "Phone": None,
            "Education": None,
            "Skills": [],
        }


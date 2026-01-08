"""
Resume Parser Package

A robust resume parsing system that extracts and structures candidate information
from PDF resumes.

Example:
    >>> from src.pipeline import process_resume
    >>> result = process_resume("resume.pdf")
    >>> print(result['Skills'])
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from src.pipeline import process_resume

__all__ = ["process_resume"]

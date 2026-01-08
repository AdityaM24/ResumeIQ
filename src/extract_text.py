"""
PDF Text Extraction Module

This module handles extraction of text content from PDF files using PyMuPDF.
It provides robust error handling for corrupted or unusual PDF files.
"""

import logging
from typing import Optional
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a single PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file to extract text from.
        
    Returns:
        str: Extracted text from all pages of the PDF.
        
    Raises:
        FileNotFoundError: If the PDF file does not exist.
        RuntimeError: If PDF extraction fails due to corruption or format issues.
        
    Example:
        >>> text = extract_text_from_pdf("resume.pdf")
        >>> print(f"Extracted {len(text)} characters")
    """
    try:
        if not pdf_path or not pdf_path.strip():
            raise ValueError("PDF path cannot be empty")
            
        text = ""
        with fitz.open(pdf_path) as doc:
            total_pages = len(doc)
            logger.debug(f"Opened PDF with {total_pages} pages: {pdf_path}")
            
            for page_num, page in enumerate(doc, 1):
                try:
                    page_text = page.get_text()
                    text += page_text
                    logger.debug(f"Extracted {len(page_text)} chars from page {page_num}/{total_pages}")
                except Exception as e:
                    logger.warning(f"Error extracting page {page_num}: {str(e)}")
                    continue
        
        logger.info(f"Successfully extracted {len(text)} characters from {pdf_path}")
        return text
        
    except FileNotFoundError as e:
        logger.error(f"PDF file not found: {pdf_path}")
        raise
    except Exception as e:
        logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
        raise RuntimeError(f"Failed to extract text from {pdf_path}: {str(e)}")


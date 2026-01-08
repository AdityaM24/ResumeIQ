"""
Tests for the text extraction module.
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from src.extract_text import extract_text_from_pdf


class TestExtractTextFromPDF:
    """Test suite for extract_text_from_pdf function."""
    
    def test_extract_text_from_valid_pdf(self):
        """Test extraction from a valid PDF file."""
        with patch('src.extract_text.fitz.open') as mock_open:
            # Mock PDF document
            mock_doc = MagicMock()
            mock_page = MagicMock()
            mock_page.get_text.return_value = "Sample resume text"
            mock_doc.__iter__.return_value = [mock_page]
            mock_doc.__enter__.return_value = mock_doc
            mock_doc.__exit__.return_value = None
            mock_open.return_value = mock_doc
            
            result = extract_text_from_pdf("test.pdf")
            
            assert result == "Sample resume text"
            assert isinstance(result, str)
    
    def test_extract_text_empty_path_raises_error(self):
        """Test that empty path raises ValueError."""
        with pytest.raises(ValueError):
            extract_text_from_pdf("")
    
    def test_extract_text_none_path_raises_error(self):
        """Test that None path raises ValueError."""
        with pytest.raises(ValueError):
            extract_text_from_pdf(None)
    
    def test_extract_text_multiple_pages(self):
        """Test extraction from PDF with multiple pages."""
        with patch('src.extract_text.fitz.open') as mock_open:
            mock_doc = MagicMock()
            mock_page1 = MagicMock()
            mock_page2 = MagicMock()
            mock_page1.get_text.return_value = "Page 1 text "
            mock_page2.get_text.return_value = "Page 2 text"
            
            mock_doc.__iter__.return_value = [mock_page1, mock_page2]
            mock_doc.__enter__.return_value = mock_doc
            mock_doc.__exit__.return_value = None
            mock_open.return_value = mock_doc
            
            result = extract_text_from_pdf("multi_page.pdf")
            
            assert "Page 1 text" in result
            assert "Page 2 text" in result
    
    def test_extract_text_file_not_found(self):
        """Test handling of non-existent file."""
        with patch('src.extract_text.fitz.open') as mock_open:
            mock_open.side_effect = FileNotFoundError("File not found")
            
            with pytest.raises(FileNotFoundError):
                extract_text_from_pdf("nonexistent.pdf")

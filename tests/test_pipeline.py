"""
Tests for the resume processing pipeline.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.pipeline import process_resume


class TestProcessResume:
    """Test suite for process_resume function."""
    
    @patch('src.pipeline.parse_resume')
    @patch('src.pipeline.normalize_text')
    @patch('src.pipeline.extract_text_from_pdf')
    def test_process_resume_valid(self, mock_extract, mock_normalize, mock_parse):
        """Test processing of a valid resume."""
        mock_extract.return_value = "Raw text"
        mock_normalize.return_value = "Cleaned text"
        mock_parse.return_value = {
            "Name": "John Smith",
            "Email": "john@example.com",
            "Education": "Bachelor",
            "Skills": ["Python"]
        }
        
        result = process_resume("test.pdf")
        
        assert result is not None
        assert "File" in result
        assert result["Name"] == "John Smith"
        assert result["Email"] == "john@example.com"
        mock_extract.assert_called_once_with("test.pdf")
    
    def test_process_resume_empty_path_raises_error(self):
        """Test that empty path raises ValueError."""
        with pytest.raises(ValueError):
            process_resume("")
    
    def test_process_resume_none_path_raises_error(self):
        """Test that None path raises ValueError."""
        with pytest.raises(ValueError):
            process_resume(None)
    
    @patch('src.pipeline.extract_text_from_pdf')
    def test_process_resume_handles_extraction_error(self, mock_extract):
        """Test handling of extraction errors."""
        mock_extract.side_effect = Exception("Extraction failed")
        
        result = process_resume("test.pdf")
        
        # Should return None on error
        assert result is None

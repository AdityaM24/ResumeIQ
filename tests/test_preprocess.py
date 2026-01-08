"""
Tests for the text preprocessing module.
"""

import pytest
from src.preprocess import normalize_text, clean_text


class TestNormalizeText:
    """Test suite for normalize_text function."""
    
    def test_normalize_multiple_newlines(self):
        """Test that multiple newlines are collapsed."""
        text = "John Smith\n\n\nPython Expert"
        result = normalize_text(text)
        assert "\n" not in result
        assert result == "John Smith Python Expert"
    
    def test_normalize_multiple_spaces(self):
        """Test that multiple spaces are collapsed."""
        text = "John    Smith   Python"
        result = normalize_text(text)
        assert result == "John Smith Python"
    
    def test_normalize_mixed_whitespace(self):
        """Test normalization of mixed whitespace."""
        text = "John  \n  Smith\n\nPython  Expert"
        result = normalize_text(text)
        assert result == "John Smith Python Expert"
    
    def test_normalize_strips_leading_trailing(self):
        """Test that leading/trailing whitespace is removed."""
        text = "  John Smith  "
        result = normalize_text(text)
        assert result == "John Smith"
    
    def test_normalize_empty_string(self):
        """Test normalization of empty string."""
        result = normalize_text("")
        assert result == ""
    
    def test_normalize_whitespace_only(self):
        """Test normalization of whitespace-only string."""
        result = normalize_text("   \n\n   ")
        assert result == ""


class TestCleanText:
    """Test suite for clean_text function."""
    
    def test_clean_text_basic(self):
        """Test basic text cleaning."""
        text = "John   Smith\n\nPython Expert"
        result = clean_text(text)
        assert result == "John Smith Python Expert"
    
    def test_clean_text_remove_special_characters(self):
        """Test removal of special characters."""
        text = "John@Smith#Python$Expert"
        result = clean_text(text, remove_special=True)
        # Should preserve alphanumeric and @ symbol
        assert "John" in result
        assert "Smith" in result
        assert "#" not in result
        assert "$" not in result
    
    def test_clean_text_preserves_email(self):
        """Test that email format is preserved."""
        text = "john@example.com"
        result = clean_text(text, remove_special=True)
        assert "john@example.com" in result

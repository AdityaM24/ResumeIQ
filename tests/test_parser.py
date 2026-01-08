"""
Tests for the resume parser module.
"""

import pytest
from src.parser import (
    extract_name, extract_email, extract_phone,
    extract_education, extract_skills, parse_resume
)


class TestExtractName:
    """Test suite for extract_name function."""
    
    def test_extract_name_basic(self):
        """Test extraction of basic name."""
        text = "John Smith Software Engineer"
        result = extract_name(text)
        assert result is not None
        assert "John" in result
        assert "Smith" in result
    
    def test_extract_name_empty_text(self):
        """Test extraction from empty text."""
        result = extract_name("")
        assert result is None
    
    def test_extract_name_single_word(self):
        """Test extraction with single word."""
        result = extract_name("CEO")
        assert result is None or isinstance(result, str)


class TestExtractEmail:
    """Test suite for extract_email function."""
    
    def test_extract_email_valid(self):
        """Test extraction of valid email."""
        text = "john.smith@example.com"
        result = extract_email(text)
        assert result == "john.smith@example.com"
    
    def test_extract_email_with_text(self):
        """Test extraction from text with email."""
        text = "Contact me at john@company.co.uk for details"
        result = extract_email(text)
        assert result == "john@company.co.uk"
    
    def test_extract_email_not_found(self):
        """Test when no email is found."""
        result = extract_email("No email here")
        assert result is None
    
    def test_extract_email_case_insensitive(self):
        """Test that email extraction is case-insensitive."""
        text = "JOHN@EXAMPLE.COM"
        result = extract_email(text)
        assert result == "john@example.com"


class TestExtractPhone:
    """Test suite for extract_phone function."""
    
    def test_extract_phone_10_digit(self):
        """Test extraction of 10-digit phone."""
        text = "1234567890"
        result = extract_phone(text)
        assert result == "1234567890"
    
    def test_extract_phone_formatted(self):
        """Test extraction of formatted phone."""
        text = "(123) 456-7890"
        result = extract_phone(text)
        assert result is not None
        assert "123" in result
        assert "456" in result
    
    def test_extract_phone_not_found(self):
        """Test when no phone is found."""
        result = extract_phone("No phone number here")
        assert result is None


class TestExtractEducation:
    """Test suite for extract_education function."""
    
    def test_extract_education_bachelor(self):
        """Test extraction of Bachelor degree."""
        text = "Bachelor of Science in Computer Science"
        result = extract_education(text)
        assert result == "Bachelor"
    
    def test_extract_education_master(self):
        """Test extraction of Master degree."""
        text = "Master's degree in Data Science"
        result = extract_education(text)
        assert result == "Master"
    
    def test_extract_education_btech(self):
        """Test extraction of B.Tech degree."""
        text = "B.Tech in Electronics and Communication"
        result = extract_education(text)
        assert result == "B.Tech"
    
    def test_extract_education_not_found(self):
        """Test when no education is found."""
        result = extract_education("High school diploma")
        assert result is None
    
    def test_extract_education_case_insensitive(self):
        """Test case-insensitive matching."""
        text = "bachelor of arts"
        result = extract_education(text)
        assert result == "Bachelor"


class TestExtractSkills:
    """Test suite for extract_skills function."""
    
    def test_extract_skills_multiple(self):
        """Test extraction of multiple skills."""
        text = "Python, SQL, Machine Learning, Pandas"
        result = extract_skills(text)
        assert isinstance(result, list)
        assert "Python" in result
        assert "SQL" in result
        assert len(result) >= 3
    
    def test_extract_skills_case_insensitive(self):
        """Test case-insensitive skill matching."""
        text = "python, PANDAS, machine learning"
        result = extract_skills(text)
        assert "Python" in result
        assert "Pandas" in result
    
    def test_extract_skills_no_duplicates(self):
        """Test that skills are not duplicated."""
        text = "Python Python Python"
        result = extract_skills(text)
        count = result.count("Python")
        assert count <= 1
    
    def test_extract_skills_empty_text(self):
        """Test extraction from text with no skills."""
        result = extract_skills("No skills mentioned")
        assert isinstance(result, list)
        assert len(result) == 0


class TestParseResume:
    """Test suite for parse_resume function."""
    
    def test_parse_resume_complete(self):
        """Test parsing of complete resume."""
        text = """
        John Smith
        john.smith@example.com
        1234567890
        Bachelor of Science in Computer Science
        Python, SQL, Machine Learning, Pandas
        """
        result = parse_resume(text)
        
        assert isinstance(result, dict)
        assert "Name" in result
        assert "Email" in result
        assert "Phone" in result
        assert "Education" in result
        assert "Skills" in result
        assert result["Email"] == "john.smith@example.com"
    
    def test_parse_resume_partial(self):
        """Test parsing of resume with missing fields."""
        text = "John Smith john@example.com"
        result = parse_resume(text)
        
        assert isinstance(result, dict)
        assert result["Email"] == "john@example.com"
        assert "Name" in result
    
    def test_parse_resume_returns_dict(self):
        """Test that parse_resume always returns a dict."""
        result = parse_resume("")
        assert isinstance(result, dict)
        assert "Name" in result
        assert "Email" in result
        assert "Phone" in result
        assert "Education" in result
        assert "Skills" in result

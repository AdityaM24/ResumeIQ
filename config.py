"""
Configuration module for resume parser.

This module contains all configurable constants for the resume parsing system.
Modify these settings to customize behavior without changing core code.
"""

import os
import logging
from typing import List

"""
Configuration module for resume parser.

This module contains all configurable constants for the resume parsing system.
Modify these settings to customize behavior without changing core code.
"""

import os
import logging
from typing import List

# ==============================================================================
# DIRECTORIES
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "data", "raw_resumes")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "processed_output")
OUTPUT_FILE = "parsed_resumes.csv"

# ==============================================================================
# SKILLS DATABASE
# ==============================================================================
SKILLS_KEYWORDS: List[str] = [
    # Programming Languages
    "Python",
    "Java",
    "JavaScript",
    "C++",
    "C#",
    "Go",
    "Rust",
    "PHP",
    "TypeScript",
    
    # Web Frameworks
    "Django",
    "Flask",
    "FastAPI",
    "React",
    "Angular",
    "Vue.js",
    "Node.js",
    "Express",
    
    # Data Science & ML
    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "NLP",
    "Computer Vision",
    
    # Data Tools
    "Pandas",
    "NumPy",
    "SQL",
    "Matplotlib",
    "Seaborn",
    "Plotly",
    
    # Databases
    "MongoDB",
    "PostgreSQL",
    "MySQL",
    "Redis",
    "Elasticsearch",
    
    # Cloud & DevOps
    "AWS",
    "Azure",
    "Google Cloud",
    "Docker",
    "Kubernetes",
    "Jenkins",
    "Git",
    "CI/CD",
    
    # Tools & Platforms
    "Excel",
    "Power BI",
    "Tableau",
    "Jupyter",
    "Linux",
    "Windows",
    "Mac",
    "Postman",
    "REST API",
]

# ==============================================================================
# EDUCATION KEYWORDS
# ==============================================================================
EDUCATION_KEYWORDS: List[str] = [
    "Bachelor",
    "Master",
    "B.Tech",
    "M.Tech",
    "B.E",
    "M.E",
    "MBA",
    "B.Sc",
    "M.Sc",
    "B.A",
    "M.A",
    "B.Com",
    "BCA",
    "MCA",
    "Ph.D",
    "Diploma",
]

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = os.path.join(BASE_DIR, "logs", "resume_parser.log")

# Create logs directory if it doesn't exist
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# ==============================================================================
# PARSER SETTINGS
# ==============================================================================
# Maximum length of text to process (in characters)
MAX_TEXT_LENGTH = 100000

# Whether to stop on first error or continue processing
STOP_ON_ERROR = False

# Email regex pattern
EMAIL_PATTERN = r'[\w\.-]+@[\w\.-]+\.\w+'

# Phone number pattern (US format and international)
PHONE_PATTERN = r'\b\d{10}\b|\+\d{1,3}[-.\s]?\d{10}\b|\(\d{3}\)\s?\d{3}[-.\s]?\d{4}'

# ==============================================================================
# PDF PROCESSING
# ==============================================================================
# Supported file extensions
SUPPORTED_EXTENSIONS = [".pdf"]

# Whether to skip malformed PDFs or raise errors
SKIP_MALFORMED_PDFS = True

# ==============================================================================
# OUTPUT SETTINGS
# ==============================================================================
# Whether to include file path in output
INCLUDE_FILE_PATH = True

# CSV encoding
CSV_ENCODING = "utf-8"

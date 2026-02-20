"""
Resume Information Extraction Module

This module extracts structured information from resume text using the Groq API.
It utilizes LLM reasoning to map unstructured text into a rigid JSON schema.
"""

import os
import json
import logging
from typing import Dict, Any
from groq import Groq

logger = logging.getLogger(__name__)

RESUME_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "skills": {"type": "array", "items": {"type": "string"}},
        "tools": {"type": "array", "items": {"type": "string"}},
        "experience_years": {"type": "number"},
        "domains": {"type": "array", "items": {"type": "string"}},
        "projects": {"type": "array", "items": {"type": "string"}},
        "education": {"type": "array", "items": {"type": "string"}},
        "seniority_indicators": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["name", "email", "skills", "tools", "experience_years", "domains", "projects", "education", "seniority_indicators"]
}

def parse_resume(text: str, api_key: str = "") -> Dict[str, Any]:
    """
    Parse resume text and extract all structured information using an LLM.
    
    Args:
        text (str): Preprocessed resume text.
        api_key (str): Optional API key from user request.
        
    Returns:
        Dict[str, Any]: Structured resume representation.
    """
    key_to_use = api_key if api_key else os.environ.get("GROQ_API_KEY")
    
    fallback_data = {
        "name": None, "email": None, "skills": [], "tools": [],
        "experience_years": 0, "domains": [], "projects": [],
        "education": [], "seniority_indicators": []
    }
    
    if not key_to_use:
        logger.warning("GROQ_API_KEY not found. Returning empty fallback data.")
        return fallback_data
        
    try:
        logger.info("Extracting structured resume data via Groq API...")
        client = Groq(api_key=key_to_use)
        
        prompt = f"""
        Extract the following resume into a structured JSON format according to this exact schema:
        {json.dumps(RESUME_SCHEMA)}
        
        Resume Text:
        {text[:5000]} # Truncated
        
        Provide ONLY valid JSON.
        """
        
        # We use llama3-8b-8192 which is very fast and capable of JSON if prompted correctly.
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a JSON extractor. Output ONLY valid JSON containing the requested schema. No markdown wrapping, no conversational text."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant", # LLaMA 3.1 is better at following JSON constraints
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        
        result_json = chat_completion.choices[0].message.content
        parsed_data = json.loads(result_json)
        logger.info("Successfully parsed resume structure via LLM.")
        return parsed_data
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode LLM JSON for resume: {str(e)}")
        return fallback_data
    except Exception as e:
        logger.error(f"Error parsing resume via Groq: {str(e)}")
        return fallback_data

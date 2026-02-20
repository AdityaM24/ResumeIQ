"""
Job Description Parser Module

This module extracts structured entities from Job Description (JD) text using Groq LLM.
"""

import os
import json
import logging
from typing import Dict, Any
from groq import Groq

logger = logging.getLogger(__name__)

JD_SCHEMA = {
    "type": "object",
    "properties": {
        "required_skills": {"type": "array", "items": {"type": "string"}},
        "preferred_skills": {"type": "array", "items": {"type": "string"}},
        "required_tools": {"type": "array", "items": {"type": "string"}},
        "experience_years": {"type": "number"},
        "domain": {"type": "string"},
        "seniority_level": {"type": "string"}
    },
    "required": ["required_skills", "preferred_skills", "required_tools", "experience_years", "domain", "seniority_level"]
}

def parse_jd(text: str, api_key: str = "") -> Dict[str, Any]:
    """
    Parse Job Description text and extract structured requirements via LLM.
    
    Args:
        text (str): Job Description raw or preprocessed text.
        api_key (str): Optional API key.
        
    Returns:
        Dict[str, Any]: Dictionary containing structured JD data.
    """
    key_to_use = api_key if api_key else os.environ.get("GROQ_API_KEY")
    
    fallback_data = {
        "required_skills": [],
        "preferred_skills": [],
        "required_tools": [],
        "experience_years": 0.0,
        "domain": "Unknown",
        "seniority_level": "Unknown"
    }
    
    if not key_to_use:
        logger.warning("GROQ_API_KEY not found. Returning empty fallback data for JD.")
        return fallback_data
        
    try:
        logger.info("Extracting structured JD data via Groq API...")
        client = Groq(api_key=key_to_use)
        
        prompt = f"""
        Extract the following job description into a structured JSON format according to this exact schema:
        {json.dumps(JD_SCHEMA)}
        
        Job Description:
        {text[:5000]} # Truncated
        
        Provide ONLY valid JSON.
        """
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a JSON extractor. Output ONLY valid JSON containing the requested schema. No markdown wrapping, no conversational text."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        
        result_json = chat_completion.choices[0].message.content
        parsed_data = json.loads(result_json)
        logger.info("Successfully parsed JD structure via LLM.")
        return parsed_data
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode LLM JSON for JD: {str(e)}")
        return fallback_data
    except Exception as e:
        logger.error(f"Error parsing JD via Groq: {str(e)}")
        return fallback_data

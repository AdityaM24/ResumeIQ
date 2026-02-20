import os
import json
import logging
from typing import Dict, Any, List
from groq import Groq

logger = logging.getLogger(__name__)

SUGGESTIONS_SCHEMA = {
    "type": "object",
    "properties": {
        "missing_skills_importance": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "skill": {"type": "string"},
                    "importance": {"type": "string", "enum": ["High", "Medium", "Low"]}
                }
            }
        },
        "match_summary": {"type": "string"},
        "top_5_improvements": {
            "type": "array",
            "items": {"type": "string"},
            "maxItems": 5
        },
        "rewrite_examples": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "original": {"type": "string"},
                    "rewritten": {"type": "string"}
                }
            }
        },
        "keywords_to_include": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["missing_skills_importance", "match_summary", "top_5_improvements", "rewrite_examples", "keywords_to_include"]
}

def generate_improvement_suggestions(
    resume_json: Dict[str, Any],
    jd_json: Dict[str, Any],
    score_breakdown: Dict[str, Any],
    api_key: str = ""
) -> Dict[str, Any]:
    """
    FR5, FR6 & FR7: LLM-Based Improvement Suggestions & Explainability
    Retrieves a dense JSON structure of actionable rewrite advice based on the ATS score deficit.
    """
    key_to_use = api_key if api_key else os.environ.get("GROQ_API_KEY")
    
    fallback = {
        "missing_skills_importance": [],
        "match_summary": "AI Suggestions unavailable. Please provide a Groq API Key.",
        "top_5_improvements": [],
        "rewrite_examples": [],
        "keywords_to_include": []
    }
    
    if not key_to_use:
        logger.warning("GROQ_API_KEY not found. Skipping LLM suggestions.")
        return fallback
        
    try:
        client = Groq(api_key=key_to_use)
        
        prompt = f"""
        You are an expert ATS (Applicant Tracking System) intelligence engine.
        Analyze the candidate's parsed resume and the target JD. 
        
        Resume Data:
        {json.dumps(resume_json)}
        
        Job Description Data:
        {json.dumps(jd_json)}
        
        Match Score Breakdown:
        {json.dumps(score_breakdown)}
        
        Output highly actionable, strictly structured JSON according to this schema:
        {json.dumps(SUGGESTIONS_SCHEMA)}
        
        Rules:
        1. Categorize missing skills as High, Medium, or Low importance for this specific role.
        2. Provide exact text snippets from the resume in 'original' and improve them in 'rewritten' to match the JD vocabulary natively.
        3. Do NOT include markdown wrapping like ```json.
        """
        
        logger.info("Requesting structured insight / suggestions from Groq...")
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a JSON generator. Output ONLY valid JSON matching the schema."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        
        result_json = chat_completion.choices[0].message.content
        parsed_data = json.loads(result_json)
        logger.info("Successfully received structured insights.")
        return parsed_data
        
    except Exception as e:
        logger.error(f"Error generating LLM suggestions: {str(e)}")
        return fallback

import logging
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer, util

logger = logging.getLogger(__name__)
_model = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info("Loading SentenceTransformer model 'all-MiniLM-L6-v2'...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def calculate_semantic_similarity(resume_text: str, jd_text: str) -> float:
    """Calculate overall semantic similarity score."""
    try:
        model = get_model()
        resume_embedding = model.encode(resume_text, convert_to_tensor=True)
        jd_embedding = model.encode(jd_text, convert_to_tensor=True)
        score = util.cos_sim(resume_embedding, jd_embedding).item() * 100
        return round(max(0.0, min(100.0, score)), 2)
    except Exception as e:
        logger.error(f"Error calculating semantic similarity: {e}")
        return 0.0

def calculate_match_metrics(resume_items: List[str], jd_items: List[str]) -> Tuple[float, List[str], List[str]]:
    """Calculates coverage % and returns matching and missing items."""
    if not jd_items:
        return 100.0, resume_items, []
    
    r_lower = [i.lower() for i in resume_items]
    matching = []
    missing = []
    
    for item in jd_items:
        if item.lower() in r_lower:
            matching.append(item)
        else:
            missing.append(item)
            
    coverage = (len(matching) / len(jd_items)) * 100
    return round(coverage, 2), matching, missing

def calculate_experience_score(resume_years: float, jd_years: float, resume_domains: List[str], jd_domain: str) -> float:
    """Calculates experience alignment based on years and domain match."""
    score = 100.0
    
    # Penalize if missing years
    if resume_years < jd_years:
        deficit = jd_years - resume_years
        score -= (deficit / max(jd_years, 1)) * 50  # Up to 50% penalty
        
    # Bonus for domain match
    if jd_domain and jd_domain.lower() != "unknown":
        if any(jd_domain.lower() in d.lower() for d in resume_domains):
            score += 15
            
    return round(max(0.0, min(100.0, score)), 2)

def compute_final_score(resume_json: dict, jd_json: dict, full_resume_text: str, full_jd_text: str) -> dict:
    """
    FR4: Weighted Scoring Engine
    0.35 * Semantic Similarity
    0.30 * Skill Match Score
    0.20 * Experience Alignment
    0.15 * Tool Match
    """
    semantic_score = calculate_semantic_similarity(full_resume_text, full_jd_text)
    
    skills_score, matched_skills, missing_skills = calculate_match_metrics(
        resume_json.get("skills", []), jd_json.get("required_skills", [])
    )
    
    tools_score, matched_tools, missing_tools = calculate_match_metrics(
        resume_json.get("tools", []), jd_json.get("required_tools", [])
    )
    
    exp_score = calculate_experience_score(
        float(resume_json.get("experience_years", 0)),
        float(jd_json.get("experience_years", 0)),
        resume_json.get("domains", []),
        jd_json.get("domain", "Unknown")
    )
    
    # Final Formula
    overall_score = (
        (0.35 * semantic_score) +
        (0.30 * skills_score) +
        (0.20 * exp_score) +
        (0.15 * tools_score)
    )
    
    return {
        "overall_score": int(round(overall_score, 0)),
        "section_scores": {
            "semantic_similarity": semantic_score,
            "skills_match": skills_score,
            "experience_alignment": exp_score,
            "tools_match": tools_score
        },
        "missing_skills": missing_skills,
        "matched_skills": matched_skills,
        "missing_tools": missing_tools,
        "matched_tools": matched_tools
    }

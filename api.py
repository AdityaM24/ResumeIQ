from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import shutil
import tempfile
import logging
from dotenv import load_dotenv

load_dotenv()

from src.extract_text import extract_text_from_pdf
from src.preprocess import normalize_text
from src.parser import parse_resume
from src.jd_parser import parse_jd
from src.matcher import compute_final_score
from src.llm_suggester import generate_improvement_suggestions

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ResumeIQ Intelligence Engine",
    description="Phase 2 API: Advanced Resume-JD Semantic Matching, Skill Parsing, and AI Explanations.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeResponse(BaseModel):
    overall_score: int
    section_scores: dict
    missing_skills: list
    missing_tools: list
    improvement_suggestions: dict

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume_jd(
    resume_file: UploadFile = File(...),
    jd_text: str = Form(...),
    api_key: str = Form("")
):
    """
    POST /analyze
    Analyzes the uploaded resume against a Job Description.
    Extracts structured schemas using Groq LLMs, computes weighted semantic matching,
    detects prioritized skill gaps, and returns actionable JSON insights.
    """
    if not resume_file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for resumes.")
        
    temp_pdf_path = None
    try:
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        shutil.copyfileobj(resume_file.file, fp)
        temp_pdf_path = fp.name
        fp.close()
        
        # 1. Extraction & Parsing
        resume_raw_text = extract_text_from_pdf(temp_pdf_path)
        if not resume_raw_text:
             raise HTTPException(status_code=400, detail="Could not extract text from the provided PDF.")
             
        resume_clean = normalize_text(resume_raw_text)
        jd_clean = normalize_text(jd_text)
        
        # FR1 & FR2: Structured JSON Parsing via LLM
        resume_json = parse_resume(resume_clean, api_key=api_key)
        jd_json = parse_jd(jd_clean, api_key=api_key)
        
        # FR3 & FR4: Embeddings & Weighted Score
        score_data = compute_final_score(resume_json, jd_json, resume_clean, jd_clean)
        
        # FR5, FR6, FR7: Explainability Insight Generation
        suggestions = generate_improvement_suggestions(
            resume_json=resume_json,
            jd_json=jd_json,
            score_breakdown=score_data,
            api_key=api_key
        )
        
        return AnalyzeResponse(
            overall_score=score_data["overall_score"],
            section_scores=score_data["section_scores"],
            missing_skills=score_data["missing_skills"],
            missing_tools=score_data["missing_tools"],
            improvement_suggestions=suggestions
        )
        
    except Exception as e:
        logger.error(f"Error in /analyze endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        if temp_pdf_path and os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

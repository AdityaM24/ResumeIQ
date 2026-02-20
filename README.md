# 🧠 ResumeIQ - Intelligence Engine

An AI-powered **Resume ↔ Job Description** intelligence engine matching system using LLaMA structured extraction (via Groq API) and Semantic Embeddings.

ResumeIQ replaces primitive ATS keyword matching with **contextual AI reasoning**. It parses data into structured schemas, computes weighted match scores, detects critical skill gaps, and generates highly actionable resume improvement intelligence.

## 🚀 Vision & Core Capabilities

- **Semantic Match Scoring (Not Keyword Stuffing)**: Uses `sentence-transformers` to compute cosine similarity between the candidate's experience and the required JD context.
- **Skill Gap Intelligence**: Automatically detects missing skills and weights them by their Importance (High/Medium/Low) to the specific role.
- **Actionable AI Guidance**: Generates 3-5 precise, "Before & After" bullet rewrites to immediately improve the resume's ATS performance.
- **Explainable Breakdown**: Granular scoring components (Semantic Meaning, Skill Coverage, Experience Alignment, Tool Match) are fully exposed via API and UI.

## 🏗️ System Architecture

- **Backend / API**: FastAPI (Stateless `POST /analyze` schema)
- **Parsing & Reasoning Engine**: Groq API (`llama-3.1-8b-instant`) strictly constrained to JSON Object schemas.
- **Embedding Layer**: Local HuggingFace `all-MiniLM-L6-v2`
- **Frontend / Dashboard**: Streamlit (Reactive JSON Viewer & Intelligence UI)

## 📦 Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/AdityaM24/ResumeIQ.git
cd ResumeIQ
```

2. **Create and activate a virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Add Configuration**
Get a free API Key from [console.groq.com](https://console.groq.com).
```bash
echo "GROQ_API_KEY=your_key_here" > .env
```

## 💻 Usage (Streamlit Dashboard & FastAPI)

ResumeIQ requires **two concurrent services** to run: the inference API backend, and the interactive frontend dashboard.

**Terminal 1 (Start the Backend API):**
```bash
source .venv/bin/activate
uvicorn api:app --reload
```

**Terminal 2 (Start the UI Dashboard):**
```bash
source .venv/bin/activate
streamlit run app.py
```

Navigate to `http://localhost:8501` to use the intelligent dashboard. Use your Groq API key in the configuration sidebar to activate reasoning capabilities.

---

## 📡 API Design

The engine can be consumed headlessly by SaaS products or internal HR tools.

### `POST /analyze`
**Inputs (Form Data):**
- `resume_file`: (File, PDF)
- `jd_text`: (String)
- `api_key`: (String, Optional. Uses `.env` fallback)

**Output Payload Schema (Example):**
```json
{
  "overall_score": 78,
  "section_scores": {
    "semantic_similarity": 82.5,
    "skills_match": 70,
    "experience_alignment": 85,
    "tools_match": 60
  },
  "missing_skills": ["Kubernetes", "Redis"],
  "missing_tools": ["Jira"],
  "improvement_suggestions": {
    "missing_skills_importance": [...],
    "match_summary": "...",
    "top_5_improvements": [...],
    "rewrite_examples": [...]
  }
}
```

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to your branch and open a Pull Request

## 📜 License
This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 👤 Author
Aditya Mahale
- GitHub: [@AdityaM24](https://github.com/AdityaM24)
- Email: adityamahale76@gmail.com

import streamlit as st
import requests
import json
import logging

# Set custom Streamlit configuration
st.set_page_config(
    page_title="ResumeIQ - Intelligence Engine",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
    .main { background-color: #f7f9fc; }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 6px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .high-imp { color: #d32f2f; font-weight: bold; }
    .med-imp { color: #f57c00; font-weight: bold; }
    .low-imp { color: #388e3c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 ResumeIQ Intelligence Engine")
st.markdown("Contextual AI reasoning comparing resumes to target Job Descriptions.")

with st.sidebar:
    st.header("⚙️ Configuration")
    groq_api_key = st.text_input("Groq API Key", type="password")
    if not groq_api_key:
        st.warning("Please enter your Groq API Key to enable structured parsing and AI reasoning.")

col1, col2 = st.columns(2)
with col1:
    st.header("1. Upload Resume")
    resume_file = st.file_uploader("Upload Resume (PDF format)", type=["pdf"])

with col2:
    st.header("2. Target Job Description")
    jd_text = st.text_area("Paste JD details here:", height=200)

api_url = "http://localhost:8000/analyze"

if st.button("Start Analysis"):
    if not resume_file or not jd_text.strip():
        st.error("Please provide both a Resume and a Job Description.")
    else:
        with st.spinner("Extracting schemas, executing section-wise embeddings, and calculating alignment..."):
            try:
                files = {"resume_file": (resume_file.name, resume_file, "application/pdf")}
                data = {
                    "jd_text": jd_text,
                    "api_key": groq_api_key if groq_api_key else ""
                }
                
                response = requests.post(api_url, files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("Analysis Complete!")
                    
                    st.markdown("---")
                    st.header("📊 Match Breakdown")
                    
                    # Score Cards
                    sc1, sc2, sc3 = st.columns([1, 2, 1])
                    with sc2:
                        overall = result.get('overall_score', 0)
                        st.markdown(f"<div class='metric-card'><h3>ATS Intelligence Score</h3><h1 style='color: #1E3A8A; font-size: 4rem;'>{overall} / 100</h1></div>", unsafe_allow_html=True)
                    
                    # Section Scores
                    st.markdown("### Weighted Components")
                    sec_scores = result.get("section_scores", {})
                    cc1, cc2, cc3, cc4 = st.columns(4)
                    cc1.metric("Semantic Meaning", f"{sec_scores.get('semantic_similarity', 0)}%")
                    cc2.metric("Skill Coverage", f"{sec_scores.get('skills_match', 0)}%")
                    cc3.metric("Experience Alignment", f"{sec_scores.get('experience_alignment', 0)}%")
                    cc4.metric("Tool Match", f"{sec_scores.get('tools_match', 0)}%")
                    
                    st.markdown("---")
                    
                    # Intelligence Tabs
                    tab1, tab2, tab3 = st.tabs(["Actionable Insights", "Skill Intelligence", "Schema Data"])
                    
                    suggestions_data = result.get("improvement_suggestions", {})
                    
                    with tab1:
                        st.markdown("#### 📝 Executive Summary")
                        st.info(suggestions_data.get("match_summary", "No summary available."))
                        
                        st.markdown("#### 🎯 Top Improvement Actions")
                        actions = suggestions_data.get("top_5_improvements", [])
                        for i, act in enumerate(actions, 1):
                            st.write(f"{i}. {act}")
                            
                        st.markdown("#### ✨ Before & After Rewrites")
                        rewrites = suggestions_data.get("rewrite_examples", [])
                        for rw in rewrites:
                            st.markdown(f"**Original:** `{rw.get('original', '')}`")
                            st.markdown(f"**Better:** <span style='color: #2e7d32; font-weight: bold;'>{rw.get('rewritten', '')}</span>", unsafe_allow_html=True)
                            st.markdown("<hr style='margin: 10px 0;'/>", unsafe_allow_html=True)
                    
                    with tab2:
                        st.markdown("#### 🚨 Missing Critical Skills")
                        importance_list = suggestions_data.get("missing_skills_importance", [])
                        if importance_list:
                            for idx, item in enumerate(importance_list):
                                skill = item.get("skill", "")
                                imp = item.get("importance", "Low")
                                color_class = "high-imp" if imp == "High" else ("med-imp" if imp == "Medium" else "low-imp")
                                st.markdown(f"- **{skill}** (<span class='{color_class}'>{imp} Priority</span>)", unsafe_allow_html=True)
                        else:
                            st.success("No major missing skills identified against this JD!")
                            
                        st.markdown("#### 🔑 Keywords to Include")
                        kws = suggestions_data.get("keywords_to_include", [])
                        st.write(", ".join(kws) if kws else "None identified.")
                        
                    with tab3:
                        st.markdown("#### Raw API Payload Delivery")
                        with st.expander("View Full JSON Response"):
                            st.json(result)
                            
            except Exception as e:
                st.error(f"Error connecting to backend: {str(e)}")

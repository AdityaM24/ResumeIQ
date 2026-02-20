# Quick Start Guide - ResumeIQ

Get your ResumeIQ Intelligence Engine up and running in 5 minutes!

## 1️⃣ Prerequisites

- Python 3.8 or higher
- A free [Groq API Key](https://console.groq.com)
- A terminal/command prompt

## 2️⃣ Installation (2 minutes)

```bash
# Clone the repository
git clone https://github.com/AdityaM24/ResumeIQ.git
cd ResumeIQ

# Create a virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 3️⃣ Add the Configuration

We use Groq (LLaMA-3.1) to power the structured intelligent extraction layer.

**Option A (Recommended): Environment File**
Create a `.env` file in the root directory:
```bash
echo "GROQ_API_KEY=gsk_your_key_here" > .env
```

**Option B: Dashboard Configuration**
You can also directly paste your key into the Streamlit dashboard side-panel when you launch the UI!

## 4️⃣ Run the Engine (1 minute)

Because this is a decoupled API and Frontend architecture, you need to run **both** the backend Fastapi server and the frontend Streamlit dashboard.

**Open Terminal 1 (Run Backend):**
```bash
source .venv/bin/activate
uvicorn api:app --reload
```
You should see: `Uvicorn running on http://127.0.0.1:8000`

**Open Terminal 2 (Run Frontend):**
```bash
source .venv/bin/activate
streamlit run app.py
```
This will automatically open your web browser to `http://localhost:8501`.

## 5️⃣ Analyze Your Match

1. Make sure your Groq API key is defined in `.env` OR pasted into the UI Sidebar.
2. Upload any PDF Resume.
3. Paste a Job Description.
4. Click **Start Analysis**.

The intelligence engine will semantically weigh your skills and output highly structured missing skill reports, score breakdowns, and rewrite suggestions!

## ❓ Troubleshooting

### Error: `Unexpected token` or `Failed to decode JSON`
This means the API key is not set, or Groq tripped up on the file. Make sure your key is valid and the PDF isn't entirely an image (we only parse the text layer of PDFs so far).

### Error: `Port 8000 is already in use`
Change the FastAPI run port by adding `--port 8001` or similar. Remember to update `app.py`'s API target URL if you do this.

## 📚 Full Documentation

See [README.md](README.md) for comprehensive architectural documentation.

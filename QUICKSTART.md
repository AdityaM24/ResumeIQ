# Quick Start Guide - Resume Parser

Get your Resume Parser up and running in 5 minutes!

## 1️⃣ Prerequisites

- Python 3.8 or higher
- pip or conda
- A terminal/command prompt

## 2️⃣ Installation (2 minutes)

```bash
# Clone the repository
git clone https://github.com/AdityaM24/ResumeIQ.git
cd ResumeIQ

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 3️⃣ Prepare Your Data (1 minute)

Place your resume PDF files in the `data/raw_resumes/` directory:

```
resume-parser/
├── data/
│   └── raw_resumes/
│       ├── john_smith_resume.pdf
│       ├── jane_doe_resume.pdf
│       └── ... (more PDFs)
```

## 4️⃣ Run the Parser (1 minute)

```bash
# Process all resumes
python run.py
```

**Output**: Check `data/processed_output/parsed_resumes.csv`

## 5️⃣ Analyze Results (1 minute)

```bash
# Launch Jupyter notebook
jupyter notebook notebooks/analysis.ipynb
```

## 📋 Example Output

The parser generates a CSV with:
- **Name**: Extracted candidate name
- **Email**: Contact email address
- **Phone**: Phone number
- **Education**: Highest degree
- **Skills**: Identified technical skills
- **File**: Source PDF filename

Example:
```
Name,Email,Phone,Education,Skills,File
John Smith,john@example.com,1234567890,Bachelor,"Python, SQL, Machine Learning",john_smith_resume.pdf
```

## 🔧 Advanced Usage

### Debug Mode
```bash
python run.py --debug
```

### Custom Directories
```bash
python run.py --input /path/to/resumes --output-dir /path/to/output
```

### Custom Output File
```bash
python run.py --output results.csv
```

## 🧪 Run Tests

```bash
# All tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=src --cov-report=html
```

## 📚 Full Documentation

See [README.md](README.md) for comprehensive documentation.

## ❓ Troubleshooting

### Error: `No such file or directory: 'data/raw_resumes'`
Create the directory:
```bash
mkdir -p data/raw_resumes
```

### Error: `ModuleNotFoundError: No module named 'fitz'`
Install PyMuPDF:
```bash
pip install PyMuPDF==1.23.8
```

### Error: `csv file not found`
Make sure you've run `python run.py` first to generate the CSV.

## 📧 Need Help?

- Check [README.md](README.md) for detailed documentation
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Open an issue on GitHub for bug reports

## 🎉 You're All Set!

Happy parsing! 🚀

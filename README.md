# Resume Parser - Portfolio Project

A robust resume parsing system that extracts and structures candidate information from PDF resumes. This project demonstrates proficiency in text processing, data engineering, and building scalable data pipelines.

## Project Overview

This application automates extraction of key information from resume PDFs including personal details, education, skills, and experience-ready fields. It is designed for recruiter dashboards, ATS systems, and data analysis pipelines.

## Features

- PDF text extraction with PyMuPDF (fitz)
- Text preprocessing and normalization
- Regex-based field extraction with validation
- Batch processing for multiple resumes
- Comprehensive error handling and logging
- Structured CSV output
- Full type hints for code quality

## Tech Stack

- Language: Python 3.8+
- Core Libraries: PyMuPDF (fitz), pandas, regex
- Testing: pytest
- Code Quality: type hints, docstrings, logging

## Installation

1. Clone the repository
```bash
git clone https://github.com/AdityaM24/ResumeIQ.git
cd ResumeIQ
```
2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

Process all resumes in batch:
```bash
python run.py
```

Programmatic use:
```python
from src.pipeline import process_resume

result = process_resume("path/to/resume.pdf")
print(result)
```

## Directory Structure

```
resume-parser/
├── README.md
├── requirements.txt
├── setup.py
├── run.py
├── config.py
├── src/
│   ├── __init__.py
│   ├── extract_text.py
│   ├── preprocess.py
│   ├── parser.py
│   └── pipeline.py
├── tests/
│   ├── __init__.py
│   ├── test_extract_text.py
│   ├── test_parser.py
│   └── test_pipeline.py
├── notebooks/
│   └── analysis.ipynb
└── data/
    ├── raw_resumes/
    └── processed_output/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to your branch and open a Pull Request

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Author

Aditya Mahale
- GitHub: [@AdityaM24](https://github.com/AdityaM24)
- Email: adityamahale76@gmail.com
- Project: [ResumeIQ](https://github.com/AdityaM24/ResumeIQ)

## Contact

- Open an issue: https://github.com/AdityaM24/ResumeIQ/issues
- Email: adityamahale76@gmail.com

# Contributing to Resume Parser

Thank you for your interest in contributing to Resume Parser! This document provides guidelines and instructions for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/resume-parser.git
   cd resume-parser
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

### Code Style

- Follow **PEP 8** style guide
- Use **type hints** for all functions
- Add **docstrings** to all modules and functions
- Use **Google-style docstrings**

Format code with Black:
```bash
black src/ tests/ run.py config.py
```

### Testing

Before submitting a PR, ensure all tests pass:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_parser.py -v
```

### Linting

Check code quality:
```bash
flake8 src/ tests/ run.py config.py
isort src/ tests/ run.py config.py
```

## Making Changes

### Bug Fixes

1. Create a branch for the bug fix:
   ```bash
   git checkout -b fix/issue-description
   ```
2. Make your changes
3. Add tests for the fix
4. Update documentation if needed
5. Commit with clear message:
   ```bash
   git commit -m "Fix: Brief description of the fix"
   ```

### New Features

1. Create a feature branch:
   ```bash
   git checkout -b feature/feature-name
   ```
2. Implement the feature with tests
3. Update README if adding new functionality
4. Commit with clear message:
   ```bash
   git commit -m "Feature: Add description of new feature"
   ```

## Pull Request Process

1. **Update** the README.md with any new functionality
2. **Add tests** for new code (coverage should remain high)
3. **Ensure** all tests pass locally
4. **Format** code with Black and lint with Flake8
5. **Write a clear PR description** explaining:
   - What changes are made
   - Why the changes are needed
   - How to test the changes
6. **Link** any related issues

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Standards

Examples of behavior that contributes to a positive environment:
- Using welcoming and inclusive language
- Being respectful of differing opinions
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

## Questions or Need Help?

- **Issues**: Open a GitHub issue at [AdityaM24/ResumeIQ/issues](https://github.com/AdityaM24/ResumeIQ/issues)
- **Discussions**: Use GitHub Discussions at [AdityaM24/ResumeIQ/discussions](https://github.com/AdityaM24/ResumeIQ/discussions)
- **Email**: Contact at adityamahale76@gmail.com

## Recognition

All contributions will be recognized in the project's contributor list.

Thank you for contributing to Resume Parser! 🎉

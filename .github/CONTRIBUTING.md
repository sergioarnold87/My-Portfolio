# Contributing to Sergio Arnold's Portfolio

Thank you for your interest in contributing to this portfolio! While this is primarily a personal showcase, I welcome suggestions, bug reports, and improvements.

## 🤝 How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with a clear title and description
3. **Include details:**
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots if applicable

### Proposing Changes

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the guidelines below
4. **Commit with clear messages:**
   ```bash
   git commit -m "feat: add feature description"
   git commit -m "fix: resolve issue with XYZ"
   git commit -m "docs: update README for project ABC"
   ```
5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request** with a clear description

## 📝 Commit Message Convention

Follow conventional commits format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, no logic change)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

**Examples:**
```
feat: add sentiment analysis to climate project
fix: correct data preprocessing in computer vision pipeline
docs: update installation instructions for Linux Mint
refactor: optimize ETL pipeline performance
```

## 🎨 Code Style Guidelines

### Python Code

- **PEP 8 compliance:** Follow Python's style guide
- **Line length:** Max 100 characters (flexible to 120 for readability)
- **Formatting:** Use `black` for automatic formatting:
  ```bash
  black your_file.py
  ```
- **Linting:** Run `flake8` before committing:
  ```bash
  flake8 your_file.py
  ```
- **Docstrings:** Use Google-style docstrings:
  ```python
  def function_name(param1: str, param2: int) -> bool:
      """Brief description of function.
      
      Args:
          param1: Description of param1
          param2: Description of param2
          
      Returns:
          Description of return value
      """
  ```

### Project Structure

Each project should maintain:
```
project-name/
├── README.md              # Comprehensive documentation
├── requirements.txt       # Python dependencies
├── .gitignore            # Ignore rules
├── src/                  # Source code
├── notebooks/            # Jupyter notebooks
├── data/                 # Data files (gitignored)
└── tests/                # Unit tests
```

### Documentation

- **README files:** Must include Overview, Architecture, Tech Stack, Setup, and Key Learnings
- **Code comments:** Explain *why*, not *what*
- **Inline documentation:** For complex algorithms or business logic

## 🧪 Testing

- Write tests for new features when applicable
- Ensure existing tests pass before submitting PR
- Use pytest for Python projects:
  ```bash
  pytest tests/
  ```

## 🔄 Git Workflow

We follow a simplified Git Flow:

1. **Main branch:** Production-ready code
2. **Develop branch:** Integration branch for features
3. **Feature branches:** Individual features/fixes
4. **Pull Requests:** All changes must go through PR review

### Branch Naming Convention

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

**Examples:**
```
feature/add-rag-chatbot
fix/airflow-dag-timeout
docs/update-setup-instructions
refactor/optimize-etl-pipeline
```

## 📋 Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages follow conventions
- [ ] No merge conflicts with main branch
- [ ] Dependencies are documented in requirements.txt
- [ ] Sensitive data (API keys, credentials) are not committed

## 🚀 Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sergioarnold87/My-Portfolio.git
   cd My-Portfolio
   ```

2. **Set up virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   # For specific project
   cd project-name
   pip install -r requirements.txt
   
   # For development tools
   pip install black flake8 pytest
   ```

4. **Configure git hooks (optional):**
   ```bash
   # Pre-commit hook for formatting
   pip install pre-commit
   pre-commit install
   ```

## 🌟 Recognition

Contributors will be acknowledged in:
- Project README files
- Release notes
- Portfolio documentation

## 📫 Contact

For questions or discussions:
- **Email:** sergioarnold87@gmail.com
- **LinkedIn:** [linkedin.com/in/sergioarnold87](https://www.linkedin.com/in/sergioarnold87/)
- **GitHub Issues:** Preferred for technical discussions

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project (GNU General Public License v3.0).

---

**Thank you for contributing to this portfolio! Every improvement helps showcase better engineering practices.** 🚀

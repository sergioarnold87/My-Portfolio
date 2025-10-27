# GitHub Best Practices Guide

This document outlines Git and GitHub best practices for maintaining this portfolio and collaborating on projects.

## 📚 Table of Contents

1. [Branch Strategy](#branch-strategy)
2. [Commit Guidelines](#commit-guidelines)
3. [Pull Request Process](#pull-request-process)
4. [Code Review](#code-review)
5. [Issue Management](#issue-management)
6. [Security](#security)
7. [Documentation](#documentation)

---

## 🌿 Branch Strategy

### Main Branches

- **`main`**: Production-ready code. Protected branch.
- **`develop`**: Integration branch for features. All feature branches merge here first.

### Supporting Branches

#### Feature Branches
```bash
# Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/add-sentiment-analysis

# Work on your feature...

# Push to remote
git push -u origin feature/add-sentiment-analysis
```

#### Fix Branches
```bash
# For bug fixes
git checkout -b fix/resolve-airflow-timeout
```

#### Hotfix Branches
```bash
# For urgent production fixes
git checkout main
git checkout -b hotfix/critical-security-patch
```

### Branch Naming Convention

Format: `type/short-description-kebab-case`

**Types:**
- `feature/` - New features
- `fix/` - Bug fixes
- `hotfix/` - Critical production fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Test additions/modifications
- `chore/` - Maintenance tasks

**Examples:**
```
feature/rag-document-upload
fix/chromadb-connection-error
docs/update-installation-guide
refactor/optimize-etl-pipeline
test/add-unit-tests-preprocessing
chore/update-dependencies
```

---

## 💬 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, semicolons, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `chore`: Maintenance, dependencies, configuration
- `ci`: CI/CD changes

#### Scope (optional)
Project or module affected: `chatbot`, `etl`, `cv-model`, `airflow-dag`

#### Subject
- Use imperative mood ("add" not "added")
- Don't capitalize first letter
- No period at the end
- Max 50 characters

#### Body (optional)
- Explain what and why, not how
- Wrap at 72 characters

#### Footer (optional)
- Reference issues: `Closes #123`, `Fixes #456`
- Breaking changes: `BREAKING CHANGE: description`

### Examples

**Simple commit:**
```bash
git commit -m "feat(chatbot): add conversation history export"
```

**Detailed commit:**
```bash
git commit -m "feat(etl): implement incremental data loading

Add incremental loading strategy to reduce processing time
and avoid reprocessing historical data.

- Add watermark tracking table
- Implement delta detection logic
- Add unit tests for incremental logic

Closes #42"
```

**Fix commit:**
```bash
git commit -m "fix(airflow): resolve DAG timeout issue

Increase task timeout from 300s to 600s to handle
large dataset processing.

Fixes #67"
```

### Atomic Commits

- One logical change per commit
- Commit should be revertable independently
- Don't mix refactoring with feature additions

```bash
# Good - atomic commits
git commit -m "feat: add user authentication"
git commit -m "refactor: extract validation logic"
git commit -m "docs: update API documentation"

# Bad - mixed changes
git commit -m "add auth, refactor code, update docs"
```

---

## 🔄 Pull Request Process

### Creating a Pull Request

1. **Ensure branch is up-to-date:**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout feature/your-feature
   git merge develop
   # Resolve conflicts if any
   ```

2. **Push your branch:**
   ```bash
   git push origin feature/your-feature
   ```

3. **Create PR on GitHub:**
   - Use descriptive title
   - Fill out PR template completely
   - Link related issues
   - Add labels (feature, bug, documentation, etc.)
   - Request reviewers
   - Assign yourself

### PR Title Format

```
<type>(<scope>): <description>
```

Examples:
- `feat(rag): add document upload functionality`
- `fix(cv-model): correct image preprocessing pipeline`
- `docs(readme): update installation instructions`

### PR Description Checklist

- [ ] Clear description of changes
- [ ] Motivation/context for changes
- [ ] Screenshots/demos (if applicable)
- [ ] Testing performed
- [ ] Breaking changes noted
- [ ] Documentation updated

### Before Submitting PR

```bash
# Run linters
black .
flake8 .

# Run tests
pytest tests/

# Check for secrets
git secrets --scan

# Ensure .gitignore is updated
git status  # Should not show unwanted files
```

---

## 👀 Code Review

### For Reviewers

**What to Check:**
- [ ] Code follows project style guidelines
- [ ] Logic is sound and efficient
- [ ] Edge cases are handled
- [ ] Tests are adequate
- [ ] Documentation is clear
- [ ] No security vulnerabilities
- [ ] No hardcoded credentials
- [ ] Performance implications considered

**Review Etiquette:**
- Be constructive and respectful
- Explain the "why" behind suggestions
- Acknowledge good practices
- Distinguish between "must fix" and "nice to have"

**Comment Prefixes:**
- `MUST:` Critical change required
- `SHOULD:` Strong recommendation
- `NITS:` Minor suggestion
- `QUESTION:` Seeking clarification
- `FYI:` Informational

### For Authors

- Respond to all comments
- Don't take feedback personally
- Ask for clarification if needed
- Update PR based on feedback
- Re-request review after changes

---

## 📋 Issue Management

### Creating Issues

**Title Format:**
```
[TYPE] Clear, concise description
```

Types: `BUG`, `FEATURE`, `DOCS`, `ENHANCEMENT`

**Examples:**
- `[BUG] Airflow DAG fails on large datasets`
- `[FEATURE] Add RAG system with ChromaDB`
- `[DOCS] Missing setup instructions for GCP project`

### Issue Templates

**Bug Report:**
- Description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, dependencies)
- Screenshots/logs

**Feature Request:**
- Problem to solve
- Proposed solution
- Alternatives considered
- Additional context

### Labels

- `bug` - Something isn't working
- `feature` - New feature or request
- `documentation` - Documentation improvements
- `enhancement` - Improvement to existing feature
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `priority: high/medium/low`
- `status: in-progress/blocked/review`

---

## 🔐 Security

### Never Commit Sensitive Data

**Prohibited:**
- API keys
- Passwords
- Database credentials
- Private keys
- Tokens
- Environment variables with secrets

### Use Environment Variables

```python
# Good
import os
api_key = os.getenv('OPENAI_API_KEY')

# Bad
api_key = 'sk-1234567890abcdef'  # NEVER DO THIS
```

### .env File Structure

```bash
# .env (gitignored)
OPENAI_API_KEY=sk-your-key-here
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/db
```

### .env.example Template

```bash
# .env.example (committed)
OPENAI_API_KEY=your_openai_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Scan for Secrets

```bash
# Install git-secrets
git secrets --install

# Scan repository
git secrets --scan

# Scan history
git secrets --scan-history
```

### If You Accidentally Commit Secrets

1. **Immediately revoke the credential**
2. **Remove from history:**
   ```bash
   git filter-branch --force --index-filter \
   "git rm --cached --ignore-unmatch path/to/file" \
   --prune-empty --tag-name-filter cat -- --all
   ```
3. **Force push (be careful):**
   ```bash
   git push origin --force --all
   ```
4. **Notify team**

---

## 📖 Documentation

### README Standards

Every project must have a comprehensive README with:

1. **Header:** Title, badges, tagline
2. **Overview:** What the project does
3. **Architecture/Pipeline:** Visual diagram
4. **Tech Stack:** Technologies used
5. **How to Run:** Installation and usage
6. **Key Learnings:** Insights gained
7. **Project Structure:** Directory layout
8. **License:** License information
9. **Contact:** How to reach you

### Code Documentation

**Python Docstrings:**
```python
def process_data(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Process raw data according to configuration.
    
    This function applies transformations specified in the config
    dictionary to clean and prepare data for analysis.
    
    Args:
        df: Raw input DataFrame
        config: Configuration dictionary with keys:
            - 'remove_nulls': bool
            - 'normalize': bool
            - 'encoding': str
    
    Returns:
        Processed DataFrame ready for analysis
        
    Raises:
        ValueError: If required config keys are missing
        
    Example:
        >>> config = {'remove_nulls': True, 'normalize': True}
        >>> processed = process_data(raw_df, config)
    """
```

### Inline Comments

```python
# Good - explains WHY
# Use exponential backoff to avoid rate limiting
time.sleep(2 ** retry_count)

# Bad - explains WHAT (obvious)
# Increment counter
counter += 1
```

---

## 🚀 Workflow Summary

### Daily Workflow

```bash
# 1. Start your day
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/your-feature

# 3. Work and commit frequently
git add .
git commit -m "feat: implement feature X"

# 4. Keep branch updated
git fetch origin
git merge origin/develop

# 5. Push and create PR
git push origin feature/your-feature
# Create PR on GitHub

# 6. After PR is merged
git checkout develop
git pull origin develop
git branch -d feature/your-feature
```

### Release Workflow

```bash
# 1. Create release branch
git checkout develop
git checkout -b release/v1.2.0

# 2. Update version numbers, changelog
# Make final adjustments

# 3. Merge to main
git checkout main
git merge release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags

# 4. Merge back to develop
git checkout develop
git merge release/v1.2.0
git push origin develop

# 5. Delete release branch
git branch -d release/v1.2.0
```

---

## 📚 Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Semantic Versioning](https://semver.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)

---

**Following these practices ensures clean, maintainable, and collaborative development!** 🎯

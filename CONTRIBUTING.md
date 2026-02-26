# Contributing Guidelines

## Development Workflow

### Branch Strategy

We follow **Git Flow** with feature branches:

- `main` - Production-ready code (protected)
- `develop` - Integration branch for features
- `feature/*` - New features (e.g., `feature/database-service`)
- `bugfix/*` - Bug fixes
- `hotfix/*` - Critical production fixes

### Commit Message Convention

We follow **Conventional Commits**:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(database): Add SQLite schema initialization

- Create artists, beats, email_history tables
- Add CRUD operations
- Implement connection pooling

Closes #5
```

```
fix(auth): Handle token refresh errors gracefully

Fixes #12
```

### Pull Request Process

1. **Create Feature Branch**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**:
   - Write code following style guide
   - Add tests
   - Update documentation

3. **Commit Changes**:
   ```bash
   git add .
   git commit -m "feat(scope): description"
   ```

4. **Push and Create PR**:
   ```bash
   git push origin feature/your-feature-name
   ```
   - Create PR on GitHub
   - Fill out PR template
   - Request review

5. **Code Review**:
   - Address review comments
   - Update PR if needed
   - Wait for approval

6. **Merge**:
   - Squash and merge to `develop`
   - Delete feature branch

### Code Review Checklist

- [ ] Code follows style guide
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No sensitive data committed
- [ ] Error handling implemented
- [ ] Logging added where appropriate

## Code Standards

### Python Style Guide

- Follow **PEP 8** (use `black` formatter)
- Maximum line length: 88 characters (Black default)
- Use type hints for all functions
- Docstrings for all public functions/classes
- Use `isort` for import sorting

### Example:

```python
from typing import List, Optional
from pathlib import Path

def get_artists_from_drive(folder_id: str) -> List[dict]:
    """
    Fetch artist list from Google Drive folder.

    Args:
        folder_id: Google Drive folder ID

    Returns:
        List of dictionaries with 'name' and 'email' keys

    Raises:
        GoogleAPIError: If API call fails
    """
    # Implementation
    pass
```

### Testing Requirements

- Unit tests for all services
- Integration tests for API interactions
- Minimum 80% code coverage
- All tests must pass before merging

### Documentation

- Update README for user-facing changes
- Update docstrings for code changes
- Update NEXT_STEPS.md for new features
- Add examples for complex features

## Development Setup

1. **Fork and Clone**:
   ```bash
   git clone https://github.com/your-username/ContactAutomation.git
   cd ContactAutomation
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Install Pre-commit Hooks**:
   ```bash
   pre-commit install
   ```

5. **Run Tests**:
   ```bash
   pytest
   ```

6. **Run Linting**:
   ```bash
   black .
   isort .
   flake8 .
   mypy .
   ```

## Issue Reporting

Use GitHub Issues with appropriate labels:
- `bug` - Something isn't working
- `feature` - New feature request
- `enhancement` - Improvement to existing feature
- `documentation` - Documentation improvements
- `question` - Questions or discussions

## Questions?

Open a discussion or issue on GitHub.

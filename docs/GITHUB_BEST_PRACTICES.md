# GitHub Best Practices

This document outlines GitHub-specific best practices followed in this project.

## Repository Structure

### Branch Strategy

We follow **Git Flow**:

```
main (production-ready)
  └── develop (integration)
       ├── feature/database-service
       ├── feature/drive-integration
       ├── bugfix/email-error
       └── hotfix/critical-bug
```

**Branch Naming**:
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Critical production fixes
- `docs/*` - Documentation updates
- `refactor/*` - Code refactoring

### Branch Protection

**Main Branch**:
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ No direct pushes (except hotfixes)

**Develop Branch**:
- ✅ Require pull request reviews
- ✅ Require status checks to pass

## Commit Messages

Follow **Conventional Commits**:

```
<type>(<scope>): <subject>

<body>

<footer>
```

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

## Pull Requests

### PR Process

1. **Create Feature Branch**
2. **Make Changes** (with tests)
3. **Push to GitHub**
4. **Create PR** (fill template)
5. **Request Review**
6. **Address Feedback**
7. **Get Approval**
8. **Merge** (squash and merge)

### PR Requirements

- [ ] Descriptive title
- [ ] Template filled out
- [ ] Related issues linked
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All checks passing
- [ ] At least 1 approval

### PR Template

Always use the PR template (`.github/PULL_REQUEST_TEMPLATE.md`)

## Issues

### Issue Types

- **Bug Report**: Use bug template
- **Feature Request**: Use feature template
- **Documentation**: Use feature template
- **Question**: Use discussion or issue

### Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or improvement
- `documentation` - Documentation changes
- `question` - Questions or discussions
- `help wanted` - Extra attention needed
- `good first issue` - Good for newcomers
- `priority: high` - High priority
- `priority: low` - Low priority

### Issue Workflow

1. Create issue with template
2. Add appropriate labels
3. Assign to milestone (if applicable)
4. Link to related issues/PRs
5. Close when resolved

## Releases

### Release Process

1. **Update Version**:
   - Update version in code
   - Update CHANGELOG.md

2. **Create Release**:
   - Go to GitHub Releases
   - Click "Draft a new release"
   - Tag: `v1.0.0`
   - Title: `v1.0.0 - Feature Name`
   - Description: Copy from CHANGELOG

3. **Publish Release**:
   - Creates tag
   - Triggers workflows (if configured)

### Release Notes

- Use CHANGELOG.md content
- Highlight breaking changes
- List new features
- Mention bug fixes

## GitHub Actions

### CI Workflow

Runs on:
- Push to `main` or `develop`
- Pull requests to `main` or `develop`

Checks:
- Code formatting (Black)
- Import sorting (isort)
- Linting (Flake8)
- Type checking (MyPy)
- Tests (pytest)

### Pre-commit Workflow

Runs pre-commit hooks on:
- Pull requests
- Pushes

## Code Reviews

### Review Checklist

- [ ] Code follows style guide
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No sensitive data
- [ ] Error handling present
- [ ] Logging appropriate
- [ ] Performance considered

### Review Process

1. **Request Review**: Assign reviewers
2. **Review**: Comment on code
3. **Address Feedback**: Make changes
4. **Re-request Review**: If needed
5. **Approve**: When satisfied
6. **Merge**: After approval

## Security

### Secrets Management

- ✅ Never commit secrets
- ✅ Use GitHub Secrets for CI/CD
- ✅ Use environment variables
- ✅ Rotate credentials regularly

### Security Scanning

- Dependabot for dependency updates
- Security advisories monitoring
- Regular dependency audits

## Documentation

### README

- Clear project description
- Setup instructions
- Usage examples
- Contributing guidelines
- License information

### Documentation Files

- `CONTRIBUTING.md` - How to contribute
- `CHANGELOG.md` - Version history
- `docs/` - Additional documentation
- Code comments and docstrings

## Project Management

### Milestones

Use milestones for:
- Major releases
- Feature sets
- Sprint planning

### Projects

Use GitHub Projects for:
- Kanban boards
- Roadmap tracking
- Task management

### Discussions

Use Discussions for:
- Questions
- Ideas
- General conversation

## Best Practices Summary

✅ **Do**:
- Use feature branches
- Write descriptive commit messages
- Fill out PR templates
- Request code reviews
- Update documentation
- Follow naming conventions
- Use labels appropriately
- Keep branches up to date

❌ **Don't**:
- Commit directly to main/develop
- Commit secrets or credentials
- Force push to shared branches
- Merge without review
- Skip tests
- Ignore linting errors
- Leave PRs without description

## Resources

- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Best Practices](https://docs.github.com/en/get-started/quickstart/github-flow)

# AGENTS.md

This file provides guidance to AI agents when working with GitHub configuration and automation.

## Directory Overview

This directory contains GitHub-specific configuration files for repository automation, workflows, issue templates, and security settings.

## GitHub Configuration

### Automation Components

1. **Workflows**: GitHub Actions for CI/CD, testing, and deployment
2. **Issue Templates**: Standardized templates for bug reports and feature requests
3. **Security**: Dependabot and secret scanning configuration
4. **Pull Request Templates**: Templates for consistent PR descriptions

### Key Files

- `workflows/` - GitHub Actions workflow definitions
- `ISSUE_TEMPLATE/` - Issue and bug report templates
- `dependabot.yml` - Automated dependency updates configuration
- `secret_scanning.yml` - Secret scanning configuration
- `pull_request_template.md` - Pull request template

## Agent Guidelines

### GitHub Actions Workflows

The workflows automate:

1. **Continuous Integration**: Run tests on every push and PR
2. **Code Quality**: Linting, formatting, and type checking
3. **Security Scanning**: Dependency and vulnerability scanning
4. **Documentation**: Generate and deploy documentation
5. **Release Management**: Automated releases and changelog generation

### Best Practices for Agents

1. **Workflow Triggers**: Understand when workflows are triggered
2. **Environment Variables**: Use secrets for sensitive configuration
3. **Caching**: Leverage caching for faster workflow execution
4. **Matrix Builds**: Test across multiple Python versions and environments
5. **Security**: Never commit secrets or sensitive information

### Common Workflow Patterns

#### CI/CD Pipeline

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install uv
        uv sync --extra dev
    
    - name: Run linting
      run: make lint
    
    - name: Run tests
      run: make test
```

#### Security Scanning

```yaml
name: Security

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  security:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run security scan
      uses: github/super-linter@v4
      env:
        DEFAULT_BRANCH: main
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Run dependency check
      uses: pypa/gh-action-pip-audit@v1.0.0
      with:
        inputs: requirements.txt
```

### Issue Templates

Standardized templates help users report issues effectively:

#### Bug Report Template

```markdown
---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment:**
- OS: [e.g. iOS]
- Python Version: [e.g. 3.11]
- Graphiti Version: [e.g. 1.0.0]

**Additional context**
Add any other context about the problem here.
```

#### Feature Request Template

```markdown
---
name: Feature Request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions.

**Additional context**
Add any other context or screenshots about the feature request here.
```

### Dependabot Configuration

Automated dependency management:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    reviewers:
      - "maintainer-team"
    assignees:
      - "dependency-manager"
    commit-message:
      prefix: "deps"
      include: "scope"
    
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
    reviewers:
      - "maintainer-team"
```

### Security Configuration

#### Secret Scanning

```yaml
# Prevent accidental commit of secrets
name: Secret Scanning

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run secret scan
      uses: trufflesecurity/trufflehog@v3.0.0
      with:
        path: ./
        base: main
        head: HEAD
```

### Pull Request Templates

Standard PR template:

```markdown
## Description
Brief description of the changes in this PR.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Code is commented where necessary
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Repository Management

#### Branch Protection Rules

```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "continuous-integration",
      "security-scan"
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 2,
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true
  },
  "restrictions": null
}
```

#### Code Owners

```
# Global owners
* @maintainer-team

# Core components
/graphiti_core/ @core-team
/server/ @backend-team
/mcp_server/ @mcp-team

# Documentation
*.md @docs-team
/docs/ @docs-team

# Configuration
/.github/ @devops-team
/docker-compose.yml @devops-team
```

### Release Automation

#### Automated Release Workflow

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Build package
      run: |
        pip install build
        python -m build
    
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@v1.8.0
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
    
    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        draft: false
        prerelease: false
```

### Monitoring and Notifications

#### Status Checks

```yaml
name: Status Check

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  health-check:
    runs-on: ubuntu-latest
    
    steps:
    - name: Check service health
      run: |
        curl -f https://api.example.com/health || exit 1
    
    - name: Notify on failure
      if: failure()
      uses: 8398a7/action-slack@v3
      with:
        status: failure
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Performance Monitoring

#### Benchmark Tracking

```yaml
name: Performance

on:
  push:
    branches: [ main ]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run benchmarks
      run: |
        python -m pytest tests/performance/ --benchmark-json=benchmark.json
    
    - name: Store benchmark result
      uses: benchmark-action/github-action-benchmark@v1
      with:
        tool: 'pytest'
        output-file-path: benchmark.json
        github-token: ${{ secrets.GITHUB_TOKEN }}
        auto-push: true
```

### Documentation Automation

#### Auto-generate Documentation

```yaml
name: Documentation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  docs:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -e .[docs]
    
    - name: Build documentation
      run: |
        cd docs
        make html
    
    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/main'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs/_build/html
```

### Best Practices Summary

1. **Automation**: Automate repetitive tasks with GitHub Actions
2. **Security**: Implement security scanning and secret detection
3. **Quality Gates**: Use status checks to maintain code quality
4. **Documentation**: Keep documentation updated and accessible
5. **Monitoring**: Monitor repository health and performance continuously
# Contributing to Amazon Task Manager

Thank you for considering contributing to the Amazon Task Manager project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by its Code of Conduct. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find that the bug has already been reported. When you are creating a bug report, please include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed after following the steps
- Explain which behavior you expected to see instead and why
- Include screenshots if possible
- Include details about your environment (OS, Docker version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- A clear and descriptive title
- A detailed description of the proposed functionality
- Any possible implementation details
- Why this enhancement would be useful to most users

### Pull Requests

- Fill in the required template
- Do not include issue numbers in the PR title
- Follow the Python style guide (PEP 8)
- Include appropriate tests
- Document new code
- End all files with a newline

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/amazon-task-manager.git
   cd amazon-task-manager
   ```

3. Set up the development environment:
   ```bash
   docker-compose up -d
   ```

4. Make your changes and test them

## Testing

Run the test suite to ensure your changes don't break existing functionality:

```bash
docker-compose exec web pytest
```

## Style Guidelines

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Python Style Guide

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).

### Documentation Style Guide

- Use Markdown for documentation
- Reference functions, classes, and modules in backticks
- Include code examples where appropriate

## Additional Notes

### Issue and Pull Request Labels

| Label name | Description |
| --- | --- |
| `bug` | Confirmed bugs or reports likely to be bugs |
| `enhancement` | Feature requests |
| `documentation` | Documentation improvements |
| `good first issue` | Good for newcomers |
| `help wanted` | Extra attention is needed |

## Thank You!

Your contributions to open source, large or small, make projects like this possible. Thank you for taking the time to contribute.
# Contributing

Thanks for your interest in contributing!

This document outlines how to contribute effectively to this project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**

    ```bash
    git clone https://github.com/your-username/repo-name.git
    cd repo-name
    ```

3. **Create a branch**

```bash
   git checkout -b feature/your-feature-name
```

4. **Install dependencies**

```bash
  uv sync
  pip install -r requirements.txt
```

5. **Run the project**

```bash
   uv run main.py
```

## Guidelines

### Code Style

- Follow existing code patterns in the project
- Keep code simple and readable
- Use meaningful variable and function names
- Avoid unnecessary complexity

### Documentation

- Update documentation if your changes affect usage
- Add comments for complex logic
- Keep README accurate

### Commits

Use conventional commit messages:

```bash
feat: add batch download support
fix: handle invalid URL parsing
refactor: simplify download service
```

## Making Changes

- Keep changes focused and minimal
- Avoid mixing unrelated changes in a single PR
- Test your changes before submitting

## Pull Requests

Before opening a PR:

- Ensure the project builds/runs successfully
- Verify your changes work as expected
- Update relevant documentation if needed

When submitting:

- Clearly describe what your PR does
- Mention any related issues
- Keep the PR scope small and focused

## Reporting Issues

If you find a bug or have a feature request, open an issue with:

- A clear description of the problem
- Steps to reproduce (if applicable)
- Expected vs actual behavior
- Relevant logs or screenshots

## Code of Conduct

- Be respectful and constructive
- Focus on improving the project
- Communicate clearly and professionally

## Notes

- Do not commit sensitive information (e.g., API keys, credentials)
- Follow best practices for security and privacy

Thanks for contributing! 🚀

---
name: PytestBestPractices
description: provides best practices for using pytest effectively in Python projects, including project layout, test discovery, and running tests in isolated environments.
---

# pytest: Good Integration Practices (Summary)

Source: https://docs.pytest.org/en/stable/explanation/goodpractices.html

## Goal of these practices
- Make tests reliable, easy to run locally and in CI, and representative of how users will run/install your package.
- Keep the test suite maintainable as the project grows.

## Install the project the way users do
- Prefer running tests against an installed package rather than relying on importing from the repository root.
- For local development, use an editable install so changes are picked up without reinstalls:
  - python -m pip install -e .

### Tests outside the package
Typical structure:
- src/your_package/...
- tests/...

Why this is useful:
- Encourages testing the installed package (more realistic).
- Reduces accidental imports from the working directory.

## Follow pytest’s test discovery rules
- Name tests so pytest can find them consistently.
- Common conventions include:
  - Files: test_*.py or *_test.py
  - Functions: test_*
  - Classes: Test*

## Prefer --import-mode=importlib for new projects
- Using importlib-based importing can prevent surprises caused by Python path/working-directory quirks.
- This is particularly helpful when your repository structure could otherwise shadow installed packages.

## Run tests like CI: isolated environments
- Use tox (or another environment manager) to run tests in clean, reproducible virtualenvs.
- This helps catch missing dependencies and packaging issues early.

## Avoid deprecated/legacy approaches
- Avoid setup.py test and pytest-runner; they are discouraged in modern Python packaging workflows.
- Use standard tooling (pip, build, tox, etc.) and invoke pytest directly.

## Keep configuration centralized
- Put pytest settings in a single place (often pyproject.toml, pytest.ini, or tox.ini) so everyone runs tests the same way.
- Keep paths, markers, and defaults explicit and documented.

## Enforce style for tests
- Tools like flake8-pytest-style can help keep tests consistent and readable.

## Practical checklist
- [ ] python -m pip install -e .
- [ ] Ensure tests pass when the package is installed (not just importable from the repo root).
- [ ] Adopt a clear tests/ layout and naming conventions.
- [ ] Consider --import-mode=importlib.
- [ ] Run in isolated envs (e.g., tox) before merging.
- [ ] Keep pytest config centralized.
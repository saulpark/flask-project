# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask web application currently serving a "Hello World" page, with plans to evolve into a full-featured note-taking application with rich-text editing, user authentication, and public sharing capabilities. See `TECH-SPEC.MD` for the complete technical specification of the planned features.

**Current Stack:**
- Flask 3.0.0 (with Blueprint pattern)
- Python 3.12+
- Jinja2 templates
- Bootstrap 5 (for styling)

**Planned Stack (from TECH-SPEC.MD):**
- SQLAlchemy (ORM) + SQLite
- Flask-Login (authentication)
- Quill.js (rich-text editor)
- Flask-WTF (forms & CSRF protection)

## Development Commands

### First-time Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# With activated venv
python run.py

# Or directly
./venv/Scripts/python.exe run.py  # Windows
./venv/bin/python run.py          # macOS/Linux
```

The app runs on `http://localhost:5000` in debug mode.

## Architecture

### Application Factory Pattern
The app uses Flask's application factory pattern in `app/__init__.py`:
- `create_app()` function initializes and configures the Flask app
- Blueprints are registered within the factory
- Allows for multiple app instances with different configs (testing, production, etc.)

### Blueprint Pattern
Routes are organized using Flask Blueprints (`app/routes.py`):
- Main blueprint named `'main'` handles primary routes
- Blueprint endpoints are prefixed: `'main.index'`, `'main.about'`
- In templates, use `url_for('main.route_name')` not `url_for('route_name')`

**Example:**
```python
# app/routes.py
from flask import Blueprint
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')
```

### Template Structure
- `base.html`: Base template with navigation, includes Bootstrap 5
- Child templates extend base using `{% extends "base.html" %}`
- Navigation links must use blueprint-prefixed endpoints

## Important Conventions

### Adding New Routes
1. Define routes in `app/routes.py` using the `@bp.route()` decorator
2. Update navigation in `app/templates/base.html` if needed
3. Remember to use `url_for('main.route_name')` in templates

### Future Database Work (TECH-SPEC.MD)
When implementing the note-taking features:
- Models will be in `app/models.py`
- Use `extensions.py` for shared extensions (db, login_manager, etc.)
- Organize features into blueprints: `app/auth/` and `app/notes/`
- Use SQLAlchemy with `datetime.utcnow` for timestamp defaults
- Store Quill Delta JSON as Text in SQLite

### Security Requirements (from TECH-SPEC.MD)
- Password hashing via Werkzeug
- CSRF protection on all state-changing requests
- Secure session cookies in production
- No raw HTML injection from user input

## Project Structure Evolution

**Current:**
```
app/
  __init__.py       # Application factory
  routes.py         # Blueprint with routes
  templates/        # Jinja2 templates
  static/           # CSS, JS, images
```

**Planned (per TECH-SPEC.MD):**
```
app/
  __init__.py
  config.py
  extensions.py     # db, login_manager, csrf
  models.py         # User, Note models
  auth/
    routes.py
    forms.py
  notes/
    routes.py
    forms.py
    services.py     # Business logic
  templates/
    base.html
    auth/
    notes/
  static/
migrations/         # Alembic/Flask-Migrate
tests/
```

## Virtual Environment

The `venv/` directory contains the Python virtual environment and should:
- Never be committed (already in `.gitignore`)
- Be recreated from `requirements.txt` on new machines
- Be activated before running any Python commands

## Git Workflow

Current branches:
- `master`: Main development branch
- `tech_spec_definition`: Branch with technical specification
- `initialize_claude_project`: Feature branch for initial setup

When adding dependencies, update `requirements.txt`:
```bash
pip freeze > requirements.txt
```

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Keep your replies extremly concice and focus on conveying the key information. No unnecessary fluff, no long code snippets.

Whenever working with any third-party library or something similar, you MUST look up the official documentation to ensure that you’re working with up-to-date information.

Use the DocsExplorer subagent for efficient documentation lookup.

## Project Overview

A Flask note-taking application with user authentication, CRUD notes, and public sharing via unique tokens.

**Current Stack:**
- Flask 3.0.0 (with Blueprint pattern)
- Python 3.12+
- SQLAlchemy + SQLite (`notes.db`)
- Flask-Login (session-based authentication)
- Flask-WTF + CSRFProtect (forms & CSRF protection)
- Bootstrap 5 + Bootstrap Icons (UI)
- Jinja2 templates

**Not yet implemented:**
- Quill.js (rich-text editor) — currently using plain textarea
- Flask-Migrate / Alembic (migrations)

**Known issues:** See [AUDIT.md](AUDIT.md) for the full list of security and correctness issues pending resolution.

## Development Commands

### First-time Setup
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### Running the Application
```bash
python run.py
```
The app runs on `http://localhost:5000` in debug mode.

### Running Tests
```bash
python -m pytest tests/ -v
```
Tests use in-memory SQLite and disabled CSRF. Shared fixtures are in `tests/conftest.py`.

### Docker
```bash
docker-compose up --build
```
- Flask app: `http://localhost:5000`
- SQLite Web UI: `http://localhost:8080` (password-protected, see `.env`)

## Architecture

### Application Factory (`app/__init__.py`)
- `create_app()` initializes Flask, registers extensions (`db`, `login_manager`, `csrf`), and registers all blueprints

### Blueprints
| Blueprint | Prefix | Purpose |
|-----------|--------|---------|
| `main` | `/` | Home, About pages |
| `auth` | `/auth` | Login, Register, Logout |
| `notes` | `/notes` | CRUD notes, sharing |
| `users` | `/users` | User management |

In templates, always use `url_for('blueprint.route_name')`.

### Extensions (`app/extensions.py`)
- `db` — SQLAlchemy instance
- `login_manager` — Flask-Login, `login_view="auth.login"`
- `csrf` — CSRFProtect (all POST forms require CSRF token)

### Authentication
- All routes require `@login_required` except `auth.login`, `auth.register`, and `notes.public_note`
- Auth forms use WTForms (`app/auth/forms.py`: `LoginForm`, `RegisterForm`)
- `UserService.authenticate()` handles credential validation
- Unauthenticated users are redirected to `/auth/login`

### CSRF Protection
Every POST form must include:
```html
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```
Or for WTForms: `{{ form.hidden_tag() }}`

## Project Structure

```
app/
  __init__.py          # Application factory
  extensions.py        # db, login_manager, csrf
  routes.py            # 'main' blueprint (Home, About)
  auth/
    __init__.py        # 'auth' blueprint definition
    routes.py          # login, register, logout
    forms.py           # LoginForm, RegisterForm
  models/
    __init__.py        # Re-exports User, Note
    user.py            # User model (UserMixin)
    note.py            # Note model
  notes/
    __init__.py        # 'notes' blueprint definition
    routes.py          # CRUD + share/unshare + public view
    services.py        # NoteService business logic
  users/
    __init__.py        # 'users' blueprint definition
    routes.py          # User management routes
  services/
    __init__.py        # Services package
    user_service.py    # UserService (create, authenticate, etc.)
  templates/
    base.html          # Bootstrap 5 layout, nav, flash messages
    index.html         # Home page
    about.html         # About page
    auth/              # login.html, register.html
    notes/             # list, new, edit, view, public
    users/             # list, new, view, password
  static/
    css/style.css      # Minimal custom CSS (Bootstrap handles most)
run.py                   # Entry point (python run.py)
requirements.txt         # Pinned dependencies
docker-compose.yml
Dockerfile
README.md
README.docker.md
AUDIT.md                 # Codebase audit findings and pending fixes
TECH-SPEC.MD             # Technical specification
.env                     # SQLite Web password (gitignored)
.gitignore
```

## Important Conventions

### Adding New Routes
1. Define in the appropriate blueprint's `routes.py`
2. Add `@login_required` decorator (unless public)
3. Include CSRF token in any POST forms
4. Use `url_for('blueprint.route_name')` in templates

### Models
- `User` (`app/models/user.py`): email, password_hash, timestamps, `set_password()`/`check_password()`
- `Note` (`app/models/note.py`): user_id FK, title, content_delta (JSON), is_shared, share_token, timestamps

### Security
- Password hashing via Werkzeug
- CSRF protection on all state-changing requests
- `@login_required` on all non-public routes
- Note ownership enforced via `_get_own_note_or_404()` in `app/notes/routes.py`
- User routes restricted to own profile via `_ensure_own_user()` in `app/users/routes.py`

## Virtual Environment

The `venv/` directory should:
- Never be committed (in `.gitignore`)
- Be recreated from `requirements.txt` on new machines

## Git Workflow

### Pre-commit Agents (MANDATORY)
Before every `git commit` or `git push`, you MUST invoke both agents using the Task tool:
1. **TestUpdate** (`subagent_type: TestUpdate`) — updates/adds tests to match code changes
2. **UpdateProjectDocs** (`subagent_type: UpdateProjectDocs`) — updates README.md, CLAUDE.md, AUDIT.md, TECH-SPEC.MD

Run both agents **in parallel** before staging and committing. Do NOT skip this step.

The PreToolUse hook will also run `pytest` as a final gate — if tests fail, the commit is blocked.

### Adding Dependencies
```bash
pip freeze > requirements.txt
```

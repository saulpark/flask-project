# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Keep your replies extremly concice and focus on conveying the key information. No unnecessary fluff, no long code snippets.

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
docker-compose.yml
Dockerfile
.env                   # SQLite Web password (gitignored)
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
- Notes routes use `current_user.id` (not hardcoded)

## Virtual Environment

The `venv/` directory should:
- Never be committed (in `.gitignore`)
- Be recreated from `requirements.txt` on new machines

## Git Workflow

When adding dependencies:
```bash
pip freeze > requirements.txt
```

# Flask Note-Taking Application

A Flask web application for creating and managing notes with user authentication, public sharing via unique tokens, and a Bootstrap 5 UI.

## Project Structure

```
flask-project/
├── app/
│   ├── __init__.py              # Application factory
│   ├── extensions.py            # db, login_manager, csrf instances
│   ├── routes.py                # Main blueprint (Home, About)
│   ├── auth/
│   │   ├── __init__.py          # Auth blueprint definition
│   │   ├── routes.py            # Login, register, logout
│   │   └── forms.py             # LoginForm, RegisterForm (WTForms)
│   ├── models/
│   │   ├── __init__.py          # Re-exports User, Note
│   │   ├── user.py              # User model with authentication
│   │   └── note.py              # Note model with sharing
│   ├── notes/
│   │   ├── __init__.py          # Notes blueprint definition
│   │   ├── routes.py            # CRUD + share/unshare + public view
│   │   └── services.py          # NoteService business logic
│   ├── users/
│   │   ├── __init__.py          # Users blueprint definition
│   │   └── routes.py            # User management routes
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py      # UserService (create, authenticate, etc.)
│   ├── templates/
│   │   ├── base.html            # Bootstrap 5 layout, nav, flash messages
│   │   ├── index.html           # Home page
│   │   ├── about.html           # About page
│   │   ├── auth/                # login.html, register.html
│   │   ├── notes/               # list, new, edit, view, public
│   │   └── users/               # list, new, view, password
│   └── static/
│       └── css/style.css        # Minimal custom CSS
├── tests/
│   ├── __init__.py
│   ├── test_user_service.py     # User service tests
│   └── test_notes_service.py    # Notes service tests
├── instance/                    # SQLite database location
├── run.py                       # Application entry point
├── requirements.txt             # Pinned Python dependencies
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example                 # Environment variables template
├── .gitignore
├── CLAUDE.md                    # AI assistant guidance
├── TECH-SPEC.MD                 # Technical specification
├── AUDIT.md                     # Codebase audit findings
└── README.docker.md             # Docker-specific documentation
```

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables (optional)

```bash
copy .env.example .env
```

### 4. Run the application

```bash
python run.py
```

The app runs at `http://localhost:5000` in debug mode.

### 5. Initialize the database

Tables are not yet auto-created. Run manually:

```python
python
>>> from app import create_app
>>> from app.extensions import db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

## Features

- **User authentication** — email/password login with session-based auth (Flask-Login)
- **Notes CRUD** — create, view, edit, delete notes
- **Public sharing** — share notes via unique token URLs, toggle on/off
- **CSRF protection** — all POST forms protected via Flask-WTF CSRFProtect
- **Bootstrap 5 UI** — responsive layout with Bootstrap Icons
- **Service layer architecture** — business logic separated from routes
- **Docker support** — with SQLite Web UI for database inspection

## Current Limitations

See [AUDIT.md](AUDIT.md) for the full list. Key items:

- Note ownership is not enforced (any user can access any note)
- Users blueprint has no authorization (any user can manage all users)
- Quill.js rich-text editor not yet integrated (using plain textarea)
- Flask-Migrate not yet wired up
- `SECRET_KEY` is hardcoded (not env-based)

## Docker

```bash
# Start both Flask app and SQLite Web UI
docker-compose up

# Run in background
docker-compose up -d

# Stop
docker-compose down
```

- Flask App: `http://localhost:5000`
- SQLite Web UI: `http://localhost:8080`

See [README.docker.md](README.docker.md) for more Docker details.

## Testing

```bash
pytest
pytest --cov=app
pytest tests/test_user_service.py
```

## Tech Spec

See [TECH-SPEC.MD](TECH-SPEC.MD) for the full technical specification and milestone tracking.

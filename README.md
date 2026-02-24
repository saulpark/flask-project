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
├── AUDIT_LOG.md                 # Audit issue history (opened/resolved dates)
├── README.docker.md             # Docker-specific documentation
└── .claude/
    ├── commands/
    │   └── CodeReview.md        # /CodeReview slash command
    └── hooks/
        └── pre-git.sh           # Pre-commit hook: runs pytest gate
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

### 5. Database

Tables are created automatically when the app starts via `db.create_all()` in the application factory.

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

- `SECRET_KEY` and `DATABASE_URL` are hardcoded — not env-based (AUDIT #4, #21)
- No rate limiting on the login endpoint — brute-force possible (AUDIT #18)
- Cookie security flags not configured for production (AUDIT #19)
- Quill.js rich-text editor not yet integrated (using plain textarea)
- Flask-Migrate not yet wired up

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

### Development Workflow

Before committing changes, the project uses automated agents to maintain code quality and documentation:

1. **TestUpdate agent** — automatically creates or updates tests to match code changes
2. **UpdateProjectDocs agent** — updates README.md, CLAUDE.md, AUDIT.md, and TECH-SPEC.MD as needed

These agents run automatically via a PreToolUse hook before git operations (commit/push). The hook also runs pytest as a final gate — commits are blocked if tests fail.

A `/CodeReview` slash command is also available for on-demand code reviews. Results are written to `AUDIT.md` and `AUDIT_LOG.md`. Optional `MODE` values: `BUGS`, `SECURITY`, `PERFORMANCE`, or combinations like `BUGS,SECURITY`.

See [CLAUDE.md](CLAUDE.md) Git Workflow section for details.

## Tech Spec

See [TECH-SPEC.MD](TECH-SPEC.MD) for the full technical specification and milestone tracking.

# Flask Note-Taking Application

A Flask web application with SQLAlchemy models, service layer architecture, and comprehensive testing. Features user management and note-taking capabilities with rich-text support (planned).

## Project Structure

```
flask-project/
├── app/
│   ├── __init__.py              # Application factory
│   ├── extensions.py            # Database and extension instances
│   ├── routes.py                # Main blueprint routes
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User model with authentication
│   │   └── note.py              # Note model with sharing
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py      # User CRUD operations
│   ├── notes/
│   │   ├── __init__.py
│   │   ├── routes.py            # Note routes (planned)
│   │   └── services.py          # Note CRUD operations
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Stylesheets
│   │   └── js/                  # JavaScript files
│   └── templates/
│       ├── base.html            # Base template
│       ├── index.html           # Home page
│       └── about.html           # About page
├── tests/
│   ├── test_user_service.py     # User service tests
│   └── test_notes_service.py    # Notes service tests
├── instance/                    # SQLite database location
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker container definition
├── docker-compose.yml           # Multi-container Docker setup
├── .dockerignore               # Docker ignore rules
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── CLAUDE.md                   # AI assistant guidance
└── TECH-SPEC.MD                # Technical specification
```

## Setup Instructions

### 1. Create a Virtual Environment

```bash
python -m venv venv
```

### 2. Activate the Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables (Optional)

Copy the example environment file and update it with your settings:

```bash
copy .env.example .env
```

### 5. Run the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

### 6. Initialize the Database

```bash
# Create database tables
flask db upgrade
# Or run Python and create tables manually
python
>>> from app import create_app
>>> from app.extensions import db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

## Features

- **Application factory pattern** for better organization
- **SQLAlchemy ORM** with User and Note models
- **Service layer architecture** for business logic separation
- **User authentication** with password hashing (Werkzeug)
- **Note management** with sharing capabilities via tokens
- **Comprehensive testing** with pytest and pytest-mock
- **Database migrations** support (Flask-Migrate)
- **Template inheritance** with Jinja2
- **Static files support** (CSS, JavaScript)
- **Docker support** with SQLite Web UI (sqlite-web)
- Clean, modular project structure

## Docker Usage

### Quick Start with Docker Compose (Recommended)

```bash
# Start both Flask app and SQLite Web UI
docker-compose up

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

**Access:**
- Flask App: `http://localhost:5000`
- SQLite Web UI: `http://localhost:8080`

### Build and Run with Docker (Manual)

```bash
# Build the image
docker build -t flask-notes-app .

# Run the Flask container
docker run -p 5000:5000 -v $(pwd)/instance:/app/instance flask-notes-app

# Run sqlite-web in a separate container
docker run -p 8080:8080 -v $(pwd)/instance:/app/instance flask-notes-app \
  sqlite_web --host 0.0.0.0 --port 8080 instance/app.db
```

### SQLite Web UI Features

The SQLite Web UI (port 8080) provides:
- Browse tables and view data
- Execute SQL queries with syntax highlighting
- Export data to CSV/JSON
- View table schemas and indexes
- Read-only mode available for safety

## Database Models

### User Model
- Email-based authentication with password hashing
- One-to-many relationship with notes
- Timestamps for created_at and updated_at

### Note Model
- Title and content (Quill Delta JSON format)
- Sharing functionality with unique tokens
- Foreign key relationship to User
- Timestamps for created_at and updated_at

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_user_service.py
```

## Development

- **Routes**: Edit in [app/routes.py](app/routes.py) or blueprint-specific routes
- **Models**: Add/modify in [app/models/](app/models/)
- **Services**: Business logic in [app/services/](app/services/) and [app/notes/services.py](app/notes/services.py)
- **Templates**: Add in [app/templates/](app/templates/)
- **Static files**: CSS, JS, images in [app/static/](app/static/)
- **Configuration**: App factory in [app/__init__.py](app/__init__.py)

## Service Layer

The application uses a service layer pattern for business logic:

- **UserService** (`app/services/user_service.py`): User CRUD operations
- **NotesService** (`app/notes/services.py`): Note CRUD operations with sharing

## Next Steps

- [ ] Implement authentication routes and forms
- [ ] Add Quill.js rich-text editor integration
- [ ] Create note management UI
- [ ] Add public note sharing views
- [ ] Implement CSRF protection with Flask-WTF
- [ ] Add production configuration

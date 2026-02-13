# Flask Project

A simple Flask web application with a clean structure and ready-to-use templates.

## Project Structure

```
flask-project/
├── app/
│   ├── __init__.py          # Application factory
│   ├── routes.py            # Route definitions
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Stylesheets
│   │   └── js/              # JavaScript files
│   └── templates/
│       ├── base.html        # Base template
│       ├── index.html       # Home page
│       └── about.html       # About page
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── .gitignore              # Git ignore rules
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

## Features

- Application factory pattern for better organization
- Template inheritance with Jinja2
- Static files support (CSS, JavaScript)
- Basic routing examples
- Environment configuration support
- Clean project structure

## Development

- Edit routes in [app/routes.py](app/routes.py)
- Add templates in [app/templates/](app/templates/)
- Add static files (CSS, JS, images) in [app/static/](app/static/)
- Configure the app in [app/__init__.py](app/__init__.py)

## Next Steps

- Add a database (SQLAlchemy)
- Implement user authentication
- Add forms with Flask-WTF
- Set up blueprints for larger applications
- Add testing with pytest

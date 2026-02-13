# Docker Setup

## Quick Start

### Build and run with Docker Compose
```bash
docker-compose up --build
```

The app will be available at http://localhost:5000

### Stop the application
```bash
docker-compose down
```

## Commands

### Build the image
```bash
docker-compose build
```

### Run in detached mode
```bash
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f
```

### Create a test user
```bash
docker-compose exec web python -c "from app import create_app; from app.extensions import db; from app.services.user_service import UserService; app = create_app(); app.app_context().push(); user = UserService.create_user('test@example.com', 'password123'); print(f'User created! ID: {user.id}')"
```

### Access container shell
```bash
docker-compose exec web bash
```

### Run tests in container
```bash
docker-compose exec web pytest tests/ -v
```

## Database Persistence

The SQLite database is stored in `./instance/notes.db` and persists between container restarts.

To reset the database:
```bash
rm -f instance/notes.db
docker-compose restart
```

## Environment Variables

Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

## Production Notes

For production:
1. Set a strong `SECRET_KEY` in `.env`
2. Set `FLASK_ENV=production`
3. Consider PostgreSQL instead of SQLite
4. Use reverse proxy (nginx)
5. Enable HTTPS

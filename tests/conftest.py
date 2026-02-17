import pytest
from app import create_app
from app.extensions import db as _db
from app.models import User, Note


@pytest.fixture
def app():
    """Create a test Flask application with in-memory SQLite."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'WTF_CSRF_ENABLED': False,
        'SERVER_NAME': 'localhost',
    })

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.rollback()
        _db.drop_all()


@pytest.fixture
def db(app):
    """Provide the database session."""
    return _db


@pytest.fixture
def client(app):
    """Provide a Flask test client."""
    return app.test_client()


@pytest.fixture
def user(app, db):
    """Create a test user and return it."""
    u = User(email='test@example.com')
    u.set_password('password123')
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def other_user(app, db):
    """Create a second test user."""
    u = User(email='other@example.com')
    u.set_password('password123')
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def note(app, db, user):
    """Create a test note owned by `user`."""
    n = Note(
        user_id=user.id,
        title='Test Note',
        content_delta='{"ops":[{"insert":"Hello\\n"}]}',
    )
    db.session.add(n)
    db.session.commit()
    return n


@pytest.fixture
def auth_client(client, user):
    """Return a test client logged in as `user`."""
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123',
    })
    return client

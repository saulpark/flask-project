from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    from app.extensions import db, login_manager, csrf
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.routes import bp
    app.register_blueprint(bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.notes import bp as notes_bp
    app.register_blueprint(notes_bp)

    from app.users import bp as users_bp
    app.register_blueprint(users_bp)

    return app

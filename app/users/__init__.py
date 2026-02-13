from flask import Blueprint

bp = Blueprint('users', __name__, url_prefix='/users')

# Import routes at the end to avoid circular imports
from app.users import routes  # noqa: F401, E402

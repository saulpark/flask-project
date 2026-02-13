import pytest
from unittest.mock import MagicMock, patch
from app import create_app
from app.services.user_service import UserService
from app.models import User


@pytest.fixture
def app():
    """Create and configure a test Flask application"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def app_context(app):
    """Create an application context for tests"""
    with app.app_context():
        yield app


class TestUserService:
    """Unit tests for UserService with mocked database"""

    def test_create_user_success(self, app_context):
        """Test successful user creation"""
        with patch('app.services.user_service.db.session') as mock_session, \
             patch('app.services.user_service.UserService.get_user_by_email', return_value=None):

            email = "test@example.com"
            password = "password123"

            result = UserService.create_user(email, password)

            assert mock_session.add.called
            assert mock_session.commit.called
            assert result.email == email

    def test_create_user_duplicate_email(self, app_context):
        """Test creating user with existing email raises error"""
        with patch('app.services.user_service.UserService.get_user_by_email') as mock_get:
            mock_user = MagicMock(spec=User)
            mock_get.return_value = mock_user

            with pytest.raises(ValueError, match="Email already registered"):
                UserService.create_user("existing@example.com", "password")

    def test_create_user_invalid_email(self, app_context):
        """Test creating user with invalid email raises error"""
        with patch('app.services.user_service.UserService.get_user_by_email', return_value=None):
            with pytest.raises(ValueError, match="Invalid email format"):
                UserService.create_user("invalid-email", "password")

    def test_create_user_short_password(self, app_context):
        """Test creating user with short password raises error"""
        with patch('app.services.user_service.UserService.get_user_by_email', return_value=None):
            with pytest.raises(ValueError, match="Password must be at least 6 characters"):
                UserService.create_user("test@example.com", "12345")

    def test_get_user_by_id_found(self, app_context):
        """Test retrieving existing user by ID"""
        with patch('app.services.user_service.db.session') as mock_session:
            mock_user = MagicMock(spec=User)
            mock_user.id = 1
            mock_user.email = "test@example.com"
            mock_session.get.return_value = mock_user

            result = UserService.get_user_by_id(1)

            assert result == mock_user
            mock_session.get.assert_called_once_with(User, 1)

    def test_get_user_by_id_not_found(self, app_context):
        """Test retrieving non-existent user returns None"""
        with patch('app.services.user_service.db.session') as mock_session:
            mock_session.get.return_value = None

            result = UserService.get_user_by_id(999)

            assert result is None

    def test_get_user_by_email_found(self, app_context):
        """Test retrieving user by email"""
        with patch('app.models.User.query') as mock_query:
            mock_user = MagicMock(spec=User)
            mock_user.email = "test@example.com"

            mock_filter = MagicMock()
            mock_query.filter_by.return_value = mock_filter
            mock_filter.first.return_value = mock_user

            result = UserService.get_user_by_email("test@example.com")

            assert result == mock_user
            mock_query.filter_by.assert_called_once_with(email="test@example.com")

    def test_get_user_by_email_not_found(self, app_context):
        """Test retrieving non-existent email returns None"""
        with patch('app.models.User.query') as mock_query:
            mock_filter = MagicMock()
            mock_query.filter_by.return_value = mock_filter
            mock_filter.first.return_value = None

            result = UserService.get_user_by_email("nonexistent@example.com")

            assert result is None

    def test_authenticate_success(self, app_context):
        """Test successful authentication"""
        with patch('app.services.user_service.UserService.get_user_by_email') as mock_get:
            mock_user = MagicMock(spec=User)
            mock_user.check_password.return_value = True
            mock_get.return_value = mock_user

            result = UserService.authenticate("test@example.com", "correct_password")

            assert result == mock_user
            mock_user.check_password.assert_called_once_with("correct_password")

    def test_authenticate_wrong_password(self, app_context):
        """Test authentication with wrong password"""
        with patch('app.services.user_service.UserService.get_user_by_email') as mock_get:
            mock_user = MagicMock(spec=User)
            mock_user.check_password.return_value = False
            mock_get.return_value = mock_user

            result = UserService.authenticate("test@example.com", "wrong_password")

            assert result is None

    def test_authenticate_user_not_found(self, app_context):
        """Test authentication with non-existent user"""
        with patch('app.services.user_service.UserService.get_user_by_email', return_value=None):
            result = UserService.authenticate("nonexistent@example.com", "password")

            assert result is None

    def test_update_password_success(self, app_context):
        """Test successful password update"""
        with patch('app.services.user_service.db.session') as mock_session, \
             patch('app.services.user_service.UserService.get_user_by_id') as mock_get:

            mock_user = MagicMock(spec=User)
            mock_user.check_password.return_value = True
            mock_get.return_value = mock_user

            result = UserService.update_password(1, "old_pass", "new_password123")

            assert result is True
            mock_user.set_password.assert_called_once_with("new_password123")
            assert mock_session.commit.called

    def test_update_password_user_not_found(self, app_context):
        """Test updating password for non-existent user"""
        with patch('app.services.user_service.UserService.get_user_by_id', return_value=None):
            with pytest.raises(ValueError, match="User not found"):
                UserService.update_password(999, "old_pass", "new_pass")

    def test_update_password_wrong_old_password(self, app_context):
        """Test updating password with incorrect old password"""
        with patch('app.services.user_service.UserService.get_user_by_id') as mock_get:
            mock_user = MagicMock(spec=User)
            mock_user.check_password.return_value = False
            mock_get.return_value = mock_user

            with pytest.raises(ValueError, match="Current password is incorrect"):
                UserService.update_password(1, "wrong_old", "new_pass")

    def test_update_password_invalid_new_password(self, app_context):
        """Test updating with invalid new password"""
        with patch('app.services.user_service.UserService.get_user_by_id') as mock_get:
            mock_user = MagicMock(spec=User)
            mock_user.check_password.return_value = True
            mock_get.return_value = mock_user

            with pytest.raises(ValueError, match="New password must be at least 6 characters"):
                UserService.update_password(1, "old_pass", "short")

    def test_delete_user_success(self, app_context):
        """Test successful user deletion"""
        with patch('app.services.user_service.db.session') as mock_session, \
             patch('app.services.user_service.UserService.get_user_by_id') as mock_get:

            mock_user = MagicMock(spec=User)
            mock_get.return_value = mock_user

            result = UserService.delete_user(1)

            assert result is True
            mock_session.delete.assert_called_once_with(mock_user)
            assert mock_session.commit.called

    def test_delete_user_not_found(self, app_context):
        """Test deleting non-existent user"""
        with patch('app.services.user_service.UserService.get_user_by_id', return_value=None):
            with pytest.raises(ValueError, match="User not found"):
                UserService.delete_user(999)

    def test_get_all_users(self, app_context):
        """Test retrieving all users"""
        with patch('app.models.User.query') as mock_query:
            mock_user1 = MagicMock(spec=User)
            mock_user2 = MagicMock(spec=User)
            mock_order = MagicMock()

            mock_query.order_by.return_value = mock_order
            mock_order.all.return_value = [mock_user1, mock_user2]

            result = UserService.get_all_users()

            assert len(result) == 2
            assert result[0] == mock_user1
            assert result[1] == mock_user2

import pytest
from unittest.mock import MagicMock, patch
from app import create_app
from app.notes.services import NoteService
from app.models import Note


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


class TestNoteService:
    """Unit tests for NoteService with mocked database"""

    def test_create_note_success(self, app_context):
        """Test successful note creation"""
        with patch('app.notes.services.db.session') as mock_session:
            # Setup
            user_id = 1
            title = "Test Note"
            content = '{"ops":[{"insert":"Hello\\n"}]}'

            # Execute
            result = NoteService.create_note(user_id, title, content)

            # Verify
            assert mock_session.add.called
            assert mock_session.commit.called
            assert result.user_id == user_id
            assert result.title == title
            assert result.content_delta == content

    def test_create_note_invalid_json(self, app_context):
        """Test validation for invalid JSON content"""
        with patch('app.notes.services.db.session'):
            # Invalid JSON
            invalid_content = "not a valid json"

            with pytest.raises(ValueError, match="Invalid JSON content"):
                NoteService.create_note(1, "Title", invalid_content)

    def test_create_note_content_too_large(self, app_context):
        """Test validation for content exceeding max size"""
        with patch('app.notes.services.db.session'):
            # Create content larger than 2 MB
            large_content = '{"ops":[{"insert":"' + ('x' * (3 * 1024 * 1024)) + '"}]}'

            with pytest.raises(ValueError, match="Content exceeds maximum size"):
                NoteService.create_note(1, "Title", large_content)

    def test_get_note_by_id_found(self, app_context):
        """Test retrieving existing note"""
        with patch('app.notes.services.db.session') as mock_session:
            # Setup mock
            mock_note = MagicMock(spec=Note)
            mock_note.id = 1
            mock_note.title = "Test"
            mock_session.get.return_value = mock_note

            # Execute
            result = NoteService.get_note_by_id(1)

            # Verify
            assert result == mock_note
            mock_session.get.assert_called_once_with(Note, 1)

    def test_get_note_by_id_not_found(self, app_context):
        """Test retrieving non-existent note returns None"""
        with patch('app.notes.services.db.session') as mock_session:
            mock_session.get.return_value = None

            result = NoteService.get_note_by_id(999)

            assert result is None

    def test_get_all_notes(self, app_context):
        """Test retrieving all notes for a user"""
        with patch('app.models.Note.query') as mock_query:
            # Setup mocks
            mock_note1 = MagicMock(spec=Note)
            mock_note2 = MagicMock(spec=Note)
            mock_filter = MagicMock()
            mock_order = MagicMock()

            mock_query.filter_by.return_value = mock_filter
            mock_filter.order_by.return_value = mock_order
            mock_order.all.return_value = [mock_note1, mock_note2]

            # Execute
            result = NoteService.get_all_notes(1)

            # Verify
            assert len(result) == 2
            mock_query.filter_by.assert_called_once_with(user_id=1)

    def test_update_note_success(self, app_context):
        """Test successful note update"""
        with patch('app.notes.services.db.session') as mock_session:
            # Setup
            mock_note = MagicMock(spec=Note)
            mock_note.id = 1
            mock_session.get.return_value = mock_note

            new_title = "Updated Title"
            new_content = '{"ops":[{"insert":"Updated\\n"}]}'

            # Execute
            result = NoteService.update_note(1, new_title, new_content)

            # Verify
            assert result.title == new_title
            assert result.content_delta == new_content
            assert mock_session.commit.called

    def test_update_note_not_found(self, app_context):
        """Test updating non-existent note raises error"""
        with patch('app.notes.services.db.session') as mock_session:
            mock_session.get.return_value = None

            with pytest.raises(ValueError, match="Note not found"):
                NoteService.update_note(999, "Title", '{"ops":[]}')

    def test_update_note_invalid_json(self, app_context):
        """Test updating with invalid JSON raises error"""
        with patch('app.notes.services.db.session') as mock_session:
            mock_note = MagicMock(spec=Note)
            mock_session.get.return_value = mock_note

            with pytest.raises(ValueError, match="Invalid JSON content"):
                NoteService.update_note(1, "Title", "invalid json")

    def test_delete_note_success(self, app_context):
        """Test successful deletion"""
        with patch('app.notes.services.db.session') as mock_session:
            mock_note = MagicMock(spec=Note)
            mock_session.get.return_value = mock_note

            result = NoteService.delete_note(1)

            assert result is True
            mock_session.delete.assert_called_once_with(mock_note)
            assert mock_session.commit.called

    def test_delete_note_not_found(self, app_context):
        """Test deleting non-existent note raises error"""
        with patch('app.notes.services.db.session') as mock_session:
            mock_session.get.return_value = None

            with pytest.raises(ValueError, match="Note not found"):
                NoteService.delete_note(999)

    def test_share_note_generates_token(self, app_context):
        """Test share creates unique token"""
        with patch('app.notes.services.db.session') as mock_session:
            mock_note = MagicMock(spec=Note)
            mock_note.is_shared = False
            mock_note.share_token = None
            mock_session.get.return_value = mock_note

            token = NoteService.share_note(1)

            assert token is not None
            assert len(token) > 0
            assert mock_note.is_shared is True
            assert mock_note.share_token == token
            assert mock_session.commit.called

    def test_share_note_not_found(self, app_context):
        """Test sharing non-existent note raises error"""
        with patch('app.notes.services.db.session') as mock_session:
            mock_session.get.return_value = None

            with pytest.raises(ValueError, match="Note not found"):
                NoteService.share_note(999)

    def test_unshare_note_clears_token(self, app_context):
        """Test unshare disables sharing"""
        with patch('app.notes.services.db.session') as mock_session:
            mock_note = MagicMock(spec=Note)
            mock_note.is_shared = True
            mock_note.share_token = "some_token"
            mock_session.get.return_value = mock_note

            result = NoteService.unshare_note(1)

            assert result is True
            assert mock_note.is_shared is False
            assert mock_note.share_token is None
            assert mock_session.commit.called

    def test_unshare_note_not_found(self, app_context):
        """Test unsharing non-existent note raises error"""
        with patch('app.notes.services.db.session') as mock_session:
            mock_session.get.return_value = None

            with pytest.raises(ValueError, match="Note not found"):
                NoteService.unshare_note(999)

    def test_get_note_by_token_valid(self, app_context):
        """Test public access with valid token"""
        with patch('app.models.Note.query') as mock_query:
            mock_note = MagicMock(spec=Note)
            mock_note.is_shared = True
            mock_note.share_token = "valid_token"

            mock_filter = MagicMock()
            mock_query.filter_by.return_value = mock_filter
            mock_filter.first.return_value = mock_note

            result = NoteService.get_note_by_token("valid_token")

            assert result == mock_note
            mock_query.filter_by.assert_called_once_with(
                share_token="valid_token",
                is_shared=True
            )

    def test_get_note_by_token_invalid(self, app_context):
        """Test public access with invalid token returns None"""
        with patch('app.models.Note.query') as mock_query:
            mock_filter = MagicMock()
            mock_query.filter_by.return_value = mock_filter
            mock_filter.first.return_value = None

            result = NoteService.get_note_by_token("invalid_token")

            assert result is None

    def test_get_note_by_token_not_shared(self, app_context):
        """Test accessing unshared note by token returns None"""
        with patch('app.models.Note.query') as mock_query:
            mock_filter = MagicMock()
            mock_query.filter_by.return_value = mock_filter
            mock_filter.first.return_value = None

            result = NoteService.get_note_by_token("token_of_unshared_note")

            assert result is None

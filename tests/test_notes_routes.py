class TestNoteOwnership:
    """Tests that users can only access their own notes."""

    def test_view_own_note(self, auth_client, note):
        resp = auth_client.get(f'/notes/{note.id}')
        assert resp.status_code == 200

    def test_view_other_users_note_returns_403(self, auth_client, db, other_user):
        from app.models import Note
        other_note = Note(
            user_id=other_user.id,
            title='Other Note',
            content_delta='{"ops":[{"insert":"secret\\n"}]}',
        )
        db.session.add(other_note)
        db.session.commit()

        resp = auth_client.get(f'/notes/{other_note.id}')
        assert resp.status_code == 403

    def test_edit_other_users_note_returns_403(self, auth_client, db, other_user):
        from app.models import Note
        other_note = Note(
            user_id=other_user.id,
            title='Other Note',
            content_delta='{"ops":[{"insert":"secret\\n"}]}',
        )
        db.session.add(other_note)
        db.session.commit()

        resp = auth_client.get(f'/notes/{other_note.id}/edit')
        assert resp.status_code == 403

    def test_update_other_users_note_returns_403(self, auth_client, db, other_user):
        from app.models import Note
        other_note = Note(
            user_id=other_user.id,
            title='Other Note',
            content_delta='{"ops":[{"insert":"secret\\n"}]}',
        )
        db.session.add(other_note)
        db.session.commit()

        resp = auth_client.post(f'/notes/{other_note.id}', data={
            'title': 'Hacked',
            'content': 'pwned',
        })
        assert resp.status_code == 403

    def test_delete_other_users_note_returns_403(self, auth_client, db, other_user):
        from app.models import Note
        other_note = Note(
            user_id=other_user.id,
            title='Other Note',
            content_delta='{"ops":[{"insert":"secret\\n"}]}',
        )
        db.session.add(other_note)
        db.session.commit()

        resp = auth_client.post(f'/notes/{other_note.id}/delete')
        assert resp.status_code == 403

    def test_share_other_users_note_returns_403(self, auth_client, db, other_user):
        from app.models import Note
        other_note = Note(
            user_id=other_user.id,
            title='Other Note',
            content_delta='{"ops":[{"insert":"secret\\n"}]}',
        )
        db.session.add(other_note)
        db.session.commit()

        resp = auth_client.post(f'/notes/{other_note.id}/share')
        assert resp.status_code == 403

    def test_unshare_other_users_note_returns_403(self, auth_client, db, other_user):
        from app.models import Note
        other_note = Note(
            user_id=other_user.id,
            title='Other Note',
            content_delta='{"ops":[{"insert":"secret\\n"}]}',
        )
        db.session.add(other_note)
        db.session.commit()

        resp = auth_client.post(f'/notes/{other_note.id}/unshare')
        assert resp.status_code == 403

    def test_view_nonexistent_note_returns_404(self, auth_client):
        resp = auth_client.get('/notes/9999')
        assert resp.status_code == 404


class TestNoteCRUDRoutes:
    """Tests for note CRUD operations through routes."""

    def test_list_notes(self, auth_client, note):
        resp = auth_client.get('/notes/')
        assert resp.status_code == 200
        assert b'Test Note' in resp.data

    def test_new_note_form(self, auth_client):
        resp = auth_client.get('/notes/new')
        assert resp.status_code == 200

    def test_create_note(self, auth_client):
        resp = auth_client.post('/notes', data={
            'title': 'New Note',
            'content': 'Some content',
        }, follow_redirects=False)
        assert resp.status_code == 302

    def test_create_note_empty_content_rejected(self, auth_client):
        resp = auth_client.post('/notes', data={
            'title': 'Empty',
            'content': '',
        }, follow_redirects=True)
        assert b'Content is required' in resp.data

    def test_edit_note_form(self, auth_client, note):
        resp = auth_client.get(f'/notes/{note.id}/edit')
        assert resp.status_code == 200

    def test_update_note(self, auth_client, note):
        resp = auth_client.post(f'/notes/{note.id}', data={
            'title': 'Updated Title',
            'content': 'Updated content',
        }, follow_redirects=False)
        assert resp.status_code == 302

    def test_delete_note(self, auth_client, note):
        resp = auth_client.post(f'/notes/{note.id}/delete', follow_redirects=False)
        assert resp.status_code == 302

        # Verify note is gone
        resp = auth_client.get(f'/notes/{note.id}')
        assert resp.status_code == 404


class TestNoteShareRoutes:
    """Tests for note sharing/unsharing through routes."""

    def test_share_note_redirects(self, auth_client, note):
        resp = auth_client.post(f'/notes/{note.id}/share', follow_redirects=False)
        assert resp.status_code == 302

    def test_share_creates_public_link(self, auth_client, note):
        resp = auth_client.post(f'/notes/{note.id}/share', follow_redirects=True)
        assert b'Note shared!' in resp.data

    def test_public_note_accessible(self, client, db, note):
        from app.notes.services import NoteService
        token = NoteService.share_note(note.id)

        resp = client.get(f'/notes/p/{token}')
        assert resp.status_code == 200
        assert b'Test Note' in resp.data

    def test_public_note_invalid_token_404(self, client):
        resp = client.get('/notes/p/nonexistent_token')
        assert resp.status_code == 404

    def test_unshare_note(self, auth_client, note):
        # Share first
        auth_client.post(f'/notes/{note.id}/share')

        # Unshare
        resp = auth_client.post(f'/notes/{note.id}/unshare', follow_redirects=True)
        assert b'Note unshared' in resp.data

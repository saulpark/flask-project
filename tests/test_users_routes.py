class TestUserOwnership:
    """Tests that users can only access their own profile."""

    def test_view_own_profile(self, auth_client, user):
        resp = auth_client.get(f'/users/{user.id}')
        assert resp.status_code == 200
        assert b'test@example.com' in resp.data

    def test_view_other_user_returns_403(self, auth_client, other_user):
        resp = auth_client.get(f'/users/{other_user.id}')
        assert resp.status_code == 403

    def test_edit_password_own_user(self, auth_client, user):
        resp = auth_client.get(f'/users/{user.id}/password')
        assert resp.status_code == 200

    def test_edit_password_other_user_returns_403(self, auth_client, other_user):
        resp = auth_client.get(f'/users/{other_user.id}/password')
        assert resp.status_code == 403

    def test_update_password_other_user_returns_403(self, auth_client, other_user):
        resp = auth_client.post(f'/users/{other_user.id}/password', data={
            'old_password': 'password123',
            'new_password': 'newpass456',
            'confirm_password': 'newpass456',
        })
        assert resp.status_code == 403


class TestPasswordChange:
    """Tests for password change flow."""

    def test_change_password_success(self, auth_client, user):
        resp = auth_client.post(f'/users/{user.id}/password', data={
            'old_password': 'password123',
            'new_password': 'newpass456',
            'confirm_password': 'newpass456',
        }, follow_redirects=True)
        assert b'Password updated' in resp.data

    def test_change_password_wrong_old(self, auth_client, user):
        resp = auth_client.post(f'/users/{user.id}/password', data={
            'old_password': 'wrongpassword',
            'new_password': 'newpass456',
            'confirm_password': 'newpass456',
        }, follow_redirects=True)
        assert resp.status_code == 200
        assert b'Password updated' not in resp.data

    def test_change_password_mismatch(self, auth_client, user):
        resp = auth_client.post(f'/users/{user.id}/password', data={
            'old_password': 'password123',
            'new_password': 'newpass456',
            'confirm_password': 'different789',
        }, follow_redirects=True)
        assert b'do not match' in resp.data

    def test_change_password_empty_fields(self, auth_client, user):
        resp = auth_client.post(f'/users/{user.id}/password', data={
            'old_password': '',
            'new_password': '',
            'confirm_password': '',
        }, follow_redirects=True)
        assert b'required' in resp.data
